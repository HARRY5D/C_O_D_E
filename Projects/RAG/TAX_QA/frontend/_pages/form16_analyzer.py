"""
Form16 Analyzer — upload and automatically extract Form 16 data.
"""
import os
import tempfile
import streamlit as st
from frontend.components.cards import metric_card


def show_form16_analyzer():
    st.markdown('<p class="section-header">📄 Form16 Analyzer</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Upload your Form 16 PDF for automatic tax analysis</p>', unsafe_allow_html=True)

    st.info("**Optional Feature** — This page is useful if you have your Form 16 available. You can also use the Tax Assistant or Tax Calculator without it.")

    uploaded = st.file_uploader(
        "Drop your Form 16 PDF here",
        type=["pdf"],
        key="form16_main_upload",
        help="Form 16 is issued by your employer. It contains your salary, TDS, and deductions for the financial year.",
    )

    if uploaded:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(uploaded.read())
            tmp_path = tmp.name

        with st.spinner("🔍 Extracting Form 16 data..."):
            try:
                from form16_parser.parser import extract_form16
                from tax_engine.calculator import calculate_full_tax

                form16_data = extract_form16(tmp_path)
                b = form16_data.part_b
                a = form16_data.part_a

            except Exception as e:
                st.error(f"Error parsing Form 16: {e}")
                os.unlink(tmp_path)
                return

        os.unlink(tmp_path)

        # Confidence indicator
        confidence = form16_data.extraction_confidence or 0
        conf_color = "#4ECDC4" if confidence > 0.6 else "#FFD700" if confidence > 0.3 else "#FF6B6B"
        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.3); border-radius:8px; padding:12px; border:1px solid {conf_color}; margin-bottom:16px;">
            <span style="color:{conf_color}; font-weight:600;">Extraction Confidence: {confidence*100:.0f}%</span>
            <span style="color:#8B949E; font-size:13px; margin-left:12px;">
            {"✅ Good extraction" if confidence > 0.6 else "⚠️ Partial extraction — verify manually" if confidence > 0.3 else "❌ Low confidence — please verify all values"}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Employer info
        if a.employer_name:
            st.markdown(f"**Employer**: {a.employer_name} | **TAN**: {a.employer_tan or 'N/A'} | **AY**: {a.assessment_year}")

        # KPI cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            metric_card("Gross Salary", f"₹{b.gross_salary:,.0f}", "", "#4ECDC4", "💼")
        with col2:
            metric_card("TDS Deducted", f"₹{b.tds_deducted:,.0f}", "", "#FF6B6B", "🏦")
        with col3:
            metric_card("Taxable Income", f"₹{b.taxable_income:,.0f}", "", "#FFD700", "📊")
        with col4:
            metric_card("Total Tax Payable", f"₹{b.total_tax_payable:,.0f}", "", "#A78BFA", "💰")

        st.divider()
        st.markdown("### 📋 Deductions Extracted")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Chapter VI-A Deductions**")
            st.markdown(f"- Section 80C: ₹{b.sec_80c:,.0f}")
            st.markdown(f"- Section 80D: ₹{b.sec_80d:,.0f}")
            st.markdown(f"- 80CCD(1B) NPS: ₹{b.sec_80ccd1b:,.0f}")
            st.markdown(f"- Employer NPS 80CCD(2): ₹{b.employer_nps_80ccd2:,.0f}")
            st.markdown(f"- Section 80E: ₹{b.sec_80e:,.0f}")
            st.markdown(f"- Section 80G: ₹{b.sec_80g:,.0f}")
            st.markdown(f"- Section 80TTA: ₹{b.sec_80tta:,.0f}")
            st.markdown(f"**Total Deductions: ₹{b.total_deductions_chapter_via:,.0f}**")

        with col2:
            st.markdown("**Tax Computation**")
            st.markdown(f"- Tax on Income: ₹{b.tax_on_income:,.0f}")
            st.markdown(f"- Rebate 87A: ₹{b.rebate_87a:,.0f}")
            st.markdown(f"- Surcharge: ₹{b.surcharge:,.0f}")
            st.markdown(f"- H&E Cess (4%): ₹{b.cess:,.0f}")
            st.markdown(f"**Total Tax Payable: ₹{b.total_tax_payable:,.0f}**")
            refund = b.tds_deducted - b.total_tax_payable
            if refund > 0:
                st.success(f"🎉 Refund Due: ₹{refund:,.0f}")
            elif refund < 0:
                st.warning(f"⚠️ Additional Tax Due: ₹{abs(refund):,.0f}")
            else:
                st.info("✅ TDS matches tax payable — no refund or additional tax")

        # Parsing notes
        if form16_data.parsing_notes:
            st.warning("**Extraction Notes:**\n" + "\n".join(f"- {n}" for n in form16_data.parsing_notes))

        # Run full analysis
        if b.gross_salary and b.gross_salary > 0:
            if st.button("🔍 Run Full Tax Analysis", key="form16_analyze"):
                tax_profile = form16_data.to_tax_profile()
                try:
                    from tax_engine.calculator import calculate_full_tax
                    result = calculate_full_tax(tax_profile)
                    st.session_state["last_tax_result"] = result
                    st.session_state["last_tax_profile"] = tax_profile
                    st.success("✅ Analysis complete! Switch to **Tax Calculator** or **Tax Optimizer** for detailed view.")
                except Exception as e:
                    st.error(f"Analysis error: {e}")
