"""
Digital PDF Extractor — uses PyMuPDF for text and pdfplumber for tables.
Preserves headings, paragraphs, and structure.
"""
import re
import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict, Any


HEADER_FOOTER_PATTERNS = [
    r"^\s*\d+\s*$",                        # standalone page numbers
    r"Income.Tax.Act",                      # repeated doc titles
    r"^\s*www\.",                           # website footers
    r"^\s*\(Inserted\s+by",                # amendment notes at page edges
    r"^\s*\[See\s+rule",                   # rule references at edges
]


def _is_noise(line: str) -> bool:
    line = line.strip()
    if not line:
        return True
    for pat in HEADER_FOOTER_PATTERNS:
        if re.search(pat, line, re.IGNORECASE):
            return True
    return False


def extract_text_from_digital_pdf(
    pdf_path: str,
    source_name: str = "",
    year: str = "2026",
) -> List[Dict[str, Any]]:
    """
    Extract structured text from a digital PDF using PyMuPDF.

    Returns list of page dicts:
    [
        {
            "page_num": int,
            "text": str,
            "source": str,
            "year": str,
        },
        ...
    ]
    """
    doc = fitz.open(pdf_path)
    pages = []

    source = source_name or Path(pdf_path).stem

    for page_num in range(len(doc)):
        page = doc[page_num]
        raw_text = page.get_text("text")

        # Clean line by line
        lines = raw_text.split("\n")
        clean_lines = [ln for ln in lines if not _is_noise(ln)]
        clean_text = "\n".join(clean_lines).strip()

        if len(clean_text) < 50:
            # Skip mostly empty pages
            continue

        pages.append({
            "page_num": page_num + 1,
            "text": clean_text,
            "source": source,
            "year": year,
        })

    doc.close()
    return pages
