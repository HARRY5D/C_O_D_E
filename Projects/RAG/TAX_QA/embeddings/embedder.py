"""
BGE Embedder — generates dense embeddings using BAAI/bge-small-en-v1.5
Stores chunk text + embedding + metadata for FAISS indexing.
"""
# Prevent TensorFlow import crash due to Protobuf version conflict on Windows
import sys
sys.modules['tensorflow'] = None

import os
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm
from sentence_transformers import SentenceTransformer


class BGEEmbedder:
    """
    Wrapper for BAAI/bge-small-en-v1.5 embedding model.
    BGE models require a query prefix for retrieval queries.
    """

    QUERY_PREFIX = "Represent this sentence for searching relevant passages: "
    PASSAGE_PREFIX = ""  # No prefix for passages/documents

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5", device: str = "cpu"):
        print(f"[Embedder] Loading model: {model_name}")
        self.model = SentenceTransformer(model_name, device=device)
        self.model_name = model_name
        print("[Embedder] Model loaded successfully")

    def embed_passages(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Embed document passages (no prefix needed for BGE passage encoding)."""
        return self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=True,  # L2 normalize for cosine similarity
        )

    def embed_query(self, query: str) -> np.ndarray:
        """Embed a user query with the BGE query prefix."""
        prefixed = self.QUERY_PREFIX + query
        return self.model.encode(
            [prefixed],
            normalize_embeddings=True,
        )[0]

    def embed_chunks(
        self,
        chunks: List[Dict[str, Any]],
        batch_size: int = 32,
    ) -> List[Dict[str, Any]]:
        """
        Generate embeddings for all chunks.
        Returns chunks with 'embedding' field added.
        """
        texts = [c.get("chunk_text", "") for c in chunks]
        print(f"[Embedder] Embedding {len(texts)} chunks...")
        embeddings = self.embed_passages(texts, batch_size=batch_size)

        enriched = []
        for chunk, emb in zip(chunks, embeddings):
            enriched.append({
                **chunk,
                "embedding": emb.tolist(),
            })

        print(f"[Embedder] Done. Embedding dim: {embeddings.shape[1]}")
        return enriched

    @property
    def embedding_dim(self) -> int:
        return self.model.get_sentence_embedding_dimension()


def save_embeddings(
    embedded_chunks: List[Dict[str, Any]],
    output_path: str = "embeddings/chunks_with_embeddings.json",
) -> None:
    """Save embedded chunks to JSON (for inspection / backup)."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(embedded_chunks, f, ensure_ascii=False, indent=2)
    print(f"[Embedder] Saved {len(embedded_chunks)} embedded chunks → {output_path}")


def load_embeddings(path: str = "embeddings/chunks_with_embeddings.json") -> List[Dict[str, Any]]:
    """Load embedded chunks from JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
