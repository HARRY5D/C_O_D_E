"""
Tax Optimizer page — identifies unused deductions and quantifies savings.
"""
import streamlit as st
from frontend.components.charts import optimization_horizontal_bar, tax_savings_gauge
from frontend.components.cards import metric_card, priority_badge


def show_tax_optimizer():
    st.markdown('<p class="section-header">📈 Tax Optimizer</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Discover missed deductions and maximize your tax savings</p>', unsafe_allow_html=True)

    # Check if tax calculation was done first
    has_profile = "last_tax_profile" in st.session_state and "last_tax_result" in st.session_state

    if has_profile:
        st.info("✅ Using profile from Tax Calculator. You can also enter values below to analyze a different scenario.")

    with st.expander("📝 Enter Profile for Optimization", expanded=not has_profile):
        col1, col2, col3 = st.columns(3)
        with col1:
            gross_salary = st.number_input("Gross Salary (₹)", min_value=0,
                                           value=st.session_state.get("last_tax_profile", {}).get("gross_salary", 1_200_000),
                                           step=50_000, format="%d", key="opt_salary")
        with col2:
            used_80c = st.number_input("Total 80C Invested (₹)", min_value=0,
                                       value=int(sum([
                                           st.session_state.get("last_tax_profile", {}).get(k, 0)
                                           for k in ["elss", "ppf", "epf", "life_insurance", "home_loan_principal", "nsc", "other_80c"]
                                       ])),
                                       max_value=150_000, step=5_000, format="%d", key="opt_80c")
        with col3:
            health_self = st.number_input("Health Ins. (Self) (₹)", min_value=0,
                                          value=st.session_state.get("last_tax_profile", {}).get("health_insurance_self", 0),
                                          max_value=50_000, step=1_000, format="%d", key="opt_80d_self")

        col1, col2, col3 = st.columns(3)
        with col1:
            health_parents = st.number_input("Health Ins. (Parents) (₹)", min_value=0,
                                             value=st.session_state.get("last_tax_profile", {}).get("health_insurance_parents", 0),
                                             max_value=50_000, step=1_000, format="%d", key="opt_80d_par")
        with col2:
            additional_nps = st.number_input("Additional NPS 80CCD(1B) (₹)", min_value=0,
                                             value=st.session_state.get("last_tax_profile", {}).get("additional_nps_80ccd1b", 0),
                                             max_value=50_000, step=5_000, format="%d", key="opt_nps")
        with col3:
            parent_senior = st.checkbox("Parents age 60+?", value=False, key="opt_parent_senior")

        analyze_btn = st.button("🔍 Analyze Optimization Opportunities", key="opt_analyze", use_container_width=True)

    if analyze_btn or has_profile:
        profile = st.session_state.get("last_tax_profile", {
            "gross_salary": gross_salary,
            "other_80c": used_80c,
            "health_insurance_self": health_self,
            "health_insurance_parents": health_parents,
            "additional_nps_80ccd1b": additional_nps,
            "parent_age_above_60": parent_senior,
        })

        with st.spinner("Finding optimization opportunities..."):
            try:
                from tax_engine.calculator import calculate_full_tax
                from optimization.optimizer import find_optimization_opportunities

                if "last_tax_result" not in st.session_state:
                    st.session_state["last_tax_result"] = calculate_full_tax(profile)

                opt_result = find_optimization_opportunities(
                    profile=profile,
                    tax_result=st.session_state["last_tax_result"],
                )
            except Exception as e:
                st.error(f"Error: {e}")
                return

        # Summary KPIs
        col1, col2, col3 = st.columns(3)
        with col1:
            old_tax = st.session_state["last_tax_result"]["old_regime"]["total_tax"]
            metric_card("Current Old Regime Tax", f"₹{old_tax:,.0f}", "", "#FF6B6B", "🏛️")
        with col2:
            new_tax = st.session_state["last_tax_result"]["new_regime"]["total_tax"]
            metric_card("Current New Regime Tax", f"₹{new_tax:,.0f}", "", "#4ECDC4", "✨")
        with col3:
            pot_savings = opt_result["total_potential_additional_savings"]
            metric_card("Additional Savings Possible", f"₹{pot_savings:,.0f}", "Under Old Regime", "#FFD700", "💰")

        st.divider()
        st.markdown(f"### 📝 {opt_result['summary']}")

        # Gauge + bar chart
        col1, col2 = st.columns([1, 2])
        with col1:
            if pot_savings > 0:
                st.plotly_chart(tax_savings_gauge(pot_savings, max(pot_savings * 1.5, 100_000)), use_container_width=True)

        with col2:
            if opt_result["opportunities"]:
                st.plotly_chart(optimization_horizontal_bar(opt_result["opportunities"]), use_container_width=True)

        st.divider()
        st.markdown("### 🎯 Optimization Opportunities")

        for opp in opt_result["opportunities"]:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{opp['title']}** — Section {opp['section']}")
                    st.markdown(f"Current: ₹{opp['current_investment']:,.0f} | Limit: ₹{opp['limit']:,.0f} | Gap: ₹{opp['remaining_capacity']:,.0f}")
                    st.markdown(f"Instruments: {', '.join(opp['instruments'])}")
                with col2:
                    st.markdown(f"**Tax Savings: ₹{opp['estimated_tax_savings']:,.0f}**")
                    priority_badge(opp.get("priority", "MEDIUM"))
                st.divider()
