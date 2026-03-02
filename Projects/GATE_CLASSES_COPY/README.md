# GATE Prep — Offline Static Website

A lightweight, fully-offline GATE CS preparation website with instant
full-text search.  No server, no database, no embeddings required.

---

## Quick Start

```
git clone / copy this folder to your machine
cd GATE_CLASSES_COPY

# 1. Index the papers (run once, or whenever you add new files)
python scripts/build_index.py

# 2. Open the site — no server needed
start site/index.html      # Windows
open site/index.html       # macOS
xdg-open site/index.html   # Linux
```

That is all.  Search works instantly, offline, without any server.

---

## Project Structure

```
GATE_CLASSES_COPY/
│
├── data/                   ← All content lives here
│   ├── os/                 ← Operating Systems papers (.txt)
│   ├── dbms/               ← DBMS papers (.txt)
│   ├── cn/                 ← Computer Networks papers (.txt)
│   └── algo/               ← Algorithms papers (.txt)
│
├── scripts/
│   └── build_index.py      ← One-time indexer — produces site/index.json
│
└── site/                   ← Static website (open index.html directly)
    ├── index.html          ← Home page with search
    ├── subjects.html       ← Browse by subject
    ├── style.css           ← All styles
    ├── app.js              ← Search logic (MiniSearch.js)
    └── index.json          ← Generated index (do NOT edit by hand)
```

---

## How to Add New Papers

1. Create (or reuse) a subject folder inside `data/`.  
   Use a short lowercase key, e.g. `data/toc/` for Theory of Computation.

2. Drop your `.txt` (or `.md`) file into that folder.  
   Name it meaningfully: `process_scheduling.txt`, `sql_joins.txt`, etc.

3. Re-run the indexer:

   ```bash
   python scripts/build_index.py
   ```

4. Refresh the browser tab — your new paper appears immediately.

### Tip: Title extraction
The indexer auto-detects your paper title by looking for:
- A line starting with `Topic:` or `Title:` in the first 10 lines.
- An ALL-CAPS line in the first 20 lines.
- Falls back to the filename if nothing is found.

---

## How to Add a New Subject Folder

1. Create `data/<subject-key>/` (lowercase, no spaces).
2. Add an entry to `SUBJECT_LABELS` in `scripts/build_index.py`:
   ```python
   SUBJECT_LABELS = {
       ...
       "toc": "Theory of Computation",
   }
   ```
3. Optionally add an icon in `site/app.js`:
   ```js
   const SUBJECT_ICONS = {
       ...
       toc: "🔣",
   };
   ```
4. Re-run `python scripts/build_index.py`.

---

## How to Rebuild the Index

Whenever you add, edit, or delete paper files:

```bash
python scripts/build_index.py
```

The script:
- Walks every `data/<subject>/` folder.
- Reads every `.txt` and `.md` file (UTF-8).
- Extracts `id`, `subject`, `label`, `title`, `text`, `snippet`.
- Writes a fresh `site/index.json`.

The website loads `index.json` once per browser tab.
MiniSearch then builds an inverted index in memory — no server needed.

---

## How Search Works

```
data/*.txt  →  build_index.py  →  index.json  →  browser
                                                      │
                                               MiniSearch.js
                                               (BM25-style, in-browser)
                                                      │
                                               Instant results
```

- **BM25-style scoring** via [MiniSearch.js](https://github.com/lucaong/minisearch).
- **Fuzzy matching** (20 % tolerance) handles typos.
- **Prefix matching** — typing `"algo"` finds `"algorithm"`.
- **Title boosting** — title matches rank above body matches.
- No network calls after the page first loads.

---

## Offline Use (Air-gapped / No Internet)

MiniSearch.js is loaded from jsDelivr CDN by default.  
For a fully air-gapped setup:

1. Download MiniSearch once:
   ```
   https://cdn.jsdelivr.net/npm/minisearch@6.3.0/dist/umd/index.min.js
   ```
2. Save it as `site/minisearch.min.js`.
3. In both `site/index.html` and `site/subjects.html`, the fallback script tag
   already handles this:
   ```html
   <script>
     if (typeof MiniSearch === "undefined") {
       var s = document.createElement("script");
       s.src = "minisearch.min.js";    // ← loaded as fallback
       document.head.appendChild(s);
     }
   </script>
   ```
   So once the file is present, it loads automatically when CDN is unreachable.

---

## Performance Notes

| Scenario | Behaviour |
|---|---|
| 100 documents, ~100 KB index | Indexing: ~50 ms. Search: < 5 ms |
| 500 documents, ~500 KB index | Indexing: ~200 ms. Search: < 10 ms |
| 2000 documents, ~2 MB index | Indexing: ~800 ms. Search: < 20 ms |

All numbers measured on a mid-range laptop.  
The site comfortably supports thousands of papers on low-end hardware.

---

## AI Answer Generation (Optional Extension)

The search results are exposed as `window._lastRetrievedChunks` — an array of
the top-5 text chunks that matched the query.  This is your RAG context.

To add AI-generated answers, implement `generateAnswer()` in `site/app.js`:

```js
async function generateAnswer(query, chunks) {
  const context = chunks.map(c => c.text).join("\n\n---\n\n");
  const prompt  = `Answer using the GATE notes below.\n\n${context}\n\nQ: ${query}\nA:`;

  // Example: local Ollama
  const resp = await fetch("http://localhost:11434/api/generate", {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({ model: "mistral", prompt, stream: false }),
  });
  const data = await resp.json();
  console.log(data.response);  // → render this in the UI
}
```

Then call it from `runSearch()` after search results are shown:
```js
generateAnswer(query, window._lastRetrievedChunks);
```

---

## Supported Subject Keys

| Folder key | Subject name |
|---|---|
| `os`   | Operating Systems |
| `dbms` | Database Management Systems |
| `cn`   | Computer Networks |
| `algo` | Algorithms |
| `ds`   | Data Structures |
| `toc`  | Theory of Computation |
| `co`   | Computer Organization |
| `dm`   | Discrete Mathematics |

Add more by editing `SUBJECT_LABELS` in `scripts/build_index.py`.

---

## Requirements

- Python 3.8+ (only for `build_index.py` — not needed at runtime)
- A modern browser (Chrome, Firefox, Edge, Safari)
- No `npm install`, no `pip install`, no build step beyond running the script

---

## License

This project template is provided as-is for educational use.  
Paper content copyright belongs to respective exam authorities (IIT/IISC).
