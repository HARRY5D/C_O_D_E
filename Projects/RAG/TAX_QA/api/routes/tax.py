"""
Tax calculation and optimization endpoints.
All calculations are deterministic — no LLM involvement.
"""
from fastapi import APIRouter, HTTPException
from api.schemas import (
    TaxCalculationRequest, TaxCalculationResponse,
    RegimeResult, OptimizationResponse, RegimeCompareResponse,
)

router = APIRouter()


@router.post("/calculate-tax", response_model=TaxCalculationResponse)
async def calculate_tax(request: TaxCalculationRequest):
    """
    Deterministic tax calculation for both regimes.
    Returns old/new regime tax, deductions breakdown, and recommendation.
    """
    try:
        from tax_engine.calculator import calculate_full_tax

        profile = request.model_dump()
        result = calculate_full_tax(profile)

        old = result["old_regime"]
        new = result["new_regime"]

        return TaxCalculationResponse(
            old_regime=RegimeResult(
                regime="Old",
                taxable_income=old["taxable_income"],
                total_tax=old["total_tax"],
                effective_rate=old["effective_rate"],
                total_deductions=old["total_deductions"],
            ),
            new_regime=RegimeResult(
                regime="New",
                taxable_income=new["taxable_income"],
                total_tax=new["total_tax"],
                effective_rate=new["effective_rate"],
                total_deductions=new["total_deductions"],
            ),
            recommendation=result["recommendation"],
            detail=result["detail"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize-tax", response_model=OptimizationResponse)
async def optimize_tax(request: TaxCalculationRequest):
    """
    Find unused deduction opportunities based on current tax profile.
    Returns ranked savings suggestions with estimated tax impact.
    """
    try:
        from tax_engine.calculator import calculate_full_tax
        from optimization.optimizer import find_optimization_opportunities

        profile = request.model_dump()
        tax_result = calculate_full_tax(profile)
        opt_result = find_optimization_opportunities(profile, tax_result)

        return OptimizationResponse(**opt_result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare-regimes", response_model=RegimeCompareResponse)
async def compare_regimes(request: TaxCalculationRequest):
    """
    Compare old vs new regime with break-even analysis.
    """
    try:
        from tax_engine.calculator import calculate_full_tax
        from tax_engine.deductions import SEC_80C_LIMIT

        profile = request.model_dump()
        result = calculate_full_tax(profile)

        old = result["old_regime"]
        new = result["new_regime"]

        # Break-even analysis
        old_deductions = old["total_deductions"]
        new_deductions = new["total_deductions"]
        deduction_advantage = old_deductions - new_deductions

        break_even = {
            "old_regime_deductions": old_deductions,
            "new_regime_deductions": new_deductions,
            "extra_deductions_in_old": deduction_advantage,
            "note": (
                f"You are claiming ₹{deduction_advantage:,.0f} more in deductions under Old Regime. "
                f"This makes Old Regime beneficial."
                if deduction_advantage > 0 else
                f"New Regime has higher standard deductions (₹75,000 vs ₹50,000). "
                f"Old Regime needs ₹{abs(deduction_advantage):,.0f} more in deductions to be beneficial."
            ),
        }

        return RegimeCompareResponse(
            old_regime=RegimeResult(
                regime="Old",
                taxable_income=old["taxable_income"],
                total_tax=old["total_tax"],
                effective_rate=old["effective_rate"],
                total_deductions=old["total_deductions"],
            ),
            new_regime=RegimeResult(
                regime="New",
                taxable_income=new["taxable_income"],
                total_tax=new["total_tax"],
                effective_rate=new["effective_rate"],
                total_deductions=new["total_deductions"],
            ),
            recommendation=result["recommendation"],
            break_even_analysis=break_even,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
