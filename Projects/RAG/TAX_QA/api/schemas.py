"""
API Request/Response Schemas — Pydantic models for all FastAPI endpoints.
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


# ─── Query endpoint ───────────────────────────────────────────────────────────
class QueryRequest(BaseModel):
    question: str = Field(..., description="User's tax question", min_length=3)
    mode: str = Field(default="chat", description="'chat' or 'document'")
    tax_profile: Optional[Dict[str, Any]] = Field(default=None, description="Optional income/deduction profile")
    form16_path: Optional[str] = Field(default=None, description="Optional path to Form 16 PDF")


class SourceDoc(BaseModel):
    text: str
    source: str
    section: str
    score: float


class QueryResponse(BaseModel):
    question: str
    answer: str
    citations: str
    source_docs: List[Dict[str, Any]]
    processing_steps: List[str]
    intent: str


# ─── Tax calculation endpoint ──────────────────────────────────────────────────
class TaxCalculationRequest(BaseModel):
    gross_salary: float = Field(..., ge=0, description="Annual gross salary in INR")
    basic_salary: Optional[float] = Field(default=None)
    hra_received: Optional[float] = Field(default=0)
    rent_paid: Optional[float] = Field(default=0)
    is_metro: Optional[bool] = Field(default=False)
    elss: Optional[float] = Field(default=0)
    ppf: Optional[float] = Field(default=0)
    epf: Optional[float] = Field(default=0)
    life_insurance: Optional[float] = Field(default=0)
    home_loan_principal: Optional[float] = Field(default=0)
    nsc: Optional[float] = Field(default=0)
    other_80c: Optional[float] = Field(default=0)
    health_insurance_self: Optional[float] = Field(default=0)
    health_insurance_parents: Optional[float] = Field(default=0)
    self_age_above_60: Optional[bool] = Field(default=False)
    parent_age_above_60: Optional[bool] = Field(default=False)
    employee_nps: Optional[float] = Field(default=0)
    employer_nps: Optional[float] = Field(default=0)
    additional_nps_80ccd1b: Optional[float] = Field(default=0)
    home_loan_interest: Optional[float] = Field(default=0)
    is_self_occupied: Optional[bool] = Field(default=True)
    savings_interest: Optional[float] = Field(default=0)
    other_income: Optional[float] = Field(default=0)


class RegimeResult(BaseModel):
    regime: str
    taxable_income: float
    total_tax: float
    effective_rate: float
    total_deductions: float


class TaxCalculationResponse(BaseModel):
    old_regime: RegimeResult
    new_regime: RegimeResult
    recommendation: Dict[str, Any]
    detail: Dict[str, Any]


# ─── Optimization endpoint ────────────────────────────────────────────────────
class OptimizationResponse(BaseModel):
    current_old_regime_tax: float
    current_new_regime_tax: float
    total_potential_additional_savings: float
    summary: str
    opportunities: List[Dict[str, Any]]


# ─── Compare regimes endpoint ──────────────────────────────────────────────────
class RegimeCompareResponse(BaseModel):
    old_regime: RegimeResult
    new_regime: RegimeResult
    recommendation: Dict[str, Any]
    break_even_analysis: Dict[str, Any]


# ─── Form16 endpoint ───────────────────────────────────────────────────────────
class Form16Response(BaseModel):
    extracted: bool
    gross_salary: float
    tds_deducted: float
    taxable_income: float
    deductions: Dict[str, Any]
    tax_computation: Dict[str, Any]
    confidence: float
    notes: List[str]
    tax_analysis: Optional[Dict[str, Any]] = None
