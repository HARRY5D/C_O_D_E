"""
Metadata Tagger — enriches chunks with structured metadata for filtering.
"""
from typing import Dict, Any
from preprocessing.section_detector import detect_sections, get_primary_section, get_topic


SOURCE_NAME_MAP = {
    "Income_tax_axt_1962": "Income Tax Act 1962",
    "Income-tax-Rules-1962": "Income Tax Rules 1962",
    "Finance_Bill": "Finance Bill 2025",
    "budget memorandum": "Budget Memorandum 2025",
    "budget_speech": "Budget Speech 2025",
    # Curated docs
    "80C": "Curated — Section 80C",
    "80D": "Curated — Section 80D",
    "NPS": "Curated — NPS",
    "HRA": "Curated — HRA",
    "Home_Loan": "Curated — Home Loan",
    "Old_vs_New_Regime": "Curated — Old vs New Regime",
    "Tax_Slabs": "Curated — Tax Slabs",
}


def tag_chunk(chunk: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add standardized metadata to a chunk for FAISS metadata filtering.

    Metadata fields:
    - source       : Human-readable document name
    - section      : Primary section reference (e.g., "80C")
    - topic        : Topic category (e.g., "deduction_investments")
    - year         : Tax year
    - document_name: Original filename stem
    - chunk_id     : Unique chunk identifier
    - is_curated   : True if from hand-crafted knowledge base
    """
    text = chunk.get("chunk_text", "")
    raw_source = chunk.get("source", "unknown")

    sections = detect_sections(text)
    primary_section = get_primary_section(text)
    topic = get_topic(primary_section)

    # Check if override section from page-level detection
    if chunk.get("primary_section") and chunk["primary_section"] != "general":
        primary_section = chunk["primary_section"]
        topic = get_topic(primary_section)

    human_source = SOURCE_NAME_MAP.get(raw_source, raw_source)
    is_curated = raw_source in SOURCE_NAME_MAP and "Curated" in SOURCE_NAME_MAP.get(raw_source, "")

    return {
        **chunk,
        "metadata": {
            "source": human_source,
            "document_name": raw_source,
            "section": primary_section,
            "all_sections": sections,
            "topic": topic,
            "year": chunk.get("year", "2026"),
            "page_num": chunk.get("page_num", 0),
            "chunk_id": chunk.get("chunk_id", 0),
            "is_curated": is_curated,
            "char_count": chunk.get("char_count", len(text)),
            "approx_tokens": chunk.get("approx_tokens", len(text) // 4),
        },
    }


def tag_chunks(chunks: list) -> list:
    return [tag_chunk(c) for c in chunks]
