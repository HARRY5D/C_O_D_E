"""
Tax Assistant — Primary chat interface with LangGraph orchestration.
Supports both Chat Mode (no upload) and Document Mode (Form16 upload).
"""
import os
import sys
import tempfile
import streamlit as st
from frontend.components.cards import source_citation_card


def _extract_result(result: dict) -> tuple:
    """
    Safely extract (answer, citations, steps) from a run_query() result.
    run_query() always returns a plain dict (model_dump'd), so all values
    including rag_context are plain dicts — no Pydantic objects.
    """
    answer = result.get("final_answer") or "I couldn't generate a response."

    rag_ctx = result.get("rag_context") or {}
    if isinstance(rag_ctx, dict):
        citations = rag_ctx.get("citations", "")
    elif hasattr(rag_ctx, "citations"):   # safety net for Pydantic object
        citations = rag_ctx.citations or ""
    else:
        citations = ""

    steps = result.get("processing_steps") or []
    return answer, citations, steps


def _run_query_and_store(user_query: str, mode: str):
    """Run the LangGraph query and append the assistant reply to session messages."""
    with st.spinner("🔍 Analyzing your question..."):
        try:
            from recommendation_engine.graph import run_query

            form16_path = (
                st.session_state.form16_path
                if mode == "📄 Document Mode (Form16)"
                else None
            )

            result = run_query(
                user_query=user_query,
                mode="document" if form16_path else "chat",
                form16_path=form16_path,
            )

            answer, citations, steps = _extract_result(result)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "citations": citations,
                "steps": steps,
            })

        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"❌ **Error:** {str(e)}\n\nIf it's a retrieval error, ensure the RAG index is built:\n```\npython scripts/build_index.py\n```",
                "citations": "",
                "steps": [],
            })


def show_tax_assistant():
    st.markdown('<p class="section-header">💬 Tax Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Ask anything about Indian taxes — backed by legal documents & AI</p>', unsafe_allow_html=True)

    # ─── Session state init ────────────────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "form16_path" not in st.session_state:
        st.session_state.form16_path = None
    if "pending_query" not in st.session_state:
        st.session_state.pending_query = None   # for suggestion button flow

    # ─── Mode selector + Form16 upload ────────────────────────────────────────
    col1, col2 = st.columns([2, 1])
    with col1:
        mode = st.radio(
            "Mode",
            options=["💬 Chat Mode", "📄 Document Mode (Form16)"],
            horizontal=True,
            help="Chat Mode: ask any question. Document Mode: upload Form16 for personalized analysis.",
            key="mode_selector",
        )

    with col2:
        if mode == "📄 Document Mode (Form16)":
            uploaded = st.file_uploader("Upload Form 16 PDF", type=["pdf"], key="form16_upload")
            if uploaded:
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                    tmp.write(uploaded.read())
                    st.session_state.form16_path = tmp.name
                st.success("✅ Form 16 uploaded!")
        else:
            st.session_state.form16_path = None

    st.divider()

    # ─── Suggestion buttons ────────────────────────────────────────────────────
    # Only show when chat is empty AND no pending query
    if not st.session_state.messages and st.session_state.pending_query is None:
        st.markdown("**💡 Try asking:**")
        suggestions = [
            "I earn ₹12 lakh. Which tax regime should I choose?",
            "Can I claim both HRA and home loan deductions?",
            "What is the 80C deduction limit for FY 2025-26?",
            "I invested ₹75,000 in ELSS. What else can I claim?",
            "How much can I save with NPS investment?",
        ]
        cols = st.columns(len(suggestions))
        for i, (col, s) in enumerate(zip(cols, suggestions)):
            with col:
                if st.button(s, key=f"sugg_{i}", use_container_width=True):
                    # Store as pending query so we can process it after rerun
                    st.session_state.messages.append({"role": "user", "content": s})
                    st.session_state.pending_query = s
                    st.rerun()
        st.markdown("")

    # ─── Process pending query (from suggestion button) ────────────────────────
    if st.session_state.pending_query is not None:
        query = st.session_state.pending_query
        st.session_state.pending_query = None   # clear BEFORE calling so no loop
        _run_query_and_store(query, mode)
        st.rerun()

    # ─── Chat history display ──────────────────────────────────────────────────
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-user">
                <p class="chat-label" style="color:#4ECDC4;">You</p>
                <p style="margin:0;">{msg["content"]}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-assistant">
                <p class="chat-label" style="color:#FF6B6B;">FinAssist AI</p>
                <div style="margin:0;">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

            # Citations expander
            citations = msg.get("citations", "")
            if citations:
                with st.expander("📚 Sources", expanded=False):
                    for cite in citations.split("\n"):
                        if cite.strip():
                            st.markdown(f"- {cite.strip()}")

            # Processing steps (debug info)
            steps = msg.get("steps", [])
            if steps:
                with st.expander("🔬 Processing steps", expanded=False):
                    st.markdown(" → ".join(steps))

    # ─── Chat input (typed queries) ────────────────────────────────────────────
    user_input = st.chat_input("Ask a tax question...", key="chat_input")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        _run_query_and_store(user_input, mode)
        st.rerun()

    # ─── Clear chat ─────────────────────────────────────────────────────────────
    if st.session_state.messages:
        st.markdown("---")
        if st.button("🗑️ Clear Conversation", key="clear_chat"):
            st.session_state.messages = []
            st.session_state.pending_query = None
            st.rerun()
