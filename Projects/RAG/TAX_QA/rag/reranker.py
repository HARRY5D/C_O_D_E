"""
BGE Reranker — cross-encoder reranking using sentence-transformers CrossEncoder.

Uses sentence-transformers CrossEncoder instead of FlagEmbedding to avoid
native code crashes on Windows/Python 3.13.
BAAI/bge-reranker-base is directly compatible with CrossEncoder.

Takes top-20 retrieved candidates, returns top-5 reranked results.
"""
# Prevent TensorFlow import crash due to Protobuf version conflict on Windows
import sys
sys.modules['tensorflow'] = None

from typing import List, Dict, Any


class BGEReranker:
    """
    Cross-encoder reranker using sentence-transformers CrossEncoder.
    Unlike bi-encoders (FAISS/BM25), cross-encoders score query-document
    pairs jointly for higher accuracy.

    Falls back to score-based top-k slicing if the model cannot be loaded.
    """

    def __init__(self, model_name: str = "BAAI/bge-reranker-base"):
        self._model_name = model_name
        self._reranker = None
        self._available = False
        self._load_model(model_name)

    def _load_model(self, model_name: str) -> None:
        """Attempt to load the CrossEncoder model; fall back gracefully if it fails."""
        # Try primary model, then a lightweight fallback that doesn't need TensorFlow
        models_to_try = [
            model_name,
            "cross-encoder/ms-marco-MiniLM-L-6-v2",  # Pure PyTorch, no TF dependency
        ]

        for m in models_to_try:
            try:
                from sentence_transformers import CrossEncoder
                print(f"[Reranker] Loading cross-encoder: {m}")
                self._reranker = CrossEncoder(m)
                self._available = True
                self._model_name = m
                print(f"[Reranker] Cross-encoder loaded ✓ ({m})")
                return
            except Exception as e:
                print(f"[Reranker] Warning: Could not load '{m}': {e}")

        print("[Reranker] All reranker models failed. Using score-based top-k slicing.")
        self._available = False

    def rerank(
        self,
        query: str,
        candidates: List[Dict[str, Any]],
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Rerank candidate documents for a given query.

        Args:
            query: The user's query string
            candidates: List of retrieval results (each with 'text' key)
            top_k: Number of final results to return

        Returns:
            Top-K reranked results with 'rerank_score' added.
            Falls back to top-k slicing by retrieval score if model unavailable.
        """
        if not candidates:
            return []

        # Fallback: no reranker available → return top-k by original retrieval score
        if not self._available or self._reranker is None:
            scored = [
                {**c, "rerank_score": float(c.get("score", c.get("rrf_score", 0.0)))}
                for c in candidates
            ]
            scored.sort(key=lambda x: x["rerank_score"], reverse=True)
            return scored[:top_k]

        # Use CrossEncoder for proper reranking
        try:
            texts = [c.get("text", "") for c in candidates]
            pairs = [[query, t] for t in texts]

            scores = self._reranker.predict(pairs)

            # Handle scalar edge case
            if not hasattr(scores, "__len__"):
                scores = [float(scores)]

            scored = [
                {**c, "rerank_score": float(s)}
                for c, s in zip(candidates, scores)
            ]
            scored.sort(key=lambda x: x["rerank_score"], reverse=True)
            return scored[:top_k]

        except Exception as e:
            print(f"[Reranker] Reranking error: {e}. Using fallback.")
            return candidates[:top_k]
