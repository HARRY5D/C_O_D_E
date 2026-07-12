"""
Chunking — Section-Based + Semantic Splitting
Target: 500-800 tokens per chunk, preserving legal section boundaries.
"""
import re
from typing import List, Dict, Any


# Tax section heading patterns
SECTION_HEADING_RE = re.compile(
    r"^(?:Section|Sec\.)\s+\d+[A-Z]?(?:\([^)]+\))*\b",
    re.MULTILINE | re.IGNORECASE,
)

MAX_CHUNK_CHARS = 3200   # ~800 tokens at ~4 chars/token
MIN_CHUNK_CHARS = 400    # ~100 tokens — avoid trivial chunks
OVERLAP_CHARS = 200      # overlap for context continuity


def split_by_sections(text: str) -> List[str]:
    """
    Split text at section headings.
    Returns list of section text blocks.
    """
    boundaries = [m.start() for m in SECTION_HEADING_RE.finditer(text)]
    if not boundaries:
        return [text]

    sections = []
    for i, start in enumerate(boundaries):
        end = boundaries[i + 1] if i + 1 < len(boundaries) else len(text)
        section_text = text[start:end].strip()
        if section_text:
            sections.append(section_text)

    return sections


def split_by_size(text: str, max_chars: int = MAX_CHUNK_CHARS, overlap: int = OVERLAP_CHARS) -> List[str]:
    """
    Split text into overlapping windows by character count.
    Tries to split at sentence/paragraph boundaries.
    """
    if len(text) <= max_chars:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chars

        if end < len(text):
            # Find last paragraph break or sentence end before limit
            para_break = text.rfind("\n\n", start, end)
            sent_break = text.rfind(". ", start, end)
            break_point = max(para_break, sent_break)
            if break_point > start + MIN_CHUNK_CHARS:
                end = break_point + 1

        chunk = text[start:end].strip()
        if len(chunk) >= MIN_CHUNK_CHARS:
            chunks.append(chunk)

        start = end - overlap

    return chunks


def chunk_document_pages(
    pages: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Two-pass chunking:
    1. Try section-based splitting
    2. Then size-based splitting within each section

    Returns list of chunk dicts with inherited metadata.
    """
    all_chunks = []
    chunk_id = 0

    for page in pages:
        text = page.get("text", "")
        if not text:
            continue

        # Pass 1: section split
        sections = split_by_sections(text)

        for section_text in sections:
            # Pass 2: size split within section
            sub_chunks = split_by_size(section_text)

            for sub in sub_chunks:
                if len(sub) < MIN_CHUNK_CHARS:
                    continue

                chunk = {
                    **page,
                    "chunk_id": chunk_id,
                    "chunk_text": sub,
                    "char_count": len(sub),
                    "approx_tokens": len(sub) // 4,
                }
                all_chunks.append(chunk)
                chunk_id += 1

    return all_chunks
