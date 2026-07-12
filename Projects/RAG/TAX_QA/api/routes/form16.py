"""
/analyze-form16 endpoint — upload and parse Form 16 PDF.
"""
import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from api.schemas import Form16Response

router = APIRouter()


@router.post("/analyze-form16", response_model=Form16Response)
async def analyze_form16(file: UploadFile = File(...)):
    """
    Upload a Form 16 PDF and extract structured tax information.
    Optionally runs full tax analysis on extracted data.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Save uploaded file to temp location
    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        from form16_parser.parser import extract_form16
        from tax_engine.calculator import calculate_full_tax

        form16_data = extract_form16(tmp_path)
        tax_profile = form16_data.to_tax_profile()

        # Run tax calculation if gross salary was extracted
        tax_analysis = None
        if form16_data.part_b.gross_salary and form16_data.part_b.gross_salary > 0:
            tax_analysis = calculate_full_tax(tax_profile)

        b = form16_data.part_b
        return Form16Response(
            extracted=form16_data.extraction_confidence > 0.1,
            gross_salary=b.gross_salary or 0,
            tds_deducted=b.tds_deducted or 0,
            taxable_income=b.taxable_income or 0,
            deductions={
                "sec_80c": b.sec_80c,
                "sec_80d": b.sec_80d,
                "sec_80ccd1b": b.sec_80ccd1b,
                "employer_nps_80ccd2": b.employer_nps_80ccd2,
                "sec_80e": b.sec_80e,
                "sec_80g": b.sec_80g,
                "sec_80tta": b.sec_80tta,
                "total_chapter_via": b.total_deductions_chapter_via,
            },
            tax_computation={
                "tax_on_income": b.tax_on_income,
                "rebate_87a": b.rebate_87a,
                "surcharge": b.surcharge,
                "cess": b.cess,
                "total_tax_payable": b.total_tax_payable,
            },
            confidence=form16_data.extraction_confidence or 0,
            notes=form16_data.parsing_notes or [],
            tax_analysis=tax_analysis,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
