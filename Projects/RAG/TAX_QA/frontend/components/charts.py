"""
Plotly chart components for FinAssist AI.
"""
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List


# ─── Color Palette ─────────────────────────────────────────────────────────────
OLD_REGIME_COLOR = "#FF6B6B"
NEW_REGIME_COLOR = "#4ECDC4"
SAVINGS_COLOR = "#45B7D1"
BACKGROUND = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(255,255,255,0.1)"
TEXT_COLOR = "#E2E8F0"

CHART_LAYOUT = dict(
    paper_bgcolor=BACKGROUND,
    plot_bgcolor=BACKGROUND,
    font=dict(color=TEXT_COLOR, family="Inter, sans-serif"),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0.3)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
)


def regime_comparison_bar(old_tax: float, new_tax: float) -> go.Figure:
    """Side-by-side bar chart comparing old vs new regime tax."""
    fig = go.Figure(data=[
        go.Bar(
            name="Old Regime",
            x=["Tax Liability"],
            y=[old_tax],
            marker_color=OLD_REGIME_COLOR,
            text=[f"₹{old_tax:,.0f}"],
            textposition="outside",
            textfont=dict(size=14, color=TEXT_COLOR),
        ),
        go.Bar(
            name="New Regime",
            x=["Tax Liability"],
            y=[new_tax],
            marker_color=NEW_REGIME_COLOR,
            text=[f"₹{new_tax:,.0f}"],
            textposition="outside",
            textfont=dict(size=14, color=TEXT_COLOR),
        ),
    ])
    fig.update_layout(
        **CHART_LAYOUT,
        title="Old vs New Regime Tax Comparison",
        barmode="group",
        yaxis=dict(gridcolor=GRID_COLOR, title="Tax (₹)", tickformat=",.0f"),
        xaxis=dict(gridcolor=GRID_COLOR),
    )
    return fig


def deductions_donut(breakdown: Dict[str, float]) -> go.Figure:
    """Donut chart showing deduction breakdown."""
    labels = [k.replace("_", " ").title() for k, v in breakdown.items() if v > 0]
    values = [v for v in breakdown.values() if v > 0]

    if not values:
        return go.Figure()

    colors = px.colors.qualitative.Set2[:len(values)]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=colors, line=dict(color="#1A202C", width=2)),
        textinfo="label+percent",
        textfont=dict(size=11, color=TEXT_COLOR),
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>",
    )])

    total = sum(values)
    fig.add_annotation(
        text=f"₹{total:,.0f}<br>Total",
        x=0.5, y=0.5,
        font=dict(size=14, color=TEXT_COLOR),
        showarrow=False,
    )

    fig.update_layout(
        **CHART_LAYOUT,
        title="Deductions Breakdown",
        showlegend=True,
    )
    return fig


def tax_savings_gauge(savings: float, max_savings: float = 200000) -> go.Figure:
    """Gauge chart showing potential tax savings."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=savings,
        title={"text": "Potential Tax Savings", "font": {"color": TEXT_COLOR, "size": 16}},
        number={"prefix": "₹", "font": {"size": 24, "color": TEXT_COLOR}, "valueformat": ",.0f"},
        gauge={
            "axis": {"range": [0, max_savings], "tickformat": ",.0f", "tickcolor": TEXT_COLOR},
            "bar": {"color": SAVINGS_COLOR},
            "bgcolor": "rgba(255,255,255,0.05)",
            "steps": [
                {"range": [0, max_savings * 0.33], "color": "rgba(255,107,107,0.15)"},
                {"range": [max_savings * 0.33, max_savings * 0.66], "color": "rgba(255,193,7,0.15)"},
                {"range": [max_savings * 0.66, max_savings], "color": "rgba(78,205,196,0.15)"},
            ],
            "threshold": {
                "line": {"color": "#FFD700", "width": 3},
                "thickness": 0.75,
                "value": savings,
            },
        },
    ))
    fig.update_layout(**CHART_LAYOUT, height=280)
    return fig


def slab_waterfall(regime: str, taxable_income: float, slabs: List[Dict]) -> go.Figure:
    """Waterfall chart showing how tax builds up across slabs."""
    names = [s["label"] for s in slabs]
    values = [s["tax"] for s in slabs]

    fig = go.Figure(go.Waterfall(
        name=f"{regime} Regime",
        orientation="v",
        measure=["relative"] * len(values) + ["total"],
        x=names + ["Total Tax"],
        y=values + [sum(values)],
        connector={"line": {"color": "rgba(255,255,255,0.2)"}},
        decreasing={"marker": {"color": SAVINGS_COLOR}},
        increasing={"marker": {"color": OLD_REGIME_COLOR if regime == "Old" else NEW_REGIME_COLOR}},
        totals={"marker": {"color": "#FFD700"}},
        text=[f"₹{v:,.0f}" for v in values] + [f"₹{sum(values):,.0f}"],
        textposition="outside",
        textfont=dict(color=TEXT_COLOR),
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        title=f"{regime} Regime — Tax Build-up by Slab",
        yaxis=dict(gridcolor=GRID_COLOR, tickformat=",.0f"),
    )
    return fig


def optimization_horizontal_bar(opportunities: List[Dict]) -> go.Figure:
    """Horizontal bar chart for tax savings opportunities."""
    if not opportunities:
        return go.Figure()

    titles = [o["title"][:35] + "…" if len(o["title"]) > 35 else o["title"] for o in opportunities]
    savings = [o["estimated_tax_savings"] for o in opportunities]
    priorities = [o.get("priority", "MEDIUM") for o in opportunities]

    colors = [
        "#FF6B6B" if p == "HIGH" else "#FFD700" if p == "MEDIUM" else "#4ECDC4"
        for p in priorities
    ]

    fig = go.Figure(go.Bar(
        y=titles,
        x=savings,
        orientation="h",
        marker_color=colors,
        text=[f"₹{s:,.0f}" for s in savings],
        textposition="outside",
        textfont=dict(color=TEXT_COLOR),
        hovertemplate="<b>%{y}</b><br>Savings: ₹%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        title="Tax Saving Opportunities",
        xaxis=dict(gridcolor=GRID_COLOR, tickformat=",.0f", title="Estimated Savings (₹)"),
        yaxis=dict(autorange="reversed"),
        height=max(250, len(opportunities) * 60),
    )
    return fig
