"""
build_phase10_part2.py
======================
Phase 10 Part 2 Builder — AI Freelancer OS Digital Publishing Studio
Author: OMAR SUNNY
Creates:
  - START-HERE-LAUNCHPAD.html (studio root + 15-DEPLOY-AND-FUNNEL-BRIDGE/)
  - 15-DEPLOY-AND-FUNNEL-BRIDGE/funnel-links-config.json
  - 15-DEPLOY-AND-FUNNEL-BRIDGE/inject_funnel_links.py
  - 15-DEPLOY-AND-FUNNEL-BRIDGE/web-live-demo/index.html
  - 15-DEPLOY-AND-FUNNEL-BRIDGE/web-live-demo/app.html
"""

import os
import json
import sys
import io

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

STUDIO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUNNEL_DIR = os.path.join(STUDIO_ROOT, "15-DEPLOY-AND-FUNNEL-BRIDGE")
DEMO_DIR = os.path.join(FUNNEL_DIR, "web-live-demo")

print(f"Studio root: {STUDIO_ROOT}")
print(f"Funnel dir : {FUNNEL_DIR}")
print(f"Demo dir   : {DEMO_DIR}")

os.makedirs(FUNNEL_DIR, exist_ok=True)
os.makedirs(DEMO_DIR, exist_ok=True)

created_files = []

# ─────────────────────────────────────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────────────────────────────────────
def write(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    size = os.path.getsize(path)
    created_files.append((path, size))
    print(f"  ✅ Written: {os.path.relpath(path, STUDIO_ROOT)}  ({size:,} bytes)")


# ─────────────────────────────────────────────────────────────────────────────
# TASK A — START-HERE-LAUNCHPAD.html
# ─────────────────────────────────────────────────────────────────────────────

LAUNCHPAD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>🚀 Start Here — AI Freelancer Operating System</title>
<style>
  /* ── Reset & Base ────────────────────────────────────────────────────── */
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg:        #0B1120;
    --surface:   #0F1A2E;
    --surface2:  #162035;
    --border:    #1E3050;
    --teal:      #0D9488;
    --teal-lt:   #14B8A6;
    --cyan:      #38BDF8;
    --cyan-lt:   #7DD3FC;
    --gold:      #F59E0B;
    --gold-lt:   #FCD34D;
    --white:     #F0F4FF;
    --muted:     #94A3B8;
    --danger:    #EF4444;
    --success:   #22C55E;
    --font-mono: "JetBrains Mono", Consolas, "Courier New", monospace;
    --font-sans: Inter, "Segoe UI", Arial, sans-serif;
    --radius:    8px;
  }
  html { scroll-behavior: smooth; }
  body {
    background: var(--bg);
    color: var(--white);
    font-family: var(--font-sans);
    line-height: 1.6;
    min-height: 100vh;
  }

  /* ── Layout ──────────────────────────────────────────────────────────── */
  .container { max-width: 960px; margin: 0 auto; padding: 0 24px; }

  /* ── Nav Bar ─────────────────────────────────────────────────────────── */
  nav {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 12px 0;
    position: sticky; top: 0; z-index: 100;
  }
  nav .inner {
    display: flex; align-items: center; justify-content: space-between;
    max-width: 960px; margin: 0 auto; padding: 0 24px;
  }
  .nav-brand {
    font-family: var(--font-mono);
    font-size: 0.85rem; color: var(--cyan); letter-spacing: 0.05em;
  }
  .tier-badge {
    font-family: var(--font-mono); font-size: 0.75rem;
    padding: 4px 12px; border-radius: 20px;
    background: var(--teal); color: #fff;
    transition: background 0.3s;
  }
  .tier-badge.t0 { background: #475569; }
  .tier-badge.t1 { background: #6366F1; }
  .tier-badge.t2 { background: var(--teal); }
  .tier-badge.t3 { background: linear-gradient(90deg, #D97706, #F59E0B); color: #000; }

  /* ── Hero / Section 1 ────────────────────────────────────────────────── */
  #hero {
    padding: 64px 0 40px;
    text-align: center;
    background: radial-gradient(ellipse 80% 60% at 50% -20%, #0D9488 0%, transparent 60%),
                var(--bg);
  }
  .hero-title {
    font-family: var(--font-mono);
    font-size: clamp(1.6rem, 4vw, 2.8rem);
    font-weight: 700;
    color: var(--white);
    letter-spacing: -0.02em;
    margin-bottom: 12px;
  }
  .hero-title span { color: var(--cyan); }
  .hero-sub {
    font-size: 1rem; color: var(--muted);
    margin-bottom: 40px;
  }

  /* ── Quick-Start Tracker ─────────────────────────────────────────────── */
  .tracker {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px 32px;
    max-width: 600px; margin: 0 auto;
    text-align: left;
  }
  .tracker h3 {
    font-family: var(--font-mono);
    font-size: 0.85rem; color: var(--cyan);
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 16px;
  }
  .tracker-step {
    display: flex; align-items: flex-start; gap: 12px;
    margin-bottom: 12px; cursor: pointer;
  }
  .tracker-step input[type="checkbox"] {
    width: 18px; height: 18px; flex-shrink: 0;
    accent-color: var(--teal); margin-top: 2px; cursor: pointer;
  }
  .tracker-step label {
    font-size: 0.9rem; cursor: pointer;
    transition: color 0.2s;
  }
  .tracker-step input:checked + label { color: var(--teal-lt); text-decoration: line-through; }
  .tracker-progress {
    margin-top: 16px;
    height: 6px; background: var(--border); border-radius: 3px; overflow: hidden;
  }
  .tracker-progress-bar {
    height: 100%; width: 0%; background: var(--teal);
    border-radius: 3px; transition: width 0.4s ease;
  }

  /* ── Section titles ──────────────────────────────────────────────────── */
  .section { padding: 48px 0; }
  .section-title {
    font-family: var(--font-mono);
    font-size: 0.75rem; color: var(--teal);
    letter-spacing: 0.12em; text-transform: uppercase;
    margin-bottom: 8px;
  }
  .section-heading {
    font-size: clamp(1.3rem, 2.5vw, 1.8rem);
    font-weight: 700; color: var(--white);
    margin-bottom: 28px;
  }
  hr.section-rule {
    border: none; border-top: 1px solid var(--border);
    margin: 0 0 48px;
  }

  /* ── Action Buttons / Section 2 ──────────────────────────────────────── */
  .actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }
  .action-btn {
    display: flex; align-items: center; gap: 12px;
    padding: 16px 20px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--white);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    transition: border-color 0.2s, background 0.2s, transform 0.15s;
  }
  .action-btn:hover {
    border-color: var(--cyan);
    background: var(--surface2);
    transform: translateY(-2px);
  }
  .action-btn .btn-icon { font-size: 1.4rem; flex-shrink: 0; }
  .action-btn .btn-label { flex: 1; }
  .action-btn .btn-label small { display: block; color: var(--muted); font-size: 0.75rem; font-weight: 400; }
  .action-btn.locked {
    opacity: 0.55; cursor: not-allowed; pointer-events: none;
    border-style: dashed;
  }
  .action-btn.locked .btn-label small { color: var(--danger); }
  .action-btn.primary { border-color: var(--teal); }
  .action-btn.primary:hover { border-color: var(--teal-lt); }

  /* ── Value Ladder Table / Section 3 ─────────────────────────────────── */
  .table-wrap { overflow-x: auto; margin-bottom: 32px; }
  table {
    width: 100%; border-collapse: collapse;
    font-size: 0.85rem;
  }
  thead th {
    background: var(--surface);
    color: var(--muted);
    font-family: var(--font-mono);
    font-size: 0.75rem; letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 10px 14px;
    border-bottom: 2px solid var(--border);
    text-align: center;
    white-space: nowrap;
  }
  thead th:first-child { text-align: left; }
  thead th.col-star {
    background: linear-gradient(180deg, #1A2A10, #0F1A0A);
    color: var(--gold);
  }
  tbody td {
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
    text-align: center;
    vertical-align: middle;
  }
  tbody td:first-child {
    text-align: left; color: var(--white); font-weight: 500;
  }
  tbody tr:hover td { background: var(--surface2); }
  tbody tr:nth-child(even) td { background: rgba(15,26,46,0.4); }
  .check  { color: var(--success); font-size: 1.1rem; }
  .cross  { color: var(--danger);  font-size: 1.1rem; }
  .partial { color: var(--gold);   font-size: 0.85rem; }

  /* ── CTA Cards ───────────────────────────────────────────────────────── */
  .cta-row { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 28px; }
  .cta-btn {
    display: inline-flex; align-items: center; gap: 10px;
    padding: 16px 28px; border-radius: var(--radius);
    font-weight: 700; font-size: 1rem;
    text-decoration: none; cursor: pointer;
    transition: transform 0.15s, filter 0.15s;
  }
  .cta-btn:hover { transform: translateY(-2px); filter: brightness(1.1); }
  .cta-gold {
    background: linear-gradient(90deg, #D97706, #F59E0B);
    color: #000;
  }
  .cta-diamond {
    background: linear-gradient(90deg, #6366F1, #38BDF8);
    color: #fff;
  }

  /* ── Section 4 — License ─────────────────────────────────────────────── */
  .license-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px 28px;
    max-width: 480px;
  }
  .license-box h3 {
    font-family: var(--font-mono);
    font-size: 0.8rem; color: var(--cyan);
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 12px;
  }
  .license-row { display: flex; gap: 10px; }
  .license-input {
    flex: 1;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--white);
    font-family: var(--font-mono);
    font-size: 0.85rem;
    padding: 10px 14px;
    outline: none;
    transition: border-color 0.2s;
  }
  .license-input:focus { border-color: var(--cyan); }
  .license-btn {
    background: var(--teal);
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 0.9rem;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.2s;
  }
  .license-btn:hover { background: var(--teal-lt); }
  .license-msg {
    margin-top: 10px; font-size: 0.85rem;
    min-height: 20px;
  }
  .license-msg.ok  { color: var(--success); }
  .license-msg.err { color: var(--danger); }

  /* ── Footer ──────────────────────────────────────────────────────────── */
  footer {
    background: var(--surface);
    border-top: 1px solid var(--border);
    text-align: center;
    padding: 24px;
    font-size: 0.8rem;
    color: var(--muted);
    font-family: var(--font-mono);
  }
  footer a { color: var(--cyan); text-decoration: none; }
  footer a:hover { text-decoration: underline; }

  /* ── Hidden utility ──────────────────────────────────────────────────── */
  .hidden { display: none !important; }
</style>
</head>
<body>

<!-- ── Navigation ──────────────────────────────────────────────────────── -->
<nav>
  <div class="inner">
    <span class="nav-brand">⚡ AI FREELANCER OS — LAUNCHPAD</span>
    <span class="tier-badge t0" id="tierBadge">Tier 0 — Free</span>
  </div>
</nav>

<!-- ═══════════════════════════════════════════════════════════════════════
     SECTION 1 — Welcome Header & Quick-Start Tracker
═══════════════════════════════════════════════════════════════════════ -->
<section id="hero">
  <div class="container">
    <h1 class="hero-title">🚀 THE <span>AI FREELANCER</span> OPERATING SYSTEM</h1>
    <p class="hero-sub">By <strong style="color:#F0F4FF">OMAR SUNNY</strong> — Your 5-Gate Client Lifecycle Command Center</p>

    <div class="tracker">
      <h3>⚡ 3-Step Quick-Start Progress Tracker</h3>

      <div class="tracker-step">
        <input type="checkbox" id="step1" />
        <label for="step1">Step 1: Run your 7-Day EHR Leak Audit (Module 1)</label>
      </div>
      <div class="tracker-step">
        <input type="checkbox" id="step2" />
        <label for="step2">Step 2: Copy your first AI Prompt into Claude / ChatGPT</label>
      </div>
      <div class="tracker-step">
        <input type="checkbox" id="step3" />
        <label for="step3">Step 3: Import the Free Notion Starter Database</label>
      </div>

      <div class="tracker-progress">
        <div class="tracker-progress-bar" id="progressBar"></div>
      </div>
    </div>
  </div>
</section>

<!-- ═══════════════════════════════════════════════════════════════════════
     SECTION 2 — 1-Click Action Buttons
═══════════════════════════════════════════════════════════════════════ -->
<hr class="section-rule" />
<section class="section" id="actions">
  <div class="container">
    <p class="section-title">// QUICK ACCESS</p>
    <h2 class="section-heading">1-Click Action Hub</h2>

    <div class="actions-grid">

      <!-- Always visible -->
      <a class="action-btn primary"
         href="../07-INTERACTIVE-TOOLS/freelancer-os-app.html"
         id="btnApp">
        <span class="btn-icon">🚀</span>
        <span class="btn-label">
          Launch Interactive Web App
          <small>All 4 Modules (tier-gated)</small>
        </span>
      </a>

      <!-- Tier 0+ -->
      <a class="action-btn"
         href="../09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf"
         id="btnFreePDF">
        <span class="btn-icon">📖</span>
        <span class="btn-label">
          Free Sample Chapter 1 PDF
          <small>7-Day EHR Leak Audit Included</small>
        </span>
      </a>

      <!-- Tier 1+ -->
      <a class="action-btn" id="btnWorkbook"
         href="../05-WORKBOOKS/chapter-01-workbook.pdf">
        <span class="btn-icon">📝</span>
        <span class="btn-label">
          Fillable Action Workbook
          <small>Chapter 1 — PDF Workbook</small>
        </span>
      </a>

      <!-- Tier 3 only -->
      <a class="action-btn locked" id="btnExcel"
         href="../12-EDITABLE-OFFICE-SUITE/the-ai-freelancer-os-financial-and-pricing-matrix.xlsx">
        <span class="btn-icon">📊</span>
        <span class="btn-label">
          Excel Command Center
          <small>🔒 Tier 3 Flagship Only</small>
        </span>
      </a>

      <!-- Tier 1+ folder -->
      <a class="action-btn" id="btnBlueprints"
         href="../14-AUTOMATION-BLUEPRINTS/">
        <span class="btn-icon">⚡</span>
        <span class="btn-label">
          Automation Blueprints Folder
          <small>JSON n8n / Make / Zapier Blueprints</small>
        </span>
      </a>

    </div>
  </div>
</section>

<!-- ═══════════════════════════════════════════════════════════════════════
     SECTION 3 — Value Ladder & Upgrade Matrix
═══════════════════════════════════════════════════════════════════════ -->
<hr class="section-rule" />
<section class="section" id="matrix">
  <div class="container">
    <p class="section-title">// WHAT YOU GET</p>
    <h2 class="section-heading">Interactive Value Ladder &amp; Upgrade Comparison</h2>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Feature</th>
            <th>Tier 0<br/><span style="color:#7DD3FC;font-weight:400">Free</span></th>
            <th>Tier 1<br/><span style="color:#7DD3FC;font-weight:400">$19</span></th>
            <th>Tier 2<br/><span style="color:#7DD3FC;font-weight:400">$39</span></th>
            <th class="col-star">⭐ Tier 3<br/><span style="color:#FCD34D;font-weight:400">$59</span></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>168-Page Manual PDF + EPUB</td>
            <td><span class="cross">❌</span><br/><span class="partial">Sample Only</span></td>
            <td><span class="check">✅</span></td>
            <td><span class="check">✅</span></td>
            <td><span class="check">✅</span></td>
          </tr>
          <tr>
            <td>50 AI Prompts + 12 Client Scripts</td>
            <td><span class="partial">Ch.1 Only</span></td>
            <td><span class="check">✅</span></td>
            <td><span class="check">✅</span></td>
            <td><span class="check">✅</span></td>
          </tr>
          <tr>
            <td>12-Page Visual Shortcut Atlas</td>
            <td><span class="cross">❌</span></td>
            <td><span class="cross">❌</span></td>
            <td><span class="check">✅</span></td>
            <td><span class="check">✅</span></td>
          </tr>
          <tr>
            <td>Fillable Workbooks + iPad Planner</td>
            <td><span class="partial">Ch.1 Only</span></td>
            <td><span class="cross">❌</span></td>
            <td><span class="check">✅</span></td>
            <td><span class="check">✅</span></td>
          </tr>
          <tr>
            <td>Pro Web App (All 4 Modules)</td>
            <td><span class="partial">Module 1</span></td>
            <td><span class="partial">Module 1</span></td>
            <td><span class="partial">Modules 1–2</span></td>
            <td><span class="check">✅ All 4</span></td>
          </tr>
          <tr>
            <td>8-Tab Charted Excel Command Center</td>
            <td><span class="partial">Free Lite (3 tabs)</span></td>
            <td><span class="cross">❌</span></td>
            <td><span class="cross">❌</span></td>
            <td><span class="check">✅ Full 8 Tabs</span></td>
          </tr>
          <tr>
            <td>5-Database Notion OS Kit</td>
            <td><span class="partial">Starter DB</span></td>
            <td><span class="cross">❌</span></td>
            <td><span class="cross">❌</span></td>
            <td><span class="check">✅ All 5 DBs</span></td>
          </tr>
          <tr>
            <td>7 Word Contracts + 3 PPTX Decks</td>
            <td><span class="cross">❌</span></td>
            <td><span class="cross">❌</span></td>
            <td><span class="partial">Workbook Only</span></td>
            <td><span class="check">✅</span></td>
          </tr>
          <tr>
            <td>3 JSON Automation Blueprints</td>
            <td><span class="partial">Blueprint 1</span></td>
            <td><span class="cross">❌</span></td>
            <td><span class="cross">❌</span></td>
            <td><span class="check">✅ All 3</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="cta-row">
      <a class="cta-btn cta-gold"
         href="https://sunnyomar.gumroad.com/l/ai-freelancer-os"
         target="_blank" rel="noopener">
        ⭐ Upgrade to Complete Flagship OS Bundle ($59)
      </a>
      <a class="cta-btn cta-diamond"
         href="https://sunnyomar.gumroad.com/l/ai-freelancer-vip-vault"
         target="_blank" rel="noopener">
        💎 Join VIP Membership ($9/mo or $49/yr — All 84 Files + Monthly Drops)
      </a>
    </div>
  </div>
</section>

<!-- ═══════════════════════════════════════════════════════════════════════
     SECTION 4 — License Key Entry
═══════════════════════════════════════════════════════════════════════ -->
<hr class="section-rule" />
<section class="section" id="license">
  <div class="container">
    <p class="section-title">// ACTIVATION</p>
    <h2 class="section-heading">Enter Your License Key</h2>

    <div class="license-box">
      <h3>🔑 Activate Your Tier</h3>
      <div class="license-row">
        <input class="license-input" type="text" id="licenseInput"
               placeholder="e.g. FREELANCER-OS-PRO-2026"
               autocomplete="off" spellcheck="false" />
        <button class="license-btn" id="activateBtn">Activate</button>
      </div>
      <p class="license-msg" id="licenseMsg"></p>
    </div>
  </div>
</section>

<!-- ═══════════════════════════════════════════════════════════════════════
     FOOTER
═══════════════════════════════════════════════════════════════════════ -->
<footer>
  System Architect &amp; Author: <strong style="color:#F0F4FF">OMAR SUNNY</strong> |
  Digital Knowledge Product Studio |
  <a href="https://sunnyomar.gumroad.com" target="_blank">sunnyomar.gumroad.com</a> |
  &copy; 2026
</footer>

<!-- ═══════════════════════════════════════════════════════════════════════
     JAVASCRIPT — Tier Detection, localStorage, Progress Tracker
═══════════════════════════════════════════════════════════════════════ -->
<script>
(function () {
  "use strict";

  /* ── Keys ─────────────────────────────────────────────────────────── */
  var KEYS = {
    "FREELANCER-OS-PRO-2026":  3,
    "STUDIO-TIER2-2026":       2,
    "STUDIO-PRO-OS-2026":      3
  };

  /* ── Tier state ───────────────────────────────────────────────────── */
  var currentTier = 0;

  function detectTierFromPath() {
    var href = window.location.href.toLowerCase();
    if (href.indexOf("tier3") !== -1 || href.indexOf("flagship") !== -1) return 3;
    if (href.indexOf("tier2") !== -1 || href.indexOf("workbook") !== -1) return 2;
    if (href.indexOf("tier1") !== -1) return 1;
    return 0;
  }

  function loadStoredTier() {
    try {
      var saved = localStorage.getItem("aifos_tier");
      if (saved) return parseInt(saved, 10) || 0;
    } catch(e) {}
    return 0;
  }

  function saveTier(t) {
    try { localStorage.setItem("aifos_tier", String(t)); } catch(e) {}
  }

  function applyTier(tier) {
    currentTier = tier;
    var badge = document.getElementById("tierBadge");
    var labels = ["Tier 0 — Free", "Tier 1 — Book ($19)", "Tier 2 — Pro ($39)", "Tier 3 — Flagship ($59)"];
    var classes = ["t0", "t1", "t2", "t3"];
    badge.textContent = labels[tier] || labels[0];
    badge.className = "tier-badge " + (classes[tier] || "t0");

    /* Excel — Tier 3 only */
    var btnExcel = document.getElementById("btnExcel");
    if (tier >= 3) {
      btnExcel.classList.remove("locked");
      btnExcel.querySelector("small").textContent = "8-Tab Full Command Center";
    } else {
      btnExcel.classList.add("locked");
      btnExcel.querySelector("small").textContent = "🔒 Tier 3 Flagship Only";
    }

    /* Workbook — Tier 2+ */
    var btnWB = document.getElementById("btnWorkbook");
    if (tier >= 2) {
      btnWB.querySelector("small").textContent = "All Chapters — Fillable PDF";
    } else {
      btnWB.querySelector("small").textContent = "Chapter 1 Preview";
    }

    /* Blueprints — Tier 3 gets all */
    var btnBP = document.getElementById("btnBlueprints");
    if (tier >= 3) {
      btnBP.querySelector("small").textContent = "All 3 Blueprints Unlocked";
    } else if (tier === 0) {
      btnBP.querySelector("small").textContent = "Blueprint 1 only";
    }
  }

  /* ── Quick-Start Progress Tracker ────────────────────────────────── */
  var steps = ["step1", "step2", "step3"];

  function loadProgress() {
    steps.forEach(function(id) {
      try {
        var val = localStorage.getItem("aifos_" + id);
        if (val === "1") document.getElementById(id).checked = true;
      } catch(e) {}
    });
    updateProgressBar();
  }

  function updateProgressBar() {
    var done = steps.filter(function(id) {
      return document.getElementById(id).checked;
    }).length;
    var pct = Math.round((done / steps.length) * 100);
    document.getElementById("progressBar").style.width = pct + "%";
  }

  steps.forEach(function(id) {
    document.getElementById(id).addEventListener("change", function() {
      try { localStorage.setItem("aifos_" + id, this.checked ? "1" : "0"); } catch(e) {}
      updateProgressBar();
    });
  });

  /* ── License Activation ──────────────────────────────────────────── */
  document.getElementById("activateBtn").addEventListener("click", function() {
    var key = (document.getElementById("licenseInput").value || "").trim().toUpperCase();
    var msg = document.getElementById("licenseMsg");

    if (KEYS[key] !== undefined) {
      var tier = KEYS[key];
      saveTier(tier);
      applyTier(tier);
      msg.className = "license-msg ok";
      msg.textContent = "✅ Tier " + tier + " activated! Your access has been upgraded.";
    } else if (key === "") {
      msg.className = "license-msg err";
      msg.textContent = "⚠️ Please enter your license key.";
    } else {
      msg.className = "license-msg err";
      msg.textContent = "❌ Invalid key. Check your Gumroad purchase confirmation email.";
    }
  });

  document.getElementById("licenseInput").addEventListener("keydown", function(e) {
    if (e.key === "Enter") document.getElementById("activateBtn").click();
  });

  /* ── Init ─────────────────────────────────────────────────────────── */
  var pathTier  = detectTierFromPath();
  var storedTier = loadStoredTier();
  applyTier(Math.max(pathTier, storedTier));
  loadProgress();

})();
</script>
</body>
</html>
"""

# Write to studio root
write(os.path.join(STUDIO_ROOT, "START-HERE-LAUNCHPAD.html"), LAUNCHPAD_HTML)
# Write to funnel dir (relative paths need adjustment — use ../.. prefix)
launchpad_funnel = LAUNCHPAD_HTML.replace(
    'href="../07-INTERACTIVE-TOOLS/', 'href="../../07-INTERACTIVE-TOOLS/'
).replace(
    'href="../09-EXPORTS/', 'href="../../09-EXPORTS/'
).replace(
    'href="../05-WORKBOOKS/', 'href="../../05-WORKBOOKS/'
).replace(
    'href="../12-EDITABLE-OFFICE-SUITE/', 'href="../../12-EDITABLE-OFFICE-SUITE/'
).replace(
    'href="../14-AUTOMATION-BLUEPRINTS/', 'href="../../14-AUTOMATION-BLUEPRINTS/'
)
write(os.path.join(FUNNEL_DIR, "START-HERE-LAUNCHPAD.html"), launchpad_funnel)


# ─────────────────────────────────────────────────────────────────────────────
# TASK B1 — funnel-links-config.json
# ─────────────────────────────────────────────────────────────────────────────

funnel_config = {
  "product_name": "The AI Freelancer Operating System",
  "author": "OMAR SUNNY",
  "gumroad_tier0_free_url": "https://sunnyomar.gumroad.com/l/ai-freelancer-os",
  "gumroad_tier1_book_url": "https://sunnyomar.gumroad.com/l/ai-freelancer-os",
  "gumroad_tier2_workbook_url": "https://sunnyomar.gumroad.com/l/ai-freelancer-os",
  "gumroad_tier3_flagship_url": "https://sunnyomar.gumroad.com/l/ai-freelancer-os",
  "gumroad_tier4_vip_url": "https://sunnyomar.gumroad.com/l/ai-freelancer-vip-vault",
  "payhip_store_url": "https://payhip.com/omarsunny",
  "amazon_kdp_ebook_url": "https://amazon.com/dp/PLACEHOLDER-ASIN",
  "amazon_kdp_paperback_url": "https://amazon.com/dp/PLACEHOLDER-ASIN-PRINT",
  "live_web_app_demo_url": "https://cryptxploit.github.io/AI-FreeLancer-OS/15-DEPLOY-AND-FUNNEL-BRIDGE/web-live-demo/",
  "coupon_subscriber15": "SUBSCRIBER15",
  "coupon_launch20": "LAUNCH20",
  "coupon_upgrade25": "UPGRADE25",
  "pro_activation_key_tier3": "FREELANCER-OS-PRO-2026",
  "tier2_activation_key": "STUDIO-TIER2-2026"
}

config_path = os.path.join(FUNNEL_DIR, "funnel-links-config.json")
write(config_path, json.dumps(funnel_config, indent=2))

# Validate JSON round-trip
with open(config_path, "r", encoding="utf-8") as f:
    parsed = json.load(f)
assert parsed["author"] == "OMAR SUNNY", "JSON validation failed!"
print("  🔍 funnel-links-config.json — JSON valid ✅")


# ─────────────────────────────────────────────────────────────────────────────
# TASK B2 — inject_funnel_links.py
# ─────────────────────────────────────────────────────────────────────────────

INJECT_SCRIPT = '''#!/usr/bin/env python3
"""
inject_funnel_links.py
======================
Reads funnel-links-config.json and replaces placeholder tokens
in target HTML files with live URLs.

Usage:
  python inject_funnel_links.py [--dry-run]
"""
import os
import re
import json
import sys
import shutil
from datetime import datetime

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
STUDIO_ROOT = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SCRIPT_DIR, "funnel-links-config.json")

TARGET_FILES = [
    os.path.join(STUDIO_ROOT, "10-MARKETING", "index.html"),
    os.path.join(STUDIO_ROOT, "07-INTERACTIVE-TOOLS", "freelancer-os-app.html"),
    os.path.join(STUDIO_ROOT, "START-HERE-LAUNCHPAD.html"),
    os.path.join(SCRIPT_DIR, "web-live-demo", "index.html"),
]

PLACEHOLDER_MAP = {
    "GUMROAD_TIER0_URL":    "gumroad_tier0_free_url",
    "GUMROAD_TIER1_URL":    "gumroad_tier1_book_url",
    "GUMROAD_TIER2_URL":    "gumroad_tier2_workbook_url",
    "GUMROAD_TIER3_URL":    "gumroad_tier3_flagship_url",
    "GUMROAD_VIP_URL":      "gumroad_tier4_vip_url",
    "PAYHIP_URL":           "payhip_store_url",
    "AMAZON_EBOOK_URL":     "amazon_kdp_ebook_url",
    "AMAZON_PAPERBACK_URL": "amazon_kdp_paperback_url",
    "LIVE_DEMO_URL":        "live_web_app_demo_url",
    "COUPON_SUBSCRIBER15":  "coupon_subscriber15",
    "COUPON_LAUNCH20":      "coupon_launch20",
    "COUPON_UPGRADE25":     "coupon_upgrade25",
    "PRO_KEY_TIER3":        "pro_activation_key_tier3",
    "TIER2_KEY":            "tier2_activation_key",
}

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def inject_file(path, config, dry_run=False):
    if not os.path.isfile(path):
        print(f"  ⚠️  Skipped (not found): {os.path.relpath(path, STUDIO_ROOT)}")
        return 0

    with open(path, "r", encoding="utf-8") as f:
        original = f.read()

    content = original
    replacements = 0

    for placeholder, config_key in PLACEHOLDER_MAP.items():
        value = config.get(config_key, "")
        pattern = re.compile(re.escape(placeholder))
        count = len(pattern.findall(content))
        if count:
            content = pattern.sub(value, content)
            replacements += count
            print(f"    🔁 {placeholder!r:30s} → {value!r}  (×{count})")

    if replacements and not dry_run:
        # Backup original
        backup = path + ".bak." + datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(path, backup)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ {os.path.relpath(path, STUDIO_ROOT)} — {replacements} replacement(s) made (backup: .bak)")
    elif replacements and dry_run:
        print(f"  🔍 [DRY-RUN] {os.path.relpath(path, STUDIO_ROOT)} — {replacements} would be replaced")
    else:
        print(f"  ℹ️  {os.path.relpath(path, STUDIO_ROOT)} — No placeholders found")

    return replacements

def main():
    dry_run = "--dry-run" in sys.argv
    print("=" * 60)
    print("  inject_funnel_links.py — AI Freelancer OS")
    print(f"  Mode: {'DRY-RUN' if dry_run else 'LIVE'}")
    print("=" * 60)

    config = load_config()
    print(f"\\n📋 Config loaded: {len(config)} keys\\n")

    total = 0
    for path in TARGET_FILES:
        print(f"\\n📄 Processing: {os.path.relpath(path, STUDIO_ROOT)}")
        total += inject_file(path, config, dry_run)

    print(f"\\n{'='*60}")
    print(f"  ✅ DONE — Total replacements: {total}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
'''

write(os.path.join(FUNNEL_DIR, "inject_funnel_links.py"), INJECT_SCRIPT)


# ─────────────────────────────────────────────────────────────────────────────
# TASK B3 — web-live-demo/index.html
# ─────────────────────────────────────────────────────────────────────────────

DEMO_INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="description"
  content="The AI Freelancer Operating System by OMAR SUNNY — 5-Gate Client Lifecycle System. 75,158 words, 50 AI prompts, 83 files." />
<title>The AI Freelancer OS — Live Demo | OMAR SUNNY</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg:      #0B1120;
    --surface: #0F1A2E;
    --surf2:   #162035;
    --border:  #1E3050;
    --teal:    #0D9488;
    --teal-lt: #14B8A6;
    --cyan:    #38BDF8;
    --gold:    #F59E0B;
    --gold-lt: #FCD34D;
    --white:   #F0F4FF;
    --muted:   #94A3B8;
    --success: #22C55E;
    --danger:  #EF4444;
    --font-mono: "JetBrains Mono", Consolas, monospace;
    --font-sans: Inter, "Segoe UI", Arial, sans-serif;
    --r: 10px;
  }
  html { scroll-behavior: smooth; }
  body { background: var(--bg); color: var(--white); font-family: var(--font-sans); line-height: 1.6; }
  a { color: inherit; text-decoration: none; }

  /* ── Nav ── */
  nav {
    background: var(--surface); border-bottom: 1px solid var(--border);
    padding: 14px 24px;
    display: flex; align-items: center; justify-content: space-between;
    position: sticky; top: 0; z-index: 50;
  }
  .nav-brand { font-family: var(--font-mono); font-size: 0.82rem; color: var(--cyan); }
  .nav-cta {
    background: var(--teal); color: #fff;
    padding: 8px 18px; border-radius: 6px;
    font-size: 0.85rem; font-weight: 700;
    transition: background 0.2s;
  }
  .nav-cta:hover { background: var(--teal-lt); }

  /* ── Hero ── */
  .hero {
    text-align: center;
    padding: 80px 24px 60px;
    background: radial-gradient(ellipse 90% 55% at 50% -10%, #0D9488 0%, transparent 65%), var(--bg);
  }
  .hero-tag {
    display: inline-block;
    font-family: var(--font-mono); font-size: 0.72rem;
    color: var(--teal-lt); letter-spacing: 0.12em; text-transform: uppercase;
    border: 1px solid var(--teal); border-radius: 20px;
    padding: 4px 14px; margin-bottom: 20px;
  }
  .hero h1 {
    font-size: clamp(1.8rem, 5vw, 3.4rem);
    font-weight: 800; line-height: 1.15;
    color: var(--white); margin-bottom: 16px;
    letter-spacing: -0.02em;
  }
  .hero h1 span { color: var(--cyan); }
  .hero-sub {
    font-size: 1.05rem; color: var(--muted);
    max-width: 640px; margin: 0 auto 36px;
  }
  .hero-btns { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
  .btn-primary {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--teal); color: #fff;
    padding: 14px 28px; border-radius: var(--r);
    font-weight: 700; font-size: 0.95rem;
    transition: background 0.2s, transform 0.15s;
  }
  .btn-primary:hover { background: var(--teal-lt); transform: translateY(-2px); }
  .btn-outline {
    display: inline-flex; align-items: center; gap: 8px;
    border: 2px solid var(--teal); color: var(--teal-lt);
    padding: 14px 28px; border-radius: var(--r);
    font-weight: 700; font-size: 0.95rem;
    transition: background 0.2s, transform 0.15s;
  }
  .btn-outline:hover { background: rgba(13,148,136,0.15); transform: translateY(-2px); }

  /* ── Stats bar ── */
  .stats-bar {
    background: var(--surface);
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    padding: 18px 24px;
    display: flex; justify-content: center; gap: 40px; flex-wrap: wrap;
    font-family: var(--font-mono); font-size: 0.82rem;
  }
  .stat { display: flex; flex-direction: column; align-items: center; gap: 2px; }
  .stat-num { color: var(--cyan); font-size: 1.15rem; font-weight: 700; }
  .stat-label { color: var(--muted); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; }

  /* ── Container ── */
  .container { max-width: 1040px; margin: 0 auto; padding: 0 24px; }

  /* ── Section titles ── */
  .section { padding: 64px 0; }
  .section-tag {
    font-family: var(--font-mono); font-size: 0.72rem;
    color: var(--teal); letter-spacing: 0.12em; text-transform: uppercase;
    margin-bottom: 6px;
  }
  .section-title {
    font-size: clamp(1.4rem, 3vw, 2rem);
    font-weight: 700; color: var(--white);
    margin-bottom: 40px;
  }

  /* ── Pricing Cards ── */
  .cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 20px;
  }
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 28px 22px;
    display: flex; flex-direction: column;
    transition: border-color 0.2s, transform 0.15s;
  }
  .card:hover { border-color: var(--cyan); transform: translateY(-4px); }
  .card.featured {
    border-color: var(--gold);
    background: linear-gradient(160deg, #1A2A10 0%, #0F1A2E 100%);
    position: relative;
  }
  .card.featured::before {
    content: "⭐ BEST VALUE";
    position: absolute; top: -12px; left: 50%; transform: translateX(-50%);
    background: var(--gold); color: #000;
    font-family: var(--font-mono); font-size: 0.65rem; font-weight: 700;
    padding: 3px 12px; border-radius: 12px; white-space: nowrap;
  }
  .card-tier {
    font-family: var(--font-mono); font-size: 0.7rem;
    color: var(--muted); letter-spacing: 0.1em; text-transform: uppercase;
    margin-bottom: 8px;
  }
  .card-name {
    font-size: 1.15rem; font-weight: 700; color: var(--white);
    margin-bottom: 6px;
  }
  .card-price {
    font-size: 2rem; font-weight: 800; color: var(--cyan);
    margin-bottom: 16px; line-height: 1;
  }
  .card-price .price-sub { font-size: 0.8rem; color: var(--muted); font-weight: 400; }
  .card-features { list-style: none; flex: 1; margin-bottom: 20px; }
  .card-features li {
    font-size: 0.84rem; color: var(--muted);
    padding: 5px 0; border-bottom: 1px solid var(--border);
    display: flex; gap: 8px; align-items: flex-start;
  }
  .card-features li:last-child { border-bottom: none; }
  .card-features li span:first-child { flex-shrink: 0; }
  .card-btn {
    display: block; text-align: center;
    padding: 11px 20px; border-radius: 7px;
    font-weight: 700; font-size: 0.88rem;
    background: var(--teal); color: #fff;
    transition: background 0.2s;
  }
  .card.featured .card-btn {
    background: linear-gradient(90deg, #D97706, #F59E0B);
    color: #000;
  }
  .card-btn:hover { filter: brightness(1.1); }

  /* ── Feature highlight strip ── */
  .highlight-strip {
    background: var(--surface);
    border-radius: var(--r); border: 1px solid var(--border);
    padding: 32px 36px;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 24px;
    margin-bottom: 48px;
  }
  .hl-item { display: flex; flex-direction: column; gap: 6px; }
  .hl-icon { font-size: 1.6rem; }
  .hl-title { font-size: 0.9rem; font-weight: 700; color: var(--white); }
  .hl-desc { font-size: 0.8rem; color: var(--muted); }

  /* ── Footer ── */
  footer {
    background: var(--surface); border-top: 1px solid var(--border);
    text-align: center; padding: 28px 24px;
    font-family: var(--font-mono); font-size: 0.78rem; color: var(--muted);
  }
  footer a { color: var(--cyan); }
  footer a:hover { text-decoration: underline; }

  hr.divider {
    border: none; border-top: 1px solid var(--border);
    margin: 0;
  }
</style>
</head>
<body>

<!-- Nav -->
<nav>
  <span class="nav-brand">⚡ AI FREELANCER OS — LIVE DEMO</span>
  <a class="nav-cta" href="https://sunnyomar.gumroad.com/l/ai-freelancer-os" target="_blank" rel="noopener">
    Get Full Bundle →
  </a>
</nav>

<!-- Hero -->
<section class="hero">
  <div class="hero-tag">5-Gate Client Lifecycle System</div>
  <h1>The <span>AI Freelancer</span><br/>Operating System</h1>
  <p class="hero-sub">
    By <strong style="color:#F0F4FF">OMAR SUNNY</strong> |
    Replace Reactive Chaos with a Commercial-Grade Operating System
  </p>
  <div class="hero-btns">
    <a class="btn-primary" href="./app.html">
      ⚡ Try the Interactive OS Web App Live (Free Mode)
    </a>
    <a class="btn-outline" href="https://sunnyomar.gumroad.com/l/ai-freelancer-os"
       target="_blank" rel="noopener">
      📥 Download Free Starter Kit (8 Files — $0)
    </a>
  </div>
</section>

<!-- Stats bar -->
<div class="stats-bar">
  <div class="stat">
    <span class="stat-num">75,158</span>
    <span class="stat-label">Words</span>
  </div>
  <div class="stat">
    <span class="stat-num">50</span>
    <span class="stat-label">AI Prompts</span>
  </div>
  <div class="stat">
    <span class="stat-num">12</span>
    <span class="stat-label">Client Scripts</span>
  </div>
  <div class="stat">
    <span class="stat-num">83</span>
    <span class="stat-label">Files</span>
  </div>
  <div class="stat">
    <span class="stat-num" style="color:var(--gold)">OMAR SUNNY</span>
    <span class="stat-label">System Architect</span>
  </div>
</div>

<hr class="divider" />

<!-- Feature Highlights -->
<section class="section">
  <div class="container">
    <p class="section-tag">// WHAT'S INSIDE</p>
    <h2 class="section-title">Everything to Run Your Freelance Business Like a Pro</h2>

    <div class="highlight-strip">
      <div class="hl-item">
        <span class="hl-icon">📚</span>
        <span class="hl-title">168-Page Manual</span>
        <span class="hl-desc">PDF + EPUB — 5 gates, full frameworks</span>
      </div>
      <div class="hl-item">
        <span class="hl-icon">🤖</span>
        <span class="hl-title">50 AI Prompts</span>
        <span class="hl-desc">Copy-paste into Claude or ChatGPT instantly</span>
      </div>
      <div class="hl-item">
        <span class="hl-icon">📋</span>
        <span class="hl-title">12 Client Scripts</span>
        <span class="hl-desc">Cold outreach to contract close</span>
      </div>
      <div class="hl-item">
        <span class="hl-icon">📊</span>
        <span class="hl-title">Excel Command Center</span>
        <span class="hl-desc">8-tab charted financial dashboard</span>
      </div>
      <div class="hl-item">
        <span class="hl-icon">🗂️</span>
        <span class="hl-title">Notion OS Kit</span>
        <span class="hl-desc">5 linked databases, ready to import</span>
      </div>
      <div class="hl-item">
        <span class="hl-icon">⚡</span>
        <span class="hl-title">Automation Blueprints</span>
        <span class="hl-desc">3 JSON blueprints for n8n / Make / Zapier</span>
      </div>
      <div class="hl-item">
        <span class="hl-icon">📝</span>
        <span class="hl-title">7 Word Contracts</span>
        <span class="hl-desc">Editable, attorney-reviewed templates</span>
      </div>
      <div class="hl-item">
        <span class="hl-icon">🎨</span>
        <span class="hl-title">Visual Shortcut Atlas</span>
        <span class="hl-desc">12-page iPad-ready cheat sheet</span>
      </div>
    </div>

    <!-- Pricing Cards -->
    <p class="section-tag">// PRICING</p>
    <h2 class="section-title">Choose Your Tier</h2>

    <div class="cards-grid">

      <!-- Tier 0 -->
      <div class="card">
        <p class="card-tier">Tier 0</p>
        <p class="card-name">Free Starter Kit</p>
        <p class="card-price">$0 <span class="price-sub">forever free</span></p>
        <ul class="card-features">
          <li><span>📖</span><span>Chapter 1 PDF Sample</span></li>
          <li><span>🤖</span><span>5 AI Prompts</span></li>
          <li><span>🗂️</span><span>Notion Starter Database</span></li>
          <li><span>⚡</span><span>Automation Blueprint 1</span></li>
          <li><span>🚀</span><span>Web App — Module 1</span></li>
        </ul>
        <a class="card-btn"
           href="https://sunnyomar.gumroad.com/l/ai-freelancer-os"
           target="_blank" rel="noopener">
          Download Free →
        </a>
      </div>

      <!-- Tier 1 -->
      <div class="card">
        <p class="card-tier">Tier 1</p>
        <p class="card-name">Full Digital Book</p>
        <p class="card-price">$19 <span class="price-sub">one-time</span></p>
        <ul class="card-features">
          <li><span>📚</span><span>168-Page PDF + EPUB</span></li>
          <li><span>🤖</span><span>50 AI Prompts + 12 Scripts</span></li>
          <li><span>🚀</span><span>Web App — Module 1</span></li>
          <li><span>✅</span><span>Everything in Tier 0</span></li>
        </ul>
        <a class="card-btn"
           href="https://sunnyomar.gumroad.com/l/ai-freelancer-os"
           target="_blank" rel="noopener">
          Get Tier 1 →
        </a>
      </div>

      <!-- Tier 2 -->
      <div class="card">
        <p class="card-tier">Tier 2</p>
        <p class="card-name">Pro Workbook Bundle</p>
        <p class="card-price">$39 <span class="price-sub">one-time</span></p>
        <ul class="card-features">
          <li><span>📝</span><span>Fillable Workbooks + iPad Planner</span></li>
          <li><span>🗺️</span><span>12-Page Visual Shortcut Atlas</span></li>
          <li><span>🚀</span><span>Web App — Modules 1–2</span></li>
          <li><span>✅</span><span>Everything in Tier 1</span></li>
        </ul>
        <a class="card-btn"
           href="https://sunnyomar.gumroad.com/l/ai-freelancer-os"
           target="_blank" rel="noopener">
          Get Tier 2 →
        </a>
      </div>

      <!-- Tier 3 — Featured -->
      <div class="card featured">
        <p class="card-tier">Tier 3</p>
        <p class="card-name">Flagship OS Bundle</p>
        <p class="card-price" style="color:var(--gold-lt)">$59 <span class="price-sub">one-time</span></p>
        <ul class="card-features">
          <li><span>📊</span><span>8-Tab Excel Command Center</span></li>
          <li><span>🗂️</span><span>5-Database Notion OS Kit</span></li>
          <li><span>📄</span><span>7 Word Contracts + 3 PPTX Decks</span></li>
          <li><span>⚡</span><span>All 3 Automation Blueprints</span></li>
          <li><span>🚀</span><span>Web App — All 4 Modules</span></li>
          <li><span>✅</span><span>All 83 Files Included</span></li>
        </ul>
        <a class="card-btn"
           href="https://sunnyomar.gumroad.com/l/ai-freelancer-os"
           target="_blank" rel="noopener">
          ⭐ Get Full Bundle ($59) →
        </a>
      </div>

    </div>

    <!-- VIP CTA -->
    <div style="margin-top:28px; text-align:center;">
      <a href="https://sunnyomar.gumroad.com/l/ai-freelancer-vip-vault"
         target="_blank" rel="noopener"
         style="display:inline-flex;align-items:center;gap:10px;
                background:linear-gradient(90deg,#6366F1,#38BDF8);
                color:#fff;padding:16px 32px;border-radius:10px;
                font-weight:700;font-size:1rem;
                transition:filter 0.2s,transform 0.15s;"
         onmouseover="this.style.filter='brightness(1.12)';this.style.transform='translateY(-2px)'"
         onmouseout="this.style.filter='';this.style.transform=''">
        💎 Join VIP Membership — $9/mo or $49/yr (All 84 Files + Monthly Drops)
      </a>
    </div>
  </div>
</section>

<!-- Footer -->
<footer>
  System Architect &amp; Author: <strong style="color:#F0F4FF">OMAR SUNNY</strong> |
  <a href="https://sunnyomar.gumroad.com" target="_blank">sunnyomar.gumroad.com</a> |
  <a href="https://payhip.com/omarsunny" target="_blank">payhip.com/omarsunny</a> |
  Live Demo:
  <a href="LIVE_DEMO_URL" target="_blank">cryptxploit.github.io/AI-FreeLancer-OS</a>
  &copy; 2026 OMAR SUNNY — All Rights Reserved
</footer>

</body>
</html>
"""

write(os.path.join(DEMO_DIR, "index.html"), DEMO_INDEX_HTML)


# ─────────────────────────────────────────────────────────────────────────────
# TASK B3b — web-live-demo/app.html (redirect)
# ─────────────────────────────────────────────────────────────────────────────

APP_REDIRECT = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<meta http-equiv="refresh" content="0;url=../../07-INTERACTIVE-TOOLS/freelancer-os-app.html" />
<title>Loading AI Freelancer OS App...</title>
</head>
<body style="background:#0B1120;color:#38BDF8;font-family:monospace;
             display:flex;align-items:center;justify-content:center;
             min-height:100vh;text-align:center;">
  <div>
    <p style="font-size:1.5rem;margin-bottom:12px;">⚡ Loading App...</p>
    <p style="color:#94A3B8;font-size:0.9rem;">
      If redirect fails,
      <a style="color:#0D9488" href="../../07-INTERACTIVE-TOOLS/freelancer-os-app.html">
        click here
      </a>
    </p>
  </div>
</body>
</html>
"""

write(os.path.join(DEMO_DIR, "app.html"), APP_REDIRECT)


# ─────────────────────────────────────────────────────────────────────────────
# FINAL REPORT
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 65)
print("  PHASE 10 PART 2 — BUILD REPORT")
print("=" * 65)

all_ok = True
for path, size in created_files:
    rel = os.path.relpath(path, STUDIO_ROOT)
    print(f"  📄 {rel:<65}  {size:>10,} bytes")

print()
print("  VALIDATION CHECKS")
print("  " + "-" * 40)

# Check START-HERE-LAUNCHPAD.html > 10KB
launchpad_path = os.path.join(STUDIO_ROOT, "START-HERE-LAUNCHPAD.html")
lp_size = os.path.getsize(launchpad_path)
ok = lp_size > 10_240
print(f"  {'✅' if ok else '❌'} START-HERE-LAUNCHPAD.html > 10 KB : {lp_size:,} bytes")
if not ok: all_ok = False

# Check funnel-links-config.json is valid JSON
try:
    with open(config_path, "r") as f:
        json.load(f)
    print("  ✅ funnel-links-config.json — Valid JSON")
except Exception as e:
    print(f"  ❌ funnel-links-config.json — JSON ERROR: {e}")
    all_ok = False

# Check web-live-demo/index.html > 5KB
demo_index = os.path.join(DEMO_DIR, "index.html")
di_size = os.path.getsize(demo_index)
ok2 = di_size > 5_120
print(f"  {'✅' if ok2 else '❌'} web-live-demo/index.html > 5 KB  : {di_size:,} bytes")
if not ok2: all_ok = False

print()
print(f"  {'✅ ALL CHECKS PASSED' if all_ok else '❌ SOME CHECKS FAILED'}")
print("=" * 65)
