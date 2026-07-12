"""
LangSmith Configuration for FinAssist AI.

With Ollama (local LLM), tracing still works automatically because:
- ChatOllama is a LangChain object
- LangChain auto-traces all LLM calls when LANGCHAIN_TRACING_V2=true is set
- You will see every prompt, response, latency, and token count in LangSmith

No wrap_gemini or special Gemini setup needed.

Usage:
    from config.langsmith_config import configure_langsmith
    configure_langsmith()
"""
import os
from config.settings import settings


_configured = False


def configure_langsmith() -> None:
    """Set all required LangSmith + LangChain tracing environment variables.
    Idempotent — safe to call multiple times, only configures once per process.
    ChatOllama will be traced automatically once these are set.
    """
    global _configured
    if _configured:
        return
    _configured = True

    api_key  = settings.langsmith_api_key
    endpoint = settings.langsmith_endpoint
    project  = settings.langsmith_project

    # ── LangSmith native vars (LangSmith SDK >= 0.1) ──────────────────────────
    os.environ["LANGSMITH_TRACING"]  = "true"
    os.environ["LANGSMITH_API_KEY"]  = api_key
    os.environ["LANGSMITH_ENDPOINT"] = endpoint
    os.environ["LANGSMITH_PROJECT"]  = project

    # ── LangChain tracing vars (required by langchain-core / LangGraph) ───────
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"]    = api_key
    os.environ["LANGCHAIN_ENDPOINT"]   = endpoint
    os.environ["LANGCHAIN_PROJECT"]    = project


# ── COMMENTED OUT — Gemini client no longer needed (using Ollama locally) ──────
#
# def get_gemini_client():
#     """Return a LangSmith-traced google-genai client using wrappers.wrap_gemini()."""
#     try:
#         from google import genai
#         from langsmith import wrappers
#         gemini_client = genai.Client()
#         traced_client = wrappers.wrap_gemini(
#             gemini_client,
#             tracing_extra={
#                 "tags": ["gemini", "finassist-ai"],
#                 "metadata": {"project": settings.langsmith_project},
#             },
#         )
#         return traced_client
#     except ImportError:
#         from google import genai
#         return genai.Client()
