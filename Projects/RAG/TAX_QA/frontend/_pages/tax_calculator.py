"""
Tax Calculator page — deterministic old/new regime comparison.
"""
import streamlit as st
from frontend.components.charts import regime_comparison_bar, deductions_donut
from frontend.components.cards import metric_card, regime_badge


def show_tax_calculator():
    st.markdown('<p class="section-header">🧮 Tax Calculator</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Accurate tax calculation for FY 2025-26 — no LLM, pure Python</p>', unsafe_allow_html=True)

    with st.form("tax_calc_form"):
        st.markdown("### 💼 Income Details")
        col1, col2, col3 = st.columns(3)
        with col1:
            gross_salary = st.number_input("Gross Annual Salary (₹)", min_value=0, value=1_200_000, step=10_000, format="%d")
        with col2:
            basic_salary = st.number_input("Basic Salary (₹/year)", min_value=0, value=600_000, step=10_000, format="%d",
                                           help="Typically 40-50% of gross salary")
        with col3:
            other_income = st.number_input("Other Income (₹)", min_value=0, value=0, step=5_000, format="%d",
                                           help="Interest, capital gains, etc.")

        st.markdown("### 🏠 HRA Details")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            hra_received = st.number_input("HRA Received (₹/year)", min_value=0, value=150_000, step=5_000, format="%d")
        with col2:
            rent_paid = st.number_input("Rent Paid (₹/year)", min_value=0, value=180_000, step=5_000, format="%d")
        with col3:
            is_metro = st.selectbox("City Type", options=["Non-Metro (40%)", "Metro (50%)"], index=0)
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            is_metro_bool = is_metro.startswith("Metro")

        st.markdown("### 📊 Section 80C Investments")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            elss = st.number_input("ELSS (₹)", min_value=0, value=0, step=5_000, format="%d")
            ppf = st.number_input("PPF (₹)", min_value=0, value=0, step=5_000, format="%d")
        with col2:
            epf = st.number_input("EPF Employee (₹)", min_value=0, value=0, step=5_000, format="%d")
            life_insurance = st.number_input("Life Insurance (₹)", min_value=0, value=0, step=5_000, format="%d")
        with col3:
            home_loan_principal = st.number_input("Home Loan Principal (₹)", min_value=0, value=0, step=5_000, format="%d")
            nsc = st.number_input("NSC (₹)", min_value=0, value=0, step=5_000, format="%d")
        with col4:
            other_80c = st.number_input("Other 80C (₹)", min_value=0, value=0, step=5_000, format="%d")

        st.markdown("### 🏥 Section 80D — Health Insurance")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            health_self = st.number_input("Self/Family Premium (₹)", min_value=0, value=0, step=1_000, format="%d")
        with col2:
            health_parents = st.number_input("Parents Premium (₹)", min_value=0, value=0, step=1_000, format="%d")
        with col3:
            self_senior = st.checkbox("Self age 60+?", value=False)
        with col4:
            parent_senior = st.checkbox("Parents age 60+?", value=False)

        st.markdown("### 🏦 NPS Investments")
        col1, col2, col3 = st.columns(3)
        with col1:
            additional_nps = st.number_input("Additional NPS 80CCD(1B) (₹)", min_value=0, max_value=50_000, value=0, step=5_000, format="%d")
        with col2:
            employer_nps = st.number_input("Employer NPS 80CCD(2) (₹)", min_value=0, value=0, step=5_000, format="%d")
        with col3:
            is_govt = st.checkbox("Government Employer?", value=False)

        st.markdown("### 🏘️ Home Loan Interest")
        col1, col2 = st.columns(2)
        with col1:
            home_loan_interest = st.number_input("Home Loan Interest (₹/year)", min_value=0, value=0, step=5_000, format="%d")
        with col2:
            is_self_occupied = st.selectbox("Property Type", ["Self-Occupied", "Let-Out"], index=0) == "Self-Occupied"

        submitted = st.form_submit_button("🧮 Calculate Tax", use_container_width=True)

    if submitted:
        profile = {
            "gross_salary": gross_salary,
            "basic_salary": basic_salary,
            "hra_received": hra_received,
            "rent_paid": rent_paid,
            "is_metro": is_metro_bool,
            "elss": elss,
            "ppf": ppf,
            "epf": epf,
            "life_insurance": life_insurance,
            "home_loan_principal": home_loan_principal,
            "nsc": nsc,
            "other_80c": other_80c,
            "health_insurance_self": health_self,
            "health_insurance_parents": health_parents,
            "self_age_above_60": self_senior,
            "parent_age_above_60": parent_senior,
            "additional_nps_80ccd1b": additional_nps,
            "employer_nps": employer_nps,
            "is_govt_employer": is_govt,
            "home_loan_interest": home_loan_interest,
            "is_self_occupied": is_self_occupied,
            "other_income": other_income,
        }

        with st.spinner("Calculating..."):
            try:
                from tax_engine.calculator import calculate_full_tax
                result = calculate_full_tax(profile)
            except Exception as e:
                st.error(f"Calculation error: {e}")
                return

        # Store in session state for other pages
        st.session_state["last_tax_result"] = result
        st.session_state["last_tax_profile"] = profile

        old = result["old_regime"]
        new = result["new_regime"]
        rec = result["recommendation"]

        st.divider()
        st.markdown("### 📊 Results")

        # KPI cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            metric_card("Old Regime Tax", f"₹{old['total_tax']:,.0f}", f"Effective: {old['effective_rate']}%", "#FF6B6B", "🏛️")
        with col2:
            metric_card("New Regime Tax", f"₹{new['total_tax']:,.0f}", f"Effective: {new['effective_rate']}%", "#4ECDC4", "✨")
        with col3:
            savings = abs(rec["tax_savings"])
            metric_card("Tax Savings", f"₹{savings:,.0f}", f"with {rec['regime']} Regime", "#FFD700", "💰")
        with col4:
            metric_card("Recommended", rec["regime"] + " Regime", rec["note"][:40] + "...", "#A78BFA", "🎯")

        # Charts
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(
                regime_comparison_bar(old["total_tax"], new["total_tax"]),
                use_container_width=True,
            )
        with col2:
            deduction_breakdown = old.get("deduction_breakdown", {})
            # Remove zero values and non-numeric
            clean_breakdown = {k: v for k, v in deduction_breakdown.items() if isinstance(v, (int, float)) and v > 0}
            if clean_breakdown:
                st.plotly_chart(deductions_donut(clean_breakdown), use_container_width=True)

        # Detailed breakdown
        with st.expander("📋 Full Tax Breakdown", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Old Regime**")
                st.markdown(f"- Gross Income: ₹{old.get('gross_income', 0):,.0f}")
                st.markdown(f"- Total Deductions: ₹{old['total_deductions']:,.0f}")
                st.markdown(f"- Taxable Income: ₹{old['taxable_income']:,.0f}")
                st.markdown(f"- Basic Tax: ₹{old['basic_tax']:,.0f}")
                st.markdown(f"- Rebate 87A: ₹{old['rebate_87a']:,.0f}")
                st.markdown(f"- Surcharge: ₹{old['surcharge']:,.0f}")
                st.markdown(f"- Cess (4%): ₹{old['cess']:,.0f}")
                st.markdown(f"**Total Tax: ₹{old['total_tax']:,.0f}**")

            with col2:
                st.markdown("**New Regime**")
                st.markdown(f"- Gross Income: ₹{new.get('gross_income', 0):,.0f}")
                st.markdown(f"- Total Deductions: ₹{new['total_deductions']:,.0f}")
                st.markdown(f"- Taxable Income: ₹{new['taxable_income']:,.0f}")
                st.markdown(f"- Basic Tax: ₹{new['basic_tax']:,.0f}")
                st.markdown(f"- Rebate 87A: ₹{new['rebate_87a']:,.0f}")
                st.markdown(f"- Surcharge: ₹{new['surcharge']:,.0f}")
                st.markdown(f"- Cess (4%): ₹{new['cess']:,.0f}")
                st.markdown(f"**Total Tax: ₹{new['total_tax']:,.0f}**")
