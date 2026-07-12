"""
Index Builder Script — generates embeddings and builds the FAISS index.

Usage:
    python scripts/build_index.py

Prerequisites:
    python scripts/process_pdfs.py must have been run first.
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings
from embeddings.embedder import BGEEmbedder, save_embeddings
from vectordb.faiss_store import FAISSStore


def main():
    processed_dir = settings.abs_processed_dir
    chunks_file = processed_dir / "all_chunks.json"

    if not chunks_file.exists():
        print("❌ Chunks file not found. Run: python scripts/process_pdfs.py first")
        sys.exit(1)

    print(f"[Build] Loading chunks from {chunks_file}")
    with open(chunks_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"[Build] Total chunks: {len(chunks)}")

    # ─── Step 1: Generate Embeddings ───────────────────────────────────────────
    print("\n[Step 1] Generating BGE embeddings...")
    embedder = BGEEmbedder(model_name=settings.embedding_model)
    embedded_chunks = embedder.embed_chunks(chunks, batch_size=32)

    # Save embedded chunks (optional backup)
    embeddings_backup = settings.base_dir / "embeddings" / "chunks_with_embeddings.json"
    save_embeddings(embedded_chunks, str(embeddings_backup))

    # ─── Step 2: Build & Save FAISS Index ─────────────────────────────────────
    print("\n[Step 2] Building FAISS index...")
    faiss_store = FAISSStore(
        embedding_dim=embedder.embedding_dim,
        index_path=str(settings.abs_faiss_index_path),
    )
    faiss_store.build(embedded_chunks)
    faiss_store.save()

    print(f"\n✅ Index built successfully!")
    print(f"   Vectors: {faiss_store.index.ntotal}")
    print(f"   Index path: {settings.abs_faiss_index_path}")
    print(f"\nNext step: streamlit run frontend/app.py")


if __name__ == "__main__":
    main()
