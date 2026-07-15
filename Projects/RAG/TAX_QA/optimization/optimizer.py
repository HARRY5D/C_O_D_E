"""
Tax Optimization Engine — FY 2025-26
Identifies unused deduction capacity and quantifies potential savings.
Deterministic. No LLM.
"""
from tax_engine.deductions import (
    SEC_80C_LIMIT,
    SEC_80D_SELF_BELOW_60,
    SEC_80D_SELF_ABOVE_60,
    SEC_80D_PARENTS_BELOW_60,
    SEC_80D_PARENTS_ABOVE_60,
    SEC_80CCD1B_LIMIT,
)
from tax_engine.slabs import calculate_old_regime_tax, calculate_new_regime_tax


def find_optimization_opportunities(
    profile: dict,
    tax_result: dict,
    preferred_regime: str = "auto",
) -> dict:
    """
    Given a tax profile and existing tax result, find:
    - Unused deduction capacity
    - Estimated additional savings per suggestion
    - Priority-ranked recommendations

    Args:
        preferred_regime: "old", "new", or "auto" (use recommendation)
    """
    suggestions = []
    total_potential_savings = 0.0

    # Determine effective regime for optimization
    effective_regime = preferred_regime
    if effective_regime == "auto":
        effective_regime = tax_result.get("recommendation", {}).get("regime", "old").lower()
        if "new" in effective_regime:
            effective_regime = "new"
        else:
            effective_regime = "old"

    # Under New Regime, Chapter VI-A deductions (80C, 80D, NPS 80CCD1B) are BLOCKED.
    # Only suggest these if user is on Old Regime.
    is_old_regime = (effective_regime != "new")

    # Current values
    elss = float(profile.get("elss", 0))
    ppf = float(profile.get("ppf", 0))
    epf = float(profile.get("epf", 0))
    life_ins = float(profile.get("life_insurance", 0))
    home_principal = float(profile.get("home_loan_principal", 0))
    other_80c = float(profile.get("other_80c", 0))
    total_80c = elss + ppf + epf + life_ins + home_principal + other_80c
    used_80c = min(total_80c, SEC_80C_LIMIT)

    health_self = float(profile.get("health_insurance_self", 0))
    health_parents = float(profile.get("health_insurance_parents", 0))
    self_above_60 = bool(profile.get("self_age_above_60", False))
    parent_above_60 = bool(profile.get("parent_age_above_60", False))
    self_limit = SEC_80D_SELF_ABOVE_60 if self_above_60 else SEC_80D_SELF_BELOW_60
    parent_limit = SEC_80D_PARENTS_ABOVE_60 if parent_above_60 else SEC_80D_PARENTS_BELOW_60

    additional_nps = float(profile.get("additional_nps_80ccd1b", 0))

    gross_salary = float(profile.get("gross_salary", 0))
    old_taxable = tax_result.get("old_regime", {}).get("taxable_income", 0)

    # Helper: marginal tax rate on old regime
    def marginal_savings(deduction_amount: float) -> float:
        current_tax = calculate_old_regime_tax(old_taxable)["total_tax"]
        new_tax = calculate_old_regime_tax(max(0, old_taxable - deduction_amount))["total_tax"]
        return round(current_tax - new_tax, 2)

    # ─── 80C Gap ───────────────────────────────────────────────────────────────
    remaining_80c = SEC_80C_LIMIT - used_80c
    if remaining_80c > 0:
        savings = marginal_savings(remaining_80c)
        total_potential_savings += savings
        suggestions.append({
            "section": "80C",
            "title": "Maximize Section 80C Deduction",
            "current_investment": round(used_80c, 2),
            "limit": SEC_80C_LIMIT,
            "remaining_capacity": round(remaining_80c, 2),
            "instruments": ["ELSS Mutual Fund", "PPF", "Tax-Saver FD", "NSC", "Life Insurance Premium"],
            "estimated_tax_savings": savings,
            "priority": "HIGH" if remaining_80c > 50_000 else "MEDIUM",
        })

    # ─── 80D Self Gap ──────────────────────────────────────────────────────────
    remaining_80d_self = self_limit - health_self
    if remaining_80d_self > 0:
        savings = marginal_savings(remaining_80d_self)
        total_potential_savings += savings
        suggestions.append({
            "section": "80D",
            "title": "Get Health Insurance for Self/Family",
            "current_investment": health_self,
            "limit": self_limit,
            "remaining_capacity": round(remaining_80d_self, 2),
            "instruments": ["Health Insurance Policy"],
            "estimated_tax_savings": savings,
            "priority": "HIGH" if health_self == 0 else "MEDIUM",
        })

    # ─── 80D Parents Gap ───────────────────────────────────────────────────────
    remaining_80d_parents = parent_limit - health_parents
    if remaining_80d_parents > 0:
        savings = marginal_savings(remaining_80d_parents)
        total_potential_savings += savings
        suggestions.append({
            "section": "80D",
            "title": "Health Insurance for Parents",
            "current_investment": health_parents,
            "limit": parent_limit,
            "remaining_capacity": round(remaining_80d_parents, 2),
            "instruments": ["Parents Health Insurance Policy"],
            "estimated_tax_savings": savings,
            "priority": "HIGH" if health_parents == 0 and parent_limit >= 50_000 else "MEDIUM",
        })

    # ─── 80CCD(1B) NPS Gap ─────────────────────────────────────────────────────
    remaining_nps = SEC_80CCD1B_LIMIT - additional_nps
    if remaining_nps > 0:
        savings = marginal_savings(remaining_nps)
        total_potential_savings += savings
        suggestions.append({
            "section": "80CCD(1B)",
            "title": "Additional NPS Investment (over 80C)",
            "current_investment": additional_nps,
            "limit": SEC_80CCD1B_LIMIT,
            "remaining_capacity": round(remaining_nps, 2),
            "instruments": ["National Pension System (NPS) Tier-I"],
            "estimated_tax_savings": savings,
            "priority": "HIGH" if additional_nps == 0 else "MEDIUM",
        })

    # Sort by savings descending
    suggestions.sort(key=lambda x: x["estimated_tax_savings"], reverse=True)

    return {
        "current_old_regime_tax": tax_result.get("old_regime", {}).get("total_tax", 0),
        "current_new_regime_tax": tax_result.get("new_regime", {}).get("total_tax", 0),
        "total_potential_additional_savings": round(total_potential_savings, 2),
        "opportunities": suggestions,
        "summary": (
            f"You can save an additional ₹{total_potential_savings:,.0f} by fully utilizing "
            f"available deductions under Old Regime."
        ) if total_potential_savings > 0 else "You are optimally utilizing all major deductions!",
    }
