# FinAssist AI 💰

**Intelligent Indian Tax Planning Assistant — FY 2025-26**

A hybrid financial intelligence system combining deterministic tax calculation, hybrid RAG retrieval, and LangGraph orchestration for accurate tax guidance.

---

## Architecture

```
User (Streamlit)
      │
LangGraph Orchestrator
      │
  ┌───┼─────────────────┐
  ▼   ▼                 ▼
Tax  RAG Engine    Form16 Parser
Engine (FAISS+BM25+Reranker)
  │                     │
  └─────────┬───────────┘
            ▼
        Gemini 1.5 Flash
            ▼
      Final Answer + Citations
```

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | LangGraph + LangChain |
| LLM | Gemini 1.5 Flash |
| Embeddings | BAAI/bge-small-en-v1.5 |
| Reranker | BAAI/bge-reranker-base |
| Vector Store | FAISS |
| Sparse Retrieval | BM25 (rank-bm25) |
| PDF Processing | PyMuPDF + pdfplumber |
| OCR (optional) | PaddleOCR |
| Tax Engine | Python rule engine (deterministic) |
| Backend | FastAPI |
| Frontend | Streamlit + Plotly |
| Tracing | LangSmith (APAC) |

---

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys (already pre-filled for this project).

### 3. Move PDFs to raw/ directory

```bash
python scripts/move_pdfs.py
```

### 4. Process PDFs & Build Knowledge Base

```bash
python scripts/process_pdfs.py
```

### 5. Build FAISS Index

```bash
python scripts/build_index.py
```

### 6. Run Tests

```bash
pytest tests/test_tax_engine.py -v
pytest tests/test_retrieval.py -v
```

### 7. Start the Application

**Option A: Streamlit Frontend (recommended)**
```bash
streamlit run frontend/app.py
```

**Option B: FastAPI Backend**
```bash
uvicorn api.main:app --reload
# API docs at: http://localhost:8000/docs
```

---

## Features

### 💬 Tax Assistant (Chat Mode)
- Ask any tax question in plain English
- Backed by 5 official PDFs + 7 curated knowledge documents
- Hybrid retrieval: Dense (FAISS) + BM25 + BGE reranking
- LangSmith traces every conversation

### 🧮 Tax Calculator
- Deterministic calculation — **no LLM involvement**
- Both Old and New regime with full breakdown
- Section 80C, 80D, HRA, NPS, Home Loan deductions
- FY 2025-26 revised New Regime slabs

### 📈 Tax Optimizer
- Identifies unused deduction capacity
- Ranks opportunities by savings potential
- Priority-based recommendations

### 📄 Form16 Analyzer
- Upload Form 16 PDF
- Automatic extraction using PyMuPDF + regex
- Full tax analysis from extracted data

### ⚖️ Regime Comparator
- Side-by-side Old vs New regime
- Break-even deduction analysis
- Interactive Plotly charts

---

## Data Sources

- `Income_tax_axt_1962.pdf` — Income Tax Act 1961
- `Income-tax-Rules-1962.pdf` — Income Tax Rules 1962
- `Finance_Bill.pdf` — Finance Bill 2025
- `budget memorandum.pdf` — Budget Memorandum 2025
- `budget_speech.pdf` — Budget Speech 2025

**Curated Knowledge Base** (7 hand-crafted documents):
- `80C.md`, `80D.md`, `NPS.md`, `HRA.md`
- `Home_Loan.md`, `Old_vs_New_Regime.md`, `Tax_Slabs.md`

---

## Project Structure

```
TAX_QA/
├── data/raw/          # Source PDFs
├── data/curated/      # Hand-crafted knowledge docs
├── preprocessing/     # PDF extraction pipeline
├── chunking/          # Section + semantic chunking
├── embeddings/        # BGE embedder
├── vectordb/          # FAISS vector store
├── rag/               # Hybrid retriever + reranker + chain
├── tax_engine/        # Deterministic Python tax calculator
├── optimization/      # Tax savings optimizer
├── form16_parser/     # Form 16 PDF extractor
├── recommendation_engine/ # LangGraph orchestrator
├── api/               # FastAPI backend
├── frontend/          # Streamlit UI
├── config/            # Settings + LangSmith config
├── scripts/           # Data pipeline scripts
└── tests/             # Pytest test suite
```

---

## Key Principle

> **The LLM never calculates tax.** All tax numbers are produced by the Python rule engine.
> The LLM only explains, contextualizes, and generates recommendations.

---

## LangSmith Tracing

All LangGraph and LangChain runs are automatically traced to:
- **Project**: `Tax RAG`
- **Endpoint**: `https://apac.api.smith.langchain.com`

---

## License

For educational/research use only. Tax calculations are for guidance only — consult a CA for professional advice.
