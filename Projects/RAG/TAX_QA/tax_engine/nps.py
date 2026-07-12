"""
NPS Calculator — Sections 80CCD(1), 80CCD(1B), 80CCD(2)
FY 2025-26. Deterministic. No LLM.
"""

# Limits
SEC_80CCD1_LIMIT_PCT = 0.10          # 10% of basic salary (employee contribution)
SEC_80CCD2_LIMIT_PCT_PRIVATE = 0.10  # 10% of basic for private employers
SEC_80CCD2_LIMIT_PCT_GOVT = 0.14     # 14% of basic for government employers
SEC_80CCD1B_LIMIT = 50_000           # Additional deduction over 80C


def calculate_nps_deductions(
    basic_salary: float,
    employee_nps: float = 0,
    employer_nps: float = 0,
    additional_nps_80ccd1b: float = 0,
    is_govt_employer: bool = False,
) -> dict:
    """
    Full NPS deduction breakdown.

    80CCD(1)   → employee contribution (part of 80C 1.5L limit)
    80CCD(1B)  → additional employee contribution (extra 50k over 80C)
    80CCD(2)   → employer contribution (NOT part of 80C, NO individual limit)
    """
    # 80CCD(1): employee contribution capped at 10% of basic
    sec_80ccd1_limit = basic_salary * SEC_80CCD1_LIMIT_PCT
    sec_80ccd1_deduction = min(employee_nps, sec_80ccd1_limit)

    # 80CCD(1B): additional employee NPS
    sec_80ccd1b_deduction = min(additional_nps_80ccd1b, SEC_80CCD1B_LIMIT)

    # 80CCD(2): employer NPS (fully deductible up to the percentage limit)
    employer_limit_pct = SEC_80CCD2_LIMIT_PCT_GOVT if is_govt_employer else SEC_80CCD2_LIMIT_PCT_PRIVATE
    sec_80ccd2_limit = basic_salary * employer_limit_pct
    sec_80ccd2_deduction = min(employer_nps, sec_80ccd2_limit)

    total_deduction = sec_80ccd1_deduction + sec_80ccd1b_deduction + sec_80ccd2_deduction

    return {
        "basic_salary": basic_salary,
        "employee_nps_invested": employee_nps,
        "employer_nps_invested": employer_nps,
        "sec_80ccd1": {
            "deduction": round(sec_80ccd1_deduction, 2),
            "limit": round(sec_80ccd1_limit, 2),
            "note": "Part of overall 80C limit of ₹1,50,000",
        },
        "sec_80ccd1b": {
            "deduction": round(sec_80ccd1b_deduction, 2),
            "limit": SEC_80CCD1B_LIMIT,
            "remaining": round(SEC_80CCD1B_LIMIT - sec_80ccd1b_deduction, 2),
            "note": "Additional deduction over and above 80C",
        },
        "sec_80ccd2": {
            "deduction": round(sec_80ccd2_deduction, 2),
            "limit": round(sec_80ccd2_limit, 2),
            "is_govt": is_govt_employer,
            "note": "Employer contribution — no cap on individual (subject to % limit)",
        },
        "total_nps_deduction": round(total_deduction, 2),
    }
