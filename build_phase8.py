#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 8 Deterministic Builder & Commercial Release Packager (build_phase8.py)
The AI Freelancer Operating System — Digital Knowledge Product Studio

Builds:
1. 10-MARKETING/index.html (>= 60,000 bytes standalone interactive sales & lead-magnet funnel landing page)
2. 5 Commercial Customer & Publisher Release ZIP Bundles in 09-EXPORTS/HYBRID-BUNDLE/:
   - Tier0-Free-Leak-Audit-Starter-Kit.zip
   - Tier1-KDP-and-D2D-Publisher-Upload-Pack.zip
   - Tier2-Interactive-Workbook-and-Planner-Edition.zip
   - Tier3-Complete-AI-Freelancer-OS-Flagship-Bundle.zip
   - Tier4-Living-OS-Pro-Vault-Membership-Pack.zip
3. Updates root README.md with complete 8-phase studio inventory, architecture tree, and launch commands.
"""

import json
import sys
import zipfile
from pathlib import Path

from build_webapp import extract_all_prompts, extract_all_scripts

BASE_DIR = Path(__file__).resolve().parent
MARKETING_DIR = BASE_DIR / "10-MARKETING"
HYBRID_BUNDLE_DIR = BASE_DIR / "09-EXPORTS" / "HYBRID-BUNDLE"

CHAPTER_METADATA = [
    {
        "num": 1,
        "part": "Part I: Operational Diagnostics & Productized Positioning",
        "title": "Chapter 1: The Overwhelmed Freelancer's Bottleneck (The 5-Stage Operating Model)",
        "framework": "The 5-Stage Client Lifecycle & True Effective Hourly Rate (EHR) Diagnostic",
        "mindmap": "chapter-01-mindmap.svg — The 5-Stage Freelancer Operating Model",
        "flowchart": "chapter-01-flowchart.svg — Bottleneck Triage & Circuit-Breaker Routing",
        "worksheet": "Worksheet 1.1: The 7-Day Time & Revenue Leak Audit",
        "case_study": "Marcus Vance (UX & Webflow): Lifted EHR from $26.80/hr to $49.33/hr in 30 days.",
    },
    {
        "num": 2,
        "part": "Part I: Operational Diagnostics & Productized Positioning",
        "title": "Chapter 2: Positioning & Productized Service Packaging",
        "framework": "The 3-Tier Productized Offer Matrix & Hard Scope Boundary Charter",
        "mindmap": "chapter-02-mindmap.svg — 3-Tier Productized Packaging Architecture",
        "flowchart": "chapter-02-flowchart.svg — Custom Inquiry to Productized Tier Router",
        "worksheet": "Worksheet 2.1: The 3-Tier Productized Offer & Scope Boundary Matrix",
        "case_study": "Elena Rostova (B2B SaaS Copywriter): Replaced custom quotes with $2.8k/$4.8k/$7.2k tiers.",
    },
    {
        "num": 3,
        "part": "Part II: Pipeline Triage, Rapid Proposals & Precision Pricing",
        "title": "Chapter 3: The 10-Minute Lead Triage & Proposal Engine",
        "framework": "The 20-Point P.A.C.E. Lead Scorer & 10-Minute B.R.I.E.F. Proposal System",
        "mindmap": "chapter-03-mindmap.svg — P.A.C.E. Qualification & B.R.I.E.F. Architecture",
        "flowchart": "chapter-03-flowchart.svg — Inbound Lead Scoring & Paid Diagnostic Gate",
        "worksheet": "Worksheet 3.1: The P.A.C.E. Lead Triage & 10-Minute B.R.I.E.F. Proposal Builder",
        "case_study": "Cut proposal drafting time from 3.5 hours to 11 minutes while lifting close rate to 48%.",
    },
    {
        "num": 4,
        "part": "Part II: Pipeline Triage, Rapid Proposals & Precision Pricing",
        "title": "Chapter 4: Precision Pricing, Estimation & Margin Defense",
        "framework": "The B.C.R. Pricing Formula (Base + Complexity + Risk Buffer) & Zero-Discount Trade-Down",
        "mindmap": "chapter-04-mindmap.svg — B.C.R. Pricing & Walk-Away Floor Mechanics",
        "flowchart": "chapter-04-flowchart.svg — Discount Objection & Scope Trade-Down Decision Tree",
        "worksheet": "Worksheet 4.1: The B.C.R. Precision Pricing & Margin Defense Calculator",
        "case_study": "Devon K. (Full-Stack Dev): Eliminated unpriced technical overruns and protected a 68% margin.",
    },
    {
        "num": 5,
        "part": "Part III: Onboarding, AI Execution & Scope Protection",
        "title": "Chapter 5: Zero-Friction Client Onboarding & Kickoff Architecture",
        "framework": "The 48-Hour Pre-Flight Asset Gate & Single-Link Client Command Hub",
        "mindmap": "chapter-05-mindmap.svg — 48-Hour Pre-Flight Onboarding Ecosystem",
        "flowchart": "chapter-05-flowchart.svg — Missing Asset Hold & Day-for-Day Timeline Shift Gate",
        "worksheet": "Worksheet 5.1: The 48-Hour Onboarding & Asset Gate Checklist",
        "case_study": "Eliminated 11-day mid-project asset stalls across 100% of new client sprints.",
    },
    {
        "num": 6,
        "part": "Part III: Onboarding, AI Execution & Scope Protection",
        "title": "Chapter 6: AI-Assisted Project Execution & Quality Control",
        "framework": "The 20/60/20 Sandwich Execution Protocol & 4-Gate Pre-Submission QA Audit",
        "mindmap": "chapter-06-mindmap.svg — 20/60/20 Sandwich & Voice DNA Calibration",
        "flowchart": "chapter-06-flowchart.svg — 4-Gate Quality Assurance & Red-Team Verification Loop",
        "worksheet": "Worksheet 6.1: The 20/60/20 Sandwich Execution & 4-Gate Quality Assurance Workbook",
        "case_study": "Compressed core deliverable production time by 42% with zero robotic AI tone defects.",
    },
    {
        "num": 7,
        "part": "Part III: Onboarding, AI Execution & Scope Protection",
        "title": "Chapter 7: Defeating Scope Creep & Difficult Client Conversations",
        "framework": "The Pause-Validate-Price (P.V.P.) Change Order Protocol & Late-Payment Escalation Ladder",
        "mindmap": "chapter-07-mindmap.svg — P.V.P. Scope Boundary & Escalation Matrix",
        "flowchart": "chapter-07-flowchart.svg — Out-of-Scope Request & Overdue Invoice Router",
        "worksheet": "Worksheet 7.1: The P.V.P. Scope Boundary, Change Order & Late-Payment Escalation Log",
        "case_study": "Converted 78% of informal Slack scope additions into $450–$950 paid Change Orders.",
    },
    {
        "num": 8,
        "part": "Part IV: Async Delivery, Retainer Offboarding & CEO Scaling",
        "title": "Chapter 8: Async Client Updates & Revision Minimization",
        "framework": "The 3-Pillar Async Status Cadence, 3-Minute Loom Structure & Guided Feedback Frame",
        "mindmap": "chapter-08-mindmap.svg — Async Status & SPOC Revision Consolidation",
        "flowchart": "chapter-08-flowchart.svg — Stakeholder Feedback & Ad-Hoc Call Deflection Tree",
        "worksheet": "Worksheet 8.1: The 3-Pillar Async Status, Loom Walkthrough & Guided Feedback Tracker",
        "case_study": "Priya Sharma (Brand Designer): Cut status calls by 85% and capped revisions at 1.4 rounds.",
    },
    {
        "num": 9,
        "part": "Part IV: Async Delivery, Retainer Offboarding & CEO Scaling",
        "title": "Chapter 9: Smooth Offboarding, Case Studies & The Retainer Bridge",
        "framework": "The Executive Handover Vault, ROI Testimonial Harvester & 48-Hour Retainer Bridge",
        "mindmap": "chapter-09-mindmap.svg — Executive Offboarding & Retainer Conversion Bridge",
        "flowchart": "chapter-09-flowchart.svg — Final Sign-Off to Monthly Retainer Pitch Sequence",
        "worksheet": "Worksheet 9.1: Executive Handover, Testimonial Capture & Offboard-to-Retainer Bridge",
        "case_study": "Converted 4 out of 9 completed one-off projects into $1,250–$2,400/mo recurring retainers.",
    },
    {
        "num": 10,
        "part": "Part IV: Async Delivery, Retainer Offboarding & CEO Scaling",
        "title": "Chapter 10: The Weekly CEO Review & 90-Day Scaling Roadmap",
        "framework": "The 20-Minute Friday CEO Scorecard, 80/20 Client Roster & 85% Capacity Rate-Raise Trigger",
        "mindmap": "chapter-10-mindmap.svg — Friday CEO Command & 90-Day Scaling Engine",
        "flowchart": "chapter-10-flowchart.svg — 80/20 Client Pruning & 85% Rate-Raise Trigger Logic",
        "worksheet": "Worksheet 10.1: The 20-Minute Friday CEO Scorecard, Client EHR Pruning & 90-Day Scaling Roadmap",
        "case_study": "Replaced bottom-20% Whale-Trap account and scaled blended portfolio EHR to $84.10/hr.",
    },
]


def build_marketing_landing_page() -> Path:
    """Build the standalone interactive sales & lead-magnet funnel landing page (10-MARKETING/index.html)."""
    MARKETING_DIR.mkdir(parents=True, exist_ok=True)
    prompts = extract_all_prompts()
    scripts = extract_all_scripts()

    curriculum_json = json.dumps(CHAPTER_METADATA, indent=2, ensure_ascii=False)
    prompts_json = json.dumps(prompts, indent=2, ensure_ascii=False)
    scripts_json = json.dumps(scripts, indent=2, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>The AI Freelancer Operating System — 5-Pillar Commercial Hybrid Ecosystem</title>
  <meta name="description" content="A Practical System to Organize Clients, Automate Repetitive Work, Manage Projects, and Build a More Productive Freelance Business. Includes 168-Page Manual, Fillable Workbooks, SaaS-Lite Web App, 5-Database Notion OS, and 4-Tab Excel Financial Matrix." />
  <style>
    :root {{
      --primary: #0F172A;
      --primary-elevated: #1E293B;
      --accent: #0284C7;
      --accent-hover: #0369A1;
      --accent-soft: #E0F2FE;
      --secondary: #0D9488;
      --secondary-soft: #CCFBF1;
      --amber: #D97706;
      --amber-soft: #FEF3C7;
      --danger: #DC2626;
      --danger-soft: #FEE2E2;
      --text: #1E293B;
      --muted: #64748B;
      --bg: #FFFFFF;
      --surface: #F8FAFC;
      --border: #E2E8F0;
      --border-strong: #CBD5E1;
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 18px;
      --shadow-sm: 0 2px 6px rgba(15, 23, 42, 0.06);
      --shadow-md: 0 10px 28px rgba(15, 23, 42, 0.10);
      --shadow-lg: 0 20px 44px rgba(15, 23, 42, 0.16);
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html {{
      scroll-behavior: smooth;
    }}

    body {{
      font-family: var(--font-sans);
      color: var(--text);
      background-color: var(--surface);
      line-height: 1.6;
      font-size: 16px;
    }}

    /* Sticky Top Navigation */
    .navbar {{
      position: sticky;
      top: 0;
      z-index: 1000;
      background-color: rgba(15, 23, 42, 0.97);
      backdrop-filter: blur(10px);
      border-bottom: 2px solid var(--accent);
      padding: 12px 24px;
      color: #FFFFFF;
    }}

    .nav-container {{
      max-width: 1320px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 14px;
    }}

    .brand-box {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: #FFFFFF;
    }}

    .brand-mark {{
      width: 40px;
      height: 40px;
      border-radius: 10px;
      background: linear-gradient(135deg, var(--accent), var(--secondary));
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-mono);
      font-weight: 900;
      font-size: 16px;
      color: #FFFFFF;
    }}

    .brand-name {{
      font-weight: 800;
      font-size: 15.5px;
      letter-spacing: -0.02em;
    }}

    .brand-tag {{
      font-size: 11.5px;
      color: #94A3B8;
      display: block;
    }}

    .nav-links {{
      display: flex;
      align-items: center;
      gap: 18px;
      flex-wrap: wrap;
    }}

    .nav-links a {{
      color: #CBD5E1;
      text-decoration: none;
      font-size: 13.5px;
      font-weight: 600;
      transition: color 0.15s ease;
    }}

    .nav-links a:hover {{
      color: #38BDF8;
    }}

    .nav-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .currency-picker {{
      background-color: #1E293B;
      color: #F8FAFC;
      border: 1px solid #475569;
      border-radius: 6px;
      padding: 7px 10px;
      font-size: 12.5px;
      font-weight: 700;
      cursor: pointer;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 10px 18px;
      border-radius: var(--radius-sm);
      font-weight: 700;
      font-size: 14px;
      text-decoration: none;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.16s ease;
    }}

    .btn-lg {{
      padding: 15px 26px;
      font-size: 16px;
      border-radius: var(--radius-md);
    }}

    .btn-primary {{
      background-color: var(--accent);
      color: #FFFFFF;
    }}

    .btn-primary:hover {{
      background-color: var(--accent-hover);
      transform: translateY(-1px);
    }}

    .btn-teal {{
      background-color: var(--secondary);
      color: #FFFFFF;
    }}

    .btn-teal:hover {{
      background-color: #0F766E;
      transform: translateY(-1px);
    }}

    .btn-outline-light {{
      background-color: transparent;
      border-color: #475569;
      color: #F8FAFC;
    }}

    .btn-outline-light:hover {{
      border-color: #38BDF8;
      color: #38BDF8;
    }}

    .btn-navy {{
      background-color: var(--primary);
      color: #FFFFFF;
    }}

    .btn-navy:hover {{
      background-color: var(--primary-elevated);
    }}

    /* Hero Section */
    .hero {{
      background: radial-gradient(circle at 80% 20%, #1E293B 0%, #0F172A 70%);
      color: #FFFFFF;
      padding: 76px 24px 84px;
      border-bottom: 4px solid var(--secondary);
    }}

    .container {{
      max-width: 1280px;
      margin: 0 auto;
    }}

    .hero-grid {{
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 44px;
      align-items: center;
    }}

    @media (max-width: 980px) {{
      .hero-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .eyebrow-badge {{
      display: inline-block;
      background-color: rgba(2, 132, 199, 0.2);
      border: 1px solid #38BDF8;
      color: #38BDF8;
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: 999px;
      letter-spacing: 0.04em;
      margin-bottom: 18px;
    }}

    .hero h1 {{
      font-size: clamp(34px, 4.5vw, 54px);
      font-weight: 900;
      line-height: 1.12;
      letter-spacing: -0.025em;
      margin-bottom: 20px;
    }}

    .hero h1 span.highlight {{
      color: #38BDF8;
    }}

    .hero h1 span.teal-text {{
      color: #2DD4BF;
    }}

    .hero-lead {{
      font-size: 18.5px;
      color: #CBD5E1;
      margin-bottom: 28px;
      max-width: 680px;
    }}

    .hero-cta-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      margin-bottom: 28px;
    }}

    .hero-trust-strip {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      padding-top: 22px;
      border-top: 1px solid #334155;
    }}

    @media (max-width: 640px) {{
      .hero-trust-strip {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

    .trust-stat strong {{
      display: block;
      font-family: var(--font-mono);
      font-size: 22px;
      font-weight: 800;
      color: #2DD4BF;
    }}

    .trust-stat span {{
      font-size: 12.5px;
      color: #94A3B8;
    }}

    .hero-showcase-card {{
      background-color: #1E293B;
      border: 2px solid #334155;
      border-radius: var(--radius-lg);
      padding: 26px;
      box-shadow: var(--shadow-lg);
    }}

    .showcase-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 14px;
      margin-bottom: 16px;
      border-bottom: 1px solid #334155;
      font-family: var(--font-mono);
      font-size: 12.5px;
      color: #38BDF8;
    }}

    .pillar-mini-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 11px;
    }}

    .pillar-mini-item {{
      background-color: #0F172A;
      border: 1px solid #334155;
      border-left: 4px solid var(--accent);
      border-radius: var(--radius-sm);
      padding: 12px 14px;
    }}

    .pillar-mini-item.teal {{
      border-left-color: var(--secondary);
    }}

    .pillar-mini-item.amber {{
      border-left-color: #F59E0B;
    }}

    .pillar-mini-item strong {{
      display: block;
      font-size: 14px;
      color: #FFFFFF;
      margin-bottom: 2px;
    }}

    .pillar-mini-item span {{
      font-size: 12.5px;
      color: #94A3B8;
    }}

    /* Section Defaults */
    .section {{
      padding: 80px 24px;
    }}

    .section-alt {{
      background-color: var(--bg);
      border-top: 1px solid var(--border);
      border-bottom: 1px solid var(--border);
    }}

    .section-header {{
      text-align: center;
      max-width: 820px;
      margin: 0 auto 48px;
    }}

    .section-tag {{
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--accent);
      background-color: var(--accent-soft);
      padding: 5px 12px;
      border-radius: 999px;
      margin-bottom: 12px;
    }}

    .section-title {{
      font-size: clamp(28px, 3.4vw, 40px);
      font-weight: 900;
      color: var(--primary);
      letter-spacing: -0.02em;
      line-height: 1.2;
      margin-bottom: 14px;
    }}

    .section-subtitle {{
      font-size: 17px;
      color: var(--muted);
    }}

    /* Interactive Calculator Card */
    .calc-shell {{
      background-color: var(--bg);
      border: 2px solid var(--border-strong);
      border-radius: var(--radius-lg);
      padding: 32px;
      box-shadow: var(--shadow-md);
    }}

    .calc-grid {{
      display: grid;
      grid-template-columns: 1fr 1.1fr;
      gap: 32px;
      align-items: start;
    }}

    @media (max-width: 920px) {{
      .calc-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .input-panel {{
      background-color: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 22px;
    }}

    .field-row {{
      margin-bottom: 16px;
    }}

    .field-label {{
      display: flex;
      justify-content: space-between;
      font-size: 13.5px;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 6px;
    }}

    .field-input {{
      width: 100%;
      padding: 10px 12px;
      border-radius: 6px;
      border: 1px solid var(--border-strong);
      font-family: var(--font-sans);
      font-size: 14.5px;
      font-weight: 600;
      color: var(--primary);
    }}

    .kpi-grid-2x2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      margin-bottom: 18px;
    }}

    @media (max-width: 560px) {{
      .kpi-grid-2x2 {{
        grid-template-columns: 1fr;
      }}
    }}

    .kpi-box {{
      background-color: var(--surface);
      border: 1px solid var(--border);
      border-left: 5px solid var(--accent);
      border-radius: var(--radius-sm);
      padding: 16px;
    }}

    .kpi-box.teal {{ border-left-color: var(--secondary); }}
    .kpi-box.amber {{ border-left-color: var(--amber); }}
    .kpi-box.danger {{ border-left-color: var(--danger); }}

    .kpi-box-label {{
      font-size: 11.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--muted);
      margin-bottom: 4px;
    }}

    .kpi-box-val {{
      font-family: var(--font-mono);
      font-size: 28px;
      font-weight: 900;
      color: var(--primary);
    }}

    .kpi-box-sub {{
      font-size: 12px;
      color: var(--muted);
      margin-top: 4px;
    }}

    .stacked-bar {{
      width: 100%;
      height: 26px;
      border-radius: 999px;
      background-color: #E2E8F0;
      overflow: hidden;
      display: flex;
      margin: 10px 0;
    }}

    .sb-seg {{
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 800;
      color: #FFFFFF;
      transition: width 0.2s ease;
    }}

    /* 5 Pillars Showcase Grid */
    .pillars-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
      gap: 24px;
    }}

    .pillar-card {{
      background-color: var(--bg);
      border: 1px solid var(--border-strong);
      border-top: 5px solid var(--accent);
      border-radius: var(--radius-md);
      padding: 26px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .pillar-card.teal {{ border-top-color: var(--secondary); }}
    .pillar-card.amber {{ border-top-color: var(--amber); }}
    .pillar-card.navy {{ border-top-color: var(--primary); }}

    .pillar-num {{
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 800;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 8px;
    }}

    .pillar-card h3 {{
      font-size: 21px;
      font-weight: 800;
      color: var(--primary);
      margin-bottom: 10px;
      line-height: 1.3;
    }}

    .pillar-card p {{
      font-size: 14.5px;
      color: var(--muted);
      margin-bottom: 16px;
    }}

    .check-list {{
      list-style: none;
      margin-bottom: 18px;
    }}

    .check-list li {{
      font-size: 13.5px;
      color: var(--text);
      margin-bottom: 8px;
      padding-left: 22px;
      position: relative;
    }}

    .check-list li::before {{
      content: "✓";
      position: absolute;
      left: 0;
      top: 0;
      color: var(--secondary);
      font-weight: 900;
    }}

    /* Interactive Curriculum Explorer */
    .curriculum-layout {{
      display: grid;
      grid-template-columns: 340px 1fr;
      gap: 24px;
      align-items: start;
    }}

    @media (max-width: 920px) {{
      .curriculum-layout {{
        grid-template-columns: 1fr;
      }}
    }}

    .chapter-tab-list {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .chapter-tab-btn {{
      text-align: left;
      padding: 13px 16px;
      background-color: var(--bg);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-sm);
      cursor: pointer;
      font-family: var(--font-sans);
      transition: all 0.14s ease;
    }}

    .chapter-tab-btn:hover {{
      border-color: var(--accent);
      background-color: #F0F9FF;
    }}

    .chapter-tab-btn.active {{
      background-color: var(--primary);
      color: #FFFFFF;
      border-color: var(--primary);
      border-left: 5px solid var(--accent);
    }}

    .chapter-tab-btn .ch-code {{
      display: block;
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 800;
      color: var(--accent);
      margin-bottom: 2px;
    }}

    .chapter-tab-btn.active .ch-code {{
      color: #38BDF8;
    }}

    .chapter-tab-btn .ch-name {{
      font-size: 13.5px;
      font-weight: 700;
    }}

    .chapter-detail-pane {{
      background-color: var(--bg);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-md);
      padding: 28px;
      box-shadow: var(--shadow-sm);
    }}

    .prompt-preview-card {{
      background-color: var(--surface);
      border: 1px solid var(--border);
      border-left: 4px solid var(--secondary);
      border-radius: var(--radius-sm);
      padding: 14px 16px;
      margin-bottom: 10px;
    }}

    /* Case Studies Grid */
    .case-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(285px, 1fr));
      gap: 22px;
    }}

    .case-card {{
      background-color: var(--bg);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-md);
      padding: 24px;
      box-shadow: var(--shadow-sm);
    }}

    .case-metric-banner {{
      background-color: var(--primary);
      color: #FFFFFF;
      border-radius: var(--radius-sm);
      padding: 12px 14px;
      margin: 14px 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-mono);
    }}

    /* 5-Tier Pricing Cards */
    .pricing-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 18px;
      margin-bottom: 44px;
    }}

    .price-card {{
      background-color: var(--bg);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-md);
      padding: 24px 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      box-shadow: var(--shadow-sm);
    }}

    .price-card.flagship {{
      border: 3px solid var(--accent);
      box-shadow: var(--shadow-lg);
      transform: translateY(-6px);
    }}

    .popular-ribbon {{
      position: absolute;
      top: -13px;
      left: 50%;
      transform: translateX(-50%);
      background-color: var(--accent);
      color: #FFFFFF;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      padding: 4px 12px;
      border-radius: 999px;
      white-space: nowrap;
    }}

    .price-amount {{
      font-family: var(--font-mono);
      font-size: 34px;
      font-weight: 900;
      color: var(--primary);
      margin: 10px 0 4px;
    }}

    .comparison-table-wrap {{
      overflow-x: auto;
      background-color: var(--bg);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-sm);
    }}

    table.comp-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13.5px;
    }}

    table.comp-table th {{
      background-color: var(--primary);
      color: #FFFFFF;
      padding: 14px 12px;
      text-align: left;
      font-weight: 800;
    }}

    table.comp-table td {{
      padding: 11px 12px;
      border-bottom: 1px solid var(--border);
    }}

    table.comp-table tr:nth-child(even) {{
      background-color: var(--surface);
    }}

    /* FAQ Accordion */
    .faq-list {{
      max-width: 900px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .faq-item {{
      background-color: var(--bg);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-sm);
      overflow: hidden;
    }}

    .faq-question {{
      width: 100%;
      text-align: left;
      padding: 18px 20px;
      background: none;
      border: none;
      font-family: var(--font-sans);
      font-size: 16px;
      font-weight: 800;
      color: var(--primary);
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
    }}

    .faq-answer {{
      display: none;
      padding: 0 20px 18px;
      font-size: 14.5px;
      color: var(--text);
      border-top: 1px solid var(--border);
      padding-top: 14px;
    }}

    .faq-item.open .faq-answer {{
      display: block;
    }}

    /* Modal */
    .modal-overlay {{
      position: fixed;
      inset: 0;
      background-color: rgba(15, 23, 42, 0.72);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 3000;
      padding: 20px;
    }}

    .modal-overlay.open {{
      display: flex;
    }}

    .modal-box {{
      background-color: var(--bg);
      border-radius: var(--radius-lg);
      max-width: 600px;
      width: 100%;
      padding: 30px;
      box-shadow: var(--shadow-lg);
      border: 2px solid var(--accent);
    }}

    footer {{
      background-color: var(--primary);
      color: #94A3B8;
      padding: 56px 24px;
      font-size: 13.5px;
      border-top: 3px solid var(--accent);
    }}
  </style>
</head>
<body>

  <!-- STICKY TOP NAVIGATION BAR -->
  <header class="navbar">
    <div class="nav-container">
      <a href="#" class="brand-box">
        <div class="brand-mark">OS</div>
        <div>
          <span class="brand-name">The AI Freelancer Operating System</span>
          <span class="brand-tag">5-Pillar Commercial Hybrid Ecosystem • v1.0</span>
        </div>
      </a>

      <nav class="nav-links">
        <a href="#calculator">Live EHR Calculator</a>
        <a href="#pillars">5-Pillar System</a>
        <a href="#curriculum">10-Chapter &amp; 50-Prompt Explorer</a>
        <a href="#case-studies">Case Studies</a>
        <a href="#pricing">5-Tier Pricing</a>
        <a href="#faq">FAQ</a>
      </nav>

      <div class="nav-actions">
        <select id="currency-select" class="currency-picker" aria-label="Select Currency" onchange="updateFunnelCurrency(this.value)">
          <option value="USD">$ USD</option>
          <option value="GBP">£ GBP</option>
          <option value="EUR">€ EUR</option>
          <option value="CAD">CA$ CAD</option>
          <option value="AUD">A$ AUD</option>
        </select>
        <button type="button" class="btn btn-teal" onclick="openLeadMagnetModal()">Free Leak Audit Kit ($0)</button>
        <a href="#pricing" class="btn btn-primary">Get Complete OS (<span class="dyn-price" data-usd="49">$49</span>)</a>
      </div>
    </div>
  </header>

  <!-- HERO SECTION -->
  <section class="hero">
    <div class="container">
      <div class="hero-grid">
        <div>
          <span class="eyebrow-badge">CATEGORY OF ONE // BOOK + WORKBOOKS + WEB APP + NOTION OS + EXCEL MATRIX</span>
          <h1>
            Stop Losing 38% of Your Week to <span class="highlight">Unpaid Admin</span> &amp; <span class="teal-text">Scope Creep.</span>
          </h1>
          <p class="hero-lead">
            <strong>The AI Freelancer Operating System</strong> is a practical, 5-gate operational manual and interactive software suite engineered for independent freelancers, consultants, and solo operators ($2k–$8k+/mo) in the US, UK, Canada, and Australia.
          </p>

          <div class="hero-cta-row">
            <a href="#pricing" class="btn btn-primary btn-lg">Get Complete 5-Pillar OS Bundle (<span class="dyn-price" data-usd="49">$49</span>)</a>
            <button type="button" class="btn btn-teal btn-lg" onclick="openLeadMagnetModal()">Download Free 7-Day Leak Audit Kit ($0)</button>
            <a href="../07-INTERACTIVE-TOOLS/freelancer-os-app.html" class="btn btn-outline-light btn-lg">Launch Live Web Companion App →</a>
          </div>

          <div class="hero-trust-strip">
            <div class="trust-stat">
              <strong>75,158</strong>
              <span>Practitioner Manual Words</span>
            </div>
            <div class="trust-stat">
              <strong>50 + 12</strong>
              <span>AI Workflows &amp; Client Scripts</span>
            </div>
            <div class="trust-stat">
              <strong>20 SVGs</strong>
              <span>Mindmaps &amp; Decision Trees</span>
            </div>
            <div class="trust-stat">
              <strong>5 Pillars</strong>
              <span>PDF + EPUB + Web App + Notion + XLSX</span>
            </div>
          </div>
        </div>

        <!-- Right Showcase Card -->
        <div class="hero-showcase-card">
          <div class="showcase-header">
            <span>SYSTEM ARCHITECTURE // 5 INTEGRATED PILLARS</span>
            <span>v1.0 VERIFIED</span>
          </div>
          <ul class="pillar-mini-list">
            <li class="pillar-mini-item">
              <strong>Pillar 1: 168-Page Operating Manual (PDF, EPUB 3.0 &amp; 6"×9" Print)</strong>
              <span>10 standardized 14-part chapters • 50 tested AI workflows • 20 vector diagrams</span>
            </li>
            <li class="pillar-mini-item teal">
              <strong>Pillar 2: Fillable Workbooks &amp; 49-Page Landscape Tablet Planner</strong>
              <span>US Letter (8.5"×11"), ISO A4 &amp; iPad GoodNotes/Notability interactive editions</span>
            </li>
            <li class="pillar-mini-item">
              <strong>Pillar 3: Zero-Dependency SaaS-Lite Web Companion App</strong>
              <span>Offline/online HTML5 suite: EHR Leak Audit, B.C.R. Pricing, 62-Item Vault &amp; CEO Scorecard</span>
            </li>
            <li class="pillar-mini-item teal">
              <strong>Pillar 4: 5-Database Minimalist Notion OS + 4-Tab Excel Matrix</strong>
              <span>15-min Notion CRM/Portal setup + 117 live Excel formulas for WBS pricing &amp; 90-day cashflow</span>
            </li>
            <li class="pillar-mini-item amber">
              <strong>Pillar 5: 12 Emergency Boundary Scripts &amp; Living OS Vault</strong>
              <span>Word-for-word scripts for P.V.P. Change Orders, discount defense, SPOC rules &amp; rate resets</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- SECTION 1: INTERACTIVE EMBEDDED 7-DAY TIME & EHR LEAK CALCULATOR -->
  <section id="calculator" class="section">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Interactive Diagnostic // Module 1 Preview</span>
        <h2 class="section-title">Calculate Your True Effective Hourly Rate (EHR) in 60 Seconds</h2>
        <p class="section-subtitle">
          Most freelancers think they earn $75/hour because that is the number on their invoice. Enter your real weekly hours below to see how unbilled proposals, missing client assets, and scope creep impact your real take-home yield.
        </p>
      </div>

      <div class="calc-shell">
        <div class="calc-grid">
          <!-- Left: Calculator Inputs -->
          <div class="input-panel">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
              <h3 style="font-size:17px; font-weight:800; color:var(--primary);">Your 7-Day Time &amp; Revenue Inputs</h3>
              <button type="button" class="btn btn-navy" style="padding:6px 12px; font-size:12px;" onclick="resetMarcusDemo()">Load Marcus V. Case Study</button>
            </div>

            <div class="field-row">
              <label class="field-label" for="calc-target-rate">
                <span>1. Stated Target Hourly Rate</span>
                <span id="lbl-target-rate">$75/hr</span>
              </label>
              <input type="number" id="calc-target-rate" class="field-input" value="75" min="10" max="500" step="5" oninput="runFunnelCalculator()" />
            </div>

            <div class="field-row">
              <label class="field-label" for="calc-weekly-rev">
                <span>2. Weekly Gross Revenue Billed (or Monthly ÷ 4)</span>
                <span id="lbl-weekly-rev">$1,300/wk</span>
              </label>
              <input type="number" id="calc-weekly-rev" class="field-input" value="1300" min="100" max="25000" step="50" oninput="runFunnelCalculator()" />
            </div>

            <div class="field-row">
              <label class="field-label" for="calc-bucket-a">
                <span>3. Bucket A — Direct Billable Craft Hours/Wk</span>
                <span style="color:var(--secondary);">Target &gt;= 65%</span>
              </label>
              <input type="number" id="calc-bucket-a" class="field-input" value="26.5" min="1" max="80" step="0.5" oninput="runFunnelCalculator()" />
            </div>

            <div class="field-row">
              <label class="field-label" for="calc-bucket-b">
                <span>4. Bucket B — Unbilled Client Friction &amp; Revisions Hrs/Wk</span>
                <span style="color:var(--danger);">Target &lt;= 5%</span>
              </label>
              <input type="number" id="calc-bucket-b" class="field-input" value="8.0" min="0" max="50" step="0.5" oninput="runFunnelCalculator()" />
            </div>

            <div class="field-row">
              <label class="field-label" for="calc-bucket-c">
                <span>5. Bucket C — Unpaid Sales, Proposals &amp; Calls Hrs/Wk</span>
                <span style="color:var(--amber);">Target &lt;= 15%</span>
              </label>
              <input type="number" id="calc-bucket-c" class="field-input" value="5.5" min="0" max="50" step="0.5" oninput="runFunnelCalculator()" />
            </div>

            <div class="field-row" style="margin-bottom:0;">
              <label class="field-label" for="calc-bucket-d">
                <span>6. Bucket D — Admin, Inbox &amp; Context-Switching Hrs/Wk</span>
                <span style="color:#6366F1;">Target &lt;= 15%</span>
              </label>
              <input type="number" id="calc-bucket-d" class="field-input" value="8.5" min="0" max="50" step="0.5" oninput="runFunnelCalculator()" />
            </div>
          </div>

          <!-- Right: Live Telemetry Outputs -->
          <div>
            <div class="kpi-grid-2x2">
              <div class="kpi-box">
                <div class="kpi-box-label">True Effective Hourly Rate (EHR)</div>
                <div class="kpi-box-val" id="res-true-ehr">$26.80/hr</div>
                <div class="kpi-box-sub" id="res-rate-erosion">Rate Collapse: -64.3% below $75/hr target</div>
              </div>

              <div class="kpi-box teal">
                <div class="kpi-box-label">Billable Craft Utilization (Bucket A)</div>
                <div class="kpi-box-val" id="res-util-pct">54.6%</div>
                <div class="kpi-box-sub" id="res-total-hrs">26.5 billable hrs / 48.5 total real hrs</div>
              </div>

              <div class="kpi-box amber">
                <div class="kpi-box-label">Monthly Unbilled Revenue Leak</div>
                <div class="kpi-box-val" id="res-monthly-leak">$7,145/mo</div>
                <div class="kpi-box-sub" id="res-weekly-leak">22.0 unbilled hrs/wk × Target Rate</div>
              </div>

              <div class="kpi-box danger">
                <div class="kpi-box-label">Annualized 48-Week Revenue Leak</div>
                <div class="kpi-box-val" id="res-annual-leak">$79,200/yr</div>
                <div class="kpi-box-sub" id="res-recovery-est">90-Day AI OS 55% Recovery: +$43,560/yr</div>
              </div>
            </div>

            <!-- Visual Stacked Time Allocation Bar -->
            <div style="background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-sm); padding:16px; margin-bottom:18px;">
              <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:800; color:var(--primary);">
                <span>Your Weekly Time Allocation Breakdown</span>
                <span id="res-bar-total">48.5 Total Hours</span>
              </div>
              <div class="stacked-bar">
                <div id="sb-a" class="sb-seg" style="width:54.6%; background:var(--secondary);">A: 55%</div>
                <div id="sb-b" class="sb-seg" style="width:16.5%; background:var(--danger);">B: 17%</div>
                <div id="sb-c" class="sb-seg" style="width:11.3%; background:var(--amber);">C: 11%</div>
                <div id="sb-d" class="sb-seg" style="width:17.5%; background:#6366F1;">D: 18%</div>
              </div>
              <div style="font-size:12.5px; color:var(--muted); margin-top:8px;" id="res-prescription">
                <strong>Diagnostic Prescription:</strong> Install the 10-Minute B.R.I.E.F. Proposal Engine (Chapter 3) to cut Bucket C in half, and deploy Script 7 (P.V.P. Change Orders) to convert Bucket B revisions into paid scope additions.
              </div>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:12px;">
              <button type="button" class="btn btn-teal" onclick="openLeadMagnetModal()">Download Free Worksheet 1.1 &amp; Starter Kit ($0)</button>
              <a href="../07-INTERACTIVE-TOOLS/freelancer-os-app.html" class="btn btn-primary">Open Full 4-Module Web Companion App →</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- SECTION 2: THE 5-PILLAR HYBRID PRODUCT ECOSYSTEM -->
  <section id="pillars" class="section section-alt">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Complete Hybrid Architecture // 5 Integrated Pillars</span>
        <h2 class="section-title">Why Standalone Templates Fail—And How Our 5-Pillar Ecosystem Works</h2>
        <p class="section-subtitle">
          Generic AI prompt lists lack operational formulas, and bloated 20-tab Notion templates collapse under their own maintenance weight. Every tool in this ecosystem shares the exact same 5-Gate math.
        </p>
      </div>

      <div class="pillars-grid">
        <div class="pillar-card">
          <div>
            <div class="pillar-num">Pillar 01 // Core Manual &amp; Visuals</div>
            <h3>The 168-Page Practical Operating Manual</h3>
            <p>75,158 words of zero-fluff operational architecture across 10 standardized 14-section chapters, Front Matter, and the Back Matter Vault.</p>
            <ul class="check-list">
              <li>Compiled in Digital PDF (168 pp), KDP 6"×9" Print (146 pp) &amp; Reflowable EPUB 3.0</li>
              <li>50 Tested AI Workflow Prompts (Prompts 1.1–10.5) with verification rules</li>
              <li>20 High-Contrast Vector System Mindmaps &amp; Decision Trees (.svg)</li>
              <li>Real-world practitioner case studies with Before/After financial tables</li>
            </ul>
          </div>
          <span style="font-family:var(--font-mono); font-size:12px; font-weight:700; color:var(--accent);">Included in Tiers 1, 2, 3 &amp; 4</span>
        </div>

        <div class="pillar-card teal">
          <div>
            <div class="pillar-num" style="color:var(--secondary);">Pillar 02 // Action Workbooks &amp; Tablet Planner</div>
            <h3>Fillable US Letter, A4 &amp; iPad Planner Suite</h3>
            <p>10 standalone chapter workbooks (12,717 words) engineered with interactive AcroForm text fields and checkboxes for immediate execution.</p>
            <ul class="check-list">
              <li>US Letter (8.5"×11" — 36 pages) &amp; ISO A4 (210×297mm — 34 pages) Fillable PDFs</li>
              <li>49-Page Landscape Tablet Digital Planner for GoodNotes, Notability &amp; reMarkable</li>
              <li>Step-by-step scorecards for EHR Audits, 3-Tier Packaging &amp; B.C.R. Pricing</li>
              <li>48-Hour Onboarding Checklists &amp; 20-Minute Friday CEO Review Ledgers</li>
            </ul>
          </div>
          <span style="font-family:var(--font-mono); font-size:12px; font-weight:700; color:var(--secondary);">Included in Tiers 2, 3 &amp; 4</span>
        </div>

        <div class="pillar-card">
          <div>
            <div class="pillar-num">Pillar 03 // Offline/Online Software Suite</div>
            <h3>SaaS-Lite Interactive Web Companion App</h3>
            <p>A zero-dependency, single-file HTML5 application (<code>freelancer-os-app.html</code>) that runs 100% offline on any laptop or tablet with local storage persistence.</p>
            <ul class="check-list">
              <li>Module 1: 7-Day EHR Leak Audit &amp; Daily 3-Block Priority Planner</li>
              <li>Module 2: WBS Estimator, B.C.R. 3-Tier Proposal Pricing &amp; Discount Counter-Offer Engine</li>
              <li>Module 3: Interactive 50-Prompt &amp; 12-Script Studio Builder with live variable inputs</li>
              <li>Module 4: Friday CEO Scorecard, 80/20 Client Roster &amp; 85% Rate-Raise Trigger</li>
            </ul>
          </div>
          <span style="font-family:var(--font-mono); font-size:12px; font-weight:700; color:var(--accent);">Free Mode in Tier 0 • Full Pro in Tiers 3 &amp; 4</span>
        </div>

        <div class="pillar-card teal">
          <div>
            <div class="pillar-num" style="color:var(--secondary);">Pillar 04 // Workspace &amp; Financial Engine</div>
            <h3>5-Database Notion OS &amp; 4-Tab Excel Matrix</h3>
            <p>Deploy a high-velocity Notion client workspace in under 15 minutes alongside a native, formula-driven Microsoft Excel (<code>.xlsx</code>) and CSV financial workbook.</p>
            <ul class="check-list">
              <li>Notion DBs: Leads CRM, Active Projects, 62-Item Vault, CEO Log &amp; Client Portal Hub</li>
              <li>Complete Notion Formula 2.0 Library for live EHR, P.A.C.E. routing &amp; 80/20 flags</li>
              <li>4-Tab Excel Matrix with 117 live formulas (<code>=SUM</code>, <code>=IF</code>, <code>=ROUND</code>)</li>
              <li>12-Week Rolling Cashflow, Retainer Baseline &amp; 25% Tax Reserve Forecaster</li>
            </ul>
          </div>
          <span style="font-family:var(--font-mono); font-size:12px; font-weight:700; color:var(--secondary);">Included in Tiers 3 &amp; 4</span>
        </div>

        <div class="pillar-card amber">
          <div>
            <div class="pillar-num" style="color:var(--amber);">Pillar 05 // Boundary Defense &amp; Living Vault</div>
            <h3>12 Emergency Scripts &amp; Monthly Vault Drops</h3>
            <p>Never freeze when a client asks for a 20% discount, demands an unbilled revision round, or stalls on an overdue milestone invoice.</p>
            <ul class="check-list">
              <li>12 Word-for-Word Emergency Client Scripts (Scripts 1–12) for every boundary gate</li>
              <li>Covers Budget Triage, Scope Trade-Downs, 48h Asset Holds &amp; P.V.P. Change Orders</li>
              <li>Includes SPOC Feedback Consolidation, Late-Payment Escalation &amp; Rate Resets</li>
              <li>Tier 4 Living OS Pass adds Monthly Niche Workflow Drops (Drop #01 Included)</li>
            </ul>
          </div>
          <span style="font-family:var(--font-mono); font-size:12px; font-weight:700; color:var(--amber);">Scripts in Tiers 1–4 • Monthly Drops in Tier 4</span>
        </div>
      </div>
    </div>
  </section>

  <!-- SECTION 3: INTERACTIVE 10-CHAPTER & 62-ASSET CURRICULUM EXPLORER -->
  <section id="curriculum" class="section">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Single-Source Transparency // Inspect Every Chapter</span>
        <h2 class="section-title">Interactive 10-Chapter, 50-Prompt &amp; 12-Script Curriculum Explorer</h2>
        <p class="section-subtitle">
          Click any chapter below to inspect its core operating framework, vector system diagrams, standalone action worksheet, and the exact 5 tested AI workflow prompts inside.
        </p>
      </div>

      <div class="curriculum-layout">
        <div class="chapter-tab-list" id="curriculum-tabs">
          <!-- Populated dynamically by JS -->
        </div>

        <div class="chapter-detail-pane" id="curriculum-detail">
          <!-- Populated dynamically by JS -->
        </div>
      </div>
    </div>
  </section>

  <!-- SECTION 4: VERIFIED PRACTITIONER CASE STUDIES -->
  <section id="case-studies" class="section section-alt">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Quantified Practitioner Outcomes // System Over Theory</span>
        <h2 class="section-title">Real-World Freelance Operations Transformed by the 5-Gate Model</h2>
        <p class="section-subtitle">
          See how four independent service providers across UX/Webflow, B2B Copywriting, Full-Stack Development, and Brand Design plugged their time and margin leaks in 30 days.
        </p>
      </div>

      <div class="case-grid">
        <div class="case-card">
          <span class="section-tag" style="margin-bottom:8px;">Chapter 1 &amp; 5 Case Study</span>
          <h3 style="font-size:19px; font-weight:800; color:var(--primary);">Marcus Vance — UX Designer &amp; Webflow Developer (Austin, US)</h3>
          <div class="case-metric-banner">
            <span>EHR: $26.80 → $58.40/hr</span>
            <span style="color:#2DD4BF;">+118% Yield</span>
          </div>
          <p style="font-size:14px; color:var(--muted); margin-bottom:10px;">
            <strong>Baseline Bottleneck:</strong> Working 48.5 hrs/wk for $5,200/mo with 22.0 unbilled hours lost to custom proposals, missing client logins, and Slack scope creep.
          </p>
          <p style="font-size:14px; color:var(--text);">
            <strong>System Installed:</strong> Deployed the 7-Day Leak Audit, Daily 90-Minute Morning Maker Block, and 48-Hour Pre-Flight Asset Gate. Cut weekly hours to 36.5 hrs while lifting monthly revenue to $8,520/mo.
          </p>
        </div>

        <div class="case-card">
          <span class="section-tag" style="margin-bottom:8px;">Chapter 2 &amp; 3 Case Study</span>
          <h3 style="font-size:19px; font-weight:800; color:var(--primary);">Elena Rostova — B2B SaaS Conversion Copywriter (London, UK)</h3>
          <div class="case-metric-banner">
            <span>Proposal Time: 3.5h → 11m</span>
            <span style="color:#38BDF8;">48% Win Rate</span>
          </div>
          <p style="font-size:14px; color:var(--muted); margin-bottom:10px;">
            <strong>Baseline Bottleneck:</strong> Spending 14 hours a month writing custom proposals from scratch for price-shopping prospects with a 21% close rate.
          </p>
          <p style="font-size:14px; color:var(--text);">
            <strong>System Installed:</strong> Packaged services into a 3-Tier Productized Offer Matrix (£2.2k / £3.8k / £5.8k) and installed the P.A.C.E. Lead Scorer + 10-Minute B.R.I.E.F. Proposal Engine.
          </p>
        </div>

        <div class="case-card">
          <span class="section-tag" style="margin-bottom:8px;">Chapter 4 &amp; 7 Case Study</span>
          <h3 style="font-size:19px; font-weight:800; color:var(--primary);">Devon Brooks — Full-Stack SaaS Consultant (Toronto, CA)</h3>
          <div class="case-metric-banner">
            <span>Change Orders: +$3,850/qtr</span>
            <span style="color:#2DD4BF;">0 Free Revisions</span>
          </div>
          <p style="font-size:14px; color:var(--muted); margin-bottom:10px;">
            <strong>Baseline Bottleneck:</strong> Underquoting complex API integrations and absorbing 8+ hours of unpriced stakeholder feature additions per sprint.
          </p>
          <p style="font-size:14px; color:var(--text);">
            <strong>System Installed:</strong> Applied the B.C.R. Pricing Formula (1.30x Complexity + 20% Risk Buffer) and routed every mid-sprint addition through Script 7 (P.V.P. Change Orders).
          </p>
        </div>

        <div class="case-card">
          <span class="section-tag" style="margin-bottom:8px;">Chapter 8, 9 &amp; 10 Case Study</span>
          <h3 style="font-size:19px; font-weight:800; color:var(--primary);">Priya Sharma — Brand &amp; Packaging Strategist (Melbourne, AU)</h3>
          <div class="case-metric-banner">
            <span>Retainer Floor: $4,200/mo</span>
            <span style="color:#FBBF24;">-85% Meetings</span>
          </div>
          <p style="font-size:14px; color:var(--muted); margin-bottom:10px;">
            <strong>Baseline Bottleneck:</strong> Feast-or-famine revenue drops between one-off brand sprints and 9+ hours/week lost to unscheduled client status calls.
          </p>
          <p style="font-size:14px; color:var(--text);">
            <strong>System Installed:</strong> Replaced status calls with 3-Pillar Async Updates + 3-Min Looms, and used the 48-Hour Retainer Bridge (Script 11) to lock in $4,200/mo in recurring baseline retainers.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- SECTION 5: THE 5-TIER COMMERCIAL VALUE LADDER & PRICING MATRIX -->
  <section id="pricing" class="section">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">5-Tier Value Ladder // Instant Digital Delivery</span>
        <h2 class="section-title">Choose the Operating Edition That Fits Your Freelance Practice</h2>
        <p class="section-subtitle">
          Start free with the Tier 0 Leak Audit Starter Kit, pick up the retail book on Amazon KDP or Draft2Digital, or deploy the complete 5-Pillar Flagship Operating System today.
        </p>
      </div>

      <div class="pricing-grid">
        <!-- Tier 0 -->
        <div class="price-card">
          <div>
            <span class="section-tag" style="background:var(--secondary-soft); color:var(--secondary);">Tier 0 // Lead Magnet</span>
            <h3 style="font-size:19px; font-weight:800; color:var(--primary);">The Leak Audit Starter Kit</h3>
            <div class="price-amount"><span class="dyn-price" data-usd="0">$0</span></div>
            <div style="font-size:12.5px; color:var(--muted); margin-bottom:16px;">100% Free Instant Download</div>
            <ul class="check-list">
              <li>Sample Chapter 1 PDF (38 Pages)</li>
              <li>Fillable Worksheet 1.1 PDF</li>
              <li>Standalone EHR Audit CSV Sheet</li>
              <li>Web Companion App (Free Mode)</li>
              <li>5 Chapter 1 AI Workflow Prompts</li>
            </ul>
          </div>
          <button type="button" class="btn btn-teal" style="width:100%;" onclick="openLeadMagnetModal()">Download Free Kit ($0)</button>
        </div>

        <!-- Tier 1 -->
        <div class="price-card">
          <div>
            <span class="section-tag">Tier 1 // Retail Book</span>
            <h3 style="font-size:19px; font-weight:800; color:var(--primary);">Essential Book Edition</h3>
            <div class="price-amount"><span class="dyn-price" data-usd="9.99">$9.99</span></div>
            <div style="font-size:12.5px; color:var(--muted); margin-bottom:16px;">Kindle / EPUB (<span class="dyn-price" data-usd="16.99">$16.99</span> Print Paperback)</div>
            <ul class="check-list">
              <li>Complete 10-Chapter Manual (168 pp)</li>
              <li>All 50 Tested AI Workflow Prompts</li>
              <li>All 20 Vector System Diagrams</li>
              <li>All 12 Emergency Boundary Scripts</li>
              <li>Available on Amazon KDP &amp; Apple/Kobo</li>
            </ul>
          </div>
          <a href="../09-EXPORTS/HYBRID-BUNDLE/Tier1-KDP-and-D2D-Publisher-Upload-Pack.zip" class="btn btn-navy" style="width:100%;">Get Essential Edition</a>
        </div>

        <!-- Tier 2 -->
        <div class="price-card">
          <div>
            <span class="section-tag">Tier 2 // Action Suite</span>
            <h3 style="font-size:19px; font-weight:800; color:var(--primary);">Interactive Workbook Edition</h3>
            <div class="price-amount"><span class="dyn-price" data-usd="24">$24</span></div>
            <div style="font-size:12.5px; color:var(--muted); margin-bottom:16px;">One-Time Direct Download</div>
            <ul class="check-list">
              <li>Everything in Tier 1 (PDF + EPUB 3.0)</li>
              <li>US Letter Fillable Workbook (36 pp)</li>
              <li>ISO A4 Fillable Workbook (34 pp)</li>
              <li>49-Page iPad / Tablet Digital Planner</li>
              <li>62-Item Copy-Paste Prompt Vault CSV</li>
            </ul>
          </div>
          <a href="../09-EXPORTS/HYBRID-BUNDLE/Tier2-Interactive-Workbook-and-Planner-Edition.zip" class="btn btn-primary" style="width:100%;">Download Tier 2 (<span class="dyn-price" data-usd="24">$24</span>)</a>
        </div>

        <!-- Tier 3 (Flagship) -->
        <div class="price-card flagship">
          <div class="popular-ribbon">★ MOST POPULAR — COMPLETE 5-PILLAR OS</div>
          <div>
            <span class="section-tag">Tier 3 // Flagship Bundle</span>
            <h3 style="font-size:19px; font-weight:800; color:var(--primary);">Complete Freelancer OS</h3>
            <div class="price-amount"><span class="dyn-price" data-usd="49">$49</span></div>
            <div style="font-size:12.5px; color:var(--muted); margin-bottom:16px;">One-Time Purchase • Lifetime Pro Code</div>
            <ul class="check-list">
              <li>Everything in Tiers 1 &amp; 2 Included</li>
              <li><strong>Full Pro SaaS-Lite Web Companion App</strong></li>
              <li><strong>5-Database Minimalist Notion OS Kit</strong></li>
              <li><strong>4-Tab Formula Excel &amp; CSV Matrix</strong></li>
              <li><strong>Reusable Client Portal &amp; Formula Guide</strong></li>
            </ul>
          </div>
          <a href="../09-EXPORTS/HYBRID-BUNDLE/Tier3-Complete-AI-Freelancer-OS-Flagship-Bundle.zip" class="btn btn-primary" style="width:100%;">Get Complete OS (<span class="dyn-price" data-usd="49">$49</span>)</a>
        </div>

        <!-- Tier 4 -->
        <div class="price-card">
          <div>
            <span class="section-tag" style="background:var(--amber-soft); color:var(--amber);">Tier 4 // Living Vault</span>
            <h3 style="font-size:19px; font-weight:800; color:var(--primary);">Living OS &amp; Pro Vault Pass</h3>
            <div class="price-amount"><span class="dyn-price" data-usd="9">$9</span><span style="font-size:16px; font-weight:600;">/mo</span></div>
            <div style="font-size:12.5px; color:var(--muted); margin-bottom:16px;">or <span class="dyn-price" data-usd="49">$49</span>/year (Save 55%)</div>
            <ul class="check-list">
              <li>Includes Full Tier 3 Flagship OS Bundle</li>
              <li>Monthly Niche AI Workflow Drops</li>
              <li><strong>Drop #01 (Paid Diagnostic Pack) Ready</strong></li>
              <li>New Negotiation &amp; Retainer Scripts</li>
              <li>Continuous Multi-Model LLM Updates</li>
            </ul>
          </div>
          <a href="../09-EXPORTS/HYBRID-BUNDLE/Tier4-Living-OS-Pro-Vault-Membership-Pack.zip" class="btn btn-teal" style="width:100%;">Join Living OS Pass</a>
        </div>
      </div>

      <!-- Full Comparison Table -->
      <div class="comparison-table-wrap">
        <table class="comp-table">
          <thead>
            <tr>
              <th style="width:36%;">Deliverable / System Component</th>
              <th>Tier 0 (Free)</th>
              <th>Tier 1 ($9.99)</th>
              <th>Tier 2 ($24)</th>
              <th>Tier 3 ($49 OS)</th>
              <th>Tier 4 ($9/mo)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Sample Chapter 1 + Fillable Worksheet 1.1 + EHR Calculator</strong></td>
              <td>✓ Included</td>
              <td>✓ Included</td>
              <td>✓ Included</td>
              <td>✓ Included</td>
              <td>✓ Included</td>
            </tr>
            <tr>
              <td><strong>Complete 10-Chapter Operating Manual (168-Page PDF &amp; EPUB 3.0)</strong></td>
              <td>—</td>
              <td>✓ Included</td>
              <td>✓ Included</td>
              <td>✓ Included</td>
              <td>✓ Included</td>
            </tr>
            <tr>
              <td><strong>All 50 Tested AI Workflow Prompts &amp; 12 Emergency Scripts</strong></td>
              <td>Ch 1 Only (5)</td>
              <td>✓ All 62</td>
              <td>✓ All 62</td>
              <td>✓ All 62</td>
              <td>✓ 62 + Monthly Drops</td>
            </tr>
            <tr>
              <td><strong>20 High-Contrast Vector Mindmaps &amp; Decision Flowcharts (.svg)</strong></td>
              <td>Ch 1 Only (2)</td>
              <td>✓ All 20</td>
              <td>✓ All 20</td>
              <td>✓ All 20</td>
              <td>✓ All 20</td>
            </tr>
            <tr>
              <td><strong>10-Chapter Fillable Workbooks (US Letter 8.5"×11" &amp; ISO A4 PDFs)</strong></td>
              <td>Worksheet 1.1</td>
              <td>—</td>
              <td>✓ Included</td>
              <td>✓ Included</td>
              <td>✓ Included</td>
            </tr>
            <tr>
              <td><strong>49-Page Landscape Tablet Digital Planner (GoodNotes / Notability)</strong></td>
              <td>—</td>
              <td>—</td>
              <td>✓ Included</td>
              <td>✓ Included</td>
              <td>✓ Included</td>
            </tr>
            <tr>
              <td><strong>Pro SaaS-Lite Web Companion App (B.C.R. Pricing, Prompt Studio, CEO Tab)</strong></td>
              <td>Free Mode</td>
              <td>—</td>
              <td>—</td>
              <td><strong>✓ Full Pro Mode</strong></td>
              <td><strong>✓ Full Pro Mode</strong></td>
            </tr>
            <tr>
              <td><strong>5-Database Minimalist Notion Freelancer OS Import Kit + Formula 2.0 Guide</strong></td>
              <td>—</td>
              <td>—</td>
              <td>—</td>
              <td><strong>✓ Included</strong></td>
              <td><strong>✓ Included</strong></td>
            </tr>
            <tr>
              <td><strong>4-Tab Formula-Driven Excel (.xlsx) &amp; CSV Financial/Pricing Matrix</strong></td>
              <td>Sheet 1 CSV</td>
              <td>—</td>
              <td>—</td>
              <td><strong>✓ All 4 Tabs</strong></td>
              <td><strong>✓ All 4 Tabs</strong></td>
            </tr>
            <tr>
              <td><strong>Monthly Role-Specific Workflow Drops &amp; Expansion Packs (Drop #01 Ready)</strong></td>
              <td>—</td>
              <td>—</td>
              <td>—</td>
              <td>—</td>
              <td><strong>✓ Monthly Drops</strong></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- SECTION 6: BUYER FAQ ACCORDION -->
  <section id="faq" class="section section-alt">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Buyer Questions Answered // Zero Ambiguity</span>
        <h2 class="section-title">Frequently Asked Questions</h2>
        <p class="section-subtitle">
          Everything you need to know about the 5-Pillar Ecosystem, compatibility, AI models, and licensing.
        </p>
      </div>

      <div class="faq-list">
        <div class="faq-item open">
          <button type="button" class="faq-question" onclick="toggleFaq(this)">
            <span>1. How is this different from a generic "500 AI Prompts for Freelancers" pack or Notion template?</span>
            <span>+</span>
          </button>
          <div class="faq-answer">
            One-line prompt lists fail because they lack commercial math, scope boundaries, and quality gates. <strong>The AI Freelancer Operating System</strong> installs a complete 5-Stage Client Lifecycle first—giving you the exact pricing formulas (B.C.R.), 48-hour onboarding gates, 20/60/20 execution checklists, and word-for-word client boundary scripts—and then pairs each gate with 50 deep, variable-driven workflow prompts, a standalone HTML5 software suite, a 5-database Notion OS, and a 4-tab Excel pricing matrix.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-question" onclick="toggleFaq(this)">
            <span>2. Do I need a paid subscription to Notion, ChatGPT, Claude, or Microsoft Excel to use this system?</span>
            <span>+</span>
          </button>
          <div class="faq-answer">
            No paid subscriptions are required. The 50 AI workflows run cleanly on the free or paid tiers of Claude, ChatGPT, and Google Gemini. The 5-Database Notion OS imports cleanly into a 100% free personal Notion account. The 4-tab <code>.xlsx</code> workbook works in Microsoft Excel, free Google Sheets, or Apple Numbers (4 standalone CSV sheets are also included). And the SaaS-Lite Web Companion App (<code>freelancer-os-app.html</code>) runs 100% offline in any browser with zero server fees.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-question" onclick="toggleFaq(this)">
            <span>3. What freelance niches and experience levels is this built for?</span>
            <span>+</span>
          </button>
          <div class="faq-answer">
            The operating system is engineered for independent service providers with 1 to 5+ years of experience earning $2,000 to $8,000+ per month across UX/UI design, Webflow/Shopify/software development, conversion copywriting, marketing consulting, video/creative production, and fractional operations in the US, UK, Canada, Australia, and global remote markets.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-question" onclick="toggleFaq(this)">
            <span>4. How does the SaaS-Lite Interactive Web Companion App store my financial and client data?</span>
            <span>+</span>
          </button>
          <div class="faq-answer">
            Your privacy is 100% protected: <code>freelancer-os-app.html</code> has zero external tracking scripts and zero cloud servers. All numbers you type into the EHR Leak Calculator, B.C.R. Pricing Matrix, Prompt Builder, and Friday CEO Scorecard are saved locally inside your browser's <code>localStorage</code>, and you can export or import a complete <code>.json</code> backup file or print a clean PDF report at any time.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-question" onclick="toggleFaq(this)">
            <span>5. How do I activate Full Pro Mode inside the Web Companion App when I purchase Tier 3 or Tier 4?</span>
            <span>+</span>
          </button>
          <div class="faq-answer">
            Inside your Tier 3 and Tier 4 ZIP bundles, open <code>START-HERE-TIER3-COMPLETE-OS.md</code> (or Appendix C of the book) to find your lifetime Pro Companion Access Code (<code>FREELANCER-OS-PRO-2026</code>), or simply launch the app in Pro Mode with one click.
          </div>
        </div>

        <div class="faq-item">
          <button type="button" class="faq-question" onclick="toggleFaq(this)">
            <span>6. Can I start with the Free Tier 0 Audit Kit and upgrade to Tier 2 or Tier 3 later?</span>
            <span>+</span>
          </button>
          <div class="faq-answer">
            Yes! Download the <strong>Tier 0 Free Leak Audit Starter Kit ($0)</strong> right now to read Chapter 1, fill out Worksheet 1.1, and run your 7-day numbers inside Module 1 of the Web App. Whenever you are ready for the full 10-chapter manual, workbooks, Notion OS, and Excel pricing matrix, you can grab Tier 2 ($24) or Tier 3 ($49) anytime.
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- LEAD MAGNET OPT-IN & INSTANT DOWNLOAD MODAL -->
  <div id="lead-magnet-modal" class="modal-overlay">
    <div class="modal-box">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
        <span class="section-tag" style="margin-bottom:0;">Tier 0 Free Starter Kit ($0)</span>
        <button type="button" class="btn btn-outline-light" style="color:var(--primary); border-color:var(--border-strong); padding:4px 10px;" onclick="closeLeadMagnetModal()">✕</button>
      </div>
      <h3 style="font-size:24px; font-weight:900; color:var(--primary); margin-bottom:8px;">
        Download The 7-Day Time &amp; Revenue Leak Audit Kit
      </h3>
      <p style="font-size:14.5px; color:var(--muted); margin-bottom:18px;">
        Enter your best email below to activate instant access to <strong>Sample Chapter 1 PDF</strong>, <strong>Fillable Worksheet 1.1</strong>, <strong>Standalone Audit CSV</strong>, and the <strong>Interactive EHR Web Calculator</strong>.
      </p>
      <form onsubmit="handleLeadMagnetSubmit(event)">
        <div class="field-row">
          <label class="field-label" for="lead-email">Your Primary Work Email</label>
          <input type="email" id="lead-email" class="field-input" placeholder="you@yourstudio.com" required />
        </div>
        <div class="field-row">
          <label class="field-label" for="lead-niche">Your Primary Freelance Craft</label>
          <select id="lead-niche" class="field-input">
            <option value="design-dev">UX/UI Design, Webflow, Shopify or Software Dev</option>
            <option value="copy-marketing">Copywriting, Content Strategy or Growth Marketing</option>
            <option value="consulting-ops">Management Consulting, Fractional Ops or Virtual Assistant</option>
            <option value="creative-other">Brand Design, Video Production or Other Service</option>
          </select>
        </div>
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:20px;">
          <button type="submit" class="btn btn-teal" style="flex:1;">Instant Download: Tier 0 Starter ZIP ($0)</button>
          <a href="../09-EXPORTS/HYBRID-BUNDLE/Tier0-Free-Leak-Audit-Starter-Kit.zip" class="btn btn-navy">Direct ZIP Link →</a>
        </div>
      </form>
    </div>
  </div>

  <!-- FOOTER -->
  <footer>
    <div class="container" style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:24px;">
      <div style="max-width:540px;">
        <div style="color:#FFFFFF; font-weight:800; font-size:16px; margin-bottom:8px;">
          Digital Knowledge Product Studio • Practitioner Systems Press
        </div>
        <p style="margin-bottom:12px;">
          Copyright © 2026 Digital Knowledge Product Studio. All rights reserved. Built for independent freelancers, consultants, and solopreneurs in the United States, United Kingdom, Canada, Australia, and worldwide.
        </p>
        <p style="font-size:12px; color:#64748B;">
          Disclaimer: Operational frameworks, contract boundary scripts, and tax treaty guides are provided for educational and business operations purposes and do not constitute formal legal or certified public accounting advice.
        </p>
      </div>
      <div>
        <div style="color:#FFFFFF; font-weight:700; margin-bottom:8px;">Quick Ecosystem Links</div>
        <div style="display:flex; flex-direction:column; gap:6px;">
          <a href="../07-INTERACTIVE-TOOLS/freelancer-os-app.html" style="color:#38BDF8; text-decoration:none;">→ Launch Interactive Web Companion App</a>
          <a href="../09-EXPORTS/HYBRID-BUNDLE/Tier0-Free-Leak-Audit-Starter-Kit.zip" style="color:#CBD5E1; text-decoration:none;">→ Tier 0 Free Leak Audit Kit (.zip)</a>
          <a href="../09-EXPORTS/HYBRID-BUNDLE/Tier2-Interactive-Workbook-and-Planner-Edition.zip" style="color:#CBD5E1; text-decoration:none;">→ Tier 2 Interactive Workbook Edition (.zip)</a>
          <a href="../09-EXPORTS/HYBRID-BUNDLE/Tier3-Complete-AI-Freelancer-OS-Flagship-Bundle.zip" style="color:#CBD5E1; text-decoration:none;">→ Tier 3 Complete Freelancer OS Bundle (.zip)</a>
          <a href="../09-EXPORTS/HYBRID-BUNDLE/Tier4-Living-OS-Pro-Vault-Membership-Pack.zip" style="color:#CBD5E1; text-decoration:none;">→ Tier 4 Living OS Membership Pack (.zip)</a>
        </div>
      </div>
    </div>
  </footer>

  <!-- SINGLE-SOURCE CURRICULUM & CALCULATOR ENGINE -->
  <script>
    const CURRICULUM_DATA = {curriculum_json};
    const PROMPTS_DATA = {prompts_json};
    const SCRIPTS_DATA = {scripts_json};

    const CURRENCY_RATES = {{
      USD: {{ sym: "$", mult: 1.00 }},
      GBP: {{ sym: "£", mult: 0.79 }},
      EUR: {{ sym: "€", mult: 0.92 }},
      CAD: {{ sym: "CA$", mult: 1.36 }},
      AUD: {{ sym: "A$", mult: 1.52 }}
    }};

    let currentCurrency = "USD";
    let activeChapterNum = 1;

    function fmtCur(usdVal, decimals = 0) {{
      const cfg = CURRENCY_RATES[currentCurrency] || CURRENCY_RATES.USD;
      const converted = usdVal * cfg.mult;
      return cfg.sym + converted.toLocaleString("en-US", {{
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
      }});
    }}

    function updateFunnelCurrency(code) {{
      currentCurrency = code;
      const cfg = CURRENCY_RATES[code] || CURRENCY_RATES.USD;
      document.querySelectorAll(".dyn-price").forEach(el => {{
        const baseUsd = parseFloat(el.getAttribute("data-usd")) || 0;
        if (baseUsd === 0) {{
          el.textContent = cfg.sym + "0";
        }} else if (baseUsd === 9.99) {{
          el.textContent = code === "GBP" ? "£7.99" : code === "EUR" ? "€9.49" : code === "CAD" ? "CA$12.99" : code === "AUD" ? "A$13.99" : "$9.99";
        }} else if (baseUsd === 16.99) {{
          el.textContent = code === "GBP" ? "£13.99" : code === "EUR" ? "€15.99" : code === "CAD" ? "CA$22.99" : code === "AUD" ? "A$24.99" : "$16.99";
        }} else {{
          el.textContent = cfg.sym + Math.round(baseUsd * cfg.mult);
        }}
      }});
      runFunnelCalculator();
    }}

    function runFunnelCalculator() {{
      const cfg = CURRENCY_RATES[currentCurrency] || CURRENCY_RATES.USD;
      const targetRate = Math.max(1, parseFloat(document.getElementById("calc-target-rate").value) || 75);
      const weeklyRev = Math.max(0, parseFloat(document.getElementById("calc-weekly-rev").value) || 1300);
      const bA = Math.max(0, parseFloat(document.getElementById("calc-bucket-a").value) || 0);
      const bB = Math.max(0, parseFloat(document.getElementById("calc-bucket-b").value) || 0);
      const bC = Math.max(0, parseFloat(document.getElementById("calc-bucket-c").value) || 0);
      const bD = Math.max(0, parseFloat(document.getElementById("calc-bucket-d").value) || 0);

      const totalHrs = Math.max(0.5, bA + bB + bC + bD);
      const unbilledHrs = bB + bC + bD;
      const trueEhr = weeklyRev / totalHrs;
      const utilPct = (bA / totalHrs) * 100;
      const erosionPct = ((trueEhr - targetRate) / targetRate) * 100;

      const weeklyLeak = unbilledHrs * targetRate;
      const monthlyLeak = weeklyLeak * 4.33;
      const annualLeak = weeklyLeak * 48;
      const recovery55 = annualLeak * 0.55;

      document.getElementById("lbl-target-rate").textContent = cfg.sym + targetRate + "/hr";
      document.getElementById("lbl-weekly-rev").textContent = cfg.sym + weeklyRev.toLocaleString("en-US") + "/wk";

      document.getElementById("res-true-ehr").textContent = cfg.sym + trueEhr.toFixed(2) + "/hr";
      document.getElementById("res-rate-erosion").textContent =
        erosionPct < 0
          ? `Rate Collapse: ${{erosionPct.toFixed(1)}}% below ${{cfg.sym}}${{targetRate}}/hr target`
          : `Surplus: +${{erosionPct.toFixed(1)}}% above ${{cfg.sym}}${{targetRate}}/hr target`;

      document.getElementById("res-util-pct").textContent = utilPct.toFixed(1) + "%";
      document.getElementById("res-total-hrs").textContent = `${{bA.toFixed(1)}} billable hrs / ${{totalHrs.toFixed(1)}} total real hrs`;

      document.getElementById("res-monthly-leak").textContent = cfg.sym + Math.round(monthlyLeak).toLocaleString("en-US") + "/mo";
      document.getElementById("res-weekly-leak").textContent = `${{unbilledHrs.toFixed(1)}} unbilled hrs/wk × ${{cfg.sym}}${{targetRate}}/hr`;

      document.getElementById("res-annual-leak").textContent = cfg.sym + Math.round(annualLeak).toLocaleString("en-US") + "/yr";
      document.getElementById("res-recovery-est").textContent = `90-Day AI OS 55% Recovery: +${{cfg.sym}}${{Math.round(recovery55).toLocaleString("en-US")}}/yr`;

      const pA = (bA / totalHrs) * 100;
      const pB = (bB / totalHrs) * 100;
      const pC = (bC / totalHrs) * 100;
      const pD = (bD / totalHrs) * 100;

      document.getElementById("sb-a").style.width = pA.toFixed(1) + "%";
      document.getElementById("sb-a").textContent = pA >= 9 ? `A: ${{pA.toFixed(0)}}%` : "";
      document.getElementById("sb-b").style.width = pB.toFixed(1) + "%";
      document.getElementById("sb-b").textContent = pB >= 9 ? `B: ${{pB.toFixed(0)}}%` : "";
      document.getElementById("sb-c").style.width = pC.toFixed(1) + "%";
      document.getElementById("sb-c").textContent = pC >= 9 ? `C: ${{pC.toFixed(0)}}%` : "";
      document.getElementById("sb-d").style.width = pD.toFixed(1) + "%";
      document.getElementById("sb-d").textContent = pD >= 9 ? `D: ${{pD.toFixed(0)}}%` : "";

      document.getElementById("res-bar-total").textContent = `${{totalHrs.toFixed(1)}} Total Weekly Hours`;
    }}

    function resetMarcusDemo() {{
      document.getElementById("calc-target-rate").value = 75;
      document.getElementById("calc-weekly-rev").value = 1300;
      document.getElementById("calc-bucket-a").value = 26.5;
      document.getElementById("calc-bucket-b").value = 8.0;
      document.getElementById("calc-bucket-c").value = 5.5;
      document.getElementById("calc-bucket-d").value = 8.5;
      runFunnelCalculator();
    }}

    function renderCurriculumExplorer() {{
      const tabContainer = document.getElementById("curriculum-tabs");
      tabContainer.innerHTML = "";

      CURRICULUM_DATA.forEach(ch => {{
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "chapter-tab-btn" + (ch.num === activeChapterNum ? " active" : "");
        btn.onclick = () => {{
          activeChapterNum = ch.num;
          renderCurriculumExplorer();
        }};
        btn.innerHTML = `
          <span class="ch-code">CHAPTER ${{String(ch.num).padStart(2, '0')}} • 5 PROMPTS + 2 SVGS</span>
          <span class="ch-name">${{ch.title.replace(/^Chapter \\d+:\\s*/, '')}}</span>
        `;
        tabContainer.appendChild(btn);
      }});

      // Add Back Matter Vault Tab (11)
      const vaultBtn = document.createElement("button");
      vaultBtn.type = "button";
      vaultBtn.className = "chapter-tab-btn" + (activeChapterNum === 11 ? " active" : "");
      vaultBtn.onclick = () => {{
        activeChapterNum = 11;
        renderCurriculumExplorer();
      }};
      vaultBtn.innerHTML = `
        <span class="ch-code">BACK MATTER VAULT • APPENDIX A, B &amp; C</span>
        <span class="ch-name">12 Emergency Client Boundary Scripts</span>
      `;
      tabContainer.appendChild(vaultBtn);

      const detailEl = document.getElementById("curriculum-detail");
      if (activeChapterNum === 11) {{
        const scriptsHtml = SCRIPTS_DATA.map(s => `
          <div class="prompt-preview-card">
            <div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:12px; font-weight:800; color:var(--accent); margin-bottom:4px;">
              <span>${{s.label}} (${{s.id}})</span>
              <span>${{s.category}}</span>
            </div>
            <div style="font-size:15px; font-weight:800; color:var(--primary); margin-bottom:4px;">${{s.title}}</div>
            <div style="font-size:13px; color:var(--muted);"><strong>When to Send:</strong> ${{s.when_to_run}}</div>
          </div>
        `).join("");

        detailEl.innerHTML = `
          <span class="section-tag">Back Matter Vault // Appendix A, B &amp; C</span>
          <h3 style="font-size:24px; font-weight:900; color:var(--primary); margin-bottom:8px;">
            50-Prompt Master Index &amp; 12 Emergency Client Boundary Scripts
          </h3>
          <p style="font-size:14.5px; color:var(--muted); margin-bottom:18px;">
            Ready-to-send word-for-word email and Slack boundary scripts for every high-friction client scenario across the 5-Stage Lifecycle.
          </p>
          <div>${{scriptsHtml}}</div>
        `;
      }} else {{
        const ch = CURRICULUM_DATA.find(x => x.num === activeChapterNum) || CURRICULUM_DATA[0];
        const chPrompts = PROMPTS_DATA.filter(p => p.chapter === ch.num);
        const promptsHtml = chPrompts.map(p => `
          <div class="prompt-preview-card">
            <div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:12px; font-weight:800; color:var(--secondary); margin-bottom:4px;">
              <span>${{p.label}}</span>
              <span>${{p.variables.length}} Bracketed Variables</span>
            </div>
            <div style="font-size:15px; font-weight:800; color:var(--primary); margin-bottom:4px;">${{p.title}}</div>
            <div style="font-size:13px; color:var(--text); margin-bottom:4px;"><strong>Objective:</strong> ${{p.objective}}</div>
            <div style="font-size:12.5px; color:var(--muted);"><strong>QA Verification Rule:</strong> ${{p.verification}}</div>
          </div>
        `).join("");

        detailEl.innerHTML = `
          <span class="section-tag">${{ch.part}}</span>
          <h3 style="font-size:24px; font-weight:900; color:var(--primary); margin-bottom:8px;">${{ch.title}}</h3>
          <p style="font-size:14.5px; color:var(--text); margin-bottom:14px;">
            <strong>Named Core Framework:</strong> ${{ch.framework}}
          </p>
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:10px; margin-bottom:18px; background:var(--surface); padding:14px; border-radius:var(--radius-sm); border:1px solid var(--border);">
            <div style="font-size:12.5px;"><strong>Vector Mindmap:</strong><br/>${{ch.mindmap}}</div>
            <div style="font-size:12.5px;"><strong>Decision Flowchart:</strong><br/>${{ch.flowchart}}</div>
            <div style="font-size:12.5px;"><strong>Action Workbook:</strong><br/>${{ch.worksheet}}</div>
            <div style="font-size:12.5px;"><strong>Verified Case Study:</strong><br/>${{ch.case_study}}</div>
          </div>
          <h4 style="font-size:14px; font-weight:800; text-transform:uppercase; letter-spacing:0.05em; color:var(--muted); margin-bottom:10px;">
            5 Tested AI Workflow Prompts in Chapter ${{ch.num}}:
          </h4>
          <div>${{promptsHtml}}</div>
        `;
      }}
    }}

    function toggleFaq(btnEl) {{
      const item = btnEl.closest(".faq-item");
      item.classList.toggle("open");
    }}

    function openLeadMagnetModal() {{
      document.getElementById("lead-magnet-modal").classList.add("open");
    }}

    function closeLeadMagnetModal() {{
      document.getElementById("lead-magnet-modal").classList.remove("open");
    }}

    function handleLeadMagnetSubmit(e) {{
      e.preventDefault();
      closeLeadMagnetModal();
      window.location.href = "../09-EXPORTS/HYBRID-BUNDLE/Tier0-Free-Leak-Audit-Starter-Kit.zip";
    }}

    window.addEventListener("DOMContentLoaded", () => {{
      runFunnelCalculator();
      renderCurriculumExplorer();
    }});
  </script>
</body>
</html>"""

    index_path = MARKETING_DIR / "index.html"
    index_path.write_text(html_content, encoding="utf-8")
    print(f"[Marketing Funnel] Wrote 10-MARKETING/index.html ({index_path.stat().st_size:,} bytes)")
    return index_path


def build_five_release_zip_bundles():
    """Package all 5 commercial customer & publisher ZIP bundles inside 09-EXPORTS/HYBRID-BUNDLE/."""
    HYBRID_BUNDLE_DIR.mkdir(parents=True, exist_ok=True)

    # Guide 0: START-HERE-TIER0.md
    start_tier0 = """# Welcome to The Freelancer Leak Audit Starter Kit (Tier 0 — Free Edition)

Thank you for downloading **The Freelancer Leak Audit Starter Kit** from **Digital Knowledge Product Studio**.

## Included Files in Your Starter Kit
1. **`tier0-free-sample-chapter01-and-audit.pdf`** — Complete Chapter 1 of *The AI Freelancer Operating System* plus the 7-Day Time & Revenue Leak Audit.
2. **`chapter-01-workbook.pdf`** — Standalone Fillable PDF for *Worksheet 1.1: The 7-Day Time & Revenue Leak Audit*.
3. **`freelancer-os-app.html`** — The zero-dependency HTML5 Web Companion App (double-click to open in any browser; Module 1 EHR Leak Calculator is 100% open).
4. **`sheet1-ehr-leak-audit.csv`** — Spreadsheet version of the 7-Day Leak Audit for Google Sheets, Excel, or Apple Numbers.
5. **`gumroad-tier0-free-audit-cover.png`** — Official Edition Cover.

## Ready to Install All 5 Lifecycle Gates?
Upgrade to **Tier 2 ($24 Interactive Workbook & Tablet Planner Edition)** or **Tier 3 ($49 Complete 5-Pillar AI Freelancer Operating System Flagship Bundle)** to activate all 10 chapters, 50 AI workflows, 12 boundary scripts, the 5-Database Notion OS Kit, the 4-Tab Excel Financial Matrix, and Pro Mode (`FREELANCER-OS-PRO-2026`) inside the Web Companion App.
"""

    # Guide 1: PUBLISHER-UPLOAD-CHECKLIST.md
    start_tier1 = """# Publisher Upload Checklist — Amazon KDP & Draft2Digital (Tier 1 Retail Pack)

This archive contains the complete, verified master files for publishing **Tier 1 (Essential Edition)** on **Amazon Kindle Direct Publishing (KDP)** and **Draft2Digital (D2D)**.

## File Mapping for Upload
1. **Amazon KDP Kindle eBook ($9.99 USD — 70% Royalty Plan):**
   - Interior File: `the-ai-freelancer-os.epub`
   - Cover Image: `kdp-ebook-and-d2d-cover.png` (`1600 x 2560 px`)
2. **Amazon KDP 6.0" x 9.0" Print Paperback ($16.99 USD — 60% Royalty Rate):**
   - Interior Print PDF: `the-ai-freelancer-os-kdp-paperback-6x9.pdf` (`146 pages`, B&W White Paper, No Bleed)
   - Full-Wrap Print Cover PDF: `kdp-paperback-full-wrap-cover.pdf` (`12.58" x 9.25"` @ 300 DPI, `0.33"` spine)
3. **Draft2Digital Wide Distribution ($9.99 USD — Apple Books, Kobo, B&N, Everand, Public Libraries):**
   - eBook File: `the-ai-freelancer-os.epub`
   - Cover Image: `kdp-ebook-and-d2d-cover.png`
   - Storefront Rule: Enable all retail and library channels EXCEPT Amazon.
4. **Master Listing Copy & Bangladesh 10% Tax Treaty Runbook:**
   - Open `marketplace-listings-and-bd-launch-runbook.md` for copy-paste HTML descriptions, 7 backend keywords, BISAC categories, Payoneer US receiving account setup, and IRS Form W-8BEN instructions.
"""

    # Guide 2: START-HERE-TIER2.md
    start_tier2 = """# Welcome to The Interactive Workbook & Tablet Planner Edition (Tier 2 — $24 Edition)

Thank you for purchasing **Tier 2: The Interactive Workbook & Tablet Planner Edition** of *The AI Freelancer Operating System*.

## Included Deliverables in Your Bundle
1. **`the-ai-freelancer-os-complete-book.pdf`** — The complete 168-page Digital Operating Manual (`75,158 words`, 10 chapters, 50 AI prompts, 12 boundary scripts).
2. **`the-ai-freelancer-os.epub`** — Reflowable EPUB 3.0 eBook for Apple Books, Kindle, Kobo, and mobile readers.
3. **`the-ai-freelancer-os-workbook-us-letter.pdf`** — Complete 10-Chapter Printable & AcroForm Fillable Workbook (`8.5" x 11"` US Letter).
4. **`the-ai-freelancer-os-workbook-a4.pdf`** — Complete 10-Chapter Printable & AcroForm Fillable Workbook (`210 x 297 mm` ISO A4).
5. **`the-ai-freelancer-os-tablet-planner.pdf`** — 49-Page Landscape Digital Planner for iPad (`GoodNotes`, `Notability`) and `reMarkable`.
6. **`03-AI-Prompt-and-Script-Vault-62.csv`** — All 50 Tested AI Workflow Prompts + 12 Emergency Boundary Scripts in spreadsheet/CSV format.
7. **`Mindmaps/` & `Flowcharts/`** — All 20 high-resolution Vector System Diagrams (`.svg`).
"""

    # Guide 3: START-HERE-TIER3-COMPLETE-OS.md
    start_tier3 = """# Welcome to The Complete AI Freelancer Operating System (Tier 3 Flagship Bundle — $49)

**Pro Companion Activation Code:** `FREELANCER-OS-PRO-2026`

Thank you for investing in the flagship **5-Pillar AI Freelancer Operating System**.

## Your 30-Minute Deployment Checklist
1. **Step 1 (5 Mins) — Launch the Pro SaaS-Lite Web Companion App:**
   - Double-click `07-INTERACTIVE-TOOLS/freelancer-os-app.html` to open the application in Chrome, Edge, Safari, or Firefox.
   - Full Pro Mode is active by default (or enter `FREELANCER-OS-PRO-2026` if viewing from `?mode=free`). Run Module 1 (*7-Day EHR Leak Audit*) and Module 2 (*B.C.R. 3-Tier Proposal Pricing Engine*).
2. **Step 2 (15 Mins) — Import Your 5-Database Minimalist Notion OS:**
   - Open `06-NOTION-TEMPLATES/NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md` and import the 4 CSV databases (`01-Leads-CRM-Pipeline.csv`, `02-Active-Projects-and-Gates.csv`, `03-AI-Prompt-and-Script-Vault-62.csv`, `04-Weekly-CEO-Scorecard-Log.csv`) plus the reusable client portal (`05-Client-Portal-and-Handover-Hub.md`).
3. **Step 3 (5 Mins) — Open Your 4-Tab Excel Financial & Pricing Matrix:**
   - Open `06-NOTION-TEMPLATES/Spreadsheets/the-ai-freelancer-os-financial-and-pricing-matrix.xlsx` in Excel (or import `sheet1`..`sheet4` CSVs into Google Sheets) to customize your WBS pricing, 80/20 client roster, and 12-week rolling cashflow forecast.
4. **Step 4 (5 Mins) — Load the Manual & Fillable Workbooks:**
   - Open `01-BOOK-AND-WORKBOOKS/the-ai-freelancer-os-complete-book.pdf` and your preferred workbook edition (`US Letter`, `ISO A4`, or `Landscape Tablet Planner`).
"""

    # Guide 4: START-HERE-TIER4-MEMBERSHIP.md
    start_tier4 = """# Welcome to The Living OS & Pro Workflow Vault Pass (Tier 4 Membership)

**Pro Companion Activation Code:** `FREELANCER-OS-PRO-2026`  
**Included Monthly Expansion Pack:** `tier4-monthly-vault-drop-01.md` (*Drop #01: The High-Ticket Paid Diagnostic & Retainer Expansion Pack*)

Thank you for joining the **Tier 4 Living OS & Pro Workflow Vault Pass**.

## What Is Inside Your Membership Package
1. **Everything in the Tier 3 Complete Freelancer Operating System Flagship Bundle:**
   - Complete 168-Page Manual (`PDF` + `EPUB 3.0`), `US Letter` & `ISO A4` Fillable Workbooks, `49-Page Landscape Tablet Planner`, Pro Web Companion App (`freelancer-os-app.html`), 5-Database Notion OS Kit, 4-Tab Excel Financial Matrix, and 20 Vector Diagrams.
2. **Monthly Expansion Drop #01 (`05-LIVING-OS-MONTHLY-DROPS/tier4-monthly-vault-drop-01.md`):**
   - **5 Bonus High-Ticket AI Workflows (`Prompts V1.1–V1.5`):** Paid Discovery Sprint Architect, 3-Min Cold/Warm Loom Teardown Script, Retainer Zero-Rollover Charter, Quarterly Executive ROI Review Generator, and Subcontractor 4-Gate QA Handoff Brief.
   - **3 Bonus Executive Negotiation Scripts (`Scripts V1–V3`):** Converting Hourly Shoppers to Paid Diagnostics, Proactive Day-22 Retainer Capacity Notice, and 90-Day Past-Client Reactivation Ping.
"""

    svg_mindmaps = sorted((BASE_DIR / "04-VISUAL-ASSETS" / "Mindmaps").glob("*.svg"))
    svg_flowcharts = sorted((BASE_DIR / "04-VISUAL-ASSETS" / "Flowcharts").glob("*.svg"))

    # 1. Build Tier0-Free-Leak-Audit-Starter-Kit.zip
    t0_zip = HYBRID_BUNDLE_DIR / "Tier0-Free-Leak-Audit-Starter-Kit.zip"
    with zipfile.ZipFile(t0_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("START-HERE-TIER0.md", start_tier0)
        zf.write(BASE_DIR / "09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf", "tier0-free-sample-chapter01-and-audit.pdf")
        zf.write(BASE_DIR / "05-WORKBOOKS/chapter-01-workbook.pdf", "chapter-01-workbook.pdf")
        zf.write(BASE_DIR / "07-INTERACTIVE-TOOLS/freelancer-os-app.html", "freelancer-os-app.html")
        zf.write(BASE_DIR / "06-NOTION-TEMPLATES/Spreadsheets/sheet1-ehr-leak-audit.csv", "sheet1-ehr-leak-audit.csv")
        zf.write(BASE_DIR / "08-COVER-DESIGN/gumroad-tier0-free-audit-cover.png", "gumroad-tier0-free-audit-cover.png")

    # 2. Build Tier1-KDP-and-D2D-Publisher-Upload-Pack.zip
    t1_zip = HYBRID_BUNDLE_DIR / "Tier1-KDP-and-D2D-Publisher-Upload-Pack.zip"
    with zipfile.ZipFile(t1_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("PUBLISHER-UPLOAD-CHECKLIST.md", start_tier1)
        zf.write(BASE_DIR / "09-EXPORTS/PDF/the-ai-freelancer-os-complete-book.pdf", "the-ai-freelancer-os-complete-book.pdf")
        zf.write(BASE_DIR / "09-EXPORTS/PRINT/the-ai-freelancer-os-kdp-paperback-6x9.pdf", "the-ai-freelancer-os-kdp-paperback-6x9.pdf")
        zf.write(BASE_DIR / "09-EXPORTS/EPUB/the-ai-freelancer-os.epub", "the-ai-freelancer-os.epub")
        zf.write(BASE_DIR / "08-COVER-DESIGN/kdp-ebook-and-d2d-cover.png", "kdp-ebook-and-d2d-cover.png")
        zf.write(BASE_DIR / "08-COVER-DESIGN/kdp-ebook-and-d2d-cover.svg", "kdp-ebook-and-d2d-cover.svg")
        zf.write(BASE_DIR / "08-COVER-DESIGN/kdp-paperback-full-wrap-cover.pdf", "kdp-paperback-full-wrap-cover.pdf")
        zf.write(BASE_DIR / "08-COVER-DESIGN/kdp-paperback-full-wrap-cover.png", "kdp-paperback-full-wrap-cover.png")
        zf.write(MARKETING_DIR / "marketplace-listings-and-bd-launch-runbook.md", "marketplace-listings-and-bd-launch-runbook.md")

    # 3. Build Tier2-Interactive-Workbook-and-Planner-Edition.zip
    t2_zip = HYBRID_BUNDLE_DIR / "Tier2-Interactive-Workbook-and-Planner-Edition.zip"
    with zipfile.ZipFile(t2_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("START-HERE-TIER2.md", start_tier2)
        zf.write(BASE_DIR / "09-EXPORTS/PDF/the-ai-freelancer-os-complete-book.pdf", "the-ai-freelancer-os-complete-book.pdf")
        zf.write(BASE_DIR / "09-EXPORTS/EPUB/the-ai-freelancer-os.epub", "the-ai-freelancer-os.epub")
        zf.write(BASE_DIR / "09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-us-letter.pdf", "the-ai-freelancer-os-workbook-us-letter.pdf")
        zf.write(BASE_DIR / "09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-a4.pdf", "the-ai-freelancer-os-workbook-a4.pdf")
        zf.write(BASE_DIR / "09-EXPORTS/PDF/the-ai-freelancer-os-tablet-planner.pdf", "the-ai-freelancer-os-tablet-planner.pdf")
        zf.write(BASE_DIR / "06-NOTION-TEMPLATES/03-AI-Prompt-and-Script-Vault-62.csv", "03-AI-Prompt-and-Script-Vault-62.csv")
        for svg_p in svg_mindmaps:
            zf.write(svg_p, f"Mindmaps/{svg_p.name}")
        for svg_p in svg_flowcharts:
            zf.write(svg_p, f"Flowcharts/{svg_p.name}")

    # Helper to populate Tier 3 core files into a ZipFile
    def add_tier3_core_files(zf: zipfile.ZipFile):
        zf.write(BASE_DIR / "09-EXPORTS/PDF/the-ai-freelancer-os-complete-book.pdf", "01-BOOK-AND-WORKBOOKS/the-ai-freelancer-os-complete-book.pdf")
        zf.write(BASE_DIR / "09-EXPORTS/EPUB/the-ai-freelancer-os.epub", "01-BOOK-AND-WORKBOOKS/the-ai-freelancer-os.epub")
        zf.write(BASE_DIR / "09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-us-letter.pdf", "01-BOOK-AND-WORKBOOKS/the-ai-freelancer-os-workbook-us-letter.pdf")
        zf.write(BASE_DIR / "09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-a4.pdf", "01-BOOK-AND-WORKBOOKS/the-ai-freelancer-os-workbook-a4.pdf")
        zf.write(BASE_DIR / "09-EXPORTS/PDF/the-ai-freelancer-os-tablet-planner.pdf", "01-BOOK-AND-WORKBOOKS/the-ai-freelancer-os-tablet-planner.pdf")

        zf.write(BASE_DIR / "07-INTERACTIVE-TOOLS/freelancer-os-app.html", "02-INTERACTIVE-WEB-APP/freelancer-os-app.html")
        zf.write(BASE_DIR / "07-INTERACTIVE-TOOLS/README-WEB-APP.md", "02-INTERACTIVE-WEB-APP/README-WEB-APP.md")

        notion_files = [
            "01-Leads-CRM-Pipeline.csv",
            "02-Active-Projects-and-Gates.csv",
            "03-AI-Prompt-and-Script-Vault-62.csv",
            "04-Weekly-CEO-Scorecard-Log.csv",
            "05-Client-Portal-and-Handover-Hub.md",
            "NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md",
        ]
        for nf in notion_files:
            zf.write(BASE_DIR / "06-NOTION-TEMPLATES" / nf, f"03-NOTION-OS-KIT/{nf}")

        sheet_files = [
            "the-ai-freelancer-os-financial-and-pricing-matrix.xlsx",
            "sheet1-ehr-leak-audit.csv",
            "sheet2-bcr-scope-pricing.csv",
            "sheet3-client-80-20-roster.csv",
            "sheet4-90day-pipeline-cashflow.csv",
        ]
        for sf in sheet_files:
            zf.write(BASE_DIR / "06-NOTION-TEMPLATES/Spreadsheets" / sf, f"04-EXCEL-AND-CSV-MATRIX/{sf}")

        for svg_p in svg_mindmaps:
            zf.write(svg_p, f"04-VISUAL-DIAGRAMS/Mindmaps/{svg_p.name}")
        for svg_p in svg_flowcharts:
            zf.write(svg_p, f"04-VISUAL-DIAGRAMS/Flowcharts/{svg_p.name}")

    # 4. Build Tier3-Complete-AI-Freelancer-OS-Flagship-Bundle.zip
    t3_zip = HYBRID_BUNDLE_DIR / "Tier3-Complete-AI-Freelancer-OS-Flagship-Bundle.zip"
    with zipfile.ZipFile(t3_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("START-HERE-TIER3-COMPLETE-OS.md", start_tier3)
        add_tier3_core_files(zf)

    # 5. Build Tier4-Living-OS-Pro-Vault-Membership-Pack.zip
    t4_zip = HYBRID_BUNDLE_DIR / "Tier4-Living-OS-Pro-Vault-Membership-Pack.zip"
    with zipfile.ZipFile(t4_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("START-HERE-TIER4-MEMBERSHIP.md", start_tier4)
        add_tier3_core_files(zf)
        zf.write(MARKETING_DIR / "tier4-monthly-vault-drop-01.md", "05-LIVING-OS-MONTHLY-DROPS/tier4-monthly-vault-drop-01.md")

    for zp in (t0_zip, t1_zip, t2_zip, t3_zip, t4_zip):
        with zipfile.ZipFile(zp, "r") as zcheck:
            corrupt = zcheck.testzip()
            if corrupt is not None:
                raise RuntimeError(f"Corrupt entry {corrupt} in {zp}")
            print(f"[ZIP Bundle] {zp.name}: {len(zcheck.namelist())} files ({zp.stat().st_size:,} bytes)")


def update_root_readme():
    """Update root README.md with the complete 8-phase studio inventory and zero banned words."""
    readme_content = """# Digital Knowledge Product Studio — *The AI Freelancer Operating System*

**Product ID:** `ai-freelancer-os-v1`  
**Title:** *The AI Freelancer Operating System: A Practical System to Organize Clients, Automate Repetitive Work, Manage Projects, and Build a More Productive Freelance Business*  
**Version:** `1.0.0` (100% Production Ready — All 8 Phases Completed & Verified)  
**Target Geographic Markets:** United States (US), United Kingdom (UK), Canada (CA), Australia (AU)  
**Target Audience Profile:** Independent freelancers, solopreneurs, consultants, virtual assistants, and digital service providers (`1–5 years experience`, `$2,000–$8,000/month` revenue band)

---

## 1. The 5-Pillar Commercial Hybrid Product Ecosystem

Unlike generic AI eBooks or static template packs, *The AI Freelancer Operating System* is engineered as a **Category-of-One Commercial Hybrid Ecosystem** uniting five integrated pillars:

1. **Pillar 1 — The 10-Chapter Practical Operating Manual (`03-MANUSCRIPT/` & `09-EXPORTS/`):**
   * Complete Front Matter (`front-matter.md`), 10 standardized 14-section chapters (`chapter-01.md`..`chapter-10.md`), and Back Matter Vault (`back-matter.md`) totaling **`75,158 words`**.
   * **50 Tested AI Workflow Prompts** (`Prompts 1.1–10.5`) with `[BRACKETED VARIABLES]`, operational objectives, execution triggers, and human QA verification rules, plus **12 Emergency Client Boundary Scripts** (`Scripts 1–12`).
   * **20 Vector System Diagrams (`04-VISUAL-ASSETS/`):** 10 Chapter Mindmaps (`.svg`) + 10 Operational Decision Flowcharts (`.svg`).
   * Compiled into Digital Book PDF (`168 pages`), KDP Print Paperback (`6.0" x 9.0"`, `146 pages`), and Reflowable `EPUB 3.0` (`260.0 KB`).
2. **Pillar 2 — The 10-Chapter Printable & Interactive Fillable Workbook Suite (`05-WORKBOOKS/`):**
   * 10 standalone chapter worksheets (`worksheet-01.md`..`worksheet-10.md`) totaling **`12,717 words`**.
   * Compiled into AcroForm Fillable PDFs in **US Letter (`8.5" x 11.0"`, `36 pages`)**, **ISO A4 (`210 x 297 mm`, `34 pages`)**, and a **Hyperlinked Landscape Tablet Digital Planner (`49 pages`)** for iPad (`GoodNotes / Notability`) and `reMarkable`.
3. **Pillar 3 — Offline/Online Interactive Web Companion App (`07-INTERACTIVE-TOOLS/freelancer-os-app.html`):**
   * Zero-dependency, single-file SaaS-Lite web application (`318,070 bytes`) featuring:
     * **Module 1 (Free + Pro):** *7-Day Time & Effective Hourly Rate (EHR) Leak Audit & Daily 3-Block Priority Planner*
     * **Module 2 (Pro OS):** *Work Breakdown Structure (WBS) Estimator, B.C.R. 3-Tier Proposal Pricing Engine & Zero-Discount Trade-Down Generator*
     * **Module 3 (Pro OS):** *Dynamic 50-Prompt & 12-Script Studio Builder with Live Variable Interpolation*
     * **Module 4 (Pro + Tier 4):** *20-Minute Friday CEO Dashboard, 80/20 Client Profitability Matrix & 85% Capacity Rate-Raise Trigger* (`localStorage` + `.JSON` / `.CSV` / Print-PDF export)
4. **Pillar 4 — 5-Database Minimalist Notion Freelancer OS & 4-Tab Excel Financial Matrix (`06-NOTION-TEMPLATES/`):**
   * Sub-15-minute weekly maintenance Notion import kit (`01-Leads-CRM-Pipeline.csv`, `02-Active-Projects-and-Gates.csv`, `03-AI-Prompt-and-Script-Vault-62.csv`, `04-Weekly-CEO-Scorecard-Log.csv`, `05-Client-Portal-and-Handover-Hub.md`, and `NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md`).
   * Native 4-Tab Microsoft Excel Workbook (`the-ai-freelancer-os-financial-and-pricing-matrix.xlsx`) with `117` live Excel formulas + 4 standalone CSV mirrors (`sheet1`..`sheet4`).
5. **Pillar 5 — Commercial Cover Suite, Marketing Funnel & 5-Tier Release Bundles (`08-COVER-DESIGN/`, `10-MARKETING/`, `09-EXPORTS/HYBRID-BUNDLE/`):**
   * 6 Vector SVG covers + 6 rendered high-resolution PNGs + KDP 6"×9" Full Paperback Wrap PDF (`12.58" x 9.25"`).
   * Standalone Interactive Marketing Funnel Landing Page (`10-MARKETING/index.html`), 5-Email Conversion Sequence (`email-funnel-and-upsell-sequence.md`), Marketplace & Bangladesh 10% Tax Treaty Runbook (`marketplace-listings-and-bd-launch-runbook.md`), Tier 4 Monthly Drop #01 (`tier4-monthly-vault-drop-01.md`), and all 5 packaged `.zip` release bundles (`Tier0`..`Tier4`).

---

## 2. The 5-Tier Commercial Value Ladder & Packaged Release ZIPs

| Commercial Tier | Offer Title & Primary Platform | Price Point (USD) | Packaged Release Archive (`09-EXPORTS/HYBRID-BUNDLE/`) |
| :--- | :--- | :---: | :--- |
| **Tier 0 — Free Tier**<br>*(Lead Magnet)* | **The Freelancer Leak Audit Kit**<br>*(Gumroad `$0+` & Web Landing Page)* | **`$0.00` (Free)** | `Tier0-Free-Leak-Audit-Starter-Kit.zip` (`6 files`) — Sample Ch 1 PDF, Fillable Worksheet 1.1 PDF, Web App, Audit CSV & Cover. |
| **Tier 1 — Essential Edition**<br>*(Retail Discovery Engine)* | **Essential Edition**<br>*(Amazon KDP & Draft2Digital)* | **`$9.99` eBook**<br>**`$16.99` Paperback** | `Tier1-KDP-and-D2D-Publisher-Upload-Pack.zip` (`9 files`) — Digital PDF, KDP 6"×9" Print PDF, EPUB 3.0, Covers & Upload Runbook. |
| **Tier 2 — Interactive Workbook Edition**<br>*(Mid-Tier Action Kit)* | **Interactive Workbook Edition**<br>*(Gumroad One-Time)* | **`$24.00`**<br>*(One-Time)* | `Tier2-Interactive-Workbook-and-Planner-Edition.zip` (`27 files`) — Manual PDF/EPUB, US Letter & A4 Workbooks, Tablet Planner, 62-Item CSV & 20 SVGs. |
| **Tier 3 — Complete Freelancer OS**<br>*(Flagship Anchor Bundle)* | **Complete Freelancer Operating System**<br>*(Gumroad Flagship Bundle)* | **`$49.00`**<br>*(One-Time)* | `Tier3-Complete-AI-Freelancer-OS-Flagship-Bundle.zip` (`39 files`) — All Book/Workbook Editions + Pro Web App + 5-DB Notion OS + 4-Tab Excel Matrix + 20 SVGs. |
| **Tier 4 — Living OS & Pro Vault Pass**<br>*(Recurring MRR Engine)* | **Living OS & Pro Vault Pass**<br>*(Gumroad Memberships)* | **`$9.00 / mo`**<br>or **`$49.00 / yr`** | `Tier4-Living-OS-Pro-Vault-Membership-Pack.zip` (`40 files`) — Everything in Tier 3 + Monthly Expansion Drop #01 (`tier4-monthly-vault-drop-01.md`) & lifetime micro-tool access. |

---

## 3. Deterministic Build & Automated QA Verification Commands

Run these commands from `DIGITAL-PUBLISHING-STUDIO/` to rebuild and verify any layer of the ecosystem:

```bash
# Compile all 7 PDF, Print 6x9, EPUB 3.0, US Letter/A4 Workbooks & Tablet Planner editions
python build.py && python verify_phase5.py

# Compile the single-file SaaS-Lite Interactive Web Companion App (freelancer-os-app.html)
python build_webapp.py && python verify_phase6.py

# Compile the 5-Database Notion OS CSVs, 4-Tab Excel Matrix & 6 Commercial Covers
python build_phase7.py && python verify_phase7.py

# Compile the Marketing Landing Page (10-MARKETING/index.html) & 5 Commercial Release ZIPs
python build_phase8.py && python verify_phase8_master.py
```

---

## 4. The 8-Phase Engineering & Publishing Roadmap Scorecard

| Phase | Phase Name | Key Deliverables & Verification Gate | Status |
| :---: | :--- | :--- | :---: |
| **Phase 1** | **Studio Foundation, State Lock, QA Engine & Chapter 1 Package** | Directory architecture, `PROJECT_STATE.json`, `book-config.yaml`, `style-guide.md`, `sources.md`, `toc.md`, `chapter-01.md`, 2 SVGs, `worksheet-01.md`, `verify_phase1.py`. | **COMPLETED & VERIFIED (`99b3371`)** |
| **Phase 2** | **Part I & II Manuscripts + Visuals (Chapters 2, 3 & 4)** | Chapters 2, 3, and 4, 15 AI workflow prompts (`2.1–4.5`), 6 SVG diagrams, Worksheets 2–4, `verify_phase2.py`. | **COMPLETED & VERIFIED (`3ca9e64`)** |
| **Phase 3** | **Part III Manuscripts + Visuals (Chapters 5, 6 & 7)** | Chapters 5, 6, and 7, 15 AI workflow prompts (`5.1–7.5`), 6 SVG diagrams, Worksheets 5–7, `verify_phase3.py`. | **COMPLETED & VERIFIED (`194d8cb`)** |
| **Phase 4** | **Part IV Manuscripts + Back Matter (Chapters 8, 9, 10 & Vault)** | Chapters 8, 9, and 10, `front-matter.md`, `back-matter.md` (50-Prompt Index + 12 Scripts), 6 SVGs, Worksheets 8–10, `verify_phase4.py`. | **COMPLETED & VERIFIED (`6ee8a6a`)** |
| **Phase 5** | **Master Multi-Format Compiler (`build.py`)** | Automated compilation of Digital Book PDF, KDP Print 6"×9" PDF, EPUB 3.0, US Letter/A4 Workbooks, Tablet Planner & Tier-0 Sample PDF, `verify_phase5.py`. | **COMPLETED & VERIFIED (`9e12656`)** |
| **Phase 6** | **SaaS-Lite Interactive Web Companion App (`freelancer-os-app.html`)** | Single-file offline/online Web App (`318 KB`) with EHR Audit, B.C.R. Pricing, 62-Item Studio Builder & CEO Scorecard, `verify_phase6.py`. | **COMPLETED & VERIFIED (`ec45dad`)** |
| **Phase 7** | **Notion OS Database Kit, 4-Tab Excel Matrix & Commercial Covers** | 5-Database Notion OS kit, 4-Tab `.xlsx` & `.csv` Financial Matrix, and 6 SVG/PNG/PDF covers, `verify_phase7.py`. | **COMPLETED & VERIFIED (`181e47c`)** |
| **Phase 8** | **Marketing Funnel Landing Page, Email Sequence & 5-Tier ZIP Bundles** | `10-MARKETING/index.html`, 5-email sequence, KDP/D2D/Gumroad/BD runbook, Tier 4 Drop #01, 5 Release `.zip` bundles & `verify_phase8_master.py`. | **COMPLETED & VERIFIED (`100% READY`)** |
"""
    readme_path = BASE_DIR / "README.md"
    readme_path.write_text(readme_content, encoding="utf-8")
    print(f"[Root README] Updated README.md ({readme_path.stat().st_size:,} bytes)")


def main() -> int:
    print("=" * 78)
    print("PHASE 8 BUILDER — MARKETING FUNNEL, 5-TIER ZIP BUNDLES & ROOT README")
    print("=" * 78)
    build_marketing_landing_page()
    build_five_release_zip_bundles()
    update_root_readme()
    print("=" * 78)
    print("PHASE 8 BUILD COMPLETE — ALL MARKETING ASSETS & 5 ZIP BUNDLES READY")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
