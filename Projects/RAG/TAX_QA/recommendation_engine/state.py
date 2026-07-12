"""
LangGraph State — typed state schema for the FinAssist AI workflow.
"""
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field


class UserMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class TaxEngineResult(BaseModel):
    """Result from deterministic tax calculation."""
    old_regime_tax: float = 0.0
    new_regime_tax: float = 0.0
    recommended_regime: str = ""
    tax_savings: float = 0.0
    full_result: Dict[str, Any] = Field(default_factory=dict)


class RetrievedContext(BaseModel):
    """Result from RAG retrieval."""
    context: str = ""
    citations: str = ""
    source_docs: List[Dict[str, Any]] = Field(default_factory=list)


class OptimizationResult(BaseModel):
    """Result from tax optimization engine."""
    total_potential_savings: float = 0.0
    opportunities: List[Dict[str, Any]] = Field(default_factory=list)
    summary: str = ""


class Form16Result(BaseModel):
    """Result from Form 16 extraction."""
    extracted: bool = False
    data: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 0.0
    notes: List[str] = Field(default_factory=list)


class GraphState(BaseModel):
    """
    Central state for LangGraph workflow.
    All nodes read from and write to this shared state.
    """
    # Input
    user_query: str = ""
    mode: Literal["chat", "document"] = "chat"
    tax_profile: Dict[str, Any] = Field(default_factory=dict)
    form16_path: Optional[str] = None
    chat_history: List[UserMessage] = Field(default_factory=list)

    # Intent detection
    intent: Literal[
        "tax_question",
        "calculation_request",
        "optimization_request",
        "form16_analysis",
        "regime_comparison",
        "general_chat",
    ] = "tax_question"
    needs_calculation: bool = False
    needs_retrieval: bool = True
    needs_optimization: bool = False
    needs_form16: bool = False

    # Intermediate results
    tax_result: Optional[TaxEngineResult] = None
    rag_context: Optional[RetrievedContext] = None
    optimization_result: Optional[OptimizationResult] = None
    form16_result: Optional[Form16Result] = None

    # Final output
    final_answer: str = ""
    processing_steps: List[str] = Field(default_factory=list)
    error: Optional[str] = None
