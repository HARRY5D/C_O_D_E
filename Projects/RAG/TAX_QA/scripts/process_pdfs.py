"""
PDF Processing Script — runs the full preprocessing pipeline on all PDFs.
Outputs structured JSON files to the processed/ directory.

Usage:
    python scripts/process_pdfs.py
"""
import os
import sys
import json
from pathlib import Path
from tqdm import tqdm

# Ensure project root on path
sys.path.insert(0, str(Path(__file__).parent.parent))

from preprocessing.pdf_detector import detect_pdf_type, is_digital
from preprocessing.digital_extractor import extract_text_from_digital_pdf
from preprocessing.section_detector import tag_page_with_sections
from chunking.semantic_chunker import chunk_document_pages
from chunking.metadata_tagger import tag_chunks
from config.settings import settings


SOURCE_MAP = {
    "Income_tax_axt_1962.pdf": ("Income Tax Act 1961", "Income_tax_axt_1962"),
    "Income-tax-Rules-1962.pdf": ("Income Tax Rules 1962", "Income-tax-Rules-1962"),
    "Finance_Bill.pdf": ("Finance Bill 2025", "Finance_Bill"),
    "budget memorandum.pdf": ("Budget Memorandum 2025", "budget memorandum"),
    "budget_speech.pdf": ("Budget Speech 2025", "budget_speech"),
}


def process_curated_docs(curated_dir: Path, processed_dir: Path) -> list:
    """Convert curated markdown files to chunk format."""
    chunks = []
    chunk_id = 0

    for md_file in curated_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        source_name = md_file.stem

        # Simple split by H2 headers for curated docs
        sections = content.split("\n## ")
        for i, section in enumerate(sections):
            if not section.strip():
                continue
            text = ("## " + section) if i > 0 else section

            chunk = {
                "chunk_id": chunk_id,
                "chunk_text": text.strip(),
                "source": source_name,
                "page_num": 0,
                "year": "2026",
                "char_count": len(text),
                "approx_tokens": len(text) // 4,
                "is_curated": True,
            }
            chunks.append(chunk)
            chunk_id += 1

    print(f"[Curated] Processed {len(chunks)} chunks from {curated_dir}")
    return chunks


def process_pdf(pdf_path: Path, source_name: str, stem: str) -> list:
    """Process a single PDF through detection → extraction → chunking."""
    print(f"\n[PDF] Processing: {pdf_path.name}")

    # Detect type
    detection = detect_pdf_type(str(pdf_path))
    print(f"  Type: {detection['type']} | Pages: {detection['total_pages']} | Density: {detection['text_density']}")

    if is_digital(str(pdf_path)):
        pages = extract_text_from_digital_pdf(str(pdf_path), source_name=stem, year="2026")
    else:
        print("  → Scanned PDF detected, using OCR...")
        from preprocessing.ocr_extractor import extract_text_with_ocr
        pages = extract_text_with_ocr(str(pdf_path), source_name=stem, year="2026")

    print(f"  Extracted: {len(pages)} pages with content")

    # Tag sections
    pages = [tag_page_with_sections(p) for p in pages]

    # Chunk
    chunks = chunk_document_pages(pages)
    print(f"  Chunks: {len(chunks)}")

    return chunks


def main():
    raw_dir = settings.abs_raw_pdf_dir
    curated_dir = settings.abs_curated_dir
    processed_dir = settings.abs_processed_dir
    processed_dir.mkdir(parents=True, exist_ok=True)

    all_chunks = []

    # Check for cached PDF chunks in existing all_chunks.json
    output_file = processed_dir / "all_chunks.json"
    cached_pdf_chunks = []
    
    if output_file.exists():
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                existing_chunks = json.load(f)
            # A chunk is a cached PDF chunk if it doesn't have is_curated=True 
            # and its source doesn't match any curated file stem.
            curated_stems = {md.stem for md in curated_dir.glob("*.md")}
            cached_pdf_chunks = [
                c for c in existing_chunks 
                if not c.get("is_curated", False) and c.get("source") not in curated_stems
            ]
            if cached_pdf_chunks:
                print(f"\n[Cache] Loaded {len(cached_pdf_chunks)} PDF chunks from existing {output_file.name}")
        except Exception as e:
            print(f"⚠️ Could not load cached chunks: {e}")

    # Process curated knowledge base (always run to pick up new documents or changes)
    print("\n=== Processing Curated Knowledge Base ===")
    curated_chunks = process_curated_docs(curated_dir, processed_dir)
    tagged_curated = tag_chunks(curated_chunks)
    all_chunks.extend(tagged_curated)

    if cached_pdf_chunks:
        # Use cached PDF chunks
        print("\n=== Reusing Cached PDF Chunks ===")
        all_chunks.extend(cached_pdf_chunks)
    else:
        # Full processing fallback
        print("\n=== Processing PDFs (Full extraction) ===")
        for filename, (human_name, stem) in SOURCE_MAP.items():
            pdf_path = raw_dir / filename
            if not pdf_path.exists():
                pdf_path = settings.base_dir / "data" / filename
            if not pdf_path.exists():
                print(f"⚠️  Skipping {filename} — not found")
                continue

            try:
                chunks = process_pdf(pdf_path, human_name, stem)
                tagged = tag_chunks(chunks)
                all_chunks.extend(tagged)
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

    # Save all chunks (without embeddings)
    output_file = processed_dir / "all_chunks.json"
    # Remove embedding field if present
    for chunk in all_chunks:
        chunk.pop("embedding", None)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Total chunks: {len(all_chunks)}")
    print(f"✅ Saved to: {output_file}")
    print(f"\nNext step: python scripts/build_index.py")


if __name__ == "__main__":
    main()
