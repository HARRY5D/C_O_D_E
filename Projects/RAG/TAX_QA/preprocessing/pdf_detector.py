"""
PDF Type Detector — determines if a PDF is digital (text-based) or scanned (image-based).
Routes to the appropriate extractor.
"""
import fitz  # PyMuPDF


def detect_pdf_type(pdf_path: str, sample_pages: int = 5) -> dict:
    """
    Detect whether a PDF is digital or scanned by checking text density
    on the first N pages.

    Returns:
        {
            "path": str,
            "type": "digital" | "scanned" | "mixed",
            "text_density": float,   # avg chars per page
            "total_pages": int,
        }
    """
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    pages_to_check = min(sample_pages, total_pages)

    char_counts = []
    for i in range(pages_to_check):
        page = doc[i]
        text = page.get_text("text")
        char_counts.append(len(text.strip()))

    doc.close()

    avg_chars = sum(char_counts) / len(char_counts) if char_counts else 0

    # Heuristic: < 100 chars/page → scanned; > 500 → digital
    if avg_chars >= 500:
        pdf_type = "digital"
    elif avg_chars >= 100:
        pdf_type = "mixed"
    else:
        pdf_type = "scanned"

    return {
        "path": pdf_path,
        "type": pdf_type,
        "text_density": round(avg_chars, 1),
        "total_pages": total_pages,
        "sample_pages_checked": pages_to_check,
    }


def is_digital(pdf_path: str) -> bool:
    return detect_pdf_type(pdf_path)["type"] in ("digital", "mixed")
