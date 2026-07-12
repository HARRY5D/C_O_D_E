"""Dashboard page — KPI cards + quick stats."""
import streamlit as st
from frontend.components.cards import metric_card


def show_dashboard():
    st.markdown('<p class="section-header">🏠 Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Your tax planning overview for FY 2025-26</p>', unsafe_allow_html=True)

    # Quick start cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("New Regime Rebate", "₹12 Lakh", "Zero tax up to ₹12L", "#4ECDC4", "🎯")
    with col2:
        metric_card("80C Limit", "₹1,50,000", "Max deduction", "#FF6B6B", "📊")
    with col3:
        metric_card("NPS Extra Deduction", "₹50,000", "Over 80C limit", "#FFD700", "🏦")
    with col4:
        metric_card("Health Insurance", "₹25,000–₹1L", "Section 80D", "#A78BFA", "🏥")

    st.divider()

    # Feature cards
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>💬 Tax Assistant</h4>
            <p>Ask any tax question in plain English. Get answers backed by legal sections.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>🧮 Tax Calculator</h4>
            <p>Enter your income and deductions to get accurate old/new regime tax comparison.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
            <h4>📈 Tax Optimizer</h4>
            <p>Find unused deduction capacity and estimate additional tax savings.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # FY 2025-26 Highlights
    st.markdown("### 📋 FY 2025-26 Key Changes")
    col1, col2 = st.columns(2)

    with col1:
        st.info("""
**New Regime — Revised Slabs (Budget 2025)**
- ₹0 – ₹4L: Nil
- ₹4L – ₹8L: 5%
- ₹8L – ₹12L: 10%
- ₹12L – ₹16L: 15%
- ₹16L – ₹20L: 20%
- ₹20L – ₹24L: 25%
- Above ₹24L: 30%
        """)

    with col2:
        st.success("""
**Key Benefits**
- ✅ Rebate u/s 87A: Zero tax up to ₹12 lakh (New Regime)
- ✅ Standard Deduction: ₹75,000 (New) / ₹50,000 (Old)
- ✅ NPS 80CCD(2): Available in BOTH regimes
- ✅ 80C: ₹1,50,000 deduction (Old Regime)
- ✅ 80D: Up to ₹1,00,000 (Old Regime)
- ✅ NPS extra 80CCD(1B): ₹50,000 (Old Regime)
        """)
