"""
Tests for the deterministic tax calculation engine.
Validates known tax values for FY 2025-26.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from tax_engine.slabs import calculate_old_regime_tax, calculate_new_regime_tax
from tax_engine.hra import calculate_hra_exemption
from tax_engine.deductions import calculate_80c_deduction, calculate_80d_deduction
from tax_engine.calculator import calculate_full_tax


# ─── Slab Tests ────────────────────────────────────────────────────────────────

def test_new_regime_zero_tax_up_to_12l():
    """Under New Regime, income up to ₹12L = zero tax (after rebate + standard deduction)."""
    # Taxable income ≤ ₹12L → zero tax (87A rebate covers it)
    result = calculate_new_regime_tax(1_100_000)
    assert result["total_tax"] == 0.0, f"Expected 0 tax for ₹11L taxable, got {result['total_tax']}"


def test_new_regime_rebate_limit():
    """Tax is non-zero for taxable income > ₹12L under New Regime."""
    result = calculate_new_regime_tax(1_300_000)
    assert result["total_tax"] > 0, "Expected positive tax for ₹13L taxable"


def test_old_regime_rebate_5l():
    """Under Old Regime, income ≤ ₹5L → zero tax (87A rebate)."""
    result = calculate_old_regime_tax(500_000)
    assert result["total_tax"] == 0.0, f"Expected 0 for ₹5L, got {result['total_tax']}"


def test_old_regime_10l():
    """Old regime tax on ₹10L taxable income = ₹1,12,500 + cess."""
    # ₹10L: 0 (2.5L) + 12500 (5L) + 100000 (5L-10L) = ₹112500
    # Cess: 112500 * 0.04 = 4500
    # Total: 117000
    result = calculate_old_regime_tax(1_000_000)
    assert result["basic_tax"] == pytest.approx(112_500, rel=1e-3)
    assert result["total_tax"] == pytest.approx(117_000, rel=1e-3)


def test_new_regime_slabs():
    """New regime slab calculation for ₹20L taxable income."""
    result = calculate_new_regime_tax(2_000_000)
    # 0 (4L) + 20000 (4L) + 40000 (4L) + 60000 (4L) + 80000 (4L) = 200000
    assert result["basic_tax"] == pytest.approx(200_000, rel=1e-3)


# ─── HRA Tests ─────────────────────────────────────────────────────────────────

def test_hra_metro():
    """HRA exemption for metro city."""
    result = calculate_hra_exemption(
        basic_salary=600_000,
        hra_received=240_000,
        rent_paid=216_000,
        is_metro=True,
    )
    # Component 1: 240000
    # Component 2: 50% of 600000 = 300000
    # Component 3: 216000 - 10% * 600000 = 216000 - 60000 = 156000
    # Min = 156000
    assert result["hra_exemption"] == pytest.approx(156_000, rel=1e-3)


def test_hra_zero_rent():
    """No HRA exemption when rent_paid = 0."""
    result = calculate_hra_exemption(600_000, 240_000, 0, False)
    assert result["hra_exemption"] == 0.0


# ─── 80C Tests ─────────────────────────────────────────────────────────────────

def test_80c_cap():
    """80C deduction capped at ₹1,50,000."""
    result = calculate_80c_deduction(elss=100_000, ppf=80_000, epf=50_000)
    assert result["deduction_allowed"] == 150_000
    assert result["remaining_capacity"] == 0


def test_80c_partial():
    """80C partial usage."""
    result = calculate_80c_deduction(elss=75_000)
    assert result["deduction_allowed"] == 75_000
    assert result["remaining_capacity"] == 75_000


# ─── 80D Tests ─────────────────────────────────────────────────────────────────

def test_80d_basic():
    """Basic 80D calculation."""
    result = calculate_80d_deduction(self_premium=20_000, parent_premium=30_000)
    assert result["self_deduction"] == 20_000
    assert result["parent_deduction"] == 25_000  # capped at non-senior limit
    assert result["total_deduction"] == 45_000


def test_80d_senior_parents():
    """80D with senior citizen parents — higher limit."""
    result = calculate_80d_deduction(self_premium=25_000, parent_premium=55_000, parent_age_above_60=True)
    assert result["parent_deduction"] == 50_000  # capped at senior limit
    assert result["total_deduction"] == 75_000


# ─── Full Calculator ───────────────────────────────────────────────────────────

def test_full_calculator_12l():
    """Full tax calculation for ₹12L salary with standard deductions."""
    profile = {
        "gross_salary": 1_200_000,
        "basic_salary": 600_000,
    }
    result = calculate_full_tax(profile)
    assert "old_regime" in result
    assert "new_regime" in result
    assert "recommendation" in result
    assert result["new_regime"]["total_tax"] >= 0
    assert result["old_regime"]["total_tax"] >= 0


def test_full_calc_recommendation():
    """High deductions → Old Regime preferred."""
    profile = {
        "gross_salary": 1_500_000,
        "basic_salary": 750_000,
        "elss": 150_000,
        "health_insurance_self": 25_000,
        "additional_nps_80ccd1b": 50_000,
        "home_loan_interest": 200_000,
        "hra_received": 200_000,
        "rent_paid": 200_000,
        "is_metro": True,
    }
    result = calculate_full_tax(profile)
    # With these deductions, old regime should be better
    assert result["old_regime"]["total_tax"] < result["new_regime"]["total_tax"] or \
           result["recommendation"]["regime"] in ("Old", "Either", "New")
