"""
FinAssist AI — Main Streamlit Application
"""
import sys
import os

# Ensure project root is in path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
try:
    from config.langsmith_config import configure_langsmith
    configure_langsmith()
except Exception:
    pass  # LangSmith config failure must never crash the app


# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinAssist AI — Indian Tax Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ─── Google Font ─── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ─── Root Variables ─── */
:root {
    --bg-primary: #0D1117;
    --bg-secondary: #161B22;
    --bg-card: #1C2333;
    --bg-hover: #21262D;
    --accent-primary: #4ECDC4;
    --accent-secondary: #FF6B6B;
    --accent-gold: #FFD700;
    --text-primary: #E6EDF3;
    --text-secondary: #8B949E;
    --border-color: rgba(255,255,255,0.1);
    --radius: 12px;
    --shadow: 0 4px 24px rgba(0,0,0,0.4);
}

/* ─── Base ─── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1117 0%, #161B22 100%);
    border-right: 1px solid var(--border-color);
}

[data-testid="stSidebar"] .stRadio label {
    color: var(--text-primary) !important;
    font-weight: 500;
}

/* ─── Metric Cards ─── */
.metric-card {
    background: var(--bg-card);
    border-radius: var(--radius);
    padding: 20px;
    text-align: center;
    box-shadow: var(--shadow);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    border: 1px solid var(--border-color);
    height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.6);
}
.card-icon { font-size: 28px; margin-bottom: 6px; }
.card-title { color: var(--text-secondary); font-size: 12px; font-weight: 500; margin: 0; text-transform: uppercase; letter-spacing: 1px; }
.card-value { font-size: 22px; font-weight: 700; margin: 4px 0 0 0; }
.card-delta { font-size: 12px; color: var(--accent-primary); margin: 2px 0 0 0; }

/* ─── Info Cards ─── */
.info-card {
    background: var(--bg-card);
    border-radius: var(--radius);
    padding: 16px;
    border: 1px solid var(--border-color);
    margin-bottom: 12px;
}
.info-card h4 { color: var(--accent-primary); margin: 0 0 8px 0; font-size: 15px; }
.info-card p { color: var(--text-secondary); margin: 0; font-size: 13px; }

/* ─── Chat Messages ─── */
.chat-user {
    background: linear-gradient(135deg, #1C2333 0%, #21262D 100%);
    border-left: 3px solid var(--accent-primary);
    border-radius: 0 var(--radius) var(--radius) var(--radius);
    padding: 14px 18px;
    margin: 12px 0;
    max-width: 80%;
    margin-left: auto;
    box-shadow: var(--shadow);
}
.chat-assistant {
    background: linear-gradient(135deg, #161B22 0%, #1C2333 100%);
    border-left: 3px solid var(--accent-secondary);
    border-radius: 0 var(--radius) var(--radius) var(--radius);
    padding: 14px 18px;
    margin: 12px 0;
    max-width: 85%;
    box-shadow: var(--shadow);
}
.chat-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    margin-bottom: 6px;
}

/* ─── Section Headers ─── */
.section-header {
    font-size: 24px;
    font-weight: 700;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
}
.section-sub {
    color: var(--text-secondary);
    font-size: 14px;
    margin-bottom: 20px;
}

/* ─── Streamlit overrides ─── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-primary), #3DBDB5) !important;
    color: #0D1117 !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(78,205,196,0.4) !important;
}
.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
}
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
}
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border-radius: var(--radius) !important;
    padding: 12px !important;
    border: 1px solid var(--border-color) !important;
}
.stAlert {
    border-radius: var(--radius) !important;
}
hr {
    border-color: var(--border-color) !important;
    margin: 20px 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 10px 0 20px 0;">
        <div style="font-size:40px;">💰</div>
        <h2 style="color:#4ECDC4; margin:8px 0 4px 0; font-size:20px;">FinAssist AI</h2>
        <p style="color:#8B949E; font-size:12px; margin:0;">Indian Tax Planning Assistant</p>
        <p style="color:#8B949E; font-size:11px; margin:4px 0 0 0;">FY 2025-26 / AY 2026-27</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "Navigation",
        options=[
            "🏠 Dashboard",
            "💬 Tax Assistant",
            "🧮 Tax Calculator",
            "📈 Tax Optimizer",
            "📄 Form16 Analyzer",
            "⚖️ Regime Comparator",
            "ℹ️ About",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("""
    <div style="padding:10px; background:rgba(78,205,196,0.1); border-radius:8px; border:1px solid rgba(78,205,196,0.2);">
        <p style="color:#8B949E; font-size:11px; margin:0;">
        <b style="color:#4ECDC4;">⚡ Powered by</b><br>
        • Qwen2.5-Coder (Ollama)<br>
        • BGE Embeddings<br>
        • FAISS + BM25 Hybrid<br>
        • LangGraph Orchestration
        </p>
    </div>
    """, unsafe_allow_html=True)

# ─── Page Routing ──────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    from frontend._pages.dashboard import show_dashboard
    show_dashboard()

elif page == "💬 Tax Assistant":
    from frontend._pages.tax_assistant import show_tax_assistant
    show_tax_assistant()

elif page == "🧮 Tax Calculator":
    from frontend._pages.tax_calculator import show_tax_calculator
    show_tax_calculator()

elif page == "📈 Tax Optimizer":
    from frontend._pages.tax_optimizer import show_tax_optimizer
    show_tax_optimizer()

elif page == "📄 Form16 Analyzer":
    from frontend._pages.form16_analyzer import show_form16_analyzer
    show_form16_analyzer()

elif page == "⚖️ Regime Comparator":
    from frontend._pages.regime_comparator import show_regime_comparator
    show_regime_comparator()

elif page == "ℹ️ About":
    st.markdown('<p class="section-header">FinAssist AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Intelligent Tax Planning for Indian Taxpayers</p>', unsafe_allow_html=True)

    st.markdown("""
    ### 🏗️ Architecture
    FinAssist AI uses a **hybrid financial intelligence system**:

    | Layer | Technology |
    |---|---|
    | **Orchestration** | LangGraph (state machine) |
    | **LLM** | Qwen2.5-Coder 7B via Ollama (local, offline) |
    | **RAG Retrieval** | Dense (FAISS) + BM25 + Reranking |
    | **Embeddings** | BAAI/bge-small-en-v1.5 |
    | **Reranker** | CrossEncoder (sentence-transformers) |
    | **Tax Engine** | Deterministic Python (no LLM) |
    | **PDF Processing** | PyMuPDF + PaddleOCR |
    | **Tracing** | LangSmith (EU endpoint) |

    ### 📋 Key Principle
    > **The LLM never calculates tax.** All tax numbers come from the Python rule engine.
    > The LLM only explains, contextualizes, and recommends.

    ### 📖 Data Sources
    - Income Tax Act 1961 (amended)
    - Income Tax Rules 1962
    - Finance Bill 2025
    - Budget Memorandum 2025
    - Budget Speech 2025
    - Curated expert knowledge base (7 topic documents)
    """)
