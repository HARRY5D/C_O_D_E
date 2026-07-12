"""
Hybrid Retriever — Dense (FAISS) + BM25 + Reciprocal Rank Fusion.
Retrieves top-20, fuses, returns candidates for reranking.
"""
import numpy as np
from typing import List, Dict, Any, Optional
from rank_bm25 import BM25Okapi

from embeddings.embedder import BGEEmbedder
from vectordb.faiss_store import FAISSStore


def _tokenize(text: str) -> List[str]:
    """Simple whitespace + lowercase tokenizer for BM25."""
    return text.lower().split()


def reciprocal_rank_fusion(
    rankings: List[List[Dict[str, Any]]],
    k: int = 60,
) -> List[Dict[str, Any]]:
    """
    Fuse multiple ranked lists using Reciprocal Rank Fusion (RRF).
    k=60 is the standard constant from the original RRF paper.
    """
    scores: Dict[str, float] = {}
    items: Dict[str, Dict[str, Any]] = {}

    for ranked_list in rankings:
        for rank, item in enumerate(ranked_list):
            key = item["text"][:100]  # Use first 100 chars as dedup key
            rrf_score = 1.0 / (k + rank + 1)
            scores[key] = scores.get(key, 0.0) + rrf_score
            if key not in items:
                items[key] = item

    # Sort by fused score descending
    sorted_keys = sorted(scores, key=lambda k: scores[k], reverse=True)
    fused = []
    for key in sorted_keys:
        item = items[key]
        item["rrf_score"] = round(scores[key], 6)
        fused.append(item)

    return fused


class HybridRetriever:
    """
    Hybrid retrieval: Dense (FAISS) + BM25 + RRF fusion.

    Pipeline:
        query → BGE embedding → FAISS top-20
               → BM25 top-20
               → RRF fusion
               → top-N candidates for reranking
    """

    def __init__(
        self,
        embedder: BGEEmbedder,
        faiss_store: FAISSStore,
        top_k: int = 20,
    ):
        self.embedder = embedder
        self.faiss_store = faiss_store
        self.top_k = top_k
        self._bm25: Optional[BM25Okapi] = None
        self._bm25_corpus: Optional[List[Dict[str, Any]]] = None

    def _build_bm25(self) -> None:
        """Build BM25 index from the FAISS store's text corpus."""
        if self._bm25 is None:
            print("[Retriever] Building BM25 index...")
            corpus = self.faiss_store.texts
            tokenized = [_tokenize(t) for t in corpus]
            self._bm25 = BM25Okapi(tokenized)
            self._bm25_corpus = [
                {"text": t, "metadata": m, "index": i}
                for i, (t, m) in enumerate(zip(self.faiss_store.texts, self.faiss_store.metadata))
            ]
            print(f"[Retriever] BM25 index built on {len(corpus)} documents")

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        filter_section: Optional[str] = None,
        filter_source: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Hybrid retrieval with RRF fusion.
        Returns top-N candidates sorted by fused score.
        """
        k = top_k or self.top_k

        # Ensure FAISS is loaded
        if not self.faiss_store.is_loaded():
            self.faiss_store.load()

        # Build BM25 if not built
        self._build_bm25()

        # ─── Dense Retrieval ──────────────────────────────────────────────────
        query_emb = self.embedder.embed_query(query)
        dense_results = self.faiss_store.search(
            query_emb,
            top_k=k,
            filter_section=filter_section,
            filter_source=filter_source,
        )

        # ─── BM25 Retrieval ───────────────────────────────────────────────────
        tokenized_query = _tokenize(query)
        bm25_scores = self._bm25.get_scores(tokenized_query)
        top_bm25_indices = np.argsort(bm25_scores)[::-1][:k]

        bm25_results = []
        for idx in top_bm25_indices:
            if bm25_scores[idx] <= 0:
                continue
            item = self._bm25_corpus[idx]
            meta = item["metadata"]

            # Apply same filters
            if filter_section and meta.get("section", "") != filter_section:
                continue
            if filter_source and filter_source.lower() not in meta.get("source", "").lower():
                continue

            bm25_results.append({
                **item,
                "bm25_score": float(bm25_scores[idx]),
            })

        # ─── RRF Fusion ───────────────────────────────────────────────────────
        fused = reciprocal_rank_fusion([dense_results, bm25_results])

        return fused[:k]
