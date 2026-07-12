"""
Home Loan Deduction Calculator — Section 24(b) and Section 80C (Principal)
FY 2025-26. Deterministic. No LLM.
"""

# Section 24(b) — Interest on home loan
SEC_24B_SELF_OCCUPIED_LIMIT = 200_000   # ₹2,00,000 for self-occupied property
SEC_24B_LET_OUT_LIMIT = None            # Unlimited for let-out property (subject to loss setoff rules)

# Section 80EEA — First-time homebuyers (stamp duty ≤ ₹45L, loan sanctioned Apr 2019 – Mar 2022)
SEC_80EEA_LIMIT = 150_000


def calculate_home_loan_deductions(
    principal_repaid: float = 0,
    interest_paid: float = 0,
    is_self_occupied: bool = True,
    is_first_time_buyer_80eea: bool = False,
    stamp_duty_value_lakh: float = 0,
) -> dict:
    """
    Home loan deduction breakdown.
    - Principal → goes into 80C (handled in deductions.py, passed here for reference)
    - Interest  → Section 24(b)
    - Additional→ Section 80EEA (if eligible)
    """
    # Section 24(b) interest
    if is_self_occupied:
        interest_deduction = min(interest_paid, SEC_24B_SELF_OCCUPIED_LIMIT)
    else:
        interest_deduction = interest_paid  # let-out: full interest allowed

    # Section 80EEA eligibility (first-time buyer, stamp duty ≤ 45L)
    sec_80eea_deduction = 0.0
    if is_first_time_buyer_80eea and stamp_duty_value_lakh <= 45:
        sec_80eea_deduction = min(interest_paid - interest_deduction, SEC_80EEA_LIMIT)
        sec_80eea_deduction = max(0.0, sec_80eea_deduction)

    return {
        "principal_repaid": round(principal_repaid, 2),
        "note_principal": "Principal repayment qualifies under Section 80C (₹1.5L limit)",
        "interest_paid": round(interest_paid, 2),
        "property_type": "Self-Occupied" if is_self_occupied else "Let-Out",
        "sec_24b": {
            "deduction": round(interest_deduction, 2),
            "limit": SEC_24B_SELF_OCCUPIED_LIMIT if is_self_occupied else "Unlimited",
        },
        "sec_80eea": {
            "eligible": is_first_time_buyer_80eea and stamp_duty_value_lakh <= 45,
            "deduction": round(sec_80eea_deduction, 2),
            "limit": SEC_80EEA_LIMIT,
        },
        "total_interest_deduction": round(interest_deduction + sec_80eea_deduction, 2),
    }
