"""
OCR Extractor — PaddleOCR fallback for scanned PDFs.
Only invoked when PDF is detected as scanned by pdf_detector.py.
"""
from typing import List, Dict, Any
from pathlib import Path


def extract_text_with_ocr(
    pdf_path: str,
    source_name: str = "",
    year: str = "2026",
) -> List[Dict[str, Any]]:
    """
    Extract text from a scanned PDF using PaddleOCR.
    Falls back to a clear error message if PaddleOCR is not installed.

    Returns same format as digital_extractor for pipeline compatibility.
    """
    try:
        import fitz  # PyMuPDF for PDF → image conversion
        from paddleocr import PaddleOCR
        import numpy as np
    except ImportError:
        raise RuntimeError(
            "PaddleOCR is not installed. Run: pip install paddlepaddle paddleocr\n"
            "Note: PaddleOCR is only needed for scanned PDFs. "
            "All your current PDFs are digital — PyMuPDF handles them."
        )

    ocr = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)
    doc = fitz.open(pdf_path)
    source = source_name or Path(pdf_path).stem
    pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        # Render page to image (300 DPI for accuracy)
        mat = fitz.Matrix(300 / 72, 300 / 72)
        pix = page.get_pixmap(matrix=mat)
        img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height, pix.width, pix.n
        )

        result = ocr.ocr(img_array, cls=True)
        if not result or not result[0]:
            continue

        lines = [line[1][0] for line in result[0] if line[1][1] > 0.5]
        text = "\n".join(lines).strip()

        if len(text) < 50:
            continue

        pages.append({
            "page_num": page_num + 1,
            "text": text,
            "source": source,
            "year": year,
            "method": "ocr",
        })

    doc.close()
    return pages
