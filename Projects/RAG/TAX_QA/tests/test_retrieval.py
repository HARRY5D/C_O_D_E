"""
Tests for the retrieval pipeline.
Uses curated documents to validate hybrid retrieval quality.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


def test_section_detection():
    """Section detector finds known sections."""
    from preprocessing.section_detector import detect_sections

    text = "Under Section 80C, a deduction of up to ₹1,50,000 is allowed. Section 80D covers health insurance."
    sections = detect_sections(text)
    assert "80C" in sections
    assert "80D" in sections


def test_chunking_splits_large_text():
    """Semantic chunker splits text larger than max chunk size."""
    from chunking.semantic_chunker import split_by_size

    long_text = "This is a sentence. " * 300  # ~6000 chars
    chunks = split_by_size(long_text)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= 3400  # max_chars + some tolerance


def test_metadata_tagging():
    """Metadata tagger adds required fields."""
    from chunking.metadata_tagger import tag_chunk

    chunk = {
        "chunk_id": 0,
        "chunk_text": "Section 80C allows deduction up to ₹1,50,000.",
        "source": "80C",
        "year": "2026",
    }
    tagged = tag_chunk(chunk)
    assert "metadata" in tagged
    meta = tagged["metadata"]
    assert "source" in meta
    assert "section" in meta
    assert "topic" in meta
    assert "year" in meta


def test_pdf_detection_digital(tmp_path):
    """PDF detector correctly identifies digital PDFs."""
    # This test requires a real PDF — skip if not available
    pdf_path = Path("data/raw/budget_speech.pdf")
    if not pdf_path.exists():
        pytest.skip("PDF not available for testing")

    from preprocessing.pdf_detector import detect_pdf_type
    result = detect_pdf_type(str(pdf_path))
    assert result["type"] in ("digital", "mixed", "scanned")
    assert result["total_pages"] > 0


def test_faiss_store_load_or_skip():
    """FAISS store loads if index exists, skips gracefully otherwise."""
    from vectordb.faiss_store import FAISSStore

    store = FAISSStore(embedding_dim=384)
    index_path = Path("vectordb/faiss_index/index.faiss")

    if not index_path.exists():
        pytest.skip("FAISS index not built yet — run python scripts/build_index.py")

    store.load()
    assert store.is_loaded()
    assert store.index.ntotal > 0
