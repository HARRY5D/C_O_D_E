const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Adversarial Robustness in Vision Models";

// Color palette: deep navy, electric blue accent, white, slate gray
const C = {
  navy:    "0D1B2A",
  blue:    "1E6FD9",
  accent:  "00C2FF",
  white:   "FFFFFF",
  offWhite:"F0F4F8",
  gray:    "64748B",
  light:   "CBD5E1",
  red:     "E53E3E",
  green:   "38A169",
  yellow:  "ECC94B",
};

// ─── Slide 1: Title ────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  // Big accent rectangle left
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.18, h: 5.625, fill: { color: C.accent }, line: { color: C.accent } });

  // Title
  s.addText("Adversarial Robustness", {
    x: 0.45, y: 0.8, w: 9.1, h: 1.1,
    fontSize: 42, bold: true, color: C.white, fontFace: "Calibri", align: "left",
  });
  s.addText("in Vision Models", {
    x: 0.45, y: 1.75, w: 9.1, h: 0.9,
    fontSize: 38, bold: true, color: C.accent, fontFace: "Calibri", align: "left",
  });

  // Subtitle
  s.addText("Empirical Evaluation of Adversarial Robustness", {
    x: 0.45, y: 2.75, w: 9.1, h: 0.45,
    fontSize: 17, color: C.light, fontFace: "Calibri", align: "left",
  });

  // Authors
  s.addText("Harshil Patel · Harnish Patel · Aayush Patel · Aman Paya", {
    x: 0.45, y: 3.35, w: 9.1, h: 0.35,
    fontSize: 13, color: C.gray, fontFace: "Calibri", align: "left",
  });
  s.addText("Computer Engineering Dept. | CHARUSAT University", {
    x: 0.45, y: 3.75, w: 9.1, h: 0.3,
    fontSize: 12, color: C.gray, fontFace: "Calibri", align: "left",
  });

  // Bottom strip
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.1, w: 10, h: 0.525, fill: { color: "0A1520" }, line: { color: "0A1520" } });
  s.addText("ResNet20  |  SimpleCNN  |  MNIST  |  CIFAR-10  |  7 Attack Types", {
    x: 0.4, y: 5.15, w: 9.2, h: 0.42,
    fontSize: 11, color: C.accent, fontFace: "Calibri", align: "center",
  });
}

// ─── Slide 2: Overview / Contributions ────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.offWhite };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.72, fill: { color: C.navy }, line: { color: C.navy } });
  s.addText("Overview & Contributions", {
    x: 0.4, y: 0.1, w: 9.2, h: 0.52, fontSize: 24, bold: true, color: C.white, fontFace: "Calibri",
  });

  const items = [
    { num: "01", title: "Systematic Evaluation", body: "ResNet20 (CIFAR-10) and SimpleCNN (MNIST) against 7 adversarial attacks — no adversarial training applied." },
    { num: "02", title: "7 Attack Types Compared", body: "Gradient-based · Black-box · Optimization-based · Randomized covering the full adversarial threat landscape." },
    { num: "03", title: "Robustness Curves & ASR", body: "Quantitative analysis of accuracy decay vs. perturbation budget ε and Attack Success Rate across scenarios." },
    { num: "04", title: "Security Implications", body: "Insights for practitioners in healthcare, autonomous systems, and surveillance — >90% accuracy is not enough." },
    { num: "05", title: "Reproducible Benchmark", body: "Open-source pipeline using Foolbox 3.3 & ART libraries for the research community." },
  ];

  items.forEach((it, i) => {
    const col = i < 3 ? 0 : 1;
    const row = i < 3 ? i : i - 3;
    const x = col === 0 ? 0.3 : 5.3;
    const y = 0.95 + row * 1.45;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.6, h: 1.25,
      fill: { color: C.white },
      shadow: { type: "outer", color: "000000", opacity: 0.08, blur: 6, offset: 2, angle: 135 },
      line: { color: C.light, width: 0.5 },
    });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.07, h: 1.25, fill: { color: C.blue }, line: { color: C.blue } });
    s.addText(it.num, { x: x + 0.14, y: y + 0.07, w: 0.5, h: 0.38, fontSize: 18, bold: true, color: C.accent, fontFace: "Calibri" });
    s.addText(it.title, { x: x + 0.14, y: y + 0.38, w: 4.3, h: 0.32, fontSize: 12, bold: true, color: C.navy, fontFace: "Calibri" });
    s.addText(it.body, { x: x + 0.14, y: y + 0.68, w: 4.3, h: 0.52, fontSize: 10, color: C.gray, fontFace: "Calibri" });
  });
}

// ─── Slide 3: Threat Landscape & Models ───────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.offWhite };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.72, fill: { color: C.navy }, line: { color: C.navy } });
  s.addText("Models & Attack Taxonomy", {
    x: 0.4, y: 0.1, w: 9.2, h: 0.52, fontSize: 24, bold: true, color: C.white, fontFace: "Calibri",
  });

  // Left panel – models
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 0.9, w: 4.4, h: 4.4, fill: { color: C.white }, line: { color: C.light, width: 0.5 } });
  s.addText("Vision Models", { x: 0.3, y: 0.9, w: 4.4, h: 0.45, fontSize: 14, bold: true, color: C.white, fontFace: "Calibri", align: "center",
    fill: { color: C.blue } });

  const modelData = [
    ["ResNet20", "CIFAR-10", "20 layers + residual connections", "Clean Acc: 92.5%"],
    ["SimpleCNN", "MNIST", "2 conv stages (32→64 filters)", "Clean Acc: 99.1%"],
  ];
  modelData.forEach((m, i) => {
    const y = 1.5 + i * 1.85;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.55, y, w: 3.9, h: 1.55,
      fill: { color: i === 0 ? "EBF4FF" : "F0FFF4" }, line: { color: i === 0 ? "93C5FD" : "86EFAC", width: 0.8 } });
    s.addText(m[0], { x: 0.65, y: y + 0.08, w: 3.7, h: 0.32, fontSize: 15, bold: true, color: C.navy, fontFace: "Calibri" });
    s.addText(`Dataset: ${m[1]}`, { x: 0.65, y: y + 0.38, w: 3.7, h: 0.25, fontSize: 11, color: C.gray, fontFace: "Calibri" });
    s.addText(m[2], { x: 0.65, y: y + 0.62, w: 3.7, h: 0.25, fontSize: 10, color: C.gray, fontFace: "Calibri" });
    s.addText(m[3], { x: 0.65, y: y + 0.86, w: 3.7, h: 0.35, fontSize: 13, bold: true, color: i === 0 ? C.blue : C.green, fontFace: "Calibri" });
  });

  // Right panel – attack categories
  s.addShape(pres.shapes.RECTANGLE, { x: 5.0, y: 0.9, w: 4.7, h: 4.4, fill: { color: C.white }, line: { color: C.light, width: 0.5 } });
  s.addText("7 Attack Categories", { x: 5.0, y: 0.9, w: 4.7, h: 0.45, fontSize: 14, bold: true, color: C.white, fontFace: "Calibri", align: "center",
    fill: { color: C.navy } });

  const attacks = [
    { cat: "Gradient-Based", color: "C53030", attacks: "FGSM, PGD" },
    { cat: "Black-Box", color: "2C7A7B", attacks: "Boundary, SimBA, Square" },
    { cat: "Optimization", color: "6B46C1", attacks: "Adam-Based Attack" },
    { cat: "Randomized", color: "C05621", attacks: "Random Noise (baseline)" },
  ];
  attacks.forEach((a, i) => {
    const y = 1.45 + i * 0.95;
    s.addShape(pres.shapes.RECTANGLE, { x: 5.2, y, w: 4.3, h: 0.78, fill: { color: C.offWhite }, line: { color: C.light, width: 0.5 } });
    s.addShape(pres.shapes.RECTANGLE, { x: 5.2, y, w: 0.07, h: 0.78, fill: { color: a.color }, line: { color: a.color } });
    s.addText(a.cat, { x: 5.35, y: y + 0.06, w: 4.0, h: 0.28, fontSize: 12, bold: true, color: a.color, fontFace: "Calibri" });
    s.addText(a.attacks, { x: 5.35, y: y + 0.38, w: 4.0, h: 0.28, fontSize: 10, color: C.gray, fontFace: "Calibri" });
  });
}

// ─── Slide 4: Attack Formulations ─────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.72, fill: { color: "0A1520" }, line: { color: "0A1520" } });
  s.addText("Attack Formulations", {
    x: 0.4, y: 0.1, w: 9.2, h: 0.52, fontSize: 24, bold: true, color: C.accent, fontFace: "Calibri",
  });

  const attacks = [
    { name: "FGSM", type: "White-box · Single Step", eq: "x_adv = x + ε · sign(∇ₓ L(θ,x,y))", desc: "Fastest attack. Perturbs in gradient sign direction once. Lower-bound on vulnerability." },
    { name: "PGD", type: "White-box · Iterative", eq: "x^(t+1) = Π_ε(x^t + α · sign(∇ₓ L))", desc: "40-step iterative refinement within ℓ∞ ball. De-facto standard for robustness evaluation." },
    { name: "Boundary", type: "Black-box · Decision-based", eq: "x^(t+1) = x^t + δ_t  (label-only)", desc: "Walks along decision boundary. No gradients needed — just model output labels." },
    { name: "SimBA", type: "Black-box · Query-efficient", eq: "x_adv = x + ε · q_i  (orthogonal)", desc: "Randomly perturbs along DCT basis vectors. Surprisingly effective with 1000 queries." },
    { name: "Square", type: "Black-box · Patch-based", eq: "x_adv = x + ε · M  (sparse mask)", desc: "Applies random square-region perturbations. State-of-the-art black-box efficiency." },
    { name: "Adam", type: "White-box · Optimization", eq: "δ = argmax L(θ, x+δ, y)  via Adam", desc: "Adaptive gradient ascent — achieves 100% ASR on SimpleCNN/MNIST." },
  ];

  attacks.forEach((a, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = col === 0 ? 0.25 : 5.2;
    const y = 0.88 + row * 1.55;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.65, h: 1.35,
      fill: { color: "162030" }, line: { color: C.accent, width: 0.5 },
    });
    s.addText(a.name, { x: x + 0.15, y: y + 0.08, w: 2, h: 0.35, fontSize: 14, bold: true, color: C.accent, fontFace: "Calibri" });
    s.addText(a.type, { x: x + 0.15, y: y + 0.38, w: 4.35, h: 0.22, fontSize: 9, color: C.light, fontFace: "Calibri", italic: true });
    s.addText(a.eq, { x: x + 0.15, y: y + 0.58, w: 4.35, h: 0.3, fontSize: 10, color: C.yellow, fontFace: "Consolas" });
    s.addText(a.desc, { x: x + 0.15, y: y + 0.88, w: 4.35, h: 0.38, fontSize: 9.5, color: C.gray, fontFace: "Calibri" });
  });
}

// ─── Slide 5: ResNet20 on CIFAR-10 Results ────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.offWhite };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.72, fill: { color: C.navy }, line: { color: C.navy } });
  s.addText("ResNet20 on CIFAR-10: Performance Collapse", {
    x: 0.4, y: 0.1, w: 9.2, h: 0.52, fontSize: 22, bold: true, color: C.white, fontFace: "Calibri",
  });

  // Stats callouts
  const stats = [
    { val: "92.5%", label: "Clean Accuracy", color: C.green },
    { val: "4.2%",  label: "PGD at ε=0.05",  color: C.red },
    { val: "88pt",  label: "Accuracy Drop",   color: C.yellow },
    { val: "100%",  label: "Adam ASR",         color: "C53030" },
  ];

  stats.forEach((st, i) => {
    const y = 0.95 + i * 1.1;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 6.45, y, w: 3.2, h: 0.9,
      fill: { color: C.white }, line: { color: C.light, width: 0.5 },
      shadow: { type: "outer", color: "000000", opacity: 0.07, blur: 4, offset: 2, angle: 135 },
    });
    s.addText(st.val, { x: 6.55, y: y + 0.06, w: 3.0, h: 0.44, fontSize: 28, bold: true, color: st.color, fontFace: "Calibri", align: "center" });
    s.addText(st.label, { x: 6.55, y: y + 0.55, w: 3.0, h: 0.28, fontSize: 10, color: C.gray, fontFace: "Calibri", align: "center" });
  });

  // Key insight text
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 0.95, w: 5.8, h: 4.35, fill: { color: C.white }, line: { color: C.light, width: 0.5 } });
  s.addText("Performance Collapse Under Attack", { x: 0.45, y: 1.05, w: 5.5, h: 0.4, fontSize: 14, bold: true, color: C.navy, fontFace: "Calibri" });
  
  const bulletText = [
    "FGSM (ε=0.05): 92.5% → 29.1% (-63.4pt)",
    "PGD (ε=0.05): 92.5% → 4.2% (-88.3pt)",
    "Standard training leaves models catastrophically exposed",
    "Even with minimal perturbation (ε=0.01), accuracy collapses",
  ];

  bulletText.forEach((text, idx) => {
    s.addText("• " + text, { x: 0.6, y: 1.55 + idx * 0.8, w: 5.3, h: 0.65, fontSize: 10, color: C.gray, fontFace: "Calibri" });
  });
}

// ─── Slide 6: SimpleCNN on MNIST – ASR ────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.offWhite };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.72, fill: { color: C.navy }, line: { color: C.navy } });
  s.addText("SimpleCNN on MNIST: All 7 Attacks (ε = 0.1)", {
    x: 0.4, y: 0.1, w: 9.2, h: 0.52, fontSize: 22, bold: true, color: C.white, fontFace: "Calibri",
  });

  // Ranking table
  const rows = [
    [{ text: "Attack", options: { bold: true, color: C.white, fill: { color: C.navy } } },
     { text: "ASR (%)", options: { bold: true, color: C.white, fill: { color: C.navy } } },
     { text: "Tier", options: { bold: true, color: C.white, fill: { color: C.navy } } }],
    ["Adam Attack", "100.0", "Critical"],
    ["PGD",         "95.0",  "Severe"],
    ["Boundary",    "82.1",  "High"],
    ["Square",      "74.8",  "High"],
    ["SimBA",       "71.5",  "High"],
    ["FGSM",        "67.4",  "Moderate"],
    ["Random Noise","30.0",  "Low"],
  ];

  const tierColors = { "Critical": "C53030", "Severe": "C05621", "High": C.blue, "Moderate": C.gray, "Low": C.green };

  const formattedRows = rows.map((row, ri) => {
    if (ri === 0) return row;
    return [
      { text: row[0], options: { color: C.navy } },
      { text: row[1], options: { bold: true, color: tierColors[row[2]] || C.navy } },
      { text: row[2], options: { color: tierColors[row[2]] || C.gray, bold: ri <= 3 } },
    ];
  });

  s.addTable(formattedRows, {
    x: 0.5, y: 0.9, w: 9.0, h: 4.5,
    fontSize: 11, fontFace: "Calibri",
    border: { pt: 0.5, color: C.light },
    rowH: 0.45,
    align: "center",
    colW: [3.5, 2.75, 2.75],
  });

  // Key insight footer
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 5.1, w: 9.4, h: 0.38, fill: { color: "EBF4FF" }, line: { color: "93C5FD", width: 0.5 } });
  s.addText("→  Adam & PGD are the most dangerous attacks (95-100% ASR).  Black-box Boundary attack reaches 82.1% without gradients.  Even random noise baseline (30%) shows structured vulnerability.", {
    x: 0.45, y: 5.14, w: 9.1, h: 0.3, fontSize: 9, color: C.navy, fontFace: "Calibri",
  });
}

// ─── Slide 7: Key Findings ────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.72, fill: { color: "0A1520" }, line: { color: "0A1520" } });
  s.addText("Key Findings", {
    x: 0.4, y: 0.1, w: 9.2, h: 0.52, fontSize: 24, bold: true, color: C.accent, fontFace: "Calibri",
  });

  const findings = [
    {
      icon: "01",
      color: C.red,
      title: "Iterative Attacks Dominate",
      body: "PGD (ε=0.05) collapses ResNet20 from 92.5% → 4.2% — an 88-point drop. Standard training leaves models catastrophically exposed.",
    },
    {
      icon: "02",
      color: "C05621",
      title: "Black-Box Threats Are Real",
      body: "Boundary Attack achieves 82.1% ASR on MNIST without any gradient access. Restricting model APIs is not sufficient protection.",
    },
    {
      icon: "03",
      color: C.yellow,
      title: "Optimization Attacks Saturate",
      body: "Adam-based attack achieves 100% ASR — worst-case white-box scenario. Even 40-step PGD reaches 95% ASR on undefended models.",
    },
    {
      icon: "04",
      color: C.accent,
      title: "Complexity ≠ Robustness",
      body: "Deeper ResNet20 shows similar or worse relative robustness vs. SimpleCNN under normalized attack budgets. Architecture alone is no defense.",
    },
    {
      icon: "05",
      color: C.green,
      title: "Random Noise is the Lower Bound",
      body: "30% ASR for random noise confirms vulnerability is structured, not mere input sensitivity — adversarial attacks are fundamentally optimization problems.",
    },
  ];

  findings.forEach((f, i) => {
    const col = i < 3 ? 0 : 1;
    const row = i < 3 ? i : i - 3;
    const x = col === 0 ? 0.25 : 5.25;
    const y = 0.88 + row * 1.52;
    const h = 1.32;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.7, h,
      fill: { color: "0E1E30" }, line: { color: f.color, width: 1 },
    });
    s.addText(f.icon, { x: x + 0.15, y: y + 0.1, w: 0.45, h: 0.38, fontSize: 18, bold: true, color: f.color, fontFace: "Calibri" });
    s.addText(f.title, { x: x + 0.62, y: y + 0.1, w: 3.9, h: 0.38, fontSize: 12, bold: true, color: C.white, fontFace: "Calibri" });
    s.addText(f.body, { x: x + 0.15, y: y + 0.52, w: 4.45, h: 0.72, fontSize: 10, color: C.light, fontFace: "Calibri" });
  });
}

// ─── Slide 8: Recommendations ─────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.offWhite };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.72, fill: { color: C.navy }, line: { color: C.navy } });
  s.addText("Recommendations for Practitioners", {
    x: 0.4, y: 0.1, w: 9.2, h: 0.52, fontSize: 22, bold: true, color: C.white, fontFace: "Calibri",
  });

  // Three columns
  const recs = [
    {
      num: "I", color: C.red, title: "Mandatory Adversarial Evaluation",
      points: ["Test with ≥3 attack types", "Include white-box & black-box", "Use AutoAttack benchmark", "Set robustness thresholds"],
    },
    {
      num: "II", color: C.yellow, title: "Adopt Adversarial Training",
      points: ["Apply PGD adversarial training", "Consider TRADES method", "Use ensemble training", "Optimize for efficiency"],
    },
    {
      num: "III", color: C.green, title: "Consider Certified Robustness",
      points: ["Randomized smoothing", "Convex defenses", "Provable guarantees", "Trade-off analysis"],
    },
  ];

  recs.forEach((r, i) => {
    const x = 0.3 + i * 3.25;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 0.88, w: 3.05, h: 4.5, fill: { color: C.white }, line: { color: C.light, width: 0.5 } });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 0.88, w: 3.05, h: 0.65, fill: { color: r.color }, line: { color: r.color } });
    s.addText(`Step ${r.num}`, { x, y: 0.88, w: 3.05, h: 0.28, fontSize: 10, color: C.white, fontFace: "Calibri", align: "center", bold: true });
    s.addText(r.title, { x, y: 1.12, w: 3.05, h: 0.38, fontSize: 10, color: C.white, fontFace: "Calibri", align: "center" });
    r.points.forEach((pt, pi) => {
      const py = 1.65 + pi * 0.77;
      s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: py + 0.06, w: 0.2, h: 0.2, fill: { color: r.color }, line: { color: r.color } });
      s.addText(pt, { x: x + 0.48, y: py, w: 2.45, h: 0.65, fontSize: 10, color: C.navy, fontFace: "Calibri" });
    });
  });

  // Future work strip
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.15, w: 10, h: 0.475, fill: { color: C.navy }, line: { color: C.navy } });
  s.addText("Future Work: Defended models · Adaptive attacks · ResNet50 · ViT · ImageNet · MedMNIST", {
    x: 0.4, y: 5.19, w: 9.2, h: 0.38, fontSize: 10, color: C.accent, fontFace: "Calibri", align: "center",
  });
}

// ─── Slide 9: Conclusion ─────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: C.navy };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.18, h: 5.625, fill: { color: C.accent }, line: { color: C.accent } });

  s.addText("Conclusion", {
    x: 0.45, y: 0.45, w: 9.1, h: 0.65, fontSize: 34, bold: true, color: C.accent, fontFace: "Calibri",
  });

  const bullets = [
    "Vision models are far more fragile than high test scores suggest — PGD drives ResNet20 from 92.5% → 4.2%",
    "Black-box attacks prove that API restrictions alone are insufficient — Boundary achieves 82.1% ASR",
    "Optimization-based Adam attack achieves 100% ASR — the worst-case white-box threat with no defense",
    "Model depth and complexity do not imply robustness; architecture is not a substitute for evaluation",
    "Robustness must be treated as a primary criterion for any safety-critical deployment",
  ];

  bullets.forEach((b, i) => {
    const y = 1.25 + i * 0.82;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y: y + 0.05, w: 0.32, h: 0.32, fill: { color: C.accent }, line: { color: C.accent } });
    s.addText((i + 1).toString(), { x: 0.45, y: y + 0.05, w: 0.32, h: 0.32, fontSize: 11, bold: true, color: C.navy, fontFace: "Calibri", align: "center", valign: "middle" });
    s.addText(b, { x: 0.92, y, w: 8.7, h: 0.72, fontSize: 12.5, color: C.light, fontFace: "Calibri" });
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y: 5.1, w: 9.1, h: 0.35, fill: { color: "0A1520" }, line: { color: "0A1520" } });
  s.addText('"Adversarial evaluation must be a primary requirement — not an afterthought — for high-stakes deployment."', {
    x: 0.55, y: 5.1, w: 8.9, h: 0.35, fontSize: 10, color: C.accent, fontFace: "Calibri", italic: true, align: "center",
  });
}

// Write file
pres.writeFile({ fileName: "d:\\JAVA\\CODE\\Crypto_code\\mfa-ppt\\Adversarial_Robustness_Vision_Models.pptx" })
  .then(() => console.log("✓ Presentation generated successfully: Adversarial_Robustness_Vision_Models.pptx"))
  .catch(e => console.error("Error:", e));
