"""
Form 16 Parser — extracts tax information from Form 16 PDFs using PyMuPDF + regex.
"""
import re
import fitz  # PyMuPDF
from typing import Optional
from form16_parser.schema import Form16Data, Part_A, Part_B


# ─── Regex Patterns ────────────────────────────────────────────────────────────
PATTERNS = {
    # Part A
    "employer_name": r"Name\s+of\s+(?:the\s+)?[Ee]mployer[:\s]+([A-Z][^\n]{2,60})",
    "employer_tan": r"TAN\s+of\s+(?:the\s+)?[Ee]mployer[:\s]+([A-Z0-9]{10})",
    "employer_pan": r"PAN\s+of\s+(?:the\s+)?[Ee]mployer[:\s]+([A-Z]{5}[0-9]{4}[A-Z])",
    "employee_pan": r"PAN\s+of\s+(?:the\s+)?[Ee]mployee[:\s]+([A-Z]{5}[0-9]{4}[A-Z])",
    "assessment_year": r"Assessment\s+Year[:\s]+(\d{4}-\d{2,4})",
    "financial_year": r"Financial\s+Year[:\s]+(\d{4}-\d{2,4})",

    # Salary components (Part B)
    "gross_salary": [
        r"Gross\s+[Ss]alary[:\s₹,]+([\d,]+(?:\.\d{2})?)",
        r"Total\s+[Ss]alary[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    ],
    "basic_salary": r"Basic\s+[Ss]alary[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    "hra_received": r"House\s+Rent\s+Allowance[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    "hra_exemption": [
        r"HRA\s+[Ee]xemption[:\s₹,]+([\d,]+(?:\.\d{2})?)",
        r"Exempt\s+HRA[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    ],

    # TDS
    "tds_deducted": [
        r"Total\s+[Tt]ax\s+[Dd]educted[:\s₹,]+([\d,]+(?:\.\d{2})?)",
        r"TDS\s+[Dd]educted[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    ],

    # Deductions
    "sec_80c": r"(?:80C|80-C)[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    "sec_80d": r"(?:80D|80-D)[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    "sec_80ccd1b": r"80CCD\s*\(1B\)[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    "employer_nps_80ccd2": r"80CCD\s*\(2\)[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    "sec_80e": r"(?:80E)[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    "sec_80g": r"(?:80G)[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    "sec_80tta": r"(?:80TTA)[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    "total_deductions_chapter_via": r"(?:Total\s+deductions|Total\s+VI-A)[:\s₹,]+([\d,]+(?:\.\d{2})?)",

    # Tax computation
    "taxable_income": r"(?:Taxable\s+[Ii]ncome|Net\s+[Tt]axable)[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    "total_tax_payable": r"(?:Total\s+[Tt]ax\s+[Pp]ayable|Tax\s+[Pp]ayable)[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    "rebate_87a": r"(?:Rebate|87A)[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    "surcharge": r"Surcharge[:\s₹,]+([\d,]+(?:\.\d{2})?)",
    "cess": r"(?:Cess|Health\s+and\s+Education\s+Cess)[:\s₹,]+([\d,]+(?:\.\d{2})?)",
}


def _clean_amount(s: str) -> float:
    """Convert '12,50,000.00' → 1250000.0"""
    try:
        return float(s.replace(",", ""))
    except (ValueError, AttributeError):
        return 0.0


def _extract_field(text: str, pattern) -> Optional[str]:
    """Try one or more regex patterns, return first match."""
    patterns = pattern if isinstance(pattern, list) else [pattern]
    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def extract_form16(pdf_path: str) -> Form16Data:
    """
    Extract Form 16 data from a PDF file.
    Returns a Form16Data Pydantic model.
    """
    # Extract full text
    doc = fitz.open(pdf_path)
    all_text = []
    for page in doc:
        all_text.append(page.get_text("text"))
    doc.close()

    full_text = "\n".join(all_text)
    notes = []
    confidence_hits = 0
    total_fields = len(PATTERNS)

    # ─── Part A ────────────────────────────────────────────────────────────────
    part_a = Part_A(
        employer_name=_extract_field(full_text, PATTERNS["employer_name"]),
        employer_tan=_extract_field(full_text, PATTERNS["employer_tan"]),
        employer_pan=_extract_field(full_text, PATTERNS["employer_pan"]),
        employee_pan=_extract_field(full_text, PATTERNS["employee_pan"]),
        assessment_year=_extract_field(full_text, PATTERNS["assessment_year"]) or "2026-27",
        financial_year=_extract_field(full_text, PATTERNS["financial_year"]) or "2025-26",
    )

    # ─── Part B ────────────────────────────────────────────────────────────────
    def get_amount(field: str) -> float:
        val = _extract_field(full_text, PATTERNS[field])
        if val:
            confidence_hits
            return _clean_amount(val)
        return 0.0

    # Count hits for confidence
    extracted_amounts = {}
    for field in [
        "gross_salary", "basic_salary", "hra_received", "hra_exemption",
        "tds_deducted", "sec_80c", "sec_80d", "sec_80ccd1b", "employer_nps_80ccd2",
        "sec_80e", "sec_80g", "sec_80tta", "total_deductions_chapter_via",
        "taxable_income", "total_tax_payable", "rebate_87a", "surcharge", "cess"
    ]:
        val = _extract_field(full_text, PATTERNS[field])
        extracted_amounts[field] = _clean_amount(val) if val else 0.0
        if val:
            confidence_hits += 1

    part_b = Part_B(
        gross_salary=extracted_amounts.get("gross_salary", 0),
        basic_salary=extracted_amounts.get("basic_salary", 0),
        hra_received=extracted_amounts.get("hra_received", 0),
        hra_exemption=extracted_amounts.get("hra_exemption", 0),
        tds_deducted=extracted_amounts.get("tds_deducted", 0),
        sec_80c=extracted_amounts.get("sec_80c", 0),
        sec_80d=extracted_amounts.get("sec_80d", 0),
        sec_80ccd1b=extracted_amounts.get("sec_80ccd1b", 0),
        employer_nps_80ccd2=extracted_amounts.get("employer_nps_80ccd2", 0),
        sec_80e=extracted_amounts.get("sec_80e", 0),
        sec_80g=extracted_amounts.get("sec_80g", 0),
        sec_80tta=extracted_amounts.get("sec_80tta", 0),
        total_deductions_chapter_via=extracted_amounts.get("total_deductions_chapter_via", 0),
        taxable_income=extracted_amounts.get("taxable_income", 0),
        total_tax_payable=extracted_amounts.get("total_tax_payable", 0),
        rebate_87a=extracted_amounts.get("rebate_87a", 0),
        surcharge=extracted_amounts.get("surcharge", 0),
        cess=extracted_amounts.get("cess", 0),
    )

    if extracted_amounts.get("gross_salary", 0) == 0:
        notes.append("Could not extract gross salary — please verify")
    if extracted_amounts.get("tds_deducted", 0) == 0:
        notes.append("Could not extract TDS amount — please verify")

    confidence = round(confidence_hits / max(total_fields, 1), 2)

    return Form16Data(
        part_a=part_a,
        part_b=part_b,
        raw_text_preview=full_text[:500],
        extraction_confidence=confidence,
        parsing_notes=notes,
    )
