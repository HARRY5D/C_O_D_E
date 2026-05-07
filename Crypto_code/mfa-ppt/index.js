const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.title = 'Multi-Factor Authentication (MFA) Attacks & Bypass Techniques';

// Color Palette — Dark cyber/security theme
const C = {
  bg_dark:   "0D1B2A",  // Deep navy (dark slides)
  bg_light:  "F0F4F8",  // Light blue-grey (content slides)
  accent:    "00C2FF",  // Cyan accent
  accent2:   "FF4C4C",  // Red/danger accent
  accent3:   "00E676",  // Green accent
  white:     "FFFFFF",
  dark_text: "1A2535",
  mid_text:  "344A65",
  muted:     "607D8B",
  card_bg:   "FFFFFF",
  card_border:"E3EAF2",
  header_bg: "132338",
};

const makeShadow = () => ({ type: "outer", blur: 8, offset: 2, angle: 135, color: "000000", opacity: 0.12 });

// ─────────────────────────────────────────────
// SLIDE 1 — Title / Introduction
// ─────────────────────────────────────────────
{
  let sl = pres.addSlide();
  sl.background = { color: C.bg_dark };

  // Left side — dark panel with accent
  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.25, h: 5.625, fill: { color: C.accent } });

  // Circuit-board decorative rectangles (top-right corner)
  const deco = [
    { x: 7.8, y: 0.1, w: 2.1, h: 0.08 },
    { x: 9.6, y: 0.1, w: 0.08, h: 1.2 },
    { x: 8.5, y: 0.6, w: 1.4, h: 0.08 },
    { x: 8.5, y: 0.6, w: 0.08, h: 0.9 },
    { x: 7.8, y: 1.2, w: 1.0, h: 0.08 },
  ];
  deco.forEach(d => sl.addShape(pres.shapes.RECTANGLE, { ...d, fill: { color: C.accent, transparency: 60 } }));

  // Tag line
  sl.addText("CYBERSECURITY SEMINAR", {
    x: 0.5, y: 0.35, w: 9, h: 0.4,
    fontSize: 11, color: C.accent, bold: true, charSpacing: 5, align: "left",
  });

  // Main title
  sl.addText("Multi-Factor Authentication", {
    x: 0.5, y: 0.9, w: 9, h: 1.1,
    fontSize: 42, color: C.white, bold: true, align: "left",
  });
  sl.addText("(MFA) Attacks &", {
    x: 0.5, y: 1.85, w: 9, h: 0.9,
    fontSize: 42, color: C.accent, bold: true, align: "left",
  });
  sl.addText("Bypass Techniques", {
    x: 0.5, y: 2.65, w: 9, h: 0.9,
    fontSize: 42, color: C.white, bold: true, align: "left",
  });

  // Separator
  sl.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 3.68, w: 4.5, h: 0.04, fill: { color: C.accent } });

  // Student IDs — 2 column layout
  const col1 = [
    { id: "23DCE101", name: "Jay Prajapati" },
    { id: "23DCE129", name: "Vansh Vyas" },
    { id: "23DCE082", name: "Harshilkumar Patel" },
  ];
  const col2 = [
    { id: "23DCE080", name: "Harnish Patel" },
    { id: "23DCE068", name: "Kevin Meghani" },
  ];

  col1.forEach((s, i) => {
    sl.addText(s.id, { x: 0.5, y: 3.85 + i*0.33, w: 1.8, h: 0.28, fontSize: 10, color: C.accent, bold: true });
    sl.addText(s.name, { x: 2.15, y: 3.85 + i*0.33, w: 2.5, h: 0.28, fontSize: 10, color: C.white });
  });
  col2.forEach((s, i) => {
    sl.addText(s.id, { x: 5.2, y: 3.85 + i*0.33, w: 1.8, h: 0.28, fontSize: 10, color: C.accent, bold: true });
    sl.addText(s.name, { x: 6.9, y: 3.85 + i*0.33, w: 2.5, h: 0.28, fontSize: 10, color: C.white });
  });

  // Institution
  sl.addText("Gujarat Technological University  ·  Computer Engineering  ·  2025–26", {
    x: 0.5, y: 5.15, w: 9, h: 0.3, fontSize: 10, color: C.muted, italic: true, align: "left",
  });
}

// ─────────────────────────────────────────────
// SLIDE 2 — Outline
// ─────────────────────────────────────────────
{
  let sl = pres.addSlide();
  sl.background = { color: C.bg_dark };

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.25, h: 5.625, fill: { color: C.accent } });

  sl.addText("PRESENTATION OUTLINE", {
    x: 0.5, y: 0.3, w: 9, h: 0.45, fontSize: 11, color: C.accent, bold: true, charSpacing: 5,
  });
  sl.addText("What We'll Cover Today", {
    x: 0.5, y: 0.7, w: 9, h: 0.7, fontSize: 30, color: C.white, bold: true,
  });

  // 2 columns of topic cards
  const topics = [
    { num: "01", title: "Introduction to MFA",        presenter: "Jay Prajapati",        id: "23DCE101", col: 0, row: 0 },
    { num: "02", title: "SIM Swapping & SS7 Attacks", presenter: "Jay Prajapati",        id: "23DCE101", col: 0, row: 1 },
    { num: "03", title: "Phishing & AiTM Attacks",    presenter: "Vansh Vyas",           id: "23DCE129", col: 1, row: 0 },
    { num: "04", title: "OTP & Push Bombing",         presenter: "Vansh Vyas",           id: "23DCE129", col: 1, row: 1 },
    { num: "05", title: "Token Hijacking & Replay",   presenter: "Harshilkumar Patel",   id: "23DCE082", col: 0, row: 2 },
    { num: "06", title: "Social Engineering & Deepfakes", presenter: "Harnish Patel",   id: "23DCE080", col: 1, row: 2 },
    { num: "07", title: "Real-World Case Studies",    presenter: "Kevin Meghani",        id: "23DCE068", col: 0, row: 3 },
    { num: "08", title: "Countermeasures & Future",   presenter: "Kevin Meghani",        id: "23DCE068", col: 1, row: 3 },
  ];

  const cardW = 4.4, cardH = 0.78, startX = [0.4, 5.1], startY = 1.6, gapY = 0.9;
  topics.forEach(t => {
    const x = startX[t.col];
    const y = startY + t.row * gapY;
    sl.addShape(pres.shapes.RECTANGLE, { x, y, w: cardW, h: cardH, fill: { color: "132338" }, shadow: makeShadow() });
    sl.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.06, h: cardH, fill: { color: C.accent } });
    sl.addText(t.num, { x: x+0.12, y: y+0.08, w: 0.5, h: 0.3, fontSize: 13, color: C.accent, bold: true });
    sl.addText(t.title, { x: x+0.62, y: y+0.06, w: cardW-0.75, h: 0.36, fontSize: 12, color: C.white, bold: true });
    sl.addText(`${t.id} · ${t.presenter}`, { x: x+0.62, y: y+0.44, w: cardW-0.75, h: 0.24, fontSize: 9.5, color: C.muted });
  });
}

// ─────────────────────────────────────────────
// SLIDE 3 — Introduction to MFA (Jay Prajapati - 23DCE101)
// ─────────────────────────────────────────────
{
  let sl = pres.addSlide();
  sl.background = { color: C.bg_light };

  // Header bar
  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.7, fill: { color: C.bg_dark } });
  sl.addText("Introduction to Multi-Factor Authentication", {
    x: 0.4, y: 0, w: 8, h: 0.7, fontSize: 20, color: C.white, bold: true, valign: "middle",
  });
  sl.addText("23DCE101 · Jay Prajapati", { x: 7.5, y: 0, w: 2.3, h: 0.7, fontSize: 9, color: C.accent, valign: "middle", align: "right" });

  // What is MFA?
  sl.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 0.85, w: 5.8, h: 2.05, fill: { color: C.card_bg }, shadow: makeShadow() });
  sl.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 0.85, w: 0.07, h: 2.05, fill: { color: C.accent } });
  sl.addText("What is MFA?", { x: 0.6, y: 0.9, w: 5.4, h: 0.35, fontSize: 13, color: C.dark_text, bold: true });
  sl.addText([
    { text: "Multi-Factor Authentication (MFA) requires users to provide TWO or more verification factors before granting access. It combines:", options: { breakLine: true } },
    { text: "Knowledge  —  Something you know (password, PIN)", options: { bullet: true, breakLine: true } },
    { text: "Possession  —  Something you have (phone, hardware key)", options: { bullet: true, breakLine: true } },
    { text: "Inherence  —  Something you are (fingerprint, face ID)", options: { bullet: true } },
  ], { x: 0.6, y: 1.3, w: 5.4, h: 1.5, fontSize: 11.5, color: C.dark_text });

  // Stats panel
  sl.addShape(pres.shapes.RECTANGLE, { x: 6.4, y: 0.85, w: 3.2, h: 2.05, fill: { color: C.bg_dark }, shadow: makeShadow() });
  const stats = [
    { val: "99.9%", label: "of account hacks blocked by MFA" },
    { val: "~80%", label: "of breaches involve stolen credentials" },
    { val: "3B+", label: "credentials leaked since 2019" },
  ];
  stats.forEach((s, i) => {
    sl.addText(s.val, { x: 6.5, y: 0.95 + i*0.64, w: 3.0, h: 0.38, fontSize: 20, color: C.accent, bold: true, align: "center" });
    sl.addText(s.label, { x: 6.5, y: 1.3 + i*0.64, w: 3.0, h: 0.22, fontSize: 9, color: C.white, align: "center" });
  });

  // MFA Types row
  sl.addText("Common MFA Methods", { x: 0.4, y: 3.05, w: 9.2, h: 0.3, fontSize: 13, color: C.dark_text, bold: true });
  const methods = [
    { title: "SMS OTP",     desc: "One-time password sent via text message" },
    { title: "TOTP App",    desc: "Time-based OTP via apps like Google Authenticator" },
    { title: "Push Notify", desc: "Approve request via mobile app notification" },
    { title: "Hardware Key",desc: "Physical FIDO2/YubiKey device" },
    { title: "Biometrics",  desc: "Fingerprint, face, or voice recognition" },
  ];
  methods.forEach((m, i) => {
    const bx = 0.4 + i * 1.92;
    sl.addShape(pres.shapes.RECTANGLE, { x: bx, y: 3.42, w: 1.82, h: 1.8, fill: { color: C.card_bg }, shadow: makeShadow() });
    sl.addShape(pres.shapes.RECTANGLE, { x: bx, y: 3.42, w: 1.82, h: 0.32, fill: { color: C.header_bg } });
    sl.addText(m.title, { x: bx+0.05, y: 3.42, w: 1.72, h: 0.32, fontSize: 10, color: C.accent, bold: true, valign: "middle", align: "center" });
    sl.addText(m.desc, { x: bx+0.08, y: 3.8, w: 1.66, h: 1.2, fontSize: 10, color: C.dark_text, align: "center" });
  });

  // Footer
  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.45, w: 10, h: 0.175, fill: { color: C.bg_dark } });
  sl.addText("MFA Attacks & Bypass Techniques", { x: 0.3, y: 5.44, w: 9.4, h: 0.18, fontSize: 8, color: C.muted, valign: "middle" });
  sl.addText("03 / 11", { x: 9.0, y: 5.44, w: 0.8, h: 0.18, fontSize: 8, color: C.muted, valign: "middle", align: "right" });
}

// ─────────────────────────────────────────────
// SLIDE 4 — SIM Swapping & SS7 Attacks (Jay Prajapati)
// ─────────────────────────────────────────────
{
  let sl = pres.addSlide();
  sl.background = { color: C.bg_light };

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.7, fill: { color: C.bg_dark } });
  sl.addText("SIM Swapping & SS7 Protocol Attacks", {
    x: 0.4, y: 0, w: 8, h: 0.7, fontSize: 20, color: C.white, bold: true, valign: "middle",
  });
  sl.addText("23DCE101 · Jay Prajapati", { x: 7.5, y: 0, w: 2.3, h: 0.7, fontSize: 9, color: C.accent, valign: "middle", align: "right" });

  // SIM Swapping section
  sl.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 0.82, w: 4.6, h: 2.3, fill: { color: C.card_bg }, shadow: makeShadow() });
  sl.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 0.82, w: 4.6, h: 0.38, fill: { color: C.accent2 } });
  sl.addText("SIM Swapping Attack", { x: 0.5, y: 0.82, w: 4.4, h: 0.38, fontSize: 13, color: C.white, bold: true, valign: "middle" });
  sl.addText([
    { text: "Attacker gathers victim's personal data via OSINT or phishing", options: { bullet: true, breakLine: true } },
    { text: "Calls carrier posing as victim to transfer SIM to attacker-controlled device", options: { bullet: true, breakLine: true } },
    { text: "All SMS OTPs, calls redirected to attacker's phone", options: { bullet: true, breakLine: true } },
    { text: "Bypasses SMS-based MFA completely", options: { bullet: true, breakLine: true } },
    { text: "High-profile victims: Jack Dorsey, crypto exchanges, celebrities", options: { bullet: true } },
  ], { x: 0.55, y: 1.28, w: 4.3, h: 1.75, fontSize: 11, color: C.dark_text });

  // SS7 section
  sl.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 0.82, w: 4.4, h: 2.3, fill: { color: C.card_bg }, shadow: makeShadow() });
  sl.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 0.82, w: 4.4, h: 0.38, fill: { color: C.mid_text } });
  sl.addText("SS7 Protocol Vulnerability", { x: 5.3, y: 0.82, w: 4.2, h: 0.38, fontSize: 13, color: C.white, bold: true, valign: "middle" });
  sl.addText([
    { text: "SS7 (Signalling System 7) is 1970s-era telecom infrastructure still in use globally", options: { bullet: true, breakLine: true } },
    { text: "Attacker with SS7 access can intercept ANY SMS or voice call", options: { bullet: true, breakLine: true } },
    { text: "Track location of any mobile user worldwide", options: { bullet: true, breakLine: true } },
    { text: "No need to deceive the carrier — works silently at network level", options: { bullet: true, breakLine: true } },
    { text: "Used by nation-state actors, intelligence agencies, criminal groups", options: { bullet: true } },
  ], { x: 5.35, y: 1.28, w: 4.15, h: 1.75, fontSize: 11, color: C.dark_text });

  // Attack flow
  sl.addText("SIM Swap Attack Flow", { x: 0.4, y: 3.25, w: 9.2, h: 0.3, fontSize: 12, color: C.dark_text, bold: true });
  const steps = ["1. Gather\nVictim Info", "2. Contact\nCarrier", "3. SIM\nTransferred", "4. Intercept\nSMS OTP", "5. Account\nCompromised"];
  const colors = [C.muted, C.mid_text, C.accent2, C.accent2, "8B0000"];
  steps.forEach((s, i) => {
    const bx = 0.4 + i * 1.88;
    sl.addShape(pres.shapes.RECTANGLE, { x: bx, y: 3.62, w: 1.72, h: 1.55, fill: { color: colors[i] }, shadow: makeShadow() });
    sl.addText(s, { x: bx+0.06, y: 3.7, w: 1.6, h: 1.38, fontSize: 11, color: C.white, bold: true, align: "center", valign: "middle" });
    if (i < 4) sl.addShape(pres.shapes.RECTANGLE, { x: bx+1.72, y: 4.31, w: 0.16, h: 0.06, fill: { color: C.accent } });
  });

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.45, w: 10, h: 0.175, fill: { color: C.bg_dark } });
  sl.addText("MFA Attacks & Bypass Techniques", { x: 0.3, y: 5.44, w: 9.4, h: 0.18, fontSize: 8, color: C.muted, valign: "middle" });
  sl.addText("04 / 11", { x: 9.0, y: 5.44, w: 0.8, h: 0.18, fontSize: 8, color: C.muted, valign: "middle", align: "right" });
}

// ─────────────────────────────────────────────
// SLIDE 5 — Phishing & AiTM Attacks (Vansh Vyas - 23DCE129)
// ─────────────────────────────────────────────
{
  let sl = pres.addSlide();
  sl.background = { color: C.bg_light };

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.7, fill: { color: C.bg_dark } });
  sl.addText("Phishing & Adversary-in-the-Middle (AiTM) Attacks", {
    x: 0.4, y: 0, w: 8, h: 0.7, fontSize: 18, color: C.white, bold: true, valign: "middle",
  });
  sl.addText("23DCE129 · Vansh Vyas", { x: 7.5, y: 0, w: 2.3, h: 0.7, fontSize: 9, color: C.accent, valign: "middle", align: "right" });

  // AiTM diagram using shapes
  sl.addText("How AiTM (Evilginx2) Works", { x: 0.4, y: 0.78, w: 5.5, h: 0.32, fontSize: 13, color: C.dark_text, bold: true });

  // Boxes
  const boxes = [
    { x: 0.3, y: 1.18, w: 1.5, label: "Victim\nUser", color: C.muted },
    { x: 2.3, y: 1.18, w: 2.0, label: "Attacker\nProxy Server\n(AiTM)", color: C.accent2 },
    { x: 4.9, y: 1.18, w: 1.5, label: "Legit\nLogin Server", color: C.mid_text },
  ];
  boxes.forEach(b => {
    sl.addShape(pres.shapes.RECTANGLE, { x: b.x, y: b.y, w: b.w, h: 1.0, fill: { color: b.color }, shadow: makeShadow() });
    sl.addText(b.label, { x: b.x, y: b.y, w: b.w, h: 1.0, fontSize: 11, color: C.white, bold: true, align: "center", valign: "middle" });
  });
  // Arrows
  sl.addShape(pres.shapes.RECTANGLE, { x: 1.8, y: 1.6, w: 0.5, h: 0.06, fill: { color: C.accent } });
  sl.addShape(pres.shapes.RECTANGLE, { x: 4.3, y: 1.6, w: 0.6, h: 0.06, fill: { color: C.accent } });

  sl.addText("1. Victim enters creds on fake site", { x: 0.3, y: 2.28, w: 2.0, h: 0.3, fontSize: 9.5, color: C.muted, align: "center" });
  sl.addText("2. Proxy relays to real server\n3. Captures session token", { x: 2.3, y: 2.28, w: 2.2, h: 0.4, fontSize: 9.5, color: C.accent2, align: "center" });
  sl.addText("4. Attacker reuses\nstolen token", { x: 4.9, y: 2.28, w: 1.6, h: 0.4, fontSize: 9.5, color: C.muted, align: "center" });

  // Real-world tools + impact
  sl.addShape(pres.shapes.RECTANGLE, { x: 6.5, y: 0.78, w: 3.1, h: 2.2, fill: { color: C.bg_dark }, shadow: makeShadow() });
  sl.addText("Known Tools & Kits", { x: 6.6, y: 0.85, w: 2.9, h: 0.32, fontSize: 12, color: C.accent, bold: true });
  const tools = ["Evilginx2  —  Session hijacking proxy", "Modlishka  —  Reverse proxy phishing", "Muraena  —  Go-based AiTM toolkit", "EvilnoVNC  —  Real-time browser hijack"];
  tools.forEach((t, i) => {
    sl.addText(t, { x: 6.65, y: 1.25 + i*0.35, w: 2.9, h: 0.3, fontSize: 10, color: C.white });
  });

  // Types of phishing
  sl.addText("MFA-Targeting Phishing Variants", { x: 0.4, y: 2.85, w: 9.2, h: 0.3, fontSize: 13, color: C.dark_text, bold: true });
  const variants = [
    { title: "Spear Phishing", desc: "Targeted emails impersonating IT or management to harvest OTPs" },
    { title: "Voice Phishing\n(Vishing)", desc: "Caller impersonates bank/IT, tricks victim into sharing OTP live" },
    { title: "QR Code\nPhishing", desc: "Fake QR redirects user to attacker's proxy — token captured" },
    { title: "Browser-in-\nBrowser", desc: "Fake browser window inside webpage — indistinguishable from real login" },
  ];
  variants.forEach((v, i) => {
    const bx = 0.4 + i * 2.36;
    sl.addShape(pres.shapes.RECTANGLE, { x: bx, y: 3.22, w: 2.2, h: 2.0, fill: { color: C.card_bg }, shadow: makeShadow() });
    sl.addShape(pres.shapes.RECTANGLE, { x: bx, y: 3.22, w: 2.2, h: 0.42, fill: { color: C.header_bg } });
    sl.addText(v.title, { x: bx+0.08, y: 3.22, w: 2.04, h: 0.42, fontSize: 11, color: C.accent, bold: true, valign: "middle", align: "center" });
    sl.addText(v.desc, { x: bx+0.1, y: 3.7, w: 2.0, h: 1.4, fontSize: 10.5, color: C.dark_text });
  });

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.45, w: 10, h: 0.175, fill: { color: C.bg_dark } });
  sl.addText("MFA Attacks & Bypass Techniques", { x: 0.3, y: 5.44, w: 9.4, h: 0.18, fontSize: 8, color: C.muted, valign: "middle" });
  sl.addText("05 / 11", { x: 9.0, y: 5.44, w: 0.8, h: 0.18, fontSize: 8, color: C.muted, valign: "middle", align: "right" });
}

// ─────────────────────────────────────────────
// SLIDE 6 — OTP Bruteforce & MFA Fatigue/Push Bombing (Vansh Vyas)
// ─────────────────────────────────────────────
{
  let sl = pres.addSlide();
  sl.background = { color: C.bg_light };

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.7, fill: { color: C.bg_dark } });
  sl.addText("OTP Bruteforce & MFA Fatigue / Push Bombing", {
    x: 0.4, y: 0, w: 8, h: 0.7, fontSize: 18, color: C.white, bold: true, valign: "middle",
  });
  sl.addText("23DCE129 · Vansh Vyas", { x: 7.5, y: 0, w: 2.3, h: 0.7, fontSize: 9, color: C.accent, valign: "middle", align: "right" });

  // OTP Brute Force
  sl.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 0.82, w: 4.55, h: 2.1, fill: { color: C.card_bg }, shadow: makeShadow() });
  sl.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 0.82, w: 4.55, h: 0.4, fill: { color: C.mid_text } });
  sl.addText("OTP Brute Force & Prediction", { x: 0.5, y: 0.82, w: 4.35, h: 0.4, fontSize: 13, color: C.white, bold: true, valign: "middle" });
  sl.addText([
    { text: "6-digit OTPs have only 1,000,000 combinations — weak to rapid guessing", options: { bullet: true, breakLine: true } },
    { text: "Weak PRNG implementations allow OTP prediction by analyzing seed patterns", options: { bullet: true, breakLine: true } },
    { text: "No rate limiting on some platforms enables automated brute force", options: { bullet: true, breakLine: true } },
    { text: "SMS OTPs often valid 10+ minutes — widens the attack window significantly", options: { bullet: true } },
  ], { x: 0.55, y: 1.3, w: 4.25, h: 1.55, fontSize: 11, color: C.dark_text });

  // MFA Fatigue
  sl.addShape(pres.shapes.RECTANGLE, { x: 5.15, y: 0.82, w: 4.45, h: 2.1, fill: { color: C.card_bg }, shadow: makeShadow() });
  sl.addShape(pres.shapes.RECTANGLE, { x: 5.15, y: 0.82, w: 4.45, h: 0.4, fill: { color: C.accent2 } });
  sl.addText("MFA Fatigue / Push Bombing", { x: 5.25, y: 0.82, w: 4.25, h: 0.4, fontSize: 13, color: C.white, bold: true, valign: "middle" });
  sl.addText([
    { text: "Attacker already has valid username + password (stolen credentials)", options: { bullet: true, breakLine: true } },
    { text: "Sends hundreds of MFA push approvals to victim's phone", options: { bullet: true, breakLine: true } },
    { text: "Victim accepts just to stop the notifications — account compromised", options: { bullet: true, breakLine: true } },
    { text: "Used in Uber (2022) & Cisco breaches — highly effective at scale", options: { bullet: true } },
  ], { x: 5.3, y: 1.3, w: 4.15, h: 1.55, fontSize: 11, color: C.dark_text });

  // Defense vs Attack columns
  sl.addText("OTP Attacks — Mitigation Strategies", { x: 0.4, y: 3.06, w: 9.2, h: 0.32, fontSize: 12, color: C.dark_text, bold: true });

  sl.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 3.44, w: 4.55, h: 1.75, fill: { color: C.bg_dark }, shadow: makeShadow() });
  sl.addText("Attack Indicators", { x: 0.5, y: 3.5, w: 4.35, h: 0.3, fontSize: 11, color: C.accent2, bold: true });
  const indicators = ["Multiple failed OTP attempts in short window", "Push notifications from unusual geo-location", "Auth requests outside business hours", "Excessive push notifications (>5 in 1 min)"];
  indicators.forEach((it, i) => {
    sl.addText("⚠ " + it, { x: 0.55, y: 3.85 + i*0.3, w: 4.2, h: 0.26, fontSize: 10.5, color: "FFC107" });
  });

  sl.addShape(pres.shapes.RECTANGLE, { x: 5.15, y: 3.44, w: 4.45, h: 1.75, fill: { color: "E8F5E9" }, shadow: makeShadow() });
  sl.addText("Mitigations", { x: 5.25, y: 3.5, w: 4.25, h: 0.3, fontSize: 11, color: "2E7D32", bold: true });
  const mits = ["Rate limiting on OTP endpoints", "Number matching in push notifications", "Short OTP validity windows (30–60s)", "FIDO2/Passkeys eliminate OTP entirely"];
  mits.forEach((m, i) => {
    sl.addText("✓ " + m, { x: 5.3, y: 3.85 + i*0.3, w: 4.1, h: 0.26, fontSize: 10.5, color: "2E7D32" });
  });

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.45, w: 10, h: 0.175, fill: { color: C.bg_dark } });
  sl.addText("MFA Attacks & Bypass Techniques", { x: 0.3, y: 5.44, w: 9.4, h: 0.18, fontSize: 8, color: C.muted, valign: "middle" });
  sl.addText("06 / 11", { x: 9.0, y: 5.44, w: 0.8, h: 0.18, fontSize: 8, color: C.muted, valign: "middle", align: "right" });
}

// ─────────────────────────────────────────────
// SLIDE 7 — Token Hijacking & Session Replay (Harshilkumar Patel - 23DCE082)
// ─────────────────────────────────────────────
{
  let sl = pres.addSlide();
  sl.background = { color: C.bg_light };

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.7, fill: { color: C.bg_dark } });
  sl.addText("Token Hijacking, Session Replay & MITM Attacks", {
    x: 0.4, y: 0, w: 8, h: 0.7, fontSize: 18, color: C.white, bold: true, valign: "middle",
  });
  sl.addText("23DCE082 · Harshilkumar Patel", { x: 6.8, y: 0, w: 3.0, h: 0.7, fontSize: 9, color: C.accent, valign: "middle", align: "right" });

  // 3 column cards
  const cards = [
    {
      title: "Session Token Hijacking",
      color: C.accent2,
      points: [
        "After MFA success, server issues a session token (cookie)",
        "Attacker steals this token via XSS, malicious browser extension, or network sniffing",
        "Token reused to access account with NO further MFA prompt",
        "AiTM attacks specifically target post-MFA session tokens",
        "Tools: Cookie-Editor, Burp Suite, BeEF framework",
      ]
    },
    {
      title: "TOTP Replay Attacks",
      color: C.mid_text,
      points: [
        "TOTP codes valid for 30s — but with clock skew allowance up to 90s",
        "Attacker intercepts OTP and reuses within validity window",
        "Real-time phishing pages relay OTP instantly to attacker",
        "Servers failing to mark used tokens allow multiple uses",
        "Solution: Single-use OTP enforcement at server side",
      ]
    },
    {
      title: "MITM & SSL Stripping",
      color: C.header_bg,
      points: [
        "Attacker positions between user and authentication server",
        "SSL stripping downgrades HTTPS to HTTP, exposing credentials",
        "Can capture 2FA codes in transit on unsecured networks",
        "Open Wi-Fi hotspots prime target for MITM interception",
        "HSTS + HPKP headers mitigate SSL stripping effectively",
      ]
    }
  ];

  cards.forEach((card, i) => {
    const bx = 0.3 + i * 3.22;
    sl.addShape(pres.shapes.RECTANGLE, { x: bx, y: 0.82, w: 3.1, h: 4.52, fill: { color: C.card_bg }, shadow: makeShadow() });
    sl.addShape(pres.shapes.RECTANGLE, { x: bx, y: 0.82, w: 3.1, h: 0.5, fill: { color: card.color } });
    sl.addText(card.title, { x: bx+0.1, y: 0.82, w: 2.9, h: 0.5, fontSize: 12, color: C.white, bold: true, valign: "middle", align: "center" });
    card.points.forEach((pt, j) => {
      sl.addText(pt, { x: bx+0.15, y: 1.42 + j*0.75, w: 2.8, h: 0.68, fontSize: 10.5, color: C.dark_text,
        bullet: true });
    });
  });

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.45, w: 10, h: 0.175, fill: { color: C.bg_dark } });
  sl.addText("MFA Attacks & Bypass Techniques", { x: 0.3, y: 5.44, w: 9.4, h: 0.18, fontSize: 8, color: C.muted, valign: "middle" });
  sl.addText("07 / 11", { x: 9.0, y: 5.44, w: 0.8, h: 0.18, fontSize: 8, color: C.muted, valign: "middle", align: "right" });
}

// ─────────────────────────────────────────────
// SLIDE 8 — Social Engineering & Deepfake Attacks (Harnish Patel - 23DCE080)
// ─────────────────────────────────────────────
{
  let sl = pres.addSlide();
  sl.background = { color: C.bg_light };

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.7, fill: { color: C.bg_dark } });
  sl.addText("Social Engineering, Deepfakes & Biometric Spoofing", {
    x: 0.4, y: 0, w: 8, h: 0.7, fontSize: 17, color: C.white, bold: true, valign: "middle",
  });
  sl.addText("23DCE080 · Harnish Patel", { x: 7.5, y: 0, w: 2.3, h: 0.7, fontSize: 9, color: C.accent, valign: "middle", align: "right" });

  // Social Engineering panel
  sl.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 0.82, w: 5.6, h: 2.15, fill: { color: C.card_bg }, shadow: makeShadow() });
  sl.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 0.82, w: 0.07, h: 2.15, fill: { color: C.accent } });
  sl.addText("Social Engineering — Human as the Weakest Link", { x: 0.58, y: 0.87, w: 5.3, h: 0.32, fontSize: 12, color: C.dark_text, bold: true });
  sl.addText([
    { text: "Tech Support Scam: Attacker poses as IT staff, requests victim read OTP aloud for 'verification'", options: { bullet: true, breakLine: true } },
    { text: "Pretexting: Elaborate false scenario built to earn trust before requesting MFA codes", options: { bullet: true, breakLine: true } },
    { text: "Insider Threats: Corrupt employee with physical access bypasses MFA entirely", options: { bullet: true, breakLine: true } },
    { text: "Recovery Abuse: Exploit backup codes or account recovery to bypass MFA altogether", options: { bullet: true } },
  ], { x: 0.58, y: 1.26, w: 5.3, h: 1.65, fontSize: 11, color: C.dark_text });

  // Deepfake panel
  sl.addShape(pres.shapes.RECTANGLE, { x: 6.2, y: 0.82, w: 3.4, h: 2.15, fill: { color: C.bg_dark }, shadow: makeShadow() });
  sl.addText("AI Deepfakes vs Biometrics", { x: 6.3, y: 0.88, w: 3.2, h: 0.3, fontSize: 12, color: C.accent, bold: true });
  const dfPoints = [
    "Face-swap videos bypass facial recognition MFA",
    "AI voice cloning defeats voice-print authentication",
    "Printed 2D photos can fool iris scanners",
    "Deepfake video calls impersonate executives for wire transfers",
  ];
  dfPoints.forEach((p, i) => {
    sl.addText(p, { x: 6.35, y: 1.25 + i*0.38, w: 3.1, h: 0.34, fontSize: 10, color: C.white, bullet: true });
  });

  // Known real-world social engineering cases
  sl.addText("Real-World Social Engineering MFA Bypasses", { x: 0.4, y: 3.1, w: 9.2, h: 0.3, fontSize: 12, color: C.dark_text, bold: true });
  const cases = [
    { org: "Twilio (2022)", desc: "SMS phishing of employees → MFA bypass → 125 customer orgs compromised" },
    { org: "Cloudflare (2022)", desc: "Same campaign hit Cloudflare — stopped by FIDO2 hardware keys" },
    { org: "LastPass (2022)", desc: "Deepfake audio of CEO used in vishing attempt on employee" },
    { org: "MGM/Caesars (2023)", desc: "10-min phone call social-engineered IT helpdesk, reset MFA, extorted $15M" },
  ];
  cases.forEach((c, i) => {
    const bx = 0.4 + (i%2) * 4.75;
    const by = 3.5 + Math.floor(i/2) * 0.98;
    sl.addShape(pres.shapes.RECTANGLE, { x: bx, y: by, w: 4.5, h: 0.85, fill: { color: C.card_bg }, shadow: makeShadow() });
    sl.addShape(pres.shapes.RECTANGLE, { x: bx, y: by, w: 0.06, h: 0.85, fill: { color: C.accent2 } });
    sl.addText(c.org, { x: bx+0.15, y: by+0.07, w: 4.2, h: 0.28, fontSize: 11, color: C.accent2, bold: true });
    sl.addText(c.desc, { x: bx+0.15, y: by+0.38, w: 4.2, h: 0.42, fontSize: 10, color: C.dark_text });
  });

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.45, w: 10, h: 0.175, fill: { color: C.bg_dark } });
  sl.addText("MFA Attacks & Bypass Techniques", { x: 0.3, y: 5.44, w: 9.4, h: 0.18, fontSize: 8, color: C.muted, valign: "middle" });
  sl.addText("08 / 11", { x: 9.0, y: 5.44, w: 0.8, h: 0.18, fontSize: 8, color: C.muted, valign: "middle", align: "right" });
}

// ─────────────────────────────────────────────
// SLIDE 9 — Real-World Case Studies (Kevin Meghani - 23DCE068)
// ─────────────────────────────────────────────
{
  let sl = pres.addSlide();
  sl.background = { color: C.bg_light };

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.7, fill: { color: C.bg_dark } });
  sl.addText("Real-World MFA Bypass Case Studies", {
    x: 0.4, y: 0, w: 8, h: 0.7, fontSize: 20, color: C.white, bold: true, valign: "middle",
  });
  sl.addText("23DCE068 · Kevin Meghani", { x: 7.5, y: 0, w: 2.3, h: 0.7, fontSize: 9, color: C.accent, valign: "middle", align: "right" });

  // 2x3 case study grid
  const caseStudies = [
    { title: "Uber Data Breach (2022)", tag: "MFA Fatigue",     color: C.accent2,
      detail: "Attacker purchased credentials from dark web. Sent MFA push notifications until contractor approved. Attacker gained access to internal Slack, AWS, and HackerOne. Posted 'I am a hacker' on Slack. Full internal compromise via one MFA approval." },
    { title: "Microsoft / GitHub (2022)", tag: "OAuth Token Theft", color: C.mid_text,
      detail: "Lapsus$ group stole OAuth tokens from developer accounts. Bypassed MFA by hijacking authenticated sessions. Accessed Microsoft source code repositories. Demonstrated that post-authentication tokens are as valuable as passwords." },
    { title: "Crypto.com (2022)", tag: "2FA Bypass",         color: "7B1FA2",
      detail: "$34M stolen from 483 user accounts. MFA bypass mechanism undisclosed but confirmed. Exchange initially denied then confirmed breach. Reimbursed all affected users. Highlighted custodial wallet MFA vulnerabilities." },
    { title: "Twilio & Okta (2022)", tag: "Supply Chain + SE",  color: "E65100",
      detail: "Group-IB dubbed the campaign '0ktapus'. 169 organizations compromised via Twilio access. Okta breach gave attackers access to customer systems. Phishing pages harvested MFA codes in real time. 9,931 credentials stolen." },
    { title: "Cisco (2022)", tag: "Vishing + MFA Push",  color: "1565C0",
      detail: "Employee's personal Google account credentials stolen. Attacker used vishing + MFA push bombing. Ultimately got employee to accept push after repeated calls. Ransomware group Yanluowang claimed access. Cisco confirmed but denied data theft." },
    { title: "Microsoft 365 / MSTIC (2022)", tag: "AiTM Phishing",  color: "2E7D32",
      detail: "Microsoft identified large-scale AiTM phishing campaign targeting 10,000+ organizations. Used proxy-based phishing to steal session cookies post-MFA. Attacker signed into Microsoft 365 using stolen cookies. Demonstrated MFA is NOT foolproof against AiTM." },
  ];

  caseStudies.forEach((cs, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const bx = 0.35 + col * 4.9;
    const by = 0.85 + row * 1.6;
    sl.addShape(pres.shapes.RECTANGLE, { x: bx, y: by, w: 4.6, h: 1.5, fill: { color: C.card_bg }, shadow: makeShadow() });
    sl.addShape(pres.shapes.RECTANGLE, { x: bx, y: by, w: 4.6, h: 0.38, fill: { color: cs.color } });
    sl.addText(cs.title, { x: bx+0.12, y: by, w: 3.0, h: 0.38, fontSize: 11.5, color: C.white, bold: true, valign: "middle" });
    sl.addShape(pres.shapes.RECTANGLE, { x: bx+3.2, y: by+0.07, w: 1.2, h: 0.24, fill: { color: "FFFFFF", transparency: 30 } });
    sl.addText(cs.tag, { x: bx+3.2, y: by+0.07, w: 1.2, h: 0.24, fontSize: 8, color: C.white, bold: true, align: "center", valign: "middle" });
    sl.addText(cs.detail, { x: bx+0.12, y: by+0.44, w: 4.35, h: 1.0, fontSize: 9.5, color: C.dark_text });
  });

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.45, w: 10, h: 0.175, fill: { color: C.bg_dark } });
  sl.addText("MFA Attacks & Bypass Techniques", { x: 0.3, y: 5.44, w: 9.4, h: 0.18, fontSize: 8, color: C.muted, valign: "middle" });
  sl.addText("09 / 11", { x: 9.0, y: 5.44, w: 0.8, h: 0.18, fontSize: 8, color: C.muted, valign: "middle", align: "right" });
}

// ─────────────────────────────────────────────
// SLIDE 10 — Countermeasures & Mitigation (Harshilkumar & Kevin)
// ─────────────────────────────────────────────
{
  let sl = pres.addSlide();
  sl.background = { color: C.bg_light };

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.7, fill: { color: C.bg_dark } });
  sl.addText("Countermeasures & Hardening Against MFA Attacks", {
    x: 0.4, y: 0, w: 8.5, h: 0.7, fontSize: 18, color: C.white, bold: true, valign: "middle",
  });

  // 4 quadrant layout
  const quads = [
    {
      title: "Phishing-Resistant MFA",
      color: "1565C0",
      items: [
        "FIDO2/WebAuthn hardware security keys (YubiKey)",
        "Passkeys — cryptographic, device-bound, phishing-proof",
        "Certificate-based authentication (smartcard/PIV)",
        "Binding MFA to origin URL prevents AiTM relay",
      ]
    },
    {
      title: "OTP & Push Hardening",
      color: "2E7D32",
      items: [
        "Number matching — user must type code shown in app",
        "Additional context (geo, device) in push notification",
        "Rate limiting & CAPTCHA on authentication endpoints",
        "Short token TTL with single-use enforcement",
      ]
    },
    {
      title: "Network & Session Security",
      color: "6A1B9A",
      items: [
        "Enforce HTTPS + HSTS to prevent SSL stripping",
        "Invalidate sessions on IP/device change",
        "Token binding ties session to TLS connection",
        "Short session lifetimes + re-authentication policies",
      ]
    },
    {
      title: "Organizational Controls",
      color: "BF360C",
      items: [
        "Security awareness training for social engineering",
        "Zero-trust architecture — verify every access request",
        "Privileged Access Workstations (PAW) for admins",
        "Dark web monitoring for leaked credentials",
      ]
    },
  ];

  quads.forEach((q, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const bx = 0.35 + col * 4.9;
    const by = 0.85 + row * 2.3;
    sl.addShape(pres.shapes.RECTANGLE, { x: bx, y: by, w: 4.6, h: 2.2, fill: { color: C.card_bg }, shadow: makeShadow() });
    sl.addShape(pres.shapes.RECTANGLE, { x: bx, y: by, w: 0.08, h: 2.2, fill: { color: q.color } });
    sl.addText(q.title, { x: bx+0.18, y: by+0.1, w: 4.3, h: 0.32, fontSize: 13, color: q.color, bold: true });
    sl.addText(q.items.map(it => ({ text: it, options: { bullet: true, breakLine: true } })),
      { x: bx+0.18, y: by+0.48, w: 4.28, h: 1.65, fontSize: 10.5, color: C.dark_text });
  });

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.45, w: 10, h: 0.175, fill: { color: C.bg_dark } });
  sl.addText("MFA Attacks & Bypass Techniques", { x: 0.3, y: 5.44, w: 9.4, h: 0.18, fontSize: 8, color: C.muted, valign: "middle" });
  sl.addText("10 / 11", { x: 9.0, y: 5.44, w: 0.8, h: 0.18, fontSize: 8, color: C.muted, valign: "middle", align: "right" });
}

// ─────────────────────────────────────────────
// SLIDE 11 — Conclusion, Future Scope & References
// ─────────────────────────────────────────────
{
  let sl = pres.addSlide();
  sl.background = { color: C.bg_dark };

  sl.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.25, h: 5.625, fill: { color: C.accent } });

  sl.addText("CONCLUSION & FUTURE SCOPE", {
    x: 0.5, y: 0.25, w: 9, h: 0.38, fontSize: 11, color: C.accent, bold: true, charSpacing: 5,
  });
  sl.addText("What We Learned & What Lies Ahead", {
    x: 0.5, y: 0.58, w: 9, h: 0.55, fontSize: 24, color: C.white, bold: true,
  });

  // Key takeaways
  sl.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.2, w: 5.65, h: 2.75, fill: { color: "132338" }, shadow: makeShadow() });
  sl.addText("Key Takeaways", { x: 0.55, y: 1.28, w: 5.35, h: 0.3, fontSize: 12, color: C.accent, bold: true });
  const takeaways = [
    "No MFA is unbreakable — attack surface depends on the factor type",
    "SMS/OTP-based MFA is significantly weaker than FIDO2/Passkeys",
    "Human factors (social engineering, fatigue) remain the biggest vector",
    "AiTM & session hijacking bypass MFA at the protocol level",
    "Phishing-resistant MFA (hardware keys, passkeys) is the gold standard",
    "Defense-in-depth: combine MFA with zero-trust, monitoring, training",
  ];
  takeaways.forEach((t, i) => {
    sl.addText(t, { x: 0.55, y: 1.64 + i*0.3, w: 5.35, h: 0.26, fontSize: 10.5, color: C.white, bullet: true });
  });

  // Future scope
  sl.addShape(pres.shapes.RECTANGLE, { x: 6.25, y: 1.2, w: 3.35, h: 2.75, fill: { color: "132338" }, shadow: makeShadow() });
  sl.addText("Future Scope", { x: 6.38, y: 1.28, w: 3.1, h: 0.3, fontSize: 12, color: C.accent3, bold: true });
  const future = [
    "Passkey & FIDO2 mainstream adoption",
    "AI-driven adaptive authentication",
    "Behavioral biometrics as continuous MFA",
    "Post-quantum cryptography for auth tokens",
    "Decentralized identity (DID/W3C standards)",
    "Real-time deepfake liveness detection",
  ];
  future.forEach((f, i) => {
    sl.addText(f, { x: 6.38, y: 1.64 + i*0.3, w: 3.1, h: 0.26, fontSize: 10.5, color: C.white, bullet: true });
  });

  // References
  sl.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 4.08, w: 9.2, h: 1.3, fill: { color: "0D1422" } });
  sl.addText("References", { x: 0.55, y: 4.13, w: 9.0, h: 0.28, fontSize: 10, color: C.accent, bold: true });
  const refs = [
    "[1] Microsoft Security Blog — AiTM Phishing at Scale (2022). microsoft.com/security",
    "[2] CISA — Implementing Phishing-Resistant MFA (2022). cisa.gov",
    "[3] NIST SP 800-63B — Digital Identity Guidelines. nvlpubs.nist.gov",
    "[4] Mandiant / Google — MFA Bypass Techniques in the Wild (2023). mandiant.com",
    "[5] Evilginx2 Documentation — kgretzky.com/evilginx   [6] Uber Incident Report (2022). uber.com/newsroom",
  ];
  refs.forEach((r, i) => {
    sl.addText(r, { x: 0.55, y: 4.46 + i*0.24, w: 9.0, h: 0.22, fontSize: 8.5, color: C.muted });
  });

  // Team footer
  sl.addText("Jay Prajapati  ·  Vansh Vyas  ·  Harshilkumar Patel  ·  Harnish Patel  ·  Kevin Meghani  |  GTU — 2025–26", {
    x: 0.5, y: 5.42, w: 9.2, h: 0.18, fontSize: 8, color: C.muted, align: "center",
  });
}

// ─────────────────────────────────────────────
// Write file
// ─────────────────────────────────────────────
pres.writeFile({ fileName: "MFA_Attacks_Bypass_Techniques.pptx" })
  .then(() => console.log("Done!"))
  .catch(e => console.error("Error:", e));