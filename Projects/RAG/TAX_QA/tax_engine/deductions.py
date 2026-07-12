"""
Deductions Calculator — Sections 80C, 80D, 80CCD(1B), 80TTA, 80G
FY 2025-26. Deterministic. No LLM.
"""

# ─── Section 80C limits ────────────────────────────────────────────────────────
SEC_80C_LIMIT = 150_000  # ₹1,50,000

# ─── Section 80D (health insurance) ───────────────────────────────────────────
SEC_80D_SELF_BELOW_60 = 25_000
SEC_80D_SELF_ABOVE_60 = 50_000
SEC_80D_PARENTS_BELOW_60 = 25_000
SEC_80D_PARENTS_ABOVE_60 = 50_000

# ─── Section 80CCD(1B) — NPS additional deduction ────────────────────────────
SEC_80CCD1B_LIMIT = 50_000

# ─── Section 80TTA — savings interest ─────────────────────────────────────────
SEC_80TTA_LIMIT = 10_000

# ─── Standard Deduction ───────────────────────────────────────────────────────
STANDARD_DEDUCTION_OLD = 50_000
STANDARD_DEDUCTION_NEW = 75_000   # Increased in Budget 2024 for new regime


def calculate_80c_deduction(
    elss: float = 0,
    ppf: float = 0,
    epf: float = 0,
    life_insurance: float = 0,
    home_loan_principal: float = 0,
    nsc: float = 0,
    tuition_fees: float = 0,
    sukanya_samriddhi: float = 0,
    tax_saver_fd: float = 0,
    others: float = 0,
) -> dict:
    total_invested = (
        elss + ppf + epf + life_insurance + home_loan_principal
        + nsc + tuition_fees + sukanya_samriddhi + tax_saver_fd + others
    )
    deduction = min(total_invested, SEC_80C_LIMIT)
    remaining_capacity = SEC_80C_LIMIT - deduction

    return {
        "section": "80C",
        "total_invested": round(total_invested, 2),
        "deduction_allowed": round(deduction, 2),
        "limit": SEC_80C_LIMIT,
        "remaining_capacity": round(remaining_capacity, 2),
        "breakdown": {
            "elss": elss,
            "ppf": ppf,
            "epf": epf,
            "life_insurance": life_insurance,
            "home_loan_principal": home_loan_principal,
            "nsc": nsc,
            "tuition_fees": tuition_fees,
            "sukanya_samriddhi": sukanya_samriddhi,
            "tax_saver_fd": tax_saver_fd,
            "others": others,
        },
    }


def calculate_80d_deduction(
    self_premium: float = 0,
    parent_premium: float = 0,
    self_age_above_60: bool = False,
    parent_age_above_60: bool = False,
    preventive_health_checkup: float = 0,
) -> dict:
    self_limit = SEC_80D_SELF_ABOVE_60 if self_age_above_60 else SEC_80D_SELF_BELOW_60
    parent_limit = SEC_80D_PARENTS_ABOVE_60 if parent_age_above_60 else SEC_80D_PARENTS_BELOW_60

    self_deduction = min(self_premium + min(preventive_health_checkup, 5000), self_limit)
    parent_deduction = min(parent_premium, parent_limit)
    total = self_deduction + parent_deduction

    return {
        "section": "80D",
        "self_premium": self_premium,
        "self_limit": self_limit,
        "self_deduction": round(self_deduction, 2),
        "parent_premium": parent_premium,
        "parent_limit": parent_limit,
        "parent_deduction": round(parent_deduction, 2),
        "preventive_checkup": min(preventive_health_checkup, 5000),
        "total_deduction": round(total, 2),
        "remaining_self": round(max(0, self_limit - self_deduction), 2),
        "remaining_parent": round(max(0, parent_limit - parent_deduction), 2),
    }


def calculate_80ccd1b_deduction(nps_additional: float = 0) -> dict:
    """Additional NPS deduction u/s 80CCD(1B) — over and above 80C."""
    deduction = min(nps_additional, SEC_80CCD1B_LIMIT)
    return {
        "section": "80CCD(1B)",
        "nps_invested": round(nps_additional, 2),
        "deduction_allowed": round(deduction, 2),
        "limit": SEC_80CCD1B_LIMIT,
        "remaining_capacity": round(SEC_80CCD1B_LIMIT - deduction, 2),
    }


def calculate_80tta_deduction(savings_interest: float = 0) -> dict:
    """Section 80TTA — savings account interest (not applicable for 60+ → use 80TTB)."""
    deduction = min(savings_interest, SEC_80TTA_LIMIT)
    return {
        "section": "80TTA",
        "interest_earned": round(savings_interest, 2),
        "deduction_allowed": round(deduction, 2),
        "limit": SEC_80TTA_LIMIT,
    }
