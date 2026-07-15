"""
Income from House Property — FY 2025-26
Deterministic. No LLM.

Implements:
  - Section 23: Gross Annual Value / Net Annual Value
  - Section 24(a): 30% standard deduction on NAV
  - Section 24(b): Home loan interest (self-occupied cap vs let-out no cap)
  - Section 71B: HP loss set-off limit (Rs.2L) and carry-forward rules
"""

# Constants
SEC_24A_RATE: float = 0.30                # 30% standard deduction on NAV
SEC_24B_SELF_OCCUPIED_LIMIT: float = 200_000.0  # Rs.2L cap for self-occupied
HP_LOSS_SETOFF_LIMIT: float = 200_000.0   # Max HP loss setoff against other income


def calculate_house_property_income(
    annual_rent: float = 0.0,
    municipal_taxes_paid: float = 0.0,
    home_loan_interest: float = 0.0,
    is_let_out: bool = True,
    is_self_occupied: bool = False,
) -> dict:
    """
    Compute Income from House Property under Sections 22-27.

    Args:
        annual_rent          : Gross annual rent received/receivable (Rs.)
                               For self-occupied: pass 0.0 (NAV deemed nil)
        municipal_taxes_paid : Municipal/property taxes paid by OWNER during year (Rs.)
        home_loan_interest   : Annual interest paid on home loan (Rs.)
        is_let_out           : True if property is rented out (let-out)
        is_self_occupied     : True if owner lives in the property (self-occupied)

    Returns dict:
        gross_annual_value   : GAV (max of actual rent and fair market rent)
        municipal_taxes      : Taxes actually paid by owner
        nav                  : Net Annual Value (GAV - municipal taxes)
        sec_24a_deduction    : 30% of NAV (standard deduction)
        sec_24b_deduction    : Home loan interest deduction (may be capped)
        sec_24b_cap_applied  : True if Rs.2L cap was applied (self-occupied only)
        gross_hp_income      : NAV - 24(a) - 24(b) (can be negative)
        hp_loss_setoff       : Amount of HP loss that can offset other income (max 2L)
        hp_loss_carried_fwd  : Amount of HP loss to carry forward (8 years, HP only)
        taxable_hp_income    : Net HP income after set-off (0 if loss, or positive income)
        hp_income_to_add     : Amount to ADD to gross income (positive HP income)
        hp_loss_to_deduct    : Amount to DEDUCT from gross income (loss set-off, max 2L)
    """
    annual_rent = max(0.0, float(annual_rent))
    municipal_taxes_paid = max(0.0, float(municipal_taxes_paid))
    home_loan_interest = max(0.0, float(home_loan_interest))

    # --- Step 1: Gross Annual Value ---
    if is_self_occupied and not is_let_out:
        # For self-occupied property, Annual Value is deemed NIL under Section 23(2)
        gav = 0.0
    else:
        # For let-out property, GAV = actual rent received (simplified; ignores
        # fair rental value comparison which requires external data)
        gav = annual_rent

    # --- Step 2: Net Annual Value = GAV - Municipal Taxes ---
    nav = max(0.0, gav - municipal_taxes_paid)

    # --- Step 3: Section 24(a) — Standard Deduction (30% of NAV) ---
    # Always applicable to let-out property. Does NOT apply if NAV is zero.
    if nav > 0 and not is_self_occupied:
        sec_24a = round(nav * SEC_24A_RATE, 2)
    else:
        sec_24a = 0.0

    # --- Step 4: Section 24(b) — Home Loan Interest ---
    sec_24b_cap_applied = False
    if is_self_occupied and not is_let_out:
        # Self-occupied: capped at Rs.2,00,000 per Section 24(b) proviso
        sec_24b = min(home_loan_interest, SEC_24B_SELF_OCCUPIED_LIMIT)
        if home_loan_interest > SEC_24B_SELF_OCCUPIED_LIMIT:
            sec_24b_cap_applied = True
    else:
        # Let-out: ACTUAL interest, no cap
        sec_24b = home_loan_interest
        sec_24b_cap_applied = False

    # --- Step 5: Income from House Property ---
    gross_hp_income = nav - sec_24a - sec_24b

    # --- Step 6: Loss Set-Off and Carry Forward (Section 71B) ---
    hp_loss_setoff = 0.0
    hp_loss_carried_fwd = 0.0
    taxable_hp_income = 0.0
    hp_income_to_add = 0.0
    hp_loss_to_deduct = 0.0

    if gross_hp_income >= 0:
        # Positive HP income — taxable
        taxable_hp_income = gross_hp_income
        hp_income_to_add = gross_hp_income
    else:
        # Loss from House Property
        total_loss = abs(gross_hp_income)

        # Max Rs.2L can be set off against salary/other income in same year
        hp_loss_setoff = min(total_loss, HP_LOSS_SETOFF_LIMIT)
        hp_loss_carried_fwd = round(total_loss - hp_loss_setoff, 2)

        hp_loss_to_deduct = hp_loss_setoff
        taxable_hp_income = 0.0  # Loss is absorbed, not a positive taxable amount

    return {
        "gross_annual_value": round(gav, 2),
        "municipal_taxes": round(municipal_taxes_paid, 2),
        "nav": round(nav, 2),
        "sec_24a_deduction": round(sec_24a, 2),
        "sec_24b_deduction": round(sec_24b, 2),
        "sec_24b_cap_applied": sec_24b_cap_applied,
        "gross_hp_income": round(gross_hp_income, 2),
        "hp_loss_setoff": round(hp_loss_setoff, 2),
        "hp_loss_carried_fwd": round(hp_loss_carried_fwd, 2),
        "taxable_hp_income": round(taxable_hp_income, 2),
        "hp_income_to_add": round(hp_income_to_add, 2),
        "hp_loss_to_deduct": round(hp_loss_to_deduct, 2),
        "is_let_out": is_let_out,
        "is_self_occupied": is_self_occupied,
    }
