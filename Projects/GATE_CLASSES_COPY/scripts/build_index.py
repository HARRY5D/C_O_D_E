#!/usr/bin/env python3
"""
build_index.py  –  One-time indexer for GATE Prep static website
=================================================================
Scans TWO content roots:

  1.  data/                   – plain-text (.txt / .md) notes & summaries
  2.  test series_scrapped/   – real GATE test-series PDFs, subject folders

Produces a single  site/index.json  loaded once by the browser.
MiniSearch.js then builds an in-memory inverted index for instant search.

Run this script whenever you add or change files.

Usage
-----
    python scripts/build_index.py

Adding new content
------------------
* Drop a .txt/.md file into  data/<subject>/
  OR drop a .pdf into  "test series_scrapped/<subject>/"
* Re-run: python scripts/build_index.py
* Refresh the browser — done.
"""

import re
import sys
import json
from pathlib import Path
from datetime import datetime, timezone


# ─── Locate project root ─────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent.resolve()
ROOT_DIR    = SCRIPT_DIR.parent.resolve()

DATA_DIR    = ROOT_DIR / "data"
PDF_DIR     = ROOT_DIR / "test series_scrapped"
OUTPUT_FILE = ROOT_DIR / "site" / "index.json"

SNIPPET_LENGTH = 500   # chars shown in result cards

# ── Subject label map  (add entries for any new folder you create) ─────────
SUBJECT_LABELS = {
    # data/ folders
    "os":               "Operating Systems",
    "dbms":             "Database Management Systems",
    "cn":               "Computer Networks",
    "algo":             "Algorithms",
    "ds":               "Data Structures",
    "toc":              "Theory of Computation",
    "co":               "Computer Organization",
    "dm":               "Discrete Mathematics",
    # test series_scrapped/ folders  (keys = folder name lowercased)
    "c":                "C Programming",
    "cd":               "Compiler Design",
    "coa":              "Computer Organization & Architecture",
    "dld":              "Digital Logic Design",
    "full_length test": "Full Length Tests",
    "mix_tests":        "Mixed Subject Tests",
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_label(folder_name: str) -> str:
    return SUBJECT_LABELS.get(folder_name.lower(), folder_name.replace("_", " ").title())


def build_snippet(text: str) -> str:
    cleaned = re.sub(r"\n{3,}", "\n\n", text).strip()
    return cleaned[:SNIPPET_LENGTH] + ("…" if len(cleaned) > SNIPPET_LENGTH else "")


def extract_title_from_text(content: str, stem: str) -> str:
    """Pull a title from file content or fall back to filename stem."""
    for line in content.splitlines()[:10]:
        m = re.match(r"^(?:Topic|Title)\s*:\s*(.+)", line, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    for line in content.splitlines()[:20]:
        s = line.strip()
        if s and s.isupper() and 5 < len(s) < 80:
            return s.title()
    return stem.replace("_", " ").replace("-", " ").title()


def title_from_pdf_name(filename: str) -> str:
    """'OS Topic Wise Test 1 - Scheduling.pdf' → 'OS Topic Wise Test 1 - Scheduling'"""
    stem = Path(filename).stem
    return re.sub(r"\s{2,}", " ", stem).strip()


def extract_text_from_pdf(path: Path) -> str:
    """Extract plain text from a PDF with pdfplumber. Returns '' on failure."""
    try:
        import pdfplumber
    except ImportError:
        print("\n  [WARN] pdfplumber not installed — skipping PDFs.", file=sys.stderr)
        print("         Fix: pip install pdfplumber", file=sys.stderr)
        return ""
    try:
        import logging
        # Suppress noisy "FontBBox" warnings that come from pdfminer's font parser
        logging.getLogger("pdfminer").setLevel(logging.ERROR)

        pages = []
        with pdfplumber.open(str(path)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    pages.append(t)
        return "\n\n".join(pages)
    except Exception as e:
        print(f"\n  [ERROR] {path.name}: {e}", file=sys.stderr)
        return ""


# ─── Indexing routines ────────────────────────────────────────────────────────

def index_text_files(start_id: int) -> tuple[list[dict], int]:
    """Scan data/ for .txt and .md files."""
    docs   = []
    doc_id = start_id

    if not DATA_DIR.exists():
        print(f"  [SKIP] data/ not found at {DATA_DIR}")
        return docs, doc_id

    for subject_dir in sorted(d for d in DATA_DIR.iterdir() if d.is_dir()):
        label = get_label(subject_dir.name)
        files = sorted(
            f for f in subject_dir.rglob("*")
            if f.is_file() and f.suffix.lower() in {".txt", ".md"}
        )
        if not files:
            continue

        print(f"  [TXT] {label:<45}  {len(files):3d} file(s)")
        for fp in files:
            try:
                content = fp.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                print(f"    [ERROR] {fp.name}: {e}", file=sys.stderr)
                continue
            if not content.strip():
                continue
            docs.append({
                "id":       str(doc_id),
                "subject":  subject_dir.name.lower(),
                "label":    label,
                "title":    extract_title_from_text(content, fp.stem),
                "text":     content,
                "snippet":  build_snippet(content),
                "filename": fp.relative_to(DATA_DIR).as_posix(),
                "source":   "notes",
            })
            doc_id += 1

    return docs, doc_id


def index_pdf_files(start_id: int) -> tuple[list[dict], int]:
    """Scan test series_scrapped/ for PDFs and extract their text."""
    docs   = []
    doc_id = start_id

    if not PDF_DIR.exists():
        print(f"  [SKIP] 'test series_scrapped/' not found at {PDF_DIR}")
        return docs, doc_id

    subject_dirs = sorted(d for d in PDF_DIR.iterdir() if d.is_dir())
    total = sum(
        1 for d in subject_dirs
        for f in d.iterdir() if f.is_file() and f.suffix.lower() == ".pdf"
    )
    print(f"\n  Scanning {total} PDF(s) across {len(subject_dirs)} subject folder(s)…\n")

    for subject_dir in subject_dirs:
        folder_key = subject_dir.name.lower().replace(" ", "_")
        label      = get_label(subject_dir.name)
        pdfs = sorted(
            f for f in subject_dir.iterdir()
            if f.is_file() and f.suffix.lower() == ".pdf"
        )
        if not pdfs:
            continue

        print(f"  [PDF] {label:<45}  {len(pdfs):3d} file(s)  ", end="", flush=True)
        ok = 0
        for fp in pdfs:
            text = extract_text_from_pdf(fp)
            if not text.strip():
                continue    # skip blank / image-only PDFs
            docs.append({
                "id":       str(doc_id),
                "subject":  folder_key,
                "label":    label,
                "title":    title_from_pdf_name(fp.name),
                "text":     text,
                "snippet":  build_snippet(text),
                "filename": fp.relative_to(PDF_DIR).as_posix(),
                "source":   "test-series",
            })
            doc_id += 1
            ok += 1
        print(f"({ok} extracted)")

    return docs, doc_id


# ─── Output ───────────────────────────────────────────────────────────────────

def write_index(documents: list[dict]) -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    by_subject: dict[str, int] = {}
    for d in documents:
        by_subject[d["label"]] = by_subject.get(d["label"], 0) + 1

    payload = {
        "version":   2,
        "generated": datetime.now(timezone.utc).isoformat(),
        "totalDocs": len(documents),
        "subjects":  by_subject,
        "documents": documents,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))

    size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    print(f"\n  Output   : {OUTPUT_FILE}")
    print(f"  Size     : {size_mb:.2f} MB")
    print(f"  Docs     : {len(documents)}")
    for subj, cnt in sorted(by_subject.items()):
        print(f"             • {subj:<45} {cnt:3d}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("  GATE Prep — Index Builder  (txt + PDF)")
    print("=" * 65)
    print(f"  Notes  : {DATA_DIR}")
    print(f"  PDFs   : {PDF_DIR}")
    print(f"  Output : {OUTPUT_FILE}\n")

    txt_docs, next_id = index_text_files(start_id=1)
    pdf_docs, _       = index_pdf_files(start_id=next_id)
    all_docs          = txt_docs + pdf_docs

    if not all_docs:
        print("\n[WARN] No documents indexed.", file=sys.stderr)
        sys.exit(0)

    print()
    write_index(all_docs)
    print("\n✓  Done.  Open site/index.html in your browser.")
    print("   (No server needed — just double-click the file.)")


if __name__ == "__main__":
    main()
