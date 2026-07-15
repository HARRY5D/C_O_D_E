"""
RAG Chain — Retrieval-augmented generation pipeline.
Integrates HybridRetriever + BGEReranker + local Ollama LLM.
LangSmith tracing is automatic via LANGCHAIN_TRACING_V2 env var (ChatOllama is a LangChain object).
"""
from typing import List, Dict, Any

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from rag.retriever import HybridRetriever
from rag.reranker import BGEReranker
from config.settings import settings


TAX_SYSTEM_PROMPT = """You are FinAssist AI, an expert Indian tax advisor specializing in FY 2025-26 taxation.

CRITICAL ANTI-HALLUCINATION RULES:
1. NEVER perform tax calculations yourself. If tax figures are not provided in context, direct the user to use the Tax Calculator.
2. DO NOT explain or break down calculations (tax slabs, bracket math, deduction arithmetic) unless the exact breakdown is in RETRIEVED LEGAL CONTEXT.
3. If RETRIEVED LEGAL CONTEXT is empty or irrelevant, do not speculate. Recommend the calculator or a professional.
4. NEVER invent or assume tax rates, slabs, limits, exemptions, or section numbers not in RETRIEVED LEGAL CONTEXT.
5. Cite section numbers ONLY if they appear in SOURCE CITATIONS below. Do NOT invent section references.
6. FREELANCER RULE: Never cite Section 194-I for freelancers (that is TDS on Rent).
   Freelancer income = Section 28 | Freelancer TDS = Section 194J | Presumptive tax = Section 44ADA.
7. REGIME RULE: If the user has specified old regime or new regime, present ONLY that regime's numbers.

RETRIEVED LEGAL CONTEXT:
{context}

SOURCE CITATIONS:
{citations}
"""


def format_context(docs: List[Dict[str, Any]]) -> tuple[str, str]:
    """Format retrieved docs into context string and citations list."""
    context_parts = []
    citations = []

    for i, doc in enumerate(docs, 1):
        text = doc.get("text", "")
        meta = doc.get("metadata", {})
        source = meta.get("source", "Unknown")
        section = meta.get("section", "")

        context_parts.append(f"[Chunk {i}] {text}")

        cite = f"[{i}] {source}"
        if section and section != "general":
            cite += f" - Section {section}"
        citations.append(cite)

    return "\n\n---\n\n".join(context_parts), "\n".join(citations)


class RAGChain:
    """
    Full RAG pipeline:
    Query -> Hybrid Retrieval -> Reranking -> Prompt -> Ollama LLM (traced) -> Answer
    """

    def __init__(
        self,
        retriever: HybridRetriever,
        reranker: BGEReranker,
        top_k_retrieve: int = 20,
        top_k_rerank: int = 5,
    ):
        self.retriever = retriever
        self.reranker = reranker
        self.top_k_retrieve = top_k_retrieve
        self.top_k_rerank = top_k_rerank

        # Initialize Ollama LLM — LangSmith traces automatically
        self._llm = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=settings.llm_temperature,
        )
        self._fallback_llm = ChatOllama(
            model=settings.ollama_fallback_model,
            base_url=settings.ollama_base_url,
            temperature=settings.llm_temperature,
        )

    def _call_llm(self, system_prompt: str, user_question: str) -> str:
        """Call Ollama LLM with system + user message. Falls back to secondary model."""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_question),
        ]
        for llm in [self._llm, self._fallback_llm]:
            try:
                response = llm.invoke(messages)
                return response.content or ""
            except Exception:
                continue
        return "[LLM unavailable. Is Ollama running? Run: ollama serve]"

    def query(self, question: str) -> Dict[str, Any]:
        """
        Run a question through the full RAG pipeline.
        Returns answer + source docs for citation display.
        """
        # Retrieve and rerank
        candidates = self.retriever.retrieve(question, top_k=self.top_k_retrieve)
        reranked = self.reranker.rerank(question, candidates, top_k=self.top_k_rerank)
        context, citations = format_context(reranked)

        # Build prompt
        system_prompt = TAX_SYSTEM_PROMPT.format(context=context, citations=citations)

        # Call local LLM with LangSmith tracing
        answer = self._call_llm(system_prompt, question)

        return {
            "question": question,
            "answer": answer,
            "source_docs": reranked,
            "citations": citations,
        }

    def query_stream(self, question: str):
        """Stream the Ollama response token by token (for Streamlit st.write_stream)."""
        candidates = self.retriever.retrieve(question, top_k=self.top_k_retrieve)
        reranked = self.reranker.rerank(question, candidates, top_k=self.top_k_rerank)
        context, citations = format_context(reranked)

        system_prompt = TAX_SYSTEM_PROMPT.format(context=context, citations=citations)
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=question),
        ]

        # Stream via ChatOllama
        for chunk in self._llm.stream(messages):
            if chunk.content:
                yield chunk.content
