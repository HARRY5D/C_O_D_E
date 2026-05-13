/**
 * test.js — GATE Mock Test Engine
 * Loads questions.json → builds test → manages state → scores → shows results
 */

'use strict';

/* ═══════════════════════════ State ══════════════════════════════ */
let ALL_QUESTIONS = [];       // full bank from questions.json
let SUBJECTS      = [];       // unique subjects present in bank

let testQuestions = [];       // selected subset for current test
let currentIdx    = 0;        // 0-based index of displayed question

// Per-question state  key = question.id
const answers   = {};         // { id: ['A'] or ['A','C'] }
const visited   = new Set();  // all opened question ids
const answered  = new Set();  // ids with a saved answer
const marked    = new Set();  // marked-for-review ids

// Timer
let timerInterval = null;
let timerSeconds  = 0;        // remaining seconds (0 = no timer)

/* ═══════════════════════════ Boot ═══════════════════════════════ */
(async function init() {
  try {
    const resp = await fetch('questions.json');
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    const data = await resp.json();
    ALL_QUESTIONS = data.questions || [];
    populateSetup(data);
  } catch (e) {
    document.getElementById('availText').textContent =
      '⚠ Could not load questions.json — make sure you ran parse_questions.py';
    console.error(e);
  }
})();

/* ═══════════════════════════ Setup Screen ═══════════════════════ */
function populateSetup(data) {
  // Subject selector
  SUBJECTS = Object.keys(data.bySubject || {}).sort();
  const sel = document.getElementById('subjectSelect');
  SUBJECTS.forEach(s => {
    const opt = document.createElement('option');
    opt.value = s;
    opt.textContent = `${s}  (${data.bySubject[s]})`;
    sel.appendChild(opt);
  });

  // Pre-select subject from URL param (?subject=Algorithms)
  const urlSubject = new URLSearchParams(location.search).get('subject');
  if (urlSubject) {
    const found = [...sel.options].find(o => o.value === urlSubject);
    if (found) sel.value = urlSubject;
  }

  // Count buttons → update availability text on change
  document.getElementById('subjectSelect').addEventListener('change', updateAvailability);
  document.getElementById('customCount').addEventListener('input', updateAvailability);
  document.querySelectorAll('input[name="qtype"]').forEach(r => r.addEventListener('change', updateAvailability));
  document.querySelectorAll('.count-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.count-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('customCount').value = '';
      updateAvailability();
    });
  });

  updateAvailability();
}

function getSetupValues() {
  const subject = document.getElementById('subjectSelect').value;

  // Selected count: custom input takes priority over count-btn
  const custom = parseInt(document.getElementById('customCount').value, 10);
  const active = document.querySelector('.count-btn.active');
  const count  = (!isNaN(custom) && custom > 0) ? custom
               : (active ? parseInt(active.dataset.n, 10) : 30);

  const qtype  = document.querySelector('input[name="qtype"]:checked').value;
  const timer  = document.querySelector('input[name="timer"]:checked').value;
  return { subject, count, qtype, timer };
}

function updateAvailability() {
  const { subject, count, qtype } = getSetupValues();
  const pool = filterPool(subject, qtype);
  const avail = pool.length;
  const actual = Math.min(count, avail);
  const bar  = document.getElementById('availText');
  bar.textContent = `${avail} questions available · test will use ${actual}`;
  document.getElementById('startTestBtn').disabled = avail === 0;
}

function filterPool(subject, qtype) {
  return ALL_QUESTIONS.filter(q => {
    const subMatch  = (subject === 'all') || q.label === subject;
    const typeMatch = (qtype   === 'all') || q.type  === qtype;
    return subMatch && typeMatch;
  });
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

/* ═══════════════════════════ Start Test ════════════════════════ */
function startTest() {
  const { subject, count, qtype, timer } = getSetupValues();
  const pool = filterPool(subject, qtype);
  testQuestions = shuffle([...pool]).slice(0, count);

  if (testQuestions.length === 0) { alert('No questions matched your filter.'); return; }

  // Clear state
  Object.keys(answers).forEach(k => delete answers[k]);
  visited.clear(); answered.clear(); marked.clear();
  currentIdx = 0;

  // Build palette
  buildPalette();

  // Timer
  if (timer === 'none') {
    timerSeconds = 0;
    document.getElementById('timerBox').style.display = 'none';
  } else {
    const mins = timer === 'auto'
      ? testQuestions.reduce((s, q) => s + (q.type === 'msq' ? 2.5 : 2), 0)
      : parseInt(timer, 10);
    timerSeconds = Math.round(mins * 60);
    document.getElementById('timerBox').style.display = 'flex';
    startTimer();
  }

  showScreen('examScreen');
  renderQuestion(0);
  updateExamHeader();
}

/* ═══════════════════════════ Timer ═════════════════════════════ */
function startTimer() {
  clearInterval(timerInterval);
  updateTimerDisplay();
  timerInterval = setInterval(() => {
    timerSeconds--;
    updateTimerDisplay();
    if (timerSeconds <= 0) { clearInterval(timerInterval); submitTest(); }
  }, 1000);
}

function updateTimerDisplay() {
  const h = Math.floor(timerSeconds / 3600);
  const m = Math.floor((timerSeconds % 3600) / 60);
  const s = timerSeconds % 60;
  const fmt = n => String(n).padStart(2, '0');
  document.getElementById('timerDigits').textContent = `${fmt(h)} : ${fmt(m)} : ${fmt(s)}`;
  const box = document.getElementById('timerBox');
  box.classList.toggle('timer-warning', timerSeconds <= 300 && timerSeconds > 60);
  box.classList.toggle('timer-danger',  timerSeconds <= 60);
}

/* ═══════════════════════════ Render Question ═══════════════════ */
function renderQuestion(idx) {
  currentIdx = idx;
  const q = testQuestions[idx];
  if (!q) return;

  visited.add(q.id);
  updatePalette();
  updateExamHeader();

  // Meta bar
  document.getElementById('qNumberTag').textContent  = `Q.${idx + 1}`;
  document.getElementById('qTypeTag').textContent    = q.type.toUpperCase();
  document.getElementById('qMarksTag').textContent   =
    q.marks + ' Mark' + (q.marks > 1 ? 's' : '') +
    (q.type === 'mcq' ? ` (Penalty: ${q.penalty})` : ' (No Penalty)');

  // Question text
  document.getElementById('qText').innerHTML = formatText(q.text);

  // Options
  const optDiv = document.getElementById('qOptions');
  optDiv.innerHTML = '';

  if (!q.options || Object.keys(q.options).length === 0) {
    optDiv.innerHTML = '<p class="no-opts">No options recorded for this question.</p>';
  } else {
    const userAns = answers[q.id] || [];
    ['A','B','C','D'].forEach(letter => {
      if (!q.options[letter]) return;
      const li = document.createElement('label');
      li.className = 'option-item' + (userAns.includes(letter) ? ' selected' : '');
      li.dataset.letter = letter;

      const inp = document.createElement('input');
      inp.type  = q.type === 'mcq' ? 'radio' : 'checkbox';
      inp.name  = 'option';
      inp.value = letter;
      inp.checked = userAns.includes(letter);

      inp.addEventListener('change', () => handleOptionChange(q, letter));

      const badge = document.createElement('span');
      badge.className = 'option-badge';
      badge.textContent = letter;

      const text = document.createElement('span');
      text.className = 'option-text';
      text.innerHTML = formatText(q.options[letter]);

      li.appendChild(inp);
      li.appendChild(badge);
      li.appendChild(text);
      optDiv.appendChild(li);

      // Click anywhere on label syncs checkbox/radio
      li.addEventListener('click', e => {
        if (e.target === inp) return; // already handled
      });
    });
  }

  // Prev button
  document.getElementById('btnPrev').disabled = idx === 0;
  document.getElementById('examSection').textContent = q.label || q.subject;
}

function handleOptionChange(q, letter) {
  if (q.type === 'mcq') {
    answers[q.id] = [letter];
  } else {
    const cur = answers[q.id] || [];
    if (cur.includes(letter)) {
      answers[q.id] = cur.filter(l => l !== letter);
    } else {
      answers[q.id] = [...cur, letter];
    }
  }
  // Auto-highlight selected options
  document.querySelectorAll('.option-item').forEach(li => {
    const inp = li.querySelector('input');
    li.classList.toggle('selected', inp.checked);
  });
}

function formatText(t) {
  if (!t) return '';
  // Preserve line breaks and basic LaTeX-like monospace
  return t
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br>');
}

/* ═══════════════════════════ Navigation ════════════════════════ */
function saveAndNext() {
  const q = testQuestions[currentIdx];
  if (q && answers[q.id] && answers[q.id].length > 0) {
    answered.add(q.id);
    marked.delete(q.id); // saving clears pending mark
  }
  if (currentIdx < testQuestions.length - 1) renderQuestion(currentIdx + 1);
  updatePalette();
}

function goToPrev() {
  if (currentIdx > 0) renderQuestion(currentIdx - 1);
}

function markForReview() {
  const q = testQuestions[currentIdx];
  if (!q) return;
  marked.add(q.id);
  if (answers[q.id] && answers[q.id].length > 0) answered.add(q.id);
  updatePalette();
  if (currentIdx < testQuestions.length - 1) renderQuestion(currentIdx + 1);
}

function clearResponse() {
  const q = testQuestions[currentIdx];
  if (!q) return;
  delete answers[q.id];
  answered.delete(q.id);
  document.querySelectorAll('.option-item input').forEach(i => i.checked = false);
  document.querySelectorAll('.option-item').forEach(li => li.classList.remove('selected'));
  updatePalette();
}

/* ═══════════════════════════ Palette ═══════════════════════════ */
function buildPalette() {
  const grid = document.getElementById('paletteGrid');
  grid.innerHTML = '';
  testQuestions.forEach((q, idx) => {
    const btn = document.createElement('button');
    btn.className = 'pal-circle not-visited';
    btn.textContent = idx + 1;
    btn.id = `palBtn_${q.id}`;
    btn.onclick = () => renderQuestion(idx);
    grid.appendChild(btn);
  });
}

function getPaletteState(q) {
  const isVisited = visited.has(q.id);
  const isAnswered = answered.has(q.id) || (answers[q.id] && answers[q.id].length > 0);
  const isMarked   = marked.has(q.id);

  if (!isVisited)            return 'not-visited';
  if (isAnswered && isMarked) return 'answered-marked';
  if (isMarked)               return 'marked';
  if (isAnswered)             return 'answered';
  return 'not-answered';
}

function updatePalette() {
  testQuestions.forEach(q => {
    const btn = document.getElementById(`palBtn_${q.id}`);
    if (!btn) return;
    btn.className = 'pal-circle ' + getPaletteState(q);
    if (testQuestions[currentIdx]?.id === q.id) btn.classList.add('current');
  });

  // Stats row
  let notVisited=0, notAnswered=0, ans=0, mrk=0, ansMrk=0;
  testQuestions.forEach(q => {
    const s = getPaletteState(q);
    if (s === 'not-visited')     notVisited++;
    else if (s === 'not-answered') notAnswered++;
    else if (s === 'answered')     ans++;
    else if (s === 'marked')       mrk++;
    else if (s === 'answered-marked') ansMrk++;
  });
  document.getElementById('paletteStats').innerHTML =
    `<span class="stat-chip nv">${notVisited} Not Visited</span>` +
    `<span class="stat-chip na">${notAnswered} Not Answered</span>` +
    `<span class="stat-chip an">${ans} Answered</span>` +
    `<span class="stat-chip mk">${mrk} Marked</span>`;
}

function updateExamHeader() {
  const total = testQuestions.length;
  document.getElementById('examCounter').textContent = `Q ${currentIdx+1} / ${total}`;
}

/* ═══════════════════════════ Submit ════════════════════════════ */
function confirmSubmit() {
  const total     = testQuestions.length;
  const attCount  = testQuestions.reduce((s, q) =>
    s + (answers[q.id] && answers[q.id].length > 0 ? 1 : 0), 0);
  const notAns    = total - attCount;

  document.getElementById('submitSummary').innerHTML =
    `<div class="submit-row"><span>Total Questions</span><strong>${total}</strong></div>` +
    `<div class="submit-row"><span>Attempted</span><strong>${attCount}</strong></div>` +
    `<div class="submit-row warn"><span>Not Attempted</span><strong>${notAns}</strong></div>`;

  document.getElementById('submitModal').classList.remove('hidden');
}

function closeSubmitModal(e) {
  if (!e || e.target === document.getElementById('submitModal'))
    document.getElementById('submitModal').classList.add('hidden');
}

function submitTest() {
  clearInterval(timerInterval);
  document.getElementById('submitModal').classList.add('hidden');
  buildResults();
  showScreen('resultsScreen');
}

/* ═══════════════════════════ Scoring ═══════════════════════════ */
function arraysEqual(a, b) {
  if (!a || !b) return false;
  const sa = [...a].sort(), sb = [...b].sort();
  return sa.length === sb.length && sa.every((v, i) => v === sb[i]);
}

function scoreQuestion(q) {
  const userAns = answers[q.id] || [];
  if (userAns.length === 0) return { status: 'unattempted', score: 0 };
  const correct = arraysEqual(userAns, q.answer);
  if (correct) return { status: 'correct', score: q.marks };
  // MSQ: no penalty; MCQ: penalty
  const pen = q.type === 'mcq' ? -parseFloat(q.penalty || 0) : 0;
  return { status: 'wrong', score: pen };
}

/* ═══════════════════════════ Results ═══════════════════════════ */
function buildResults() {
  let totalScore = 0, maxScore = 0;
  let correct=0, wrong=0, unattempted=0;
  const subjectMap = {}; // subject → {score, max, correct, wrong, total}

  testQuestions.forEach(q => {
    const { status, score } = scoreQuestion(q);
    totalScore += score;
    maxScore   += q.marks;
    if (status === 'correct')     correct++;
    else if (status === 'wrong')  wrong++;
    else                          unattempted++;

    if (!subjectMap[q.subject]) subjectMap[q.subject] = { score:0, max:0, correct:0, wrong:0, total:0 };
    subjectMap[q.subject].score   += score;
    subjectMap[q.subject].max     += q.marks;
    subjectMap[q.subject].total   += 1;
    if (status === 'correct') subjectMap[q.subject].correct++;
    if (status === 'wrong')   subjectMap[q.subject].wrong++;
  });

  const pct = maxScore > 0 ? ((totalScore / maxScore) * 100).toFixed(1) : 0;

  /* Score card */
  document.getElementById('scoreCard').innerHTML = `
    <div class="score-main">
      <div class="score-circle ${pct >= 60 ? 'pass' : 'fail'}">
        <div class="score-num">${totalScore.toFixed(2)}</div>
        <div class="score-denom">/ ${maxScore}</div>
      </div>
      <div class="score-meta">
        <h2 class="score-title">${pct >= 60 ? '🎉 Good Work!' : '📖 Keep Practising'}</h2>
        <p class="score-pct">${pct}% accuracy</p>
        <div class="score-stats">
          <div class="score-stat correct">${correct} Correct</div>
          <div class="score-stat wrong">${wrong} Wrong</div>
          <div class="score-stat unattempted">${unattempted} Skipped</div>
          <div class="score-stat total">${testQuestions.length} Total</div>
        </div>
      </div>
    </div>`;

  /* Subject breakdown */
  const rows = Object.entries(subjectMap).map(([sub, d]) =>
    `<tr>
       <td>${sub}</td>
       <td>${d.total}</td>
       <td class="correct-cell">${d.correct}</td>
       <td class="wrong-cell">${d.wrong}</td>
       <td>${(d.total - d.correct - d.wrong)}</td>
       <td><strong>${d.score.toFixed(2)} / ${d.max}</strong></td>
     </tr>`).join('');

  document.getElementById('subjectBreakdown').innerHTML = `
    <table class="breakdown-table">
      <thead><tr>
        <th>Subject</th><th>Total</th><th>Correct</th><th>Wrong</th><th>Skipped</th><th>Score</th>
      </tr></thead>
      <tbody>${rows}</tbody>
    </table>`;
}

function showReview() {
  const panel = document.getElementById('reviewPanel');
  panel.classList.toggle('hidden');
  if (panel.classList.contains('hidden')) return;

  const list = document.getElementById('reviewList');
  list.innerHTML = '';

  testQuestions.forEach((q, idx) => {
    const userAns = answers[q.id] || [];
    const { status } = scoreQuestion(q);
    const statusClass = status === 'correct' ? 'review-correct'
                      : status === 'wrong'   ? 'review-wrong'
                      :                        'review-skip';
    const statusLabel = status === 'correct' ? '✓ Correct'
                      : status === 'wrong'   ? '✗ Wrong'
                      :                        '— Skipped';

    const optsHtml = ['A','B','C','D'].map(l => {
      if (!q.options[l]) return '';
      const isCorrect = q.answer.includes(l);
      const isUser    = userAns.includes(l);
      let cls = 'rv-opt';
      if (isCorrect) cls += ' rv-correct';
      if (isUser && !isCorrect) cls += ' rv-wrong-pick';
      return `<div class="${cls}">
        <span class="rv-badge">${l}</span>
        <span>${formatText(q.options[l])}</span>
        ${isCorrect ? '<span class="rv-tick">✓</span>' : ''}
        ${isUser && !isCorrect ? '<span class="rv-cross">✗</span>' : ''}
      </div>`;
    }).join('');

    list.innerHTML += `
      <div class="review-card ${statusClass}">
        <div class="rv-header">
          <span class="rv-qnum">Q.${idx+1}</span>
          <span class="rv-subject">${q.subject}</span>
          <span class="rv-type">${q.type.toUpperCase()}</span>
          <span class="rv-status">${statusLabel}</span>
        </div>
        <div class="rv-text">${formatText(q.text)}</div>
        <div class="rv-opts">${optsHtml}</div>
        <div class="rv-footer">
          Your answer: <strong>${userAns.length ? userAns.join(', ') : 'Not attempted'}</strong>
          &nbsp;|&nbsp;
          Correct answer: <strong>${q.answer.join(', ')}</strong>
        </div>
      </div>`;
  });
}

/* ═══════════════════════════ Utility ═══════════════════════════ */
function showScreen(screenId) {
  ['setupScreen','examScreen','resultsScreen'].forEach(id => {
    document.getElementById(id).classList.toggle('hidden', id !== screenId);
  });
}
