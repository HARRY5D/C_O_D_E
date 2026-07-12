"""
Tax Slab Rules — FY 2025-26 / AY 2026-27
Both Old and New Regime. No LLM involvement.
"""
from dataclasses import dataclass
from typing import List, Tuple


# ─────────────────────────────────────────────────
#  Slab definitions: list of (upper_limit, rate)
#  upper_limit = None → no upper bound (top slab)
# ─────────────────────────────────────────────────

OLD_REGIME_SLABS: List[Tuple[int | None, float]] = [
    (250_000, 0.00),
    (500_000, 0.05),
    (1_000_000, 0.20),
    (None, 0.30),
]

# New Regime 2025-26 (Budget 2025 revised slabs)
NEW_REGIME_SLABS: List[Tuple[int | None, float]] = [
    (400_000, 0.00),
    (800_000, 0.05),
    (1_200_000, 0.10),
    (1_600_000, 0.15),
    (2_000_000, 0.20),
    (2_400_000, 0.25),
    (None, 0.30),
]

# Surcharge slabs (same for both regimes)
SURCHARGE_SLABS: List[Tuple[int | None, float]] = [
    (5_000_000, 0.00),
    (10_000_000, 0.10),
    (20_000_000, 0.15),
    (50_000_000, 0.25),
    (None, 0.25),   # Capped at 25% for new regime (was 37% for old, but capped)
]

HEALTH_EDUCATION_CESS: float = 0.04  # 4% on tax + surcharge

# Rebate u/s 87A
OLD_REGIME_REBATE_LIMIT: int = 500_000   # Income up to 5L → full tax rebate (max ₹12,500)
OLD_REGIME_MAX_REBATE: int = 12_500

NEW_REGIME_REBATE_LIMIT: int = 1_200_000  # Income up to 12L → full tax rebate (max ₹60,000)
NEW_REGIME_MAX_REBATE: int = 60_000


def _slab_tax(taxable_income: float, slabs: List[Tuple[int | None, float]]) -> float:
    """Calculate tax using progressive slab structure."""
    tax = 0.0
    prev = 0
    for upper, rate in slabs:
        if taxable_income <= prev:
            break
        if upper is None:
            taxable_in_slab = taxable_income - prev
        else:
            taxable_in_slab = min(taxable_income, upper) - prev
        tax += taxable_in_slab * rate
        if upper is not None:
            prev = upper
    return tax


def _surcharge(tax_before_surcharge: float, total_income: float) -> float:
    """Marginal relief-aware surcharge calculation."""
    rate = 0.0
    for upper, r in SURCHARGE_SLABS:
        if upper is None or total_income <= upper:
            rate = r
            break
    return tax_before_surcharge * rate


def calculate_old_regime_tax(taxable_income: float) -> dict:
    """
    Full old-regime tax computation.
    Returns breakdown dict.
    """
    basic_tax = _slab_tax(taxable_income, OLD_REGIME_SLABS)

    # 87A rebate
    rebate = 0.0
    if taxable_income <= OLD_REGIME_REBATE_LIMIT:
        rebate = min(basic_tax, OLD_REGIME_MAX_REBATE)

    tax_after_rebate = max(0.0, basic_tax - rebate)
    surcharge = _surcharge(tax_after_rebate, taxable_income)
    cess = (tax_after_rebate + surcharge) * HEALTH_EDUCATION_CESS
    total_tax = tax_after_rebate + surcharge + cess

    return {
        "regime": "Old",
        "taxable_income": taxable_income,
        "basic_tax": round(basic_tax, 2),
        "rebate_87a": round(rebate, 2),
        "tax_after_rebate": round(tax_after_rebate, 2),
        "surcharge": round(surcharge, 2),
        "cess": round(cess, 2),
        "total_tax": round(total_tax, 2),
        "effective_rate": round((total_tax / taxable_income * 100) if taxable_income > 0 else 0, 2),
    }


def calculate_new_regime_tax(taxable_income: float) -> dict:
    """
    Full new-regime tax computation (FY 2025-26 revised slabs).
    Returns breakdown dict.
    """
    basic_tax = _slab_tax(taxable_income, NEW_REGIME_SLABS)

    # 87A rebate (up to ₹12L → nil tax)
    rebate = 0.0
    if taxable_income <= NEW_REGIME_REBATE_LIMIT:
        rebate = min(basic_tax, NEW_REGIME_MAX_REBATE)

    tax_after_rebate = max(0.0, basic_tax - rebate)
    surcharge = _surcharge(tax_after_rebate, taxable_income)
    cess = (tax_after_rebate + surcharge) * HEALTH_EDUCATION_CESS
    total_tax = tax_after_rebate + surcharge + cess

    return {
        "regime": "New",
        "taxable_income": taxable_income,
        "basic_tax": round(basic_tax, 2),
        "rebate_87a": round(rebate, 2),
        "tax_after_rebate": round(tax_after_rebate, 2),
        "surcharge": round(surcharge, 2),
        "cess": round(cess, 2),
        "total_tax": round(total_tax, 2),
        "effective_rate": round((total_tax / taxable_income * 100) if taxable_income > 0 else 0, 2),
    }
