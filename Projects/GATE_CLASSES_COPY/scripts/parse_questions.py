#!/usr/bin/env python3
"""
parse_questions.py  –  Extract MCQ / MSQ questions from index.json
===================================================================
Reads the full-text index produced by build_index.py, parses structured
GATE-style questions (from GATEOverflow quiz PDFs), and writes
site/questions.json used by the interactive test engine.

Question format found in the PDFs:
  Q #N  Multiple Choice Type  Award: 1  Penalty: 0.33  Subject
  <question text>
  A. <option A>
  B. <option B>
  C. <option C>
  D. <option D>
  Your Answer:  Correct Answer: X  Not Attempted  Time taken: ...  Discuss

Usage:
    python scripts/parse_questions.py

Output:
    site/questions.json
"""

import re
import json
import sys
from pathlib import Path


# ── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent.resolve()
ROOT_DIR     = SCRIPT_DIR.parent.resolve()
INDEX_FILE   = ROOT_DIR / "site" / "index.json"
OUTPUT_FILE  = ROOT_DIR / "site" / "questions.json"


# ── Regex patterns for the GATEOverflow quiz-result format ───────────────────

# Header line: "Q #3  Multiple Select Type  Award: 2  Penalty: 0  Operating System"
RE_Q_HEADER = re.compile(
    r'Q\s*#\s*(\d+)\s+'                       # Q #N
    r'(Multiple\s+(?:Choice|Select)\s+Type)'  # MCQ or MSQ
    r'\s+Award:\s*([\d.]+)'                   # marks
    r'\s+Penalty:\s*([\d.]+)',                # penalty
    re.IGNORECASE,
)

# Answer tag: "Your Answer:  Correct Answer: A;B  Not Attempted  Time taken:"
RE_ANSWER = re.compile(
    r'Correct Answer:\s*([A-D][;A-D]*)',
    re.IGNORECASE,
)

# Page-break noise line inserted by the PDF renderer
RE_PAGE_BREAK = re.compile(
    r'https?://\S+\s+\d+/\d+',
)

# Timestamp header noise from Chrome print-to-PDF
RE_TIMESTAMP = re.compile(
    r'^\d+/\d+/\d+,\s+\d+:\d+\s+[AP]M\s+\S+',
    re.MULTILINE,
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def clean_text(s: str) -> str:
    """Remove excess whitespace while preserving newlines."""
    lines = []
    for line in s.splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def strip_noise(text: str) -> str:
    """Remove PDF-rendering artefacts: URLs, time-stamps, headers."""
    text = RE_PAGE_BREAK.sub("", text)
    text = RE_TIMESTAMP.sub("", text)
    # Remove "Summary in Graph / Exam Summary" header block (first ~30 lines)
    # by looking for "EXAM RESPONSE" as the real start of questions
    marker = re.search(r'EXAM RESPONSE\s+EXAM STATS\s+FEEDBACK', text, re.IGNORECASE)
    if marker:
        text = text[marker.end():]
    return text


def split_into_blocks(text: str) -> list[str]:
    """Split text into per-question blocks using Q # headers as delimiters."""
    positions = [m.start() for m in RE_Q_HEADER.finditer(text)]
    if not positions:
        return []
    blocks = []
    for i, start in enumerate(positions):
        end = positions[i + 1] if i + 1 < len(positions) else len(text)
        blocks.append(text[start:end])
    return blocks


def parse_options(block: str) -> tuple[dict[str, str], str]:
    """
    Extract options A-D from a question block.
    Returns (options_dict, question_text_before_options).

    Handles two PDF layouts:

    Layout 1 – "text-after" (normal):
        A. Option text here
        B. Another option
        ...

    Layout 2 – "text-before" (2×2 grid PDF):
        [option A text]
        A.
        [option B text]
        B.
        ...
        D.
        [option D text]   ← last option comes AFTER its letter
    """
    # ── detect layout ──
    # "text-after": A. is followed by a space+text on the same line
    inline = re.search(r'(?m)^A\. +\S', block)  # A. <space> <text> on same line
    eol_a  = re.search(r'(?m)^A\.\s*$', block)  # A. alone on a line

    if inline:
        return _parse_text_after(block)
    elif eol_a:
        return _parse_text_before_grid(block)
    else:
        # fallback: try text-after
        return _parse_text_after(block)


def _parse_text_after(block: str) -> tuple[dict[str, str], str]:
    """Options are: 'A. text\nB. text\n...' """
    opt_pat = re.compile(r'(?m)^([A-D])\.\s+(.+?)(?=\n[A-D]\.|\nYour Answer:|$)', re.DOTALL)
    matches = list(opt_pat.finditer(block))
    if not matches:
        return {}, block
    options = {}
    for m in matches:
        key = m.group(1).upper()
        text = clean_text(m.group(2))
        # Strip trailing "Your Answer:..." noise
        text = re.sub(r'\s*Your Answer:.*', '', text, flags=re.DOTALL).strip()
        options[key] = text
    pre_text = block[: matches[0].start()]
    return options, pre_text


def _parse_text_before_grid(block: str) -> tuple[dict[str, str], str]:
    """
    Options in 2×2 grid layout extracted as:
        [text_A]  A.  [text_B]  B.  [text_C]  C.  D.  [text_D]
    Mapping: text BEFORE each letter = that option's text,
             EXCEPT option D whose text appears AFTER 'D.'.
    """
    # Find standalone letter markers (letter on its own line):  \nA.\n  or  \nA.\r\n
    letter_pat = re.compile(r'(?m)^([A-D])\.\s*$')
    markers = list(letter_pat.finditer(block))
    if len(markers) < 4:
        # Some markers may be inline; fall back
        return _parse_text_after(block)

    # Build segments
    # segments[i] = text BEFORE markers[i]
    starts = [m.start() for m in markers] + [len(block)]
    options: dict[str, str] = {}

    # Segment 0 (before A): strip question body from it.
    # We take only the last paragraph (closest to the A. marker).
    seg0 = block[: markers[0].start()]
    # The question text is in seg0 up to the last blank-ish boundary
    # → find last multi-newline gap to separate question from option A text
    gap = re.search(r'\n{2,}', seg0[::-1])  # reversed search from end
    if gap:
        opt_a_text = seg0[len(seg0) - gap.start():]
        q_text = seg0[: len(seg0) - gap.start()]
    else:
        # No clear gap; use a heuristic: last line of seg0 is option A
        lines = [l for l in seg0.splitlines() if l.strip()]
        if lines:
            opt_a_text = lines[-1]
            q_text = "\n".join(lines[:-1])
        else:
            opt_a_text = ""
            q_text = seg0

    options["A"] = clean_text(opt_a_text)

    # Segments 1–2 (between A–B and B–C) → options B and C
    for i, key in enumerate(["B", "C"], start=1):
        raw = block[markers[i - 1].end(): markers[i].start()]
        raw = re.sub(r'\nYour Answer:.*', '', raw, flags=re.DOTALL)
        options[key] = clean_text(raw)

    # Segment after D (index 3) → option D
    raw_d = block[markers[3].end():]
    raw_d = re.sub(r'\s*Your Answer:.*', '', raw_d, flags=re.DOTALL)
    options["D"] = clean_text(raw_d)

    # If option C is empty but between C and D segment has text, use that
    seg_c_d = block[markers[2].end(): markers[3].start()]
    if not options.get("C") and seg_c_d.strip():
        options["C"] = clean_text(seg_c_d)

    # Filter out empties; if we lost too many, fall back
    non_empty = sum(1 for v in options.values() if v)
    if non_empty < 2:
        return _parse_text_after(block)

    return options, q_text


def parse_block(block: str, doc_meta: dict, global_id: int) -> dict | None:
    """Parse a single question block into a structured dict."""
    header_m = RE_Q_HEADER.search(block)
    if not header_m:
        return None

    q_num    = int(header_m.group(1))
    q_type   = header_m.group(2).strip().lower()
    award    = float(header_m.group(3))
    penalty  = float(header_m.group(4))
    is_msq   = "select" in q_type   # Multiple Select = MSQ

    # Text after the header line
    after_header = block[header_m.end():].strip()

    # Extract correct answer
    ans_m   = RE_ANSWER.search(after_header)
    correct = None
    if ans_m:
        raw_ans = ans_m.group(1).upper()
        correct = raw_ans.split(";")   # ["A"] or ["A","B","D"]

    # Remove "Your Answer:..." trailing line before parsing options
    after_trimmed = after_header
    if ans_m:
        after_trimmed = after_header[: ans_m.start()]

    # Extract options and pre-option text (= question body)
    options, question_body = parse_options(after_trimmed)

    if not options:
        return None

    # Clean up question body
    # Remove page header noise: "Technical", subject name alone on line, etc.
    question_body = re.sub(r'\bDiscuss\b', '', question_body, flags=re.IGNORECASE)
    # Strip the leading subject tag if it appears (e.g. "Algorithms\n" at top)
    question_body = re.sub(r'^(Technical|Operating System|Algorithms|Data Structures|'
                           r'Computer Networks|Compiler Design|Theory of Computation|'
                           r'Computer Organization|Digital Logic|C Programming|'
                           r'Mathematics)\s*\n', '', question_body, flags=re.IGNORECASE)
    question_body = clean_text(question_body)

    if len(question_body) < 10 or len(options) < 2:
        return None

    return {
        "id":       str(global_id),
        "num":      q_num,
        "subject":  doc_meta["subject"],
        "label":    doc_meta["label"],
        "source":   doc_meta.get("source", "test-series"),
        "docTitle": doc_meta["title"],
        "type":     "msq" if is_msq else "mcq",
        "marks":    award,
        "penalty":  penalty,
        "text":     question_body,
        "options":  options,
        "answer":   correct,          # list of correct option keys, or None
    }


# ── Core pipeline ─────────────────────────────────────────────────────────────

def parse_all_questions() -> list[dict]:
    if not INDEX_FILE.exists():
        print(f"[ERROR] {INDEX_FILE} not found. Run build_index.py first.", file=sys.stderr)
        sys.exit(1)

    index = json.loads(INDEX_FILE.read_bytes())
    all_questions: list[dict] = []
    global_id = 1

    for doc in index["documents"]:
        if doc.get("source") != "test-series":
            continue   # only parse PDFs from test series

        text = strip_noise(doc["text"])
        blocks = split_into_blocks(text)
        if not blocks:
            continue

        doc_qs = 0
        for block in blocks:
            q = parse_block(block, doc, global_id)
            if q:
                all_questions.append(q)
                global_id += 1
                doc_qs += 1

        print(f"  {doc['label']:<45}  {doc['title'][:40]:<40}  {doc_qs:3d} Qs")

    return all_questions


def write_questions(questions: list[dict]) -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Build subject summary
    by_subject: dict[str, int] = {}
    by_type: dict[str, int] = {"mcq": 0, "msq": 0}
    for q in questions:
        by_subject[q["label"]] = by_subject.get(q["label"], 0) + 1
        by_type[q["type"]] = by_type.get(q["type"], 0) + 1

    payload = {
        "version":      1,
        "totalQ":       len(questions),
        "bySubject":    by_subject,
        "byType":       by_type,
        "questions":    questions,
    }

    OUTPUT_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    size_kb = OUTPUT_FILE.stat().st_size / 1024
    print(f"\n  Output : {OUTPUT_FILE}")
    print(f"  Size   : {size_kb:.1f} KB")
    print(f"  Total  : {len(questions)} questions  (MCQ: {by_type['mcq']}  MSQ: {by_type['msq']})")
    print()
    for subj, cnt in sorted(by_subject.items()):
        print(f"           • {subj:<45} {cnt:3d}")


def main():
    print("=" * 70)
    print("  GATE Prep — Question Parser")
    print("=" * 70)
    print(f"  Source : {INDEX_FILE}")
    print(f"  Output : {OUTPUT_FILE}\n")

    questions = parse_all_questions()

    if not questions:
        print("[WARN] No questions parsed.", file=sys.stderr)
        sys.exit(0)

    print()
    write_questions(questions)
    print("\n✓  Done.  Open site/test.html to start a mock test.")


if __name__ == "__main__":
    main()
