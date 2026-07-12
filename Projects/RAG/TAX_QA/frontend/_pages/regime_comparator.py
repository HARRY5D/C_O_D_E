"""
Regime Comparator — side-by-side old vs new regime comparison.
"""
import streamlit as st
from frontend.components.charts import regime_comparison_bar
from frontend.components.cards import metric_card


def show_regime_comparator():
    st.markdown('<p class="section-header">⚖️ Regime Comparator</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Old Regime vs New Regime — find what works best for you</p>', unsafe_allow_html=True)

    # Use existing profile if available
    has_result = "last_tax_result" in st.session_state

    if not has_result:
        st.info("💡 Go to **Tax Calculator** first to enter your income details, then come back here for comparison.")

    col1, col2 = st.columns(2)
    with col1:
        gross_salary = st.number_input("Gross Salary (₹)", min_value=0,
                                       value=st.session_state.get("last_tax_profile", {}).get("gross_salary", 1_200_000),
                                       step=50_000, format="%d", key="comp_salary")
    with col2:
        total_deductions_80c = st.number_input("Total 80C (₹)", min_value=0, max_value=150_000,
                                               value=50_000, step=10_000, format="%d", key="comp_80c")

    col3, col4 = st.columns(2)
    with col3:
        health_ins = st.number_input("Health Insurance 80D (₹)", min_value=0, max_value=100_000,
                                     value=0, step=5_000, format="%d", key="comp_80d")
    with col4:
        nps_extra = st.number_input("NPS 80CCD(1B) (₹)", min_value=0, max_value=50_000,
                                    value=0, step=5_000, format="%d", key="comp_nps")

    if st.button("⚖️ Compare Regimes", use_container_width=True, key="comp_btn"):
        profile = {
            "gross_salary": gross_salary,
            "other_80c": total_deductions_80c,
            "health_insurance_self": health_ins,
            "additional_nps_80ccd1b": nps_extra,
        }

        try:
            from tax_engine.calculator import calculate_full_tax
            result = calculate_full_tax(profile)
        except Exception as e:
            st.error(f"Error: {e}")
            return

        old = result["old_regime"]
        new = result["new_regime"]
        rec = result["recommendation"]

        st.divider()
        # KPI row
        col1, col2, col3 = st.columns(3)
        with col1:
            metric_card("Old Regime Tax", f"₹{old['total_tax']:,.0f}", f"{old['effective_rate']}% effective rate", "#FF6B6B", "🏛️")
        with col2:
            metric_card("New Regime Tax", f"₹{new['total_tax']:,.0f}", f"{new['effective_rate']}% effective rate", "#4ECDC4", "✨")
        with col3:
            savings = abs(rec["tax_savings"])
            metric_card("You Save", f"₹{savings:,.0f}", f"with {rec['regime']} Regime", "#FFD700", "💰")

        # Bar chart
        st.plotly_chart(regime_comparison_bar(old["total_tax"], new["total_tax"]), use_container_width=True)

        # Comparison table
        st.markdown("### 📋 Side-by-Side Comparison")
        col1, col2 = st.columns(2)

        comparison_rows = [
            ("Gross Income", f"₹{old.get('gross_income', gross_salary):,.0f}", f"₹{new.get('gross_income', gross_salary):,.0f}"),
            ("Standard Deduction", "₹50,000", "₹75,000"),
            ("80C Deduction", f"₹{old['deduction_breakdown'].get('sec_80c', 0):,.0f}", "❌ Not available"),
            ("80D Health Insurance", f"₹{old['deduction_breakdown'].get('sec_80d', 0):,.0f}", "❌ Not available"),
            ("HRA Exemption", f"₹{old['deduction_breakdown'].get('hra_exemption', 0):,.0f}", "❌ Not available"),
            ("NPS 80CCD(1B)", f"₹{old['deduction_breakdown'].get('sec_80ccd1b', 0):,.0f}", "❌ Not available"),
            ("Employer NPS 80CCD(2)", f"₹{old['deduction_breakdown'].get('sec_80ccd2_employer_nps', 0):,.0f}", f"₹{new['deduction_breakdown'].get('sec_80ccd2_employer_nps', 0):,.0f} ✅"),
            ("Total Deductions", f"₹{old['total_deductions']:,.0f}", f"₹{new['total_deductions']:,.0f}"),
            ("Taxable Income", f"₹{old['taxable_income']:,.0f}", f"₹{new['taxable_income']:,.0f}"),
            ("Basic Tax", f"₹{old['basic_tax']:,.0f}", f"₹{new['basic_tax']:,.0f}"),
            ("Rebate 87A", f"₹{old['rebate_87a']:,.0f}", f"₹{new['rebate_87a']:,.0f}"),
            ("Cess (4%)", f"₹{old['cess']:,.0f}", f"₹{new['cess']:,.0f}"),
            ("**Total Tax**", f"**₹{old['total_tax']:,.0f}**", f"**₹{new['total_tax']:,.0f}**"),
        ]

        import pandas as pd
        df = pd.DataFrame(comparison_rows, columns=["Item", "Old Regime", "New Regime"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Recommendation box
        rec_color = "#FF6B6B" if rec["regime"] == "Old" else "#4ECDC4"
        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.3); border:2px solid {rec_color}; border-radius:12px; padding:20px; margin-top:16px; text-align:center;">
            <h3 style="color:{rec_color}; margin:0 0 8px 0;">🎯 Recommendation</h3>
            <h2 style="color:{rec_color}; margin:0 0 8px 0;">{"🏛️ Old Regime" if rec["regime"] == "Old" else "✨ New Regime"}</h2>
            <p style="color:#8B949E; margin:0;">{rec["note"]}</p>
        </div>
        """, unsafe_allow_html=True)
