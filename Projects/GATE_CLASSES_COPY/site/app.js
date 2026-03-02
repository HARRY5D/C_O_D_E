/**
 * app.js  –  GATE Prep Static Website
 * ====================================
 * Responsibilities:
 *   1. Load index.json once on page load.
 *   2. Build a MiniSearch instance in the browser (BM25-style lexical search).
 *   3. Power the search box on index.html (live-as-you-type).
 *   4. Populate subject cards on index.html.
 *   5. Populate the sidebar + paper list on subjects.html.
 *   6. Open a paper in a modal overlay.
 *
 * No server, no network call after index.json is loaded, no embeddings.
 * Every operation runs locally in the browser tab.
 *
 * ─── AI Hook ──────────────────────────────────────────────────────────────
 * When a search is performed, we collect the top result text chunks into
 * `window._lastRetrievedChunks`.  To add AI-generated answers later, call:
 *
 *   generateAnswer(query, window._lastRetrievedChunks)
 *
 * and implement `generateAnswer()` using any local or remote LLM API.
 * ─────────────────────────────────────────────────────────────────────────
 */

"use strict";

// ── State ──────────────────────────────────────────────────────────────────
/** @type {{ version: number, totalDocs: number, documents: Document[] } | null} */
let _indexData = null;

/** @type {MiniSearch | null} */
let _miniSearch = null;

/** Lookup map: document id → document object */
const _docById = new Map();

/** Subject icon map — extend freely */
const SUBJECT_ICONS = {
  os:               "🖥️",
  dbms:             "🗄️",
  cn:               "🌐",
  algo:             "⚙️",
  ds:               "🌲",
  toc:              "🔣",
  co:               "🔌",
  dm:               "∀",
  // test-series subjects
  c:                "🔡",
  cd:               "⚗️",
  coa:              "🖲️",
  dld:              "🔲",
  full_length_test: "📝",
  mix_tests:        "🧪",
};

// ── Detect which page we're on ─────────────────────────────────────────────
const PAGE = (() => {
  const p = location.pathname;
  if (p.endsWith("subjects.html")) return "subjects";
  return "home";
})();


// ═══════════════════════════════════════════════════════════════════════════
// 1.  INDEX LOADING
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Fetch index.json, initialise MiniSearch, then boot the correct page.
 * index.json is loaded ONCE; subsequent searches reuse the in-memory index.
 */
async function loadIndex() {
  try {
    const resp = await fetch("index.json");
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    _indexData = await resp.json();
  } catch (err) {
    setStatus("⚠️  Could not load index.json. Run build_index.py first.", "warn");
    console.error("[GATEPrep] Failed to load index.json:", err);
    return;
  }

  // Build lookup map
  for (const doc of _indexData.documents) {
    _docById.set(doc.id, doc);
  }

  // ── Initialise MiniSearch ────────────────────────────────────────────────
  // MiniSearch builds an inverted index in the browser from the documents.
  // This is the only "indexing" step — it happens once per page load.
  _miniSearch = new MiniSearch({
    fields: ["title", "text"],          // Fields to index for search
    storeFields: ["id", "title", "subject", "label", "snippet"], // Fields to return
    searchOptions: {
      boost: { title: 3 },              // Title matches rank higher
      fuzzy: 0.2,                       // Allow ~20% fuzziness
      prefix: true,                     // Match prefixes (e.g. "algo" → "algorithm")
    },
  });

  _miniSearch.addAll(_indexData.documents);

  setStatus(
    `✓ Index loaded — ${_indexData.totalDocs} documents across ${countSubjects()} subjects`,
    "ok",
  );

  // Boot page-specific UI
  if (PAGE === "home")     bootHomePage();
  if (PAGE === "subjects") bootSubjectsPage();
}


// ── Helpers ────────────────────────────────────────────────────────────────

function countSubjects() {
  return new Set(_indexData.documents.map((d) => d.subject)).size;
}

/** Group documents by subject and return array of { subject, label, docs } */
function groupBySubject() {
  const map = new Map();
  for (const doc of _indexData.documents) {
    if (!map.has(doc.subject)) {
      map.set(doc.subject, { subject: doc.subject, label: doc.label, docs: [] });
    }
    map.get(doc.subject).docs.push(doc);
  }
  return [...map.values()];
}

function setStatus(msg, type = "ok") {
  const el = document.getElementById("searchStatus");
  if (!el) return;
  el.textContent = msg;
  el.style.color = type === "warn" ? "#fca5a5" : "#a5f3fc";
}


// ═══════════════════════════════════════════════════════════════════════════
// 2.  HOME PAGE
// ═══════════════════════════════════════════════════════════════════════════

function bootHomePage() {
  renderSubjectCards();
  bindSearchInput();
}

/** Render colored subject cards in the grid */
function renderSubjectCards() {
  const grid = document.getElementById("subjectCards");
  if (!grid) return;

  const groups = groupBySubject();
  if (!groups.length) {
    grid.innerHTML = '<p class="card-placeholder">No documents found. Add .txt files to data/ folders and re-run build_index.py.</p>';
    return;
  }

  grid.innerHTML = groups.map((g) => {
    const icon = SUBJECT_ICONS[g.subject] || "📄";
    return `
      <div class="subject-card" onclick="openSubjectPage('${g.subject}')" role="button" tabindex="0"
           aria-label="Browse ${g.label}">
        <div class="card-icon">${icon}</div>
        <div class="card-title">${g.label}</div>
        <div class="card-count">${g.docs.length} paper${g.docs.length !== 1 ? "s" : ""}</div>
      </div>`;
  }).join("");

  // Keyboard support
  grid.querySelectorAll(".subject-card").forEach((card) => {
    card.addEventListener("keydown", (e) => {
      if (e.key === "Enter") card.click();
    });
  });
}

/** Navigate to subjects.html pre-selecting a subject */
function openSubjectPage(subject) {
  window.location.href = `subjects.html?subject=${encodeURIComponent(subject)}`;
}

// ── Live Search ─────────────────────────────────────────────────────────────

function bindSearchInput() {
  const input = document.getElementById("searchInput");
  if (!input) return;

  let debounceTimer;
  input.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => runSearch(input.value.trim()), 200);
  });
  input.addEventListener("keydown", (e) => {
    if (e.key === "Escape") clearSearch();
  });
}

/** Called by the search button click or Enter key */
function triggerSearch() {
  const input = document.getElementById("searchInput");
  if (input) runSearch(input.value.trim());
}

function runSearch(query) {
  const section = document.getElementById("searchResultsSection");
  const subjectsSection = document.getElementById("subjectsSection");
  const grid = document.getElementById("resultsGrid");
  const count = document.getElementById("resultsCount");
  if (!section || !grid) return;

  if (!query) {
    clearSearch();
    return;
  }

  if (!_miniSearch) {
    setStatus("⚠️  Search index not ready yet.", "warn");
    return;
  }

  const results = _miniSearch.search(query, { combineWith: "OR", boost: { title: 3 }, fuzzy: 0.2, prefix: true });

  // ── AI Hook ────────────────────────────────────────────────────────────
  // Expose top result chunks for a future AI answer generation step.
  window._lastSearchQuery = query;
  window._lastRetrievedChunks = results.slice(0, 5).map((r) => ({
    id:      r.id,
    subject: r.subject,
    title:   r.title,
    text:    _docById.get(r.id)?.text ?? "",
    score:   r.score,
  }));
  // To add AI answers: call generateAnswer(query, window._lastRetrievedChunks)
  // ── End AI Hook ───────────────────────────────────────────────────────

  section.classList.remove("hidden");
  if (subjectsSection) subjectsSection.classList.add("hidden");

  if (!results.length) {
    count.textContent = "No results";
    grid.innerHTML = `
      <div class="no-results">
        <p>No results for "<strong>${escapeHtml(query)}</strong>"</p>
        <p style="margin-top:.5rem;font-size:.82rem">
          Try different keywords or check spelling.
        </p>
      </div>`;
    return;
  }

  count.textContent = `${results.length} result${results.length !== 1 ? "s" : ""} for "${query}"`;
  grid.innerHTML = results.slice(0, 40).map((r) => {
    const doc = _docById.get(r.id);
    if (!doc) return "";
    const highlighted = highlightSnippet(doc.snippet, query);
    const sourceTag = doc.source === "test-series"
      ? `<span class="source-tag test-series">Test Series</span>`
      : `<span class="source-tag notes">Notes</span>`;
    return `
      <div class="result-card" onclick="openPaperModal('${r.id}')" role="button" tabindex="0">
        <div class="result-meta">
          <div class="result-badge">${escapeHtml(doc.label)}</div>
          ${sourceTag}
        </div>
        <div class="result-title">${escapeHtml(doc.title)}</div>
        <div class="result-snippet">${highlighted}</div>
      </div>`;
  }).join("");

  grid.querySelectorAll(".result-card").forEach((card) => {
    card.addEventListener("keydown", (e) => {
      if (e.key === "Enter") card.click();
    });
  });
}

function clearSearch() {
  const input = document.getElementById("searchInput");
  const section = document.getElementById("searchResultsSection");
  const subjectsSection = document.getElementById("subjectsSection");

  if (input) input.value = "";
  if (section) section.classList.add("hidden");
  if (subjectsSection) subjectsSection.classList.remove("hidden");

  window._lastRetrievedChunks = [];
}


// ═══════════════════════════════════════════════════════════════════════════
// 3.  SUBJECTS PAGE
// ═══════════════════════════════════════════════════════════════════════════

function bootSubjectsPage() {
  const groups = groupBySubject();
  renderSidebar(groups);

  // Auto-select from URL param (?subject=os)
  const params = new URLSearchParams(window.location.search);
  const autoSubject = params.get("subject");
  if (autoSubject && groups.find((g) => g.subject === autoSubject)) {
    selectSubject(autoSubject, groups);
  }
}

function renderSidebar(groups) {
  const sidebar = document.getElementById("sidebarList");
  if (!sidebar) return;

  sidebar.innerHTML = groups.map((g) => {
    const icon = SUBJECT_ICONS[g.subject] || "📄";
    return `
      <li data-subject="${g.subject}">
        <button onclick="selectSubject('${g.subject}', null)">
          ${icon} ${escapeHtml(g.label)}
          <span style="float:right;font-size:.78rem;color:var(--text-secondary)">${g.docs.length}</span>
        </button>
      </li>`;
  }).join("");
}

function selectSubject(subject, groups) {
  if (!groups) groups = groupBySubject();
  const group = groups.find((g) => g.subject === subject);
  if (!group) return;

  // Update sidebar highlight
  document.querySelectorAll("#sidebarList li").forEach((li) => {
    li.classList.toggle("active", li.dataset.subject === subject);
  });

  // Update URL (no reload)
  history.replaceState(null, "", `?subject=${encodeURIComponent(subject)}`);

  // Render papers
  const placeholder = document.getElementById("papersPlaceholder");
  const header = document.getElementById("papersHeader");
  const titleEl = document.getElementById("panelSubjectTitle");
  const countEl = document.getElementById("panelPaperCount");
  const list = document.getElementById("papersList");

  if (placeholder) placeholder.style.display = "none";
  if (header) header.classList.remove("hidden");
  if (titleEl) titleEl.textContent = group.label;
  if (countEl) countEl.textContent = `${group.docs.length} paper${group.docs.length !== 1 ? "s" : ""}`;

  if (list) {
    list.innerHTML = group.docs.map((doc) => `
      <div class="paper-item" onclick="openPaperModal('${doc.id}')" role="button" tabindex="0">
        <div class="paper-icon">📄</div>
        <div class="paper-info">
          <div class="paper-title">${escapeHtml(doc.title)}</div>
          <div class="paper-snippet">${escapeHtml(doc.snippet)}</div>
        </div>
        <div class="paper-arrow">›</div>
      </div>`).join("");

    list.querySelectorAll(".paper-item").forEach((item) => {
      item.addEventListener("keydown", (e) => {
        if (e.key === "Enter") item.click();
      });
    });
  }
}


// ═══════════════════════════════════════════════════════════════════════════
// 4.  PAPER MODAL
// ═══════════════════════════════════════════════════════════════════════════

function openPaperModal(id) {
  const doc = _docById.get(id);
  if (!doc) return;

  document.getElementById("modalBadge").textContent   = doc.label;
  document.getElementById("modalTitle").textContent   = doc.title;
  document.getElementById("modalContent").textContent = doc.text;

  document.getElementById("paperModal").classList.remove("hidden");
  document.body.style.overflow = "hidden";
}

function closePaperModal(event) {
  // If event is provided (overlay click), only close when clicking directly on overlay
  if (event && event.target !== document.getElementById("paperModal")) return;

  document.getElementById("paperModal").classList.add("hidden");
  document.body.style.overflow = "";
}

// Close modal on Escape key
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closePaperModal();
});


// ═══════════════════════════════════════════════════════════════════════════
// 5.  UTILITY FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Highlight occurrences of query words in text.
 * Returns HTML string with <mark> tags.
 */
function highlightSnippet(text, query) {
  if (!query) return escapeHtml(text);
  const escaped = escapeHtml(text);
  const words = query
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .map((w) => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));

  if (!words.length) return escaped;

  const pattern = new RegExp(`(${words.join("|")})`, "gi");
  return escaped.replace(pattern, "<mark>$1</mark>");
}

/** Escape HTML special characters to prevent XSS */
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}


// ═══════════════════════════════════════════════════════════════════════════
// 6.  AI ANSWER HOOK  (placeholder — implement to add AI features)
// ═══════════════════════════════════════════════════════════════════════════

/**
 * generateAnswer(query, chunks)
 * ─────────────────────────────
 * Called with the search query and top retrieved text chunks.
 * Implement this function to integrate an LLM for RAG-style answers.
 *
 * Example implementation (with a local Ollama API):
 *
 *   async function generateAnswer(query, chunks) {
 *     const context = chunks.map(c => c.text).join("\n\n---\n\n");
 *     const prompt  = `Use the following GATE notes to answer the question.\n\n${context}\n\nQ: ${query}\nA:`;
 *     const resp = await fetch("http://localhost:11434/api/generate", {
 *       method:  "POST",
 *       headers: { "Content-Type": "application/json" },
 *       body:    JSON.stringify({ model: "mistral", prompt, stream: false }),
 *     });
 *     const data = await resp.json();
 *     displayAnswer(data.response);
 *   }
 */
// eslint-disable-next-line no-unused-vars
function generateAnswer(query, chunks) {
  // TODO: Implement AI answer generation here.
  console.log("[AI Hook] Query:", query);
  console.log("[AI Hook] Retrieved chunks:", chunks.map((c) => c.title));
}


// ═══════════════════════════════════════════════════════════════════════════
// 7.  BOOT
// ═══════════════════════════════════════════════════════════════════════════

// We wait for MiniSearch to be available (it loads from CDN / local file).
// If it is already available, loadIndex() immediately. Otherwise poll briefly.
(function waitForMiniSearch(attempts) {
  if (typeof MiniSearch !== "undefined") {
    loadIndex();
  } else if (attempts > 0) {
    setTimeout(() => waitForMiniSearch(attempts - 1), 150);
  } else {
    setStatus("⚠️  MiniSearch library not found. Download minisearch.min.js for offline use.", "warn");
  }
})(20);
