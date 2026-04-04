<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Healthy Cafe Zone — Project README</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --g: #0f2412;
  --g2: #1a3d1e;
  --g3: #2d6a35;
  --g4: #4caf6a;
  --g5: #a8e6b8;
  --g6: #e8f7ec;
  --acc: #f4c542;
  --acc2: #ff7043;
  --txt: #0d1f10;
  --txt2: #3a5c40;
  --txt3: #7a9e82;
  --white: #fff;
  --card: #ffffff;
  --border: #d4ecd9;
  --mono: 'JetBrains Mono', monospace;
  --head: 'Syne', sans-serif;
  --body: 'DM Sans', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  font-family: var(--body);
  background: var(--g6);
  color: var(--txt);
  line-height: 1.7;
  overflow-x: hidden;
}

/* ── HERO ─────────────────────────────────── */
.hero {
  background: var(--g);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 60px 24px;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 70% 50% at 20% 30%, rgba(76,175,106,0.15) 0%, transparent 60%),
    radial-gradient(ellipse 50% 40% at 80% 70%, rgba(244,197,66,0.08) 0%, transparent 60%);
}

.hero-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(76,175,106,0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(76,175,106,0.06) 1px, transparent 1px);
  background-size: 48px 48px;
}

.hero-tag {
  display: inline-block;
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--g4);
  border: 1px solid rgba(76,175,106,0.3);
  padding: 6px 16px;
  border-radius: 100px;
  margin-bottom: 32px;
  position: relative;
  animation: fadeUp 0.6s ease both;
}

.hero h1 {
  font-family: var(--head);
  font-size: clamp(42px, 7vw, 86px);
  font-weight: 800;
  line-height: 1.0;
  color: var(--white);
  position: relative;
  animation: fadeUp 0.6s 0.1s ease both;
  margin-bottom: 8px;
}

.hero h1 span {
  color: var(--g4);
  display: block;
}

.hero-sub {
  font-size: 16px;
  font-weight: 300;
  color: rgba(255,255,255,0.5);
  max-width: 520px;
  margin: 20px auto 44px;
  position: relative;
  animation: fadeUp 0.6s 0.2s ease both;
}

.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  position: relative;
  animation: fadeUp 0.6s 0.3s ease both;
  margin-bottom: 48px;
}

.badge {
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 500;
  padding: 5px 12px;
  border-radius: 6px;
  border: 1px solid;
}
.badge.py  { color: #4fc3f7; border-color: rgba(79,195,247,0.3); background: rgba(79,195,247,0.08); }
.badge.fl  { color: #a5d6a7; border-color: rgba(165,214,167,0.3); background: rgba(165,214,167,0.08); }
.badge.db  { color: #ffcc80; border-color: rgba(255,204,128,0.3); background: rgba(255,204,128,0.08); }
.badge.ml  { color: #f48fb1; border-color: rgba(244,143,177,0.3); background: rgba(244,143,177,0.08); }
.badge.pdf { color: #ce93d8; border-color: rgba(206,147,216,0.3); background: rgba(206,147,216,0.08); }
.badge.sec { color: #80cbc4; border-color: rgba(128,203,196,0.3); background: rgba(128,203,196,0.08); }

.hero-cta {
  display: flex;
  gap: 12px;
  justify-content: center;
  position: relative;
  animation: fadeUp 0.6s 0.4s ease both;
}

.btn-primary {
  font-family: var(--head);
  font-weight: 700;
  font-size: 14px;
  padding: 12px 28px;
  background: var(--g4);
  color: var(--g);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  text-decoration: none;
  transition: transform 0.2s, background 0.2s;
  letter-spacing: 0.3px;
}
.btn-primary:hover { background: var(--g5); transform: translateY(-2px); }

.btn-ghost {
  font-family: var(--head);
  font-weight: 700;
  font-size: 14px;
  padding: 12px 28px;
  background: transparent;
  color: rgba(255,255,255,0.7);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 8px;
  cursor: pointer;
  text-decoration: none;
  transition: border-color 0.2s, color 0.2s, transform 0.2s;
}
.btn-ghost:hover { border-color: rgba(255,255,255,0.4); color: #fff; transform: translateY(-2px); }

/* scroll indicator */
.scroll-hint {
  position: absolute;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  color: rgba(255,255,255,0.2);
  font-size: 11px;
  font-family: var(--mono);
  letter-spacing: 1px;
  animation: fadeUp 1s 0.8s ease both;
}
.scroll-hint::after {
  content: '';
  width: 1px;
  height: 40px;
  background: linear-gradient(to bottom, rgba(76,175,106,0.5), transparent);
  animation: pulse 2s ease-in-out infinite;
}

/* ── SECTIONS ─────────────────────────────── */
.section {
  max-width: 1100px;
  margin: 0 auto;
  padding: 80px 24px;
}

.section-label {
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--g3);
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}
.section-label::before {
  content: '';
  width: 24px;
  height: 1px;
  background: var(--g3);
}

.section-title {
  font-family: var(--head);
  font-size: clamp(28px, 4vw, 44px);
  font-weight: 800;
  color: var(--g);
  line-height: 1.1;
  margin-bottom: 48px;
}

.section-title em {
  font-style: normal;
  color: var(--g3);
}

/* ── FEATURES GRID ──────────────────────────── */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.feat-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 28px;
  transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
  cursor: default;
  position: relative;
  overflow: hidden;
}
.feat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--g3), var(--g4));
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s;
}
.feat-card:hover::before { transform: scaleX(1); }
.feat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 48px rgba(15,36,18,0.12);
  border-color: var(--g5);
}

.feat-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: var(--g6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-bottom: 16px;
}

.feat-card h3 {
  font-family: var(--head);
  font-size: 17px;
  font-weight: 700;
  color: var(--g);
  margin-bottom: 8px;
}

.feat-card p {
  font-size: 14px;
  color: var(--txt2);
  line-height: 1.6;
}

.feat-tag {
  display: inline-block;
  font-family: var(--mono);
  font-size: 10px;
  padding: 3px 8px;
  border-radius: 4px;
  margin-top: 12px;
  background: var(--g6);
  color: var(--g3);
  border: 1px solid var(--border);
}

/* ── ARCHITECTURE ────────────────────────── */
.arch-bg {
  background: var(--g);
  padding: 80px 0;
}

.arch-wrap {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
}

.arch-title {
  font-family: var(--head);
  font-size: clamp(28px, 4vw, 44px);
  font-weight: 800;
  color: var(--white);
  margin-bottom: 8px;
}
.arch-title em { font-style: normal; color: var(--g4); }

.arch-sub {
  color: rgba(255,255,255,0.4);
  font-size: 14px;
  margin-bottom: 48px;
}

.arch-layers {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.arch-layer {
  border-radius: 12px;
  overflow: hidden;
}

.arch-layer-head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  cursor: pointer;
  user-select: none;
  transition: background 0.2s;
}

.arch-layer-head:hover { filter: brightness(1.1); }

.layer-num {
  font-family: var(--mono);
  font-size: 10px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-weight: 500;
}

.arch-layer-head h4 {
  font-family: var(--head);
  font-size: 15px;
  font-weight: 700;
  flex: 1;
}

.arch-layer-head .chevron {
  font-size: 12px;
  transition: transform 0.3s;
  opacity: 0.6;
}
.arch-layer.open .chevron { transform: rotate(180deg); }

.arch-layer-body {
  display: none;
  padding: 0 20px 20px;
}
.arch-layer.open .arch-layer-body { display: block; }

.arch-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.arch-chip {
  font-family: var(--mono);
  font-size: 11px;
  padding: 5px 12px;
  border-radius: 6px;
  border: 1px solid;
  transition: transform 0.15s;
  cursor: default;
}
.arch-chip:hover { transform: scale(1.04); }

/* Layer colors */
.l1 { background: rgba(79,195,247,0.08); }
.l1 .arch-layer-head { background: rgba(79,195,247,0.12); }
.l1 .layer-num { background: rgba(79,195,247,0.2); color: #4fc3f7; }
.l1 .arch-layer-head h4 { color: #4fc3f7; }
.l1 .arch-chip { color: #4fc3f7; border-color: rgba(79,195,247,0.25); background: rgba(79,195,247,0.07); }

.l2 { background: rgba(165,214,167,0.08); }
.l2 .arch-layer-head { background: rgba(165,214,167,0.12); }
.l2 .layer-num { background: rgba(165,214,167,0.2); color: #a5d6a7; }
.l2 .arch-layer-head h4 { color: #a5d6a7; }
.l2 .arch-chip { color: #a5d6a7; border-color: rgba(165,214,167,0.25); background: rgba(165,214,167,0.07); }

.l3 { background: rgba(255,204,128,0.08); }
.l3 .arch-layer-head { background: rgba(255,204,128,0.12); }
.l3 .layer-num { background: rgba(255,204,128,0.2); color: #ffcc80; }
.l3 .arch-layer-head h4 { color: #ffcc80; }
.l3 .arch-chip { color: #ffcc80; border-color: rgba(255,204,128,0.25); background: rgba(255,204,128,0.07); }

.l4 { background: rgba(244,197,66,0.08); }
.l4 .arch-layer-head { background: rgba(244,197,66,0.12); }
.l4 .layer-num { background: rgba(244,197,66,0.2); color: #f4c542; }
.l4 .arch-layer-head h4 { color: #f4c542; }
.l4 .arch-chip { color: #f4c542; border-color: rgba(244,197,66,0.25); background: rgba(244,197,66,0.07); }

.l5 { background: rgba(206,147,216,0.08); }
.l5 .arch-layer-head { background: rgba(206,147,216,0.12); }
.l5 .layer-num { background: rgba(206,147,216,0.2); color: #ce93d8; }
.l5 .arch-layer-head h4 { color: #ce93d8; }
.l5 .arch-chip { color: #ce93d8; border-color: rgba(206,147,216,0.25); background: rgba(206,147,216,0.07); }

/* ── DB SCHEMA ────────────────────────────── */
.schema-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

.schema-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}
.schema-card:hover { transform: translateY(-3px); box-shadow: 0 12px 32px rgba(15,36,18,0.1); }

.schema-head {
  background: var(--g);
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.schema-head .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--g4); }
.schema-head h4 { font-family: var(--mono); font-size: 13px; font-weight: 500; color: var(--g4); }

.schema-fields { padding: 12px 0; }
.schema-field {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 16px;
  font-family: var(--mono);
  font-size: 11.5px;
  transition: background 0.15s;
}
.schema-field:hover { background: var(--g6); }
.field-name { color: var(--txt); font-weight: 500; flex: 1; }
.field-type { color: var(--txt3); font-size: 10px; }
.field-pk {
  font-size: 9px;
  padding: 2px 5px;
  border-radius: 3px;
  background: rgba(244,197,66,0.15);
  color: #b8960a;
  border: 1px solid rgba(244,197,66,0.3);
  font-weight: 500;
}
.field-fk {
  font-size: 9px;
  padding: 2px 5px;
  border-radius: 3px;
  background: rgba(76,175,106,0.12);
  color: var(--g3);
  border: 1px solid rgba(76,175,106,0.2);
  font-weight: 500;
}

/* ── PAYMENT FLOW ──────────────────────────── */
.flow-wrap {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 40px;
  overflow-x: auto;
}

.flow-steps {
  display: flex;
  align-items: stretch;
  gap: 0;
  min-width: 600px;
}

.flow-step {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
  cursor: pointer;
}

.flow-step:not(:last-child)::after {
  content: '→';
  position: absolute;
  right: -12px;
  top: 26px;
  color: var(--txt3);
  font-size: 18px;
  z-index: 1;
}

.flow-circle {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: var(--g6);
  border: 2px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-bottom: 12px;
  transition: background 0.2s, border-color 0.2s, transform 0.2s;
  position: relative;
  z-index: 1;
}

.flow-step:hover .flow-circle,
.flow-step.active .flow-circle {
  background: var(--g);
  border-color: var(--g3);
  transform: scale(1.1);
}

.flow-step h5 {
  font-family: var(--head);
  font-size: 13px;
  font-weight: 700;
  color: var(--g);
  margin-bottom: 4px;
}

.flow-step p {
  font-size: 11px;
  color: var(--txt3);
  line-height: 1.4;
}

.flow-detail {
  margin-top: 24px;
  padding: 20px 24px;
  background: var(--g6);
  border-radius: 12px;
  border-left: 3px solid var(--g3);
  font-size: 13px;
  color: var(--txt2);
  min-height: 60px;
  transition: all 0.3s;
}

/* ── TECH STACK TABLE ────────────────────── */
.stack-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.stack-item {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: transform 0.2s, border-color 0.2s;
}
.stack-item:hover { transform: translateY(-2px); border-color: var(--g4); }

.stack-layer {
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--txt3);
}
.stack-tech {
  font-family: var(--head);
  font-size: 16px;
  font-weight: 700;
  color: var(--g);
}
.stack-version {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--g3);
  background: var(--g6);
  padding: 2px 8px;
  border-radius: 4px;
  display: inline-block;
  width: fit-content;
}

/* ── INSTALL BLOCK ───────────────────────── */
.install-bg {
  background: var(--g);
  padding: 80px 0;
}

.code-block {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(76,175,106,0.15);
  border-radius: 14px;
  overflow: hidden;
  margin-bottom: 20px;
}

.code-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  background: rgba(255,255,255,0.03);
  border-bottom: 1px solid rgba(76,175,106,0.1);
}

.code-dots { display: flex; gap: 6px; }
.code-dots span {
  width: 10px; height: 10px; border-radius: 50%;
}
.code-dots .r { background: #ff5f57; }
.code-dots .y { background: #febc2e; }
.code-dots .g { background: #28c840; }

.code-title {
  font-family: var(--mono);
  font-size: 11px;
  color: rgba(255,255,255,0.3);
}

.copy-btn {
  font-family: var(--mono);
  font-size: 10px;
  padding: 4px 10px;
  background: rgba(76,175,106,0.1);
  color: var(--g4);
  border: 1px solid rgba(76,175,106,0.2);
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}
.copy-btn:hover { background: rgba(76,175,106,0.2); }
.copy-btn.copied { color: var(--acc); border-color: rgba(244,197,66,0.3); }

code {
  display: block;
  padding: 20px 20px;
  font-family: var(--mono);
  font-size: 12.5px;
  line-height: 1.9;
  color: rgba(255,255,255,0.75);
  overflow-x: auto;
  white-space: pre;
}

code .cmt { color: rgba(76,175,106,0.5); }
code .kw  { color: #f4c542; }
code .str { color: #a5d6a7; }
code .num { color: #ce93d8; }

/* ── SECURITY GRID ───────────────────────── */
.security-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
}

.sec-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  gap: 16px;
  align-items: flex-start;
  transition: transform 0.2s;
}
.sec-card:hover { transform: translateY(-2px); }

.sec-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  border-radius: 10px;
  background: var(--g6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.sec-card h4 { font-family: var(--head); font-size: 14px; font-weight: 700; color: var(--g); margin-bottom: 4px; }
.sec-card p { font-size: 13px; color: var(--txt2); line-height: 1.5; }

/* ── FOOTER ──────────────────────────────── */
.footer {
  background: var(--g);
  border-top: 1px solid rgba(76,175,106,0.1);
  padding: 48px 24px;
  text-align: center;
}

.footer-logo {
  font-family: var(--head);
  font-size: 24px;
  font-weight: 800;
  color: var(--g4);
  margin-bottom: 8px;
}

.footer p { font-size: 13px; color: rgba(255,255,255,0.3); margin-bottom: 24px; }

.footer-links {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.footer-link {
  font-family: var(--mono);
  font-size: 11px;
  color: rgba(255,255,255,0.3);
  text-decoration: none;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: color 0.2s;
}
.footer-link:hover { color: var(--g4); }

/* ── DIVIDER ─────────────────────────────── */
.divider {
  border: none;
  height: 1px;
  background: var(--border);
  margin: 0;
}

/* ── ANIMATIONS ──────────────────────────── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
  0%, 100% { opacity: 0.3; }
  50%       { opacity: 1; }
}

.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal.visible { opacity: 1; transform: none; }

/* stagger children */
.reveal-group > * {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.reveal-group.visible > *:nth-child(1) { opacity:1; transform:none; transition-delay:0s; }
.reveal-group.visible > *:nth-child(2) { opacity:1; transform:none; transition-delay:0.07s; }
.reveal-group.visible > *:nth-child(3) { opacity:1; transform:none; transition-delay:0.14s; }
.reveal-group.visible > *:nth-child(4) { opacity:1; transform:none; transition-delay:0.21s; }
.reveal-group.visible > *:nth-child(5) { opacity:1; transform:none; transition-delay:0.28s; }
.reveal-group.visible > *:nth-child(6) { opacity:1; transform:none; transition-delay:0.35s; }
.reveal-group.visible > *:nth-child(7) { opacity:1; transform:none; transition-delay:0.42s; }
.reveal-group.visible > *:nth-child(8) { opacity:1; transform:none; transition-delay:0.49s; }

/* ── NAV ─────────────────────────────────── */
.nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  padding: 14px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(15,36,18,0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(76,175,106,0.1);
  transition: background 0.3s;
}

.nav-logo {
  font-family: var(--head);
  font-size: 16px;
  font-weight: 800;
  color: var(--g4);
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 28px;
  list-style: none;
}

.nav-links a {
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: rgba(255,255,255,0.4);
  text-decoration: none;
  transition: color 0.2s;
}
.nav-links a:hover { color: var(--g4); }

@media (max-width: 640px) {
  .nav-links { display: none; }
}
</style>
</head>
<body>

<!-- NAV -->
<nav class="nav">
  <a href="#" class="nav-logo">🥗 HealthyCafe</a>
  <ul class="nav-links">
    <li><a href="#features">Features</a></li>
    <li><a href="#architecture">Architecture</a></li>
    <li><a href="#database">Database</a></li>
    <li><a href="#install">Install</a></li>
    <li><a href="#stack">Stack</a></li>
  </ul>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-grid"></div>
  <span class="hero-tag">🚀 Full-Stack Cafe Management System</span>
  <h1>Healthy Cafe <span>Zone</span></h1>
  <p class="hero-sub">AI-powered cafeteria management with smart food recommendations, OTP verification, real-time order tracking, and automated invoice generation.</p>
  <div class="badge-row">
    <span class="badge py">Python 3.12</span>
    <span class="badge fl">Flask 2.3.3</span>
    <span class="badge db">MySQL 8.0</span>
    <span class="badge ml">scikit-learn</span>
    <span class="badge pdf">ReportLab</span>
    <span class="badge sec">bcrypt + OTP</span>
  </div>
  <div class="hero-cta">
    <a href="#install" class="btn-primary">Get Started →</a>
    <a href="#features" class="btn-ghost">Explore Features</a>
  </div>
  <div class="scroll-hint">scroll</div>
</section>

<!-- FEATURES -->
<section class="section" id="features">
  <div class="reveal">
    <div class="section-label">What it does</div>
    <h2 class="section-title">Everything a <em>modern cafe</em><br>needs to run</h2>
  </div>
  <div class="features-grid reveal-group">
    <div class="feat-card">
      <div class="feat-icon">🤖</div>
      <h3>AI Food Chatbot</h3>
      <p>Asks for age and weight, calculates BMI, then recommends the best menu items from the live database — completely free, no API cost.</p>
      <span class="feat-tag">scikit-learn + rule engine</span>
    </div>
    <div class="feat-card">
      <div class="feat-icon">🔐</div>
      <h3>OTP Verification</h3>
      <p>Enter mobile number → get OTP → verify → download invoice. Secure 6-digit OTP with 5-minute expiry and single-use enforcement.</p>
      <span class="feat-tag">bcrypt + session auth</span>
    </div>
    <div class="feat-card">
      <div class="feat-icon">📄</div>
      <h3>PDF Invoice Generation</h3>
      <p>Professional invoices auto-generated with cafe logo watermark, itemised bill, GST, loyalty discount, and payment status badge.</p>
      <span class="feat-tag">ReportLab 4.0.4</span>
    </div>
    <div class="feat-card">
      <div class="feat-icon">📊</div>
      <h3>Admin Dashboard</h3>
      <p>Revenue charts, order distribution pie charts, best-selling items, inventory alerts, and live order management — all in one place.</p>
      <span class="feat-tag">Chart.js + Flask APIs</span>
    </div>
    <div class="feat-card">
      <div class="feat-icon">🧬</div>
      <h3>Nutrition Tracking</h3>
      <p>Every menu item has calories, protein, carbs, and fats. Profile page shows cumulative nutrition history with macro pie and bar charts.</p>
      <span class="feat-tag">Chart.js visualization</span>
    </div>
    <div class="feat-card">
      <div class="feat-icon">🪙</div>
      <h3>Health Coins</h3>
      <p>Customers earn 10 health coins per healthy item ordered. Gamification that encourages better food choices and repeat visits.</p>
      <span class="feat-tag">Loyalty system</span>
    </div>
    <div class="feat-card">
      <div class="feat-icon">🛡️</div>
      <h3>Rate Limiting & Security</h3>
      <p>Flask-Limiter prevents brute force attacks. All login attempts logged with IP address. Admin and user sessions fully separated.</p>
      <span class="feat-tag">Flask-Limiter + logs</span>
    </div>
    <div class="feat-card">
      <div class="feat-icon">📦</div>
      <h3>Order Lifecycle</h3>
      <p>Full order tracking from Pending → Preparing → Ready → Delivered. Admin can update statuses, customers see live updates.</p>
      <span class="feat-tag">Real-time status</span>
    </div>
  </div>
</section>

<hr class="divider">

<!-- ARCHITECTURE -->
<section class="arch-bg" id="architecture">
  <div class="arch-wrap">
    <div class="reveal">
      <div class="section-label" style="color:rgba(76,175,106,0.6)">How it's built</div>
      <h2 class="arch-title">System <em>Architecture</em></h2>
      <p class="arch-sub">Click each layer to expand and explore the components</p>
    </div>
    <div class="arch-layers reveal">
      <div class="arch-layer l1 open">
        <div class="arch-layer-head" onclick="toggleLayer(this)">
          <div class="layer-num">1</div>
          <h4>Users</h4>
          <span class="chevron">▼</span>
        </div>
        <div class="arch-layer-body">
          <div class="arch-chips">
            <span class="arch-chip">Customer — Browse, order, pay, track</span>
            <span class="arch-chip">Admin — Manage menu, orders, inventory</span>
          </div>
        </div>
      </div>
      <div class="arch-layer l2 open">
        <div class="arch-layer-head" onclick="toggleLayer(this)">
          <div class="layer-num">2</div>
          <h4>Frontend — HTML / CSS / JavaScript</h4>
          <span class="chevron">▼</span>
        </div>
        <div class="arch-layer-body">
          <div class="arch-chips">
            <span class="arch-chip">cafeteria.html — Menu + AI Chatbot</span>
            <span class="arch-chip">cart.html — Cart management</span>
            <span class="arch-chip">payment.html — OTP + Invoice flow</span>
            <span class="arch-chip">profile.html — Nutrition dashboard</span>
            <span class="arch-chip">orders.html — Order tracking</span>
            <span class="arch-chip">admin/dashboard.html — Analytics</span>
            <span class="arch-chip">admin/menu.html — CRUD items</span>
            <span class="arch-chip">admin/inventory.html — Stock alerts</span>
          </div>
        </div>
      </div>
      <div class="arch-layer l3 open">
        <div class="arch-layer-head" onclick="toggleLayer(this)">
          <div class="layer-num">3</div>
          <h4>Backend — Flask (app.py) REST API</h4>
          <span class="chevron">▼</span>
        </div>
        <div class="arch-layer-body">
          <div class="arch-chips">
            <span class="arch-chip">/register /login — Auth</span>
            <span class="arch-chip">/send-otp /verify-otp — OTP</span>
            <span class="arch-chip">/food-items /menu-items — Menu</span>
            <span class="arch-chip">/create-order /save-order — Orders</span>
            <span class="arch-chip">/generate-invoice — PDF</span>
            <span class="arch-chip">/api/user/profile — Profile</span>
            <span class="arch-chip">/api/user/stats — Nutrition</span>
            <span class="arch-chip">/api/user/recommendations — AI</span>
            <span class="arch-chip">/admin/dashboard — Analytics</span>
            <span class="arch-chip">/admin/orders — Order mgmt</span>
            <span class="arch-chip">/admin/inventory — Stock</span>
            <span class="arch-chip">/admin/security-logs — Audit</span>
          </div>
        </div>
      </div>
      <div class="arch-layer l4 open">
        <div class="arch-layer-head" onclick="toggleLayer(this)">
          <div class="layer-num">4</div>
          <h4>Database — MySQL 8.0</h4>
          <span class="chevron">▼</span>
        </div>
        <div class="arch-layer-body">
          <div class="arch-chips">
            <span class="arch-chip">users — Accounts + health_coins</span>
            <span class="arch-chip">menu_items — Food + macros</span>
            <span class="arch-chip">orders — Payments + status</span>
            <span class="arch-chip">order_items — Line items</span>
            <span class="arch-chip">inventory — Stock + threshold</span>
            <span class="arch-chip">login_otp — OTP + expiry</span>
            <span class="arch-chip">login_history — IP + time</span>
            <span class="arch-chip">system_settings — Config</span>
          </div>
        </div>
      </div>
      <div class="arch-layer l5 open">
        <div class="arch-layer-head" onclick="toggleLayer(this)">
          <div class="layer-num">5</div>
          <h4>External Services & Libraries</h4>
          <span class="chevron">▼</span>
        </div>
        <div class="arch-layer-body">
          <div class="arch-chips">
            <span class="arch-chip">ReportLab — PDF invoice generation</span>
            <span class="arch-chip">scikit-learn — AI food recommendations</span>
            <span class="arch-chip">Fast2SMS — OTP SMS delivery</span>
            <span class="arch-chip">Flask-Limiter — Rate limiting</span>
            <span class="arch-chip">Flask-Mail — Email notifications</span>
            <span class="arch-chip">bcrypt — Password hashing</span>
            <span class="arch-chip">Chart.js — Analytics charts</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- DATABASE -->
<section class="section" id="database">
  <div class="reveal">
    <div class="section-label">Data layer</div>
    <h2 class="section-title">Database <em>Schema</em></h2>
  </div>
  <div class="schema-grid reveal-group">
    <div class="schema-card">
      <div class="schema-head"><div class="dot"></div><h4>users</h4></div>
      <div class="schema-fields">
        <div class="schema-field"><span class="field-name">id</span><span class="field-pk">PK</span><span class="field-type">int</span></div>
        <div class="schema-field"><span class="field-name">name</span><span class="field-type">varchar</span></div>
        <div class="schema-field"><span class="field-name">email</span><span class="field-type">varchar</span></div>
        <div class="schema-field"><span class="field-name">mobile</span><span class="field-type">varchar</span></div>
        <div class="schema-field"><span class="field-name">password_hash</span><span class="field-type">text</span></div>
        <div class="schema-field"><span class="field-name">role</span><span class="field-type">enum</span></div>
        <div class="schema-field"><span class="field-name">health_coins</span><span class="field-type">int</span></div>
      </div>
    </div>
    <div class="schema-card">
      <div class="schema-head"><div class="dot"></div><h4>menu_items</h4></div>
      <div class="schema-fields">
        <div class="schema-field"><span class="field-name">id</span><span class="field-pk">PK</span><span class="field-type">int</span></div>
        <div class="schema-field"><span class="field-name">name</span><span class="field-type">varchar</span></div>
        <div class="schema-field"><span class="field-name">price</span><span class="field-type">decimal</span></div>
        <div class="schema-field"><span class="field-name">calories</span><span class="field-type">int</span></div>
        <div class="schema-field"><span class="field-name">protein</span><span class="field-type">int</span></div>
        <div class="schema-field"><span class="field-name">carbs</span><span class="field-type">int</span></div>
        <div class="schema-field"><span class="field-name">diet_type</span><span class="field-type">varchar</span></div>
      </div>
    </div>
    <div class="schema-card">
      <div class="schema-head"><div class="dot"></div><h4>orders</h4></div>
      <div class="schema-fields">
        <div class="schema-field"><span class="field-name">id</span><span class="field-pk">PK</span><span class="field-type">int</span></div>
        <div class="schema-field"><span class="field-name">user_id</span><span class="field-fk">FK</span><span class="field-type">int</span></div>
        <div class="schema-field"><span class="field-name">total_amount</span><span class="field-type">decimal</span></div>
        <div class="schema-field"><span class="field-name">order_status</span><span class="field-type">varchar</span></div>
        <div class="schema-field"><span class="field-name">payment_status</span><span class="field-type">varchar</span></div>
        <div class="schema-field"><span class="field-name">created_at</span><span class="field-type">timestamp</span></div>
      </div>
    </div>
    <div class="schema-card">
      <div class="schema-head"><div class="dot"></div><h4>order_items</h4></div>
      <div class="schema-fields">
        <div class="schema-field"><span class="field-name">id</span><span class="field-pk">PK</span><span class="field-type">int</span></div>
        <div class="schema-field"><span class="field-name">order_id</span><span class="field-fk">FK</span><span class="field-type">int</span></div>
        <div class="schema-field"><span class="field-name">menu_item_id</span><span class="field-fk">FK</span><span class="field-type">int</span></div>
        <div class="schema-field"><span class="field-name">quantity</span><span class="field-type">int</span></div>
        <div class="schema-field"><span class="field-name">price</span><span class="field-type">decimal</span></div>
      </div>
    </div>
    <div class="schema-card">
      <div class="schema-head"><div class="dot"></div><h4>inventory</h4></div>
      <div class="schema-fields">
        <div class="schema-field"><span class="field-name">id</span><span class="field-pk">PK</span><span class="field-type">int</span></div>
        <div class="schema-field"><span class="field-name">ingredient_name</span><span class="field-type">varchar</span></div>
        <div class="schema-field"><span class="field-name">quantity</span><span class="field-type">int</span></div>
        <div class="schema-field"><span class="field-name">threshold</span><span class="field-type">int</span></div>
      </div>
    </div>
    <div class="schema-card">
      <div class="schema-head"><div class="dot"></div><h4>login_otp</h4></div>
      <div class="schema-fields">
        <div class="schema-field"><span class="field-name">id</span><span class="field-pk">PK</span><span class="field-type">int</span></div>
        <div class="schema-field"><span class="field-name">user_id</span><span class="field-fk">FK</span><span class="field-type">int</span></div>
        <div class="schema-field"><span class="field-name">otp_code</span><span class="field-type">varchar(6)</span></div>
        <div class="schema-field"><span class="field-name">expiry_time</span><span class="field-type">datetime</span></div>
      </div>
    </div>
  </div>
</section>

<hr class="divider">

<!-- PAYMENT FLOW -->
<section class="section">
  <div class="reveal">
    <div class="section-label">Payment system</div>
    <h2 class="section-title">OTP → Invoice <em>Flow</em></h2>
  </div>
  <div class="flow-wrap reveal">
    <div class="flow-steps">
      <div class="flow-step active" onclick="setStep(0)">
        <div class="flow-circle">📱</div>
        <h5>Enter Mobile</h5>
        <p>10-digit number</p>
      </div>
      <div class="flow-step" onclick="setStep(1)">
        <div class="flow-circle">📤</div>
        <h5>Send OTP</h5>
        <p>Server generates</p>
      </div>
      <div class="flow-step" onclick="setStep(2)">
        <div class="flow-circle">🔢</div>
        <h5>Enter OTP</h5>
        <p>6-digit code</p>
      </div>
      <div class="flow-step" onclick="setStep(3)">
        <div class="flow-circle">✅</div>
        <h5>Verify</h5>
        <p>5 min expiry</p>
      </div>
      <div class="flow-step" onclick="setStep(4)">
        <div class="flow-circle">⬇️</div>
        <h5>Download</h5>
        <p>PDF invoice</p>
      </div>
    </div>
    <div class="flow-detail" id="flowDetail">
      Click any step above to learn more about how it works.
    </div>
  </div>
</section>

<!-- INSTALL -->
<section class="install-bg" id="install">
  <div class="arch-wrap">
    <div class="reveal">
      <div class="section-label" style="color:rgba(76,175,106,0.6)">Quick start</div>
      <h2 class="arch-title">Get it <em>Running</em></h2>
    </div>
    <div class="reveal">
      <div class="code-block">
        <div class="code-bar">
          <div class="code-dots"><span class="r"></span><span class="y"></span><span class="g"></span></div>
          <span class="code-title">bash — Installation</span>
          <button class="copy-btn" onclick="copyCode(this,'install-code')">Copy</button>
        </div>
        <code id="install-code"><span class="cmt"># Clone the repository</span>
git clone https://github.com/yourusername/healthy-cafe-management.git
cd healthy-cafe-management

<span class="cmt"># Create virtual environment</span>
python -m venv venv
<span class="kw">source</span> venv/bin/activate        <span class="cmt"># Linux/Mac</span>
venv\Scripts\activate           <span class="cmt"># Windows</span>

<span class="cmt"># Install all dependencies</span>
pip install -r requirements.txt

<span class="cmt"># Set up MySQL database</span>
mysql -u root -p
CREATE DATABASE healthy_cafe;
USE healthy_cafe;

<span class="cmt"># Run the application</span>
python app.py</code>
      </div>

      <div class="code-block">
        <div class="code-bar">
          <div class="code-dots"><span class="r"></span><span class="y"></span><span class="g"></span></div>
          <span class="code-title">.env — Environment variables</span>
          <button class="copy-btn" onclick="copyCode(this,'env-code')">Copy</button>
        </div>
        <code id="env-code">DB_HOST=<span class="str">localhost</span>
DB_USER=<span class="str">root</span>
DB_PASSWORD=<span class="str">your_mysql_password</span>
DB_NAME=<span class="str">healthy_cafe</span>

SECRET_KEY=<span class="str">your_secret_key_here</span>

MAIL_USERNAME=<span class="str">your_email@gmail.com</span>
MAIL_PASSWORD=<span class="str">your_app_password</span></code>
      </div>
    </div>
  </div>
</section>

<!-- TECH STACK -->
<section class="section" id="stack">
  <div class="reveal">
    <div class="section-label">Technologies</div>
    <h2 class="section-title">Full <em>Tech Stack</em></h2>
  </div>
  <div class="stack-grid reveal-group">
    <div class="stack-item"><div class="stack-layer">Language</div><div class="stack-tech">Python</div><div class="stack-version">v3.12</div></div>
    <div class="stack-item"><div class="stack-layer">Web Framework</div><div class="stack-tech">Flask</div><div class="stack-version">v2.3.3</div></div>
    <div class="stack-item"><div class="stack-layer">Database</div><div class="stack-tech">MySQL</div><div class="stack-version">v8.0</div></div>
    <div class="stack-item"><div class="stack-layer">Machine Learning</div><div class="stack-tech">scikit-learn</div><div class="stack-version">v1.3.0</div></div>
    <div class="stack-item"><div class="stack-layer">PDF Generation</div><div class="stack-tech">ReportLab</div><div class="stack-version">v4.0.4</div></div>
    <div class="stack-item"><div class="stack-layer">Authentication</div><div class="stack-tech">bcrypt</div><div class="stack-version">v4.0.1</div></div>
    <div class="stack-item"><div class="stack-layer">Data Processing</div><div class="stack-tech">pandas</div><div class="stack-version">v2.0.3</div></div>
    <div class="stack-item"><div class="stack-layer">Security</div><div class="stack-tech">Flask-Limiter</div><div class="stack-version">v3.5.0</div></div>
    <div class="stack-item"><div class="stack-layer">Frontend Charts</div><div class="stack-tech">Chart.js</div><div class="stack-version">latest</div></div>
  </div>
</section>

<hr class="divider">

<!-- SECURITY -->
<section class="section">
  <div class="reveal">
    <div class="section-label">Protection</div>
    <h2 class="section-title">Security <em>Features</em></h2>
  </div>
  <div class="security-grid reveal-group">
    <div class="sec-card">
      <div class="sec-icon">🔑</div>
      <div><h4>Password Hashing</h4><p>bcrypt with salt rounds — passwords never stored in plain text</p></div>
    </div>
    <div class="sec-card">
      <div class="sec-icon">⏱️</div>
      <div><h4>OTP Expiry</h4><p>6-digit OTPs expire in 5 minutes and are single-use only</p></div>
    </div>
    <div class="sec-card">
      <div class="sec-icon">🚦</div>
      <div><h4>Rate Limiting</h4><p>Flask-Limiter blocks brute force attacks on login and OTP endpoints</p></div>
    </div>
    <div class="sec-card">
      <div class="sec-icon">🗂️</div>
      <div><h4>Login Audit Log</h4><p>All login attempts recorded with timestamp and IP address</p></div>
    </div>
    <div class="sec-card">
      <div class="sec-icon">🔒</div>
      <div><h4>Session Auth</h4><p>Admin and user sessions fully separated with secret key signing</p></div>
    </div>
    <div class="sec-card">
      <div class="sec-icon">🛂</div>
      <div><h4>Password Policy</h4><p>8–12 chars, uppercase, number, and special character required</p></div>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer class="footer">
  <div class="footer-logo">🥗 Healthy Cafe Zone</div>
  <p>Built with Flask · MySQL · scikit-learn · ReportLab<br>Full-stack cafeteria management with AI recommendations</p>
  <div class="footer-links">
    <a href="#features" class="footer-link">Features</a>
    <a href="#architecture" class="footer-link">Architecture</a>
    <a href="#database" class="footer-link">Database</a>
    <a href="#install" class="footer-link">Install</a>
    <a href="#stack" class="footer-link">Stack</a>
  </div>
</footer>

<script>
// ── Scroll reveal ──────────────────────────
const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal, .reveal-group').forEach(el => io.observe(el));

// ── Architecture layer toggle ──────────────
function toggleLayer(head) {
  const layer = head.parentElement;
  layer.classList.toggle('open');
}

// ── Payment flow steps ─────────────────────
const flowDetails = [
  '📱 <strong>Step 1 — Enter Mobile Number:</strong> User selects UPI / Google Pay on the payment page and enters their 10-digit mobile number. Validated client-side before sending to server.',
  '📤 <strong>Step 2 — OTP Generated:</strong> Server creates a random 6-digit OTP, stores it in memory with a 5-minute expiry timestamp keyed to the mobile number. OTP is shown on screen (or sent via SMS if Fast2SMS is configured).',
  '🔢 <strong>Step 3 — Enter OTP:</strong> Beautiful 6-box OTP input UI with auto-focus. Each digit box accepts one number and jumps to the next automatically. Backspace navigates backwards.',
  '✅ <strong>Step 4 — Server Verification:</strong> OTP is checked against the stored value. If expired → error. If wrong → error with clear count cleared. If correct → OTP deleted from store (single-use), session marked as verified.',
  '⬇️ <strong>Step 5 — Download Invoice:</strong> After verification, the server generates a professional PDF invoice using ReportLab with cafe logo watermark, itemised bill, GST calculation, loyalty discount, and PAID badge. User downloads instantly.',
];

function setStep(i) {
  document.querySelectorAll('.flow-step').forEach((s, idx) => {
    s.classList.toggle('active', idx === i);
  });
  document.getElementById('flowDetail').innerHTML = flowDetails[i];
}

// ── Copy code ──────────────────────────────
function copyCode(btn, id) {
  const el = document.getElementById(id);
  const text = el.innerText;
  navigator.clipboard.writeText(text).then(() => {
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
  });
}

// Trigger first flow step
setStep(0);
</script>
</body>
</html>
