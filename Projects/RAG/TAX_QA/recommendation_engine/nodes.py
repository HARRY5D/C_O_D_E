"""
LangGraph Nodes - individual processing steps in the FinAssist AI workflow.
Node execution order:
  detect_intent -> [form16_parser] -> [tax_engine] -> [optimize] -> rag_retrieve -> generate_answer -> gemini_verify
"""
import re
from typing import Optional
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from recommendation_engine.state import (
    GraphState, TaxEngineResult, RetrievedContext,
    OptimizationResult, Form16Result, GeminiVerificationResult, UserMessage,
)
from config.settings import settings

_llm = None

def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=settings.llm_temperature,
        )
    return _llm


def _call_llm(prompt: str) -> str:
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
            continue
    return f"[LLM unavailable: {last_error}. Is Ollama running? Run: ollama serve]"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _detect_regime_preference(query: str) -> Optional[str]:
    """
    Detect if the user explicitly requested old or new regime.
    Returns "old", "new", or None.
    """
    text = query.lower()
    old_indicators = [
        "old regime", "old tax regime", "old system",
        "traditional regime", "without 115bac", "pre-115bac",
    ]
    new_indicators = [
        "new regime", "new tax regime", "new system",
        "115bac", "section 115bac", "concessional regime",
        "default regime",
    ]
    for ind in old_indicators:
        if ind in text:
            return "old"
    for ind in new_indicators:
        if ind in text:
            return "new"
    return None


def _extract_income_from_query(query: str) -> dict:
    """Parse income figures from a freeform user query."""
    text = query.lower().replace(",", "")
    lakh_val = 100_000
    crore_val = 10_000_000

    def to_amount(num_str, unit):
        n = float(num_str)
        if "crore" in unit or "cr" in unit:
            return n * crore_val
        if "lakh" in unit or "lpa" in unit or "lac" in unit or unit.strip() == "l":
            return n * lakh_val
        if "k" in unit:
            return n * 1_000
        return n

    profile = {}
    income_patterns = [
        # gross indicators
        (r"(?:earn|salary|ctc|package|income|gross)[^\d]*(\d+\.?\d*)\s*(lpa|lakh|lakhs|lac|crore|cr|k)", "gross"),
        # take-home / net indicators
        (r"(?:take.?home|in.?hand|net)[^\d]*(\d+\.?\d*)\s*(lpa|lakh|lakhs|lac|crore|cr|k)", "net"),
        # hypothetical phrasing: "if I earn 15 lakh", "suppose I earn 15L", "say my income is 10 lakh"
        (r"(?:if\s+i\s+earn|suppose\s+i\s+earn|say\s+i\s+earn|if\s+my\s+income\s+is|if\s+my\s+salary\s+is|assuming\s+income\s+of|earning\s+of|per\s+year\s+is)[^\d]*(\d+\.?\d*)\s*(lpa|lakh|lakhs|lac|crore|cr|k)", "gross"),
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

    freelance_keywords = [
        "freelancer", "freelance", "self-employed", "consultant",
        "contractor", "business", "independent professional"
    ]
    if any(k in text for k in freelance_keywords):
        profile["is_freelancer"] = True
    return profile


def _extract_section_refs_from_rag(rag_context: str) -> str:
    """Build whitelist of section numbers from retrieved RAG context."""
    if not rag_context:
        return ""
    pattern = r"(?:[Ss]ection\s+|[Ss]ec\.?\s*)?(\d+[A-Z]{0,4}(?:\(\w+\))?)"
    matches = re.findall(pattern, rag_context)
    seen = set()
    sections = []
    for m in matches:
        if re.search(r"[A-Za-z]", m) or (m.isdigit() and int(m) <= 300):
            key = f"Section {m}"
            if key not in seen:
                seen.add(key)
                sections.append(key)
    return ", ".join(sections) if sections else ""


# ===========================================================================
#  NODE 1: Intent Detection
# ===========================================================================

def detect_intent_node(state: GraphState) -> GraphState:
    """Classify intent, detect regime preference, set routing flags."""
    state.processing_steps.append("intent_detection")
    try:
        prompt = (
            "You are an intent classifier for a tax assistant.\n"
            "Classify the user query into exactly ONE of these intents:\n"
            "- tax_question\n"
            "- calculation_request\n"
            "- optimization_request\n"
            "- form16_analysis\n"
            "- regime_comparison\n"
            "- general_chat\n"
            "Respond with ONLY the intent label, nothing else.\n\n"
            f"User query: {state.user_query}"
        )
        intent_raw = _call_llm(prompt).strip().lower()
        valid_intents = [
            "tax_question", "calculation_request", "optimization_request",
            "form16_analysis", "regime_comparison", "general_chat",
        ]
        intent = intent_raw if intent_raw in valid_intents else "tax_question"
        state.intent = intent
        state.needs_calculation = intent in ("calculation_request", "optimization_request", "regime_comparison")
        state.needs_retrieval = intent not in ("general_chat",)
        state.needs_optimization = intent == "optimization_request"
        state.needs_form16 = intent == "form16_analysis" and state.form16_path is not None

        # Strict regime lock detection
        state.preferred_regime = _detect_regime_preference(state.user_query)

        if state.needs_calculation and not state.tax_profile:
            state.tax_profile = _extract_income_from_query(state.user_query)

    except Exception as e:
        state.intent = "tax_question"
        state.needs_retrieval = True
        state.error = f"Intent detection error: {e}"
    return state


# ===========================================================================
#  NODE 2: Form16 Parsing
# ===========================================================================

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
        state.form16_result = Form16Result(extracted=False, notes=[f"Parsing error: {e}"])
        state.error = str(e)
    return state


# ===========================================================================
#  NODE 3: Tax Engine
# ===========================================================================

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


# ===========================================================================
#  NODE 4: Optimization Engine
# ===========================================================================

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


# ===========================================================================
#  NODE 5: RAG Retrieval
# ===========================================================================

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
        candidates = retriever.retrieve(state.user_query, top_k=settings.top_k_retrieval)
        reranked = reranker.rerank(state.user_query, candidates, top_k=settings.top_k_rerank)
        context_parts = []
        citations = []
        for i, doc in enumerate(reranked, 1):
            meta = doc.get("metadata", {})
            source = meta.get("source", "")
            section = meta.get("section", "")
            context_parts.append(f"[{i}] {doc.get("text", "")}")
            cite = f"[{i}] {source}"
            if section and section != "general":
                cite += f" --- Section {section}"
            citations.append(cite)
        state.rag_context = RetrievedContext(
            context="\n\n---\n\n".join(context_parts),
            citations="\n".join(citations),
            source_docs=reranked,
        )
    except FileNotFoundError:
        state.rag_context = RetrievedContext(
            context="[Index not built yet. Run: python scripts/build_index.py]",
            citations="",
        )
    except Exception as e:
        state.error = f"RAG error: {e}"
        state.rag_context = RetrievedContext(context="", citations="")
    return state


# ===========================================================================
#  NODE 6: Answer Generation  (Anti-Hallucination Architecture)
# ===========================================================================

def generate_answer_node(state: GraphState) -> GraphState:
    """Generate the final answer using Ollama with strict anti-hallucination controls."""
    state.processing_steps.append("answer_generation")

    # 1. REGIME LOCK
    regime_lock_block = ""
    if state.preferred_regime == "old":
        regime_lock_block = (
            "\n=== REGIME LOCK: OLD REGIME ===\n"
            "The user has EXPLICITLY requested the OLD TAX REGIME.\n"
            "You MUST present figures ONLY for the Old Regime.\n"
            "DO NOT mention, show, or compare New Regime numbers unless explicitly asked.\n"
            "DO NOT recommend switching to New Regime in this response.\n"
            "=== END REGIME LOCK ===\n"
        )
    elif state.preferred_regime == "new":
        regime_lock_block = (
            "\n=== REGIME LOCK: NEW REGIME ===\n"
            "The user has EXPLICITLY requested the NEW TAX REGIME (Section 115BAC).\n"
            "You MUST present figures ONLY for the New Regime.\n"
            "DO NOT mention, show, or compare Old Regime numbers unless explicitly asked.\n"
            "DO NOT recommend switching to Old Regime in this response.\n"
            "=== END REGIME LOCK ===\n"
        )

    # 2. VERIFIED TAX DATA (from deterministic Python engine)
    verified_tax_block = "No tax calculation performed."
    if state.tax_profile:
        try:
            from tax_engine.tax_tools import format_verified_tax_for_prompt
            verified_tax_block = format_verified_tax_for_prompt(state.tax_profile)
        except Exception:
            if state.tax_result:
                tr = state.tax_result
                verified_tax_block = (
                    "=== VERIFIED TAX DATA (DO NOT OVERRIDE) ===\n"
                    f"Old Regime Tax: Rs.{tr.old_regime_tax:,.0f}\n"
                    f"New Regime Tax: Rs.{tr.new_regime_tax:,.0f}\n"
                    f"Recommended: {tr.recommended_regime} Regime\n"
                    f"Tax Savings: Rs.{tr.tax_savings:,.0f}\n"
                    "=== END VERIFIED TAX DATA ==="
                )
    elif state.tax_result:
        tr = state.tax_result
        verified_tax_block = (
            "=== VERIFIED TAX DATA (DO NOT OVERRIDE) ===\n"
            f"Old Regime Tax: Rs.{tr.old_regime_tax:,.0f}\n"
            f"New Regime Tax: Rs.{tr.new_regime_tax:,.0f}\n"
            f"Recommended: {tr.recommended_regime} Regime\n"
            f"Tax Savings: Rs.{tr.tax_savings:,.0f}\n"
            "=== END VERIFIED TAX DATA ==="
        )

    # 3. OPTIMIZATION
    opt_context = "No optimization analysis performed."
    if state.optimization_result:
        opt = state.optimization_result
        opt_context = opt.summary
        if opt.opportunities:
            lines = [
                f"- {o.get("title", "")}: saves Rs.{o.get("estimated_tax_savings", 0):,.0f}"
                for o in opt.opportunities[:3]
            ]
            opt_context += "\n" + "\n".join(lines)

    # 4. RAG + SECTION WHITELIST
    rag_context = state.rag_context.context if state.rag_context else ""
    citations = state.rag_context.citations if state.rag_context else ""
    section_refs = _extract_section_refs_from_rag(rag_context)
    if section_refs:
        legal_sections_block = (
            f"LEGAL_SECTIONS_REFERENCED (cite ONLY from this list):\n{section_refs}"
        )
    else:
        legal_sections_block = (
            "LEGAL_SECTIONS_REFERENCED: None retrieved. "
            "DO NOT cite any section numbers."
        )

    try:
        prompt = (
            "You are FinAssist AI - an expert Indian tax advisor for FY 2025-26.\n"
            + regime_lock_block
            + "\nCRITICAL ANTI-HALLUCINATION RULES:\n"
            "1. NEVER perform tax calculations yourself. Use ONLY numbers in VERIFIED_TAX_DATA.\n"
            "2. DO NOT explain slab math or deduction arithmetic unless in LEGAL_CONTEXT.\n"
            "3. NEVER invent section numbers not in LEGAL_SECTIONS_REFERENCED.\n"
            "4. Cite ONLY sections from LEGAL_SECTIONS_REFERENCED.\n"
            "5. FREELANCER RULE: Never cite Section 194-I for freelancers. "
            "   Correct sections: income=Section 28, TDS=Section 194J, presumptive=Section 44ADA.\n"
            "6. If LEGAL_CONTEXT is empty, state tax result numbers directly.\n"
            "\nVERIFIED_TAX_DATA:\n"
            + verified_tax_block
            + "\n\nLEGAL_CONTEXT:\n"
            + (rag_context or "No specific legal context retrieved.")
            + "\n\nSOURCES:\n"
            + (citations or "None")
            + "\n\n" + legal_sections_block
            + "\n\nOPTIMIZATION:\n"
            + opt_context
            + f"\n\nUser question: {state.user_query}"
        )
        answer = _call_llm(prompt)
        state.final_answer = answer
    except Exception as e:
        state.final_answer = f"I encountered an error generating the response: {e}"
        state.error = str(e)
    return state


# ===========================================================================
#  NODE 7: Gemini Section Verifier
# ===========================================================================

def gemini_verify_node(state: GraphState) -> GraphState:
    """
    Post-hoc legal section verification using Google Gemini API.
    Verifies section citations in local LLM answer. Does NOT verify tax amounts.
    Silently skips if Gemini is disabled or unavailable.
    """
    state.processing_steps.append("gemini_verification")

    if not settings.gemini_verify_enabled:
        state.gemini_verification = GeminiVerificationResult(skipped=True)
        return state

    if not state.final_answer:
        state.gemini_verification = GeminiVerificationResult(skipped=True)
        return state

    try:
        from recommendation_engine.gemini_verifier import get_verifier
        verifier = get_verifier()
        rag_citations = state.rag_context.citations if state.rag_context else ""
        result = verifier.verify_sections(
            user_question=state.user_query,
            local_answer=state.final_answer,
            rag_citations=rag_citations,
        )
        state.gemini_verification = GeminiVerificationResult(
            verified=result.get("verified", False),
            verified_sections=result.get("verified_sections", []),
            corrections=result.get("corrections", []),
            gemini_raw_response=result.get("gemini_raw_response", ""),
            skipped=result.get("skipped", False),
        )
        if not result.get("skipped") and result.get("corrections"):
            footer = verifier.format_verification_footer(result)
            if footer:
                state.final_answer += footer
    except Exception as e:
        state.gemini_verification = GeminiVerificationResult(
            skipped=True,
            gemini_raw_response=f"Verification skipped: {e}",
        )
    return state
