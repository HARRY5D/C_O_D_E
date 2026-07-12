"""
Form 16 Schema — Pydantic models for structured Form 16 extraction.
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class Part_A(BaseModel):
    """Form 16 Part A — TDS details from employer."""
    employer_name: Optional[str] = None
    employer_tan: Optional[str] = None
    employer_pan: Optional[str] = None
    employee_pan: Optional[str] = None
    assessment_year: Optional[str] = "2026-27"
    financial_year: Optional[str] = "2025-26"
    gross_salary: Optional[float] = 0.0
    tds_deducted: Optional[float] = 0.0
    tds_deposited: Optional[float] = 0.0


class Part_B(BaseModel):
    """Form 16 Part B — Salary breakdown and deductions."""
    # Income
    gross_salary: Optional[float] = 0.0
    basic_salary: Optional[float] = 0.0
    hra_received: Optional[float] = 0.0
    special_allowance: Optional[float] = 0.0
    other_allowances: Optional[float] = 0.0

    # Exemptions
    hra_exemption: Optional[float] = 0.0
    lta_exemption: Optional[float] = 0.0
    other_exemptions: Optional[float] = 0.0

    # Standard deduction
    standard_deduction: Optional[float] = 50000.0

    # Chapter VI-A Deductions
    sec_80c: Optional[float] = 0.0
    sec_80ccd1b: Optional[float] = 0.0
    sec_80d: Optional[float] = 0.0
    sec_80e: Optional[float] = 0.0
    sec_80g: Optional[float] = 0.0
    sec_80tta: Optional[float] = 0.0
    other_deductions: Optional[float] = 0.0
    total_deductions_chapter_via: Optional[float] = 0.0

    # Tax computation
    taxable_income: Optional[float] = 0.0
    tax_on_income: Optional[float] = 0.0
    rebate_87a: Optional[float] = 0.0
    surcharge: Optional[float] = 0.0
    cess: Optional[float] = 0.0
    total_tax_payable: Optional[float] = 0.0
    tds_deducted: Optional[float] = 0.0

    # NPS
    employer_nps_80ccd2: Optional[float] = 0.0


class Form16Data(BaseModel):
    """Complete Form 16 extraction result."""
    part_a: Part_A = Field(default_factory=Part_A)
    part_b: Part_B = Field(default_factory=Part_B)
    raw_text_preview: Optional[str] = None
    extraction_confidence: Optional[float] = 0.0
    parsing_notes: Optional[List[str]] = Field(default_factory=list)

    def to_tax_profile(self) -> dict:
        """Convert Form 16 data to tax calculator profile dict."""
        b = self.part_b
        return {
            "gross_salary": b.gross_salary or 0,
            "basic_salary": b.basic_salary or (b.gross_salary * 0.5 if b.gross_salary else 0),
            "hra_received": b.hra_received or 0,
            "elss": 0,  # Not in Form 16 directly
            "ppf": 0,
            "epf": 0,
            "life_insurance": 0,
            "health_insurance_self": b.sec_80d or 0,
            "additional_nps_80ccd1b": b.sec_80ccd1b or 0,
            "employer_nps": b.employer_nps_80ccd2 or 0,
            "other_80c": b.sec_80c or 0,
            "savings_interest": b.sec_80tta or 0,
        }
