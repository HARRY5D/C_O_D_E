"""
Tax Engine Tool Wrappers — FY 2025-26
======================================
Wraps every tax engine function with a clean callable interface that:
  1. Validates and coerces inputs
  2. Calls the deterministic Python function
  3. Stamps the result with `source: "tax_engine_deterministic"` so the
     LLM prompt can clearly mark these numbers as non-overridable.

Usage in nodes.py:
    from tax_engine.tax_tools import run_all_tax_tools
    verified_data = run_all_tax_tools(tax_profile)
    # Inject verified_data into the LLM prompt as VERIFIED_TAX_DATA
"""
import json
from typing import Any

from tax_engine.calculator import calculate_full_tax
from tax_engine.hra import calculate_hra_exemption
from tax_engine.deductions import (
    calculate_80c_deduction,
    calculate_80d_deduction,
    calculate_80ccd1b_deduction,
    calculate_80tta_deduction,
)
from tax_engine.nps import calculate_nps_deductions
from tax_engine.home_loan import calculate_home_loan_deductions


# ─── Individual tool wrappers ──────────────────────────────────────────────────

def tool_calculate_full_tax(profile: dict) -> dict:
    """
    Run full tax calculation for both regimes.
    Returns result stamped with source key so LLM cannot claim it computed this.
    """
    try:
        result = calculate_full_tax(profile)
        result["source"] = "tax_engine_deterministic"
        result["trust_level"] = "AUTHORITATIVE — DO NOT OVERRIDE"
        return result
    except Exception as e:
        return {
            "source": "tax_engine_deterministic",
            "error": str(e),
            "trust_level": "AUTHORITATIVE — DO NOT OVERRIDE",
        }


def tool_calculate_hra(
    basic_salary: float,
    hra_received: float,
    rent_paid: float,
    is_metro: bool = False,
) -> dict:
    """HRA exemption calculation (Old Regime only — Section 10(13A))."""
    try:
        result = calculate_hra_exemption(basic_salary, hra_received, rent_paid, is_metro)
        result["source"] = "tax_engine_deterministic"
        result["section"] = "Section 10(13A)"
        return result
    except Exception as e:
        return {"source": "tax_engine_deterministic", "error": str(e)}


def tool_calculate_80c(
    elss: float = 0, ppf: float = 0, epf: float = 0,
    life_insurance: float = 0, home_loan_principal: float = 0,
    nsc: float = 0, tuition_fees: float = 0, sukanya_samriddhi: float = 0,
    tax_saver_fd: float = 0, others: float = 0,
) -> dict:
    """Section 80C deduction (max ₹1,50,000)."""
    try:
        result = calculate_80c_deduction(
            elss=elss, ppf=ppf, epf=epf, life_insurance=life_insurance,
            home_loan_principal=home_loan_principal, nsc=nsc,
            tuition_fees=tuition_fees, sukanya_samriddhi=sukanya_samriddhi,
            tax_saver_fd=tax_saver_fd, others=others,
        )
        result["source"] = "tax_engine_deterministic"
        result["section"] = "Section 80C"
        result["max_limit"] = 150000
        return result
    except Exception as e:
        return {"source": "tax_engine_deterministic", "error": str(e)}


def tool_calculate_80d(
    self_premium: float = 0, parent_premium: float = 0,
    self_age_above_60: bool = False, parent_age_above_60: bool = False,
    preventive_health_checkup: float = 0,
) -> dict:
    """Section 80D health insurance deduction."""
    try:
        result = calculate_80d_deduction(
            self_premium=self_premium, parent_premium=parent_premium,
            self_age_above_60=self_age_above_60, parent_age_above_60=parent_age_above_60,
            preventive_health_checkup=preventive_health_checkup,
        )
        result["source"] = "tax_engine_deterministic"
        result["section"] = "Section 80D"
        return result
    except Exception as e:
        return {"source": "tax_engine_deterministic", "error": str(e)}


def tool_calculate_nps(
    basic_salary: float = 0, employee_nps: float = 0,
    employer_nps: float = 0, additional_nps_80ccd1b: float = 0,
    is_govt_employer: bool = False,
) -> dict:
    """NPS deductions: 80CCD(1), 80CCD(1B), 80CCD(2)."""
    try:
        result = calculate_nps_deductions(
            basic_salary=basic_salary, employee_nps=employee_nps,
            employer_nps=employer_nps, additional_nps_80ccd1b=additional_nps_80ccd1b,
            is_govt_employer=is_govt_employer,
        )
        result["source"] = "tax_engine_deterministic"
        result["sections"] = ["Section 80CCD(1)", "Section 80CCD(1B)", "Section 80CCD(2)"]
        return result
    except Exception as e:
        return {"source": "tax_engine_deterministic", "error": str(e)}


def tool_calculate_home_loan(
    principal_repaid: float = 0, interest_paid: float = 0,
    is_self_occupied: bool = True, is_first_time_buyer_80eea: bool = False,
    stamp_duty_value_lakh: float = 0,
) -> dict:
    """Home loan deductions: Section 24b (interest) + Section 80EEA (first-time buyer)."""
    try:
        result = calculate_home_loan_deductions(
            principal_repaid=principal_repaid, interest_paid=interest_paid,
            is_self_occupied=is_self_occupied,
            is_first_time_buyer_80eea=is_first_time_buyer_80eea,
            stamp_duty_value_lakh=stamp_duty_value_lakh,
        )
        result["source"] = "tax_engine_deterministic"
        result["sections"] = ["Section 24(b)", "Section 80EEA"]
        return result
    except Exception as e:
        return {"source": "tax_engine_deterministic", "error": str(e)}


def tool_calculate_80tta(savings_interest: float = 0) -> dict:
    """Section 80TTA — savings account interest deduction (max ₹10,000)."""
    try:
        result = calculate_80tta_deduction(savings_interest)
        result["source"] = "tax_engine_deterministic"
        result["section"] = "Section 80TTA"
        result["max_limit"] = 10000
        return result
    except Exception as e:
        return {"source": "tax_engine_deterministic", "error": str(e)}


# ─── Master runner: calls all applicable tools and returns one JSON block ──────

def run_all_tax_tools(profile: dict) -> dict:
    """
    Run all relevant tax tools for a given profile.
    Returns a single structured dict to be injected into the LLM prompt
    as VERIFIED_TAX_DATA.

    The LLM is strictly forbidden from overriding or recalculating any of
    these numbers. They are authoritative Python outputs.
    """
    g = profile
    gross = float(g.get("gross_salary", 0))
    basic = float(g.get("basic_salary", gross * 0.5))

    full_tax = tool_calculate_full_tax(profile)
    hra = tool_calculate_hra(
        basic_salary=basic,
        hra_received=float(g.get("hra_received", 0)),
        rent_paid=float(g.get("rent_paid", 0)),
        is_metro=bool(g.get("is_metro", False)),
    )
    sec_80c = tool_calculate_80c(
        elss=float(g.get("elss", 0)),
        ppf=float(g.get("ppf", 0)),
        epf=float(g.get("epf", 0)),
        life_insurance=float(g.get("life_insurance", 0)),
        home_loan_principal=float(g.get("home_loan_principal", 0)),
        nsc=float(g.get("nsc", 0)),
        tuition_fees=float(g.get("tuition_fees", 0)),
        sukanya_samriddhi=float(g.get("sukanya_samriddhi", 0)),
        tax_saver_fd=float(g.get("tax_saver_fd", 0)),
        others=float(g.get("other_80c", 0)),
    )
    sec_80d = tool_calculate_80d(
        self_premium=float(g.get("health_insurance_self", 0)),
        parent_premium=float(g.get("health_insurance_parents", 0)),
        self_age_above_60=bool(g.get("self_age_above_60", False)),
        parent_age_above_60=bool(g.get("parent_age_above_60", False)),
        preventive_health_checkup=float(g.get("preventive_checkup", 0)),
    )
    nps = tool_calculate_nps(
        basic_salary=basic,
        employee_nps=float(g.get("employee_nps", 0)),
        employer_nps=float(g.get("employer_nps", 0)),
        additional_nps_80ccd1b=float(g.get("additional_nps_80ccd1b", 0)),
        is_govt_employer=bool(g.get("is_govt_employer", False)),
    )
    home_loan = tool_calculate_home_loan(
        principal_repaid=float(g.get("home_loan_principal", 0)),
        interest_paid=float(g.get("home_loan_interest", 0)),
        is_self_occupied=bool(g.get("is_self_occupied", True)),
        is_first_time_buyer_80eea=bool(g.get("is_first_time_buyer", False)),
        stamp_duty_value_lakh=float(g.get("stamp_duty_value_lakh", 0)),
    )
    sec_80tta = tool_calculate_80tta(float(g.get("savings_interest", 0)))

    return {
        "trust_level": "AUTHORITATIVE — DO NOT OVERRIDE",
        "source": "tax_engine_deterministic",
        "is_freelancer": bool(g.get("is_freelancer", False)),
        "gross_salary": gross,
        "full_tax_result": full_tax,
        "hra_exemption": hra,
        "sec_80c": sec_80c,
        "sec_80d": sec_80d,
        "nps_deductions": nps,
        "home_loan": home_loan,
        "sec_80tta": sec_80tta,
    }


def format_verified_tax_for_prompt(profile: dict) -> str:
    """
    Run all tools and return a formatted string to embed in the LLM prompt.
    The format clearly marks the data as authoritative and non-overridable.
    """
    data = run_all_tax_tools(profile)
    full = data.get("full_tax_result", {})

    # Extract key numbers cleanly
    old_tax = full.get("old_regime", {}).get("total_tax", 0)
    new_tax = full.get("new_regime", {}).get("total_tax", 0)
    recommended = full.get("recommendation", {}).get("regime", "N/A")
    savings = full.get("recommendation", {}).get("tax_savings", 0)
    is_freelancer = data.get("is_freelancer", False)
    gross = data.get("gross_salary", 0)

    lines = [
        "=== VERIFIED TAX DATA (Deterministic Python Engine — DO NOT OVERRIDE) ===",
        f"Source: tax_engine_deterministic | Trust: AUTHORITATIVE",
        f"Gross Income: ₹{gross:,.0f}",
        f"Taxpayer Type: {'Freelancer/Professional (Section 44ADA applies)' if is_freelancer else 'Salaried Employee'}",
        "",
        f"OLD REGIME TAX:  ₹{old_tax:,.0f}",
        f"  Taxable Income: ₹{full.get('old_regime', {}).get('taxable_income', 0):,.0f}",
        f"  Total Deductions: ₹{full.get('old_regime', {}).get('total_deductions', 0):,.0f}",
        "",
        f"NEW REGIME TAX:  ₹{new_tax:,.0f}",
        f"  Taxable Income: ₹{full.get('new_regime', {}).get('taxable_income', 0):,.0f}",
        f"  Total Deductions: ₹{full.get('new_regime', {}).get('total_deductions', 0):,.0f}",
        "",
        f"RECOMMENDED: {recommended} Regime | Tax Savings: ₹{savings:,.0f}",
        "=== END VERIFIED TAX DATA ===",
        "",
        "CRITICAL INSTRUCTION: The numbers above are final. You MUST use only these numbers.",
        "DO NOT recalculate, rephrase the math, or derive different numbers.",
        "If you arrive at a different number, you are WRONG. Trust the engine.",
    ]
    return "\n".join(lines)
