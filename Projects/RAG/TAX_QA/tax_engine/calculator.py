"""
Master Tax Calculator — FY 2025-26
Orchestrates all sub-modules. Deterministic. No LLM.
"""
from tax_engine.slabs import calculate_old_regime_tax, calculate_new_regime_tax
from tax_engine.hra import calculate_hra_exemption
from tax_engine.deductions import (
    calculate_80c_deduction,
    calculate_80d_deduction,
    calculate_80ccd1b_deduction,
    calculate_80tta_deduction,
    STANDARD_DEDUCTION_OLD,
    STANDARD_DEDUCTION_NEW,
)
from tax_engine.nps import calculate_nps_deductions
from tax_engine.home_loan import calculate_home_loan_deductions
from tax_engine.rental import calculate_house_property_income


def calculate_full_tax(profile: dict) -> dict:
    """
    Full tax calculation for both regimes.

    Profile keys (all optional, defaults to 0):
        gross_salary          : Annual CTC / gross salary
        basic_salary          : Basic component of salary
        hra_received          : HRA received from employer
        rent_paid             : Actual rent paid
        is_metro              : Metro city? (bool)

        elss, ppf, epf        : 80C components
        life_insurance        : LIC premium
        home_loan_principal   : Principal repayment (80C)
        nsc, tax_saver_fd     : Other 80C
        tuition_fees          : Children tuition
        sukanya_samriddhi     : SSY
        other_80c             : Miscellaneous 80C

        health_insurance_self : 80D self + family
        health_insurance_parents : 80D parents
        self_age_above_60     : Bool
        parent_age_above_60   : Bool
        preventive_checkup    : Preventive health checkup

        employee_nps          : NPS contribution (employee)
        employer_nps          : NPS by employer
        additional_nps_80ccd1b: Extra NPS for 80CCD(1B)
        is_govt_employer      : Bool

        home_loan_interest    : Interest paid on home loan
        is_self_occupied      : Bool
        is_first_time_buyer   : Bool
        stamp_duty_value_lakh : Stamp duty value in lakhs

        savings_interest      : 80TTA
        other_income          : Other income sources

        # Rental / House Property income (Section 22-27)
        annual_rent           : Gross annual rent received (Rs.). 0 = no rental income
        municipal_taxes_paid  : Municipal taxes paid by owner (Rs.)
        is_let_out            : True = property rented out (default), False = self-occupied
        home_loan_interest_let_out : Home loan interest for let-out property (no cap)
    """
    g = profile

    gross_salary = float(g.get("gross_salary", 0))
    basic_salary = float(g.get("basic_salary", gross_salary * 0.5))  # default 50% of gross
    hra_received = float(g.get("hra_received", 0))
    rent_paid = float(g.get("rent_paid", 0))
    is_metro = bool(g.get("is_metro", False))
    other_income = float(g.get("other_income", 0))

    # ─── HRA Exemption (Old Regime only) ───────────────────────────────────────
    hra_result = calculate_hra_exemption(basic_salary, hra_received, rent_paid, is_metro)
    hra_exemption = hra_result["hra_exemption"]

    # ─── 80C ───────────────────────────────────────────────────────────────────
    c80_result = calculate_80c_deduction(
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

    # ─── 80D ───────────────────────────────────────────────────────────────────
    d80_result = calculate_80d_deduction(
        self_premium=float(g.get("health_insurance_self", 0)),
        parent_premium=float(g.get("health_insurance_parents", 0)),
        self_age_above_60=bool(g.get("self_age_above_60", False)),
        parent_age_above_60=bool(g.get("parent_age_above_60", False)),
        preventive_health_checkup=float(g.get("preventive_checkup", 0)),
    )

    # ─── NPS ───────────────────────────────────────────────────────────────────
    nps_result = calculate_nps_deductions(
        basic_salary=basic_salary,
        employee_nps=float(g.get("employee_nps", 0)),
        employer_nps=float(g.get("employer_nps", 0)),
        additional_nps_80ccd1b=float(g.get("additional_nps_80ccd1b", 0)),
        is_govt_employer=bool(g.get("is_govt_employer", False)),
    )

    # ─── Home Loan ─────────────────────────────────────────────────────────────
    hl_result = calculate_home_loan_deductions(
        principal_repaid=float(g.get("home_loan_principal", 0)),
        interest_paid=float(g.get("home_loan_interest", 0)),
        is_self_occupied=bool(g.get("is_self_occupied", True)),
        is_first_time_buyer_80eea=bool(g.get("is_first_time_buyer", False)),
        stamp_duty_value_lakh=float(g.get("stamp_duty_value_lakh", 0)),
    )

    # ─── 80TTA ─────────────────────────────────────────────────────────────────
    tta_result = calculate_80tta_deduction(float(g.get("savings_interest", 0)))

    # --- Rental / House Property Income (Sections 22-27) ---
    annual_rent = float(g.get("annual_rent", 0))
    municipal_taxes_paid = float(g.get("municipal_taxes_paid", 0))
    is_let_out = bool(g.get("is_let_out", annual_rent > 0))  # auto-detect if rent provided
    is_self_occupied_hp = not is_let_out
    # For let-out: interest from home_loan_interest or home_loan_interest_let_out
    hl_interest_let_out = float(g.get("home_loan_interest_let_out",
                                      g.get("home_loan_interest", 0) if is_let_out else 0))

    hp_result = calculate_house_property_income(
        annual_rent=annual_rent,
        municipal_taxes_paid=municipal_taxes_paid,
        home_loan_interest=hl_interest_let_out,
        is_let_out=is_let_out,
        is_self_occupied=is_self_occupied_hp,
    )

    # --- Presumptive Tax adjustments (Section 44ADA for Freelancers) ---
    is_freelancer = bool(g.get("is_freelancer", False))
    
    # ════════════════════════════════════════════════════════════════════════════
    #  OLD REGIME
    # ════════════════════════════════════════════════════════════════════════════
    if is_freelancer:
        # For a freelancer, presumptive income under Sec 44ADA is 50% of gross receipts.
        # No standard deduction (Rs.50k) or HRA exemption is allowed.
        presumptive_profit = gross_salary * 0.5
        old_gross_income = presumptive_profit + other_income + hp_result["hp_income_to_add"]
        old_deductions = (
            c80_result["deduction_allowed"]
            + d80_result["total_deduction"]
            + nps_result["sec_80ccd1b"]["deduction"]
            + hl_result["sec_24b"]["deduction"]
            + hl_result["sec_80eea"]["deduction"]
            + tta_result["deduction_allowed"]
            + hp_result["hp_loss_to_deduct"]   # HP loss set-off (max Rs.2L)
        )
    else:
        old_gross_income = gross_salary + other_income + hp_result["hp_income_to_add"]
        old_deductions = (
            STANDARD_DEDUCTION_OLD
            + hra_exemption
            + c80_result["deduction_allowed"]
            + d80_result["total_deduction"]
            + nps_result["sec_80ccd1b"]["deduction"]
            + nps_result["sec_80ccd2"]["deduction"]
            + hl_result["sec_24b"]["deduction"]
            + hl_result["sec_80eea"]["deduction"]
            + tta_result["deduction_allowed"]
            + hp_result["hp_loss_to_deduct"]   # HP loss set-off (max Rs.2L)
        )
        
    old_taxable = max(0.0, old_gross_income - old_deductions)
    old_tax_result = calculate_old_regime_tax(old_taxable)

    # ════════════════════════════════════════════════════════════════════════════
    #  NEW REGIME (most deductions not allowed, only standard deduction + 80CCD2)
    # ════════════════════════════════════════════════════════════════════════════
    if is_freelancer:
        # Under New Regime, presumptive profit is 50% of gross receipts.
        # Standard deduction (Rs.75k) and Chapter VI-A deductions are entirely blocked.
        # However, Section 24(b) interest for let-out IS allowed (income computation, not VI-A)
        presumptive_profit = gross_salary * 0.5
        new_gross_income = presumptive_profit + other_income + hp_result["hp_income_to_add"]
        new_deductions = hp_result["hp_loss_to_deduct"]  # HP loss set-off allowed under both regimes
    else:
        new_gross_income = gross_salary + other_income + hp_result["hp_income_to_add"]
        new_deductions = (
            STANDARD_DEDUCTION_NEW
            + nps_result["sec_80ccd2"]["deduction"]   # Only employer NPS allowed
            + hp_result["hp_loss_to_deduct"]           # HP loss set-off (max Rs.2L)
        )
        
    new_taxable = max(0.0, new_gross_income - new_deductions)
    new_tax_result = calculate_new_regime_tax(new_taxable)

    # ─── Recommendation ────────────────────────────────────────────────────────
    savings = new_tax_result["total_tax"] - old_tax_result["total_tax"]
    if savings > 0:
        recommended = "Old Regime"
        savings_amount = round(savings, 2)
        savings_note = f"Old Regime saves ₹{savings_amount:,.0f} more than New Regime"
    elif savings < 0:
        recommended = "New Regime"
        savings_amount = round(abs(savings), 2)
        savings_note = f"New Regime saves ₹{savings_amount:,.0f} more than Old Regime"
    else:
        recommended = "Either"
        savings_amount = 0
        savings_note = "Both regimes result in equal tax liability"

    return {
        "gross_salary": gross_salary,
        "other_income": other_income,
        "old_regime": {
            **old_tax_result,
            "gross_income": old_gross_income,
            "total_deductions": round(old_deductions, 2),
            "deduction_breakdown": {
                "standard_deduction": STANDARD_DEDUCTION_OLD,
                "hra_exemption": round(hra_exemption, 2),
                "sec_80c": c80_result["deduction_allowed"],
                "sec_80d": d80_result["total_deduction"],
                "sec_80ccd1b": nps_result["sec_80ccd1b"]["deduction"],
                "sec_80ccd2_employer_nps": nps_result["sec_80ccd2"]["deduction"],
                "sec_24b_interest": hl_result["sec_24b"]["deduction"],
                "sec_80eea": hl_result["sec_80eea"]["deduction"],
                "sec_80tta": tta_result["deduction_allowed"],
            },
        },
        "new_regime": {
            **new_tax_result,
            "gross_income": new_gross_income,
            "total_deductions": round(new_deductions, 2),
            "deduction_breakdown": {
                "standard_deduction": STANDARD_DEDUCTION_NEW,
                "sec_80ccd2_employer_nps": nps_result["sec_80ccd2"]["deduction"],
                "note": "Most deductions not applicable under New Regime",
            },
        },
        "recommendation": {
            "regime": recommended,
            "tax_savings": savings_amount,
            "note": savings_note,
        },
        "detail": {
            "hra": hra_result,
            "sec_80c": c80_result,
            "sec_80d": d80_result,
            "nps": nps_result,
            "home_loan": hl_result,
            "house_property": hp_result,
            "sec_80tta": tta_result,
        },
    }
