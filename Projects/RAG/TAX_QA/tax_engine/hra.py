"""
HRA Exemption Calculator — Section 10(13A)
Deterministic. No LLM.
"""


def calculate_hra_exemption(
    basic_salary: float,
    hra_received: float,
    rent_paid: float,
    is_metro: bool,
) -> dict:
    """
    HRA exemption = minimum of:
      1. Actual HRA received
      2. 50% of basic salary (metro) / 40% of basic salary (non-metro)
      3. Rent paid - 10% of basic salary

    Metro cities: Mumbai, Delhi, Chennai, Kolkata
    """
    city_pct = 0.50 if is_metro else 0.40

    component_1 = hra_received
    component_2 = basic_salary * city_pct
    component_3 = max(0.0, rent_paid - 0.10 * basic_salary)

    exemption = min(component_1, component_2, component_3)
    taxable_hra = hra_received - exemption

    return {
        "hra_received": round(hra_received, 2),
        "rent_paid": round(rent_paid, 2),
        "is_metro": is_metro,
        "component_1_actual_hra": round(component_1, 2),
        "component_2_city_pct": round(component_2, 2),
        "component_3_rent_minus_10pct": round(component_3, 2),
        "hra_exemption": round(exemption, 2),
        "taxable_hra": round(taxable_hra, 2),
    }
