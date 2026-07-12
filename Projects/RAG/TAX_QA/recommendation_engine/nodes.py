"""
LangGraph Nodes — individual processing steps in the FinAssist AI workflow.

Node execution order (determined by graph edges):
  detect_intent → [tax_engine] → [form16_parser] → rag_retrieve → generate_answer
"""
import json
import re
from typing import Dict, Any

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

from recommendation_engine.state import (
    GraphState, TaxEngineResult, RetrievedContext,
    OptimizationResult, Form16Result, UserMessage,
)
from config.settings import settings


# ─── Shared Ollama LLM client (lazy singleton, LangSmith auto-traced) ─────────
_llm = None

def get_llm() -> ChatOllama:
    """Return a ChatOllama instance (lazy singleton).
    LangSmith traces automatically via LANGCHAIN_TRACING_V2 env var."""
    global _llm
    if _llm is None:
        _llm = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=settings.llm_temperature,
        )
    return _llm


def _call_llm(prompt: str) -> str:
    """Call local Ollama LLM. Falls back to secondary model on failure."""
    models_to_try = [settings.ollama_model, settings.ollama_fallback_model]
    last_error = None

    for model in models_to_try:
        try:
            llm = ChatOllama(
                model=model,
                base_url=settings.ollama_base_url,
                temperature=settings.llm_temperature,
            )
            response = llm.invoke([HumanMessage(content=prompt)])
            return response.content or ""
        except Exception as e:
            last_error = e
            continue  # try fallback model

    return f"[LLM unavailable: {last_error}. Is Ollama running? Start with: ollama serve]"


# ════════════════════════════════════════════════════════════════════════════════
#  NODE 1: Intent Detection
# ════════════════════════════════════════════════════════════════════════════════

# (No ChatPromptTemplate needed — we call Ollama directly with plain strings)


def detect_intent_node(state: GraphState) -> GraphState:
    """Classify user intent and set routing flags."""
    state.processing_steps.append("intent_detection")

    try:
        prompt = f"""You are an intent classifier for a tax assistant.
Classify the user query into exactly ONE of these intents:
- tax_question: General question about tax rules, deductions, sections
- calculation_request: User wants to calculate actual tax (mentions income/salary)
- optimization_request: User wants to find tax savings opportunities
- form16_analysis: User mentions Form 16 or wants to analyze a document
- regime_comparison: User wants to compare old vs new tax regime
- general_chat: Greeting or completely off-topic

Respond with ONLY the intent label, nothing else.

User query: {state.user_query}"""

        intent_raw = _call_llm(prompt).strip().lower()

        # Map to valid intent
        valid_intents = [
            "tax_question", "calculation_request", "optimization_request",
            "form16_analysis", "regime_comparison", "general_chat"
        ]
        intent = intent_raw if intent_raw in valid_intents else "tax_question"
        state.intent = intent

        # Set routing flags
        state.needs_calculation = intent in ("calculation_request", "optimization_request", "regime_comparison")
        state.needs_retrieval = intent not in ("general_chat",)
        state.needs_optimization = intent == "optimization_request"
        state.needs_form16 = intent == "form16_analysis" and state.form16_path is not None

        # ── Extract income from query if no tax_profile yet ───────────────────
        # When user says "I earn 45 LPA" without Form16, parse it from the text
        if state.needs_calculation and not state.tax_profile:
            state.tax_profile = _extract_income_from_query(state.user_query)

    except Exception as e:
        state.intent = "tax_question"
        state.needs_retrieval = True
        state.error = f"Intent detection error: {e}"

    return state


def _extract_income_from_query(query: str) -> dict:
    """
    Try to parse income/salary figures from a freeform user query.
    Returns a minimal tax_profile dict, or {} if nothing found.
    Examples handled:
        "I earn 45 LPA"  → {"gross_salary": 4500000}
        "my CTC is 12 lakhs" → {"gross_salary": 1200000}
        "take-home is 24 lakh" → {"net_salary": 2400000}
    """
    import re

    # Normalize
    text = query.lower().replace(",", "")

    lakh_val = 100_000
    crore_val = 10_000_000

    def to_amount(num_str: str, unit: str) -> float:
        n = float(num_str)
        if "crore" in unit or "cr" in unit:
            return n * crore_val
        if "lakh" in unit or "lpa" in unit or "lac" in unit or "l" == unit.strip():
            return n * lakh_val
        if "k" in unit:
            return n * 1_000
        return n  # assume rupees

    profile = {}

    # Patterns: "45 lpa", "45 lakhs", "45 lakh", "45l", "45 LPA"
    # Also handles "45.5 lakh"
    income_patterns = [
        # gross indicators
        (r"(?:earn|salary|ctc|package|income|gross)[^\d]*(\d+\.?\d*)\s*(lpa|lakh|lakhs|lac|crore|cr|k)", "gross"),
        # take-home / net indicators
        (r"(?:take.?home|in.?hand|net)[^\d]*(\d+\.?\d*)\s*(lpa|lakh|lakhs|lac|crore|cr|k)", "net"),
        # fallback: plain number + unit near start
        (r"(\d+\.?\d*)\s*(lpa|lakh|lakhs|lac)\b", "gross"),
    ]

    for pattern, kind in income_patterns:
        m = re.search(pattern, text)
        if m:
            amount = to_amount(m.group(1), m.group(2))
            if kind == "gross" and amount > 0:
                profile["gross_salary"] = amount
            elif kind == "net" and amount > 0:
                profile["net_salary"] = amount

    # Detect freelance status
    freelance_keywords = ["freelancer", "freelance", "self-employed", "consultant", "contractor", "business", "independent professional"]
    if any(k in text for k in freelance_keywords):
        profile["is_freelancer"] = True

    return profile


# ════════════════════════════════════════════════════════════════════════════════
#  NODE 2: Form16 Parsing
# ════════════════════════════════════════════════════════════════════════════════

def form16_parser_node(state: GraphState) -> GraphState:
    """Parse Form 16 PDF and populate tax_profile."""
    state.processing_steps.append("form16_parsing")

    if not state.form16_path:
        return state

    try:
        from form16_parser.parser import extract_form16

        form16_data = extract_form16(state.form16_path)
        tax_profile = form16_data.to_tax_profile()

        state.tax_profile = tax_profile
        state.form16_result = Form16Result(
            extracted=True,
            data=form16_data.model_dump(),
            confidence=form16_data.extraction_confidence or 0.0,
            notes=form16_data.parsing_notes or [],
        )
        state.needs_calculation = True

    except Exception as e:
        state.form16_result = Form16Result(
            extracted=False,
            notes=[f"Parsing error: {str(e)}"],
        )
        state.error = str(e)

    return state


# ════════════════════════════════════════════════════════════════════════════════
#  NODE 3: Tax Engine
# ════════════════════════════════════════════════════════════════════════════════

def tax_engine_node(state: GraphState) -> GraphState:
    """Run deterministic tax calculation from tax_profile."""
    state.processing_steps.append("tax_engine")

    if not state.tax_profile:
        return state

    try:
        from tax_engine.calculator import calculate_full_tax

        result = calculate_full_tax(state.tax_profile)

        state.tax_result = TaxEngineResult(
            old_regime_tax=result["old_regime"]["total_tax"],
            new_regime_tax=result["new_regime"]["total_tax"],
            recommended_regime=result["recommendation"]["regime"],
            tax_savings=result["recommendation"]["tax_savings"],
            full_result=result,
        )

    except Exception as e:
        state.error = f"Tax engine error: {e}"

    return state


# ════════════════════════════════════════════════════════════════════════════════
#  NODE 4: Optimization Engine
# ════════════════════════════════════════════════════════════════════════════════

def optimization_node(state: GraphState) -> GraphState:
    """Find unused deduction opportunities."""
    state.processing_steps.append("optimization")

    if not state.tax_profile or not state.tax_result:
        return state

    try:
        from optimization.optimizer import find_optimization_opportunities

        opt_result = find_optimization_opportunities(
            profile=state.tax_profile,
            tax_result=state.tax_result.full_result,
        )

        state.optimization_result = OptimizationResult(
            total_potential_savings=opt_result["total_potential_additional_savings"],
            opportunities=opt_result["opportunities"],
            summary=opt_result["summary"],
        )

    except Exception as e:
        state.error = f"Optimization error: {e}"

    return state


# ════════════════════════════════════════════════════════════════════════════════
#  NODE 5: RAG Retrieval
# ════════════════════════════════════════════════════════════════════════════════

_retriever = None
_reranker = None


def get_rag_pipeline():
    """Lazy-load the RAG pipeline (embedder + FAISS + reranker)."""
    global _retriever, _reranker

    if _retriever is None:
        from embeddings.embedder import BGEEmbedder
        from vectordb.faiss_store import FAISSStore
        from rag.retriever import HybridRetriever
        from rag.reranker import BGEReranker

        embedder = BGEEmbedder(settings.embedding_model)
        faiss_store = FAISSStore(
            embedding_dim=embedder.embedding_dim,
            index_path=settings.faiss_index_path,
        )
        faiss_store.load()

        _retriever = HybridRetriever(
            embedder=embedder,
            faiss_store=faiss_store,
            top_k=settings.top_k_retrieval,
        )
        _reranker = BGEReranker(settings.reranker_model)

    return _retriever, _reranker


def rag_retrieve_node(state: GraphState) -> GraphState:
    """Retrieve legal context using hybrid RAG."""
    state.processing_steps.append("rag_retrieval")

    try:
        retriever, reranker = get_rag_pipeline()
        query = state.user_query

        candidates = retriever.retrieve(query, top_k=settings.top_k_retrieval)
        reranked = reranker.rerank(query, candidates, top_k=settings.top_k_rerank)

        # Format context
        context_parts = []
        citations = []
        for i, doc in enumerate(reranked, 1):
            meta = doc.get("metadata", {})
            source = meta.get("source", "")
            section = meta.get("section", "")
            context_parts.append(f"[{i}] {doc['text']}")
            cite = f"[{i}] {source}"
            if section and section != "general":
                cite += f" — Section {section}"
            citations.append(cite)

        state.rag_context = RetrievedContext(
            context="\n\n---\n\n".join(context_parts),
            citations="\n".join(citations),
            source_docs=reranked,
        )

    except FileNotFoundError:
        # FAISS index not built yet — continue without retrieval
        state.rag_context = RetrievedContext(
            context="[Index not built yet. Run: python scripts/build_index.py]",
            citations="",
        )
    except Exception as e:
        state.error = f"RAG error: {e}"
        state.rag_context = RetrievedContext(context="", citations="")

    return state


# ════════════════════════════════════════════════════════════════════════════════
#  NODE 6: Answer Generation
# ════════════════════════════════════════════════════════════════════════════════

# (No ChatPromptTemplate needed — prompt is built as a plain f-string below)


def generate_answer_node(state: GraphState) -> GraphState:
    """Generate the final answer using Ollama, combining all gathered context."""
    state.processing_steps.append("answer_generation")

    # Build tax context string
    tax_context = "No tax calculation performed."
    if state.tax_result:
        tr = state.tax_result
        tax_context = (
            f"Old Regime Tax: Rs.{tr.old_regime_tax:,.0f}\n"
            f"New Regime Tax: Rs.{tr.new_regime_tax:,.0f}\n"
            f"Recommended: {tr.recommended_regime} Regime\n"
            f"Tax Savings with recommendation: Rs.{tr.tax_savings:,.0f}"
        )

    # Build optimization context
    opt_context = "No optimization analysis performed."
    if state.optimization_result:
        opt = state.optimization_result
        opt_context = opt.summary
        if opt.opportunities:
            lines = [f"- {o['title']}: saves Rs.{o['estimated_tax_savings']:,.0f}" for o in opt.opportunities[:3]]
            opt_context += "\n" + "\n".join(lines)

    rag_context = state.rag_context.context if state.rag_context else ""
    citations = state.rag_context.citations if state.rag_context else ""

    try:
        prompt = f"""You are FinAssist AI - an expert Indian tax advisor for FY 2025-26.

CRITICAL CONSTRAINTS FOR PREVENTING HALLUCINATIONS:
1. NEVER perform tax calculations yourself. Use the exact numbers provided in TAX_RESULT only.
2. DO NOT explain, justify, or break down the tax calculation (such as explaining tax slabs, percentage brackets, or deductions applied) UNLESS that specific explanation is explicitly present in the retrieved LEGAL_CONTEXT below.
3. If LEGAL_CONTEXT is empty or says 'No specific legal context retrieved.', do not speculate about how the tax engine arrived at the numbers. State the tax result numbers directly, mention that the calculations are performed deterministically by the Python tax engine, and recommend using the tax calculator or consulting a professional.
4. Never invent or assume any tax slabs, rates, rebates, or exemptions that are not documented in the TAX_RESULT or the retrieved LEGAL_CONTEXT.
5. Always cite legal sections (e.g., Section 44ADA) when making factual claims, but only if they are mentioned in the retrieved LEGAL_CONTEXT. If in doubt, do not cite a section.

TAX_RESULT:
{tax_context}

LEGAL_CONTEXT:
{rag_context or 'No specific legal context retrieved.'}

SOURCES:
{citations or 'None'}

OPTIMIZATION:
{opt_context}

User question: {state.user_query}"""

        answer = _call_llm(prompt)
        state.final_answer = answer

    except Exception as e:
        state.final_answer = f"I encountered an error generating the response: {e}"
        state.error = str(e)

    return state
