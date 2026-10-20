#!/usr/bin/env python3
"""
SaaS-Lite Interactive Web Companion Application Builder (build_webapp.py)
Digital Knowledge Product Studio — The AI Freelancer Operating System (v1.0.0)

Extracts all 50 Tested AI Workflow Prompts (Prompts 1.1 through 10.5) from
03-MANUSCRIPT/Chapters/chapter-01.md..chapter-10.md and all 12 Emergency Client
Scripts (Scripts 1 through 12) from 03-MANUSCRIPT/Back-Matter/back-matter.md,
and compiles the zero-dependency offline/online single-file web application at:
- 07-INTERACTIVE-TOOLS/freelancer-os-app.html
- 09-EXPORTS/HYBRID-BUNDLE/freelancer-os-app.html
"""

import json
import re
import shutil
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

STAGE_BY_CHAPTER = {
    1: "Stage 1: Attract & Filter",
    2: "Stage 1: Attract & Filter",
    3: "Stage 2: Scope & Price",
    4: "Stage 2: Scope & Price",
    5: "Stage 3: Onboard & Align",
    6: "Stage 4: Execute & Protect",
    7: "Stage 4: Execute & Protect",
    8: "Stage 4: Execute & Protect",
    9: "Stage 5: Offboard & Retain",
    10: "Stage 5: Offboard & Retain",
}

SCRIPT_CATEGORY_MAP = {
    1: "Stage 1–2: Lead & Proposal Triage",
    2: "Stage 1–2: Lead & Proposal Triage",
    3: "Stage 1–2: Lead & Proposal Triage",
    4: "Stage 2: Scope & Price Defense",
    5: "Stage 3: Timeline & Asset Resets",
    6: "Stage 4: Scope & Revision Defense",
    7: "Stage 4: Scope & Revision Defense",
    8: "Stage 4: Timeline & Asset Resets",
    9: "Stage 4: Timeline & Asset Resets",
    10: "Stage 4: Payment & Invoice Escalation",
    11: "Stage 5: Retainer & Rate Expansion",
    12: "Stage 5: Retainer & Rate Expansion",
}

SCRIPT_CUSTOMIZATION_NOTES = {
    1: "Verify that your [Minimum Tier 2 Floor] and [Tier 1 Price] match your current B.C.R. Pricing Matrix from Module 2 before sending.",
    2: "Confirm that Option A states the 30-day 100% credit window for upgrading from the Tier 1 Diagnostic Blueprint to the full sprint.",
    3: "Send on Day +10 to Day +14 after proposal delivery; always specify a concrete 5:00 PM slot release time to create calm decision urgency.",
    4: "Enforce the Ironclad Margin Rule: never reduce price without removing concrete deliverables or revision rounds in Option B.",
    5: "Attach the direct Pre-Flight Asset Vault link and state the exact Day-for-Day shifted Milestone 1 and Final Handover dates.",
    6: "Address this message directly to the designated Single Point of Contact (SPOC) and state your recommended commercial tie-breaker for each conflict.",
    7: "Present all three P.V.P. choices (Fast-Track Paid Change Order, Zero-Cost Scope Swap, or Phase 2 Backlog) so the client stays in control.",
    8: "Schedule or send at 9:00 AM on the next business morning; never send at 10:30 PM on a Sunday night.",
    9: "Offer both an immediate same-day async resolution path and a structured next-day office-hours link requiring a 2-bullet agenda.",
    10: "CC the client's billing or accounts-payable contact and include the 1-click Stripe/ACH payment link for immediate settlement.",
    11: "Send 48 hours after delivering the Executive Handover Vault while project momentum and stakeholder satisfaction are at their peak.",
    12: "Provide at least 30 calendar days advance notice prior to the billing cycle adjustment and frame Option A as a preferred legacy partner rate.",
}


def extract_fenced_code(block: str) -> str:
    """Extract the first fenced code block from a Markdown section."""
    lines = block.splitlines()
    in_fence = False
    buf = []
    for line in lines:
        if not in_fence and line.strip().startswith("```"):
            in_fence = True
            continue
        elif in_fence and line.strip() == "```":
            break
        elif in_fence:
            buf.append(line)
    return "\n".join(buf).strip()


def extract_all_prompts() -> list[dict]:
    """Parse all 50 Tested AI Workflow Prompts (Prompts 1.1 through 10.5) from chapters 1 to 10."""
    prompts = []
    for ch in range(1, 11):
        ch_path = BASE_DIR / "03-MANUSCRIPT/Chapters" / f"chapter-{ch:02d}.md"
        txt = ch_path.read_text(encoding="utf-8")
        parts = re.split(r"(?=^###\s+Prompt\s+\d+\.\d+)", txt, flags=re.MULTILINE)
        for part in parts:
            m = re.match(r"^###\s+Prompt\s+(\d+\.\d+):?\s+([^\n]+)", part)
            if not m:
                continue
            pid = m.group(1).strip()
            title = m.group(2).strip()
            block = re.split(r"^##\s+\d+\.", part, flags=re.MULTILINE)[0]

            obj_m = re.search(r"\*\*Operational Objective:\*\*\s*([^\n]+)", block)
            when_m = re.search(r"\*\*When to Run:\*\*\s*([^\n]+)", block)
            ver_m = re.search(r"\*\*Verification Rule:\*\*\s*([^\n]+)", block)

            template = extract_fenced_code(block)
            raw_vars = list(dict.fromkeys(re.findall(r"\[[^\]]+\]", template)))

            prompts.append(
                {
                    "id": pid,
                    "label": f"Prompt {pid}",
                    "type": "prompt",
                    "chapter": ch,
                    "stage": STAGE_BY_CHAPTER[ch],
                    "title": title,
                    "objective": obj_m.group(1).strip() if obj_m else "",
                    "when_to_run": when_m.group(1).strip() if when_m else "",
                    "template": template,
                    "variables": raw_vars,
                    "verification": ver_m.group(1).strip() if ver_m else "",
                }
            )
    if len(prompts) != 50:
        raise RuntimeError(f"Expected 50 prompts, extracted {len(prompts)}")
    return prompts


def extract_all_scripts() -> list[dict]:
    """Parse all 12 Emergency Client Scripts (Scripts 1 through 12) from back-matter.md."""
    bm_path = BASE_DIR / "03-MANUSCRIPT/Back-Matter/back-matter.md"
    bm_txt = bm_path.read_text(encoding="utf-8")
    parts = re.split(r"(?=^###\s+Script\s+\d+)", bm_txt, flags=re.MULTILINE)
    scripts = []
    for part in parts:
        m = re.match(r"^###\s+Script\s+(\d+):?\s+([^\n]+)", part)
        if not m:
            continue
        num = int(m.group(1))
        sid = f"S{num}"
        title = m.group(2).strip()
        block = re.split(r"^##\s+Section\s+\d+", part, flags=re.MULTILINE)[0]

        when_m = re.search(r"\*\*When to Send:\*\*\s*([^\n]+)", block)
        template = extract_fenced_code(block)
        raw_vars = list(dict.fromkeys(re.findall(r"\[[^\]]+\]", template)))

        scripts.append(
            {
                "id": sid,
                "script_number": num,
                "label": f"Script {num}",
                "type": "script",
                "chapter": 11,
                "stage": "12 Emergency Client Scripts",
                "category": SCRIPT_CATEGORY_MAP.get(num, "Scope & Revision Defense"),
                "title": title,
                "objective": f"Ready-to-send word-for-word boundary template ({SCRIPT_CATEGORY_MAP.get(num, 'Client Operations')}).",
                "when_to_run": when_m.group(1).strip() if when_m else "",
                "when_to_use": when_m.group(1).strip() if when_m else "",
                "template": template,
                "variables": raw_vars,
                "verification": SCRIPT_CUSTOMIZATION_NOTES.get(num, "Verify all bracketed variables before sending."),
                "customization_notes": SCRIPT_CUSTOMIZATION_NOTES.get(num, "Verify all bracketed variables before sending."),
            }
        )
    if len(scripts) != 12:
        raise RuntimeError(f"Expected 12 emergency scripts, extracted {len(scripts)}")
    return scripts


def build_html_app(prompts: list[dict], scripts: list[dict]) -> str:
    """Assemble the complete zero-dependency single-file SaaS-Lite web application."""
    prompts_json = json.dumps(prompts, indent=2, ensure_ascii=False)
    scripts_json = json.dumps(scripts, indent=2, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>The AI Freelancer Operating System — Interactive Web Companion (v1.0)</title>
  <style>
    :root {{
      --primary: #0F172A;
      --primary-light: #1E293B;
      --accent: #0284C7;
      --accent-hover: #0369A1;
      --accent-soft: #E0F2FE;
      --secondary: #0D9488;
      --secondary-soft: #CCFBF1;
      --text: #1E293B;
      --muted: #64748B;
      --bg: #FFFFFF;
      --surface: #F8FAFC;
      --surface-alt: #F1F5F9;
      --border: #E2E8F0;
      --border-strong: #CBD5E1;
      --warning: #D97706;
      --warning-soft: #FEF3C7;
      --danger: #DC2626;
      --danger-soft: #FEE2E2;
      --success: #059669;
      --success-soft: #D1FAE5;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
      --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.06);
      --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.08);
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
      --font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', 'Courier New', monospace;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-sans);
      color: var(--text);
      background-color: var(--surface);
      line-height: 1.55;
      font-size: 14.5px;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}

    /* Top Command Bar */
    .top-command-bar {{
      background-color: var(--primary);
      color: #FFFFFF;
      padding: 12px 24px;
      border-bottom: 3px solid var(--accent);
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.2);
    }}

    .top-bar-inner {{
      max-width: 1440px;
      margin: 0 auto;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
    }}

    .brand-cluster {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .brand-logo {{
      width: 38px;
      height: 38px;
      border-radius: 8px;
      background: linear-gradient(135deg, var(--accent), var(--secondary));
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 15px;
      letter-spacing: -0.5px;
      color: #FFFFFF;
      flex-shrink: 0;
    }}

    .brand-title {{
      font-size: 16px;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: #FFFFFF;
      line-height: 1.2;
    }}

    .brand-subtitle {{
      font-size: 11.5px;
      color: #94A3B8;
      font-weight: 500;
    }}

    .command-controls {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
    }}

    .ctrl-select, .ctrl-btn {{
      font-family: var(--font-sans);
      font-size: 12.5px;
      font-weight: 600;
      padding: 7px 11px;
      border-radius: var(--radius-sm);
      border: 1px solid #334155;
      background-color: var(--primary-light);
      color: #F8FAFC;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .ctrl-select:hover, .ctrl-btn:hover {{
      border-color: var(--accent);
      background-color: #334155;
    }}

    .ctrl-btn.accent {{
      background-color: var(--accent);
      border-color: #38BDF8;
      color: #FFFFFF;
    }}

    .ctrl-btn.accent:hover {{
      background-color: var(--accent-hover);
    }}

    .ctrl-btn.teal {{
      background-color: var(--secondary);
      border-color: #2DD4BF;
      color: #FFFFFF;
    }}

    .save-status-badge {{
      font-size: 11.5px;
      font-weight: 600;
      padding: 5px 10px;
      border-radius: 999px;
      background-color: rgba(13, 148, 136, 0.2);
      border: 1px solid var(--secondary);
      color: #5EEAD4;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }}

    /* Module Navigation Tabs */
    .module-nav-bar {{
      background-color: var(--bg);
      border-bottom: 1px solid var(--border);
      box-shadow: var(--shadow-sm);
    }}

    .module-nav-inner {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 0 24px;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}

    .module-tab-btn {{
      font-family: var(--font-sans);
      font-size: 13.5px;
      font-weight: 700;
      color: var(--muted);
      background: transparent;
      border: none;
      border-bottom: 3px solid transparent;
      padding: 14px 18px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.15s ease;
    }}

    .module-tab-btn:hover {{
      color: var(--primary);
      background-color: var(--surface);
    }}

    .module-tab-btn.active {{
      color: var(--accent);
      border-bottom-color: var(--accent);
      background-color: #F0F9FF;
    }}

    .tier-pill {{
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      padding: 2px 6px;
      border-radius: 4px;
      letter-spacing: 0.04em;
    }}

    .tier-pill.free {{
      background-color: var(--secondary-soft);
      color: var(--secondary);
    }}

    .tier-pill.pro {{
      background-color: var(--accent-soft);
      color: var(--accent);
    }}

    /* Main Workspace Container */
    .workspace-container {{
      max-width: 1440px;
      width: 100%;
      margin: 0 auto;
      padding: 24px;
      flex: 1;
    }}

    .module-panel {{
      display: none;
    }}

    .module-panel.active {{
      display: block;
    }}

    /* Pro Edition Gate Banner (Only shown when Free Tier Mode is selected on Modules 2-4) */
    .pro-edition-gate-banner {{
      display: none;
      background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
      color: #FFFFFF;
      border: 2px solid var(--accent);
      border-radius: var(--radius-md);
      padding: 18px 22px;
      margin-bottom: 20px;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
    }}

    .pro-edition-gate-banner.visible {{
      display: flex;
    }}

    /* Grid & Cards */
    .grid-2 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
      gap: 20px;
      margin-bottom: 20px;
    }}

    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 18px;
      margin-bottom: 20px;
    }}

    .grid-4 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 20px;
    }}

    .card {{
      background-color: var(--bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 20px;
      box-shadow: var(--shadow-sm);
      margin-bottom: 20px;
    }}

    .card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border);
      padding-bottom: 12px;
      margin-bottom: 16px;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .card-title {{
      font-size: 16px;
      font-weight: 800;
      color: var(--primary);
    }}

    .card-subtitle {{
      font-size: 12.5px;
      color: var(--muted);
      margin-top: 2px;
    }}

    .badge {{
      display: inline-block;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 999px;
    }}

    .badge.navy {{ background-color: var(--primary); color: #FFFFFF; }}
    .badge.blue {{ background-color: var(--accent-soft); color: var(--accent); }}
    .badge.teal {{ background-color: var(--secondary-soft); color: var(--secondary); }}
    .badge.green {{ background-color: var(--success-soft); color: var(--success); }}
    .badge.amber {{ background-color: var(--warning-soft); color: var(--warning); }}
    .badge.red {{ background-color: var(--danger-soft); color: var(--danger); }}

    /* KPI Cards */
    .kpi-card {{
      background-color: var(--bg);
      border: 1px solid var(--border);
      border-top: 4px solid var(--accent);
      border-radius: var(--radius-md);
      padding: 16px 18px;
      box-shadow: var(--shadow-sm);
    }}

    .kpi-card.teal {{ border-top-color: var(--secondary); }}
    .kpi-card.amber {{ border-top-color: var(--warning); }}
    .kpi-card.red {{ border-top-color: var(--danger); }}
    .kpi-card.green {{ border-top-color: var(--success); }}

    .kpi-label {{
      font-size: 11.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--muted);
      margin-bottom: 6px;
    }}

    .kpi-value {{
      font-size: 26px;
      font-weight: 800;
      color: var(--primary);
      font-family: var(--font-mono);
      line-height: 1.15;
      margin-bottom: 6px;
    }}

    .kpi-meta {{
      font-size: 12px;
      color: var(--muted);
    }}

    /* Form Controls */
    .form-group {{
      margin-bottom: 14px;
    }}

    .form-label {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12.5px;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 5px;
    }}

    .form-hint {{
      font-size: 11.5px;
      color: var(--muted);
      font-weight: 500;
    }}

    .form-input, .form-select, .form-textarea {{
      width: 100%;
      font-family: var(--font-sans);
      font-size: 13.5px;
      color: var(--text);
      background-color: var(--surface);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-sm);
      padding: 8px 11px;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }}

    .form-input:focus, .form-select:focus, .form-textarea:focus {{
      outline: none;
      border-color: var(--accent);
      background-color: var(--bg);
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.12);
    }}

    .form-textarea {{
      min-height: 74px;
      resize: vertical;
      font-family: var(--font-mono);
      font-size: 12.5px;
    }}

    /* Buttons */
    .btn {{
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 700;
      padding: 9px 15px;
      border-radius: var(--radius-sm);
      border: 1px solid transparent;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.15s ease;
    }}

    .btn-primary {{
      background-color: var(--accent);
      color: #FFFFFF;
    }}
    .btn-primary:hover {{
      background-color: var(--accent-hover);
    }}

    .btn-secondary {{
      background-color: var(--secondary);
      color: #FFFFFF;
    }}
    .btn-secondary:hover {{
      background-color: #0F766E;
    }}

    .btn-navy {{
      background-color: var(--primary);
      color: #FFFFFF;
    }}
    .btn-navy:hover {{
      background-color: var(--primary-light);
    }}

    .btn-outline {{
      background-color: var(--bg);
      border-color: var(--border-strong);
      color: var(--text);
    }}
    .btn-outline:hover {{
      border-color: var(--accent);
      color: var(--accent);
    }}

    .btn-danger {{
      background-color: var(--danger-soft);
      color: var(--danger);
      border-color: #FECACA;
      padding: 5px 10px;
      font-size: 12px;
    }}

    /* Stacked Visual Bar Chart */
    .stacked-bar-container {{
      width: 100%;
      height: 28px;
      background-color: var(--surface-alt);
      border-radius: 999px;
      overflow: hidden;
      display: flex;
      margin: 12px 0;
      border: 1px solid var(--border-strong);
    }}

    .stacked-segment {{
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #FFFFFF;
      font-size: 11px;
      font-weight: 700;
      transition: width 0.25s ease;
      overflow: hidden;
      white-space: nowrap;
    }}

    .seg-a {{ background-color: var(--secondary); }}
    .seg-b {{ background-color: var(--danger); }}
    .seg-c {{ background-color: var(--warning); }}
    .seg-d {{ background-color: #6366F1; }}

    .bar-legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      font-size: 12px;
      color: var(--text);
      margin-top: 6px;
    }}

    .legend-dot {{
      display: inline-block;
      width: 10px;
      height: 10px;
      border-radius: 50%;
      margin-right: 5px;
    }}

    /* Tables */
    .table-responsive {{
      width: 100%;
      overflow-x: auto;
    }}

    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}

    table.data-table th {{
      background-color: var(--primary);
      color: #FFFFFF;
      font-weight: 700;
      text-align: left;
      padding: 10px 12px;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}

    table.data-table td {{
      padding: 9px 12px;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }}

    table.data-table tbody tr:nth-child(even) {{
      background-color: var(--surface);
    }}

    /* 3-Tier Pricing Cards */
    .tier-card {{
      background-color: var(--bg);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-md);
      padding: 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }}

    .tier-card.featured {{
      border: 2px solid var(--accent);
      background-color: #F8FAFC;
      box-shadow: var(--shadow-md);
    }}

    .tier-price {{
      font-size: 28px;
      font-weight: 800;
      font-family: var(--font-mono);
      color: var(--primary);
      margin: 8px 0;
    }}

    /* Module 3 Split-Pane Prompt Studio */
    .prompt-studio-layout {{
      display: grid;
      grid-template-columns: 370px 1fr;
      gap: 20px;
      align-items: start;
    }}

    @media (max-width: 980px) {{
      .prompt-studio-layout {{
        grid-template-columns: 1fr;
      }}
    }}

    .prompt-list-pane {{
      background-color: var(--bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      max-height: 760px;
      overflow-y: auto;
      padding: 10px;
    }}

    .prompt-item-btn {{
      width: 100%;
      text-align: left;
      background-color: var(--bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 10px 12px;
      margin-bottom: 7px;
      cursor: pointer;
      transition: all 0.12s ease;
      display: block;
    }}

    .prompt-item-btn:hover {{
      border-color: var(--accent);
      background-color: var(--surface);
    }}

    .prompt-item-btn.active {{
      border-color: var(--accent);
      border-left: 4px solid var(--accent);
      background-color: #F0F9FF;
    }}

    .prompt-item-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 4px;
      font-size: 11.5px;
      font-weight: 800;
      color: var(--accent);
    }}

    .prompt-item-title {{
      font-size: 13px;
      font-weight: 700;
      color: var(--primary);
      line-height: 1.3;
    }}

    .filter-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 10px;
    }}

    .filter-pill {{
      font-family: var(--font-sans);
      font-size: 11.5px;
      font-weight: 700;
      padding: 5px 10px;
      border-radius: 999px;
      border: 1px solid var(--border-strong);
      background-color: var(--bg);
      color: var(--muted);
      cursor: pointer;
    }}

    .filter-pill.active {{
      background-color: var(--primary);
      color: #FFFFFF;
      border-color: var(--primary);
    }}

    .assembled-prompt-box {{
      font-family: var(--font-mono);
      font-size: 12.5px;
      line-height: 1.55;
      background-color: #0F172A;
      color: #F8FAFC;
      padding: 16px;
      border-radius: var(--radius-md);
      border-left: 4px solid var(--accent);
      white-space: pre-wrap;
      word-wrap: break-word;
      max-height: 460px;
      overflow-y: auto;
      margin: 12px 0;
    }}

    .verification-box {{
      background-color: var(--secondary-soft);
      border: 1px solid #99F6E4;
      border-left: 4px solid var(--secondary);
      padding: 12px 14px;
      border-radius: var(--radius-sm);
      font-size: 12.5px;
      color: #134E4A;
      margin-top: 12px;
    }}

    .rate-raise-banner {{
      background: linear-gradient(135deg, #0D9488 0%, #0284C7 100%);
      color: #FFFFFF;
      padding: 14px 18px;
      border-radius: var(--radius-md);
      font-weight: 700;
      margin-bottom: 18px;
      display: none;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}

    .rate-raise-banner.active {{
      display: flex;
    }}

    /* Toast & Modal */
    .toast-notification {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background-color: var(--primary);
      color: #FFFFFF;
      border-left: 4px solid var(--secondary);
      padding: 12px 18px;
      border-radius: var(--radius-sm);
      box-shadow: var(--shadow-md);
      font-size: 13px;
      font-weight: 700;
      z-index: 9999;
      opacity: 0;
      transform: translateY(12px);
      pointer-events: none;
      transition: all 0.2s ease;
    }}

    .toast-notification.show {{
      opacity: 1;
      transform: translateY(0);
    }}

    .modal-backdrop {{
      position: fixed;
      inset: 0;
      background-color: rgba(15, 23, 42, 0.65);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 2000;
      padding: 20px;
    }}

    .modal-backdrop.open {{
      display: flex;
    }}

    .modal-card {{
      background-color: var(--bg);
      border-radius: var(--radius-lg);
      max-width: 640px;
      width: 100%;
      padding: 24px;
      box-shadow: 0 20px 40px rgba(15, 23, 42, 0.25);
      border: 1px solid var(--border);
    }}

    /* Print Stylesheet */
    @media print {{
      .top-command-bar,
      .module-nav-bar,
      .no-print,
      .btn,
      .filter-pills,
      .prompt-list-pane {{
        display: none !important;
      }}
      body {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-size: 10pt !important;
      }}
      .workspace-container {{
        max-width: 100% !important;
        padding: 0 !important;
      }}
      .module-panel {{
        display: block !important;
        page-break-after: always;
      }}
      .card, .kpi-card {{
        box-shadow: none !important;
        border: 1px solid #CBD5E1 !important;
        break-inside: avoid;
      }}
    }}
  </style>
</head>
<body>

  <!-- GLOBAL TOP COMMAND BAR -->
  <header class="top-command-bar">
    <div class="top-bar-inner">
      <div class="brand-cluster">
        <div class="brand-logo">OS</div>
        <div>
          <div class="brand-title">The AI Freelancer Operating System — Interactive Web Companion (v1.0)</div>
          <div class="brand-subtitle">Offline/Online Practitioner Command Suite • 50 AI Workflows • 12 Boundary Scripts • B.C.R. Pricing • Weekly CEO Scorecard</div>
        </div>
      </div>

      <div class="command-controls">
        <span id="save-status-indicator" class="save-status-badge">● Saved locally</span>

        <label for="currency-select" style="font-size:11.5px; color:#CBD5E1;">Currency:</label>
        <select id="currency-select" class="ctrl-select" onchange="handleCurrencyChange(this.value)">
          <option value="$">$ USD</option>
          <option value="£">£ GBP</option>
          <option value="€">€ EUR</option>
          <option value="CA$">CA$ CAD</option>
          <option value="A$">A$ AUD</option>
        </select>

        <label for="edition-mode-toggle" style="font-size:11.5px; color:#CBD5E1;">Edition:</label>
        <select id="edition-mode-toggle" class="ctrl-select" onchange="handleEditionModeChange(this.value)">
          <option value="pro">Tier 3/4: Complete Pro &amp; Living OS Edition</option>
          <option value="free">Tier 0: Free Diagnostic Edition</option>
        </select>

        <button type="button" class="ctrl-btn teal" onclick="loadMarcusCaseStudyDemo()">Load Marcus V. Demo Data</button>
        <button type="button" class="ctrl-btn" onclick="exportWorkspaceJson()">Export .JSON</button>
        <button type="button" class="ctrl-btn" onclick="document.getElementById('import-json-input').click()">Import .JSON</button>
        <input type="file" id="import-json-input" accept=".json" style="display:none;" onchange="importWorkspaceJson(event)" />
        <button type="button" class="ctrl-btn accent" onclick="window.print()">Print / Save PDF</button>
      </div>
    </div>
  </header>

  <!-- MODULE NAVIGATION TABS -->
  <nav class="module-nav-bar">
    <div class="module-nav-inner">
      <button type="button" class="module-tab-btn active" data-tab="tab-ehr-audit" onclick="switchModuleTab('tab-ehr-audit')">
        <span>Module 1: 7-Day EHR Leak Audit &amp; 3-Block Planner</span>
        <span class="tier-pill free">Free + Pro</span>
      </button>
      <button type="button" class="module-tab-btn" data-tab="tab-bcr-pricing" onclick="switchModuleTab('tab-bcr-pricing')">
        <span>Module 2: B.C.R. Scope &amp; 3-Tier Pricing Engine</span>
        <span class="tier-pill pro">Pro OS</span>
      </button>
      <button type="button" class="module-tab-btn" data-tab="tab-prompt-vault" onclick="switchModuleTab('tab-prompt-vault')">
        <span>Module 3: 50-Prompt &amp; 12-Script Studio Builder</span>
        <span class="tier-pill pro">Pro OS</span>
      </button>
      <button type="button" class="module-tab-btn" data-tab="tab-ceo-scorecard" onclick="switchModuleTab('tab-ceo-scorecard')">
        <span>Module 4: Friday CEO Scorecard &amp; 80/20 Client Roster</span>
        <span class="tier-pill pro">Pro + Tier 4</span>
      </button>
    </div>
  </nav>

  <!-- MAIN WORKSPACE CONTAINER -->
  <main class="workspace-container">

    <!-- PRO EDITION ACTIVATION BANNER (Visible on Modules 2-4 only when in Free Diagnostic Mode) -->
    <div id="pro-gate-banner" class="pro-edition-gate-banner no-print">
      <div>
        <div style="font-size:15px; font-weight:800; color:#38BDF8; margin-bottom:3px;">
          Tier 0 Free Diagnostic Preview Mode Active
        </div>
        <div style="font-size:13px; color:#E2E8F0;">
          You are viewing a preview of this Pro module. Enter your Tier 3/4 license code (<code>FREELANCER-OS-PRO-2026</code>) or click <strong>Activate Pro OS Mode</strong> to enable full interactive controls across Modules 2, 3, and 4.
        </div>
      </div>
      <div style="display:flex; gap:8px; align-items:center;">
        <button type="button" class="btn btn-primary" onclick="openProActivationModal()">Activate Pro OS Mode</button>
        <button type="button" class="btn btn-secondary" onclick="instantActivateProMode()">1-Click Enable Full Pro Suite</button>
      </div>
    </div>

    <!-- ================================================================== -->
    <!-- MODULE 1: 7-DAY TIME & EFFECTIVE HOURLY RATE (EHR) LEAK DIAGNOSTIC -->
    <!-- ================================================================== -->
    <section id="tab-ehr-audit" class="module-panel active">
      <div class="card">
        <div class="card-header">
          <div>
            <h1 class="card-title">Module 1: 7-Day Time &amp; Effective Hourly Rate (EHR) Leak Diagnostic</h1>
            <div class="card-subtitle">Synced with Chapter 1, Prompt 1.1 &amp; Standalone Action Worksheet 1.1 — Quantify your real hourly yield and isolate unbilled client friction.</div>
          </div>
          <div style="display:flex; gap:8px; align-items:center;" class="no-print">
            <span class="badge teal">Stage 01: Foundation Gate</span>
            <button type="button" class="btn btn-primary" onclick="generatePreFilledPrompt11()">Generate Pre-Filled Prompt 1.1 From My Audit Numbers</button>
          </div>
        </div>

        <!-- Top 4 Real-Time KPI Cards -->
        <div class="grid-4">
          <div class="kpi-card" id="kpi-card-ehr">
            <div class="kpi-label">True Effective Hourly Rate (EHR)</div>
            <div class="kpi-value" id="out-true-ehr">$26.80/hr</div>
            <div class="kpi-meta" id="out-ehr-collapse">Rate Erosion: -64.3% vs Target Rate</div>
          </div>
          <div class="kpi-card teal">
            <div class="kpi-label">Billable Craft Utilization (Bucket A)</div>
            <div class="kpi-value" id="out-utilization-pct">54.6%</div>
            <div class="kpi-meta" id="out-total-hours-meta">26.5 billable hrs / 48.5 total real hrs (Target: &gt;=65%)</div>
          </div>
          <div class="kpi-card amber">
            <div class="kpi-label">Weekly &amp; Monthly Revenue Leak</div>
            <div class="kpi-value" id="out-monthly-leak">$7,150/mo</div>
            <div class="kpi-meta" id="out-weekly-leak-meta">22.0 unbilled hrs/wk × Target Rate</div>
          </div>
          <div class="kpi-card red">
            <div class="kpi-label">Annualized 48-Week Leak Projection</div>
            <div class="kpi-value" id="out-annual-leak">$79,200/yr</div>
            <div class="kpi-meta">Recoverable margin via 5-Stage Lifecycle Gates</div>
          </div>
        </div>

        <!-- Visual Stacked Horizontal Bar Breakdown -->
        <div style="margin-bottom:20px; background:var(--surface); padding:14px 16px; border-radius:var(--radius-sm); border:1px solid var(--border);">
          <div style="display:flex; justify-content:space-between; font-size:12.5px; font-weight:700; color:var(--primary);">
            <span>Weekly Time Bucket Allocation (Buckets A, B, C &amp; D)</span>
            <span id="out-bar-summary">Total Logged: 48.5 hrs/week</span>
          </div>
          <div class="stacked-bar-container">
            <div id="bar-seg-a" class="stacked-segment seg-a" style="width:54.6%;">A: 54.6%</div>
            <div id="bar-seg-b" class="stacked-segment seg-b" style="width:16.5%;">B: 16.5%</div>
            <div id="bar-seg-c" class="stacked-segment seg-c" style="width:11.3%;">C: 11.3%</div>
            <div id="bar-seg-d" class="stacked-segment seg-d" style="width:17.5%;">D: 17.5%</div>
          </div>
          <div class="bar-legend">
            <span><i class="legend-dot" style="background:var(--secondary);"></i><strong>Bucket A:</strong> Core Billable Craft (<span id="leg-a">26.5h</span>)</span>
            <span><i class="legend-dot" style="background:var(--danger);"></i><strong>Bucket B:</strong> Unbilled Client Friction &amp; Scope Creep (<span id="leg-b">8.0h</span>)</span>
            <span><i class="legend-dot" style="background:var(--warning);"></i><strong>Bucket C:</strong> Unpaid Sales, Proposals &amp; Calls (<span id="leg-c">5.5h</span>)</span>
            <span><i class="legend-dot" style="background:#6366F1;"></i><strong>Bucket D:</strong> Admin Debt &amp; Context-Switching Drag (<span id="leg-d">8.5h</span>)</span>
          </div>
        </div>

        <!-- Audit Inputs + 5-Stage Lifecycle Bottleneck Scorecard -->
        <div class="grid-2">
          <!-- Left Column: Baseline Inputs -->
          <div style="background:var(--surface); padding:18px; border-radius:var(--radius-md); border:1px solid var(--border);">
            <h3 style="font-size:14.5px; font-weight:800; color:var(--primary); margin-bottom:12px;">
              Step 1A: 7-Day Time &amp; Revenue Audit Inputs (Worksheet 1.1 Part A)
            </h3>

            <div class="grid-2" style="grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:0;">
              <div class="form-group">
                <label class="form-label" for="ehr-niche">Service Niche / Role</label>
                <input type="text" id="ehr-niche" class="form-input" value="UX/UI Design & Webflow Development" oninput="recalcEhrModule()" />
              </div>
              <div class="form-group">
                <label class="form-label" for="ehr-period-mode">Revenue Input Mode</label>
                <select id="ehr-period-mode" class="form-select" onchange="recalcEhrModule()">
                  <option value="weekly">Weekly Gross Revenue</option>
                  <option value="monthly">Monthly Gross Revenue (÷ 4.0 wks)</option>
                </select>
              </div>
            </div>

            <div class="grid-2" style="grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:0;">
              <div class="form-group">
                <label class="form-label" for="ehr-target-rate">
                  <span>Stated Target Hourly Rate</span>
                  <span class="form-hint">Line B</span>
                </label>
                <input type="number" id="ehr-target-rate" class="form-input" value="75" min="1" step="1" oninput="recalcEhrModule()" />
              </div>
              <div class="form-group">
                <label class="form-label" for="ehr-gross-rev">
                  <span id="lbl-gross-rev">Gross Revenue Billed (Weekly)</span>
                  <span class="form-hint">Line A</span>
                </label>
                <input type="number" id="ehr-gross-rev" class="form-input" value="1300" min="0" step="50" oninput="recalcEhrModule()" />
              </div>
            </div>

            <div class="grid-2" style="grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:0;">
              <div class="form-group">
                <label class="form-label" for="ehr-bucket-a">
                  <span>Bucket A: Core Billable Hrs/Wk</span>
                  <span class="form-hint">Target &gt;=65%</span>
                </label>
                <input type="number" id="ehr-bucket-a" class="form-input" value="26.5" min="0" step="0.5" oninput="recalcEhrModule()" />
              </div>
              <div class="form-group">
                <label class="form-label" for="ehr-bucket-b">
                  <span>Bucket B: Unbilled Friction Hrs/Wk</span>
                  <span class="form-hint">Target &lt;=5%</span>
                </label>
                <input type="number" id="ehr-bucket-b" class="form-input" value="8.0" min="0" step="0.5" oninput="recalcEhrModule()" />
              </div>
            </div>

            <div class="grid-2" style="grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:0;">
              <div class="form-group">
                <label class="form-label" for="ehr-bucket-c">
                  <span>Bucket C: Sales &amp; Proposals Hrs/Wk</span>
                  <span class="form-hint">Target &lt;=15%</span>
                </label>
                <input type="number" id="ehr-bucket-c" class="form-input" value="5.5" min="0" step="0.5" oninput="recalcEhrModule()" />
              </div>
              <div class="form-group">
                <label class="form-label" for="ehr-bucket-d">
                  <span>Bucket D: Admin &amp; Context Switch Hrs</span>
                  <span class="form-hint">Target &lt;=15%</span>
                </label>
                <input type="number" id="ehr-bucket-d" class="form-input" value="8.5" min="0" step="0.5" oninput="recalcEhrModule()" />
              </div>
            </div>
          </div>

          <!-- Right Column: Interactive 5-Stage Lifecycle Bottleneck Scorecard -->
          <div style="background:var(--surface); padding:18px; border-radius:var(--radius-md); border:1px solid var(--border);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
              <h3 style="font-size:14.5px; font-weight:800; color:var(--primary);">
                Step 1B: 5-Stage Lifecycle Bottleneck Scorecard (1–5)
              </h3>
              <span class="badge navy" id="out-gate-total-score">Score: 12 / 25</span>
            </div>

            <div class="form-group">
              <label class="form-label" for="gate-score-1">
                <span>Stage 01: Attract &amp; Filter (3-Tier Offer &amp; P.A.C.E. Filter)</span>
                <strong id="val-gate-1">2 / 5</strong>
              </label>
              <input type="range" id="gate-score-1" min="1" max="5" value="2" style="width:100%;" oninput="recalcEhrModule()" />
            </div>

            <div class="form-group">
              <label class="form-label" for="gate-score-2">
                <span>Stage 02: Scope &amp; Price (10-Min B.R.I.E.F. &amp; B.C.R. Formula)</span>
                <strong id="val-gate-2">2 / 5</strong>
              </label>
              <input type="range" id="gate-score-2" min="1" max="5" value="2" style="width:100%;" oninput="recalcEhrModule()" />
            </div>

            <div class="form-group">
              <label class="form-label" for="gate-score-3">
                <span>Stage 03: Onboard &amp; Align (48-Hr Pre-Flight Asset Gate)</span>
                <strong id="val-gate-3">3 / 5</strong>
              </label>
              <input type="range" id="gate-score-3" min="1" max="5" value="3" style="width:100%;" oninput="recalcEhrModule()" />
            </div>

            <div class="form-group">
              <label class="form-label" for="gate-score-4">
                <span>Stage 04: Execute &amp; Defend (20/60/20 Sandwich &amp; P.V.P. Change Orders)</span>
                <strong id="val-gate-4">2 / 5</strong>
              </label>
              <input type="range" id="gate-score-4" min="1" max="5" value="2" style="width:100%;" oninput="recalcEhrModule()" />
            </div>

            <div class="form-group">
              <label class="form-label" for="gate-score-5">
                <span>Stage 05: Offboard &amp; Scale (Retainer Bridge &amp; 20-Min Friday CEO)</span>
                <strong id="val-gate-5">3 / 5</strong>
              </label>
              <input type="range" id="gate-score-5" min="1" max="5" value="3" style="width:100%;" oninput="recalcEhrModule()" />
            </div>

            <div id="out-bottleneck-prescription" class="verification-box" style="margin-top:10px;">
              <!-- Populated dynamically by JS -->
            </div>
          </div>
        </div>
      </div>

      <!-- Daily 3-Block Priority Planner (Synced with Prompt 1.3 & Worksheet 1.1 Part C) -->
      <div class="card">
        <div class="card-header">
          <div>
            <h2 class="card-title">Daily 3-Block Priority Architecture Planner (Worksheet 1.1 Part C &amp; Prompt 1.3)</h2>
            <div class="card-subtitle">Protect 3.5 hours of high-margin output every workday before opening reactive inbox channels.</div>
          </div>
          <div style="display:flex; gap:8px;" class="no-print">
            <button type="button" class="btn btn-outline" onclick="openPromptInVault('1.3')">Open Prompt 1.3 in Builder</button>
            <button type="button" class="btn btn-secondary" onclick="copyDailyScheduleMarkdown()">Copy Daily Schedule as Markdown</button>
          </div>
        </div>

        <div class="grid-3">
          <div style="background:var(--surface); padding:16px; border-radius:var(--radius-sm); border-top:3px solid var(--secondary);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
              <strong style="color:var(--primary);">Block 1: 90-Min Morning Maker Block</strong>
              <label style="font-size:12px; font-weight:700; color:var(--secondary);">
                <input type="checkbox" id="blk1-done" onchange="saveAppState()" /> Completed
              </label>
            </div>
            <div style="font-size:11.5px; color:var(--muted); margin-bottom:8px;">08:30–10:00 • Zero Inbox / Zero Slack • Single Highest-EHR Deliverable</div>
            <textarea id="blk1-text" class="form-textarea" oninput="saveAppState()">Client: Acme SaaS — Complete Homepage Hero & Conversion Wireframe (Milestone 1). DoD: Figma prototype link ready for internal QA.</textarea>
          </div>

          <div style="background:var(--surface); padding:16px; border-radius:var(--radius-sm); border-top:3px solid var(--accent);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
              <strong style="color:var(--primary);">Block 2: 30-Min Midday AI Admin Sprint</strong>
              <label style="font-size:12px; font-weight:700; color:var(--accent);">
                <input type="checkbox" id="blk2-done" onchange="saveAppState()" /> Completed
              </label>
            </div>
            <div style="font-size:11.5px; color:var(--muted); margin-bottom:8px;">11:30–12:00 • Batch Triage, P.V.P. Change Orders &amp; Prompt 1.4 Replies</div>
            <textarea id="blk2-text" class="form-textarea" oninput="saveAppState()">1. Send Script 7 P.V.P. Change Order quote ($450) to Client B for extra landing page.
2. Send Script 5 Pre-Flight Asset hold reminder to Client C.</textarea>
          </div>

          <div style="background:var(--surface); padding:16px; border-radius:var(--radius-sm); border-top:3px solid var(--primary);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
              <strong style="color:var(--primary);">Block 3: 90-Min Delivery &amp; Pipeline Block</strong>
              <label style="font-size:12px; font-weight:700; color:var(--primary);">
                <input type="checkbox" id="blk3-done" onchange="saveAppState()" /> Completed
              </label>
            </div>
            <div style="font-size:11.5px; color:var(--muted); margin-bottom:8px;">13:30–15:00 • 60m 20/60/20 Sandwich Execution + 30m B.R.I.E.F. Proposals</div>
            <textarea id="blk3-text" class="form-textarea" oninput="saveAppState()">1. 60m: Run Prompt 6.3 + 6.5 on Client A onboarding email sequence.
2. 30m: Generate 3-option B.R.I.E.F. proposal for Verde Beverage (Prompt 3.3).</textarea>
          </div>
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label class="form-label" for="blk-parking-lot">
            <span>"Not Today" Deferred Parking Lot &amp; Friday SOP Candidate Notes</span>
            <span class="form-hint">Protected from interrupting today's Maker Block</span>
          </label>
          <input type="text" id="blk-parking-lot" class="form-input" value="Reorganize Google Drive archive folders (Deferred to Friday 2:30 PM Admin Window); Extract Webflow SEO Pre-Launch SOP via Prompt 1.2." oninput="saveAppState()" />
        </div>
      </div>
    </section>

    <!-- ================================================================== -->
    <!-- MODULE 2: B.C.R. SCOPE, WBS ESTIMATOR & 3-TIER PRICING CALCULATOR  -->
    <!-- ================================================================== -->
    <section id="tab-bcr-pricing" class="module-panel">
      <div class="card">
        <div class="card-header">
          <div>
            <h1 class="card-title">Module 2: B.C.R. Scope, WBS Estimator &amp; 3-Tier Proposal Pricing Calculator</h1>
            <div class="card-subtitle">Synced with Chapters 2, 3 &amp; 4 and Worksheet 4.1 — Base + Complexity + Risk Buffer Formula &amp; Zero-Discount Trade-Down Counter-Offer Engine.</div>
          </div>
          <div style="display:flex; gap:8px;" class="no-print">
            <span class="badge blue">Stage 02: Commercial &amp; Pricing Gate</span>
            <button type="button" class="btn btn-outline" onclick="openPromptInVault('4.2')">Open Prompt 4.2</button>
            <button type="button" class="btn btn-primary" onclick="copyBriefProposalSummary()">Copy 3-Tier Proposal Summary</button>
          </div>
        </div>

        <!-- Step 2A: Work Breakdown Structure (WBS) Deliverable Table -->
        <div style="margin-bottom:22px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <h3 style="font-size:14.5px; font-weight:800; color:var(--primary);">
              Step 2A: Work Breakdown Structure (WBS) &amp; Hidden Admin Prep Multiplier
            </h3>
            <button type="button" class="btn btn-outline no-print" onclick="addWbsRow()">+ Add Deliverable Row</button>
          </div>

          <div class="table-responsive">
            <table class="data-table" id="wbs-table">
              <thead>
                <tr>
                  <th style="width:42%;">Project Deliverable / Module Name</th>
                  <th style="width:18%;">Optimistic Base Hrs</th>
                  <th style="width:18%;">Admin/Prep Buffer (%)</th>
                  <th style="width:14%;">Weighted Base Hrs</th>
                  <th style="width:8%;" class="no-print">Action</th>
                </tr>
              </thead>
              <tbody id="wbs-tbody">
                <!-- Populated dynamically by JS -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- Step 2B: B.C.R. Multiplier Controls -->
        <div class="grid-4" style="background:var(--surface); padding:16px; border-radius:var(--radius-md); border:1px solid var(--border);">
          <div class="form-group" style="margin-bottom:0;">
            <label class="form-label" for="bcr-hourly-rate">Target Hourly Rate</label>
            <input type="number" id="bcr-hourly-rate" class="form-input" value="85" min="10" step="5" oninput="recalcBcrModule()" />
          </div>
          <div class="form-group" style="margin-bottom:0;">
            <label class="form-label" for="bcr-complexity">Complexity Multiplier (C)</label>
            <select id="bcr-complexity" class="form-select" onchange="recalcBcrModule()">
              <option value="1.00">1.00x — Standard Repeatable Build</option>
              <option value="1.15" selected>1.15x — Moderate Integration / Custom Logic</option>
              <option value="1.30">1.30x — High Technical / Multi-Stakeholder (3+)</option>
              <option value="1.50">1.50x — Mission-Critical / Rush Executive</option>
            </select>
          </div>
          <div class="form-group" style="margin-bottom:0;">
            <label class="form-label" for="bcr-risk">Risk &amp; Dependency Buffer (R%)</label>
            <select id="bcr-risk" class="form-select" onchange="recalcBcrModule()">
              <option value="0.15">15% — Standard Client Asset Dependency</option>
              <option value="0.20" selected>20% — Moderate Copy/Asset Review Risk</option>
              <option value="0.25">25% — High Client / 3rd-Party Dependency</option>
              <option value="0.35">35% — Rush / Unverified Legacy Stack</option>
            </select>
          </div>
          <div class="form-group" style="margin-bottom:0;">
            <label class="form-label" for="bcr-passthrough">Pass-Through Licensing / Costs</label>
            <input type="number" id="bcr-passthrough" class="form-input" value="0" min="0" step="25" oninput="recalcBcrModule()" />
          </div>
        </div>

        <!-- Step 2C: 3-Tier Productized Proposal Matrix -->
        <div style="margin: 20px 0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
            <div>
              <h3 style="font-size:14.5px; font-weight:800; color:var(--primary);">
                Step 2C: Calibrated 3-Tier Proposal Pricing Matrix &amp; Walk-Away Floor
              </h3>
              <div style="font-size:12px; color:var(--muted);" id="out-bcr-formula-trace">
                Weighted Base: 31.2 hrs • B.C.R. Adjusted Equivalent: 43.1 hrs • Hard Walk-Away Minimum Floor: $3,100
              </div>
            </div>
            <div style="display:flex; gap:8px; align-items:center;">
              <label for="bcr-milestone-mode" style="font-size:12px; font-weight:700;">Milestone Split:</label>
              <select id="bcr-milestone-mode" class="form-select" style="width:auto;" onchange="recalcBcrModule()">
                <option value="50-25-25">50% Deposit / 25% Midpoint / 25% Pre-Transfer</option>
                <option value="40-30-30">40% Kickoff / 30% Day 15 / 30% Day 30</option>
                <option value="50-50">50% Upfront Deposit / 50% Final Sign-Off</option>
              </select>
            </div>
          </div>

          <div class="grid-3">
            <!-- Tier 1 -->
            <div class="tier-card">
              <div>
                <span class="badge teal">Option 1: Essential / Diagnostic Baseline (1.00x B.C.R.)</span>
                <div class="tier-price" id="out-tier1-price">$3,650</div>
                <p style="font-size:12.5px; color:var(--muted); margin-bottom:10px;">
                  Core foundational architecture and primary execution sprint with strict scope boundaries.
                </p>
                <ul style="font-size:12.5px; padding-left:18px; margin-bottom:12px;">
                  <li>Core primary deliverables from WBS</li>
                  <li><strong>1 consolidated revision round</strong> (SPOC-verified)</li>
                  <li>Standard turnaround window (14–21 business days)</li>
                  <li>Async portal delivery &amp; Loom walkthrough</li>
                </ul>
              </div>
              <div style="font-size:12px; background:var(--surface); padding:8px 10px; border-radius:4px; border:1px solid var(--border);" id="out-tier1-milestones">
                50% Deposit: $1,825 • 25% Mid: $913 • 25% Final: $912
              </div>
            </div>

            <!-- Tier 2 (Recommended Flagship Anchor) -->
            <div class="tier-card featured">
              <div>
                <span class="badge blue">Option 2: Core Transformation Anchor (1.35x Recommended)</span>
                <div class="tier-price" id="out-tier2-price">$4,950</div>
                <p style="font-size:12.5px; color:var(--muted); margin-bottom:10px;">
                  Complete turnkey implementation, priority integration, and post-launch operational assurance.
                </p>
                <ul style="font-size:12.5px; padding-left:18px; margin-bottom:12px;">
                  <li><strong>100% of WBS deliverables</strong> + priority QA stress-testing</li>
                  <li><strong>2 consolidated revision rounds</strong> + guided feedback frame</li>
                  <li>14-day post-launch optimization &amp; bug-fix guarantee</li>
                  <li>Custom Client Maintenance SOP Vault (Prompt 9.1)</li>
                </ul>
              </div>
              <div style="font-size:12px; background:#E0F2FE; padding:8px 10px; border-radius:4px; border:1px solid #BAE6FD; font-weight:600;" id="out-tier2-milestones">
                50% Deposit: $2,475 • 25% Mid: $1,238 • 25% Final: $1,237
              </div>
            </div>

            <!-- Tier 3 (High Anchor) -->
            <div class="tier-card">
              <div>
                <span class="badge navy">Option 3: Turnkey &amp; Retainer Partner (1.85x High Anchor)</span>
                <div class="tier-price" id="out-tier3-price">$6,750</div>
                <p style="font-size:12.5px; color:var(--muted); margin-bottom:10px;">
                  Expedited executive production plus a 30-day post-launch optimization &amp; team training bridge.
                </p>
                <ul style="font-size:12.5px; padding-left:18px; margin-bottom:12px;">
                  <li>Everything in Option 2 with <strong>priority calendar allocation</strong></li>
                  <li><strong>3 consolidated revision rounds</strong> + stakeholder briefing</li>
                  <li>30-day post-launch conversion/telemetry optimization sprint</li>
                  <li>Live 45-minute team handover &amp; SOP training workshop</li>
                </ul>
              </div>
              <div style="font-size:12px; background:var(--surface); padding:8px 10px; border-radius:4px; border:1px solid var(--border);" id="out-tier3-milestones">
                50% Deposit: $3,375 • 25% Mid: $1,688 • 25% Final: $1,687
              </div>
            </div>
          </div>
        </div>

        <!-- Step 2D: Discount Defense & Scope-Down Counter-Offer Generator -->
        <div style="background:var(--surface); padding:18px; border-radius:var(--radius-md); border:1px solid var(--border);">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
            <div>
              <h3 style="font-size:14.5px; font-weight:800; color:var(--primary);">
                Step 2D: Zero-Discount "Trade-Down" Counter-Offer Generator (Prompt 4.3 &amp; Script 4)
              </h3>
              <div style="font-size:12px; color:var(--muted);">
                Never cut your rate for the same scope. Enter a prospect's lower budget request to compute the exact scope reduction required to preserve your EHR.
              </div>
            </div>
            <button type="button" class="btn btn-secondary no-print" onclick="copyDiscountCounterEmail()">Copy Scope-Down Counter-Offer Email</button>
          </div>

          <div class="grid-2" style="grid-template-columns: 320px 1fr; align-items:start; margin-bottom:0;">
            <div>
              <div class="form-group">
                <label class="form-label" for="bcr-client-name">Prospect / Client Name</label>
                <input type="text" id="bcr-client-name" class="form-input" value="Marcus Tan (Verde Beverage)" oninput="recalcBcrModule()" />
              </div>
              <div class="form-group">
                <label class="form-label" for="bcr-requested-budget">Prospect's Requested Budget</label>
                <input type="number" id="bcr-requested-budget" class="form-input" value="3800" min="100" step="50" oninput="recalcBcrModule()" />
              </div>
              <div id="out-discount-gap-badge" class="badge amber" style="font-size:12px; padding:6px 10px;">
                Budget Gap: -23.2% below Option 2 Anchor
              </div>
            </div>
            <div>
              <label class="form-label" for="out-discount-counter-script">Generated Zero-Discount Scope-Tradeoff Reply (Ready to Send)</label>
              <textarea id="out-discount-counter-script" class="form-textarea" style="min-height:145px;" readonly></textarea>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================== -->
    <!-- MODULE 3: INTERACTIVE 50-PROMPT & 12-SCRIPT STUDIO BUILDER         -->
    <!-- ================================================================== -->
    <section id="tab-prompt-vault" class="module-panel">
      <div class="card">
        <div class="card-header">
          <div>
            <h1 class="card-title">Module 3: Dynamic 50-Prompt &amp; 12-Emergency-Script Studio Builder</h1>
            <div class="card-subtitle">Select any of the 50 Tested AI Workflows (Prompts 1.1–10.5) or 12 Word-for-Word Client Boundary Scripts (Scripts 1–12), fill in your custom variables, and copy in one click.</div>
          </div>
          <span class="badge navy" id="vault-counter-badge">Showing 62 / 62 Assets</span>
        </div>

        <!-- Search & Filter Bar -->
        <div style="background:var(--surface); padding:14px 16px; border-radius:var(--radius-md); border:1px solid var(--border); margin-bottom:18px;" class="no-print">
          <div class="grid-2" style="grid-template-columns: 1fr 280px; gap:12px; margin-bottom:8px;">
            <div>
              <input type="text" id="prompt-search" class="form-input" placeholder="Search all 50 prompts &amp; 12 scripts by keyword (e.g., proposal, scope creep, onboarding, retainer, invoice)..." oninput="filterPromptVault()" />
            </div>
            <div>
              <select id="prompt-chapter-select" class="form-select" onchange="filterPromptVault()">
                <option value="all">All Chapters &amp; Back Matter (62)</option>
                <option value="1">Chapter 1: 5-Stage Operating Model (5)</option>
                <option value="2">Chapter 2: Productized Packaging (5)</option>
                <option value="3">Chapter 3: 10-Min B.R.I.E.F. Proposals (5)</option>
                <option value="4">Chapter 4: B.C.R. Pricing &amp; Margin Defense (5)</option>
                <option value="5">Chapter 5: 48-Hr Client Onboarding (5)</option>
                <option value="6">Chapter 6: 20/60/20 Sandwich Execution (5)</option>
                <option value="7">Chapter 7: P.V.P. Scope Creep Defense (5)</option>
                <option value="8">Chapter 8: Async Updates &amp; Feedback (5)</option>
                <option value="9">Chapter 9: Offboarding &amp; Retainer Bridge (5)</option>
                <option value="10">Chapter 10: Weekly CEO &amp; 90-Day Scaling (5)</option>
                <option value="11">Back Matter: 12 Emergency Client Scripts (12)</option>
              </select>
            </div>
          </div>

          <div class="filter-pills" id="stage-filter-pills">
            <button type="button" class="filter-pill active" data-stage="all" onclick="setStageFilter('all', this)">All (62)</button>
            <button type="button" class="filter-pill" data-stage="Stage 1: Attract & Filter" onclick="setStageFilter('Stage 1: Attract & Filter', this)">Stage 1: Attract (Ch 1–2)</button>
            <button type="button" class="filter-pill" data-stage="Stage 2: Scope & Price" onclick="setStageFilter('Stage 2: Scope & Price', this)">Stage 2: Scope &amp; Price (Ch 3–4)</button>
            <button type="button" class="filter-pill" data-stage="Stage 3: Onboard & Align" onclick="setStageFilter('Stage 3: Onboard & Align', this)">Stage 3: Onboard (Ch 5)</button>
            <button type="button" class="filter-pill" data-stage="Stage 4: Execute & Protect" onclick="setStageFilter('Stage 4: Execute & Protect', this)">Stage 4: Execute &amp; Defend (Ch 6–8)</button>
            <button type="button" class="filter-pill" data-stage="Stage 5: Offboard & Retain" onclick="setStageFilter('Stage 5: Offboard & Retain', this)">Stage 5: Retain &amp; Scale (Ch 9–10)</button>
            <button type="button" class="filter-pill" data-stage="12 Emergency Client Scripts" onclick="setStageFilter('12 Emergency Client Scripts', this)">12 Emergency Client Scripts</button>
          </div>
        </div>

        <!-- Split-Pane Builder -->
        <div class="prompt-studio-layout">
          <!-- Left List -->
          <div class="prompt-list-pane" id="vault-item-list">
            <!-- Populated by JS -->
          </div>

          <!-- Right Active Builder -->
          <div style="background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-md); padding:20px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; flex-wrap:wrap; border-bottom:1px solid var(--border); padding-bottom:12px; margin-bottom:14px;">
              <div>
                <div style="display:flex; gap:8px; align-items:center; margin-bottom:6px;">
                  <span class="badge blue" id="active-item-id-badge">Prompt 1.1</span>
                  <span class="badge teal" id="active-item-stage-badge">Stage 1: Attract &amp; Filter</span>
                </div>
                <h2 style="font-size:17px; font-weight:800; color:var(--primary);" id="active-item-title">
                  Weekly Time-Log &amp; Unbilled Admin Leak Analyzer
                </h2>
              </div>
              <div style="display:flex; gap:8px;" class="no-print">
                <button type="button" class="btn btn-outline" onclick="resetActivePromptVariables()">Reset Variables</button>
                <button type="button" class="btn btn-secondary" onclick="downloadActivePromptMd()">Download .MD</button>
                <button type="button" class="btn btn-primary" onclick="copyAssembledPrompt()">Copy Assembled Text</button>
              </div>
            </div>

            <div style="font-size:13px; margin-bottom:6px;">
              <strong>Operational Objective:</strong> <span id="active-item-objective"></span>
            </div>
            <div style="font-size:13px; color:var(--muted); margin-bottom:14px;">
              <strong>When to Run / Send:</strong> <span id="active-item-when"></span>
            </div>

            <!-- Dynamic Bracketed Variable Input Form -->
            <div style="background:var(--bg); border:1px solid var(--border); border-radius:var(--radius-sm); padding:14px; margin-bottom:14px;">
              <div style="font-size:12.5px; font-weight:800; color:var(--primary); margin-bottom:10px; display:flex; justify-content:space-between;">
                <span>Interactive [VARIABLE] Customizer (Type below to live-update output)</span>
                <span id="active-vars-count" style="color:var(--accent);">4 variables detected</span>
              </div>
              <div id="dynamic-variables-form" class="grid-2" style="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:10px; margin-bottom:0;">
                <!-- Populated dynamically by JS -->
              </div>
            </div>

            <!-- Live Assembled Output -->
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; font-size:12.5px; font-weight:800; color:var(--primary);">
                <span>Live Assembled Prompt / Script Output (Ready to Paste into Claude, ChatGPT, Gemini, or Email)</span>
                <button type="button" class="btn btn-primary no-print" style="padding:5px 10px; font-size:11.5px;" onclick="copyAssembledPrompt()">Copy to Clipboard</button>
              </div>
              <pre id="assembled-prompt-output" class="assembled-prompt-box"></pre>
            </div>

            <!-- Mandatory Verification Rule -->
            <div class="verification-box">
              <strong>Mandatory Quality Gate &amp; Verification Rule:</strong>
              <span id="active-item-verification"></span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================== -->
    <!-- MODULE 4: 20-MINUTE FRIDAY CEO SCORECARD & 80/20 CLIENT ROSTER     -->
    <!-- ================================================================== -->
    <section id="tab-ceo-scorecard" class="module-panel">
      <div class="card">
        <div class="card-header">
          <div>
            <h1 class="card-title">Module 4: 20-Minute Friday CEO Dashboard, 80/20 Client Roster &amp; 90-Day Pipeline Tracker</h1>
            <div class="card-subtitle">Synced with Chapter 10, Prompts 10.1–10.5 &amp; Worksheet 10.1 — Audit client-level EHR, trigger automatic rate raises at 85% capacity, and log weekly CEO retros.</div>
          </div>
          <div style="display:flex; gap:8px;" class="no-print">
            <span class="badge teal">Stage 05: Weekly CEO Scaling Gate</span>
            <button type="button" class="btn btn-outline" onclick="openPromptInVault('10.1')">Open Prompt 10.1</button>
            <button type="button" class="btn btn-secondary" onclick="exportCeoLogCsv()">Export CEO Log (.CSV)</button>
          </div>
        </div>

        <!-- Automatic 85% Capacity Rate-Raise Trigger Banner -->
        <div id="capacity-rate-raise-banner" class="rate-raise-banner active">
          <div>
            <div style="font-size:14.5px; font-weight:800;">
              ⚡ RATE-RAISE TRIGGER ACTIVE (&gt;=85% Billable Capacity Booked)
            </div>
            <div style="font-size:12.5px; opacity:0.95;">
              Your current booked hours exceed 85% of your weekly billable ceiling. Increase quotes by <strong>+15% to +25%</strong> on your next 3 incoming proposals and issue Script 12 / Prompt 4.5 to your lowest-EHR legacy account.
            </div>
          </div>
          <button type="button" class="btn btn-navy no-print" onclick="openPromptInVault('S12')">Open Script 12 (Rate Calibration)</button>
        </div>

        <!-- Top 4 CEO KPI Cards -->
        <div class="grid-4">
          <div class="kpi-card teal">
            <div class="kpi-label">Portfolio Blended Client EHR</div>
            <div class="kpi-value" id="ceo-kpi-blended-ehr">$84.10/hr</div>
            <div class="kpi-meta" id="ceo-kpi-roster-summary">$7,400/mo across 88.0 real hrs</div>
          </div>
          <div class="kpi-card" id="ceo-kpi-cap-card">
            <div class="kpi-label">Weekly Capacity Utilization</div>
            <div class="kpi-value" id="ceo-kpi-capacity-pct">88.0%</div>
            <div class="kpi-meta" id="ceo-kpi-capacity-meta">26.4 booked hrs / 30.0 hr ceiling</div>
          </div>
          <div class="kpi-card green">
            <div class="kpi-label">Confirmed Retainer Floor</div>
            <div class="kpi-value" id="ceo-kpi-retainer-floor">$4,200/mo</div>
            <div class="kpi-meta" id="ceo-kpi-retainer-pct">52.5% of $8,000/mo target covered</div>
          </div>
          <div class="kpi-card amber">
            <div class="kpi-label">90-Day Pipeline Coverage</div>
            <div class="kpi-value" id="ceo-kpi-pipeline-gap">+$1,400</div>
            <div class="kpi-meta" id="ceo-kpi-pipeline-action">30-Day Forecast vs Target Goal</div>
          </div>
        </div>

        <!-- Capacity & 90-Day Pipeline Forecaster Controls -->
        <div class="grid-4" style="background:var(--surface); padding:16px; border-radius:var(--radius-md); border:1px solid var(--border);">
          <div class="form-group" style="margin-bottom:0;">
            <label class="form-label" for="ceo-target-rev">Target Monthly Revenue</label>
            <input type="number" id="ceo-target-rev" class="form-input" value="8000" min="500" step="250" oninput="recalcCeoModule()" />
          </div>
          <div class="form-group" style="margin-bottom:0;">
            <label class="form-label" for="ceo-weekly-cap">Weekly Billable Capacity (Hrs)</label>
            <input type="number" id="ceo-weekly-cap" class="form-input" value="30" min="5" step="1" oninput="recalcCeoModule()" />
          </div>
          <div class="form-group" style="margin-bottom:0;">
            <label class="form-label" for="ceo-retainer-base">Confirmed Retainer Baseline (/mo)</label>
            <input type="number" id="ceo-retainer-base" class="form-input" value="4200" min="0" step="100" oninput="recalcCeoModule()" />
          </div>
          <div class="form-group" style="margin-bottom:0;">
            <label class="form-label" for="ceo-pipeline-weighted">Weighted 90-Day Pipeline</label>
            <input type="number" id="ceo-pipeline-weighted" class="form-input" value="5200" min="0" step="250" oninput="recalcCeoModule()" />
          </div>
        </div>

        <!-- Step 4A: 80/20 Client Profitability & Friction Matrix -->
        <div style="margin: 20px 0;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div>
              <h3 style="font-size:14.5px; font-weight:800; color:var(--primary);">
                Step 4A: 80/20 Client Profitability, Real EHR &amp; Friction Roster (Worksheet 10.1 Part B)
              </h3>
              <div style="font-size:12px; color:var(--muted);">
                Automatically flags "Whale Trap" accounts (high gross fee but high unbilled hours/friction) vs. high-yield retainer candidates.
              </div>
            </div>
            <button type="button" class="btn btn-outline no-print" onclick="addClientRow()">+ Add Active Client</button>
          </div>

          <div class="table-responsive">
            <table class="data-table">
              <thead>
                <tr>
                  <th style="width:24%;">Client / Account Name</th>
                  <th style="width:14%;">Monthly Fee</th>
                  <th style="width:14%;">Real Monthly Hrs</th>
                  <th style="width:12%;">Realized EHR</th>
                  <th style="width:12%;">Friction (1–5)</th>
                  <th style="width:10%;">Rev Share</th>
                  <th style="width:14%;">80/20 CEO Action</th>
                  <th style="width:6%;" class="no-print">Del</th>
                </tr>
              </thead>
              <tbody id="client-roster-tbody">
                <!-- Populated dynamically by JS -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- Step 4B: 12-Week Friday CEO Retrospective Log -->
        <div style="background:var(--surface); padding:18px; border-radius:var(--radius-md); border:1px solid var(--border);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
            <div>
              <h3 style="font-size:14.5px; font-weight:800; color:var(--primary);">
                Step 4B: 12-Week Friday CEO Retrospective &amp; System Upgrade Log
              </h3>
              <div style="font-size:12px; color:var(--muted);">
                Record your weekly Friday 20-minute snapshot to track realized EHR growth across a 90-day operating quarter.
              </div>
            </div>
            <button type="button" class="btn btn-primary no-print" onclick="appendFridayRetroSnapshot()">+ Log Current Week Snapshot</button>
          </div>

          <div class="grid-3" style="margin-bottom:12px;" class="no-print">
            <div class="form-group" style="margin-bottom:0;">
              <label class="form-label" for="retro-failed-gate">Top Bottleneck Gate This Week</label>
              <select id="retro-failed-gate" class="form-select">
                <option value="Gate 01: Attract & Lead Filter">Gate 01: Attract &amp; Lead Filter</option>
                <option value="Gate 02: Scope & B.C.R. Pricing">Gate 02: Scope &amp; B.C.R. Pricing</option>
                <option value="Gate 03: 48-Hr Onboarding Hold">Gate 03: 48-Hr Onboarding Hold</option>
                <option value="Gate 04: P.V.P. Change Order Defense" selected>Gate 04: P.V.P. Change Order Defense</option>
                <option value="Gate 05: Offboard-to-Retainer Bridge">Gate 05: Offboard-to-Retainer Bridge</option>
              </select>
            </div>
            <div class="form-group" style="margin-bottom:0;">
              <label class="form-label" for="retro-system-fix">Permanent SOP / Clause Installed Today</label>
              <input type="text" id="retro-system-fix" class="form-input" value="Installed Script 7 P.V.P. binary choice reply for out-of-scope Slack requests" />
            </div>
            <div class="form-group" style="margin-bottom:0;">
              <label class="form-label" for="retro-monday-p1">Monday Morning Maker Block #1 Priority</label>
              <input type="text" id="retro-monday-p1" class="form-input" value="Ship FinTech Partner Milestone 2 UI Kit before 10:00 AM" />
            </div>
          </div>

          <div class="table-responsive">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Week Date</th>
                  <th>Weekly Revenue</th>
                  <th>Real Hours</th>
                  <th>Realized EHR</th>
                  <th>Bottleneck Gate</th>
                  <th>System Upgrade Installed</th>
                  <th>Monday Block-1 Priority</th>
                </tr>
              </thead>
              <tbody id="ceo-retro-tbody">
                <!-- Populated dynamically by JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- PRO EDITION ACTIVATION MODAL -->
  <div id="pro-activation-modal" class="modal-backdrop no-print">
    <div class="modal-card">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <h3 style="font-size:18px; font-weight:800; color:var(--primary);">Activate Complete Pro &amp; Living OS Mode</h3>
        <button type="button" class="btn btn-outline" style="padding:4px 9px;" onclick="closeProActivationModal()">✕</button>
      </div>
      <p style="font-size:13.5px; color:var(--muted); margin-bottom:14px;">
        Enter your Tier 3 / Tier 4 Companion Access Code from Appendix C of the book (<code>FREELANCER-OS-PRO-2026</code>) or use instant 1-click activation below to enable all 4 modules, 50 AI workflows, and 12 boundary scripts.
      </p>
      <div class="form-group">
        <label class="form-label" for="license-code-input">Companion Access Code</label>
        <input type="text" id="license-code-input" class="form-input" value="FREELANCER-OS-PRO-2026" />
      </div>
      <div style="display:flex; justify-content:flex-end; gap:10px;">
        <button type="button" class="btn btn-outline" onclick="closeProActivationModal()">Cancel</button>
        <button type="button" class="btn btn-primary" onclick="verifyAndActivateProCode()">Activate Pro Edition Now</button>
      </div>
    </div>
  </div>

  <!-- TOAST NOTIFICATION -->
  <div id="app-toast" class="toast-notification">Action completed</div>

  <!-- EMBEDDED SINGLE-SOURCE DATASET (50 PROMPTS + 12 EMERGENCY SCRIPTS) -->
  <script>
    const STUDIO_PROMPTS_DATA = {prompts_json};
    const STUDIO_SCRIPTS_DATA = {scripts_json};
    const ALL_VAULT_ITEMS = [...STUDIO_PROMPTS_DATA, ...STUDIO_SCRIPTS_DATA];

    const STORAGE_KEY = "ai_freelancer_os_workspace_v1";

    let appState = {{
      currency: "$",
      editionMode: "pro",
      activeTab: "tab-ehr-audit",
      ehr: {{
        niche: "UX/UI Design & Webflow Development",
        periodMode: "weekly",
        targetRate: 75,
        grossRev: 1300,
        bucketA: 26.5,
        bucketB: 8.0,
        bucketC: 5.5,
        bucketD: 8.5,
        gates: [2, 2, 3, 2, 3]
      }},
      planner: {{
        blk1Done: false,
        blk1Text: "Client: Acme SaaS — Complete Homepage Hero & Conversion Wireframe (Milestone 1). DoD: Figma prototype link ready for internal QA.",
        blk2Done: false,
        blk2Text: "1. Send Script 7 P.V.P. Change Order quote ($450) to Client B for extra landing page.\\n2. Send Script 5 Pre-Flight Asset hold reminder to Client C.",
        blk3Done: false,
        blk3Text: "1. 60m: Run Prompt 6.3 + 6.5 on Client A onboarding email sequence.\\n2. 30m: Generate 3-option B.R.I.E.F. proposal for Verde Beverage (Prompt 3.3).",
        parkingLot: "Reorganize Google Drive archive folders (Deferred to Friday 2:30 PM Admin Window); Extract Webflow SEO Pre-Launch SOP via Prompt 1.2."
      }},
      bcr: {{
        hourlyRate: 85,
        complexity: 1.15,
        risk: 0.20,
        passthrough: 0,
        milestoneMode: "50-25-25",
        clientName: "Marcus Tan (Verde Beverage)",
        requestedBudget: 3800,
        wbs: [
          {{ name: "1. Discovery, Architecture & Voice DNA Alignment", baseHrs: 4.5, bufferPct: 20 }},
          {{ name: "2. Core Deliverable Build & Modular Execution", baseHrs: 14.0, bufferPct: 20 }},
          {{ name: "3. Responsive / Technical Integration & Setup", baseHrs: 5.0, bufferPct: 20 }},
          {{ name: "4. 4-Gate Pre-Submission QA & Red-Team Audit", baseHrs: 3.0, bufferPct: 20 }},
          {{ name: "5. Client Walkthrough, Revisions & Handover Vault", baseHrs: 3.5, bufferPct: 20 }}
        ]
      }},
      vault: {{
        selectedId: "1.1",
        stageFilter: "all",
        chapterFilter: "all",
        searchQuery: "",
        customVars: {{}}
      }},
      ceo: {{
        targetRev: 8000,
        weeklyCap: 30,
        retainerBase: 4200,
        pipelineWeighted: 5200,
        clients: [
          {{ name: "Apex FinTech (Growth Retainer)", revenue: 2800, hours: 24.0, friction: 1 }},
          {{ name: "Verde Beverage (Brand & Packaging Sprint)", revenue: 2200, hours: 21.5, friction: 2 }},
          {{ name: "NorthStar Logistics (Legacy Custom Account)", revenue: 1500, hours: 29.5, friction: 5 }},
          {{ name: "Clarity Health (Maintenance Retainer)", revenue: 900, hours: 9.0, friction: 1 }}
        ],
        retroLog: [
          {{
            date: "2026-10-09",
            revenue: 1450,
            hours: 44.0,
            ehr: 32.95,
            gate: "Gate 03: 48-Hr Onboarding Hold",
            fix: "Enforced 100% Pre-Flight Asset Vault rule before booking kickoff calls",
            mondayP1: "Complete Apex FinTech design system tokens"
          }},
          {{
            date: "2026-10-16",
            revenue: 1850,
            hours: 37.5,
            ehr: 49.33,
            gate: "Gate 04: P.V.P. Change Order Defense",
            fix: "Converted 2 unbilled Slack requests into $650 paid P.V.P. Change Orders",
            mondayP1: "Ship Verde Beverage Milestone 1 packaging dielines"
          }}
        ]
      }}
    }};

    function showToast(msg) {{
      const t = document.getElementById("app-toast");
      t.textContent = msg;
      t.classList.add("show");
      setTimeout(() => t.classList.remove("show"), 2600);
    }}

    function fmtMoney(amount, decimals = 0) {{
      const cur = appState.currency || "$";
      const val = Number(amount) || 0;
      const sign = val < 0 ? "-" : "";
      const absVal = Math.abs(val);
      return sign + cur + absVal.toLocaleString("en-US", {{
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
      }});
    }}

    function saveAppState() {{
      try {{
        appState.planner.blk1Done = document.getElementById("blk1-done").checked;
        appState.planner.blk1Text = document.getElementById("blk1-text").value;
        appState.planner.blk2Done = document.getElementById("blk2-done").checked;
        appState.planner.blk2Text = document.getElementById("blk2-text").value;
        appState.planner.blk3Done = document.getElementById("blk3-done").checked;
        appState.planner.blk3Text = document.getElementById("blk3-text").value;
        appState.planner.parkingLot = document.getElementById("blk-parking-lot").value;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(appState));
        const badge = document.getElementById("save-status-indicator");
        if (badge) {{
          badge.textContent = "● Saved locally (" + new Date().toLocaleTimeString([], {{hour: '2-digit', minute:'2-digit'}}) + ")";
        }}
      }} catch (e) {{
        console.warn("LocalStorage save warning:", e);
      }}
    }}

    function loadAppState() {{
      try {{
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) {{
          const parsed = JSON.parse(raw);
          appState = Object.assign({{}}, appState, parsed);
        }}
      }} catch (e) {{
        console.warn("LocalStorage load warning:", e);
      }}

      // Check URL query parameter ?mode=free or ?mode=pro
      const params = new URLSearchParams(window.location.search);
      const urlMode = params.get("mode");
      if (urlMode === "free" || urlMode === "pro") {{
        appState.editionMode = urlMode;
      }}
    }}

    function syncInputsFromState() {{
      document.getElementById("currency-select").value = appState.currency || "$";
      document.getElementById("edition-mode-toggle").value = appState.editionMode || "pro";

      // Module 1
      document.getElementById("ehr-niche").value = appState.ehr.niche;
      document.getElementById("ehr-period-mode").value = appState.ehr.periodMode;
      document.getElementById("ehr-target-rate").value = appState.ehr.targetRate;
      document.getElementById("ehr-gross-rev").value = appState.ehr.grossRev;
      document.getElementById("ehr-bucket-a").value = appState.ehr.bucketA;
      document.getElementById("ehr-bucket-b").value = appState.ehr.bucketB;
      document.getElementById("ehr-bucket-c").value = appState.ehr.bucketC;
      document.getElementById("ehr-bucket-d").value = appState.ehr.bucketD;
      for (let i = 1; i <= 5; i++) {{
        document.getElementById("gate-score-" + i).value = appState.ehr.gates[i - 1] || 3;
      }}

      document.getElementById("blk1-done").checked = !!appState.planner.blk1Done;
      document.getElementById("blk1-text").value = appState.planner.blk1Text || "";
      document.getElementById("blk2-done").checked = !!appState.planner.blk2Done;
      document.getElementById("blk2-text").value = appState.planner.blk2Text || "";
      document.getElementById("blk3-done").checked = !!appState.planner.blk3Done;
      document.getElementById("blk3-text").value = appState.planner.blk3Text || "";
      document.getElementById("blk-parking-lot").value = appState.planner.parkingLot || "";

      // Module 2
      document.getElementById("bcr-hourly-rate").value = appState.bcr.hourlyRate;
      document.getElementById("bcr-complexity").value = String(appState.bcr.complexity);
      document.getElementById("bcr-risk").value = String(appState.bcr.risk);
      document.getElementById("bcr-passthrough").value = appState.bcr.passthrough;
      document.getElementById("bcr-milestone-mode").value = appState.bcr.milestoneMode;
      document.getElementById("bcr-client-name").value = appState.bcr.clientName;
      document.getElementById("bcr-requested-budget").value = appState.bcr.requestedBudget;

      // Module 4
      document.getElementById("ceo-target-rev").value = appState.ceo.targetRev;
      document.getElementById("ceo-weekly-cap").value = appState.ceo.weeklyCap;
      document.getElementById("ceo-retainer-base").value = appState.ceo.retainerBase;
      document.getElementById("ceo-pipeline-weighted").value = appState.ceo.pipelineWeighted;
    }}

    function switchModuleTab(tabId) {{
      appState.activeTab = tabId;
      document.querySelectorAll(".module-panel").forEach(p => p.classList.remove("active"));
      const target = document.getElementById(tabId);
      if (target) target.classList.add("active");

      document.querySelectorAll(".module-tab-btn").forEach(b => {{
        b.classList.toggle("active", b.getAttribute("data-tab") === tabId);
      }});

      updateProGateBannerVisibility();
      saveAppState();
    }}

    function updateProGateBannerVisibility() {{
      const banner = document.getElementById("pro-gate-banner");
      const isProTab = appState.activeTab !== "tab-ehr-audit";
      if (appState.editionMode === "free" && isProTab) {{
        banner.classList.add("visible");
      }} else {{
        banner.classList.remove("visible");
      }}
    }}

    function handleCurrencyChange(val) {{
      appState.currency = val;
      recalcEhrModule();
      recalcBcrModule();
      recalcCeoModule();
      saveAppState();
      showToast("Currency updated to " + val);
    }}

    function handleEditionModeChange(mode) {{
      appState.editionMode = mode;
      updateProGateBannerVisibility();
      saveAppState();
      showToast(mode === "pro" ? "Complete Pro OS Mode Active" : "Tier 0 Free Diagnostic Mode Active");
    }}

    function openProActivationModal() {{
      document.getElementById("pro-activation-modal").classList.add("open");
    }}

    function closeProActivationModal() {{
      document.getElementById("pro-activation-modal").classList.remove("open");
    }}

    function verifyAndActivateProCode() {{
      const code = (document.getElementById("license-code-input").value || "").trim().toUpperCase();
      if (code.length >= 4) {{
        instantActivateProMode();
        closeProActivationModal();
      }} else {{
        showToast("Please enter access code FREELANCER-OS-PRO-2026");
      }}
    }}

    function instantActivateProMode() {{
      appState.editionMode = "pro";
      document.getElementById("edition-mode-toggle").value = "pro";
      updateProGateBannerVisibility();
      saveAppState();
      showToast("Complete Pro & Living OS Mode Activated!");
    }}

    /* ====================================================================== */
    /* MODULE 1 CALCULATIONS: 7-DAY EHR LEAK AUDIT & 5-STAGE SCORECARD        */
    /* ====================================================================== */
    function recalcEhrModule() {{
      appState.ehr.niche = document.getElementById("ehr-niche").value;
      appState.ehr.periodMode = document.getElementById("ehr-period-mode").value;
      appState.ehr.targetRate = Math.max(1, parseFloat(document.getElementById("ehr-target-rate").value) || 75);
      appState.ehr.grossRev = Math.max(0, parseFloat(document.getElementById("ehr-gross-rev").value) || 0);
      appState.ehr.bucketA = Math.max(0, parseFloat(document.getElementById("ehr-bucket-a").value) || 0);
      appState.ehr.bucketB = Math.max(0, parseFloat(document.getElementById("ehr-bucket-b").value) || 0);
      appState.ehr.bucketC = Math.max(0, parseFloat(document.getElementById("ehr-bucket-c").value) || 0);
      appState.ehr.bucketD = Math.max(0, parseFloat(document.getElementById("ehr-bucket-d").value) || 0);

      document.getElementById("lbl-gross-rev").textContent =
        appState.ehr.periodMode === "monthly" ? "Gross Revenue Billed (Monthly)" : "Gross Revenue Billed (Weekly)";

      const weeklyRev = appState.ehr.periodMode === "monthly" ? appState.ehr.grossRev / 4.0 : appState.ehr.grossRev;
      const totalHours = appState.ehr.bucketA + appState.ehr.bucketB + appState.ehr.bucketC + appState.ehr.bucketD;
      const safeTotal = totalHours > 0 ? totalHours : 1;

      const trueEhr = weeklyRev / safeTotal;
      const utilizationPct = (appState.ehr.bucketA / safeTotal) * 100;
      const unbilledHours = appState.ehr.bucketB + appState.ehr.bucketC + appState.ehr.bucketD;
      const weeklyLeak = unbilledHours * appState.ehr.targetRate;
      const monthlyLeak = weeklyLeak * 4.33;
      const annualLeak = weeklyLeak * 48;
      const erosionPct = ((trueEhr - appState.ehr.targetRate) / appState.ehr.targetRate) * 100;

      document.getElementById("out-true-ehr").textContent = fmtMoney(trueEhr, 2) + "/hr";
      document.getElementById("out-ehr-collapse").textContent =
        erosionPct < 0
          ? `Rate Erosion: ${{erosionPct.toFixed(1)}}% vs ${{fmtMoney(appState.ehr.targetRate)}}/hr target`
          : `Surplus: +${{erosionPct.toFixed(1)}}% above ${{fmtMoney(appState.ehr.targetRate)}}/hr target`;

      document.getElementById("out-utilization-pct").textContent = utilizationPct.toFixed(1) + "%";
      document.getElementById("out-total-hours-meta").textContent =
        `${{appState.ehr.bucketA.toFixed(1)}} billable hrs / ${{totalHours.toFixed(1)}} total real hrs (Target: >=65%)`;

      document.getElementById("out-monthly-leak").textContent = fmtMoney(monthlyLeak, 0) + "/mo";
      document.getElementById("out-weekly-leak-meta").textContent =
        `${{unbilledHours.toFixed(1)}} non-billable hrs/wk (${{fmtMoney(weeklyLeak, 0)}}/wk opportunity cost)`;
      document.getElementById("out-annual-leak").textContent = fmtMoney(annualLeak, 0) + "/yr";

      // Update Stacked Bar
      const pctA = (appState.ehr.bucketA / safeTotal) * 100;
      const pctB = (appState.ehr.bucketB / safeTotal) * 100;
      const pctC = (appState.ehr.bucketC / safeTotal) * 100;
      const pctD = (appState.ehr.bucketD / safeTotal) * 100;

      const segA = document.getElementById("bar-seg-a");
      const segB = document.getElementById("bar-seg-b");
      const segC = document.getElementById("bar-seg-c");
      const segD = document.getElementById("bar-seg-d");
      segA.style.width = pctA.toFixed(1) + "%";
      segA.textContent = pctA >= 8 ? `A: ${{pctA.toFixed(0)}}%` : "";
      segB.style.width = pctB.toFixed(1) + "%";
      segB.textContent = pctB >= 8 ? `B: ${{pctB.toFixed(0)}}%` : "";
      segC.style.width = pctC.toFixed(1) + "%";
      segC.textContent = pctC >= 8 ? `C: ${{pctC.toFixed(0)}}%` : "";
      segD.style.width = pctD.toFixed(1) + "%";
      segD.textContent = pctD >= 8 ? `D: ${{pctD.toFixed(0)}}%` : "";

      document.getElementById("out-bar-summary").textContent = `Total Logged: ${{totalHours.toFixed(1)}} hrs/week`;
      document.getElementById("leg-a").textContent = appState.ehr.bucketA.toFixed(1) + "h";
      document.getElementById("leg-b").textContent = appState.ehr.bucketB.toFixed(1) + "h";
      document.getElementById("leg-c").textContent = appState.ehr.bucketC.toFixed(1) + "h";
      document.getElementById("leg-d").textContent = appState.ehr.bucketD.toFixed(1) + "h";

      // 5-Stage Scorecard
      const gateSpecs = [
        {{ num: 1, name: "Stage 01: Attract & Filter", fix: "Install 3-Tier Offer Matrix (Ch 2, Prompt 2.2) & P.A.C.E. Lead Scorer (Ch 3, Prompt 3.2 / Script 1)." }},
        {{ num: 2, name: "Stage 02: Scope & Price", fix: "Deploy 10-Min B.R.I.E.F. Proposals (Prompt 3.3) & B.C.R. Pricing Calculator (Module 2 / Prompt 4.2)." }},
        {{ num: 3, name: "Stage 03: Onboard & Align", fix: "Enforce 48-Hr Pre-Flight Asset Gate & Day-for-Day Timeline Shift Rule (Ch 5, Prompt 5.1 & Script 5)." }},
        {{ num: 4, name: "Stage 04: Execute & Defend", fix: "Run 20/60/20 Sandwich Execution (Ch 6) & P.V.P. Change Order Quotes (Ch 7, Prompt 7.2 & Script 7)." }},
        {{ num: 5, name: "Stage 05: Offboard & Scale", fix: "Deploy Offboard-to-Retainer Bridge (Ch 9, Prompt 9.4 & Script 11) & Friday CEO Cadence (Module 4)." }}
      ];

      let totalGateScore = 0;
      const scored = gateSpecs.map((g, idx) => {{
        const val = parseInt(document.getElementById("gate-score-" + g.num).value, 10) || 3;
        appState.ehr.gates[idx] = val;
        document.getElementById("val-gate-" + g.num).textContent = val + " / 5";
        totalGateScore += val;
        return {{ ...g, score: val }};
      }});

      document.getElementById("out-gate-total-score").textContent = `Score: ${{totalGateScore}} / 25`;
      scored.sort((a, b) => a.score - b.score);
      const low1 = scored[0];
      const low2 = scored[1];

      document.getElementById("out-bottleneck-prescription").innerHTML =
        `<strong>Priority Circuit-Breaker Prescription (Lowest Gates):</strong><br/>` +
        `1. <strong>${{low1.name}} (Score ${{low1.score}}/5):</strong> ${{low1.fix}}<br/>` +
        `2. <strong>${{low2.name}} (Score ${{low2.score}}/5):</strong> ${{low2.fix}}`;

      saveAppState();
    }}

    function generatePreFilledPrompt11() {{
      const weeklyRev = appState.ehr.periodMode === "monthly" ? appState.ehr.grossRev / 4.0 : appState.ehr.grossRev;
      appState.vault.selectedId = "1.1";
      appState.vault.customVars["1.1"] = {{
        "[E.G., UX/UI DESIGN & WEBFLOW DEVELOPMENT]": appState.ehr.niche,
        "[E.G., 65.00]": appState.ehr.targetRate.toFixed(2),
        "[E.G., 1000.00]": weeklyRev.toFixed(2),
        "[PASTE YOUR RAW 7-DAY CALENDAR NOTES, TOGGL EXPORT, OR ROUGH HOUR LIST HERE — E.G.:\\nMon: 3.5h client wireframe design, 1.5h Slack back-and-forth on unapproved copy changes, 2h writing custom proposal for Lead X, 1h email sorting.\\nTue: 4h building Webflow components, 2h chasing Client Y for missing DNS/brand logins, 1.5h unbilled revision round 4...]":
          `7-Day Audited Bucket Summary:\\n- Bucket A (Core Billable Craft): ${{appState.ehr.bucketA}} hours\\n- Bucket B (Unbilled Client Friction & Scope Creep): ${{appState.ehr.bucketB}} hours\\n- Bucket C (Sales, Proposals & Discovery Calls): ${{appState.ehr.bucketC}} hours\\n- Bucket D (Internal Admin & Context-Switching Drag): ${{appState.ehr.bucketD}} hours`
      }};
      switchModuleTab("tab-prompt-vault");
      renderPromptVault();
      showToast("Prompt 1.1 pre-filled with your 7-Day Audit numbers!");
    }}

    function copyDailyScheduleMarkdown() {{
      const md =
        `# Daily 3-Block Priority Plan (${{new Date().toISOString().slice(0,10)}})\\n\\n` +
        `- [${{appState.planner.blk1Done ? 'x' : ' '}}] **Block 1 (90-Min Maker Block — Zero Inbox):** ${{appState.planner.blk1Text}}\\n` +
        `- [${{appState.planner.blk2Done ? 'x' : ' '}}] **Block 2 (30-Min AI Admin Sprint):** ${{appState.planner.blk2Text}}\\n` +
        `- [${{appState.planner.blk3Done ? 'x' : ' '}}] **Block 3 (90-Min Delivery & Pipeline):** ${{appState.planner.blk3Text}}\\n` +
        `- **Deferred Parking Lot:** ${{appState.planner.parkingLot}}\\n`;
      navigator.clipboard.writeText(md);
      showToast("Daily 3-Block Schedule copied as Markdown!");
    }}

    /* ====================================================================== */
    /* MODULE 2 CALCULATIONS: B.C.R. WBS & 3-TIER PROPOSAL PRICING ENGINE     */
    /* ====================================================================== */
    function renderWbsTable() {{
      const tbody = document.getElementById("wbs-tbody");
      tbody.innerHTML = "";
      appState.bcr.wbs.forEach((row, idx) => {{
        const weighted = row.baseHrs * (1 + (row.bufferPct / 100));
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><input type="text" class="form-input" value="${{row.name.replace(/"/g, '&quot;')}}" oninput="updateWbsRow(${{idx}}, 'name', this.value)" /></td>
          <td><input type="number" class="form-input" value="${{row.baseHrs}}" min="0.5" step="0.5" oninput="updateWbsRow(${{idx}}, 'baseHrs', this.value)" /></td>
          <td><input type="number" class="form-input" value="${{row.bufferPct}}" min="0" max="100" step="5" oninput="updateWbsRow(${{idx}}, 'bufferPct', this.value)" /></td>
          <td><strong style="font-family:var(--font-mono);">${{weighted.toFixed(1)}} hrs</strong></td>
          <td class="no-print"><button type="button" class="btn btn-danger" onclick="removeWbsRow(${{idx}})">✕</button></td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function updateWbsRow(idx, field, val) {{
      if (field === "name") {{
        appState.bcr.wbs[idx].name = val;
      }} else {{
        appState.bcr.wbs[idx][field] = Math.max(0, parseFloat(val) || 0);
      }}
      renderWbsTable();
      recalcBcrModule();
    }}

    function addWbsRow() {{
      appState.bcr.wbs.push({{ name: "New Project Deliverable / Milestone", baseHrs: 4.0, bufferPct: 20 }});
      renderWbsTable();
      recalcBcrModule();
    }}

    function removeWbsRow(idx) {{
      if (appState.bcr.wbs.length <= 1) {{
        showToast("At least 1 deliverable row is required.");
        return;
      }}
      appState.bcr.wbs.splice(idx, 1);
      renderWbsTable();
      recalcBcrModule();
    }}

    function roundTo50(num) {{
      return Math.round(num / 50) * 50;
    }}

    function formatMilestones(totalFee, mode) {{
      if (mode === "40-30-30") {{
        const m1 = Math.round(totalFee * 0.40);
        const m2 = Math.round(totalFee * 0.30);
        const m3 = totalFee - m1 - m2;
        return `40% Kickoff: ${{fmtMoney(m1)}} • 30% Day 15: ${{fmtMoney(m2)}} • 30% Day 30: ${{fmtMoney(m3)}}`;
      }} else if (mode === "50-50") {{
        const m1 = Math.round(totalFee * 0.50);
        const m2 = totalFee - m1;
        return `50% Deposit: ${{fmtMoney(m1)}} • 50% Pre-Transfer: ${{fmtMoney(m2)}}`;
      }} else {{
        const m1 = Math.round(totalFee * 0.50);
        const m2 = Math.round(totalFee * 0.25);
        const m3 = totalFee - m1 - m2;
        return `50% Deposit: ${{fmtMoney(m1)}} • 25% Mid: ${{fmtMoney(m2)}} • 25% Final: ${{fmtMoney(m3)}}`;
      }}
    }}

    function recalcBcrModule() {{
      appState.bcr.hourlyRate = Math.max(10, parseFloat(document.getElementById("bcr-hourly-rate").value) || 85);
      appState.bcr.complexity = parseFloat(document.getElementById("bcr-complexity").value) || 1.15;
      appState.bcr.risk = parseFloat(document.getElementById("bcr-risk").value) || 0.20;
      appState.bcr.passthrough = Math.max(0, parseFloat(document.getElementById("bcr-passthrough").value) || 0);
      appState.bcr.milestoneMode = document.getElementById("bcr-milestone-mode").value;
      appState.bcr.clientName = document.getElementById("bcr-client-name").value || "Client";
      appState.bcr.requestedBudget = Math.max(0, parseFloat(document.getElementById("bcr-requested-budget").value) || 0);

      let weightedBaseHrs = 0;
      appState.bcr.wbs.forEach(r => {{
        weightedBaseHrs += r.baseHrs * (1 + (r.bufferPct / 100));
      }});

      const bcrAdjustedHrs = weightedBaseHrs * appState.bcr.complexity * (1 + appState.bcr.risk);
      const baseBcrPrice = (bcrAdjustedHrs * appState.bcr.hourlyRate) + appState.bcr.passthrough;

      const tier1Price = Math.max(250, roundTo50(baseBcrPrice));
      const tier2Price = Math.max(350, roundTo50(baseBcrPrice * 1.35));
      const tier3Price = Math.max(500, roundTo50(baseBcrPrice * 1.85));
      const walkAwayFloor = roundTo50(tier2Price * 0.85);

      document.getElementById("out-bcr-formula-trace").textContent =
        `Weighted Base: ${{weightedBaseHrs.toFixed(1)}} hrs • B.C.R. Adjusted Equivalent: ${{bcrAdjustedHrs.toFixed(1)}} hrs • Hard Walk-Away Minimum Floor: ${{fmtMoney(walkAwayFloor)}}`;

      document.getElementById("out-tier1-price").textContent = fmtMoney(tier1Price);
      document.getElementById("out-tier2-price").textContent = fmtMoney(tier2Price);
      document.getElementById("out-tier3-price").textContent = fmtMoney(tier3Price);

      document.getElementById("out-tier1-milestones").textContent = formatMilestones(tier1Price, appState.bcr.milestoneMode);
      document.getElementById("out-tier2-milestones").textContent = formatMilestones(tier2Price, appState.bcr.milestoneMode);
      document.getElementById("out-tier3-milestones").textContent = formatMilestones(tier3Price, appState.bcr.milestoneMode);

      // Discount Defense Counter-Offer Math
      const gap = tier2Price - appState.bcr.requestedBudget;
      const gapPct = tier2Price > 0 ? (gap / tier2Price) * 100 : 0;
      const badgeEl = document.getElementById("out-discount-gap-badge");

      const lastDeliverable = appState.bcr.wbs[appState.bcr.wbs.length - 1]?.name || "Secondary Module";
      const secondLastDeliverable = appState.bcr.wbs.length > 2 ? appState.bcr.wbs[appState.bcr.wbs.length - 2].name : "Extended QA & Polish";

      if (gap <= 0) {{
        badgeEl.className = "badge green";
        badgeEl.textContent = `Budget Aligned: Prospect budget meets or exceeds Option 2 (${{fmtMoney(tier2Price)}})`;
      }} else {{
        badgeEl.className = "badge amber";
        badgeEl.textContent = `Budget Gap: -${{gapPct.toFixed(1)}}% (${{fmtMoney(gap)}}) below Option 2 Anchor`;
      }}

      const counterScript =
        `Subject: Re: ${{appState.bcr.clientName}} Proposal — Adjusting scope to hit your ${{fmtMoney(appState.bcr.requestedBudget)}} budget\\n\\n` +
        `Hi ${{appState.bcr.clientName.split(" ")[0]}},\\n\\n` +
        `Thrilled to hear the team wants to move forward together! Because our pricing is calculated directly from the ${{bcrAdjustedHrs.toFixed(1)}} engineering and QA hours required to ship the full Option 2 scope (${{fmtMoney(tier2Price)}}), we keep our rates standardized across all clients and do not offer flat-percentage discounts on the same workload.\\n\\n` +
        `However, we can hit your ${{fmtMoney(appState.bcr.requestedBudget)}} target investment cleanly by adjusting the sprint scope so we protect 100% of your core launch quality:\\n\\n` +
        `• Path A (Scope-Adjusted Sprint at ${{fmtMoney(appState.bcr.requestedBudget)}}): We deliver the core high-impact foundation on schedule, cap revisions at 1 consolidated SPOC round, and move [${{secondLastDeliverable}}] + [${{lastDeliverable}}] into a Phase 2 backlog for next quarter.\\n` +
        `• Path B (Full Option 2 Scope at ${{fmtMoney(tier2Price)}} Across 3 Date-Locked Milestones): We keep 100% of deliverables and split cashflow into ${{formatMilestones(tier2Price, '40-30-30')}}.\\n` +
        `• Path C (Option 1 Essential Baseline at ${{fmtMoney(tier1Price)}}): Start with our streamlined core package today.\\n\\n` +
        `Which path feels best for the team—Path A (${{fmtMoney(appState.bcr.requestedBudget)}} Lean Scope) or Path B (${{fmtMoney(tier2Price)}} Full Scope with milestone split)?`;

      document.getElementById("out-discount-counter-script").value = counterScript;
      saveAppState();
    }}

    function copyBriefProposalSummary() {{
      const t1 = document.getElementById("out-tier1-price").textContent;
      const t2 = document.getElementById("out-tier2-price").textContent;
      const t3 = document.getElementById("out-tier3-price").textContent;
      const wbsList = appState.bcr.wbs.map(r => `- ${{r.name}} (${{r.baseHrs}}h base)`).join("\\n");
      const text =
        `# B.R.I.E.F. 3-Option Commercial Proposal Summary — ${{appState.bcr.clientName}}\\n\\n` +
        `## Core WBS Deliverables\\n${{wbsList}}\\n\\n` +
        `## 3-Tier Productized Investment Options\\n` +
        `- **Option 1 — Essential Baseline (${{t1}}):** Core outcome, 1 revision round, standard turnaround.\\n` +
        `- **Option 2 — Core Transformation (${{t2}} — Recommended):** Full WBS scope, 2 revision rounds, 14-day post-launch support + Maintenance SOP.\\n` +
        `- **Option 3 — Turnkey & Retainer Partner (${{t3}}):** Priority timeline, 3 revision rounds, 30-day optimization sprint + live workshop.\\n`;
      navigator.clipboard.writeText(text);
      showToast("3-Tier B.R.I.E.F. Proposal Summary copied!");
    }}

    function copyDiscountCounterEmail() {{
      const txt = document.getElementById("out-discount-counter-script").value;
      navigator.clipboard.writeText(txt);
      showToast("Scope-Down Counter-Offer Email copied!");
    }}

    /* ====================================================================== */
    /* MODULE 3: INTERACTIVE 50-PROMPT & 12-SCRIPT STUDIO BUILDER             */
    /* ====================================================================== */
    function setStageFilter(stage, btnEl) {{
      appState.vault.stageFilter = stage;
      document.querySelectorAll("#stage-filter-pills .filter-pill").forEach(b => b.classList.remove("active"));
      if (btnEl) btnEl.classList.add("active");
      filterPromptVault();
    }}

    function filterPromptVault() {{
      appState.vault.searchQuery = (document.getElementById("prompt-search").value || "").toLowerCase().trim();
      appState.vault.chapterFilter = document.getElementById("prompt-chapter-select").value;
      renderPromptVault();
    }}

    function renderPromptVault() {{
      const listEl = document.getElementById("vault-item-list");
      listEl.innerHTML = "";

      const filtered = ALL_VAULT_ITEMS.filter(item => {{
        if (appState.vault.stageFilter !== "all" && item.stage !== appState.vault.stageFilter) return false;
        if (appState.vault.chapterFilter !== "all" && String(item.chapter) !== String(appState.vault.chapterFilter)) return false;
        if (appState.vault.searchQuery) {{
          const hay = (item.label + " " + item.title + " " + item.objective + " " + item.template).toLowerCase();
          if (!hay.includes(appState.vault.searchQuery)) return false;
        }}
        return true;
      }});

      document.getElementById("vault-counter-badge").textContent = `Showing ${{filtered.length}} / ${{ALL_VAULT_ITEMS.length}} Assets`;

      filtered.forEach(item => {{
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "prompt-item-btn" + (item.id === appState.vault.selectedId ? " active" : "");
        btn.onclick = () => selectVaultItem(item.id);
        btn.innerHTML = `
          <div class="prompt-item-header">
            <span>${{item.label}}</span>
            <span style="color:var(--muted); font-weight:600;">${{item.type === 'script' ? 'Emergency Script' : 'Ch ' + item.chapter}}</span>
          </div>
          <div class="prompt-item-title">${{item.title}}</div>
        `;
        listEl.appendChild(btn);
      }});

      renderActiveVaultItem();
    }}

    function selectVaultItem(id) {{
      appState.vault.selectedId = id;
      renderPromptVault();
      saveAppState();
    }}

    function openPromptInVault(id) {{
      appState.vault.selectedId = id;
      appState.vault.stageFilter = "all";
      appState.vault.chapterFilter = "all";
      appState.vault.searchQuery = "";
      document.getElementById("prompt-search").value = "";
      document.getElementById("prompt-chapter-select").value = "all";
      switchModuleTab("tab-prompt-vault");
      renderPromptVault();
    }}

    function renderActiveVaultItem() {{
      const item = ALL_VAULT_ITEMS.find(x => x.id === appState.vault.selectedId) || ALL_VAULT_ITEMS[0];
      if (!item) return;

      document.getElementById("active-item-id-badge").textContent = item.label;
      document.getElementById("active-item-stage-badge").textContent = item.stage;
      document.getElementById("active-item-title").textContent = item.title;
      document.getElementById("active-item-objective").textContent = item.objective;
      document.getElementById("active-item-when").textContent = item.when_to_run;
      document.getElementById("active-item-verification").textContent = item.verification;

      const vars = item.variables || [];
      document.getElementById("active-vars-count").textContent = `${{vars.length}} customizable variable${{vars.length === 1 ? '' : 's'}}`;

      const formEl = document.getElementById("dynamic-variables-form");
      formEl.innerHTML = "";
      if (!appState.vault.customVars[item.id]) {{
        appState.vault.customVars[item.id] = {{}};
      }}
      const savedMap = appState.vault.customVars[item.id];

      vars.forEach((vToken) => {{
        const cleanLabel = vToken.replace(/^\\[|\\]$/g, "");
        const shortLabel = cleanLabel.length > 58 ? cleanLabel.slice(0, 55) + "..." : cleanLabel;
        const wrap = document.createElement("div");
        wrap.className = "form-group";
        wrap.style.marginBottom = "4px";

        const lbl = document.createElement("label");
        lbl.className = "form-label";
        lbl.style.fontSize = "11.5px";
        lbl.textContent = shortLabel;

        const inp = document.createElement("input");
        inp.type = "text";
        inp.className = "form-input";
        inp.placeholder = vToken;
        inp.value = savedMap[vToken] || "";
        inp.oninput = (e) => {{
          appState.vault.customVars[item.id][vToken] = e.target.value;
          updateAssembledPromptOutput(item);
          saveAppState();
        }};

        wrap.appendChild(lbl);
        wrap.appendChild(inp);
        formEl.appendChild(wrap);
      }});

      updateAssembledPromptOutput(item);
    }}

    function updateAssembledPromptOutput(item) {{
      let assembled = item.template;
      const savedMap = appState.vault.customVars[item.id] || {{}};
      Object.keys(savedMap).forEach(k => {{
        const val = savedMap[k];
        if (val && val.trim() !== "") {{
          assembled = assembled.split(k).join(val.trim());
        }}
      }});
      document.getElementById("assembled-prompt-output").textContent = assembled;
    }}

    function resetActivePromptVariables() {{
      const id = appState.vault.selectedId;
      appState.vault.customVars[id] = {{}};
      renderActiveVaultItem();
      saveAppState();
      showToast("Variables reset to default template placeholders.");
    }}

    function copyAssembledPrompt() {{
      const txt = document.getElementById("assembled-prompt-output").textContent;
      navigator.clipboard.writeText(txt);
      showToast("Copied assembled workflow to clipboard!");
    }}

    function downloadActivePromptMd() {{
      const item = ALL_VAULT_ITEMS.find(x => x.id === appState.vault.selectedId) || ALL_VAULT_ITEMS[0];
      const txt = document.getElementById("assembled-prompt-output").textContent;
      const fence = "```";
      const md =
        `# ${{item.label}}: ${{item.title}}\\n\\n` +
        `- **Stage:** ${{item.stage}}\\n` +
        `- **Operational Objective:** ${{item.objective}}\\n` +
        `- **When to Run:** ${{item.when_to_run}}\\n\\n` +
        `${{fence}}text\\n${{txt}}\\n${{fence}}\\n\\n` +
        `**Verification Rule:** ${{item.verification}}\\n`;
      const blob = new Blob([md], {{ type: "text/markdown;charset=utf-8" }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${{item.label.toLowerCase().replace(/\\s+/g, '-')}}.md`;
      a.click();
      URL.revokeObjectURL(url);
      showToast("Downloaded " + a.download);
    }}

    /* ====================================================================== */
    /* MODULE 4: FRIDAY CEO SCORECARD & 80/20 CLIENT ROSTER                   */
    /* ====================================================================== */
    function renderClientRoster() {{
      const tbody = document.getElementById("client-roster-tbody");
      tbody.innerHTML = "";
      const targetRate = appState.ehr.targetRate || 75;

      let totalRev = 0;
      appState.ceo.clients.forEach(c => totalRev += (parseFloat(c.revenue) || 0));
      const safeTotalRev = totalRev > 0 ? totalRev : 1;

      // Determine bottom 25% EHR threshold
      const ehrs = appState.ceo.clients.map(c => (parseFloat(c.revenue) || 0) / Math.max(1, parseFloat(c.hours) || 1)).sort((a,b) => a - b);
      const bottomQuartileThreshold = ehrs.length > 0 ? ehrs[Math.floor(ehrs.length * 0.25)] : 0;

      appState.ceo.clients.forEach((client, idx) => {{
        const rev = parseFloat(client.revenue) || 0;
        const hrs = Math.max(0.5, parseFloat(client.hours) || 1);
        const ehr = rev / hrs;
        const sharePct = (rev / safeTotalRev) * 100;
        const friction = parseInt(client.friction, 10) || 1;

        let actionBadge = "";
        if (friction >= 4 || ehr <= bottomQuartileThreshold) {{
          actionBadge = `<span class="badge red">🔴 Prune / Replace Next Qtr</span>`;
        }} else if (ehr < targetRate && friction <= 3) {{
          actionBadge = `<span class="badge amber">🟡 Re-Price +20% / Cap Scope</span>`;
        }} else {{
          actionBadge = `<span class="badge green">🟢 Retain &amp; Expand Retainer</span>`;
        }}

        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><input type="text" class="form-input" value="${{client.name.replace(/"/g, '&quot;')}}" oninput="updateClientRow(${{idx}}, 'name', this.value)" /></td>
          <td><input type="number" class="form-input" value="${{rev}}" min="0" step="50" oninput="updateClientRow(${{idx}}, 'revenue', this.value)" /></td>
          <td><input type="number" class="form-input" value="${{hrs}}" min="0.5" step="0.5" oninput="updateClientRow(${{idx}}, 'hours', this.value)" /></td>
          <td><strong style="font-family:var(--font-mono);">${{fmtMoney(ehr, 2)}}/hr</strong></td>
          <td>
            <select class="form-select" onchange="updateClientRow(${{idx}}, 'friction', this.value)">
              <option value="1" ${{friction === 1 ? 'selected' : ''}}>1 — Zero Friction</option>
              <option value="2" ${{friction === 2 ? 'selected' : ''}}>2 — Low Friction</option>
              <option value="3" ${{friction === 3 ? 'selected' : ''}}>3 — Moderate</option>
              <option value="4" ${{friction === 4 ? 'selected' : ''}}>4 — High Drag</option>
              <option value="5" ${{friction === 5 ? 'selected' : ''}}>5 — Severe Chaos</option>
            </select>
          </td>
          <td>${{sharePct.toFixed(1)}}%</td>
          <td>${{actionBadge}}</td>
          <td class="no-print"><button type="button" class="btn btn-danger" onclick="removeClientRow(${{idx}})">✕</button></td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function updateClientRow(idx, field, val) {{
      if (field === "name") {{
        appState.ceo.clients[idx].name = val;
      }} else if (field === "friction") {{
        appState.ceo.clients[idx].friction = parseInt(val, 10) || 1;
      }} else {{
        appState.ceo.clients[idx][field] = Math.max(0, parseFloat(val) || 0);
      }}
      renderClientRoster();
      recalcCeoModule();
    }}

    function addClientRow() {{
      appState.ceo.clients.push({{ name: "New Retainer / Sprint Client", revenue: 1800, hours: 16.0, friction: 2 }});
      renderClientRoster();
      recalcCeoModule();
    }}

    function removeClientRow(idx) {{
      if (appState.ceo.clients.length <= 1) {{
        showToast("Keep at least 1 active client in roster.");
        return;
      }}
      appState.ceo.clients.splice(idx, 1);
      renderClientRoster();
      recalcCeoModule();
    }}

    function recalcCeoModule() {{
      appState.ceo.targetRev = Math.max(500, parseFloat(document.getElementById("ceo-target-rev").value) || 8000);
      appState.ceo.weeklyCap = Math.max(5, parseFloat(document.getElementById("ceo-weekly-cap").value) || 30);
      appState.ceo.retainerBase = Math.max(0, parseFloat(document.getElementById("ceo-retainer-base").value) || 0);
      appState.ceo.pipelineWeighted = Math.max(0, parseFloat(document.getElementById("ceo-pipeline-weighted").value) || 0);

      let totalMonthlyRev = 0;
      let totalMonthlyHrs = 0;
      appState.ceo.clients.forEach(c => {{
        totalMonthlyRev += parseFloat(c.revenue) || 0;
        totalMonthlyHrs += parseFloat(c.hours) || 0;
      }});

      const blendedEhr = totalMonthlyRev / Math.max(1, totalMonthlyHrs);
      const weeklyBookedHrs = totalMonthlyHrs / 4.0;
      const capUtilizationPct = (weeklyBookedHrs / appState.ceo.weeklyCap) * 100;

      document.getElementById("ceo-kpi-blended-ehr").textContent = fmtMoney(blendedEhr, 2) + "/hr";
      document.getElementById("ceo-kpi-roster-summary").textContent =
        `${{fmtMoney(totalMonthlyRev, 0)}}/mo across ${{totalMonthlyHrs.toFixed(1)}} real hrs`;

      document.getElementById("ceo-kpi-capacity-pct").textContent = capUtilizationPct.toFixed(1) + "%";
      document.getElementById("ceo-kpi-capacity-meta").textContent =
        `${{weeklyBookedHrs.toFixed(1)}} booked hrs/wk vs ${{appState.ceo.weeklyCap}}h ceiling`;

      const retainerPct = (appState.ceo.retainerBase / appState.ceo.targetRev) * 100;
      document.getElementById("ceo-kpi-retainer-floor").textContent = fmtMoney(appState.ceo.retainerBase, 0) + "/mo";
      document.getElementById("ceo-kpi-retainer-pct").textContent =
        `${{retainerPct.toFixed(1)}}% of ${{fmtMoney(appState.ceo.targetRev, 0)}}/mo target locked`;

      const projected30Day = appState.ceo.retainerBase + (appState.ceo.pipelineWeighted * 0.5);
      const gap = projected30Day - appState.ceo.targetRev;
      document.getElementById("ceo-kpi-pipeline-gap").textContent =
        (gap >= 0 ? "+" : "") + fmtMoney(gap, 0);
      document.getElementById("ceo-kpi-pipeline-action").textContent =
        gap >= 0
          ? "Pipeline Healthy: Focus on Prompt 9.4 Retainer Expansion"
          : "Pipeline Gap Alert: Run Prompt 3.5 & Prompt 9.5 Warm Outreach";

      // 85% Capacity Rate-Raise Trigger Banner
      const banner = document.getElementById("capacity-rate-raise-banner");
      if (capUtilizationPct >= 85) {{
        banner.classList.add("active");
      }} else {{
        banner.classList.remove("active");
      }}

      renderRetroLog();
      saveAppState();
    }}

    function renderRetroLog() {{
      const tbody = document.getElementById("ceo-retro-tbody");
      tbody.innerHTML = "";
      appState.ceo.retroLog.forEach(entry => {{
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><strong>${{entry.date}}</strong></td>
          <td>${{fmtMoney(entry.revenue, 0)}}</td>
          <td>${{Number(entry.hours).toFixed(1)}} hrs</td>
          <td><strong style="font-family:var(--font-mono); color:var(--secondary);">${{fmtMoney(entry.ehr, 2)}}/hr</strong></td>
          <td><span class="badge blue">${{entry.gate}}</span></td>
          <td>${{entry.fix}}</td>
          <td>${{entry.mondayP1}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function appendFridayRetroSnapshot() {{
      const weeklyRev = appState.ehr.periodMode === "monthly" ? appState.ehr.grossRev / 4.0 : appState.ehr.grossRev;
      const totalHrs = appState.ehr.bucketA + appState.ehr.bucketB + appState.ehr.bucketC + appState.ehr.bucketD;
      const ehr = weeklyRev / Math.max(1, totalHrs);
      const gate = document.getElementById("retro-failed-gate").value;
      const fix = document.getElementById("retro-system-fix").value || "Standardized workflow checklist";
      const mon = document.getElementById("retro-monday-p1").value || "Core client milestone";

      appState.ceo.retroLog.unshift({{
        date: new Date().toISOString().slice(0, 10),
        revenue: weeklyRev,
        hours: totalHrs,
        ehr: ehr,
        gate: gate,
        fix: fix,
        mondayP1: mon
      }});
      renderRetroLog();
      saveAppState();
      showToast("Friday CEO Snapshot logged!");
    }}

    function exportCeoLogCsv() {{
      const headers = ["Week Date", "Weekly Revenue", "Real Hours", "Realized EHR", "Bottleneck Gate", "System Upgrade Installed", "Monday Block-1 Priority"];
      const rows = appState.ceo.retroLog.map(r => [
        r.date,
        r.revenue,
        r.hours,
        Number(r.ehr).toFixed(2),
        `"${{(r.gate || '').replace(/"/g, '""')}}"`,
        `"${{(r.fix || '').replace(/"/g, '""')}}"`,
        `"${{(r.mondayP1 || '').replace(/"/g, '""')}}"`
      ]);
      const csv = [headers.join(","), ...rows.map(r => r.join(","))].join("\\n");
      const blob = new Blob([csv], {{ type: "text/csv;charset=utf-8" }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "freelancer-os-friday-ceo-log.csv";
      a.click();
      URL.revokeObjectURL(url);
      showToast("Exported CEO Log as CSV!");
    }}

    /* ====================================================================== */
    /* GLOBAL WORKSPACE EXPORT, IMPORT & MARCUS V. CASE-STUDY DEMO DATA       */
    /* ====================================================================== */
    function exportWorkspaceJson() {{
      saveAppState();
      const jsonStr = JSON.stringify(appState, null, 2);
      const blob = new Blob([jsonStr], {{ type: "application/json;charset=utf-8" }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "freelancer-os-workspace.json";
      a.click();
      URL.revokeObjectURL(url);
      showToast("Exported workspace backup to freelancer-os-workspace.json");
    }}

    function importWorkspaceJson(event) {{
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (e) => {{
        try {{
          const imported = JSON.parse(e.target.result);
          appState = Object.assign({{}}, appState, imported);
          syncInputsFromState();
          renderWbsTable();
          renderClientRoster();
          recalcEhrModule();
          recalcBcrModule();
          recalcCeoModule();
          renderPromptVault();
          showToast("Workspace restored from JSON backup!");
        }} catch (err) {{
          showToast("Invalid JSON workspace file.");
        }}
      }};
      reader.readAsText(file);
    }}

    function loadMarcusCaseStudyDemo() {{
      appState.ehr = {{
        niche: "Independent Brand & Webflow Specialist (Marcus V. Case Study)",
        periodMode: "weekly",
        targetRate: 85,
        grossRev: 1650,
        bucketA: 25.0,
        bucketB: 6.5,
        bucketC: 4.5,
        bucketD: 5.0,
        gates: [4, 4, 3, 2, 4]
      }};
      appState.bcr.hourlyRate = 95;
      appState.bcr.complexity = 1.15;
      appState.bcr.risk = 0.20;
      appState.bcr.clientName = "Verde Beverage Co. (Marcus Tan)";
      appState.bcr.requestedBudget = 3200;
      syncInputsFromState();
      renderWbsTable();
      renderClientRoster();
      recalcEhrModule();
      recalcBcrModule();
      recalcCeoModule();
      renderPromptVault();
      showToast("Loaded Marcus V. Case-Study Demo Data across all 4 modules!");
    }}

    window.addEventListener("DOMContentLoaded", () => {{
      loadAppState();
      syncInputsFromState();
      renderWbsTable();
      renderClientRoster();
      recalcEhrModule();
      recalcBcrModule();
      recalcCeoModule();
      renderPromptVault();
      updateProGateBannerVisibility();
    }});
  </script>
</body>
</html>
"""


def main() -> int:
    print("=" * 78)
    print("BUILDING SAAS-LITE INTERACTIVE WEB COMPANION APP (freelancer-os-app.html)")
    print("=" * 78)

    prompts = extract_all_prompts()
    scripts = extract_all_scripts()
    print(f"[Parser] Extracted {len(prompts)}/50 AI Workflow Prompts and {len(scripts)}/12 Emergency Client Scripts.")

    html_content = build_html_app(prompts, scripts)

    out_primary = BASE_DIR / "07-INTERACTIVE-TOOLS/freelancer-os-app.html"
    out_bundle = BASE_DIR / "09-EXPORTS/HYBRID-BUNDLE/freelancer-os-app.html"
    out_primary.parent.mkdir(parents=True, exist_ok=True)
    out_bundle.parent.mkdir(parents=True, exist_ok=True)

    out_primary.write_text(html_content, encoding="utf-8")
    shutil.copy2(out_primary, out_bundle)

    size_bytes = out_primary.stat().st_size
    print(f"[Output] Wrote {out_primary.relative_to(BASE_DIR)} ({size_bytes:,} bytes / {size_bytes / 1024:.1f} KB)")
    print(f"[Synced] Copied to {out_bundle.relative_to(BASE_DIR)}")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
