#!/usr/bin/env python3
"""
build_phase10_part1.py
Phase 10 Part 1 Builder — The AI Freelancer OS by OMAR SUNNY
Tasks: A (HTML upgrade), B (Excel command sheet), C (Notion quickstart), D (Automation blueprint)
"""

import os
import re
import sys
import json
import shutil
import subprocess
import io

# Force UTF-8 stdout so Unicode prints work on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_PATH        = os.path.join(BASE, "07-INTERACTIVE-TOOLS", "freelancer-os-app.html")
XLSX_DIR         = os.path.join(BASE, "06-NOTION-TEMPLATES", "Spreadsheets")
XLSX_PATH        = os.path.join(XLSX_DIR, "tier0-free-lite-command-sheet.xlsx")
NOTION_FREE_DIR  = os.path.join(BASE, "06-NOTION-TEMPLATES", "Tier0-Free-Notion-Quickstart")
NOTION_GUIDE     = os.path.join(NOTION_FREE_DIR, "FREE-NOTION-QUICKSTART-GUIDE.md")
NOTION_CSV_SRC   = os.path.join(BASE, "06-NOTION-TEMPLATES", "01-Leads-CRM-Pipeline.csv")
NOTION_CSV_DST   = os.path.join(NOTION_FREE_DIR, "01-Core-Starter-Database.csv")
AUTO_DIR_SRC     = os.path.join(BASE, "14-AUTOMATION-BLUEPRINTS")
AUTO_FREE_DIR    = os.path.join(BASE, "14-AUTOMATION-BLUEPRINTS", "Tier0-Free-Starter-Automation")
AUTO_JSON_SRC    = os.path.join(AUTO_DIR_SRC, "01-lead-intake-to-ai-brief-and-notion-crm.json")
AUTO_JSON_DST    = os.path.join(AUTO_FREE_DIR, "free-automation-blueprint-01.json")
AUTO_GUIDE       = os.path.join(AUTO_FREE_DIR, "FREE-AUTOMATION-1CLICK-TEST-GUIDE.md")

results = []

# ═══════════════════════════════════════════════════════════════════════════════
# TASK A: HTML UPGRADES
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("TASK A: CRUD Web App HTML Upgrades")
print("="*70)

with open(HTML_PATH, encoding="utf-8") as f:
    html = f.read()

original_size = len(html.encode("utf-8"))
print(f"  Original HTML size: {original_size:,} bytes")
changes_made = []

# ── A1: + Add Custom Row button (if not already present with id="addEhrRow") ──
if 'id="addEhrRow"' not in html:
    anchor = 'onclick="addEhrActionRow()">+ Add Custom Row / Item</button>'
    if anchor in html:
        inject = (
            'onclick="addEhrActionRow()">+ Add Custom Row / Item</button>\n'
            '            <button type="button" id="addEhrRow" class="btn btn-outline" '
            'onclick="addEhrRow()" title="Add a fully custom row with label, hours, and rate">'
            '+ Add Custom Row (EHR)</button>'
        )
        html = html.replace(anchor, inject, 1)
        changes_made.append("A1: Added #addEhrRow button")
    else:
        # Alternative anchor: find the ehr-action-crud-table header section
        anchor2 = 'id="ehr-action-crud-table"'
        if anchor2 in html:
            inject2 = (
                'id="addEhrRow" class="btn btn-outline" style="margin-bottom:8px;" '
                'onclick="addEhrRow()" title="Add custom row: label, hours, rate">'
                '+ Add Custom Row (EHR)</button>\n          '
                '<table id="ehr-action-crud-table"'
            )
            html = html.replace('<table class="data-table" id="ehr-action-crud-table"',
                                '<button type="button" ' + inject2, 1)
            changes_made.append("A1: Injected #addEhrRow button before EHR table")
else:
    changes_made.append("A1: #addEhrRow already present — skipped")

# ── A2: Personal Notes scratchpad per module (moduleNotes_ style with auto-save) ──
# The file already has personal-notes-mod1 through mod4 textareas.
# We inject the moduleNotes_ localStorage pattern into the existing textareas.
notes_inject_js = """
    /* ── Phase 10: moduleNotes_ localStorage auto-save/restore ── */
    (function initModuleNotes() {
      ['1','2','3','4'].forEach(function(n) {
        var el = document.getElementById('moduleNotes_' + n) || document.getElementById('personal-notes-mod' + n);
        if (!el) return;
        el.id = 'moduleNotes_' + n;
        var saved = localStorage.getItem('notes_moduleNotes_' + n);
        if (saved) el.value = saved;
        el.addEventListener('input', function() {
          localStorage.setItem('notes_' + el.id, el.value);
        });
      });
    })();
"""
if "initModuleNotes" not in html:
    html = html.replace("</body>", notes_inject_js + "\n  </body>", 1)
    changes_made.append("A2: Injected moduleNotes_ auto-save/restore JS")
else:
    changes_made.append("A2: moduleNotes_ already present — skipped")

# ── A3: 1-Click JSON Workspace Backup Export (enhanced exportWorkspace button) ──
export_btn_new = """
    <!-- Phase 10: 1-Click Workspace Export Banner -->
    <div id="workspace-export-banner" style="
        background:linear-gradient(135deg,#0B1120 0%,#1E293B 100%);
        border:1px solid #0D9488; border-radius:8px; padding:12px 18px;
        display:flex; align-items:center; gap:14px; margin:10px 16px;
        position:relative; z-index:100;">
      <span style="font-size:22px;">💾</span>
      <div style="flex:1;">
        <strong style="color:#38BDF8; font-size:13px;">Workspace Backup</strong>
        <div style="color:#94A3B8; font-size:11.5px;">All your Module 1–4 inputs, notes, and custom rows saved locally.</div>
      </div>
      <button onclick="exportWorkspace()" style="
          background:#0D9488; color:#fff; border:none; border-radius:6px;
          padding:8px 16px; font-size:12.5px; font-weight:700; cursor:pointer;">
        💾 Export My Workspace
      </button>
    </div>
"""
export_fn_js = """
    /* ── Phase 10: exportWorkspace() — exports all ehr_/notes_/bcr_/ceo_ keys ── */
    function exportWorkspace() {
      var data = {};
      for (var i = 0; i < localStorage.length; i++) {
        var key = localStorage.key(i);
        if (/^(ehr_|notes_|bcr_|ceo_)/.test(key)) {
          data[key] = localStorage.getItem(key);
        }
      }
      // also export full appState if available
      if (typeof appState !== 'undefined') { data['__appState'] = appState; }
      var blob = new Blob([JSON.stringify(data, null, 2)], {type:'application/json'});
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'freelancer-os-workspace.json';
      a.click();
      URL.revokeObjectURL(a.href);
      if (typeof showToast === 'function') showToast('Workspace exported to freelancer-os-workspace.json');
    }
"""
if "function exportWorkspace()" not in html:
    # Add the function before exportWorkspaceJson
    html = html.replace("function exportWorkspaceJson()", export_fn_js + "\n    function exportWorkspaceJson()", 1)
    changes_made.append("A3: Added exportWorkspace() function")
else:
    changes_made.append("A3: exportWorkspace() already present — skipped")

# inject the export banner after the main nav / before main content
if 'workspace-export-banner' not in html:
    # Find the opening of the main app wrapper (after nav)
    anchor_main = '<main id="main-content"'
    if anchor_main in html:
        html = html.replace(anchor_main, export_btn_new + '\n  <main id="main-content"', 1)
        changes_made.append("A3: Injected export banner div")
    else:
        # fallback: inject after opening <body> tag
        html = html.replace("<body>", "<body>\n" + export_btn_new, 1)
        changes_made.append("A3: Injected export banner after <body> (fallback)")
else:
    changes_made.append("A3: Export banner already present — skipped")

# ── A4: 3-Tier Personalized Teaser Banner in Tier 2 locked tab ──
tier2_teaser_html = """
    <!-- Phase 10: Tier 2 Personalized Teaser Banner -->
    <div id="tier2teaser" class="teaser-banner" style="
        background:linear-gradient(135deg,#0B1120 0%,#1E3A5F 100%);
        border:2px solid #0284C7; border-radius:10px; padding:20px 24px;
        margin:16px 0; position:relative;">
      <div style="font-size:13px; color:#94A3B8; margin-bottom:6px; font-weight:700; letter-spacing:0.05em;">
        ⚡ PERSONALIZED AUDIT RESULT
      </div>
      <div id="tier2teaser-text" style="font-size:15px; color:#E2E8F0; line-height:1.65; font-weight:500;">
        Loading your audit results...
      </div>
      <div style="margin-top:14px;">
        <code style="background:#1E3A5F; color:#38BDF8; padding:4px 10px; border-radius:4px; font-size:12px; font-weight:700;">
          STUDIO-TIER2-2026
        </code>
        <span style="color:#64748B; font-size:12px; margin-left:8px;">— Enter this code in the Activate panel above to unlock.</span>
      </div>
      <script>
        (function renderTier2Teaser() {
          var ehr  = parseFloat(localStorage.getItem('ehr_rate') || '0');
          var leak = parseFloat(localStorage.getItem('ehr_annual_leak') || '0');
          var el   = document.getElementById('tier2teaser-text');
          if (!el) return;
          if (!ehr && typeof appState !== 'undefined') {
            ehr  = parseFloat(appState.ehrTrueRate  || appState.ehr_rate || '0');
            leak = parseFloat(appState.ehrAnnualLeak || appState.ehr_annual_leak || '0');
          }
          var ehrStr  = ehr  > 0 ? '$' + ehr.toFixed(2)  : '(enter your data in Module 1)';
          var leakStr = leak > 0 ? '$' + Math.round(leak).toLocaleString() : '(enter your data in Module 1)';
          el.innerHTML = '\u26a1 Based on your audit: Your Effective Hourly Rate is <strong style=\"color:#38BDF8\">' + ehrStr +
            '</strong> and your annual unbilled revenue leak is <strong style=\"color:#F59E0B\">' + leakStr +
            '</strong>. Your custom 90-Day Execution Roadmap is ready \u2014 Activate Tier 2 ' +
            '(Code: <strong style=\"color:#38BDF8\">STUDIO-TIER2-2026</strong>) to unlock it.';
        })();
      </script>
    </div>
"""
if "tier2teaser" not in html:
    # Try to find the tier2 locked panel — look for "STUDIO-TIER2-2026" in a section-like context
    tier2_anchor = 'value="tier2">'
    # Find the upsell / locked content panel
    # Look for the Tier 2 "locked" overlay section
    lock_anchors = [
        '<!-- DYNAMIC PERSONALIZED THIRST',
        'tier2-lock',
        'id="pill-mode-tier2"',
    ]
    injected = False
    for la in lock_anchors:
        if la in html:
            # inject just before this anchor
            html = html.replace(la, tier2_teaser_html + "\n    " + la, 1)
            changes_made.append(f"A4: Injected tier2teaser banner at anchor: {la[:40]}")
            injected = True
            break
    if not injected:
        # Fallback: inject before closing </main>
        html = html.replace("</main>", tier2_teaser_html + "\n  </main>", 1)
        changes_made.append("A4: Injected tier2teaser banner before </main> (fallback)")
else:
    changes_made.append("A4: tier2teaser already present — skipped")

# ── A5: Add STUDIO-PRO-OS-2026 alias key (already in file per search results) ──
if "STUDIO-PRO-OS-2026" in html:
    changes_made.append("A5: STUDIO-PRO-OS-2026 key alias already present — skipped")
else:
    # Inject it into the key-check logic
    html = html.replace(
        '"FREELANCER-OS-PRO-2026"',
        '"FREELANCER-OS-PRO-2026" || cleanKey === "STUDIO-PRO-OS-2026"',
        1
    )
    changes_made.append("A5: Added STUDIO-PRO-OS-2026 alias key")

# Write back
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

new_size = os.path.getsize(HTML_PATH)
print(f"  New HTML size:      {new_size:,} bytes  (delta: +{new_size - original_size:,} bytes)")
for c in changes_made:
    print(f"    ✓ {c}")
results.append(("HTML", HTML_PATH, new_size, new_size > 360000))


# ═══════════════════════════════════════════════════════════════════════════════
# TASK B: TIER 0 FREE LITE EXCEL COMMAND SHEET
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("TASK B: Tier 0 Free Lite Excel Command Sheet")
print("="*70)

try:
    import openpyxl
except ImportError:
    print("  openpyxl not found — installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
    import openpyxl

from openpyxl import Workbook
from openpyxl.styles import (Font, PatternFill, Alignment, Border, Side,
                              GradientFill)
from openpyxl.styles.numbers import FORMAT_NUMBER_COMMA_SEPARATED1 as FORMAT_NUMBER_COMMA_SEP1
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.formatting.rule import CellIsRule

os.makedirs(XLSX_DIR, exist_ok=True)
wb = Workbook()

# ── Helper colours ──
NAVY    = "0B1120"
DARK1   = "1E293B"
DARK2   = "0F172A"
TEAL    = "0D9488"
BLUE    = "0284C7"
GREY    = "475569"
WHITE   = "FFFFFF"
AMBER   = "F59E0B"
RED     = "EF4444"
GREEN   = "22C55E"

def hex_fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def bold_font(color=WHITE, size=11):
    return Font(bold=True, color=color, size=size)

def thin_border():
    s = Side(style="thin", color="334155")
    return Border(left=s, right=s, top=s, bottom=s)

# ══════════════════════════════
# TAB 1: 01_EHR_Leak_Audit
# ══════════════════════════════
ws1 = wb.active
ws1.title = "01_EHR_Leak_Audit"
ws1.sheet_properties.tabColor = TEAL

# Row 1 — mega header
ws1.merge_cells("A1:G1")
ws1["A1"] = "7-DAY TIME & REVENUE LEAK AUDIT — THE AI FREELANCER OS (BY OMAR SUNNY)"
ws1["A1"].font = Font(bold=True, color=WHITE, size=13, name="Calibri")
ws1["A1"].fill = hex_fill(NAVY)
ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws1.row_dimensions[1].height = 30

# Row 2 — empty spacer with dark fill
ws1.merge_cells("A2:G2")
ws1["A2"].fill = hex_fill(DARK2)
ws1.row_dimensions[2].height = 8

# Row 3 — column headers
headers = ["Day", "Bucket A Hrs\n(Billable)", "Bucket B Hrs\n(Client Friction)",
           "Bucket C Hrs\n(Sales Drag)", "Bucket D Hrs\n(Admin)",
           "Daily Revenue ($)", "Realized EHR ($)"]
for col, hdr in enumerate(headers, 1):
    cell = ws1.cell(row=3, column=col, value=hdr)
    cell.font = bold_font(WHITE, 10)
    cell.fill = hex_fill(DARK1)
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = thin_border()
ws1.row_dimensions[3].height = 36

# Rows 4-10: data rows (7 days) with alternating fill
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
for idx, day in enumerate(days):
    row = 4 + idx
    fill_color = DARK1 if idx % 2 == 0 else DARK2
    ws1.cell(row=row, column=1, value=day).fill = hex_fill(fill_color)
    for col in range(2, 8):
        c = ws1.cell(row=row, column=col, value=0)
        c.fill = hex_fill(fill_color)
        c.number_format = "#,##0.00"
        c.border = thin_border()
    ws1.cell(row=row, column=1).font = Font(bold=True, color=WHITE)
    ws1.cell(row=row, column=1).border = thin_border()
    ws1.cell(row=row, column=1).alignment = Alignment(horizontal="center")

# Rows 11-12 (extra days — already covered; set rows 11-12 as weekend extension)
for extra_idx, extra_day in enumerate(["Day 6 Extra", "Day 7 Extra"], 1):
    row = 10 + extra_idx
    fill_color = DARK2 if extra_idx % 2 == 0 else DARK1
    ws1.cell(row=row, column=1, value=extra_day).fill = hex_fill(fill_color)
    ws1.cell(row=row, column=1).font = Font(bold=True, color=WHITE)
    ws1.cell(row=row, column=1).border = thin_border()
    ws1.cell(row=row, column=1).alignment = Alignment(horizontal="center")
    for col in range(2, 8):
        c = ws1.cell(row=row, column=col, value=0)
        c.fill = hex_fill(fill_color)
        c.number_format = "#,##0.00"
        c.border = thin_border()

# Row 13 — TOTALS
ws1.cell(row=13, column=1, value="TOTALS").font = bold_font("F59E0B", 11)
ws1.cell(row=13, column=1).fill = hex_fill(NAVY)
ws1.cell(row=13, column=1).border = thin_border()
ws1.cell(row=13, column=1).alignment = Alignment(horizontal="center")
for col in range(2, 8):
    col_letter = get_column_letter(col)
    c = ws1.cell(row=13, column=col,
                 value=f"=SUM({col_letter}4:{col_letter}12)")
    c.font = bold_font("F59E0B", 11)
    c.fill = hex_fill(NAVY)
    c.number_format = "#,##0.00"
    c.border = thin_border()

# Row 14 — EHR formula
ws1.merge_cells("A14:F14")
ws1["A14"] = "Effective Hourly Rate (EHR) = Total Revenue ÷ Bucket A Hours"
ws1["A14"].font = Font(bold=True, color=WHITE, size=10)
ws1["A14"].fill = hex_fill(DARK1)
ws1["A14"].alignment = Alignment(horizontal="right", vertical="center")
ws1["A14"].border = thin_border()
ehr_cell = ws1["G14"]
ehr_cell.value = "=IF(B13>0, F13/B13, 0)"
ehr_cell.number_format = '"$"#,##0.00'
ehr_cell.font = Font(bold=True, color=RED, size=12)
ehr_cell.fill = hex_fill(DARK1)
ehr_cell.border = thin_border()
ehr_cell.alignment = Alignment(horizontal="center")

# Row 15 — spacer
ws1.row_dimensions[15].height = 6

# Row 16 — Annualized Unbilled Revenue Leak
ws1.merge_cells("A16:F16")
ws1["A16"] = "Annualized Unbilled Revenue Leak  (Non-Billable hrs × 52 wks × Realized EHR)"
ws1["A16"].font = Font(bold=True, color=WHITE, size=10)
ws1["A16"].fill = hex_fill(DARK1)
ws1["A16"].alignment = Alignment(horizontal="right", vertical="center")
ws1["A16"].border = thin_border()
leak_cell = ws1["G16"]
leak_cell.value = "=(B13+C13+D13)*52*G14"
leak_cell.number_format = '"$"#,##,##0'
leak_cell.font = Font(bold=True, color=RED, size=12)
leak_cell.fill = hex_fill(DARK1)
leak_cell.border = thin_border()
leak_cell.alignment = Alignment(horizontal="center")

# Column widths
col_widths = [14, 16, 18, 16, 14, 18, 16]
for i, w in enumerate(col_widths, 1):
    ws1.column_dimensions[get_column_letter(i)].width = w

# Bar chart
chart = BarChart()
chart.type = "col"
chart.title = "Daily Time Bucket Breakdown"
chart.y_axis.title = "Hours"
chart.x_axis.title = "Day"
chart.style = 10
chart.height = 12
chart.width = 22

# Data: cols B,C,D,E (Buckets A-D) for rows 4-10
data_ref = Reference(ws1, min_col=2, max_col=5, min_row=3, max_row=10)
cats_ref  = Reference(ws1, min_col=1, min_row=4, max_row=10)
chart.add_data(data_ref, titles_from_data=True)
chart.set_categories(cats_ref)
ws1.add_chart(chart, "A18")

print("  ✓ Tab 1 (01_EHR_Leak_Audit) built")

# ══════════════════════════════
# TAB 2: 02_Quick_Win_7Day_Tracker
# ══════════════════════════════
ws2 = wb.create_sheet("02_Quick_Win_7Day_Tracker")
ws2.sheet_properties.tabColor = BLUE

ws2.merge_cells("A1:F1")
ws2["A1"] = "7-DAY QUICK-WIN ACTION TRACKER (BY OMAR SUNNY)"
ws2["A1"].font = Font(bold=True, color=WHITE, size=13)
ws2["A1"].fill = hex_fill(NAVY)
ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws2.row_dimensions[1].height = 30

# Header row 2
t2_headers = ["Day", "Top Priority Task", "Gate (01-05)",
              "Time Blocked (mins)", "Done? (Y/N)", "EHR Impact ($)"]
for col, hdr in enumerate(t2_headers, 1):
    c = ws2.cell(row=2, column=col, value=hdr)
    c.font = bold_font(WHITE, 10)
    c.fill = hex_fill(DARK1)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = thin_border()
ws2.row_dimensions[2].height = 32

# Data rows 3-9 (7 days)
t2_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for idx, day in enumerate(t2_days):
    row = 3 + idx
    fill_color = DARK1 if idx % 2 == 0 else DARK2
    ws2.cell(row=row, column=1, value=day).fill = hex_fill(fill_color)
    ws2.cell(row=row, column=1).font = Font(bold=True, color=WHITE, size=10)
    ws2.cell(row=row, column=1).border = thin_border()
    ws2.cell(row=row, column=1).alignment = Alignment(horizontal="center")
    for col in range(2, 7):
        c = ws2.cell(row=row, column=col, value="")
        c.fill = hex_fill(fill_color)
        c.border = thin_border()
        c.font = Font(color=WHITE, size=10)
        if col == 4:
            c.number_format = "#,##0"
        if col == 6:
            c.number_format = '"$"#,##0.00'

# Row 10 — Completed count
ws2.cell(row=10, column=1, value="Tasks Completed:").font = bold_font(WHITE)
ws2.cell(row=10, column=1).fill = hex_fill(NAVY)
ws2.cell(row=10, column=1).border = thin_border()
ws2.cell(row=10, column=2, value='=COUNTA(E3:E9)').font = bold_font("22C55E", 11)
ws2.cell(row=10, column=2).fill = hex_fill(NAVY)
ws2.cell(row=10, column=2).border = thin_border()
ws2.cell(row=10, column=2).alignment = Alignment(horizontal="center")

# Conditional formatting for Done column (E col = col 5)
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill as PF

green_fill = PF("solid", fgColor="166534")
red_fill   = PF("solid", fgColor="7F1D1D")
ws2.conditional_formatting.add(
    "E3:E9",
    CellIsRule(operator="equal", formula=['"Y"'], fill=green_fill,
               font=Font(color=WHITE, bold=True))
)
ws2.conditional_formatting.add(
    "E3:E9",
    CellIsRule(operator="equal", formula=['"N"'], fill=red_fill,
               font=Font(color=WHITE, bold=True))
)

# Column widths
t2_widths = [14, 32, 12, 18, 12, 15]
for i, w in enumerate(t2_widths, 1):
    ws2.column_dimensions[get_column_letter(i)].width = w

print("  ✓ Tab 2 (02_Quick_Win_7Day_Tracker) built")

# ══════════════════════════════
# TAB 3: 03_Pro_Tier_Preview
# ══════════════════════════════
ws3 = wb.create_sheet("03_Pro_Tier_Preview")
ws3.sheet_properties.tabColor = GREY

ws3.merge_cells("A1:C1")
ws3["A1"] = "THE 8-TAB EXCEL COMMAND CENTER — PRO TIER PREVIEW"
ws3["A1"].font = Font(bold=True, color=WHITE, size=13)
ws3["A1"].fill = hex_fill(NAVY)
ws3["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws3.row_dimensions[1].height = 30

ws3.merge_cells("A2:C2")
ws3["A2"] = "Get the full 8-Tab Command Center in Tier 3 ($59) — https://sunnyomar.gumroad.com/l/ai-freelancer-os"
ws3["A2"].font = Font(bold=False, color="94A3B8", size=10)
ws3["A2"].fill = hex_fill(DARK2)
ws3["A2"].alignment = Alignment(horizontal="center")

# Header row 3
t3_headers = ["Tab Name", "What It Does", "Access"]
for col, hdr in enumerate(t3_headers, 1):
    c = ws3.cell(row=3, column=col, value=hdr)
    c.font = bold_font(WHITE, 10)
    c.fill = hex_fill(DARK1)
    c.alignment = Alignment(horizontal="center", vertical="center")
    c.border = thin_border()
ws3.row_dimensions[3].height = 28

tab_data = [
    ("Tab 00 — Dashboard",        "Master KPI cockpit: EHR, leak, gate scores, 90-day pulse",               "✅ INCLUDED FREE"),
    ("Tab 01 — EHR Audit",        "7-Day time & revenue leak audit with bucket breakdown + bar chart",        "✅ INCLUDED FREE"),
    ("Tab 02 — Quick Win Tracker","7-Day action tracker with EHR impact, gate tags, and completion count",    "✅ INCLUDED FREE"),
    ("Tab 03 — BCR Pricing Calc", "Base + Complexity + Risk formula, 3-Tier proposal builder, margin guard",  "🔒 Unlock in Tier 3 ($59) — https://sunnyomar.gumroad.com/l/ai-freelancer-os"),
    ("Tab 04 — WBS Estimator",    "Work-breakdown structure with auto-hour estimate and scope-creep buffer",   "🔒 Unlock in Tier 3 ($59) — https://sunnyomar.gumroad.com/l/ai-freelancer-os"),
    ("Tab 05 — Client Roster",    "Live profitability tracker per client: EHR, friction score, renewal flag",  "🔒 Unlock in Tier 3 ($59) — https://sunnyomar.gumroad.com/l/ai-freelancer-os"),
    ("Tab 06 — CEO Scorecard",    "Friday 20-min CEO review: 8-metric weekly pulse with trend arrows",         "🔒 Unlock in Tier 3 ($59) — https://sunnyomar.gumroad.com/l/ai-freelancer-os"),
    ("Tab 07 — 90-Day Roadmap",   "Quarterly milestone planner with revenue targets and gate assignments",     "🔒 Unlock in Tier 3 ($59) — https://sunnyomar.gumroad.com/l/ai-freelancer-os"),
]

FREE_COLOR  = "0D9488"
LOCKED_FILL = "1E293B"
LOCKED_TXT  = "475569"

for idx, (tab, desc, access) in enumerate(tab_data):
    row = 4 + idx
    is_free = "INCLUDED FREE" in access
    fill_color = DARK2 if idx % 2 == 0 else DARK1
    if not is_free:
        fill_color = LOCKED_FILL

    c1 = ws3.cell(row=row, column=1, value=tab)
    c1.font = Font(bold=True, color=WHITE if is_free else "64748B", size=10)
    c1.fill = hex_fill(fill_color)
    c1.border = thin_border()
    c1.alignment = Alignment(vertical="center")

    c2 = ws3.cell(row=row, column=2, value=desc)
    c2.font = Font(color=WHITE if is_free else "64748B", size=10)
    c2.fill = hex_fill(fill_color)
    c2.border = thin_border()
    c2.alignment = Alignment(wrap_text=True)

    c3 = ws3.cell(row=row, column=3, value=access)
    c3.font = Font(bold=True, color=(FREE_COLOR if is_free else LOCKED_TXT), size=10)
    c3.fill = hex_fill(fill_color)
    c3.border = thin_border()
    c3.alignment = Alignment(horizontal="center", wrap_text=True)

    ws3.row_dimensions[row].height = 30

# Column widths
ws3.column_dimensions["A"].width = 28
ws3.column_dimensions["B"].width = 52
ws3.column_dimensions["C"].width = 55

print("  ✓ Tab 3 (03_Pro_Tier_Preview) built")

wb.save(XLSX_PATH)
xlsx_size = os.path.getsize(XLSX_PATH)
print(f"  ✓ Saved: {XLSX_PATH}")
print(f"    File size: {xlsx_size:,} bytes")
results.append(("XLSX", XLSX_PATH, xlsx_size, xlsx_size > 5000))


# ═══════════════════════════════════════════════════════════════════════════════
# TASK C: FREE NOTION QUICK-START MINI-KIT
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("TASK C: Free Notion Quick-Start Mini-Kit")
print("="*70)

os.makedirs(NOTION_FREE_DIR, exist_ok=True)

# 2. Copy CSV
if os.path.exists(NOTION_CSV_SRC):
    shutil.copy2(NOTION_CSV_SRC, NOTION_CSV_DST)
    print(f"  ✓ Copied CSV to {NOTION_CSV_DST}")
else:
    print(f"  ⚠ Source CSV not found: {NOTION_CSV_SRC}")

# 1. Write guide
notion_guide_text = """\
# FREE NOTION QUICK-START GUIDE — THE AI FREELANCER OS
### By OMAR SUNNY | Tier 0 Free Edition

---

## Import Your CRM Pipeline Into Notion in 60 Seconds

This guide walks you through importing `01-Core-Starter-Database.csv` into Notion so you
can start tracking leads, client status, and revenue opportunities without building anything
from scratch.

---

### What You Get in This Free Kit

One ready-to-use Notion database covering the most critical part of a freelance operation:
**your lead and client pipeline.** The database tracks each contact from first touch through
signed contract, giving you a single place to log follow-ups, proposal status, and deal value.

---

### Step-by-Step Import Instructions

**Step 1 — Open Notion**
Go to [notion.so](https://notion.so) and sign in. If you do not have an account, the free plan
is fully sufficient for this kit.

**Step 2 — Create a New Page**
In your left sidebar, click **+ New Page**. Give it a name like `AI Freelancer OS — CRM Pipeline`.
Press Enter to confirm.

**Step 3 — Open the Import Panel**
Inside your new page, type `/` to open the block menu. Type `import` and select
**Import** from the dropdown list. A file chooser dialog will appear.

**Step 4 — Select the CSV File**
Navigate to where you saved this kit and select `01-Core-Starter-Database.csv`.
Notion will automatically parse the column headers and map them to database properties.

**Step 5 — Review the Columns**
After import, Notion creates a database with the following columns already configured:
- `Lead Name` — Contact or company name
- `Status` — Pipeline stage (New Lead, Proposal Sent, Negotiation, Signed, Lost)
- `Service Type` — The offering being discussed
- `Deal Value ($)` — Estimated or agreed project fee
- `Next Action` — The one specific step to move this deal forward
- `Follow-Up Date` — When to re-engage
- `Notes` — Free-text field for call summaries or client context

**Step 6 — Switch to Board View (Recommended)**
Click **+ Add a View** at the top left of your new database and choose **Board**.
Set the grouping to `Status`. This gives you a visual Kanban board showing every lead
by pipeline stage at a glance.

**Step 7 — Bookmark and Pin**
Click the star icon next to the page name in the sidebar to pin it for fast access.
That is your CRM pipeline, active in under 60 seconds.

---

### Tips for Getting More Out of This Database

- **Filter by Follow-Up Date** to build a daily contact rhythm. Click **Filter → Follow-Up Date
  → is on or before → Today**.
- **Sort by Deal Value** to keep your highest-value opportunities at the top of the list.
- **Use the Notes column** to paste a one-sentence outcome after every client call so your
  pipeline never goes cold from memory gaps.

---

### What Is in the Full Tier 3 Notion OS Kit?

The free kit includes this one database. The complete Tier 3 package contains all five
core databases wired together:

| # | Database | What It Does |
|---|----------|--------------|
| 1 | **CRM Pipeline** | Lead-to-signed tracking across all stages |
| 2 | **Project Command Center** | Active project milestones, deadlines, and gate checklists |
| 3 | **Deliverable Tracker** | Individual task-level progress with Bucket A/B/C/D tagging |
| 4 | **Weekly CEO Scorecard** | Friday review log: EHR, utilization, pipeline health |
| 5 | **90-Day Roadmap Planner** | Quarterly goal board with revenue targets and gate assignments |

Each database is pre-structured, pre-filtered, and linked so that a change in one propagates
across the others. No configuration required — import and start operating.

**Access the full Tier 3 Notion OS Kit at:**
[https://sunnyomar.gumroad.com/l/ai-freelancer-os](https://sunnyomar.gumroad.com/l/ai-freelancer-os)
— Use code `FREELANCER-OS-PRO-2026` or `STUDIO-PRO-OS-2026` at checkout.

---

*The AI Freelancer OS — by OMAR SUNNY*
*Built for independent service professionals who run their practice like an operating system.*
"""

with open(NOTION_GUIDE, "w", encoding="utf-8") as f:
    f.write(notion_guide_text)

notion_words = len(notion_guide_text.split())
notion_size  = os.path.getsize(NOTION_GUIDE)
print(f"  ✓ Written: {NOTION_GUIDE}")
print(f"    Size: {notion_size:,} bytes | Words: {notion_words}")
results.append(("NOTION_GUIDE", NOTION_GUIDE, notion_size, notion_words >= 400))


# ═══════════════════════════════════════════════════════════════════════════════
# TASK D: FREE AUTOMATION BLUEPRINT QUICKSTART
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("TASK D: Free Automation Blueprint Quickstart")
print("="*70)

os.makedirs(AUTO_FREE_DIR, exist_ok=True)

# 1. Copy JSON blueprint
if os.path.exists(AUTO_JSON_SRC):
    shutil.copy2(AUTO_JSON_SRC, AUTO_JSON_DST)
    # Validate JSON
    with open(AUTO_JSON_DST, encoding="utf-8") as f:
        json_data = json.load(f)
    auto_json_size = os.path.getsize(AUTO_JSON_DST)
    print(f"  ✓ Copied and validated JSON: {AUTO_JSON_DST}")
    print(f"    Size: {auto_json_size:,} bytes | Valid JSON: True")
    results.append(("AUTO_JSON", AUTO_JSON_DST, auto_json_size, True))
else:
    print(f"  ⚠ Source JSON not found: {AUTO_JSON_SRC}")
    results.append(("AUTO_JSON", AUTO_JSON_DST, 0, False))

# 2. Write guide
auto_guide_text = """\
# FREE AUTOMATION 1-CLICK TEST GUIDE
### The AI Freelancer OS — Blueprint #1
#### By OMAR SUNNY | Tier 0 Free Edition

---

## Import Blueprint #1 Into Make.com, n8n, or Zapier in Under 5 Minutes

`free-automation-blueprint-01.json` is a pre-built automation that handles one of the most
time-consuming steps in a freelance practice: turning a raw inbound lead into a structured
AI-generated brief and logging it directly into your Notion CRM.

This guide covers how to activate it on three popular no-code platforms.

---

### What This Blueprint Does

1. A new lead fills out a form or sends an email inquiry.
2. The automation sends the lead details to an AI language model.
3. The AI returns a structured client brief: service type, estimated scope, urgency rating,
   and a suggested opening message.
4. The brief is automatically logged as a new entry in your Notion CRM Pipeline database.

Total manual time replaced: approximately 25–40 minutes per new lead.

---

### Option A: Import Into Make.com (Formerly Integromat)

**Step 1** — Log in at [make.com](https://make.com) and go to your workspace.

**Step 2** — Click **Create a new scenario**, then click the three-dot menu at the top
right and choose **Import Blueprint**.

**Step 3** — Select `free-automation-blueprint-01.json` from your local files.
Make will parse the blueprint and display the automation flow as a visual diagram.

**Step 4** — Click each module with a warning icon and connect your accounts:
- **Webhook or Gmail module** — authorize your email or form tool.
- **OpenAI module** — paste your OpenAI API key (get one at platform.openai.com).
- **Notion module** — connect your Notion workspace and select the CRM Pipeline database
  you imported in Task C.

**Step 5** — Click **Run Once** to test with a sample payload. Confirm the Notion entry
appears in your database. Then click **Schedule** to activate it.

---

### Option B: Import Into n8n

**Step 1** — Open your n8n instance (cloud at app.n8n.cloud or self-hosted).

**Step 2** — Click **+New Workflow**, then click the **...** menu and choose
**Import from File**. Select `free-automation-blueprint-01.json`.

**Step 3** — n8n will display the workflow nodes. Click each node marked with a
credential warning and connect the relevant service (Webhook, OpenAI, Notion).

**Step 4** — Use the **Execute Workflow** button to run a test, then toggle
**Active** to go live.

---

### Option C: Import Into Zapier

Note: Zapier uses its own proprietary format, so the JSON cannot be imported directly.
Instead, replicate the blueprint manually using these three Zaps in sequence:

1. **Trigger** — Typeform / Google Forms / Gmail: New Submission
2. **Action 1** — OpenAI: Send Prompt → structured brief output
3. **Action 2** — Notion: Create Database Item → CRM Pipeline

Use the field mappings described in the blueprint JSON (`input_fields`, `output_schema`)
as your guide for mapping variables between steps.

---

### Tease: Blueprints #2 and #3 (Included in Tier 3)

**Blueprint #2 — Contract Signed → 48-Hour Onboarding Sequence**
The moment a contract is signed (via DocuSign or PandaDoc), this blueprint fires a
structured onboarding sequence: welcome email, pre-flight asset request, Notion project
board creation, and a calendar invite for the kickoff call. Zero manual steps.

**Blueprint #3 — Friday CEO Scorecard & Retainer Retention Engine**
Every Friday at a set time, this blueprint pulls your week's data from Notion, runs an
AI-generated performance summary against your EHR targets, and posts a structured CEO
scorecard to your Slack or email. It also flags any client due for a retainer renewal
conversation — so you never miss a high-value upsell window.

Both blueprints are included in the Tier 3 package ($59):
[https://sunnyomar.gumroad.com/l/ai-freelancer-os](https://sunnyomar.gumroad.com/l/ai-freelancer-os)
— Code: `FREELANCER-OS-PRO-2026` or `STUDIO-PRO-OS-2026`

---

*The AI Freelancer OS — by OMAR SUNNY*
*Automate the repeatable. Protect your Maker Blocks. Grow your EHR.*
"""

with open(AUTO_GUIDE, "w", encoding="utf-8") as f:
    f.write(auto_guide_text)

auto_words = len(auto_guide_text.split())
auto_size  = os.path.getsize(AUTO_GUIDE)
print(f"  ✓ Written: {AUTO_GUIDE}")
print(f"    Size: {auto_size:,} bytes | Words: {auto_words}")
results.append(("AUTO_GUIDE", AUTO_GUIDE, auto_size, auto_words >= 400))


# ═══════════════════════════════════════════════════════════════════════════════
# FINAL VERIFICATION REPORT
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("FINAL VERIFICATION REPORT")
print("="*70)

all_pass = True
for label, path, size, ok in results:
    status = "✅ PASS" if ok else "❌ FAIL"
    print(f"  {status}  [{label}]  {os.path.basename(path)}  —  {size:,} bytes")
    if not ok:
        all_pass = False

print()
if all_pass:
    print("  🎉 All tasks completed successfully!")
else:
    print("  ⚠ Some tasks require attention — see FAIL items above.")

print()
print("Summary table:")
print(f"  {'Label':<18} {'File':<52} {'Size':>12}  {'OK?'}")
print(f"  {'-'*18} {'-'*52} {'-'*12}  {'-'*4}")
for label, path, size, ok in results:
    print(f"  {label:<18} {os.path.basename(path):<52} {size:>12,}  {'YES' if ok else 'NO'}")
