"""
LangGraph Orchestrator — central workflow graph for FinAssist AI (v3).

Fixed flow:
  detect_intent
      │
  [form16_parser?]      ← only if form16 uploaded
      │
  [tax_engine?]         ← only if tax_profile available
      │
  [optimize?]           ← only if optimization intent AND tax_result available
      │
  [retrieve_context?]   ← only if needs_retrieval=True (SKIPPED for general_chat etc.)
      │
  generate_answer       ← always
      │
  END
"""
from langgraph.graph import StateGraph, END
from recommendation_engine.state import GraphState
from recommendation_engine.nodes import (
    detect_intent_node,
    form16_parser_node,
    tax_engine_node,
    optimization_node,
    rag_retrieve_node,
    generate_answer_node,
)


# ─── Routing functions ─────────────────────────────────────────────────────────

def route_after_intent(state: GraphState) -> str:
    if state.needs_form16 and state.form16_path:
        return "parse_form16"
    return "maybe_calculate"


def route_maybe_calculate(state: GraphState) -> str:
    if state.needs_calculation and bool(state.tax_profile):
        return "calculate_tax"
    return "maybe_optimize"


def route_after_calculate(state: GraphState) -> str:
    if state.needs_optimization and state.tax_result is not None:
        return "optimize"
    return "maybe_retrieve"


def route_after_optimize(state: GraphState) -> str:
    return "maybe_retrieve"


def route_maybe_retrieve(state: GraphState) -> str:
    """Skip retrieval for general_chat or any intent that doesn't need it."""
    if state.needs_retrieval:
        return "retrieve"
    return "generate"


# ─── Passthrough nodes ─────────────────────────────────────────────────────────

def maybe_calculate_node(state: GraphState) -> GraphState:
    return state


def maybe_optimize_node(state: GraphState) -> GraphState:
    return state


def maybe_retrieve_node(state: GraphState) -> GraphState:
    return state


# ─── Graph builder ─────────────────────────────────────────────────────────────

def build_finassist_graph():
    """Construct and compile the FinAssist LangGraph workflow (v3)."""
    workflow = StateGraph(GraphState)

    # ─── Processing nodes ──────────────────────────────────────────────────────
    workflow.add_node("detect_intent",    detect_intent_node)
    workflow.add_node("parse_form16",     form16_parser_node)
    workflow.add_node("calculate_tax",    tax_engine_node)
    workflow.add_node("optimize",         optimization_node)
    workflow.add_node("retrieve_context", rag_retrieve_node)
    workflow.add_node("generate_answer",  generate_answer_node)

    # ─── Passthrough routing nodes ─────────────────────────────────────────────
    workflow.add_node("maybe_calculate", maybe_calculate_node)
    workflow.add_node("maybe_optimize",  maybe_optimize_node)
    workflow.add_node("maybe_retrieve",  maybe_retrieve_node)

    # ─── Entry point ───────────────────────────────────────────────────────────
    workflow.set_entry_point("detect_intent")

    # 1. Intent → form16 OR maybe_calculate
    workflow.add_conditional_edges(
        "detect_intent",
        route_after_intent,
        {
            "parse_form16":    "parse_form16",
            "maybe_calculate": "maybe_calculate",
        },
    )

    # 2. Form16 → maybe_calculate
    workflow.add_conditional_edges(
        "parse_form16",
        route_maybe_calculate,
        {
            "calculate_tax":  "calculate_tax",
            "maybe_optimize": "maybe_optimize",
        },
    )

    # 3. maybe_calculate → calculate or skip to maybe_optimize
    workflow.add_conditional_edges(
        "maybe_calculate",
        route_maybe_calculate,
        {
            "calculate_tax":  "calculate_tax",
            "maybe_optimize": "maybe_optimize",
        },
    )

    # 4. calculate_tax → optimize or maybe_retrieve
    workflow.add_conditional_edges(
        "calculate_tax",
        route_after_calculate,
        {
            "optimize":       "optimize",
            "maybe_retrieve": "maybe_retrieve",
        },
    )

    # 5. optimize → maybe_retrieve
    workflow.add_edge("optimize", "maybe_retrieve")

    # 6. maybe_optimize → maybe_retrieve
    workflow.add_edge("maybe_optimize", "maybe_retrieve")

    # 7. maybe_retrieve → retrieve (if needs_retrieval) OR generate (skip retrieval)
    workflow.add_conditional_edges(
        "maybe_retrieve",
        route_maybe_retrieve,
        {
            "retrieve": "retrieve_context",
            "generate": "generate_answer",
        },
    )

    # 8. retrieve_context → generate
    workflow.add_edge("retrieve_context", "generate_answer")

    # 9. generate → END
    workflow.add_edge("generate_answer", END)

    return workflow.compile()


# ─── Singleton compiled graph ──────────────────────────────────────────────────
_compiled_graph = None


def get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_finassist_graph()
    return _compiled_graph


def run_query(
    user_query: str,
    mode: str = "chat",
    tax_profile: dict = None,
    form16_path: str = None,
    chat_history: list = None,
) -> dict:
    """
    Run a user query through the full LangGraph workflow.

    Always returns a plain Python dict (all nested Pydantic models
    serialized via model_dump()). Safe to use with .get() everywhere.
    """
    try:
        from config.langsmith_config import configure_langsmith
        configure_langsmith()
    except Exception:
        pass

    initial_state = GraphState(
        user_query=user_query,
        mode=mode,
        tax_profile=tax_profile or {},
        form16_path=form16_path,
        chat_history=chat_history or [],
    )

    graph = get_graph()
    raw = graph.invoke(initial_state)

    # ── Normalize to a plain dict (no Pydantic sub-objects) ───────────────────
    # LangGraph can return a dict with Pydantic objects as values (e.g. rag_context
    # is a RetrievedContext instance inside a dict). Calling model_dump() converts
    # everything to plain Python types so the frontend can safely use .get().
    if hasattr(raw, "model_dump"):
        # raw is already a Pydantic GraphState
        return raw.model_dump()
    if isinstance(raw, dict):
        # raw is a dict but values may still be Pydantic objects — reconstruct then dump
        try:
            return GraphState(**raw).model_dump()
        except Exception:
            # Fallback: manually convert any Pydantic values
            clean = {}
            for k, v in raw.items():
                clean[k] = v.model_dump() if hasattr(v, "model_dump") else v
            return clean

    return raw  # should never reach here
