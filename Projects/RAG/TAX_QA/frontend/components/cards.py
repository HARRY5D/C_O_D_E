"""
Metric card components for Streamlit dashboard.
"""
import streamlit as st


def metric_card(title: str, value: str, delta: str = "", color: str = "#4ECDC4", icon: str = "💰"):
    """Render a styled metric card."""
    delta_html = f'<p class="card-delta">{delta}</p>' if delta else ""
    st.markdown(f"""
    <div class="metric-card" style="border-top: 3px solid {color};">
        <div class="card-icon">{icon}</div>
        <p class="card-title">{title}</p>
        <p class="card-value" style="color: {color};">{value}</p>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def info_card(title: str, content: str, icon: str = "ℹ️"):
    """Render an informational card."""
    st.markdown(f"""
    <div class="info-card">
        <h4>{icon} {title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


def source_citation_card(citations: list):
    """Render source citation cards."""
    if not citations:
        return
    with st.expander("📚 Legal Sources & Citations", expanded=False):
        for cite in citations:
            st.markdown(f"- {cite}")


def regime_badge(regime: str):
    """Render a colored regime badge."""
    color = "#FF6B6B" if regime == "Old" else "#4ECDC4"
    st.markdown(
        f'<span style="background:{color};color:white;padding:4px 12px;'
        f'border-radius:20px;font-weight:600;font-size:14px;">'
        f'{"🏛️ Old Regime" if regime == "Old" else "✨ New Regime"}</span>',
        unsafe_allow_html=True,
    )


def priority_badge(priority: str):
    """Render a priority badge for optimization opportunities."""
    colors = {"HIGH": "#FF6B6B", "MEDIUM": "#FFD700", "LOW": "#4ECDC4"}
    color = colors.get(priority, "#4ECDC4")
    st.markdown(
        f'<span style="background:{color};color:#1A202C;padding:2px 8px;'
        f'border-radius:12px;font-weight:700;font-size:11px;">{priority}</span>',
        unsafe_allow_html=True,
    )
