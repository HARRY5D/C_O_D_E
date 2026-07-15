# FinAssist AI — Architecture Reference

> **Living document.** Updated at the end of every session. Use this to resume work without re-reading the full codebase.

---

## Project Purpose

An offline-first Indian Tax RAG assistant for FY 2025-26. Uses:
- **Local LLM** (Qwen2.5-Coder:7b / DeepSeek-Coder:6.7b via Ollama) for natural language answers
- **Deterministic Python Tax Engine** for all number computation (zero LLM math)
- **FAISS + BGE** vector store for legal document retrieval
- **LangGraph** for multi-node orchestration
- **LangSmith** for tracing
- **Gemini API** for post-hoc legal section verification

---

## Directory Map

```
TAX_QA/
├── architecture.md             ← THIS FILE (cross-session reference)
├── .env                        ← Secrets (not committed)
├── .env.example                ← Template for .env
├── .gitignore
├── requirements.txt
│
├── config/
│   ├── settings.py             ← Pydantic settings (loads .env)
│   └── langsmith_config.py     ← LangSmith tracing setup
│
├── data/
│   ├── raw/                    ← Source PDFs (Income Tax Act sections etc.)
│   └── curated/                ← Hand-crafted markdown legal reference docs
│       ├── 80C.md
│       ├── 80D.md
│       ├── HRA.md
│       ├── Home_Loan.md
│       ├── NPS.md
│       ├── Old_vs_New_Regime.md
│       ├── Presumptive_Taxation.md   ← Added Session 3 (Section 44ADA)
│       └── Tax_Slabs.md
│
├── preprocessing/              ← PDF → text chunk pipeline
│   └── pdf/
│
├── chunking/                   ← Text splitting logic
│
├── embeddings/
│   └── embedder.py             ← BGEEmbedder (BAAI/bge-small-en-v1.5, offline)
│
├── vectordb/
│   └── faiss_store.py          ← FAISS index (load/save/search)
│
├── rag/
│   ├── retriever.py            ← HybridRetriever (dense FAISS + BM25)
│   ├── reranker.py             ← BGEReranker (BAAI/bge-reranker-base, offline)
│   └── rag_chain.py            ← RAGChain class + TAX_SYSTEM_PROMPT
│
├── tax_engine/                 ← DETERMINISTIC — ZERO LLM. Never hallucinate.
│   ├── slabs.py                ← Old/New regime tax slab computation
│   ├── hra.py                  ← HRA exemption (Sec 10(13A))
│   ├── deductions.py           ← 80C, 80D, 80TTA limits and caps
│   ├── nps.py                  ← NPS (80CCD1B, 80CCD2)
│   ├── home_loan.py            ← Sec 24b interest, 80EEA first-time buyer
│   ├── calculator.py           ← Master orchestrator: calculate_full_tax()
│   └── tax_tools.py            ← [NEW Session 4] LangChain Tool wrappers
│
├── optimization/
│   └── optimizer.py            ← find_optimization_opportunities()
│
├── form16_parser/
│   └── parser.py               ← PDF Form16 extraction
│
├── recommendation_engine/      ← LangGraph workflow
│   ├── state.py                ← GraphState (Pydantic), all intermediate results
│   ├── nodes.py                ← All LangGraph node functions
│   ├── graph.py                ← Graph wiring + run_query() entry point
│   └── gemini_verifier.py      ← [NEW Session 4] Gemini section verification
│
├── api/                        ← FastAPI backend
│   ├── main.py
│   ├── schemas.py
│   └── routes/
│
├── frontend/                   ← Streamlit UI
│
├── scripts/
│   ├── build_index.py          ← Build FAISS index from chunks
│   └── process_pdfs.py         ← PDF → chunks (with cache)
│
├── processed/                  ← Cached chunk JSON files
└── vectordb/faiss_index/       ← Persisted FAISS index files
```

---

## LangGraph Workflow (Node Execution Order)

```
detect_intent
    │
    ├─[has form16]──► parse_form16 ─┐
    │                               │
    └─[no form16]──► maybe_calculate◄┘
                         │
              [has tax_profile]
                         │
                    calculate_tax          ← tax_engine/calculator.py
                         │
              [needs optimization]
                         │
                      optimize             ← optimization/optimizer.py
                         │
                   maybe_retrieve
                         │
              [needs retrieval = True]
                         │
                  retrieve_context         ← rag/retriever.py + reranker.py
                         │
                  generate_answer          ← Qwen/DeepSeek via Ollama
                         │
                  gemini_verify            ← [NEW] gemini_verifier.py
                         │
                        END
```

---

## Key Design Decisions

| Decision | Rationale |
|---|---|
| **Ollama local LLM, not Gemini for generation** | API key blocked by secret scanning on push; offline-first is more reliable for tax (no data leaves machine) |
| **BGE embeddings, not FinLang/finance-embeddings-investopedia** | FinLang model requires HuggingFace online fetch; our offline constraint (`HF_HUB_OFFLINE=1`) would break it. BGE small is already cached and works offline. |
| **Deterministic tax engine (no LLM math)** | LLMs hallucinate numbers. All tax math is pure Python with known slab tables. LLM only narrates the pre-computed result. |
| **FAISS not ChromaDB/Weaviate** | Zero external server dependency; index fits in RAM for this dataset size. |
| **No fine-tuning** | Tax laws change yearly — RAG with curated docs is updateable in seconds vs months of fine-tuning. |
| **Presumptive Tax (Sec 44ADA) as freelancer flag** | `is_freelancer=True` in profile triggers 50% presumptive profit calculation before slab application. |
| **Gemini for VERIFICATION only, not generation** | Local model has grounded RAG context but may cite wrong section numbers. Gemini (with its broader training) verifies section citations after-the-fact. |

---

## Anti-Hallucination Architecture (Session 4 Enhancement)

```
User Query
    │
    ▼
[detect_intent] → extracts income, is_freelancer, preferred_regime
    │
    ▼
[calculate_tax] → Python tax engine → VERIFIED_TAX_DATA (dict)
    │
    ▼
[rag_retrieve] → retrieves legal chunks → LEGAL_CONTEXT + CITATIONS
    │
    ▼
[generate_answer] ← Prompt contains:
    │                 1. REGIME LOCK (if user specified old/new)
    │                 2. VERIFIED_TAX_DATA as JSON (LLM MUST use these numbers)
    │                 3. LEGAL_CONTEXT from RAG
    │                 4. LEGAL_SECTIONS_REFERENCED (section list for LLM to cite)
    │                 5. Hard rules: no hallucination, no self-calculation
    ▼
[gemini_verify] ← checks section citations against Gemini's knowledge
    │              appends ⚠️ corrections to final answer if wrong
    ▼
Final Answer to User
```

---

## Strict Rules in Prompt (Session 4)

1. **REGIME LOCK** — If user says "old regime" or "new regime", the prompt contains a hard lock. LLM must ONLY show that regime's numbers.
2. **VERIFIED_TAX_DATA** — Full JSON from Python tax engine. LLM is told: *"These numbers are computed by a deterministic Python tax engine. You MUST use ONLY these numbers. If you calculate differently, you are WRONG."*
3. **NO MATH** — LLM is forbidden from doing arithmetic or explaining slab breakdowns unless that specific breakdown is in LEGAL_CONTEXT.
4. **SECTION CITATIONS ONLY FROM RAG** — LLM can only cite section numbers that appear in LEGAL_SECTIONS_REFERENCED.
5. **FREELANCER RULE** — If `is_freelancer=True`, LLM must reference Section 44ADA and the 50% presumptive profit rule, not treat it as salary income.

---

## Known Issues & Resolutions

| Issue | Status | Resolution |
|---|---|---|
| `ChatPromptTemplate` not defined error | ✅ Fixed (Session 2) | Removed LangChain template dependency; use plain f-string prompts |
| `RetrievedContext` has no attribute `.get` | ✅ Fixed (Session 2) | Use `state.rag_context.context` (attribute access, not `.get()`) |
| Gemini API key blocked by GitHub secret scanning | ✅ Resolved | Key removed from code; stored only in `.env` which is git-ignored |
| LLM citing wrong sections (194-I instead of 194J for freelancers) | ✅ Fixed (Session 4) | Curated `Presumptive_Taxation.md` updated; strict prompt exclusions added. |
| LLM mixing standard deduction with presumptive profit | ✅ Fixed (Session 4) | Added explicit warning headers and separate tax tables in `Tax_Slabs.md` for Salaried vs Freelancers. |
| Hypothetical income queries not running tax engine | ✅ Fixed (Session 4) | Enhanced query parsing to match "if I earn X" phrasings. |
| LLM calculating non-zero tax for under 12L net income | ✅ Fixed (Session 4) | Added detailed Section 87A Rebate explanations and tables showing final ₹0 tax payable under the New Regime. |

---

## Session Progress Log

### Session 1 (2026-06-30)
- Full project scaffold created
- Tax engine implemented (all deduction modules)
- PDF processing pipeline built
- FAISS index built with curated docs
- Streamlit UI created
- LangSmith tracing connected

### Session 2 (2026-07-10)
- Switched from Gemini to Ollama (qwen2.5-coder:7b primary, deepseek-coder:6.7b fallback)
- Fixed `ChatPromptTemplate` and `RetrievedContext.get()` bugs
- LangSmith confirmed working with local model

### Session 3 (2026-07-11)
- Added `Presumptive_Taxation.md` curated doc (Section 44ADA)
- `calculator.py` updated with `is_freelancer` flag + 50% presumptive profit logic
- `_extract_income_from_query()` detects freelance keywords
- Stricter system prompts added
- RAG index rebuilt

### Session 4 (2026-07-13) ← CURRENT
- Created `architecture.md` living documentation reference
- Implemented structured tax engine tool wrappers in `tax_tools.py`
- Implemented `GeminiVerifier` post-answer section checker in `gemini_verifier.py`
- Wired `gemini_verify_node` into LangGraph execution flow in `graph.py`
- Added strict regime locks and structured prompt inputs to prevent hallucinations
- Enhanced query parser to handle hypothetical phrasing ("if I earn X")
- Separated salaried vs freelancer estimates in `Tax_Slabs.md` to prevent RAG context confusion
- Detailed Section 87A Rebate calculations showing ₹0 tax up to ₹24L gross receipts under Section 44ADA
- Processed updated documents into RAG cache
