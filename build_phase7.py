#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 7 Deterministic Builder Script (build_phase7.py)
The AI Freelancer Operating System — Digital Knowledge Product Studio

Builds:
- SUITE A: The 5-Database Minimalist Notion Freelancer OS Import Kit (06-NOTION-TEMPLATES/)
  1. 01-Leads-CRM-Pipeline.csv (14 realistic prospect rows across all 7 stages)
  2. 02-Active-Projects-and-Gates.csv (12 realistic project/retainer rows across all 5 gates)
  3. 03-AI-Prompt-and-Script-Vault-62.csv (62 rows: 50 Prompts 1.1-10.5 + 12 Scripts S1-S12)
  4. 04-Weekly-CEO-Scorecard-Log.csv (12 rows: Week 01 to Week 12 progression from $26.80/hr to $58.40/hr)
  5. Verifies 05-Client-Portal-and-Handover-Hub.md & NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md
- SUITE B: Multi-Tab Editable Excel (.xlsx) & CSV Financial & Pricing Matrix (06-NOTION-TEMPLATES/Spreadsheets/)
  1. the-ai-freelancer-os-financial-and-pricing-matrix.xlsx (+ synced copy in 09-EXPORTS/HYBRID-BUNDLE/)
  2. sheet1-ehr-leak-audit.csv, sheet2-bcr-scope-pricing.csv, sheet3-client-80-20-roster.csv, sheet4-90day-pipeline-cashflow.csv
- SUITE C: Commercial High-Resolution Book & Bundle Cover Design Suite (08-COVER-DESIGN/)
  1. kdp-ebook-and-d2d-cover.svg + .png (1600x2560)
  2. kdp-paperback-full-wrap-cover.svg + .pdf + .png (3774x2775 / 12.58in x 9.25in)
  3. gumroad-tier0-free-audit-cover.svg + .png (1280x720)
  4. gumroad-tier2-workbook-edition-cover.svg + .png (1280x720)
  5. gumroad-tier3-complete-os-cover.svg + .png (1280x720)
  6. gumroad-tier4-living-os-membership-cover.svg + .png (1280x720)
"""

import csv
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from build_webapp import extract_all_prompts, extract_all_scripts

BASE_DIR = Path(__file__).resolve().parent
NOTION_DIR = BASE_DIR / "06-NOTION-TEMPLATES"
SPREADSHEETS_DIR = NOTION_DIR / "Spreadsheets"
COVERS_DIR = BASE_DIR / "08-COVER-DESIGN"
HYBRID_BUNDLE_DIR = BASE_DIR / "09-EXPORTS" / "HYBRID-BUNDLE"


def find_headless_browser() -> str:
    """Locate Microsoft Edge or Google Chrome on Windows for high-res PNG and PDF rendering."""
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path_str in candidates:
        if Path(path_str).exists():
            return path_str
    raise RuntimeError("No headless Chromium browser (msedge.exe or chrome.exe) found on system.")


def write_csv_utf8(path: Path, headers: list[str], rows: list[list]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        writer.writerows(rows)


# ==============================================================================
# SUITE A: 5-DATABASE MINIMALIST NOTION FREELANCER OS IMPORT KIT
# ==============================================================================
def build_notion_suite():
    NOTION_DIR.mkdir(parents=True, exist_ok=True)

    # 1. 01-Leads-CRM-Pipeline.csv (14 rows across all 7 pipeline stages)
    leads_headers = [
        "Lead ID",
        "Prospect / Contact Name",
        "Company / Brand",
        "Pipeline Stage",
        "Service Category",
        "Fit Score (0-20)",
        "Red Flags Detected",
        "Recommended Package Tier",
        "Quoted Package Price ($)",
        "Win Probability (%)",
        "Weighted Pipeline Value ($)",
        "B.R.I.E.F. Core Bottleneck",
        "Next Action Date",
        "Assigned AI Prompt ID",
        "Contact Email",
    ]
    leads_rows = [
        [
            "LD-2026-001",
            "Elena Rostova",
            "Apex FinTech Cloud",
            "05 Closed Won",
            "UX/UI & Webflow Architecture",
            19,
            "None — Clear SPOC & Approved Budget",
            "Option 3: Turnkey & Retainer Partner",
            6800,
            100,
            6800,
            "Trial-to-paid onboarding drop-off costing $14k/mo in lost ARR",
            "2026-11-02",
            "Prompt 3.3",
            "e.rostova@apexfintech.io",
        ],
        [
            "LD-2026-002",
            "Marcus Tan",
            "Verde Beverage Co.",
            "05 Closed Won",
            "Brand & Packaging Sprint",
            18,
            "None — Fast Decision Authority",
            "Option 2: Core Transformation",
            4950,
            100,
            4950,
            "Retail distributor deadline requires 5-SKU dieline overhaul in 21 days",
            "2026-11-04",
            "Prompt 4.2",
            "m.tan@verdebev.com",
        ],
        [
            "LD-2026-003",
            "Hannah Abbott",
            "Clarity Health Analytics",
            "04 Verbal Approval / Contract Sent",
            "Conversion Copy & Funnel Build",
            17,
            "Minor: Legal review takes 3 business days",
            "Option 2: Core Transformation",
            5400,
            85,
            4590,
            "Enterprise demo booking page converts at only 1.1% vs 3.5% benchmark",
            "2026-10-24",
            "Prompt 5.1",
            "habbott@clarityhealth.ai",
        ],
        [
            "LD-2026-004",
            "Devon Brooks",
            "Kinetix Robotics",
            "04 Verbal Approval / Contract Sent",
            "Productized Design System",
            18,
            "None — Executive Sponsor Direct",
            "Option 3: Turnkey & Retainer Partner",
            7500,
            80,
            6000,
            "Fragmented UI component library slowing down 6 front-end engineers",
            "2026-10-25",
            "Prompt 4.4",
            "dbrooks@kinetixbot.com",
        ],
        [
            "LD-2026-005",
            "Liam O'Connor",
            "HarborView PropTech",
            "03 3-Tier Proposal Sent",
            "SaaS Onboarding & Lifecycle Emails",
            16,
            "Asked for 15% discount — routed to Script 4 trade-down",
            "Option 2: Core Transformation",
            4600,
            60,
            2760,
            "42% of new landlord signups stall before connecting bank feed",
            "2026-10-26",
            "Prompt 4.3",
            "liam@harborview.co.uk",
        ],
        [
            "LD-2026-006",
            "Sophia Chen",
            "Luminary EdTech",
            "03 3-Tier Proposal Sent",
            "Webflow Migration & Technical SEO",
            17,
            "None — Budget pre-approved for Q4",
            "Option 2: Core Transformation",
            5200,
            65,
            3380,
            "Legacy WordPress site failing Core Web Vitals and losing organic rankings",
            "2026-10-27",
            "Prompt 3.3",
            "sophia@luminaryed.ca",
        ],
        [
            "LD-2026-007",
            "Noah Patel",
            "Vanguard Supply Chain",
            "03 3-Tier Proposal Sent",
            "B2B Case Study & Sales Enablement",
            15,
            "3 stakeholders on committee — require SPOC designation",
            "Option 1: Essential Baseline",
            3400,
            50,
            1700,
            "Enterprise sales team lacks quantified ROI case studies for Q1 outbound",
            "2026-10-28",
            "Prompt 3.5",
            "n.patel@vanguardsc.com",
        ],
        [
            "LD-2026-008",
            "Chloe Sterling",
            "Aura Skincare Labs",
            "02 B.R.I.E.F. Qualified",
            "Shopify Plus Checkout Optimization",
            16,
            "None — Completed async intake form in 4 hours",
            "Option 2: Core Transformation",
            4800,
            40,
            1920,
            "Mobile cart abandonment spiked to 74% after theme update",
            "2026-10-25",
            "Prompt 3.2",
            "chloe@auraskincare.com.au",
        ],
        [
            "LD-2026-009",
            "Julian Vance",
            "Stratos Legal Ops",
            "02 B.R.I.E.F. Qualified",
            "AI Workflow & SOP Automation",
            14,
            "Unclear technical stack — pitch Paid Diagnostic Blueprint first",
            "Option 1: Paid Diagnostic Blueprint",
            1250,
            45,
            563,
            "Paralegal team spending 18 hrs/wk manually formatting intake briefs",
            "2026-10-26",
            "Prompt 3.4",
            "jvance@stratoslegal.com",
        ],
        [
            "LD-2026-010",
            "Amara Okafor",
            "Pulse Fitness Collective",
            "01 Discovery Intake",
            "Landing Page & Lead Magnet Funnel",
            13,
            "Pending budget confirmation via Script 1 async filter",
            "Option 1: Essential Baseline",
            2950,
            25,
            738,
            "Launching corporate wellness tier without dedicated B2B capture funnel",
            "2026-10-24",
            "Prompt 3.1",
            "amara@pulsefitness.io",
        ],
        [
            "LD-2026-011",
            "Lucas Meyer",
            "Nordic CleanTech",
            "01 Discovery Intake",
            "Investor Deck & Financial Data Vis",
            16,
            "Tight 14-day timeline — apply 1.30x complexity multiplier",
            "Option 2: Core Transformation",
            4500,
            30,
            1350,
            "Series A roadshow starts Nov 18; current narrative lacks unit economics clarity",
            "2026-10-24",
            "Prompt 3.1",
            "l.meyer@nordiccleantech.org",
        ],
        [
            "LD-2026-012",
            "Rachel Greenwald",
            "Summit SaaS Advisory",
            "06 60-Day Nurture",
            "Full Website Repositioning",
            16,
            "None — Q4 budget frozen until Jan 1 fiscal reset",
            "Option 2: Core Transformation",
            5500,
            20,
            1100,
            "Shifting ICP from SMB to mid-market; scheduled for January kickoff",
            "2026-12-15",
            "Prompt 2.4",
            "rachel@summitadvisory.com",
        ],
        [
            "LD-2026-013",
            "Trevor Blake",
            "Stealth Crypto App",
            "07 Disqualified — Red Flag",
            "Full-Stack MVP Build",
            6,
            "RED FLAG: Refused deposit, demanded free spec work & $800 total budget",
            "Disqualified — Sent Script 1 Decline",
            0,
            0,
            0,
            "Unfunded concept demanding 120 hours of custom engineering for $800",
            "2026-10-21",
            "Prompt 3.2",
            "trevor@stealthapp.xyz",
        ],
        [
            "LD-2026-014",
            "Dana Kowalski",
            "Bespoke Events Co.",
            "07 Disqualified — Red Flag",
            "Ad-Hoc Graphic Design",
            8,
            "RED FLAG: Wants 24/7 Slack availability & unlimited revisions below floor",
            "Disqualified — Sent Partner Referral",
            0,
            0,
            0,
            "Seeks reactive hourly task-runner rather than structured productized sprint",
            "2026-10-21",
            "Prompt 3.2",
            "dana@bespokeevents.net",
        ],
    ]
    write_csv_utf8(NOTION_DIR / "01-Leads-CRM-Pipeline.csv", leads_headers, leads_rows)

    # 2. 02-Active-Projects-and-Gates.csv (12 rows across all 5 Lifecycle Gates)
    projects_headers = [
        "Project ID",
        "Project / Retainer Name",
        "Client Company",
        "Current Lifecycle Gate",
        "Offer Tier",
        "Contract Value ($)",
        "Deposit Status",
        "48h Asset Gate Status",
        "Quoted B.C.R. Hours",
        "Actual Hours Logged",
        "Live Project EHR ($/hr)",
        "Target EHR ($/hr)",
        "Revision Rounds Used (Max 2)",
        "Captured Change Orders ($)",
        "Friction Score (1-5)",
        "80/20 Client Action Flag",
        "Target Delivery Date",
        "Next Milestone Deliverable",
    ]
    projects_rows = [
        [
            "PRJ-2026-101",
            "Apex FinTech Growth & CRO Retainer",
            "Apex FinTech Cloud",
            "Gate 5: Offboard & Retain",
            "Tier 3 Monthly Retainer",
            2800,
            "Paid — Auto-ACH Day 1",
            "100% Verified",
            28.0,
            24.0,
            116.67,
            85.00,
            "1 of 2 Used",
            0,
            1,
            "RETAIN & EXPAND (Star Account)",
            "2026-11-30",
            "Monthly Q4 Conversion Experiment Batch #2",
        ],
        [
            "PRJ-2026-102",
            "Verde 5-SKU Packaging & Brand Sprint",
            "Verde Beverage Co.",
            "Gate 4: Execute & Protect",
            "Option 2: Core Transformation",
            4950,
            "50% Deposit + 25% M1 Paid",
            "100% Verified",
            48.0,
            41.5,
            130.12,
            85.00,
            "1 of 2 Used",
            450,
            2,
            "RETAIN & EXPAND (Pitch Retainer via Script 11)",
            "2026-11-14",
            "Final Print-Ready Dieline Package & 3D Mockups",
        ],
        [
            "PRJ-2026-103",
            "NorthStar Legacy Logistics Portal",
            "NorthStar Logistics",
            "Gate 4: Execute & Protect",
            "Legacy Custom Scope",
            1500,
            "50% Deposit Paid",
            "Partial — Chased 3x",
            18.0,
            29.5,
            50.85,
            85.00,
            "2 of 2 Used",
            0,
            5,
            "PRUNE / REPLACE NEXT QUARTER (Whale Trap)",
            "2026-11-05",
            "Final Handover + Issue Script 12 (+25% Rate Reset or Exit)",
        ],
        [
            "PRJ-2026-104",
            "Clarity Health Maintenance Retainer",
            "Clarity Health Analytics",
            "Gate 5: Offboard & Retain",
            "Option A Essential Retainer",
            1250,
            "Paid — Auto-Stripe Day 1",
            "100% Verified",
            12.0,
            9.5,
            131.58,
            85.00,
            "1 of 2 Used",
            0,
            1,
            "RETAIN & EXPAND (Upsell to Option B $2,400/mo)",
            "2026-11-30",
            "Monthly Core Web Vitals & Landing Page QA Audit",
        ],
        [
            "PRJ-2026-105",
            "VantagePoint SaaS Onboarding Redesign",
            "VantagePoint Software",
            "Gate 4: Execute & Protect",
            "Option 2: Core Transformation",
            5400,
            "50% Deposit Paid ($2,700)",
            "100% Verified",
            52.0,
            46.0,
            131.52,
            85.00,
            "1 of 2 Used",
            650,
            2,
            "RETAIN & EXPAND (High-Yield Sprint)",
            "2026-11-18",
            "Milestone 2 Interactive Figma Prototype + 3-Min Loom",
        ],
        [
            "PRJ-2026-106",
            "Solstice E-Commerce PDP Overhaul",
            "Solstice Apparel Group",
            "Gate 3: Onboard & Align",
            "Option 2: Core Transformation",
            4400,
            "50% Deposit Paid ($2,200)",
            "HELD — Missing Brand Copy (Script 5 Sent)",
            44.0,
            4.0,
            110.00,
            85.00,
            "0 of 2 Used",
            0,
            3,
            "ENFORCE 48H ASSET HOLD (Shift Timeline Day-for-Day)",
            "2026-11-25",
            "Awaiting SPOC Product Copy Upload to Activate Kickoff",
        ],
        [
            "PRJ-2026-107",
            "Meridian B2B Pitch & Positioning Kit",
            "Meridian Industrial AI",
            "Gate 3: Onboard & Align",
            "Option 1: Essential Baseline",
            3200,
            "50% Deposit Paid ($1,600)",
            "100% Verified",
            32.0,
            6.5,
            100.00,
            85.00,
            "0 of 2 Used",
            0,
            1,
            "RETAIN & EXPAND (Fast-Moving SPOC)",
            "2026-11-19",
            "Milestone 1 Voice DNA Profile & Messaging Architecture",
        ],
        [
            "PRJ-2026-108",
            "Kinetix Design System Token Sprint",
            "Kinetix Robotics",
            "Gate 2: Scope & Price",
            "Option 3: Turnkey & Retainer Partner",
            7500,
            "Invoice #108 Sent ($3,750)",
            "Pending Deposit Clearance",
            68.0,
            2.0,
            110.29,
            85.00,
            "0 of 2 Used",
            0,
            1,
            "RETAIN & EXPAND (Executive Sponsor Account)",
            "2026-12-04",
            "Countersign SOW & Provision Pre-Flight Asset Vault",
        ],
        [
            "PRJ-2026-109",
            "Luminary Webflow Technical Migration",
            "Luminary EdTech",
            "Gate 2: Scope & Price",
            "Option 2: Core Transformation",
            5200,
            "Proposal Under SPOC Review",
            "Not Started",
            50.0,
            1.5,
            104.00,
            85.00,
            "0 of 2 Used",
            0,
            2,
            "FOLLOW UP VIA SCRIPT 3 (Slot Hold Expires Friday)",
            "2026-12-10",
            "Confirm Option 2 Selection & Issue 50% Deposit Link",
        ],
        [
            "PRJ-2026-110",
            "Stratos Legal Paid Diagnostic Blueprint",
            "Stratos Legal Ops",
            "Gate 1: Attract",
            "Option 1: Paid Diagnostic Blueprint",
            1250,
            "100% Upfront Paid ($1,250)",
            "100% Verified",
            11.0,
            8.5,
            147.06,
            85.00,
            "1 of 2 Used",
            0,
            2,
            "UPSELL TO $5,400 FULL BUILD (100% Credit Window)",
            "2026-11-01",
            "Deliver 7-Page Architecture Blueprint & Option 2 Proposal",
        ],
        [
            "PRJ-2026-111",
            "Atlas Freight Custom Dashboard",
            "Atlas Freight Systems",
            "Gate 4: Execute & Protect",
            "Option 1: Essential Baseline",
            3100,
            "50% Deposit Paid",
            "100% Verified",
            36.0,
            39.0,
            79.49,
            85.00,
            "2 of 2 Used",
            300,
            3,
            "RE-PRICE +20% AT RENEWAL (Enforce Script 7 & 12)",
            "2026-11-08",
            "Final QA Audit & Pre-Transfer Invoice Settlement",
        ],
        [
            "PRJ-2026-112",
            "Veloce Cycling Club Subscription Hub",
            "Veloce Performance Ltd",
            "Gate 5: Offboard & Retain",
            "Option 2: Core Transformation",
            4800,
            "100% Settled ($4,800)",
            "100% Verified",
            45.0,
            40.0,
            120.00,
            85.00,
            "2 of 2 Used",
            0,
            1,
            "RETAIN & EXPAND (Case Study Captured via Prompt 9.2)",
            "2026-10-30",
            "Send 48-Hr Post-Handover Retainer Bridge Offer (Script 11)",
        ],
    ]
    write_csv_utf8(NOTION_DIR / "02-Active-Projects-and-Gates.csv", projects_headers, projects_rows)

    # 3. 03-AI-Prompt-and-Script-Vault-62.csv (50 Prompts + 12 Scripts = 62 rows)
    prompts = extract_all_prompts()
    scripts = extract_all_scripts()

    vault_headers = [
        "Vault ID",
        "Asset Type",
        "Title",
        "Lifecycle Stage / Category",
        "Source Chapter",
        "Operational Objective",
        "When to Run",
        "Bracketed Variables",
        "Complete Copy-Ready Template",
        "Verification Rule",
    ]
    vault_rows = []
    for p in prompts:
        vault_rows.append(
            [
                f"Prompt {p['id']}",
                "AI Workflow Prompt",
                p["title"],
                p["stage"],
                f"Chapter {p['chapter']:02d}",
                p["objective"],
                p["when_to_run"],
                ", ".join(p["variables"]),
                p["template"],
                p["verification"],
            ]
        )
    for s in scripts:
        vault_rows.append(
            [
                f"Script {s['script_number']:02d} ({s['id']})",
                "Emergency Client Script",
                s["title"],
                s["category"],
                "Back Matter — Appendix B",
                s["objective"],
                s["when_to_run"],
                ", ".join(s["variables"]),
                s["template"],
                s["verification"],
            ]
        )
    if len(vault_rows) != 62:
        raise RuntimeError(f"Expected 62 vault rows, got {len(vault_rows)}")
    write_csv_utf8(NOTION_DIR / "03-AI-Prompt-and-Script-Vault-62.csv", vault_headers, vault_rows)

    # 4. 04-Weekly-CEO-Scorecard-Log.csv (12 rows: Week 01 to Week 12 progression from $26.80/hr to $58.40/hr)
    ceo_headers = [
        "Week ID",
        "Week Ending Date",
        "Gross Revenue ($)",
        "Bucket A Billable Craft Hours",
        "Bucket B Client Friction Hours",
        "Bucket C Unpaid Admin Hours",
        "Bucket D Context-Switching Hours",
        "Total Real Hours",
        "Billable Utilization (%)",
        "True Weekly EHR ($/hr)",
        "Weekly Revenue Leak ($)",
        "Primary Failed Gate",
        "One Permanent System Upgrade Installed",
        "Monday Block-1 Priority",
    ]
    ceo_rows = [
        [
            "Week 01 (Baseline)",
            "2026-08-07",
            1300.00,
            26.5,
            8.0,
            5.5,
            8.5,
            48.5,
            "54.6%",
            26.80,
            1650.00,
            "Gate 1 & Gate 4: Reactive Inbox & Unpriced Scope Creep",
            "Completed 7-Day EHR Leak Audit (Worksheet 1.1) and locked 90-Min Morning Maker Block",
            "Draft 3-Tier Productized Offer Matrix (Prompt 2.2)",
        ],
        [
            "Week 02",
            "2026-08-14",
            1420.00,
            27.0,
            7.0,
            5.0,
            7.5,
            46.5,
            "58.1%",
            30.54,
            1462.50,
            "Gate 1: Unqualified Discovery Calls with Low-Budget Leads",
            "Installed P.A.C.E. Async Lead Filter (Prompt 3.1 & Script 1) before calendar booking",
            "Publish 3-Tier Service Menu on primary inquiry page",
        ],
        [
            "Week 03",
            "2026-08-21",
            1550.00,
            27.5,
            6.5,
            4.5,
            6.5,
            45.0,
            "61.1%",
            34.44,
            1312.50,
            "Gate 2: Custom Proposals Taking 3.5 Hours Each",
            "Deployed 10-Minute B.R.I.E.F. 3-Option Proposal Engine (Prompt 3.3)",
            "Send B.R.I.E.F. proposal to Verde Beverage Co.",
        ],
        [
            "Week 04",
            "2026-08-28",
            1680.00,
            28.0,
            5.5,
            4.0,
            5.5,
            43.0,
            "65.1%",
            39.07,
            1125.00,
            "Gate 2: Underquoting Complex Multi-Stakeholder Builds",
            "Adopted B.C.R. Pricing Formula (1.15x Complexity + 20% Risk Buffer via Prompt 4.2)",
            "Re-calculate walk-away price floors across all 3 tiers",
        ],
        [
            "Week 05",
            "2026-09-04",
            1750.00,
            28.0,
            5.0,
            3.5,
            5.0,
            41.5,
            "67.5%",
            42.17,
            1012.50,
            "Gate 3: Kickoff Stalls Due to Missing Client Logins & Copy",
            "Enforced 48-Hour Pre-Flight Asset Gate & Day-for-Day Timeline Shift (Prompt 5.1 & Script 5)",
            "Provision Notion Client Portal template for Apex FinTech",
        ],
        [
            "Week 06",
            "2026-09-11",
            1840.00,
            28.5,
            4.5,
            3.5,
            4.5,
            41.0,
            "69.5%",
            44.88,
            937.50,
            "Gate 4: Blank-Page Drafting Drag on Technical Deliverables",
            "Implemented 20/60/20 Sandwich Execution & Master Voice DNA Profile (Prompts 6.1 & 6.2)",
            "Run 4-Gate Pre-Submission QA Audit on Apex Milestone 1",
        ],
        [
            "Week 07",
            "2026-09-18",
            1950.00,
            28.5,
            3.5,
            3.0,
            4.0,
            39.0,
            "73.1%",
            50.00,
            787.50,
            "Gate 4: 'Quick Favor' Slack Requests Eroding Sprint Margin",
            "Converted 2 out-of-scope requests into $650 paid P.V.P. Change Orders (Prompt 7.2 & Script 7)",
            "Ship VantagePoint Milestone 1 Wireframe Architecture",
        ],
        [
            "Week 08",
            "2026-09-25",
            2020.00,
            29.0,
            3.0,
            3.0,
            3.5,
            38.5,
            "75.3%",
            52.47,
            712.50,
            "Gate 4: Contradictory Feedback From Multiple Client Stakeholders",
            "Enforced Single Point of Contact (SPOC) Consolidation Rule & Guided Feedback Frame (Prompt 8.3)",
            "Record 3-Minute Loom walkthrough for Verde Beverage",
        ],
        [
            "Week 09",
            "2026-10-02",
            2080.00,
            29.0,
            2.5,
            3.0,
            3.0,
            37.5,
            "77.3%",
            55.47,
            637.50,
            "Gate 5: Revenue Drop Between Completed Projects",
            "Launched Executive Handover Vault + 48-Hr Offboard-to-Retainer Bridge (Prompt 9.4 & Script 11)",
            "Pitch $1,250/mo Care Retainer to Clarity Health Analytics",
        ],
        [
            "Week 10",
            "2026-10-09",
            2120.00,
            29.0,
            2.5,
            2.5,
            3.0,
            37.0,
            "78.4%",
            57.30,
            600.00,
            "Gate 5: Legacy Low-EHR Account Consuming 30% of Hours",
            "Ran 80/20 Client Profitability Audit (Worksheet 10.1) and flagged NorthStar as Whale Trap",
            "Prepare Script 12 Legacy Rate Calibration notice for NorthStar",
        ],
        [
            "Week 11",
            "2026-10-16",
            2160.00,
            29.0,
            2.0,
            2.5,
            3.0,
            36.5,
            "79.5%",
            59.18,
            562.50,
            "Gate 2: Booked Capacity Crossed 85% Weekly Ceiling",
            "Activated 85% Capacity Rate-Raise Trigger (+20% quote increase on next 3 incoming proposals)",
            "Send $7,500 Option 3 Turnkey Proposal to Kinetix Robotics",
        ],
        [
            "Week 12 (90-Day Target)",
            "2026-10-23",
            2131.60,
            29.0,
            2.0,
            2.5,
            3.0,
            36.5,
            "79.5%",
            58.40,
            562.50,
            "System Stabilized: All 5 Lifecycle Gates Operating >= 4/5",
            "Locked Q1 90-Day Rolling Cashflow & $4,050/mo Recurring Retainer Baseline Floor",
            "Execute Q4 Retainer Renewal & Case Study Harvest Sprint",
        ],
    ]
    write_csv_utf8(NOTION_DIR / "04-Weekly-CEO-Scorecard-Log.csv", ceo_headers, ceo_rows)
    print("[Suite A] Built 4 Notion CSV Databases (Leads=14, Projects=12, Vault=62, CEO Log=12).")


# ==============================================================================
# SUITE B: 4-TAB EDITABLE EXCEL (.XLSX) & CSV FINANCIAL & PRICING MATRIX
# ==============================================================================
def style_Range_Header(ws, row_idx: int, max_col: int, fill_hex: str = "0F172A"):
    fill = PatternFill(start_color=fill_hex, end_color=fill_hex, fill_type="solid")
    font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    for c in range(1, max_col + 1):
        cell = ws.cell(row=row_idx, column=c)
        cell.fill = fill
        cell.font = font
        cell.alignment = Alignment(horizontal="left" if c <= 2 else "right", vertical="center", wrap_text=True)


def apply_sheet_polish(ws, col_widths: dict[int, int], freeze_cell: str = "A6"):
    ws.views.sheetView[0].showGridLines = True
    ws.freeze_panes = freeze_cell
    thin_border = Border(
        left=Side(style="thin", color="E2E8F0"),
        right=Side(style="thin", color="E2E8F0"),
        top=Side(style="thin", color="E2E8F0"),
        bottom=Side(style="thin", color="E2E8F0"),
    )
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            if cell.fill.fill_type is None:
                cell.border = thin_border
                if cell.font is None or cell.font.name != "Calibri":
                    cell.font = Font(name="Calibri", size=10.5, color="1E293B")
    for col_idx, width in col_widths.items():
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = max(width, 15)


def export_ws_to_csv(ws, csv_path: Path):
    rows = []
    for row in ws.iter_rows(values_only=True):
        rows.append(["" if v is None else str(v) for v in row])
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def build_excel_and_csv_suite():
    SPREADSHEETS_DIR.mkdir(parents=True, exist_ok=True)
    HYBRID_BUNDLE_DIR.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.Workbook()
    # Remove default sheet after creating our 4 tabs
    default_ws = wb.active

    navy_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    sky_fill = PatternFill(start_color="0284C7", end_color="0284C7", fill_type="solid")
    teal_fill = PatternFill(start_color="0D9488", end_color="0D9488", fill_type="solid")
    soft_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    kpi_fill = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")

    title_font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    sub_font = Font(name="Calibri", size=10.5, italic=True, color="E2E8F0")
    bold_navy = Font(name="Calibri", size=11, bold=True, color="0F172A")

    # --------------------------------------------------------------------------
    # TAB 1: 01_EHR_Leak_Audit
    # --------------------------------------------------------------------------
    ws1 = wb.create_sheet(title="01_EHR_Leak_Audit")
    ws1["A1"] = "THE AI FREELANCER OPERATING SYSTEM — TAB 1: 7-DAY TIME & REVENUE LEAK DIAGNOSTIC (EHR AUDIT)"
    ws1["A2"] = "Synced with Chapter 1, Prompt 1.1 & Worksheet 1.1 • Edit yellow/white input cells in Column C; Column C/D formulas calculate automatically."
    for r in (1, 2):
        for c in range(1, 6):
            ws1.cell(row=r, column=c).fill = navy_fill
    ws1["A1"].font = title_font
    ws1["A2"].font = sub_font

    ws1.append([])
    ws1.append(["Line ID", "Diagnostic Metric / Operational Parameter", "Current Baseline Value", "Unit / Format", "Target Benchmark & Diagnostic Notes"])
    style_Range_Header(ws1, 4, 5, "0F172A")

    tab1_rows = [
        ("Line 01", "Stated Target Billable Hourly Rate", 75.00, "$/hr", "Your goal hourly rate for scoped client work"),
        ("Line 02", "Weekly Gross Revenue Billed (7-Day Audit Window)", 1300.00, "$/week", "Gross project + retainer fees earned this week"),
        ("Line 03", "Bucket A: Core Billable Craft Hours", 26.5, "hrs/week", "Target >= 65.0% of total weekly working hours"),
        ("Line 04", "Bucket B: Unbilled Client Friction & Scope Creep Hours", 8.0, "hrs/week", "Target <= 5.0% (Enforce Script 5 & Script 7)"),
        ("Line 05", "Bucket C: Unpaid Sales, Proposals & Discovery Calls", 5.5, "hrs/week", "Target <= 15.0% (Deploy 10-Min B.R.I.E.F. Engine)"),
        ("Line 06", "Bucket D: Internal Admin & Context-Switching Drag", 8.5, "hrs/week", "Target <= 15.0% (Batch into 30-Min Midday Sprint)"),
        ("Line 07", "Total Real Working Hours Logged (Buckets A+B+C+D)", "=SUM(C7:C10)", "hrs/week", "Live Formula: Sum of all 4 weekly time buckets"),
        ("Line 08", "Total Unbilled Shadow Labor Hours (Buckets B+C+D)", "=SUM(C8:C10)", "hrs/week", "Live Formula: Hours worked at $0 direct billing"),
        ("Line 09", "Billable Craft Utilization Ratio (Bucket A %)", "=C7/C11", "%", "Live Formula: Bucket A Hours / Total Real Hours"),
        ("Line 10", "True Effective Hourly Rate (Realized EHR)", "=ROUND(C6/C11,2)", "$/hr", "Live Formula: Weekly Gross Revenue / Total Real Hours"),
        ("Line 11", "Hourly Rate Erosion vs. Stated Target Rate", "=C14-C5", "$/hr", "Live Formula: True EHR minus Stated Target Rate"),
        ("Line 12", "Weekly Unbilled Revenue Leak (Opportunity Cost)", "=ROUND(C12*C5,2)", "$/week", "Live Formula: Unbilled Hours * Stated Target Rate"),
        ("Line 13", "Monthly Unbilled Revenue Leak (4.33 Weeks)", "=ROUND(C16*4.33,2)", "$/month", "Live Formula: Weekly Revenue Leak * 4.33 weeks"),
        ("Line 14", "Annualized 48-Week Unbilled Revenue Leak", "=ROUND(C16*48,2)", "$/year", "Live Formula: Recoverable annual capacity value"),
        ("Line 15", "90-Day AI OS 55% Recovery Projection (Annualized)", "=ROUND(C18*0.55,2)", "$/year", "Live Formula: 55% shadow-labor recovery via AI OS"),
    ]
    for idx, rdata in enumerate(tab1_rows, start=5):
        ws1.append(list(rdata))
        if idx >= 11:
            for c in range(1, 6):
                ws1.cell(row=idx, column=c).fill = kpi_fill
            ws1.cell(row=idx, column=2).font = bold_navy
            ws1.cell(row=idx, column=3).font = bold_navy

    ws1.append([])
    ws1.append(["Gate ID", "5-Stage Client Lifecycle Bottleneck Scorecard", "Gate Score (1-5)", "Max Score", "Automated Gate Diagnostic Status"])
    style_Range_Header(ws1, 21, 5, "0284C7")

    gates_rows = [
        ("Stage 01", "Attract & Filter (3-Tier Offer Matrix & P.A.C.E. Lead Filter)", 2, 5, '=IF(C22<=2,"PRIORITY FIX: Install Ch 2-3 Offer & Lead Filter","HEALTHY GATE")'),
        ("Stage 02", "Scope & Price (10-Min B.R.I.E.F. & B.C.R. Pricing Formula)", 2, 5, '=IF(C23<=2,"PRIORITY FIX: Deploy Ch 3-4 B.C.R. Pricing Engine","HEALTHY GATE")'),
        ("Stage 03", "Onboard & Align (48-Hr Pre-Flight Asset Gate & Kickoff Hold)", 3, 5, '=IF(C24<=2,"PRIORITY FIX: Enforce Ch 5 48-Hr Asset Gate","MODERATE — MONITOR")'),
        ("Stage 04", "Execute & Protect (20/60/20 Sandwich & P.V.P. Change Orders)", 2, 5, '=IF(C25<=2,"PRIORITY FIX: Activate Ch 6-8 Scope Defense","HEALTHY GATE")'),
        ("Stage 05", "Offboard & Retain (Retainer Bridge & 20-Min Friday CEO Review)", 3, 5, '=IF(C26<=2,"PRIORITY FIX: Install Ch 9-10 Retainer Bridge","MODERATE — MONITOR")'),
        ("TOTAL", "Composite 5-Stage Operating System Readiness Score", "=SUM(C22:C26)", "=SUM(D22:D26)", '=IF(C27<18,"SYSTEM UPGRADE REQUIRED (<18/25)","OPERATING SYSTEM LOCKED")'),
    ]
    for rdata in gates_rows:
        ws1.append(list(rdata))

    # Format numbers on Tab 1
    for r in (5, 6, 14, 15, 16, 17, 18, 19):
        ws1.cell(row=r, column=3).number_format = "$#,##0.00"
    for r in (7, 8, 9, 10, 11, 12):
        ws1.cell(row=r, column=3).number_format = '0.0 "hrs"'
    ws1.cell(row=13, column=3).number_format = "0.0%"
    apply_sheet_polish(ws1, {1: 15, 2: 52, 3: 24, 4: 16, 5: 50}, freeze_cell="A5")

    # --------------------------------------------------------------------------
    # TAB 2: 02_BCR_Scope_Pricing
    # --------------------------------------------------------------------------
    ws2 = wb.create_sheet(title="02_BCR_Scope_Pricing")
    ws2["A1"] = "THE AI FREELANCER OPERATING SYSTEM — TAB 2: WBS ESTIMATOR & B.C.R. 3-TIER PROPOSAL PRICING ENGINE"
    ws2["A2"] = "Synced with Chapters 2, 3 & 4 and Worksheet 4.1 • Base + Complexity + Risk Buffer Formula & Milestone Payment Split"
    for r in (1, 2):
        for c in range(1, 6):
            ws2.cell(row=r, column=c).fill = navy_fill
    ws2["A1"].font = title_font
    ws2["A2"].font = sub_font

    ws2.append([])
    ws2.append(["WBS ID", "Project Deliverable / Work Breakdown Module", "Optimistic Base Hrs", "Admin & Prep Multiplier (%)", "Weighted Base Hours (Formula)"])
    style_Range_Header(ws2, 4, 5, "0F172A")

    wbs_items = [
        ("WBS-01", "Discovery Synthesis, Voice DNA & Architecture Blueprint", 4.5, 0.20),
        ("WBS-02", "Core Wireframe & Information Hierarchy System", 6.5, 0.20),
        ("WBS-03", "Primary High-Conversion Deliverable Build (Core Pages/Modules)", 12.0, 0.20),
        ("WBS-04", "Responsive Breakpoints, CMS & Technical Integration", 5.5, 0.20),
        ("WBS-05", "Copy Calibration & Conversion Micro-Copy Polish", 3.5, 0.20),
        ("WBS-06", "4-Gate Pre-Submission QA & Red-Team Verification Audit", 3.0, 0.20),
        ("WBS-07", "Consolidated SPOC Revision Round Execution (2 Rounds)", 4.0, 0.20),
        ("WBS-08", "Executive Handover Vault & 3 Custom Video SOPs", 2.5, 0.20),
    ]
    for idx, (wid, name, bhrs, mult) in enumerate(wbs_items, start=5):
        ws2.append([wid, name, bhrs, mult, f"=ROUND(C{idx}*(1+D{idx}),2)"])
        ws2.cell(row=idx, column=3).number_format = '0.0 "hrs"'
        ws2.cell(row=idx, column=4).number_format = "0.0%"
        ws2.cell(row=idx, column=5).number_format = '0.00 "hrs"'

    ws2.append(["WBS-SUM", "Total Weighted Base Hours (Including 20% Admin/Prep Buffer)", "=SUM(C5:C12)", "=AVERAGE(D5:D12)", "=SUM(E5:E12)"])
    for c in range(1, 6):
        ws2.cell(row=13, column=c).fill = kpi_fill
        ws2.cell(row=13, column=c).font = bold_navy
    ws2.cell(row=13, column=3).number_format = '0.0 "hrs"'
    ws2.cell(row=13, column=4).number_format = "0.0%"
    ws2.cell(row=13, column=5).number_format = '0.00 "hrs"'

    ws2.append([])
    ws2.append(["Param ID", "B.C.R. Pricing Engine & 3-Tier Anchor Matrix", "Input / Formula Value", "50% Kickoff Deposit", "25% Midpoint / 25% Final"])
    style_Range_Header(ws2, 15, 5, "0284C7")

    bcr_rows = [
        ("BCR-01", "Target Hourly Billable Rate ($/hr)", 85.00, "", "Baseline practitioner hourly rate"),
        ("BCR-02", "Technical & Stakeholder Complexity Multiplier (C)", 1.15, "", "1.00x Standard | 1.15x Moderate | 1.30x High | 1.50x Rush"),
        ("BCR-03", "Client Dependency & Scope Risk Buffer (R %)", 0.20, "", "15% Low Risk | 20% Standard | 25% High | 35% Legacy Stack"),
        ("BCR-04", "Direct Pass-Through Software / Font / Licensing Costs ($)", 150.00, "", "Billed at 1.0x cost outside labor margin"),
        ("BCR-05", "B.C.R. Risk-Adjusted Equivalent Hours", "=ROUND(E13*C17*(1+C18),2)", "", "Formula: Weighted Base Hrs * Complexity * (1 + Risk%)"),
        ("TIER-1", "Option 1: Essential Baseline Package Price (1.00x B.C.R.)", "=ROUND(((C20*C16)+C19)/50,0)*50", "=ROUND(C21*0.50,2)", "=ROUND(C21*0.25,2)"),
        ("TIER-2", "Option 2: Core Transformation Anchor Price (1.35x B.C.R.)", "=ROUND((((C20*C16)*1.35)+C19)/50,0)*50", "=ROUND(C22*0.50,2)", "=ROUND(C22*0.25,2)"),
        ("TIER-3", "Option 3: Turnkey & Retainer Partner Price (1.85x B.C.R.)", "=ROUND((((C20*C16)*1.85)+C19)/50,0)*50", "=ROUND(C23*0.50,2)", "=ROUND(C23*0.25,2)"),
        ("FLOOR", "Hard Walk-Away Minimum Negotiation Floor (0.85x Tier 2)", "=ROUND((C22*0.85)/50,0)*50", "=ROUND(C24*0.50,2)", "=ROUND(C24*0.25,2)"),
    ]
    for idx, rdata in enumerate(bcr_rows, start=16):
        ws2.append(list(rdata))
        if idx >= 21:
            for c in range(1, 6):
                ws2.cell(row=idx, column=c).fill = kpi_fill
                ws2.cell(row=idx, column=c).font = bold_navy
            ws2.cell(row=idx, column=3).number_format = "$#,##0.00"
            ws2.cell(row=idx, column=4).number_format = "$#,##0.00"
            ws2.cell(row=idx, column=5).number_format = "$#,##0.00"

    ws2.cell(row=16, column=3).number_format = "$#,##0.00"
    ws2.cell(row=17, column=3).number_format = "0.00"
    ws2.cell(row=18, column=3).number_format = "0.0%"
    ws2.cell(row=19, column=3).number_format = "$#,##0.00"
    ws2.cell(row=20, column=3).number_format = '0.00 "hrs"'
    apply_sheet_polish(ws2, {1: 15, 2: 52, 3: 24, 4: 22, 5: 38}, freeze_cell="A5")

    # --------------------------------------------------------------------------
    # TAB 3: 03_Client_80_20_Roster
    # --------------------------------------------------------------------------
    ws3 = wb.create_sheet(title="03_Client_80_20_Roster")
    ws3["A1"] = "THE AI FREELANCER OPERATING SYSTEM — TAB 3: 80/20 CLIENT PROFITABILITY ROSTER & 85% RATE-RAISE TRIGGER"
    ws3["A2"] = "Synced with Chapter 10 & Worksheet 10.1 • Automatically isolates Whale-Trap accounts vs. Star Retainer accounts"
    for r in (1, 2):
        for c in range(1, 8):
            ws3.cell(row=r, column=c).fill = navy_fill
    ws3["A1"].font = title_font
    ws3["A2"].font = sub_font

    ws3.append([])
    ws3.append(["Account ID", "Active Client / Retainer Account", "Monthly Gross Fee ($)", "Real Monthly Hours", "Realized Client EHR ($/hr)", "Revenue Share (%)", "Friction Score (1-5)", "Automated 80/20 CEO Action Recommendation"])
    style_Range_Header(ws3, 4, 8, "0F172A")

    clients_data = [
        ("CLI-01", "Apex FinTech Cloud (Growth Retainer)", 2800.00, 24.0, 1),
        ("CLI-02", "Verde Beverage Co. (Brand & Packaging Sprint)", 2200.00, 21.5, 2),
        ("CLI-03", "BeaconHill Software (Onboarding Redesign)", 1800.00, 16.0, 2),
        ("CLI-04", "NorthStar Logistics (Legacy Custom Account)", 1500.00, 29.5, 5),
        ("CLI-05", "Clarity Health Analytics (Care Retainer)", 1250.00, 9.5, 1),
        ("CLI-06", "Solstice Apparel Group (E-Commerce Sprint)", 1100.00, 12.0, 2),
        ("CLI-07", "Atlas Freight Systems (Legacy Dashboard)", 950.00, 16.5, 4),
        ("CLI-08", "Stratos Legal Ops (Diagnostic Blueprint)", 650.00, 5.0, 1),
    ]
    for idx, (cid, cname, rev, hrs, fric) in enumerate(clients_data, start=5):
        ehr_formula = f"=ROUND(C{idx}/D{idx},2)"
        share_formula = f"=C{idx}/$C$13"
        action_formula = f'=IF(AND(E{idx}>=85,G{idx}<=2),"RETAIN & EXPAND",IF(OR(E{idx}<65,G{idx}>=4),"PRUNE / REPLACE","RE-PRICE +20%"))'
        ws3.append([cid, cname, rev, hrs, ehr_formula, share_formula, fric, action_formula])
        ws3.cell(row=idx, column=3).number_format = "$#,##0.00"
        ws3.cell(row=idx, column=4).number_format = '0.0 "hrs"'
        ws3.cell(row=idx, column=5).number_format = "$#,##0.00"
        ws3.cell(row=idx, column=6).number_format = "0.0%"

    ws3.append(["TOTAL", "Active Client Portfolio Blended Summary", "=SUM(C5:C12)", "=SUM(D5:D12)", "=ROUND(C13/D13,2)", "=SUM(F5:F12)", "=AVERAGE(G5:G12)", '=IF(E13>=85,"PORTFOLIO EHR ABOVE $85/HR TARGET","REBALANCE LOW-EHR ACCOUNTS")'])
    for c in range(1, 9):
        ws3.cell(row=13, column=c).fill = kpi_fill
        ws3.cell(row=13, column=c).font = bold_navy
    ws3.cell(row=13, column=3).number_format = "$#,##0.00"
    ws3.cell(row=13, column=4).number_format = '0.0 "hrs"'
    ws3.cell(row=13, column=5).number_format = "$#,##0.00"
    ws3.cell(row=13, column=6).number_format = "0.0%"
    ws3.cell(row=13, column=7).number_format = "0.0"

    ws3.append([])
    ws3.append(["Cap ID", "Weekly Capacity Utilization & 85% Rate-Raise Trigger", "Metric Value", "Unit", "Executive Pricing Rule"])
    style_Range_Header(ws3, 15, 5, "0D9488")
    ws3.append(["CAP-01", "Average Weekly Booked Client Hours (Monthly Hrs / 4.0)", "=ROUND(D13/4,2)", "hrs/week", "Current weekly delivery load across active roster"])
    ws3.append(["CAP-02", "Maximum Sustainable Weekly Billable Craft Ceiling", 35.0, "hrs/week", "Protected deep-work capacity ceiling (30-35 hrs/wk)"])
    ws3.append(["CAP-03", "Weekly Capacity Utilization Percentage", "=C16/C17", "%", '=IF(C18>=0.85,"TRIGGER ACTIVE (>=85%): RAISE NEXT 3 QUOTES +15% TO +25%","CAPACITY OPEN (<85%): STANDARD B.C.R. PRICING")'])
    ws3.cell(row=16, column=3).number_format = '0.0 "hrs"'
    ws3.cell(row=17, column=3).number_format = '0.0 "hrs"'
    ws3.cell(row=18, column=3).number_format = "0.0%"
    apply_sheet_polish(ws3, {1: 15, 2: 44, 3: 22, 4: 20, 5: 22, 6: 18, 7: 18, 8: 34}, freeze_cell="A5")

    # --------------------------------------------------------------------------
    # TAB 4: 04_90Day_Pipeline_Cashflow
    # --------------------------------------------------------------------------
    ws4 = wb.create_sheet(title="04_90Day_Pipeline_Cashflow")
    ws4["A1"] = "THE AI FREELANCER OPERATING SYSTEM — TAB 4: 12-WEEK ROLLING CASHFLOW, PIPELINE & TAX RESERVE FORECASTER"
    ws4["A2"] = "Synced with Chapter 10 Financial Governance • Tracks Retainer Floor, Milestone Invoices, Weighted Pipeline, Overhead & 25% Tax Reserve"
    for r in (1, 2):
        for c in range(1, 10):
            ws4.cell(row=r, column=c).fill = navy_fill
    ws4["A1"].font = title_font
    ws4["A2"].font = sub_font

    ws4.append([])
    ws4.append([
        "Week #",
        "Week Starting Date",
        "Confirmed Retainer Baseline ($)",
        "Scheduled Milestone Invoices ($)",
        "Weighted Pipeline Inflow ($)",
        "Total Projected Gross Inflow ($)",
        "Operating & Software Overhead ($)",
        "Tax Reserve Allocation (25% Formula)",
        "Net Owner Take-Home Profit ($)",
    ])
    style_Range_Header(ws4, 4, 9, "0F172A")

    cashflow_weeks = [
        ("Week 01", "2026-11-02", 1050.00, 1350.00, 0.00, 145.00),
        ("Week 02", "2026-11-09", 1050.00, 1200.00, 350.00, 145.00),
        ("Week 03", "2026-11-16", 1050.00, 1350.00, 450.00, 145.00),
        ("Week 04", "2026-11-23", 1050.00, 1100.00, 600.00, 145.00),
        ("Week 05", "2026-11-30", 1350.00, 1250.00, 500.00, 155.00),
        ("Week 06", "2026-12-07", 1350.00, 1350.00, 650.00, 155.00),
        ("Week 07", "2026-12-14", 1350.00, 1400.00, 500.00, 155.00),
        ("Week 08", "2026-12-21", 1350.00, 950.00, 400.00, 155.00),
        ("Week 09", "2026-12-28", 1650.00, 1100.00, 550.00, 160.00),
        ("Week 10", "2027-01-04", 1650.00, 1500.00, 750.00, 160.00),
        ("Week 11", "2027-01-11", 1650.00, 1350.00, 800.00, 160.00),
        ("Week 12", "2027-01-18", 1650.00, 1600.00, 850.00, 160.00),
    ]
    for idx, (wk, dt, ret, mil, pipe, ovh) in enumerate(cashflow_weeks, start=5):
        gross_f = f"=SUM(C{idx}:E{idx})"
        tax_f = f"=ROUND((F{idx}-G{idx})*0.25,2)"
        net_f = f"=F{idx}-G{idx}-H{idx}"
        ws4.append([wk, dt, ret, mil, pipe, gross_f, ovh, tax_f, net_f])
        for col_c in range(3, 10):
            ws4.cell(row=idx, column=col_c).number_format = "$#,##0.00"

    ws4.append([
        "90-DAY TOTAL",
        "12-Week Quarter Summary",
        "=SUM(C5:C16)",
        "=SUM(D5:D16)",
        "=SUM(E5:E16)",
        "=SUM(F5:F16)",
        "=SUM(G5:G16)",
        "=SUM(H5:H16)",
        "=SUM(I5:I16)",
    ])
    for c in range(1, 10):
        ws4.cell(row=17, column=c).fill = kpi_fill
        ws4.cell(row=17, column=c).font = bold_navy
        if c >= 3:
            ws4.cell(row=17, column=c).number_format = "$#,##0.00"

    apply_sheet_polish(ws4, {1: 15, 2: 22, 3: 26, 4: 26, 5: 24, 6: 26, 7: 26, 8: 26, 9: 26}, freeze_cell="A5")

    # Remove initial default sheet
    wb.remove(default_ws)

    xlsx_primary = SPREADSHEETS_DIR / "the-ai-freelancer-os-financial-and-pricing-matrix.xlsx"
    xlsx_bundle = HYBRID_BUNDLE_DIR / "the-ai-freelancer-os-financial-and-pricing-matrix.xlsx"
    wb.save(xlsx_primary)
    shutil.copy2(xlsx_primary, xlsx_bundle)

    # Also export the 4 standalone CSV sheets for Google Sheets / Numbers
    export_ws_to_csv(ws1, SPREADSHEETS_DIR / "sheet1-ehr-leak-audit.csv")
    export_ws_to_csv(ws2, SPREADSHEETS_DIR / "sheet2-bcr-scope-pricing.csv")
    export_ws_to_csv(ws3, SPREADSHEETS_DIR / "sheet3-client-80-20-roster.csv")
    export_ws_to_csv(ws4, SPREADSHEETS_DIR / "sheet4-90day-pipeline-cashflow.csv")
    print(f"[Suite B] Built 4-Tab Excel Matrix ({xlsx_primary.stat().st_size:,} bytes) + 4 CSV Sheets.")


# ==============================================================================
# SUITE C: COMMERCIAL HIGH-RESOLUTION BOOK & BUNDLE COVER DESIGN SUITE
# ==============================================================================
def build_kdp_ebook_svg() -> str:
    """1600 x 2560 px (1:1.6 aspect ratio) Amazon KDP eBook & Draft2Digital cover."""
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 2560" width="1600" height="2560">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="55%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284C7"/>
      <stop offset="100%" stop-color="#0D9488"/>
    </linearGradient>
  </defs>

  <!-- Deep Slate Navy Background -->
  <rect width="1600" height="2560" fill="url(#bgGrad)"/>

  <!-- Architectural Blueprint Grid Overlay -->
  <g stroke="#334155" stroke-width="1" opacity="0.35">
    <line x1="120" y1="0" x2="120" y2="2560"/>
    <line x1="400" y1="0" x2="400" y2="2560"/>
    <line x1="800" y1="0" x2="800" y2="2560"/>
    <line x1="1200" y1="0" x2="1200" y2="2560"/>
    <line x1="1480" y1="0" x2="1480" y2="2560"/>
    <line x1="0" y1="220" x2="1600" y2="220"/>
    <line x1="0" y1="1080" x2="1600" y2="1080"/>
    <line x1="0" y1="1960" x2="1600" y2="1960"/>
    <line x1="0" y1="2340" x2="1600" y2="2340"/>
  </g>

  <!-- Top Accent Bar -->
  <rect x="0" y="0" width="1600" height="28" fill="url(#accentGrad)"/>

  <!-- Top Imprint Pill -->
  <rect x="120" y="90" width="1360" height="76" rx="12" fill="#1E293B" stroke="#0284C7" stroke-width="2"/>
  <text x="160" y="138" font-family="Inter, Arial, sans-serif" font-size="26" font-weight="800" fill="#38BDF8" letter-spacing="3">PRACTITIONER SYSTEMS PRESS • COMMERCIAL OPERATING MANUAL</text>
  <text x="1440" y="138" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="700" fill="#2DD4BF" text-anchor="end">EDITION v1.0</text>

  <!-- Main Title Block -->
  <text x="120" y="340" font-family="Inter, Arial, sans-serif" font-size="64" font-weight="800" fill="#38BDF8" letter-spacing="4">THE COMPLETE 5-GATE SYSTEM</text>
  <text x="120" y="490" font-family="Inter, Arial, sans-serif" font-size="132" font-weight="900" fill="#FFFFFF" letter-spacing="-2">THE AI</text>
  <text x="120" y="635" font-family="Inter, Arial, sans-serif" font-size="132" font-weight="900" fill="#FFFFFF" letter-spacing="-2">FREELANCER</text>
  <text x="120" y="780" font-family="Inter, Arial, sans-serif" font-size="124" font-weight="900" fill="#38BDF8" letter-spacing="-2">OPERATING</text>
  <text x="120" y="920" font-family="Inter, Arial, sans-serif" font-size="124" font-weight="900" fill="#2DD4BF" letter-spacing="-2">SYSTEM</text>

  <!-- Subtitle Rule & Copy -->
  <rect x="120" y="970" width="420" height="8" fill="#0284C7"/>
  <text x="120" y="1035" font-family="Inter, Arial, sans-serif" font-size="34" font-weight="600" fill="#E2E8F0">A Practical System to Organize Clients, Automate Repetitive Work,</text>
  <text x="120" y="1085" font-family="Inter, Arial, sans-serif" font-size="34" font-weight="600" fill="#E2E8F0">Manage Projects, and Build a More Productive Freelance Business</text>

  <!-- Center Architectural Diagram Card: 5-Stage Lifecycle Engine -->
  <rect x="120" y="1145" width="1360" height="770" rx="24" fill="#0B1120" stroke="#334155" stroke-width="3"/>
  <rect x="120" y="1145" width="1360" height="68" rx="24" fill="#1E293B"/>
  <text x="165" y="1188" font-family="JetBrains Mono, Consolas, monospace" font-size="25" font-weight="700" fill="#38BDF8">SYSTEM ARCHITECTURE // THE 5-STAGE CLIENT LIFECYCLE &amp; MARGIN ENGINE</text>
  <text x="1435" y="1188" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="700" fill="#2DD4BF" text-anchor="end">TARGET EHR: $85+/HR</text>

  <!-- 5 Stage Nodes Inside Diagram -->
  <g transform="translate(160, 1255)">
    <rect x="0" y="0" width="1280" height="105" rx="14" fill="#1E293B" stroke="#0284C7" stroke-width="2"/>
    <rect x="0" y="0" width="190" height="105" rx="14" fill="#0284C7"/>
    <text x="95" y="62" font-family="JetBrains Mono, Consolas, monospace" font-size="28" font-weight="800" fill="#FFFFFF" text-anchor="middle">GATE 01</text>
    <text x="225" y="46" font-family="Inter, Arial, sans-serif" font-size="28" font-weight="800" fill="#FFFFFF">ATTRACT &amp; FILTER INBOUND PIPELINE</text>
    <text x="225" y="82" font-family="Inter, Arial, sans-serif" font-size="23" font-weight="500" fill="#94A3B8">3-Tier Productized Offer Matrix • P.A.C.E. Lead Scorer • Red-Flag Filter</text>
    <text x="1245" y="60" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="700" fill="#38BDF8" text-anchor="end">CH 01–03</text>
  </g>

  <g transform="translate(160, 1380)">
    <rect x="0" y="0" width="1280" height="105" rx="14" fill="#1E293B" stroke="#0284C7" stroke-width="2"/>
    <rect x="0" y="0" width="190" height="105" rx="14" fill="#0284C7"/>
    <text x="95" y="62" font-family="JetBrains Mono, Consolas, monospace" font-size="28" font-weight="800" fill="#FFFFFF" text-anchor="middle">GATE 02</text>
    <text x="225" y="46" font-family="Inter, Arial, sans-serif" font-size="28" font-weight="800" fill="#FFFFFF">SCOPE &amp; PRICE WITH B.C.R. PRECISION</text>
    <text x="225" y="82" font-family="Inter, Arial, sans-serif" font-size="23" font-weight="500" fill="#94A3B8">10-Minute B.R.I.E.F. Proposals • Base + Complexity + Risk Buffer • Zero-Discount Defense</text>
    <text x="1245" y="60" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="700" fill="#38BDF8" text-anchor="end">CH 03–04</text>
  </g>

  <g transform="translate(160, 1505)">
    <rect x="0" y="0" width="1280" height="105" rx="14" fill="#1E293B" stroke="#0D9488" stroke-width="2"/>
    <rect x="0" y="0" width="190" height="105" rx="14" fill="#0D9488"/>
    <text x="95" y="62" font-family="JetBrains Mono, Consolas, monospace" font-size="28" font-weight="800" fill="#FFFFFF" text-anchor="middle">GATE 03</text>
    <text x="225" y="46" font-family="Inter, Arial, sans-serif" font-size="28" font-weight="800" fill="#FFFFFF">ZERO-FRICTION 48-HOUR ONBOARDING GATE</text>
    <text x="225" y="82" font-family="Inter, Arial, sans-serif" font-size="23" font-weight="500" fill="#94A3B8">Pre-Flight Asset Vault • Day-for-Day Timeline Shift Rule • Async SLA Charter</text>
    <text x="1245" y="60" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="700" fill="#2DD4BF" text-anchor="end">CH 05</text>
  </g>

  <g transform="translate(160, 1630)">
    <rect x="0" y="0" width="1280" height="105" rx="14" fill="#1E293B" stroke="#0D9488" stroke-width="2"/>
    <rect x="0" y="0" width="190" height="105" rx="14" fill="#0D9488"/>
    <text x="95" y="62" font-family="JetBrains Mono, Consolas, monospace" font-size="28" font-weight="800" fill="#FFFFFF" text-anchor="middle">GATE 04</text>
    <text x="225" y="46" font-family="Inter, Arial, sans-serif" font-size="28" font-weight="800" fill="#FFFFFF">EXECUTE, QA &amp; DEFEND SCOPE BOUNDARIES</text>
    <text x="225" y="82" font-family="Inter, Arial, sans-serif" font-size="23" font-weight="500" fill="#94A3B8">20/60/20 Sandwich Execution • P.V.P. Change Orders • 3-Pillar Async Updates</text>
    <text x="1245" y="60" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="700" fill="#2DD4BF" text-anchor="end">CH 06–08</text>
  </g>

  <g transform="translate(160, 1755)">
    <rect x="0" y="0" width="1280" height="105" rx="14" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>
    <rect x="0" y="0" width="190" height="105" rx="14" fill="#D97706"/>
    <text x="95" y="62" font-family="JetBrains Mono, Consolas, monospace" font-size="28" font-weight="800" fill="#FFFFFF" text-anchor="middle">GATE 05</text>
    <text x="225" y="46" font-family="Inter, Arial, sans-serif" font-size="28" font-weight="800" fill="#FFFFFF">OFFBOARD, RETAIN &amp; SCALE AS WEEKLY CEO</text>
    <text x="225" y="82" font-family="Inter, Arial, sans-serif" font-size="23" font-weight="500" fill="#94A3B8">Executive Handover Vault • 48-Hr Retainer Bridge • 20-Min Friday CEO Scorecard</text>
    <text x="1245" y="60" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="700" fill="#FBBF24" text-anchor="end">CH 09–10</text>
  </g>

  <!-- 3 Feature Metric Badges -->
  <rect x="120" y="1965" width="430" height="165" rx="16" fill="#1E293B" stroke="#0284C7" stroke-width="2"/>
  <text x="335" y="2035" font-family="JetBrains Mono, Consolas, monospace" font-size="52" font-weight="800" fill="#38BDF8" text-anchor="middle">50 PROMPTS</text>
  <text x="335" y="2085" font-family="Inter, Arial, sans-serif" font-size="23" font-weight="600" fill="#CBD5E1" text-anchor="middle">Tested AI Workflows &amp; QA Rules</text>

  <rect x="585" y="1965" width="430" height="165" rx="16" fill="#1E293B" stroke="#0D9488" stroke-width="2"/>
  <text x="800" y="2035" font-family="JetBrains Mono, Consolas, monospace" font-size="52" font-weight="800" fill="#2DD4BF" text-anchor="middle">20 DIAGRAMS</text>
  <text x="800" y="2085" font-family="Inter, Arial, sans-serif" font-size="23" font-weight="600" fill="#CBD5E1" text-anchor="middle">Mindmaps &amp; Decision Trees</text>

  <rect x="1050" y="1965" width="430" height="165" rx="16" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>
  <text x="1265" y="2035" font-family="JetBrains Mono, Consolas, monospace" font-size="52" font-weight="800" fill="#FBBF24" text-anchor="middle">12 SCRIPTS</text>
  <text x="1265" y="2085" font-family="Inter, Arial, sans-serif" font-size="23" font-weight="600" fill="#CBD5E1" text-anchor="middle">Client Boundary &amp; Price Defense</text>

  <!-- Bottom Author & Studio Attribution Footer -->
  <rect x="120" y="2190" width="1360" height="240" rx="18" fill="#0B1120" stroke="#1E293B" stroke-width="2"/>
  <text x="800" y="2265" font-family="Inter, Arial, sans-serif" font-size="30" font-weight="700" fill="#94A3B8" text-anchor="middle">ARCHITECTED FOR INDEPENDENT FREELANCERS, CONSULTANTS &amp; SOLOPRENEURS</text>
  <text x="800" y="2330" font-family="Inter, Arial, sans-serif" font-size="42" font-weight="900" fill="#FFFFFF" letter-spacing="3" text-anchor="middle">DIGITAL KNOWLEDGE PRODUCT STUDIO</text>
  <text x="800" y="2385" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="600" fill="#38BDF8" text-anchor="middle">US • UK • CANADA • AUSTRALIA // HYBRID EDITION WITH INTERACTIVE WORKSHEETS</text>

  <rect x="0" y="2532" width="1600" height="28" fill="url(#accentGrad)"/>
</svg>"""


def build_kdp_paperback_wrap_svg() -> str:
    """
    Full KDP 6x9 Paperback Wrap Cover (12.58in x 9.25in = 3774 x 2775 px at 300 DPI).
    Left Bleed: 0..37.5px | Back Cover: 37.5..1837.5px | Spine (0.33in=99px): 1837.5..1936.5px | Front Cover: 1936.5..3736.5px | Right Bleed: 3736.5..3774px.
    """
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3774 2775" width="3774" height="2775">
  <defs>
    <linearGradient id="wrapBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B1120"/>
      <stop offset="50%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
    <linearGradient id="barGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0D9488"/>
      <stop offset="50%" stop-color="#0284C7"/>
      <stop offset="100%" stop-color="#0D9488"/>
    </linearGradient>
  </defs>

  <!-- Full Bleed Canvas (3774 x 2775) -->
  <rect width="3774" height="2775" fill="url(#wrapBg)"/>
  <rect x="0" y="0" width="3774" height="36" fill="url(#barGrad)"/>
  <rect x="0" y="2739" width="3774" height="36" fill="url(#barGrad)"/>

  <!-- ==================================================================== -->
  <!-- BACK COVER ZONE (X: 38 to 1837, Trim Center X: 937)                  -->
  <!-- ==================================================================== -->
  <rect x="130" y="130" width="1610" height="74" rx="10" fill="#1E293B" stroke="#0D9488" stroke-width="2"/>
  <text x="165" y="177" font-family="JetBrains Mono, Consolas, monospace" font-size="25" font-weight="800" fill="#2DD4BF">STOP LOSING 38% OF YOUR WEEK TO UNBILLED ADMIN &amp; SCOPE CREEP</text>

  <text x="130" y="290" font-family="Inter, Arial, sans-serif" font-size="52" font-weight="900" fill="#FFFFFF">Turn Your Solo Practice Into a High-Margin,</text>
  <text x="130" y="355" font-family="Inter, Arial, sans-serif" font-size="52" font-weight="900" fill="#38BDF8">Systematized Operating System.</text>

  <text x="130" y="435" font-family="Inter, Arial, sans-serif" font-size="29" font-weight="500" fill="#CBD5E1">Independent freelancers, consultants, and digital service providers rarely fail from a lack</text>
  <text x="130" y="478" font-family="Inter, Arial, sans-serif" font-size="29" font-weight="500" fill="#CBD5E1">of craft skill. They stall because custom proposals, missing onboarding assets, unpriced</text>
  <text x="130" y="521" font-family="Inter, Arial, sans-serif" font-size="29" font-weight="500" fill="#CBD5E1">revisions, and reactive Slack threads quietly erode a $75/hour target rate down to $26.80/hour.</text>

  <text x="130" y="595" font-family="Inter, Arial, sans-serif" font-size="30" font-weight="700" fill="#FFFFFF">This practitioner manual installs five deterministic operational gates across your business:</text>

  <!-- Back Cover 5-Gate Architecture Table Card -->
  <rect x="130" y="635" width="1610" height="1140" rx="20" fill="#1E293B" stroke="#334155" stroke-width="3"/>

  <g transform="translate(170, 675)">
    <rect x="0" y="0" width="1530" height="190" rx="12" fill="#0F172A" stroke="#0284C7" stroke-width="2"/>
    <text x="35" y="52" font-family="JetBrains Mono, Consolas, monospace" font-size="27" font-weight="800" fill="#38BDF8">01 // DIAGNOSTIC &amp; PRODUCTIZED POSITIONING (CHAPTERS 1–2)</text>
    <text x="35" y="100" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="600" fill="#FFFFFF">Audit your True Effective Hourly Rate (EHR) across Buckets A, B, C, and D, eliminate custom</text>
    <text x="35" y="140" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="600" fill="#94A3B8">scope-from-scratch quoting, and package your expertise into a 3-Tier Offer Matrix.</text>
  </g>

  <g transform="translate(170, 890)">
    <rect x="0" y="0" width="1530" height="190" rx="12" fill="#0F172A" stroke="#0284C7" stroke-width="2"/>
    <text x="35" y="52" font-family="JetBrains Mono, Consolas, monospace" font-size="27" font-weight="800" fill="#38BDF8">02 // 10-MINUTE PROPOSALS &amp; B.C.R. PRICING ENGINE (CHAPTERS 3–4)</text>
    <text x="35" y="100" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="600" fill="#FFFFFF">Score inbound leads with the 20-point P.A.C.E. filter, generate 3-option B.R.I.E.F. proposals</text>
    <text x="35" y="140" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="600" fill="#94A3B8">in 10 minutes, and defend margins using Base + Complexity + Risk Buffer math.</text>
  </g>

  <g transform="translate(170, 1105)">
    <rect x="0" y="0" width="1530" height="190" rx="12" fill="#0F172A" stroke="#0D9488" stroke-width="2"/>
    <text x="35" y="52" font-family="JetBrains Mono, Consolas, monospace" font-size="27" font-weight="800" fill="#2DD4BF">03 // 48-HOUR ONBOARDING &amp; 20/60/20 AI EXECUTION (CHAPTERS 5–6)</text>
    <text x="35" y="100" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="600" fill="#FFFFFF">Enforce the 48-Hour Pre-Flight Asset Gate before kickoff and accelerate delivery using</text>
    <text x="35" y="140" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="600" fill="#94A3B8">the 20% Human Architecture / 60% AI Draft / 20% 4-Gate QA Sandwich Workflow.</text>
  </g>

  <g transform="translate(170, 1320)">
    <rect x="0" y="0" width="1530" height="190" rx="12" fill="#0F172A" stroke="#0D9488" stroke-width="2"/>
    <text x="35" y="52" font-family="JetBrains Mono, Consolas, monospace" font-size="27" font-weight="800" fill="#2DD4BF">04 // P.V.P. SCOPE DEFENSE &amp; ASYNC UPDATES (CHAPTERS 7–8)</text>
    <text x="35" y="100" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="600" fill="#FFFFFF">Convert unbilled scope creep into paid Change Orders with 12 word-for-word boundary scripts</text>
    <text x="35" y="140" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="600" fill="#94A3B8">and cut revision cycles in half using 3-Pillar Async Updates and Loom walkthroughs.</text>
  </g>

  <g transform="translate(170, 1535)">
    <rect x="0" y="0" width="1530" height="190" rx="12" fill="#0F172A" stroke="#F59E0B" stroke-width="2"/>
    <text x="35" y="52" font-family="JetBrains Mono, Consolas, monospace" font-size="27" font-weight="800" fill="#FBBF24">05 // THE RETAINER BRIDGE &amp; WEEKLY CEO SCORECARD (CHAPTERS 9–10)</text>
    <text x="35" y="100" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="600" fill="#FFFFFF">Convert completed projects into recurring monthly retainers 48 hours after handover and</text>
    <text x="35" y="140" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="600" fill="#94A3B8">run the 20-Minute Friday CEO Ritual with automatic 85% capacity rate-raise triggers.</text>
  </g>

  <!-- Back Cover Bottom Left: Included Companion Assets Summary -->
  <rect x="130" y="1825" width="960" height="440" rx="18" fill="#0B1120" stroke="#0284C7" stroke-width="2"/>
  <text x="170" y="1890" font-family="Inter, Arial, sans-serif" font-size="32" font-weight="800" fill="#38BDF8">INSIDE THIS COMPLETE OPERATING MANUAL:</text>
  <text x="170" y="1950" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="600" fill="#E2E8F0">• 50 Tested AI Workflow Prompts with Verification Rules</text>
  <text x="170" y="2005" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="600" fill="#E2E8F0">• 20 High-Contrast Vector System Mindmaps &amp; Decision Trees</text>
  <text x="170" y="2060" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="600" fill="#E2E8F0">• 10 Chapter Action Worksheets &amp; Implementation Scorecards</text>
  <text x="170" y="2115" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="600" fill="#E2E8F0">• 12 Ready-to-Send Client Boundary &amp; Negotiation Scripts</text>
  <text x="170" y="2170" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="600" fill="#2DD4BF">• Complimentary Download Link for Printable Checklists &amp; Tools</text>

  <text x="130" y="2580" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="700" fill="#94A3B8">CATEGORY: BUSINESS &amp; ECONOMICS / SMALL BUSINESS &amp; AI OPERATIONS</text>
  <text x="130" y="2630" font-family="Inter, Arial, sans-serif" font-size="26" font-weight="700" fill="#FFFFFF">PRACTITIONER SYSTEMS PRESS • DIGITAL KNOWLEDGE PRODUCT STUDIO</text>

  <!-- Reserved White KDP ISBN Barcode Box (2.0in x 1.2in = 600 x 360 px) -->
  <rect x="1140" y="2275" width="600" height="360" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2"/>
  <text x="1440" y="2445" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="700" fill="#475569" text-anchor="middle">AMAZON KDP ISBN BARCODE ZONE</text>
  <text x="1440" y="2485" font-family="JetBrains Mono, Consolas, monospace" font-size="20" font-weight="600" fill="#64748B" text-anchor="middle">2.00" x 1.20" (600 x 360 px @ 300 DPI)</text>

  <!-- ==================================================================== -->
  <!-- CENTER SPINE ZONE (X: 1837.5 to 1936.5, Center X: 1887, Width: 99px) -->
  <!-- ==================================================================== -->
  <rect x="1837.5" y="36" width="99" height="2703" fill="#090E1A" stroke="#1E293B" stroke-width="1"/>
  <g transform="translate(1887, 1387) rotate(90)">
    <text x="0" y="10" font-family="Inter, Arial, sans-serif" font-size="30" font-weight="800" fill="#FFFFFF" letter-spacing="2" text-anchor="middle">THE AI FREELANCER OPERATING SYSTEM   •   PRACTITIONER SYSTEMS PRESS</text>
  </g>

  <!-- ==================================================================== -->
  <!-- FRONT COVER ZONE (X: 1936.5 to 3736.5, Trim Width: 1800px)           -->
  <!-- ==================================================================== -->
  <g transform="translate(1936.5, 0)">
    <rect x="130" y="120" width="1540" height="76" rx="12" fill="#1E293B" stroke="#0284C7" stroke-width="2"/>
    <text x="170" y="168" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="800" fill="#38BDF8" letter-spacing="3">PRACTITIONER SYSTEMS PRESS • COMMERCIAL OPERATING MANUAL</text>

    <text x="130" y="360" font-family="Inter, Arial, sans-serif" font-size="64" font-weight="800" fill="#38BDF8" letter-spacing="4">THE COMPLETE 5-GATE SYSTEM</text>
    <text x="130" y="515" font-family="Inter, Arial, sans-serif" font-size="140" font-weight="900" fill="#FFFFFF" letter-spacing="-2">THE AI</text>
    <text x="130" y="665" font-family="Inter, Arial, sans-serif" font-size="140" font-weight="900" fill="#FFFFFF" letter-spacing="-2">FREELANCER</text>
    <text x="130" y="815" font-family="Inter, Arial, sans-serif" font-size="132" font-weight="900" fill="#38BDF8" letter-spacing="-2">OPERATING</text>
    <text x="130" y="965" font-family="Inter, Arial, sans-serif" font-size="132" font-weight="900" fill="#2DD4BF" letter-spacing="-2">SYSTEM</text>

    <rect x="130" y="1015" width="460" height="8" fill="#0284C7"/>
    <text x="130" y="1080" font-family="Inter, Arial, sans-serif" font-size="36" font-weight="600" fill="#E2E8F0">A Practical System to Organize Clients, Automate Repetitive Work,</text>
    <text x="130" y="1132" font-family="Inter, Arial, sans-serif" font-size="36" font-weight="600" fill="#E2E8F0">Manage Projects, and Build a More Productive Freelance Business</text>

    <!-- Front Schematic Box -->
    <rect x="130" y="1200" width="1540" height="880" rx="22" fill="#0B1120" stroke="#334155" stroke-width="3"/>
    <text x="180" y="1265" font-family="JetBrains Mono, Consolas, monospace" font-size="27" font-weight="700" fill="#38BDF8">5-STAGE LIFECYCLE ARCHITECTURE // SYSTEM OVER THEORY</text>

    <rect x="180" y="1305" width="1440" height="125" rx="12" fill="#1E293B" stroke="#0284C7" stroke-width="2"/>
    <text x="220" y="1360" font-family="JetBrains Mono, Consolas, monospace" font-size="28" font-weight="800" fill="#38BDF8">STAGE 01–02: ATTRACT, FILTER, SCOPE &amp; PRICE</text>
    <text x="220" y="1402" font-family="Inter, Arial, sans-serif" font-size="25" font-weight="500" fill="#CBD5E1">7-Day EHR Leak Audit • 3-Tier Offer Matrix • 10-Min B.R.I.E.F. Proposals • B.C.R. Pricing</text>

    <rect x="180" y="1455" width="1440" height="125" rx="12" fill="#1E293B" stroke="#0D9488" stroke-width="2"/>
    <text x="220" y="1510" font-family="JetBrains Mono, Consolas, monospace" font-size="28" font-weight="800" fill="#2DD4BF">STAGE 03: ZERO-FRICTION 48-HOUR ONBOARDING GATE</text>
    <text x="220" y="1552" font-family="Inter, Arial, sans-serif" font-size="25" font-weight="500" fill="#CBD5E1">Pre-Flight Asset Verification • Day-for-Day Timeline Shift • Single-Link Client Hub</text>

    <rect x="180" y="1605" width="1440" height="125" rx="12" fill="#1E293B" stroke="#0D9488" stroke-width="2"/>
    <text x="220" y="1660" font-family="JetBrains Mono, Consolas, monospace" font-size="28" font-weight="800" fill="#2DD4BF">STAGE 04: 20/60/20 EXECUTION &amp; P.V.P. SCOPE DEFENSE</text>
    <text x="220" y="1702" font-family="Inter, Arial, sans-serif" font-size="25" font-weight="500" fill="#CBD5E1">Voice DNA Calibration • 4-Gate QA • Paid Change Orders • 3-Pillar Async Status</text>

    <rect x="180" y="1755" width="1440" height="125" rx="12" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>
    <text x="220" y="1810" font-family="JetBrains Mono, Consolas, monospace" font-size="28" font-weight="800" fill="#FBBF24">STAGE 05: RETAINER BRIDGE &amp; WEEKLY FRIDAY CEO REVIEW</text>
    <text x="220" y="1852" font-family="Inter, Arial, sans-serif" font-size="25" font-weight="500" fill="#CBD5E1">Executive Handover Vault • 48-Hr Retainer Pitch • 80/20 Client Roster • 85% Rate Trigger</text>

    <text x="900" y="1965" font-family="JetBrains Mono, Consolas, monospace" font-size="30" font-weight="800" fill="#FFFFFF" text-anchor="middle">50 AI WORKFLOW PROMPTS  •  20 VECTOR DIAGRAMS  •  12 BOUNDARY SCRIPTS</text>
    <text x="900" y="2020" font-family="Inter, Arial, sans-serif" font-size="25" font-weight="600" fill="#38BDF8" text-anchor="middle">Includes 10 Chapter Action Workbooks &amp; Operational Scorecards</text>

    <!-- Front Bottom Attribution -->
    <rect x="130" y="2160" width="1540" height="460" rx="20" fill="#0B1120" stroke="#1E293B" stroke-width="2"/>
    <text x="900" y="2290" font-family="Inter, Arial, sans-serif" font-size="34" font-weight="700" fill="#94A3B8" text-anchor="middle">DESIGNED FOR INDEPENDENT SERVICE PROVIDERS IN US, UK, CA &amp; AU</text>
    <text x="900" y="2390" font-family="Inter, Arial, sans-serif" font-size="48" font-weight="900" fill="#FFFFFF" letter-spacing="3" text-anchor="middle">DIGITAL KNOWLEDGE PRODUCT STUDIO</text>
    <text x="900" y="2480" font-family="JetBrains Mono, Consolas, monospace" font-size="28" font-weight="700" fill="#2DD4BF" text-anchor="middle">FIRST COMMERCIAL HYBRID EDITION (2026)</text>
  </g>
</svg>"""


def build_gumroad_banner_svg(
    tier_badge: str,
    price_tag: str,
    headline_line1: str,
    headline_line2: str,
    subtitle: str,
    accent_hex: str,
    secondary_hex: str,
    cards: list[tuple[str, str, str]],
    footer_left: str,
    footer_right: str,
) -> str:
    """1280 x 720 px (16:9 HD) Gumroad Product & Bundle Cover SVG with 24 valid XML <text> nodes."""
    import html as _html

    esc = _html.escape
    c1, c2, c3, c4 = [
        (esc(a), esc(b), esc(c)) for (a, b, c) in cards[:4]
    ]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720">
  <defs>
    <linearGradient id="gBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B1120"/>
      <stop offset="60%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
    <linearGradient id="gAccent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent_hex}"/>
      <stop offset="100%" stop-color="{secondary_hex}"/>
    </linearGradient>
  </defs>

  <rect width="1280" height="720" fill="url(#gBg)"/>
  <rect x="0" y="0" width="1280" height="10" fill="url(#gAccent)"/>

  <!-- Subtle Grid Lines -->
  <g stroke="#334155" stroke-width="1" opacity="0.28">
    <line x1="60" y1="0" x2="60" y2="720"/>
    <line x1="640" y1="0" x2="640" y2="720"/>
    <line x1="1220" y1="0" x2="1220" y2="720"/>
    <line x1="0" y1="95" x2="1280" y2="95"/>
    <line x1="0" y1="635" x2="1280" y2="635"/>
  </g>

  <!-- Top Header Bar -->
  <rect x="60" y="28" width="840" height="50" rx="8" fill="#1E293B" stroke="{accent_hex}" stroke-width="1.5"/>
  <text x="82" y="59" font-family="JetBrains Mono, Consolas, monospace" font-size="16" font-weight="800" fill="#38BDF8" letter-spacing="1.5">{esc(tier_badge)}</text>

  <!-- Price Badge Top Right -->
  <rect x="920" y="24" width="300" height="58" rx="12" fill="{accent_hex}"/>
  <text x="1070" y="61" font-family="JetBrains Mono, Consolas, monospace" font-size="24" font-weight="900" fill="#FFFFFF" text-anchor="middle">{esc(price_tag)}</text>

  <!-- Main Display Title & Right Telemetry Callout -->
  <text x="60" y="132" font-family="Inter, Arial, sans-serif" font-size="18" font-weight="800" fill="#2DD4BF" letter-spacing="2.2">THE AI FREELANCER OPERATING SYSTEM • DIGITAL KNOWLEDGE PRODUCT STUDIO</text>
  <text x="60" y="192" font-family="Inter, Arial, sans-serif" font-size="50" font-weight="900" fill="#FFFFFF" letter-spacing="-1">{esc(headline_line1)}</text>
  <text x="60" y="248" font-family="Inter, Arial, sans-serif" font-size="48" font-weight="900" fill="#38BDF8" letter-spacing="-1">{esc(headline_line2)}</text>
  <text x="60" y="288" font-family="Inter, Arial, sans-serif" font-size="18.5" font-weight="500" fill="#CBD5E1">{esc(subtitle)}</text>

  <!-- 5-Stage Lifecycle Pill Bar -->
  <rect x="60" y="304" width="1160" height="32" rx="6" fill="#0B1120" stroke="#334155" stroke-width="1"/>
  <text x="80" y="325" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="700" fill="#38BDF8">STAGE 1: ATTRACT</text>
  <text x="310" y="325" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="700" fill="#38BDF8">STAGE 2: B.C.R. PRICE</text>
  <text x="565" y="325" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="700" fill="#2DD4BF">STAGE 3: 48H ONBOARD</text>
  <text x="825" y="325" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="700" fill="#2DD4BF">STAGE 4: 20/60/20 QA</text>
  <text x="1060" y="325" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="700" fill="#FBBF24">STAGE 5: CEO SCALE</text>

  <!-- 4 Deliverable Feature Cards (2x2 Grid) -->
  <g transform="translate(60, 350)">
    <rect x="0" y="0" width="565" height="125" rx="14" fill="#1E293B" stroke="{accent_hex}" stroke-width="2"/>
    <rect x="18" y="18" width="110" height="30" rx="6" fill="#0F172A"/>
    <text x="73" y="39" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#38BDF8" text-anchor="middle">{c1[0]}</text>
    <text x="18" y="74" font-family="Inter, Arial, sans-serif" font-size="21" font-weight="800" fill="#FFFFFF">{c1[1]}</text>
    <text x="18" y="102" font-family="Inter, Arial, sans-serif" font-size="15.5" font-weight="500" fill="#94A3B8">{c1[2]}</text>
  </g>

  <g transform="translate(655, 350)">
    <rect x="0" y="0" width="565" height="125" rx="14" fill="#1E293B" stroke="{secondary_hex}" stroke-width="2"/>
    <rect x="18" y="18" width="110" height="30" rx="6" fill="#0F172A"/>
    <text x="73" y="39" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#2DD4BF" text-anchor="middle">{c2[0]}</text>
    <text x="18" y="74" font-family="Inter, Arial, sans-serif" font-size="21" font-weight="800" fill="#FFFFFF">{c2[1]}</text>
    <text x="18" y="102" font-family="Inter, Arial, sans-serif" font-size="15.5" font-weight="500" fill="#94A3B8">{c2[2]}</text>
  </g>

  <g transform="translate(60, 492)">
    <rect x="0" y="0" width="565" height="125" rx="14" fill="#1E293B" stroke="{secondary_hex}" stroke-width="2"/>
    <rect x="18" y="18" width="110" height="30" rx="6" fill="#0F172A"/>
    <text x="73" y="39" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#2DD4BF" text-anchor="middle">{c3[0]}</text>
    <text x="18" y="74" font-family="Inter, Arial, sans-serif" font-size="21" font-weight="800" fill="#FFFFFF">{c3[1]}</text>
    <text x="18" y="102" font-family="Inter, Arial, sans-serif" font-size="15.5" font-weight="500" fill="#94A3B8">{c3[2]}</text>
  </g>

  <g transform="translate(655, 492)">
    <rect x="0" y="0" width="565" height="125" rx="14" fill="#1E293B" stroke="{accent_hex}" stroke-width="2"/>
    <rect x="18" y="18" width="110" height="30" rx="6" fill="#0F172A"/>
    <text x="73" y="39" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#38BDF8" text-anchor="middle">{c4[0]}</text>
    <text x="18" y="74" font-family="Inter, Arial, sans-serif" font-size="21" font-weight="800" fill="#FFFFFF">{c4[1]}</text>
    <text x="18" y="102" font-family="Inter, Arial, sans-serif" font-size="15.5" font-weight="500" fill="#94A3B8">{c4[2]}</text>
  </g>

  <!-- Bottom Telemetry Strip -->
  <rect x="60" y="638" width="1160" height="54" rx="10" fill="#0B1120" stroke="#334155" stroke-width="1.5"/>
  <text x="85" y="671" font-family="JetBrains Mono, Consolas, monospace" font-size="16" font-weight="700" fill="#E2E8F0">{esc(footer_left)}</text>
  <text x="1195" y="671" font-family="JetBrains Mono, Consolas, monospace" font-size="16" font-weight="800" fill="#38BDF8" text-anchor="end">{esc(footer_right)}</text>

  <rect x="0" y="710" width="1280" height="10" fill="url(#gAccent)"/>
</svg>"""


def render_svg_to_png(browser_exe: str, svg_path: Path, png_path: Path, width: int, height: int):
    """Render an SVG file into an exact pixel-dimension PNG via headless Chromium."""
    svg_content = svg_path.read_text(encoding="utf-8")
    html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: {width}px; height: {height}px; overflow: hidden; background: #0F172A; }}
  svg {{ width: {width}px; height: {height}px; display: block; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_html = Path(tmpdir) / "cover_render.html"
        tmp_html.write_text(html_doc, encoding="utf-8")
        cmd = [
            browser_exe,
            "--headless",
            "--disable-gpu",
            f"--window-size={width},{height}",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--screenshot={str(png_path)}",
            tmp_html.as_uri(),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def render_svg_to_pdf(browser_exe: str, svg_path: Path, pdf_path: Path, width_in: float, height_in: float):
    """Render the full-wrap paperback cover SVG into a print-ready PDF at exact inch dimensions."""
    svg_content = svg_path.read_text(encoding="utf-8")
    html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  @page {{ size: {width_in}in {height_in}in; margin: 0; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: {width_in}in; height: {height_in}in; overflow: hidden; background: #0F172A; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  svg {{ width: {width_in}in; height: {height_in}in; display: block; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_html = Path(tmpdir) / "wrap_pdf.html"
        tmp_html.write_text(html_doc, encoding="utf-8")
        cmd = [
            browser_exe,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={str(pdf_path)}",
            tmp_html.as_uri(),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def build_covers_suite():
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    browser_exe = find_headless_browser()

    # 1. KDP eBook & D2D Cover (1600 x 2560)
    ebook_svg_path = COVERS_DIR / "kdp-ebook-and-d2d-cover.svg"
    ebook_png_path = COVERS_DIR / "kdp-ebook-and-d2d-cover.png"
    ebook_svg_path.write_text(build_kdp_ebook_svg(), encoding="utf-8")
    render_svg_to_png(browser_exe, ebook_svg_path, ebook_png_path, 1600, 2560)

    # 2. KDP Paperback Full Wrap Cover (3774 x 2775 px / 12.58in x 9.25in)
    wrap_svg_path = COVERS_DIR / "kdp-paperback-full-wrap-cover.svg"
    wrap_png_path = COVERS_DIR / "kdp-paperback-full-wrap-cover.png"
    wrap_pdf_path = COVERS_DIR / "kdp-paperback-full-wrap-cover.pdf"
    wrap_svg_path.write_text(build_kdp_paperback_wrap_svg(), encoding="utf-8")
    render_svg_to_png(browser_exe, wrap_svg_path, wrap_png_path, 3774, 2775)
    render_svg_to_pdf(browser_exe, wrap_svg_path, wrap_pdf_path, 12.58, 9.25)

    # 3. Gumroad Tier 0: Free Audit Kit Cover (1280 x 720)
    t0_svg = build_gumroad_banner_svg(
        tier_badge="TIER 0 LEAD MAGNET • THE FREELANCER LEAK AUDIT KIT",
        price_tag="FREE ($0+)",
        headline_line1="7-Day Time & Revenue",
        headline_line2="Leak Diagnostic Kit",
        subtitle="Audit Your True Effective Hourly Rate (EHR), Isolate Shadow Labor & Protect 3.5 Deep-Work Hours Daily",
        accent_hex="#0D9488",
        secondary_hex="#0284C7",
        cards=[
            ("ASSET 01", "Complete Chapter 1 Sample PDF", "Full 5-Stage Lifecycle Architecture & Marcus V. Case Study"),
            ("ASSET 02", "Fillable Worksheet 1.1 PDF", "7-Day Time Bucket Audit, EHR Math & 3-Block Priority Planner"),
            ("ASSET 03", "Interactive Web EHR Calculator", "Live Browser Diagnostic Tool with Stacked Visual Time Breakdown"),
            ("ASSET 04", "5 Chapter 1 AI Workflow Prompts", "Copy-Paste Prompts 1.1–1.5 with Built-In Verification Rules"),
        ],
        footer_left="INSTANT DOWNLOAD • PDF + FILLABLE WORKBOOK + INTERACTIVE WEB APP",
        footer_right="COMPATIBLE WITH DESKTOP, IPAD & MOBILE",
    )
    t0_svg_path = COVERS_DIR / "gumroad-tier0-free-audit-cover.svg"
    t0_png_path = COVERS_DIR / "gumroad-tier0-free-audit-cover.png"
    t0_svg_path.write_text(t0_svg, encoding="utf-8")
    render_svg_to_png(browser_exe, t0_svg_path, t0_png_path, 1280, 720)

    # 4. Gumroad Tier 2: Interactive Workbook Edition Cover (1280 x 720)
    t2_svg = build_gumroad_banner_svg(
        tier_badge="TIER 2 PRACTITIONER EDITION • MANUAL + FILLABLE WORKBOOKS + PLANNER",
        price_tag="$24 EDITION",
        headline_line1="Interactive Workbook &",
        headline_line2="Tablet Planner Edition",
        subtitle="The Complete 10-Chapter Manual + US Letter & A4 Fillable Workbooks + Landscape iPad Digital Planner",
        accent_hex="#0284C7",
        secondary_hex="#0D9488",
        cards=[
            ("PILLAR 01", "Complete 10-Chapter Manual (PDF + EPUB)", "75,158 Words • 50 AI Workflow Prompts • 20 Vector Diagrams"),
            ("PILLAR 02", "US Letter & ISO A4 Fillable Workbooks", "10 Standalone Chapter Worksheets with AcroForm Input Fields"),
            ("PILLAR 03", "Landscape Tablet Digital Planner PDF", "Designed for GoodNotes, Notability & reMarkable Execution"),
            ("PILLAR 04", "12 Emergency Client Boundary Scripts", "Word-for-Word Templates for Scope Creep, Pricing & Late Invoices"),
        ],
        footer_left="INCLUDES DIGITAL BOOK PDF + EPUB 3.0 + US LETTER/A4 WORKBOOKS + TABLET PLANNER",
        footer_right="ONE-TIME PURCHASE • INSTANT ACCESS",
    )
    t2_svg_path = COVERS_DIR / "gumroad-tier2-workbook-edition-cover.svg"
    t2_png_path = COVERS_DIR / "gumroad-tier2-workbook-edition-cover.png"
    t2_svg_path.write_text(t2_svg, encoding="utf-8")
    render_svg_to_png(browser_exe, t2_svg_path, t2_png_path, 1280, 720)

    # 5. Gumroad Tier 3: Complete Freelancer OS Flagship Bundle Cover (1280 x 720)
    t3_svg = build_gumroad_banner_svg(
        tier_badge="TIER 3 FLAGSHIP BUNDLE • COMPLETE HYBRID PRODUCT & SOFTWARE ECOSYSTEM",
        price_tag="$49 COMPLETE OS",
        headline_line1="The Complete AI Freelancer",
        headline_line2="Operating System Bundle",
        subtitle="Full Pro SaaS-Lite Web App + 5-Database Notion OS Kit + 4-Tab Excel Pricing Matrix + All Book & Workbook Editions",
        accent_hex="#0284C7",
        secondary_hex="#F59E0B",
        cards=[
            ("SUITE 01", "Pro SaaS-Lite Web Companion App", "Offline/Online HTML5 App: EHR Audit, B.C.R. Pricing & 62-Item Studio"),
            ("SUITE 02", "5-Database Minimalist Notion OS Kit", "Leads CRM, Active Projects, 62-Item Vault, CEO Scorecard & Client Portal"),
            ("SUITE 03", "4-Tab Excel & CSV Financial Matrix", "Live Formulas for WBS Pricing, 80/20 Client Roster & 90-Day Cashflow"),
            ("SUITE 04", "All 7 Book, Print & Workbook Editions", "Complete Manual PDF, EPUB 3.0, US Letter/A4 Workbooks & Tablet Planner"),
        ],
        footer_left="FLAGSHIP ALL-IN-ONE SYSTEM • ZERO SUBSCRIPTIONS REQUIRED • LOCAL & CLOUD READY",
        footer_right="MOST POPULAR PRACTITIONER TIER",
    )
    t3_svg_path = COVERS_DIR / "gumroad-tier3-complete-os-cover.svg"
    t3_png_path = COVERS_DIR / "gumroad-tier3-complete-os-cover.png"
    t3_svg_path.write_text(t3_svg, encoding="utf-8")
    render_svg_to_png(browser_exe, t3_svg_path, t3_png_path, 1280, 720)

    # 6. Gumroad Tier 4: Living OS & Pro Vault Pass Membership Cover (1280 x 720)
    t4_svg = build_gumroad_banner_svg(
        tier_badge="TIER 4 CONTINUOUS EXPANSION PASS • MONTHLY AI WORKFLOW & SCRIPT DROPS",
        price_tag="$9/MO • $49/YR",
        headline_line1="Living OS & Pro Workflow",
        headline_line2="Vault Membership Pass",
        subtitle="Continuous LLM Prompt Calibration, Niche-Specific Workflow Packs, New Boundary Scripts & Micro-Tool Releases",
        accent_hex="#0D9488",
        secondary_hex="#0284C7",
        cards=[
            ("DROP 01", "Monthly Role-Specific Workflow Packs", "Calibrated Prompt Chains for Design, Dev, Copy & Consulting"),
            ("DROP 02", "Expanded Negotiation & Retainer Scripts", "Fresh Commercial Clauses & Enterprise Procurement Playbooks"),
            ("DROP 03", "Multi-Model LLM Calibration Updates", "Tuned System Prompts for Claude, GPT & Gemini Releases"),
            ("DROP 04", "All Future Studio Web Micro-Tools", "Complimentary Pro Access to Every New Calculator & Utility"),
        ],
        footer_left="GUMROAD MEMBERSHIP PASS • CANCEL ANYTIME OR SAVE 55% ON ANNUAL BILLING",
        footer_right="CONTINUOUS OPERATING UPGRADES",
    )
    t4_svg_path = COVERS_DIR / "gumroad-tier4-living-os-membership-cover.svg"
    t4_png_path = COVERS_DIR / "gumroad-tier4-living-os-membership-cover.png"
    t4_svg_path.write_text(t4_svg, encoding="utf-8")
    render_svg_to_png(browser_exe, t4_svg_path, t4_png_path, 1280, 720)

    print("[Suite C] Built 6 Vector SVG Covers, 6 High-Res PNGs, and 1 Print-Ready Paperback Wrap PDF.")


def main() -> int:
    print("=" * 78)
    print("PHASE 7 BUILDER — NOTION OS KIT, EXCEL PRICING MATRIX & COVER DESIGN SUITE")
    print("=" * 78)
    build_notion_suite()
    build_excel_and_csv_suite()
    build_covers_suite()
    print("=" * 78)
    print("PHASE 7 BUILD COMPLETE — ALL 3 SUITES GENERATED SUCCESSFULLY")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
