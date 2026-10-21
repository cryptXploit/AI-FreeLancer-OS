#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 9 Master Builder & Commercial Release Packager (build_phase9_upgrade.py)
The AI Freelancer Operating System — Digital Knowledge Product Studio

Builds all 6 Ultra-Premium Phase 9 Upgrades & Repackages All 5 Commercial Release ZIPs:
1. UPGRADE 1 (13-VISUAL-CHEAT-SHEETS/):
   - 00-ECOSYSTEM-MASTER-MAP-POSTER.svg (1600x1100, >=35 <text> nodes) + .png
   - cheat-sheet-ch01.svg .. cheat-sheet-ch10.svg (1200x1600, >=25 <text> nodes each) + 10 .pngs
   - the-ai-freelancer-os-visual-shortcut-atlas.pdf (12-Page Full-Color PDF in 13-VISUAL-CHEAT-SHEETS/ & 09-EXPORTS/PDF/)
2. UPGRADE 2 (12-EDITABLE-OFFICE-SUITE/Word-Docs/):
   - 7 Native Editable Microsoft Word (.docx) Documents (01..07)
3. UPGRADE 3 (12-EDITABLE-OFFICE-SUITE/Slide-Decks/):
   - 3 Native Editable Microsoft PowerPoint (.pptx) Widescreen Decks (12, 10, 10 slides)
4. UPGRADE 4 (06-NOTION-TEMPLATES/Spreadsheets/):
   - 8-Tab Charted Excel Command Center (the-ai-freelancer-os-financial-and-pricing-matrix.xlsx)
     with 3 embedded OpenPyXL charts on 00_Executive_Visual_Dashboard + 1 PieChart on 01_EHR_Leak_Audit
5. UPGRADE 5 (08-COVER-DESIGN/Editable-Design-Kit/):
   - design-customizer-studio.html (>=65,000 bytes, 6 templates, 5 themes, FileReader photo upload, PNG/SVG export)
6. UPGRADE 6 (14-AUTOMATION-BLUEPRINTS/):
   - 3 Importable Make.com / Zapier / n8n JSON Automation Blueprints + Setup Guide
7. Updates 10-MARKETING/index.html, root README.md, and repackages Tier0..Tier4 .zip archives.
"""

import csv
import html
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import openpyxl
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from build_phase7 import (
    apply_sheet_polish,
    export_ws_to_csv,
    find_headless_browser,
    render_svg_to_png,
    style_Range_Header,
)
from build_webapp import extract_all_prompts, extract_all_scripts
from phase9_office_and_studio import (
    build_automation_blueprints,
    build_design_customizer_studio,
    build_powerpoint_decks,
    build_word_docx_suite,
)

BASE_DIR = Path(__file__).resolve().parent
CHEAT_DIR = BASE_DIR / "13-VISUAL-CHEAT-SHEETS"
PDF_EXPORT_DIR = BASE_DIR / "09-EXPORTS" / "PDF"
HYBRID_BUNDLE_DIR = BASE_DIR / "09-EXPORTS" / "HYBRID-BUNDLE"
SPREADSHEETS_DIR = BASE_DIR / "06-NOTION-TEMPLATES" / "Spreadsheets"
MARKETING_DIR = BASE_DIR / "10-MARKETING"


# ==============================================================================
# UPGRADE 1: 60-SECOND VISUAL SHORTCUT ATLAS (11 SVGs, 11 PNGs & 12-PAGE PDF)
# ==============================================================================
CHEAT_SHEET_DATA = [
    {
        "ch": 1,
        "part": "PART I: DIAGNOSTICS & POSITIONING",
        "gate": "GATE 01: DIAGNOSTIC & CIRCUIT-BREAKER",
        "time_to_run": "15 MINS TO AUDIT",
        "title": "The Overwhelmed Freelancer's Bottleneck",
        "subtitle": "How to Diagnose Shadow Labor, Calculate True EHR & Lock Your Daily 90-Minute Maker Block",
        "tldr": [
            "1. Freelancers plateau at $3k-$6k/mo not from lack of skill, but from 45%+ Unbilled Shadow Labor.",
            "2. Track every working hour across 4 Buckets (A: Craft, B: Friction, C: Unpaid Sales, D: Admin Drag).",
            "3. Install the Daily 3-Block Operating Rhythm starting with a non-negotiable 90-Minute Maker Block.",
        ],
        "formula_name": "TRUE EFFECTIVE HOURLY RATE (EHR) FORMULA",
        "formula_eq": "True EHR ($/hr) = Weekly Gross Revenue / (Bucket A + B + C + D Hours)",
        "formula_bench": "Target Benchmark: Bucket A >= 65% of Total Hours | True EHR >= $85.00/hr",
        "steps": [
            ("STEP 01 // LOG 7 DAYS", " Categorize all work into Buckets A, B, C & D using Worksheet 1.1."),
            ("STEP 02 // COMPUTE LEAK", "Multiply Unbilled Hours (B+C+D) by Target Rate to see weekly dollar leak."),
            ("STEP 03 // SCORE 5 GATES", "Rate all 5 Lifecycle Gates (1-5) to isolate your lowest-scoring bottleneck."),
            ("STEP 04 // LOCK BLOCK 1", "Mute Slack/Email for your first 90 minutes every morning (Maker Sprint)."),
        ],
        "red_flags": [
            "RED FLAG 01: Checking client email or Slack within the first 60 minutes of waking up.",
            "RED FLAG 02: Bucket B + C + D shadow labor exceeding 35% of your total weekly work hours.",
            "RED FLAG 03: Quoting new projects based on 'gut feel' instead of historical True EHR data.",
        ],
        "kpi_target": "30-DAY TARGET KPI: Lift Billable Craft Utilization to >= 65% & Reclaim 8.5 Hrs/Week",
        "script_ref": "EMERGENCY CIRCUIT-BREAKER: Deploy Async Response Window Charter & Prompt 1.1 Leak Auditor",
    },
    {
        "ch": 2,
        "part": "PART I: DIAGNOSTICS & POSITIONING",
        "gate": "GATE 01: PRODUCTIZED PACKAGING",
        "time_to_run": "30 MINS TO PACKAGE",
        "title": "Positioning & Productized Service Packaging",
        "subtitle": "Replacing Custom Hourly Quotes With a High-Margin 3-Tier Productized Offer Matrix",
        "tldr": [
            "1. Selling custom hourly labor punishes you for getting faster and invites client micromanagement.",
            "2. Package your core skill into 3 fixed-scope tiers: Option 1 Baseline, Option 2 Core, Option 3 Turnkey.",
            "3. Attach a written Hard Scope Boundary Charter to every tier so clients know what is excluded upfront.",
        ],
        "formula_name": "3-TIER PRODUCTIZED PRICE ANCHORING RATIO",
        "formula_eq": "Tier 1 (1.0x Floor)  |  Tier 2 Recommended (1.35x-1.55x)  |  Tier 3 Turnkey (1.85x-2.25x)",
        "formula_bench": "Target Conversion Split: 15% Option 1  •  65% Option 2 (Core)  •  20% Option 3 (Turnkey)",
        "steps": [
            ("STEP 01 // ISOLATE OUTCOME", "Define the #1 expensive business bottleneck your best clients pay to solve."),
            ("STEP 02 // BUILD 3 TIERS", "Structure Option 1 (Baseline), Option 2 (Core), and Option 3 (Turnkey)."),
            ("STEP 03 // CAP REVISIONS", "Lock 2 consolidated SPOC revision rounds and explicit exclusions per tier."),
            ("STEP 04 // ADD DIAGNOSTIC", "Create a $450-$1,250 Paid Diagnostic Blueprint for uncertain prospects."),
        ],
        "red_flags": [
            "RED FLAG 01: Sending a single-price quote that forces the buyer into a binary 'Yes or No' decision.",
            "RED FLAG 02: Writing 'Unlimited Revisions' or leaving deliverable quantities vague ('a few pages').",
            "RED FLAG 03: Letting prospects pick and choose custom line items like an a-la-carte restaurant menu.",
        ],
        "kpi_target": "30-DAY TARGET KPI: Increase Average Project Deal Size by +35% to +50% via Option 2/3 Anchoring",
        "script_ref": "EMERGENCY CIRCUIT-BREAKER: Deploy Script 04 (Converting 'What Is Your Hourly Rate?' to Fixed Tiers)",
    },
    {
        "ch": 3,
        "part": "PART II: PIPELINE TRIAGE & PROPOSALS",
        "gate": "GATE 01 & 02: TRIAGE & RAPID PROPOSALS",
        "time_to_run": "10 MINS PER LEAD",
        "title": "The 10-Minute Lead Triage & Proposal Engine",
        "subtitle": "Scoring Inbound Inquiries via P.A.C.E. & Generating 3-Option B.R.I.E.F. Proposals in 10 Minutes",
        "tldr": [
            "1. Never hop on a 45-minute discovery call before an inquiry passes the 20-point P.A.C.E. Lead Filter.",
            "2. Route low-fit leads (<10 pts) to a polite decline and medium leads (10-13 pts) to a Paid Diagnostic.",
            "3. Draft complete 3-Tier B.R.I.E.F. proposals in under 10 minutes using your discovery notes and Prompt 3.3.",
        ],
        "formula_name": "20-POINT P.A.C.E. LEAD QUALIFICATION SCORER",
        "formula_eq": "P.A.C.E. Score (0-20) = Problem (0-5) + Authority (0-5) + Commercial Fit (0-5) + Execution (0-5)",
        "formula_bench": "Routing Thresholds: 14-20 Pts = Full 3-Tier Proposal | 10-13 Pts = Paid Audit | <10 Pts = Decline",
        "steps": [
            ("STEP 01 // ASYNC FILTER", "Send 4-Question Async Intake Gate (Script 01) before sharing calendar link."),
            ("STEP 02 // SCORE P.A.C.E.", "Run Prompt 3.1 to score lead 0-20 and detect scope/budget red flags."),
            ("STEP 03 // DRAFT B.R.I.E.F.", "Generate Bottleneck, Result, Implementation, Exclusions & 3-Tier Financials."),
            ("STEP 04 // 7-DAY EXPIRY", "Attach 7-day slot reservation window and automated Day 3 / Day 7 follow-ups."),
        ],
        "red_flags": [
            "RED FLAG 01: Taking discovery calls with prospects who refuse to share a ballpark budget band.",
            "RED FLAG 02: Spending 3+ hours crafting a bespoke slide deck for an unqualified lead.",
            "RED FLAG 03: Chasing ghosted prospects with 'Just checking in!' emails instead of slot-release notices.",
        ],
        "kpi_target": "30-DAY TARGET KPI: Cut Proposal Drafting Time to <= 12 Mins & Lift Close Rate to >= 45%",
        "script_ref": "EMERGENCY CIRCUIT-BREAKER: Deploy Script 01 (Async Filter), Script 02 (Decline) & Script 03 (Slot Hold)",
    },
    {
        "ch": 4,
        "part": "PART II: PIPELINE TRIAGE & PROPOSALS",
        "gate": "GATE 02: PRECISION PRICING & MARGIN DEFENSE",
        "time_to_run": "10 MINS TO PRICE",
        "title": "Precision Pricing, Estimation & Margin Defense",
        "subtitle": "Eliminating Underquoting With the B.C.R. Formula & The Zero-Discount Scope Trade-Down Protocol",
        "tldr": [
            "1. Practitioners underquote by 35%+ because they price optimistic execution hours with zero risk buffer.",
            "2. Break every project into an 8-line Work Breakdown Structure (WBS) and apply the B.C.R. Pricing Formula.",
            "3. Never discount your price for the same scope—always trade down scope modules to match a lower budget.",
        ],
        "formula_name": "THE B.C.R. PRECISION PRICING EQUATION",
        "formula_eq": "Package Price = [ (Weighted WBS Hrs * Target Rate) * Complexity (C) * (1 + Risk R%) ] + Pass-Throughs",
        "formula_bench": "Milestone Billing Law: 50% Upfront Deposit  •  25% Midpoint Prototype  •  25% Pre-Transfer Final",
        "steps": [
            ("STEP 01 // MAP WBS HOURS", "Estimate optimistic hours across 8 WBS lines and add +20% admin/prep buffer."),
            ("STEP 02 // APPLY C & R", "Multiply by Complexity (1.15x-1.50x) and Risk Buffer (+15% to +35%)."),
            ("STEP 03 // SET WALK-AWAY", "Lock your Hard Walk-Away Floor at 0.85x of Option 2 before sending."),
            ("STEP 04 // TRADE DOWN SCOPE", "If client asks for a discount, offer to remove secondary deliverables via Script 03."),
        ],
        "red_flags": [
            "RED FLAG 01: Accepting 'Net-30' or '50% on launch' terms that hand 100% of control to the client.",
            "RED FLAG 02: Cutting your price by 20% without removing a single deliverable from the Statement of Work.",
            "RED FLAG 03: Ignoring multi-stakeholder review committees when calculating your Risk Buffer (R%).",
        ],
        "kpi_target": "30-DAY TARGET KPI: 100% of Projects Billed at 50/25/25 Split With >= $85/hr Realized Margin",
        "script_ref": "EMERGENCY CIRCUIT-BREAKER: Deploy Prompt 4.2 (B.C.R. Calculator) & Zero-Discount Trade-Down Matrix",
    },
    {
        "ch": 5,
        "part": "PART III: ONBOARDING, EXECUTION & SCOPE",
        "gate": "GATE 03: 48-HOUR ONBOARDING GATE",
        "time_to_run": "48-HOUR GATE",
        "title": "Zero-Friction Client Onboarding & Kickoff Architecture",
        "subtitle": "Enforcing the 48-Hour Pre-Flight Asset Gate & Single-Link Notion Client Command Portal",
        "tldr": [
            "1. Mid-project delays almost always originate in Week 1 from starting work before client assets are ready.",
            "2. Provision a single-link Client Command Portal immediately upon 50% Kickoff Deposit clearance.",
            "3. Enforce the 48-Hour Pre-Flight Asset Gate: the delivery clock starts only when 100% of assets are verified.",
        ],
        "formula_name": "DAY-FOR-DAY TIMELINE SHIFT EQUATION",
        "formula_eq": "Adjusted Milestone Date = Original Target Date + MAX(0, Asset Verification Delay in Business Days)",
        "formula_bench": "Golden Onboarding Law: Zero Production Work Commences Prior to 50% Deposit + 5 Verified Assets",
        "steps": [
            ("STEP 01 // PROVISION HUB", "Duplicate 05-Client-Portal-and-Handover-Hub.md inside Notion in 3 minutes."),
            ("STEP 02 // SEND WELCOME", "Email Client Welcome Packet (.docx) + Pre-Flight Asset Checklist (Prompt 5.1)."),
            ("STEP 03 // VERIFY 5 ITEMS", "Confirm Brand Tokens, Copy, Logins, Voice DNA Form & SPOC Designation."),
            ("STEP 04 // LOCK KICKOFF", "Run 15-Minute Alignment Deck (.pptx) or send 3-Min Async Kickoff Loom."),
        ],
        "red_flags": [
            "RED FLAG 01: Starting wireframe or code work while waiting for the client's 50% deposit to clear.",
            "RED FLAG 02: Allowing a client to email 14 scattered attachments instead of uploading to the Pre-Flight Vault.",
            "RED FLAG 03: Compressing your weekend or QA time to make up for a client's 6-day delay in sending copy.",
        ],
        "kpi_target": "30-DAY TARGET KPI: Eliminate 100% of Mid-Sprint Asset Stalls & Cap Onboarding Setup at <= 20 Mins",
        "script_ref": "EMERGENCY CIRCUIT-BREAKER: Deploy Script 05 (Polite Project Hold & Day-for-Day Timeline Shift Notice)",
    },
    {
        "ch": 6,
        "part": "PART III: ONBOARDING, EXECUTION & SCOPE",
        "gate": "GATE 04: 20/60/20 EXECUTION & 4-GATE QA",
        "time_to_run": "42% FASTER BUILD",
        "title": "AI-Assisted Project Execution & Quality Control",
        "subtitle": "Executing Deliverables via the 20/60/20 Sandwich Protocol, Voice DNA & 4-Gate Pre-Submission QA",
        "tldr": [
            "1. Raw one-shot AI outputs look generic and destroy client trust; pure manual drafting destroys your margin.",
            "2. Use the 20/60/20 Sandwich: 20% Human Architecture -> 60% AI Accelerated Build -> 20% Human QA Polish.",
            "3. Run every deliverable through the 4-Gate Pre-Submission QA Audit before the client ever sees a link.",
        ],
        "formula_name": "THE 20 / 60 / 20 SANDWICH EXECUTION RATIO",
        "formula_eq": "Total Build Time = 20% Human Strategy & Voice DNA + 60% AI Assembly + 20% 4-Gate Red-Team QA",
        "formula_bench": "Quality Benchmark: Compress Production Hours by 40%+ With Zero Robotic AI Tone Defects",
        "steps": [
            ("STEP 01 // VOICE DNA LOCK", "Extract client's tone, vocabulary, and banned words into a Voice DNA Profile."),
            ("STEP 02 // HUMAN BLUEPRINT", "Architect the structural outline, conversion logic, and component hierarchy."),
            ("STEP 03 // MODULAR AI RUNS", "Execute chained prompts section-by-section rather than one giant prompt."),
            ("STEP 04 // 4-GATE QA AUDIT", "Verify Scope Compliance, Technical/Speed, Voice DNA & Edge-Case Red-Teaming."),
        ],
        "red_flags": [
            "RED FLAG 01: Pasting raw, unedited LLM output containing robotic filler words into a client deliverable.",
            "RED FLAG 02: Pasting confidential client financial data or credentials into public consumer AI training chats.",
            "RED FLAG 03: Sending a staging link to a client without testing mobile breakpoints and form validation first.",
        ],
        "kpi_target": "30-DAY TARGET KPI: Cut Core Deliverable Drafting Time by 40%+ & Pass 100% of 4-Gate QA Audits",
        "script_ref": "EMERGENCY CIRCUIT-BREAKER: Deploy Prompt 6.1 (Voice DNA) & Prompt 6.4 (4-Gate Pre-Submission Auditor)",
    },
    {
        "ch": 7,
        "part": "PART III: ONBOARDING, EXECUTION & SCOPE",
        "gate": "GATE 04: P.V.P. SCOPE & PAYMENT DEFENSE",
        "time_to_run": "5 MINS TO DEFEND",
        "title": "Defeating Scope Creep & Difficult Client Conversations",
        "subtitle": "Converting 'Quick Favors' Into Paid Change Orders via P.V.P. & Enforcing Late-Payment Escalation",
        "tldr": [
            "1. Scope creep rarely arrives as a giant demand; it arrives as ten 'Hey, quick 10-minute favor?' messages.",
            "2. Never say 'No' and never work for free—use Pause, Validate, Price (P.V.P.) to issue a 1-page Change Order.",
            "3. Enforce the deterministic Day +3, Day +7 (Work Pause), and Day +14 Late-Payment Escalation Ladder.",
        ],
        "formula_name": "PAUSE • VALIDATE • PRICE (P.V.P.) CHANGE ORDER FORMULA",
        "formula_eq": "Change Order Fee ($) = (Added Base Hours * 1.15 Complexity * Hourly Rate)  |  Shift = +N Business Days",
        "formula_bench": "Margin Defense Rule: Zero Out-of-Scope Work Enters Production Without Approved CO-# Addendum",
        "steps": [
            ("STEP 01 // PAUSE NEW ITEM", "Enthusiastically acknowledge the new request while keeping baseline work moving."),
            ("STEP 02 // VALIDATE IMPACT", "Calculate exact engineering hours and timeline shift (+X business days)."),
            ("STEP 03 // ISSUE CO FORM", "Send 05-PVP-Formal-Change-Order-Request-Form.docx with 3 client options."),
            ("STEP 04 // ENFORCE PAYMENT", "Trigger Script 09/10 automatically if any milestone invoice crosses Day +3/+7."),
        ],
        "red_flags": [
            "RED FLAG 01: Saying 'I'll throw this one in for free just this once' (trains the client to ask again tomorrow).",
            "RED FLAG 02: Continuing to ship new staging milestones when a prior milestone invoice is 7+ days overdue.",
            "RED FLAG 03: Transferring final editable source files or live admin credentials before the final 25% clears.",
        ],
        "kpi_target": "30-DAY TARGET KPI: Convert >= 75% of Out-of-Scope Requests Into Paid Change Orders or Phase-2 Backlog",
        "script_ref": "EMERGENCY CIRCUIT-BREAKER: Deploy Script 07 (P.V.P. Change Order), Script 09 (Day +3) & Script 10 (Day +7 Pause)",
    },
    {
        "ch": 8,
        "part": "PART IV: ASYNC DELIVERY, RETAINERS & CEO",
        "gate": "GATE 04: ASYNC UPDATES & REVISION CAP",
        "time_to_run": "15 MINS EVERY FRIDAY",
        "title": "Async Client Updates & Revision Minimization",
        "subtitle": "Eliminating Status Meetings With the 3-Pillar Friday Digest, 3-Min Looms & Guided Feedback Frame",
        "tldr": [
            "1. Clients book 'quick status calls' only when they feel anxious about progress; proactive updates cure anxiety.",
            "2. Send the 3-Pillar Friday Status Digest every Friday by 15:00 paired with a 3-Minute Loom walkthrough.",
            "3. Frame every deliverable handoff with Guided Feedback Questions and enforce the Single Point of Contact rule.",
        ],
        "formula_name": "THE 3-MINUTE LOOM WALKTHROUGH TIME ALLOCATION",
        "formula_eq": "0:00-0:30 Context & Goal  •  0:30-2:15 Decisions & Flow  •  2:15-3:00 Exact Feedback Needed",
        "formula_bench": "Revision Benchmark: Cap Revisions at <= 2.0 Consolidated Rounds & Cut Live Status Calls by 85%",
        "steps": [
            ("STEP 01 // RECORD 3M LOOM", "Walk through the milestone tying visual/code choices to buyer conversion goals."),
            ("STEP 02 // FRAME FEEDBACK", "Ask 3 specific architectural questions and state what is already locked."),
            ("STEP 03 // CONSOLIDATE SPOC", "Require the client SPOC to merge all internal team notes into one batched list."),
            ("STEP 04 // FRIDAY DIGEST", "Post Shipped This Week, In Queue Next Week & Action Needed every Friday at 15:00."),
        ],
        "red_flags": [
            "RED FLAG 01: Sending a bare Figma/staging link with 'Let me know what you think!' (invites subjective chaos).",
            "RED FLAG 02: Executing 14 piecemeal feedback emails from 4 different client employees across the week.",
            "RED FLAG 03: Accepting an unscheduled 'Can we hop on Zoom for 5 mins?' call without an async agenda.",
        ],
        "kpi_target": "30-DAY TARGET KPI: Reduce Live Status Meetings by 85% & Complete 95% of Projects Within 2 Rounds",
        "script_ref": "EMERGENCY CIRCUIT-BREAKER: Deploy Script 06 (Deflecting Ad-Hoc Calls) & Script 08 (SPOC Consolidation)",
    },
    {
        "ch": 9,
        "part": "PART IV: ASYNC DELIVERY, RETAINERS & CEO",
        "gate": "GATE 05: EXECUTIVE HANDOVER & RETAINERS",
        "time_to_run": "48-HR RETAINER BRIDGE",
        "title": "Smooth Offboarding, Case Studies & The Retainer Bridge",
        "subtitle": "Delivering the Executive Handover Vault, Harvesting ROI Case Studies & Closing Monthly Retainers",
        "tldr": [
            "1. Amateur freelancers end projects with a messy zip link; pros deliver an Executive Handover Certificate & SOPs.",
            "2. Capture structured Before/After ROI testimonials at peak client excitement right before final handover.",
            "3. Pitch the 3-Tier Monthly Retainer Menu within 48 hours of launch using the Phase-2 Opportunity Backlog.",
        ],
        "formula_name": "RECURRING RETAINER BASELINE COVERAGE RATIO",
        "formula_eq": "Retainer Coverage (%) = (Confirmed Monthly Retainer MRR / Monthly Fixed Business & Living Overhead) * 100",
        "formula_bench": "Stability Target: Build 3-4 Retainers Covering >= 100% of Monthly Baseline Expenses ($3.5k-$6k MRR)",
        "steps": [
            ("STEP 01 // SETTLE FINAL 25%", "Clear final 25% milestone invoice prior to live production ownership transfer."),
            ("STEP 02 // SHIP SOP VAULT", "Deliver 07-Final-Handover-Certificate.docx + 3 custom Loom training SOPs."),
            ("STEP 03 // HARVEST PROOF", "Send 4-Question ROI Testimonial Harvester (Prompt 9.2) to capture case study."),
            ("STEP 04 // PITCH RETAINER", "Present Deck 03 (.pptx) offering Option A ($1.25k), B ($2.4k) or C ($4.2k/mo)."),
        ],
        "red_flags": [
            "RED FLAG 01: Answering unpaid post-launch 'quick tweak' emails 6 weeks after a project ended.",
            "RED FLAG 02: Offering hourly 'rollover hours' on retainers that trap you in unscheduled monthly work debt.",
            "RED FLAG 03: Waiting 3 months after launch to ask for a testimonial when the client has moved on.",
        ],
        "kpi_target": "30-DAY TARGET KPI: Convert >= 35% of Completed Projects Into $1,250-$2,400/mo Recurring Retainers",
        "script_ref": "EMERGENCY CIRCUIT-BREAKER: Deploy Script 11 (48-Hour Post-Handover Retainer Pitch) & Handover Certificate",
    },
    {
        "ch": 10,
        "part": "PART IV: ASYNC DELIVERY, RETAINERS & CEO",
        "gate": "GATE 05: WEEKLY CEO & 80/20 PORTFOLIO",
        "time_to_run": "20 MINS EVERY FRIDAY",
        "title": "The Freelancer CEO: Capacity, 80/20 Roster & Scaling",
        "subtitle": "Running the 20-Minute Friday CEO Review, Pruning Whale-Trap Clients & Triggering Rate Increases",
        "tldr": [
            "1. Without a weekly executive review, your business drifts back into reactive inbox chaos within 30 days.",
            "2. Run the 20-Minute Friday CEO Ritual to audit True EHR, 90-day rolling cashflow, and 25% tax reserves.",
            "3. Rank all clients quarterly by Realized EHR and Friction Score, and raise rates +20% whenever capacity >= 85%.",
        ],
        "formula_name": "THE 85% CAPACITY UTILIZATION RATE-RAISE TRIGGER",
        "formula_eq": "IF (Weekly Booked Client Hours / 35.0 Max Craft Ceiling) >= 85%  -->  Raise Next 3 Proposals +15% to +25%",
        "formula_bench": "Portfolio Rule: Prune or Re-Price Any 'Whale-Trap' Account With EHR < $65/hr or Friction >= 4/5",
        "steps": [
            ("STEP 01 // FRIDAY 20M CEO", "Log weekly revenue and 4-Bucket hours in Tab 00/01 of Excel Command Center."),
            ("STEP 02 // AUDIT 80/20 ROSTER", "Classify clients into Star Accounts (Retain), Mid-Tier (Re-Price) & Whale Traps."),
            ("STEP 03 // ALLOCATE 25% TAX", "Transfer 25% of net weekly profit into dedicated Tax Reserve account."),
            ("STEP 04 // INSTALL 1 UPGRADE", "Deploy exactly one permanent template, script, or automation upgrade per week."),
        ],
        "red_flags": [
            "RED FLAG 01: Keeping a legacy 'Whale-Trap' client who consumes 35% of your hours at half your target EHR.",
            "RED FLAG 02: Keeping your package prices flat when your production calendar is booked above 85% capacity.",
            "RED FLAG 03: Co-mingling tax reserve funds with personal checking instead of automating a 25% split.",
        ],
        "kpi_target": "90-DAY TARGET KPI: Achieve >= $58-$85+/hr Blended EHR, <= 38 Hrs/Wk & 90 Days Cashflow Visibility",
        "script_ref": "EMERGENCY CIRCUIT-BREAKER: Deploy Script 12 (Legacy Client +25% Rate Calibration or Graceful Exit)",
    },
]


def build_master_ecosystem_poster_svg() -> str:
    """Build 00-ECOSYSTEM-MASTER-MAP-POSTER.svg (viewBox 0 0 1600 1100) with >= 35 <text> elements."""
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1100" width="1600" height="1100">
  <defs>
    <linearGradient id="posterBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B1120"/>
      <stop offset="50%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
    <linearGradient id="posterAccent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284C7"/>
      <stop offset="50%" stop-color="#0D9488"/>
      <stop offset="100%" stop-color="#F59E0B"/>
    </linearGradient>
  </defs>

  <rect width="1600" height="1100" fill="url(#posterBg)"/>
  <rect x="0" y="0" width="1600" height="12" fill="url(#posterAccent)"/>

  <!-- Header Banner -->
  <rect x="36" y="28" width="1528" height="92" rx="14" fill="#1E293B" stroke="#0284C7" stroke-width="2"/>
  <text x="64" y="62" font-family="JetBrains Mono, Consolas, monospace" font-size="16" font-weight="800" fill="#38BDF8" letter-spacing="2">VISUAL SHORTCUT ATLAS // MASTER WALL POSTER (00-ECOSYSTEM-MASTER-MAP)</text>
  <text x="64" y="98" font-family="Inter, Arial, sans-serif" font-size="30" font-weight="900" fill="#FFFFFF">THE AI FREELANCER OPERATING SYSTEM — 5-GATE ARCHITECTURE &amp; TOOLKIT MAP</text>
  <rect x="1250" y="46" width="290" height="56" rx="10" fill="#0284C7"/>
  <text x="1395" y="81" font-family="JetBrains Mono, Consolas, monospace" font-size="18" font-weight="800" fill="#FFFFFF" text-anchor="middle">TARGET EHR: $85+/HR</text>

  <!-- 5 Lifecycle Gate Columns Across Middle -->
  <!-- GATE 01 -->
  <g transform="translate(36, 142)">
    <rect x="0" y="0" width="292" height="540" rx="14" fill="#0F172A" stroke="#0284C7" stroke-width="2"/>
    <rect x="0" y="0" width="292" height="54" rx="14" fill="#0284C7"/>
    <text x="146" y="34" font-family="JetBrains Mono, Consolas, monospace" font-size="17" font-weight="800" fill="#FFFFFF" text-anchor="middle">GATE 01: ATTRACT &amp; FILTER</text>
    <text x="18" y="84" font-family="Inter, Arial, sans-serif" font-size="16" font-weight="800" fill="#38BDF8">Chapters 01, 02 &amp; 03</text>
    <text x="18" y="112" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• 7-Day EHR &amp; Shadow Labor Audit</text>
    <text x="18" y="138" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• Daily 90-Min Maker Block Rhythm</text>
    <text x="18" y="164" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• 3-Tier Productized Offer Matrix</text>
    <text x="18" y="190" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• 20-Point P.A.C.E. Lead Scorer</text>
    <rect x="16" y="215" width="260" height="145" rx="10" fill="#1E293B" stroke="#334155" stroke-width="1.5"/>
    <text x="30" y="242" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#2DD4BF">AI PROMPTS &amp; SCRIPTS:</text>
    <text x="30" y="268" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#CBD5E1">• Prompts 1.1–1.5 (Leak Audit)</text>
    <text x="30" y="292" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#CBD5E1">• Prompts 2.1–2.5 (3-Tier Matrix)</text>
    <text x="30" y="316" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#CBD5E1">• Prompt 3.1 (P.A.C.E. Lead Triage)</text>
    <text x="30" y="340" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#FBBF24">• Scripts 01, 02 &amp; 04 (Lead Filter)</text>
    <rect x="16" y="378" width="260" height="142" rx="10" fill="#162238" stroke="#0284C7" stroke-width="1.5"/>
    <text x="30" y="405" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#38BDF8">PLUG-AND-PLAY TOOLS:</text>
    <text x="30" y="430" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#E2E8F0">• Web App Module 1 (EHR Audit)</text>
    <text x="30" y="454" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#E2E8F0">• Excel Tab 01 (EHR Leak Audit)</text>
    <text x="30" y="478" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#E2E8F0">• Notion DB 01 (Leads Pipeline)</text>
    <text x="30" y="502" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#2DD4BF">• Automation Blueprint 01 (.json)</text>
  </g>

  <!-- GATE 02 -->
  <g transform="translate(345, 142)">
    <rect x="0" y="0" width="292" height="540" rx="14" fill="#0F172A" stroke="#0284C7" stroke-width="2"/>
    <rect x="0" y="0" width="292" height="54" rx="14" fill="#0284C7"/>
    <text x="146" y="34" font-family="JetBrains Mono, Consolas, monospace" font-size="17" font-weight="800" fill="#FFFFFF" text-anchor="middle">GATE 02: SCOPE &amp; PRICE</text>
    <text x="18" y="84" font-family="Inter, Arial, sans-serif" font-size="16" font-weight="800" fill="#38BDF8">Chapters 03 &amp; 04</text>
    <text x="18" y="112" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• 10-Min B.R.I.E.F. Proposal Engine</text>
    <text x="18" y="138" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• 8-Line WBS Hours Estimator</text>
    <text x="18" y="164" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• B.C.R. Pricing (Base+Complex+Risk)</text>
    <text x="18" y="190" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• Zero-Discount Scope Trade-Down</text>
    <rect x="16" y="215" width="260" height="145" rx="10" fill="#1E293B" stroke="#334155" stroke-width="1.5"/>
    <text x="30" y="242" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#2DD4BF">AI PROMPTS &amp; SCRIPTS:</text>
    <text x="30" y="268" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#CBD5E1">• Prompt 3.3 (B.R.I.E.F. Proposal)</text>
    <text x="30" y="292" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#CBD5E1">• Prompts 4.1–4.5 (B.C.R. Pricing)</text>
    <text x="30" y="316" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#CBD5E1">• Prompt 4.4 (Discount Defense)</text>
    <text x="30" y="340" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#FBBF24">• Script 03 (7-Day Slot Hold Notice)</text>
    <rect x="16" y="378" width="260" height="142" rx="10" fill="#162238" stroke="#0284C7" stroke-width="1.5"/>
    <text x="30" y="405" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#38BDF8">PLUG-AND-PLAY TOOLS:</text>
    <text x="30" y="430" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#E2E8F0">• Word 03 (B.R.I.E.F. Proposal .docx)</text>
    <text x="30" y="454" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#E2E8F0">• Word 04 (MSA &amp; SOW Contract .docx)</text>
    <text x="30" y="478" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#E2E8F0">• PPTX Deck 01 (12-Slide Pitch Deck)</text>
    <text x="30" y="502" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#2DD4BF">• Excel Tab 02 (B.C.R. Pricing Engine)</text>
  </g>

  <!-- GATE 03 -->
  <g transform="translate(654, 142)">
    <rect x="0" y="0" width="292" height="540" rx="14" fill="#0F172A" stroke="#0D9488" stroke-width="2"/>
    <rect x="0" y="0" width="292" height="54" rx="14" fill="#0D9488"/>
    <text x="146" y="34" font-family="JetBrains Mono, Consolas, monospace" font-size="17" font-weight="800" fill="#FFFFFF" text-anchor="middle">GATE 03: 48H ONBOARDING</text>
    <text x="18" y="84" font-family="Inter, Arial, sans-serif" font-size="16" font-weight="800" fill="#2DD4BF">Chapter 05 Architecture</text>
    <text x="18" y="112" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• 50% Deposit Clearance Gate</text>
    <text x="18" y="138" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• 48-Hour Pre-Flight Asset Vault</text>
    <text x="18" y="164" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• Day-for-Day Timeline Shift Rule</text>
    <text x="18" y="190" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• Single Point of Contact (SPOC)</text>
    <rect x="16" y="215" width="260" height="145" rx="10" fill="#1E293B" stroke="#334155" stroke-width="1.5"/>
    <text x="30" y="242" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#2DD4BF">AI PROMPTS &amp; SCRIPTS:</text>
    <text x="30" y="268" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#CBD5E1">• Prompt 5.1 (Welcome &amp; Asset Gate)</text>
    <text x="30" y="292" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#CBD5E1">• Prompt 5.2 (Kickoff Brief Builder)</text>
    <text x="30" y="316" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#CBD5E1">• Prompts 5.3–5.5 (SLA &amp; Portal Setup)</text>
    <text x="30" y="340" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#FBBF24">• Script 05 (Missing Asset Hold Notice)</text>
    <rect x="16" y="378" width="260" height="142" rx="10" fill="#162238" stroke="#0D9488" stroke-width="1.5"/>
    <text x="30" y="405" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#2DD4BF">PLUG-AND-PLAY TOOLS:</text>
    <text x="30" y="430" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#E2E8F0">• Word 06 (Welcome Packet .docx)</text>
    <text x="30" y="454" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#E2E8F0">• PPTX Deck 02 (10-Slide Kickoff Deck)</text>
    <text x="30" y="478" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#E2E8F0">• Notion 05 (Client Command Hub)</text>
    <text x="30" y="502" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#38BDF8">• Automation Blueprint 02 (.json)</text>
  </g>

  <!-- GATE 04 -->
  <g transform="translate(963, 142)">
    <rect x="0" y="0" width="292" height="540" rx="14" fill="#0F172A" stroke="#0D9488" stroke-width="2"/>
    <rect x="0" y="0" width="292" height="54" rx="14" fill="#0D9488"/>
    <text x="146" y="34" font-family="JetBrains Mono, Consolas, monospace" font-size="17" font-weight="800" fill="#FFFFFF" text-anchor="middle">GATE 04: EXECUTE &amp; DEFEND</text>
    <text x="18" y="84" font-family="Inter, Arial, sans-serif" font-size="16" font-weight="800" fill="#2DD4BF">Chapters 06, 07 &amp; 08</text>
    <text x="18" y="112" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• 20/60/20 Sandwich Execution</text>
    <text x="18" y="138" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• 4-Gate Pre-Submission QA Audit</text>
    <text x="18" y="164" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• P.V.P. Change Order Protocol</text>
    <text x="18" y="190" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• 3-Pillar Friday Digest &amp; 3m Loom</text>
    <rect x="16" y="215" width="260" height="145" rx="10" fill="#1E293B" stroke="#334155" stroke-width="1.5"/>
    <text x="30" y="242" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#2DD4BF">AI PROMPTS &amp; SCRIPTS:</text>
    <text x="30" y="268" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#CBD5E1">• Prompts 6.1–6.5 (Voice DNA &amp; QA)</text>
    <text x="30" y="292" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#CBD5E1">• Prompts 7.1–7.5 (P.V.P. Defense)</text>
    <text x="30" y="316" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#CBD5E1">• Prompts 8.1–8.5 (Async &amp; Looms)</text>
    <text x="30" y="340" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#FBBF24">• Scripts 06, 07, 08, 09 &amp; 10</text>
    <rect x="16" y="378" width="260" height="142" rx="10" fill="#162238" stroke="#0D9488" stroke-width="1.5"/>
    <text x="30" y="405" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#2DD4BF">PLUG-AND-PLAY TOOLS:</text>
    <text x="30" y="430" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#E2E8F0">• Word 05 (P.V.P. Change Order .docx)</text>
    <text x="30" y="454" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#E2E8F0">• Excel Tab 05 (Invoice Generator)</text>
    <text x="30" y="478" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#E2E8F0">• Excel Tab 06 (Daily 3-Block Log)</text>
    <text x="30" y="502" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#38BDF8">• Web App Module 3 (62-Item Studio)</text>
  </g>

  <!-- GATE 05 -->
  <g transform="translate(1272, 142)">
    <rect x="0" y="0" width="292" height="540" rx="14" fill="#0F172A" stroke="#F59E0B" stroke-width="2"/>
    <rect x="0" y="0" width="292" height="54" rx="14" fill="#D97706"/>
    <text x="146" y="34" font-family="JetBrains Mono, Consolas, monospace" font-size="17" font-weight="800" fill="#FFFFFF" text-anchor="middle">GATE 05: RETAIN &amp; SCALE</text>
    <text x="18" y="84" font-family="Inter, Arial, sans-serif" font-size="16" font-weight="800" fill="#FBBF24">Chapters 09 &amp; 10</text>
    <text x="18" y="112" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• Executive Handover &amp; 3 Video SOPs</text>
    <text x="18" y="138" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• 48-Hr Offboard-to-Retainer Bridge</text>
    <text x="18" y="164" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• 20-Min Friday CEO Scorecard</text>
    <text x="18" y="190" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="600" fill="#E2E8F0">• 80/20 Roster &amp; 85% Rate Trigger</text>
    <rect x="16" y="215" width="260" height="145" rx="10" fill="#1E293B" stroke="#334155" stroke-width="1.5"/>
    <text x="30" y="242" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#FBBF24">AI PROMPTS &amp; SCRIPTS:</text>
    <text x="30" y="268" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#CBD5E1">• Prompts 9.1–9.5 (Handover &amp; Bridge)</text>
    <text x="30" y="292" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#CBD5E1">• Prompts 10.1–10.5 (CEO &amp; 80/20)</text>
    <text x="30" y="316" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#FBBF24">• Script 11 (48h Retainer Bridge)</text>
    <text x="30" y="340" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#FBBF24">• Script 12 (Legacy +25% Rate Reset)</text>
    <rect x="16" y="378" width="260" height="142" rx="10" fill="#162238" stroke="#F59E0B" stroke-width="1.5"/>
    <text x="30" y="405" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#FBBF24">PLUG-AND-PLAY TOOLS:</text>
    <text x="30" y="430" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#E2E8F0">• Word 07 (Handover &amp; Retainer .docx)</text>
    <text x="30" y="454" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#E2E8F0">• PPTX Deck 03 (10-Slide ROI &amp; Pitch)</text>
    <text x="30" y="478" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#E2E8F0">• Excel Tabs 00, 03, 04 &amp; 07</text>
    <text x="30" y="502" font-family="Inter, Arial, sans-serif" font-size="12.5" fill="#38BDF8">• Automation Blueprint 03 (.json)</text>
  </g>

  <!-- Bottom Full-Width Ecosystem Asset Matrix -->
  <rect x="36" y="704" width="1528" height="356" rx="16" fill="#0F172A" stroke="#334155" stroke-width="2"/>
  <rect x="36" y="704" width="1528" height="48" rx="16" fill="#1E293B"/>
  <text x="64" y="734" font-family="JetBrains Mono, Consolas, monospace" font-size="16" font-weight="800" fill="#38BDF8">COMPLETE 8-PILLAR ULTRA-PREMIUM PRODUCT ECOSYSTEM DIRECTORY (QUICK FILE LOCATOR)</text>

  <!-- 4 Bottom Summary Columns -->
  <g transform="translate(60, 772)">
    <rect x="0" y="0" width="356" height="264" rx="12" fill="#1E293B" stroke="#0284C7" stroke-width="1.5"/>
    <text x="20" y="32" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#38BDF8">01 // BOOKS, WORKBOOKS &amp; ATLAS</text>
    <text x="20" y="62" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• Complete Manual PDF (168 Pages / 75k Words)</text>
    <text x="20" y="88" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• KDP 6x9 Print PDF + Reflowable EPUB 3.0</text>
    <text x="20" y="114" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• US Letter &amp; ISO A4 Fillable Workbooks</text>
    <text x="20" y="140" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• 49-Page Landscape iPad Tablet Planner PDF</text>
    <text x="20" y="166" font-family="Inter, Arial, sans-serif" font-size="13" fill="#2DD4BF">• 12-Page Visual Shortcut Atlas PDF (NEW)</text>
    <text x="20" y="192" font-family="Inter, Arial, sans-serif" font-size="13" fill="#2DD4BF">• 31 Vector SVGs (20 Diagrams + 11 Posters)</text>
    <text x="20" y="226" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700" fill="#94A3B8">FOLDER: 09-EXPORTS/ &amp; 13-VISUAL-CHEAT-SHEETS/</text>
  </g>

  <g transform="translate(434, 772)">
    <rect x="0" y="0" width="356" height="264" rx="12" fill="#1E293B" stroke="#0D9488" stroke-width="1.5"/>
    <text x="20" y="32" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#2DD4BF">02 // WORD (.DOCX) &amp; PPTX SUITE</text>
    <text x="20" y="62" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• 01 Complete Editable Book Manuscript (.docx)</text>
    <text x="20" y="88" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• 02 Complete 10-Ch Action Workbook (.docx)</text>
    <text x="20" y="114" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• 03 Client 3-Tier B.R.I.E.F. Proposal (.docx)</text>
    <text x="20" y="140" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• 04 Master Service Agreement &amp; SOW (.docx)</text>
    <text x="20" y="166" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• 05 Change Order + 06 Welcome + 07 Handover</text>
    <text x="20" y="192" font-family="Inter, Arial, sans-serif" font-size="13" fill="#38BDF8">• 3 Editable 16:9 PowerPoint Decks (32 Slides)</text>
    <text x="20" y="226" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700" fill="#94A3B8">FOLDER: 12-EDITABLE-OFFICE-SUITE/</text>
  </g>

  <g transform="translate(808, 772)">
    <rect x="0" y="0" width="356" height="264" rx="12" fill="#1E293B" stroke="#0284C7" stroke-width="1.5"/>
    <text x="20" y="32" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#38BDF8">03 // 8-TAB EXCEL &amp; 5-DB NOTION OS</text>
    <text x="20" y="62" font-family="Inter, Arial, sans-serif" font-size="13" fill="#2DD4BF">• Tab 00 Executive Dashboard (3 Live Charts)</text>
    <text x="20" y="88" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• Tab 01 EHR Audit + Tab 02 B.C.R. Pricing</text>
    <text x="20" y="114" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• Tab 03 80/20 Roster + Tab 04 90d Cashflow</text>
    <text x="20" y="140" font-family="Inter, Arial, sans-serif" font-size="13" fill="#2DD4BF">• Tab 05 Invoice + Tab 06 Time + Tab 07 Tax</text>
    <text x="20" y="166" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• 5-Database Minimalist Notion OS Import Kit</text>
    <text x="20" y="192" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• 62-Item AI Prompt &amp; Script CSV Database</text>
    <text x="20" y="226" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700" fill="#94A3B8">FOLDER: 06-NOTION-TEMPLATES/Spreadsheets/</text>
  </g>

  <g transform="translate(1182, 772)">
    <rect x="0" y="0" width="356" height="264" rx="12" fill="#1E293B" stroke="#F59E0B" stroke-width="1.5"/>
    <text x="20" y="32" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#FBBF24">04 // WEB APP, DESIGN &amp; AUTOMATION</text>
    <text x="20" y="62" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• SaaS-Lite Web Companion App (318 KB HTML)</text>
    <text x="20" y="88" font-family="Inter, Arial, sans-serif" font-size="13" fill="#2DD4BF">• Interactive Design &amp; Photo Customizer Studio</text>
    <text x="20" y="114" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• Upload Custom Photos/Logos -> Export PNG/SVG</text>
    <text x="20" y="140" font-family="Inter, Arial, sans-serif" font-size="13" fill="#2DD4BF">• 3 Make/Zapier/n8n JSON Automation Flows</text>
    <text x="20" y="166" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• Interactive Funnel Page &amp; 5-Email Sequence</text>
    <text x="20" y="192" font-family="Inter, Arial, sans-serif" font-size="13" fill="#E2E8F0">• Pro Activation Code: FREELANCER-OS-PRO-2026</text>
    <text x="20" y="226" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700" fill="#94A3B8">FOLDER: 07-TOOLS/ • 08-COVERS/ • 14-AUTO/</text>
  </g>

  <rect x="0" y="1088" width="1600" height="12" fill="url(#posterAccent)"/>
</svg>"""


def build_chapter_cheat_sheet_svg(ch_meta: dict, ch_prompts: list[dict]) -> str:
    """Build cheat-sheet-chXX.svg (viewBox 0 0 1200 1600) with >= 25 <text> elements and 6 structured visual panels."""
    ch_num = ch_meta["ch"]
    esc = html.escape

    # Format prompt rows (5 prompts per chapter)
    prompt_svg_rows = []
    for idx, p in enumerate(ch_prompts[:5]):
        py = 1090 + idx * 72
        pid = esc(f"Prompt {p['id']}")
        ptitle = esc(p["title"][:48] + ("..." if len(p["title"]) > 48 else ""))
        pwhen = esc(p["when_to_run"][:54] + ("..." if len(p["when_to_run"]) > 54 else ""))
        prompt_svg_rows.append(
            f"""
    <rect x="64" y="{py}" width="516" height="62" rx="8" fill="#1E293B" stroke="#334155" stroke-width="1.5"/>
    <rect x="64" y="{py}" width="118" height="62" rx="8" fill="#0284C7"/>
    <text x="123" y="{py + 36}" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#FFFFFF" text-anchor="middle">{pid}</text>
    <text x="196" y="{py + 26}" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="800" fill="#FFFFFF">{ptitle}</text>
    <text x="196" y="{py + 48}" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="500" fill="#94A3B8">Trigger: {pwhen}</text>"""
        )

    prompts_block = "\n".join(prompt_svg_rows)

    s1_t, s1_d = ch_meta["steps"][0]
    s2_t, s2_d = ch_meta["steps"][1]
    s3_t, s3_d = ch_meta["steps"][2]
    s4_t, s4_d = ch_meta["steps"][3]

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1600" width="1200" height="1600">
  <defs>
    <linearGradient id="csBg{ch_num}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B1120"/>
      <stop offset="55%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
    <linearGradient id="csBar{ch_num}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284C7"/>
      <stop offset="100%" stop-color="#0D9488"/>
    </linearGradient>
  </defs>

  <rect width="1200" height="1600" fill="url(#csBg{ch_num})"/>
  <rect x="0" y="0" width="1200" height="14" fill="url(#csBar{ch_num})"/>

  <!-- TOP HEADER BAR -->
  <rect x="44" y="34" width="1112" height="148" rx="16" fill="#1E293B" stroke="#0284C7" stroke-width="2.5"/>
  <text x="72" y="72" font-family="JetBrains Mono, Consolas, monospace" font-size="15" font-weight="800" fill="#38BDF8" letter-spacing="1.5">CHAPTER {ch_num:02d} VISUAL CHEAT SHEET // {esc(ch_meta['part'])}</text>
  <rect x="880" y="48" width="252" height="36" rx="8" fill="#0D9488"/>
  <text x="1006" y="71" font-family="JetBrains Mono, Consolas, monospace" font-size="13.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">{esc(ch_meta['time_to_run'])}</text>

  <text x="72" y="118" font-family="Inter, Arial, sans-serif" font-size="31" font-weight="900" fill="#FFFFFF">Ch {ch_num:02d}: {esc(ch_meta['title'])}</text>
  <text x="72" y="154" font-family="Inter, Arial, sans-serif" font-size="16" font-weight="600" fill="#CBD5E1">{esc(ch_meta['subtitle'])}</text>

  <!-- PANEL 1 (TOP-LEFT): 60-SECOND EXECUTIVE TL;DR -->
  <rect x="44" y="206" width="546" height="330" rx="16" fill="#0F172A" stroke="#0284C7" stroke-width="2"/>
  <rect x="44" y="206" width="546" height="48" rx="16" fill="#0284C7"/>
  <text x="68" y="236" font-family="JetBrains Mono, Consolas, monospace" font-size="15" font-weight="800" fill="#FFFFFF">PANEL 01 // THE 60-SECOND EXECUTIVE TL;DR</text>

  <text x="68" y="288" font-family="Inter, Arial, sans-serif" font-size="14.5" font-weight="700" fill="#F8FAFC">{esc(ch_meta['tldr'][0][:68])}</text>
  <text x="68" y="310" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="500" fill="#94A3B8">{esc(ch_meta['tldr'][0][68:])}</text>

  <text x="68" y="366" font-family="Inter, Arial, sans-serif" font-size="14.5" font-weight="700" fill="#F8FAFC">{esc(ch_meta['tldr'][1][:68])}</text>
  <text x="68" y="388" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="500" fill="#94A3B8">{esc(ch_meta['tldr'][1][68:])}</text>

  <text x="68" y="444" font-family="Inter, Arial, sans-serif" font-size="14.5" font-weight="700" fill="#F8FAFC">{esc(ch_meta['tldr'][2][:68])}</text>
  <text x="68" y="466" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="500" fill="#94A3B8">{esc(ch_meta['tldr'][2][68:])}</text>

  <rect x="68" y="488" width="498" height="32" rx="6" fill="#1E293B"/>
  <text x="317" y="509" font-family="JetBrains Mono, Consolas, monospace" font-size="12.5" font-weight="700" fill="#38BDF8" text-anchor="middle">{esc(ch_meta['gate'])}</text>

  <!-- PANEL 2 (TOP-RIGHT): CORE NAMED FRAMEWORK & FORMULA -->
  <rect x="610" y="206" width="546" height="330" rx="16" fill="#0F172A" stroke="#0D9488" stroke-width="2"/>
  <rect x="610" y="206" width="546" height="48" rx="16" fill="#0D9488"/>
  <text x="634" y="236" font-family="JetBrains Mono, Consolas, monospace" font-size="15" font-weight="800" fill="#FFFFFF">PANEL 02 // CORE NAMED FRAMEWORK &amp; EQUATION</text>

  <text x="634" y="292" font-family="JetBrains Mono, Consolas, monospace" font-size="15" font-weight="800" fill="#2DD4BF">{esc(ch_meta['formula_name'])}</text>
  <rect x="634" y="312" width="498" height="104" rx="12" fill="#1E293B" stroke="#2DD4BF" stroke-width="2"/>
  <text x="883" y="356" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#FFFFFF" text-anchor="middle">{esc(ch_meta['formula_eq'][:56])}</text>
  <text x="883" y="386" font-family="JetBrains Mono, Consolas, monospace" font-size="13.5" font-weight="700" fill="#38BDF8" text-anchor="middle">{esc(ch_meta['formula_eq'][56:])}</text>

  <text x="634" y="452" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="700" fill="#E2E8F0">OPERATIONAL BENCHMARK RULE:</text>
  <text x="634" y="478" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="600" fill="#94A3B8">{esc(ch_meta['formula_bench'])}</text>
  <text x="634" y="512" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700" fill="#FBBF24">SYNCED WORKBOOK: Worksheet {ch_num}.1 (US Letter, A4, Word &amp; Web App)</text>

  <!-- PANEL 3 (MIDDLE FULL-WIDTH): 4-STEP VISUAL EXECUTION PIPELINE -->
  <rect x="44" y="560" width="1112" height="430" rx="16" fill="#0F172A" stroke="#334155" stroke-width="2"/>
  <rect x="44" y="560" width="1112" height="48" rx="16" fill="#1E293B"/>
  <text x="68" y="590" font-family="JetBrains Mono, Consolas, monospace" font-size="15" font-weight="800" fill="#38BDF8">PANEL 03 // STEP-BY-STEP EXECUTION FLOW (60-SECOND ACTION PIPELINE)</text>

  <g transform="translate(68, 630)">
    <rect x="0" y="0" width="520" height="155" rx="12" fill="#1E293B" stroke="#0284C7" stroke-width="2"/>
    <rect x="0" y="0" width="520" height="38" rx="12" fill="#0284C7"/>
    <text x="18" y="25" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#FFFFFF">{esc(s1_t)}</text>
    <text x="18" y="76" font-family="Inter, Arial, sans-serif" font-size="14.5" font-weight="600" fill="#F8FAFC">{esc(s1_d[:56])}</text>
    <text x="18" y="102" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="500" fill="#CBD5E1">{esc(s1_d[56:])}</text>
    <text x="18" y="136" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700" fill="#38BDF8">GATE CHECK 01 --&gt; VERIFY BASELINE INPUTS</text>
  </g>

  <g transform="translate(612, 630)">
    <rect x="0" y="0" width="520" height="155" rx="12" fill="#1E293B" stroke="#0284C7" stroke-width="2"/>
    <rect x="0" y="0" width="520" height="38" rx="12" fill="#0284C7"/>
    <text x="18" y="25" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#FFFFFF">{esc(s2_t)}</text>
    <text x="18" y="76" font-family="Inter, Arial, sans-serif" font-size="14.5" font-weight="600" fill="#F8FAFC">{esc(s2_d[:56])}</text>
    <text x="18" y="102" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="500" fill="#CBD5E1">{esc(s2_d[56:])}</text>
    <text x="18" y="136" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700" fill="#38BDF8">GATE CHECK 02 --&gt; RUN AI SYNTHESIS PROMPT</text>
  </g>

  <g transform="translate(68, 808)">
    <rect x="0" y="0" width="520" height="155" rx="12" fill="#1E293B" stroke="#0D9488" stroke-width="2"/>
    <rect x="0" y="0" width="520" height="38" rx="12" fill="#0D9488"/>
    <text x="18" y="25" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#FFFFFF">{esc(s3_t)}</text>
    <text x="18" y="76" font-family="Inter, Arial, sans-serif" font-size="14.5" font-weight="600" fill="#F8FAFC">{esc(s3_d[:56])}</text>
    <text x="18" y="102" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="500" fill="#CBD5E1">{esc(s3_d[56:])}</text>
    <text x="18" y="136" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700" fill="#2DD4BF">GATE CHECK 03 --&gt; APPLY HUMAN QA FILTER</text>
  </g>

  <g transform="translate(612, 808)">
    <rect x="0" y="0" width="520" height="155" rx="12" fill="#1E293B" stroke="#0D9488" stroke-width="2"/>
    <rect x="0" y="0" width="520" height="38" rx="12" fill="#0D9488"/>
    <text x="18" y="25" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#FFFFFF">{esc(s4_t)}</text>
    <text x="18" y="76" font-family="Inter, Arial, sans-serif" font-size="14.5" font-weight="600" fill="#F8FAFC">{esc(s4_d[:56])}</text>
    <text x="18" y="102" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="500" fill="#CBD5E1">{esc(s4_d[56:])}</text>
    <text x="18" y="136" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="700" fill="#2DD4BF">GATE CHECK 04 --&gt; LOCK PERMANENT SYSTEM</text>
  </g>

  <!-- PANEL 4 (BOTTOM-LEFT): THE 5 CHAPTER AI PROMPTS QUICK-CALLER -->
  <rect x="44" y="1014" width="556" height="456" rx="16" fill="#0F172A" stroke="#0284C7" stroke-width="2"/>
  <rect x="44" y="1014" width="556" height="48" rx="16" fill="#0284C7"/>
  <text x="68" y="1044" font-family="JetBrains Mono, Consolas, monospace" font-size="15" font-weight="800" fill="#FFFFFF">PANEL 04 // 5 CHAPTER AI PROMPTS QUICK-CALLER</text>
  {prompts_block}

  <!-- PANEL 5 (BOTTOM-RIGHT): RED-FLAG CIRCUIT BREAKERS & TARGET KPI -->
  <rect x="620" y="1014" width="536" height="456" rx="16" fill="#0F172A" stroke="#F59E0B" stroke-width="2"/>
  <rect x="620" y="1014" width="536" height="48" rx="16" fill="#D97706"/>
  <text x="644" y="1044" font-family="JetBrains Mono, Consolas, monospace" font-size="15" font-weight="800" fill="#FFFFFF">PANEL 05 // RED-FLAG CIRCUIT BREAKERS &amp; KPI</text>

  <rect x="640" y="1084" width="496" height="78" rx="10" fill="#1E293B" stroke="#EF4444" stroke-width="1.5"/>
  <text x="658" y="1114" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="700" fill="#FCA5A5">{esc(ch_meta['red_flags'][0][:62])}</text>
  <text x="658" y="1138" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="500" fill="#E2E8F0">{esc(ch_meta['red_flags'][0][62:])}</text>

  <rect x="640" y="1176" width="496" height="78" rx="10" fill="#1E293B" stroke="#EF4444" stroke-width="1.5"/>
  <text x="658" y="1206" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="700" fill="#FCA5A5">{esc(ch_meta['red_flags'][1][:62])}</text>
  <text x="658" y="1230" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="500" fill="#E2E8F0">{esc(ch_meta['red_flags'][1][62:])}</text>

  <rect x="640" y="1268" width="496" height="78" rx="10" fill="#1E293B" stroke="#EF4444" stroke-width="1.5"/>
  <text x="658" y="1298" font-family="Inter, Arial, sans-serif" font-size="13.5" font-weight="700" fill="#FCA5A5">{esc(ch_meta['red_flags'][2][:62])}</text>
  <text x="658" y="1322" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="500" fill="#E2E8F0">{esc(ch_meta['red_flags'][2][62:])}</text>

  <rect x="640" y="1362" width="496" height="90" rx="10" fill="#162238" stroke="#2DD4BF" stroke-width="2"/>
  <text x="658" y="1394" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#2DD4BF">{esc(ch_meta['kpi_target'][:64])}</text>
  <text x="658" y="1416" font-family="JetBrains Mono, Consolas, monospace" font-size="12.5" font-weight="700" fill="#FFFFFF">{esc(ch_meta['kpi_target'][64:])}</text>
  <text x="658" y="1438" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="600" fill="#FBBF24">{esc(ch_meta['script_ref'])}</text>

  <!-- BOTTOM FOOTER BAR -->
  <rect x="44" y="1494" width="1112" height="68" rx="12" fill="#1E293B"/>
  <text x="72" y="1534" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#38BDF8">THE AI FREELANCER OPERATING SYSTEM  •  60-SECOND VISUAL SHORTCUT ATLAS (PAGE {ch_num + 2} OF 12)</text>
  <text x="1128" y="1534" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#2DD4BF" text-anchor="end">CHAPTER {ch_num:02d} / 10</text>
  <rect x="0" y="1586" width="1200" height="14" fill="url(#csBar{ch_num})"/>
</svg>"""


def build_visual_shortcut_atlas():
    """Generate all 11 Cheat Sheet SVGs, 11 high-res PNGs, and the 12-Page Visual Shortcut Atlas PDF."""
    CHEAT_DIR.mkdir(parents=True, exist_ok=True)
    PDF_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    browser_exe = find_headless_browser()
    all_prompts = extract_all_prompts()

    # 1. Master Ecosystem Poster SVG + PNG (1600 x 1100)
    poster_svg = build_master_ecosystem_poster_svg()
    poster_svg_path = CHEAT_DIR / "00-ECOSYSTEM-MASTER-MAP-POSTER.svg"
    poster_png_path = CHEAT_DIR / "00-ECOSYSTEM-MASTER-MAP-POSTER.png"
    poster_svg_path.write_text(poster_svg, encoding="utf-8")
    render_svg_to_png(browser_exe, poster_svg_path, poster_png_path, 1600, 1100)

    # 2. Chapters 1..10 One-Page Visual Cheat Sheets (1200 x 1600)
    chapter_svg_strings = []
    for ch_meta in CHEAT_SHEET_DATA:
        ch_num = ch_meta["ch"]
        ch_prompts = [p for p in all_prompts if p["chapter"] == ch_num]
        svg_str = build_chapter_cheat_sheet_svg(ch_meta, ch_prompts)
        chapter_svg_strings.append(svg_str)

        svg_path = CHEAT_DIR / f"cheat-sheet-ch{ch_num:02d}.svg"
        png_path = CHEAT_DIR / f"cheat-sheet-ch{ch_num:02d}.png"
        svg_path.write_text(svg_str, encoding="utf-8")
        render_svg_to_png(browser_exe, svg_path, png_path, 1200, 1600)

    # 3. Compile 12-Page Full-Color Visual Shortcut Atlas PDF
    pages_html = []

    # Page 1: Cover & How to Use the 60-Second Visual Shortcut Atlas
    page1_cover = """
    <div class="atlas-page cover-page">
      <div class="cover-inner">
        <div class="badge-bar">PRACTITIONER VISUAL COMPANION EDITION • 12 FULL-COLOR INFOGRAPHIC PAGES</div>
        <h1>THE 60-SECOND VISUAL<br/><span>SHORTCUT ATLAS</span></h1>
        <p class="subtitle">The Complete Skimmer &amp; Action-Taker Companion to <em>The AI Freelancer Operating System</em> — Master Every Chapter, Formula, Decision Gate &amp; AI Prompt Trigger in 60 Seconds Flat</p>
        <div class="grid-cards">
          <div class="c-card">
            <div class="c-tag">PAGE 02 // WALL POSTER</div>
            <div class="c-title">Master 5-Gate Ecosystem Map</div>
            <div class="c-desc">A birds-eye architectural poster mapping all 5 Lifecycle Gates, 10 Chapters, 50 Prompts, 12 Boundary Scripts, Web App Modules, Notion Databases, Excel Tabs, and Office Templates.</div>
          </div>
          <div class="c-card">
            <div class="c-tag">PAGES 03–06 // PART I &amp; II</div>
            <div class="c-title">Diagnostics, Tiers, Triage &amp; Pricing</div>
            <div class="c-desc">One-page cheat sheets for Chapters 1–4: The 7-Day EHR Leak Audit, 3-Tier Offer Matrix, 20-Point P.A.C.E. Lead Scorer, 10-Min B.R.I.E.F. Proposals &amp; B.C.R. Pricing Formula.</div>
          </div>
          <div class="c-card">
            <div class="c-tag">PAGES 07–09 // PART III</div>
            <div class="c-title">Onboarding, 20/60/20 QA &amp; Scope</div>
            <div class="c-desc">One-page cheat sheets for Chapters 5–7: The 48-Hour Pre-Flight Asset Gate, Day-for-Day Timeline Shift Rule, 20/60/20 Sandwich Execution, 4-Gate QA &amp; P.V.P. Change Orders.</div>
          </div>
          <div class="c-card">
            <div class="c-tag">PAGES 10–12 // PART IV</div>
            <div class="c-title">Async Delivery, Retainers &amp; CEO</div>
            <div class="c-desc">One-page cheat sheets for Chapters 8–10: The 3-Pillar Friday Status Digest, 3-Min Loom Structure, Executive Handover Vault, 48h Retainer Bridge &amp; 20-Min Friday CEO Review.</div>
          </div>
        </div>
        <div class="how-to-box">
          <h3>HOW TO USE THIS VISUAL ATLAS WITHOUT READING 75,000 WORDS</h3>
          <p><strong>1. Pin Page 2 to Your Desk or Second Monitor:</strong> Use the <em>Master Ecosystem Map Poster</em> to locate the exact AI Prompt, Boundary Script, Word Contract, or Excel Tab for any client situation in under 10 seconds.</p>
          <p><strong>2. Scan Any Chapter in 60 Seconds:</strong> Before a discovery call, kickoff, or Friday review, open the corresponding Chapter Cheat Sheet (Pages 3–12) and read <em>Panel 01 (TL;DR)</em>, <em>Panel 02 (Core Formula)</em>, and <em>Panel 03 (4-Step Action Pipeline)</em>.</p>
          <p><strong>3. Trigger the Right Prompt or Script Immediately:</strong> Check <em>Panel 04 (5 Prompts Quick-Caller)</em> and <em>Panel 05 (Red-Flag Circuit Breakers)</em> to copy-paste the exact prompt inside <code>freelancer-os-app.html</code>.</p>
        </div>
        <div class="footer-strip">DIGITAL KNOWLEDGE PRODUCT STUDIO • US / UK / CANADA / AUSTRALIA EDITION • PAGE 01 OF 12</div>
      </div>
    </div>
    """
    pages_html.append(page1_cover)

    # Page 2: Master Ecosystem Map Poster (Rotated or fitted cleanly into page 2)
    pages_html.append(f'<div class="atlas-page poster-page">{poster_svg}</div>')

    # Pages 3..12: Chapters 1..10 Cheat Sheets
    for svg_s in chapter_svg_strings:
        pages_html.append(f'<div class="atlas-page sheet-page">{svg_s}</div>')

    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  @page {{ size: 8.5in 11in; margin: 0; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 8.5in;
    background: #0B1120;
    font-family: 'Inter', Arial, sans-serif;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .atlas-page {{
    width: 8.5in;
    height: 11in;
    page-break-after: always;
    break-after: page;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0B1120;
    position: relative;
  }}
  .atlas-page:last-child {{
    page-break-after: auto;
    break-after: auto;
  }}
  .sheet-page svg {{
    width: 8.5in;
    height: 11in;
    display: block;
  }}
  .poster-page svg {{
    width: 8.3in;
    height: auto;
    max-height: 10.6in;
    display: block;
  }}
  .cover-page {{
    padding: 0.45in;
    background: linear-gradient(135deg, #0B1120 0%, #0F172A 60%, #1E293B 100%);
    color: #F8FAFC;
  }}
  .cover-inner {{
    width: 100%;
    height: 100%;
    border: 2px solid #0284C7;
    border-radius: 16px;
    padding: 0.4in;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: rgba(15, 23, 42, 0.85);
  }}
  .badge-bar {{
    background: #1E293B;
    border: 1px solid #0284C7;
    color: #38BDF8;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 10pt;
    font-weight: 800;
    padding: 8px 14px;
    border-radius: 8px;
    text-align: center;
    letter-spacing: 0.08em;
  }}
  h1 {{
    font-size: 34pt;
    font-weight: 900;
    line-height: 1.08;
    color: #FFFFFF;
    margin-top: 10px;
  }}
  h1 span {{ color: #2DD4BF; }}
  .subtitle {{
    font-size: 11.5pt;
    color: #CBD5E1;
    line-height: 1.45;
    margin-top: 8px;
  }}
  .grid-cards {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin: 14px 0;
  }}
  .c-card {{
    background: #1E293B;
    border: 1.5px solid #334155;
    border-radius: 10px;
    padding: 12px;
  }}
  .c-tag {{
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 8.5pt;
    font-weight: 800;
    color: #38BDF8;
    margin-bottom: 4px;
  }}
  .c-title {{
    font-size: 12pt;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 4px;
  }}
  .c-desc {{
    font-size: 9.2pt;
    color: #CBD5E1;
    line-height: 1.4;
  }}
  .how-to-box {{
    background: #162238;
    border: 1.5px solid #0D9488;
    border-radius: 12px;
    padding: 14px 16px;
  }}
  .how-to-box h3 {{
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 10pt;
    color: #2DD4BF;
    margin-bottom: 8px;
  }}
  .how-to-box p {{
    font-size: 9.5pt;
    color: #E2E8F0;
    line-height: 1.45;
    margin-bottom: 6px;
  }}
  .footer-strip {{
    background: #0F172A;
    padding: 8px 12px;
    border-radius: 8px;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 9pt;
    font-weight: 700;
    color: #38BDF8;
    text-align: center;
  }}
</style>
</head>
<body>
{"".join(pages_html)}
</body>
</html>"""

    atlas_pdf_primary = CHEAT_DIR / "the-ai-freelancer-os-visual-shortcut-atlas.pdf"
    atlas_pdf_export = PDF_EXPORT_DIR / "the-ai-freelancer-os-visual-shortcut-atlas.pdf"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_html = Path(tmpdir) / "visual_atlas.html"
        tmp_html.write_text(full_html, encoding="utf-8")
        cmd = [
            browser_exe,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={str(atlas_pdf_primary)}",
            tmp_html.as_uri(),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    shutil.copy2(atlas_pdf_primary, atlas_pdf_export)
    print(f"[Upgrade 1] Built 11 Visual Cheat Sheet SVGs, 11 PNGs, and 12-Page Visual Shortcut Atlas PDF ({atlas_pdf_primary.stat().st_size:,} bytes).")


# ==============================================================================
# UPGRADE 4: 8-TAB CHARTED EXCEL FINANCIAL, INVOICE, TIME & TAX COMMAND CENTER
# ==============================================================================
def build_8tab_excel_command_center():
    SPREADSHEETS_DIR.mkdir(parents=True, exist_ok=True)
    HYBRID_BUNDLE_DIR.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.Workbook()
    default_ws = wb.active

    navy_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    sky_fill = PatternFill(start_color="0284C7", end_color="0284C7", fill_type="solid")
    teal_fill = PatternFill(start_color="0D9488", end_color="0D9488", fill_type="solid")
    kpi_fill = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")

    title_font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    sub_font = Font(name="Calibri", size=10.5, italic=True, color="E2E8F0")
    bold_navy = Font(name="Calibri", size=11, bold=True, color="0F172A")

    # --------------------------------------------------------------------------
    # TAB 0: 00_Executive_Visual_Dashboard (With 3 Native OpenPyXL Charts)
    # --------------------------------------------------------------------------
    ws0 = wb.create_sheet(title="00_Executive_Visual_Dashboard")
    ws0["A1"] = "THE AI FREELANCER OPERATING SYSTEM — TAB 00: EXECUTIVE VISUAL COMMAND DASHBOARD (LIVE KPIs & CHARTS)"
    ws0["A2"] = "Master Visual Command Center • Synced with Tabs 01–07 • Features 3 Embedded Live Native Excel Charts (Cashflow BarChart, 4-Bucket PieChart & Client EHR Chart)"
    for r in (1, 2):
        for c in range(1, 9):
            ws0.cell(row=r, column=c).fill = navy_fill
    ws0["A1"].font = title_font
    ws0["A2"].font = sub_font

    ws0.append([])
    ws0.append(["KPI Card ID", "Executive Operating Metric", "Live Formula Value", "Target Benchmark", "Current Status / Automated Action Signal"])
    style_Range_Header(ws0, 4, 5, "0F172A")

    exec_kpis = [
        ("KPI-01", "Baseline True Effective Hourly Rate (EHR)", "='01_EHR_Leak_Audit'!C14", "$85.00 / hr", '=IF(C5>=75,"ON TARGET","BELOW TARGET — RUN CH 1-4 UPGRADES")'),
        ("KPI-02", "Billable Craft Utilization Ratio (Bucket A %)", "='01_EHR_Leak_Audit'!C13", "65.0%", '=IF(C6>=0.65,"HEALTHY UTILIZATION","SHADOW LABOR LEAK DETECTED")'),
        ("KPI-03", "Annualized 48-Week Unbilled Revenue Leak", "='01_EHR_Leak_Audit'!C18", "$0.00 / yr", "Recoverable capacity via 5-Gate AI OS"),
        ("KPI-04", "Option 2 Core Transformation Anchor Price", "='02_BCR_Scope_Pricing'!C22", "$4,950.00", "50/25/25 Milestone Billing Enabled"),
        ("KPI-05", "Active Client Portfolio Blended EHR ($/hr)", "='03_Client_80_20_Roster'!E13", "$85.00 / hr", "='03_Client_80_20_Roster'!H13"),
        ("KPI-06", "Weekly Capacity Utilization & Rate-Raise Trigger", "='03_Client_80_20_Roster'!C18", "85.0% Trigger", "='03_Client_80_20_Roster'!E18"),
        ("KPI-07", "90-Day Projected Gross Cashflow Inflow", "='04_90Day_Pipeline_Cashflow'!F17", "$35,000.00", "12-Week Retainer + Milestone + Pipeline"),
        ("KPI-08", "90-Day Net Owner Profit (After Overhead & 25% Tax)", "='04_90Day_Pipeline_Cashflow'!I17", "$24,000.00", "Protected Take-Home Owner Compensation"),
        ("KPI-09", "Current Open Client Invoice Balance Due", "='05_Client_Invoice_Generator'!E18", "Paid on Time", "='05_Client_Invoice_Generator'!E20"),
        ("KPI-10", "Annual Net Pre-Tax Business Profit (12-Month Ledger)", "='07_Annual_Tax_Expense_Ledger'!H17", "$85,000.00+", "Synced with Tab 07 Tax & Expense Ledger"),
    ]
    for idx, rdata in enumerate(exec_kpis, start=5):
        ws0.append(list(rdata))
        for c in range(1, 6):
            ws0.cell(row=idx, column=c).fill = kpi_fill if idx % 2 == 1 else PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
        ws0.cell(row=idx, column=2).font = bold_navy
        ws0.cell(row=idx, column=3).font = bold_navy

    for r in (5, 7, 8, 9, 11, 12, 13, 14):
        ws0.cell(row=r, column=3).number_format = "$#,##0.00"
    for r in (6, 10):
        ws0.cell(row=r, column=3).number_format = "0.0%"

    apply_sheet_polish(ws0, {1: 15, 2: 48, 3: 24, 4: 22, 5: 46}, freeze_cell="A5")

    # --------------------------------------------------------------------------
    # TAB 1: 01_EHR_Leak_Audit
    # --------------------------------------------------------------------------
    ws1 = wb.create_sheet(title="01_EHR_Leak_Audit")
    ws1["A1"] = "THE AI FREELANCER OPERATING SYSTEM — TAB 01: 7-DAY TIME & REVENUE LEAK DIAGNOSTIC (EHR AUDIT)"
    ws1["A2"] = "Synced with Chapter 1, Prompt 1.1 & Worksheet 1.1 • Edit input cells in Column C; formulas calculate automatically."
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

    for r in (5, 6, 14, 15, 16, 17, 18, 19):
        ws1.cell(row=r, column=3).number_format = "$#,##0.00"
    for r in (7, 8, 9, 10, 11, 12):
        ws1.cell(row=r, column=3).number_format = '0.0 "hrs"'
    ws1.cell(row=13, column=3).number_format = "0.0%"
    apply_sheet_polish(ws1, {1: 15, 2: 52, 3: 24, 4: 16, 5: 50}, freeze_cell="A5")

    # Add embedded PieChart on Tab 1 (01_EHR_Leak_Audit)
    pie_tab1 = PieChart()
    pie_tab1.title = "Weekly 4-Bucket Time Allocation (Hours)"
    pie_tab1.width = 14
    pie_tab1.height = 9
    data_ref1 = Reference(ws1, min_col=3, min_row=7, max_row=10)
    cats_ref1 = Reference(ws1, min_col=2, min_row=7, max_row=10)
    pie_tab1.add_data(data_ref1, titles_from_data=False)
    pie_tab1.set_categories(cats_ref1)
    ws1.add_chart(pie_tab1, "G4")

    # --------------------------------------------------------------------------
    # TAB 2: 02_BCR_Scope_Pricing
    # --------------------------------------------------------------------------
    ws2 = wb.create_sheet(title="02_BCR_Scope_Pricing")
    ws2["A1"] = "THE AI FREELANCER OPERATING SYSTEM — TAB 02: WBS ESTIMATOR & B.C.R. 3-TIER PROPOSAL PRICING ENGINE"
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
    ws3["A1"] = "THE AI FREELANCER OPERATING SYSTEM — TAB 03: 80/20 CLIENT PROFITABILITY ROSTER & 85% RATE-RAISE TRIGGER"
    ws3["A2"] = "Synced with Chapter 10 & Worksheet 10.1 • Automatically isolates Whale-Trap accounts vs. Star Retainer accounts"
    for r in (1, 2):
        for c in range(1, 9):
            ws3.cell(row=r, column=c).fill = navy_fill
    ws3["A1"].font = title_font
    ws3["A2"].font = sub_font

    ws3.append([])
    ws3.append(["Account ID", "Active Client / Retainer Account", "Monthly Gross Fee ($)", "Real Monthly Hours", "Realized Client EHR ($/hr)", "Revenue Share (%)", "Friction Score (1-5)", "Automated 80/20 CEO Action Recommendation"])
    style_Range_Header(ws3, 4, 8, "0F172A")

    clients_data = [
        ("CLI-01", "Apex FinTech Cloud (Growth Retainer)", 2800.00, 24.0, 1),
        ("CLI-02", "Verde Beverage Co. (Brand & Packaging Sprint)", 2200.00, 21.5, 2),
        ("CLI-03", "VantagePoint Software (Onboarding Redesign)", 1800.00, 16.0, 2),
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
    ws4["A1"] = "THE AI FREELANCER OPERATING SYSTEM — TAB 04: 12-WEEK ROLLING CASHFLOW, PIPELINE & TAX RESERVE FORECASTER"
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

    # --------------------------------------------------------------------------
    # TAB 5: 05_Client_Invoice_Generator (Print-Ready Formula Invoice Template)
    # --------------------------------------------------------------------------
    ws5 = wb.create_sheet(title="05_Client_Invoice_Generator")
    ws5["A1"] = "COMMERCIAL MILESTONE & CHANGE ORDER INVOICE — #INV-2026-104"
    ws5["A2"] = "Billed From: [Your Studio Name]  •  Billed To: Apex FinTech Cloud (Attn: Elena Rostova, SPOC)  •  Terms: Due Within 5 Calendar Days"
    for r in (1, 2):
        for c in range(1, 6):
            ws5.cell(row=r, column=c).fill = navy_fill
    ws5["A1"].font = title_font
    ws5["A2"].font = sub_font

    ws5.append([])
    ws5.append(["Item Code", "Deliverable / Milestone / Change Order Description", "Quantity / Hrs", "Unit Rate ($)", "Line Total (Formula)"])
    style_Range_Header(ws5, 4, 5, "0F172A")

    inv_items = [
        ("MS-01", "Option 2: Core Transformation Sprint — 50% Kickoff Deposit (Paid 2026-10-15)", 1.0, 2475.00),
        ("MS-02", "Option 2: Core Transformation Sprint — 25% Midpoint Prototype Milestone", 1.0, 1237.50),
        ("MS-03", "Option 2: Core Transformation Sprint — 25% Final Pre-Transfer Balance", 1.0, 1237.50),
        ("CO-01", "Approved P.V.P. Change Order #CO-2026-001 (2 Regional UK/AU Landing Pages)", 1.0, 490.00),
        ("CO-02", "Approved P.V.P. Change Order #CO-2026-001 (Custom HubSpot Webhook Mapping)", 1.0, 295.00),
        ("PT-01", "Pass-Through Commercial Font & Plugin License (At 1.0x Direct Cost)", 1.0, 150.00),
    ]
    for idx, (icode, idesc, iqty, irate) in enumerate(inv_items, start=5):
        ws5.append([icode, idesc, iqty, irate, f"=ROUND(C{idx}*D{idx},2)"])
        ws5.cell(row=idx, column=3).number_format = "0.0"
        ws5.cell(row=idx, column=4).number_format = "$#,##0.00"
        ws5.cell(row=idx, column=5).number_format = "$#,##0.00"

    ws5.append([])
    ws5.append(["SUMMARY", "Invoice Financial Summary & Milestone Settlement Tracker", "Parameter", "Notes / Terms", "Amount (USD)"])
    style_Range_Header(ws5, 12, 5, "0284C7")

    inv_summary = [
        ("SUBTOTAL", "Gross Contract + Approved Change Orders Subtotal", "", "Sum of Lines 5–10", "=SUM(E5:E10)"),
        ("TAX-RATE", "Applicable Sales / VAT / GST Rate (If Required by Jurisdiction)", 0.00, "Edit C14 if VAT/GST applies", "=ROUND(E13*C14,2)"),
        ("TOTAL", "Total Gross Invoice Amount (Including Tax)", "", "Total Contract Value", "=E13+E14"),
        ("PAID-DEP", "Less: Payments & Deposits Already Received to Date", "", "50% Kickoff + 25% Midpoint Paid", 3712.50),
        ("DAYS-LATE", "Days Past Invoice Due Date (Enter 0 if Current)", 0, "Triggers Day +3/+7/+14 Escalation", '=IF(C17>=14,150,0)'),
        ("BAL-DUE", "CURRENT BALANCE DUE UPON RECEIPT (PRE-TRANSFER GATE)", "", "Payable via Stripe / ACH / Payoneer", "=E15-E16+E17"),
        ("SPLIT-50", "Reference: Standard 50% Kickoff Deposit on Gross Total", "", "Milestone 1 Gate", "=ROUND(E15*0.50,2)"),
        ("STATUS", "Automated Payment Gate & IP Transfer Governance Status", "", "Section 6.3 & 7.2 MSA Rule", '=IF(E18<=0,"PAID IN FULL — IP TRANSFERRED",IF(C17>=7,"OVERDUE >=7 DAYS — PAUSE STAGING (SCRIPT 10)","OPEN — AWAITING SETTLEMENT PRIOR TO LIVE PUSH"))'),
    ]
    for idx, rdata in enumerate(inv_summary, start=13):
        ws5.append(list(rdata))
        if idx in (13, 15, 18, 20):
            for c in range(1, 6):
                ws5.cell(row=idx, column=c).fill = kpi_fill
                ws5.cell(row=idx, column=c).font = bold_navy
        if idx in (13, 14, 15, 16, 17, 18, 19):
            ws5.cell(row=idx, column=5).number_format = "$#,##0.00"
    ws5.cell(row=14, column=3).number_format = "0.0%"

    apply_sheet_polish(ws5, {1: 15, 2: 56, 3: 18, 4: 34, 5: 28}, freeze_cell="A5")

    # --------------------------------------------------------------------------
    # TAB 6: 06_Daily_3Block_Time_Log (30-Day Daily Time-Block & Deep-Work Tracker)
    # --------------------------------------------------------------------------
    ws6 = wb.create_sheet(title="06_Daily_3Block_Time_Log")
    ws6["A1"] = "THE AI FREELANCER OPERATING SYSTEM — TAB 06: 30-DAY DAILY 3-BLOCK DEEP-WORK & EHR LOG"
    ws6["A2"] = "Synced with Chapter 1 & Chapter 10 • Tracks Block 1 (90-Min Maker Sprint), Block 2 (Client Craft), Block 3 (Admin/Comms) & Daily EHR"
    for r in (1, 2):
        for c in range(1, 10):
            ws6.cell(row=r, column=c).fill = navy_fill
    ws6["A1"].font = title_font
    ws6["A2"].font = sub_font

    ws6.append([])
    ws6.append([
        "Day #",
        "Date",
        "Block 1: 90m Maker Hrs",
        "Block 2: Client Craft Hrs",
        "Block 3: Admin/Sales Hrs",
        "Total Daily Hrs (Formula)",
        "Deep-Work Ratio (%)",
        "Daily Revenue Earned ($)",
        "Realized Daily EHR ($/hr)",
    ])
    style_Range_Header(ws6, 4, 9, "0F172A")

    for d_idx in range(1, 31):
        row_num = d_idx + 4
        is_weekend = d_idx % 7 in (6, 0)
        b1 = 0.0 if is_weekend else 1.5
        b2 = 0.0 if is_weekend else (4.5 if d_idx % 2 == 1 else 5.0)
        b3 = 0.0 if is_weekend else (1.0 if d_idx % 3 == 0 else 1.5)
        rev = 0.0 if is_weekend else (480.00 if d_idx % 2 == 1 else 540.00)

        tot_f = f"=SUM(C{row_num}:E{row_num})"
        dw_f = f"=IF(F{row_num}>0,(C{row_num}+D{row_num})/F{row_num},0)"
        ehr_f = f"=IF(F{row_num}>0,ROUND(H{row_num}/F{row_num},2),0)"

        ws6.append([f"Day {d_idx:02d}", f"2026-11-{d_idx:02d}", b1, b2, b3, tot_f, dw_f, rev, ehr_f])
        for c_i in (3, 4, 5, 6):
            ws6.cell(row=row_num, column=c_i).number_format = '0.0 "hrs"'
        ws6.cell(row=row_num, column=7).number_format = "0.0%"
        ws6.cell(row=row_num, column=8).number_format = "$#,##0.00"
        ws6.cell(row=row_num, column=9).number_format = "$#,##0.00"

    ws6.append([
        "30-DAY SUM",
        "Monthly Deep-Work Summary",
        "=SUM(C5:C34)",
        "=SUM(D5:D34)",
        "=SUM(E5:E34)",
        "=SUM(F5:F34)",
        "=(C35+D35)/F35",
        "=SUM(H5:H34)",
        "=ROUND(H35/F35,2)",
    ])
    for c in range(1, 10):
        ws6.cell(row=35, column=c).fill = kpi_fill
        ws6.cell(row=35, column=c).font = bold_navy
    for c_i in (3, 4, 5, 6):
        ws6.cell(row=35, column=c_i).number_format = '0.0 "hrs"'
    ws6.cell(row=35, column=7).number_format = "0.0%"
    ws6.cell(row=35, column=8).number_format = "$#,##0.00"
    ws6.cell(row=35, column=9).number_format = "$#,##0.00"

    apply_sheet_polish(ws6, {1: 15, 2: 18, 3: 22, 4: 22, 5: 22, 6: 22, 7: 20, 8: 24, 9: 24}, freeze_cell="A5")

    # --------------------------------------------------------------------------
    # TAB 7: 07_Annual_Tax_Expense_Ledger (12-Month Tax & Expense Ledger)
    # --------------------------------------------------------------------------
    ws7 = wb.create_sheet(title="07_Annual_Tax_Expense_Ledger")
    ws7["A1"] = "THE AI FREELANCER OPERATING SYSTEM — TAB 07: 12-MONTH BUSINESS EXPENSE, DEDUCTION & TAX RESERVE LEDGER"
    ws7["A2"] = "Compatible with US Schedule C, UK Self-Assessment, Canada T2125 & Australia Sole Trader Reporting • Automated 25% Tax Reserve & Net Margin"
    for r in (1, 2):
        for c in range(1, 11):
            ws7.cell(row=r, column=c).fill = navy_fill
    ws7["A1"].font = title_font
    ws7["A2"].font = sub_font

    ws7.append([])
    ws7.append([
        "Month",
        "Gross Collected Revenue ($)",
        "Software & AI Stack ($)",
        "Subcontractors & QA ($)",
        "Home Office, Internet & Gear ($)",
        "Payment Fees & Marketing ($)",
        "Total Tax-Deductible Expenses ($)",
        "Net Pre-Tax Profit ($)",
        "25% Estimated Tax Reserve ($)",
        "Net Post-Tax Owner Income ($)",
    ])
    style_Range_Header(ws7, 4, 10, "0F172A")

    months_data = [
        ("Jan 2026", 6800.00, 145.00, 400.00, 220.00, 195.00),
        ("Feb 2026", 7200.00, 145.00, 450.00, 220.00, 210.00),
        ("Mar 2026", 7650.00, 145.00, 500.00, 220.00, 225.00),
        ("Apr 2026", 8100.00, 155.00, 600.00, 220.00, 240.00),
        ("May 2026", 8400.00, 155.00, 600.00, 220.00, 250.00),
        ("Jun 2026", 8900.00, 155.00, 750.00, 220.00, 265.00),
        ("Jul 2026", 9200.00, 160.00, 750.00, 220.00, 275.00),
        ("Aug 2026", 9500.00, 160.00, 800.00, 220.00, 285.00),
        ("Sep 2026", 9850.00, 160.00, 850.00, 220.00, 295.00),
        ("Oct 2026", 10200.00, 165.00, 900.00, 220.00, 305.00),
        ("Nov 2026", 10600.00, 165.00, 950.00, 220.00, 315.00),
        ("Dec 2026", 11200.00, 165.00, 1000.00, 220.00, 330.00),
    ]
    for idx, (m_name, grev, sft, subc, offc, mkt) in enumerate(months_data, start=5):
        exp_f = f"=SUM(C{idx}:F{idx})"
        net_f = f"=B{idx}-G{idx}"
        tax_f = f"=ROUND(H{idx}*0.25,2)"
        take_f = f"=H{idx}-I{idx}"
        ws7.append([m_name, grev, sft, subc, offc, mkt, exp_f, net_f, tax_f, take_f])
        for c_i in range(2, 11):
            ws7.cell(row=idx, column=c_i).number_format = "$#,##0.00"

    ws7.append([
        "ANNUAL TOTAL",
        "=SUM(B5:B16)",
        "=SUM(C5:C16)",
        "=SUM(D5:D16)",
        "=SUM(E5:E16)",
        "=SUM(F5:F16)",
        "=SUM(G5:G16)",
        "=SUM(H5:H16)",
        "=SUM(I5:I16)",
        "=SUM(J5:J16)",
    ])
    for c in range(1, 11):
        ws7.cell(row=17, column=c).fill = kpi_fill
        ws7.cell(row=17, column=c).font = bold_navy
        if c >= 2:
            ws7.cell(row=17, column=c).number_format = "$#,##0.00"

    apply_sheet_polish(ws7, {1: 16, 2: 24, 3: 22, 4: 22, 5: 24, 6: 24, 7: 26, 8: 24, 9: 24, 10: 26}, freeze_cell="A5")

    # --------------------------------------------------------------------------
    # ADD 3 EMBEDDED NATIVE OPENPYXL CHARTS ON TAB 00 (00_Executive_Visual_Dashboard)
    # --------------------------------------------------------------------------
    # Chart 1: 12-Week Cashflow & Net Profit BarChart
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "12-Week Rolling Gross Inflow vs. Net Owner Profit ($)"
    chart1.y_axis.title = "USD ($)"
    chart1.x_axis.title = "Forecast Week"
    chart1.width = 16
    chart1.height = 10
    c1_data = Reference(ws4, min_col=6, min_row=4, max_col=9, max_row=16)
    c1_cats = Reference(ws4, min_col=1, min_row=5, max_row=16)
    chart1.add_data(c1_data, titles_from_data=True)
    chart1.set_categories(c1_cats)
    ws0.add_chart(chart1, "A17")

    # Chart 2: 4-Bucket Weekly Time Allocation PieChart
    chart2 = PieChart()
    chart2.title = "7-Day Audit: 4-Bucket Time Distribution (Hours)"
    chart2.width = 13
    chart2.height = 10
    c2_data = Reference(ws1, min_col=3, min_row=7, max_row=10)
    c2_cats = Reference(ws1, min_col=2, min_row=7, max_row=10)
    chart2.add_data(c2_data, titles_from_data=False)
    chart2.set_categories(c2_cats)
    ws0.add_chart(chart2, "F17")

    # Chart 3: 12-Month Gross Revenue vs. Post-Tax Owner Income LineChart
    chart3 = LineChart()
    chart3.title = "12-Month Gross Revenue vs. Net Post-Tax Income ($)"
    chart3.style = 12
    chart3.y_axis.title = "USD ($)"
    chart3.x_axis.title = "Month"
    chart3.width = 24
    chart3.height = 10
    c3_data = Reference(ws7, min_col=2, min_row=4, max_col=10, max_row=16)
    c3_cats = Reference(ws7, min_col=1, min_row=5, max_row=16)
    chart3.add_data(c3_data, titles_from_data=True)
    chart3.set_categories(c3_cats)
    ws0.add_chart(chart3, "A37")

    # Remove initial default sheet
    wb.remove(default_ws)

    xlsx_primary = SPREADSHEETS_DIR / "the-ai-freelancer-os-financial-and-pricing-matrix.xlsx"
    xlsx_bundle = HYBRID_BUNDLE_DIR / "the-ai-freelancer-os-financial-and-pricing-matrix.xlsx"
    wb.save(xlsx_primary)
    shutil.copy2(xlsx_primary, xlsx_bundle)

    # Export CSV mirrors
    export_ws_to_csv(ws0, SPREADSHEETS_DIR / "sheet0-executive-visual-dashboard.csv")
    export_ws_to_csv(ws1, SPREADSHEETS_DIR / "sheet1-ehr-leak-audit.csv")
    export_ws_to_csv(ws2, SPREADSHEETS_DIR / "sheet2-bcr-scope-pricing.csv")
    export_ws_to_csv(ws3, SPREADSHEETS_DIR / "sheet3-client-80-20-roster.csv")
    export_ws_to_csv(ws4, SPREADSHEETS_DIR / "sheet4-90day-pipeline-cashflow.csv")
    export_ws_to_csv(ws5, SPREADSHEETS_DIR / "sheet5-client-invoice-generator.csv")
    export_ws_to_csv(ws6, SPREADSHEETS_DIR / "sheet6-daily-3block-time-log.csv")
    export_ws_to_csv(ws7, SPREADSHEETS_DIR / "sheet7-annual-tax-expense-ledger.csv")

    print(f"[Upgrade 4] Built 8-Tab Charted Excel Command Center ({xlsx_primary.stat().st_size:,} bytes) with 4 Embedded Native OpenPyXL Charts + 8 CSVs.")


# ==============================================================================
# UPDATE MARKETING LANDING PAGE (10-MARKETING/index.html) & ROOT README.md
# ==============================================================================
def update_marketing_and_readme_for_phase9():
    index_path = MARKETING_DIR / "index.html"
    if index_path.exists():
        html_txt = index_path.read_text(encoding="utf-8")
        phase9_showcase_banner = """
  <!-- PHASE 9 ULTRA-PREMIUM ECOSYSTEM EXPANSION SHOWCASE -->
  <section class="section" id="ultra-premium-expansion" style="background:#0F172A; color:#F8FAFC; border-top:3px solid #0284C7; border-bottom:3px solid #0D9488;">
    <div class="container">
      <div class="section-header">
        <span class="section-tag" style="background:rgba(56,189,248,0.15); color:#38BDF8; border-color:rgba(56,189,248,0.35);">Phase 9 Ultra-Premium Expansion // Included in Tier 2, Tier 3 &amp; Tier 4</span>
        <h2 class="section-title" style="color:#FFFFFF;">6 Plug-and-Play Agency &amp; Office Suites Included</h2>
        <p class="section-desc" style="color:#CBD5E1;">
          Don't want to read 75,000 words first? Every flagship bundle now includes our <strong>12-Page 60-Second Visual Shortcut Atlas</strong>, <strong>7 Editable Microsoft Word (.docx) Client Contracts &amp; Proposals</strong>, <strong>3 Widescreen PowerPoint (.pptx) Pitch Decks</strong>, the <strong>8-Tab Charted Excel Command Center</strong>, the <strong>Interactive Photo &amp; Cover Customizer Studio</strong>, and <strong>3 Make/Zapier/n8n JSON Automation Blueprints</strong>.
        </p>
      </div>
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(310px, 1fr)); gap:18px;">
        <div style="background:#1E293B; border:1px solid #0284C7; border-radius:12px; padding:20px;">
          <div style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:#38BDF8; margin-bottom:6px;">UPGRADE 01 // SKIMMER EDITION</div>
          <h3 style="font-size:18px; font-weight:800; color:#fff; margin-bottom:8px;">12-Page Visual Shortcut Atlas (PDF + 11 SVGs/PNGs)</h3>
          <p style="font-size:13.5px; color:#CBD5E1;">Master every chapter, formula, and AI prompt trigger in 60 seconds flat. Includes the giant <code>00-ECOSYSTEM-MASTER-MAP-POSTER</code> plus 10 one-page chapter cheat sheets.</p>
        </div>
        <div style="background:#1E293B; border:1px solid #0D9488; border-radius:12px; padding:20px;">
          <div style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:#2DD4BF; margin-bottom:6px;">UPGRADE 02 // EDITABLE WORD (.DOCX) SUITE</div>
          <h3 style="font-size:18px; font-weight:800; color:#fff; margin-bottom:8px;">7 Native Microsoft Word Client &amp; Book Docs</h3>
          <p style="font-size:13.5px; color:#CBD5E1;">Includes the Editable Book Manuscript, 10-Chapter Workbook, 3-Tier B.R.I.E.F. Proposal, Master Service Agreement (MSA/SOW), P.V.P. Change Order Form, Welcome Packet &amp; Handover Certificate.</p>
        </div>
        <div style="background:#1E293B; border:1px solid #F59E0B; border-radius:12px; padding:20px;">
          <div style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:#FBBF24; margin-bottom:6px;">UPGRADE 03 // WIDESCREEN SLIDE DECKS (.PPTX)</div>
          <h3 style="font-size:18px; font-weight:800; color:#fff; margin-bottom:8px;">3 Client-Facing PowerPoint Decks (32 Slides)</h3>
          <p style="font-size:13.5px; color:#CBD5E1;">16:9 widescreen decks with word-for-word presenter notes: 12-Slide Discovery &amp; 3-Tier Proposal Pitch Deck, 10-Slide Client Kickoff Deck, and 10-Slide ROI &amp; 90-Day Retainer Pitch Deck.</p>
        </div>
        <div style="background:#1E293B; border:1px solid #0284C7; border-radius:12px; padding:20px;">
          <div style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:#38BDF8; margin-bottom:6px;">UPGRADE 04 // 8-TAB CHARTED EXCEL</div>
          <h3 style="font-size:18px; font-weight:800; color:#fff; margin-bottom:8px;">Visual Financial, Invoice, Time &amp; Tax Matrix</h3>
          <p style="font-size:13.5px; color:#CBD5E1;">Upgraded to 8 formula-driven tabs with embedded native Excel charts: Executive Visual Dashboard, EHR Audit, B.C.R. Pricing, 80/20 Roster, 90d Cashflow, Client Invoice Generator, 30-Day Time Log &amp; 12-Mo Tax Ledger.</p>
        </div>
        <div style="background:#1E293B; border:1px solid #0D9488; border-radius:12px; padding:20px;">
          <div style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:#2DD4BF; margin-bottom:6px;">UPGRADE 05 // PHOTO &amp; GRAPHIC STUDIO</div>
          <h3 style="font-size:18px; font-weight:800; color:#fff; margin-bottom:8px;">Interactive Design Customizer Web App</h3>
          <p style="font-size:13.5px; color:#CBD5E1;">Open <code>design-customizer-studio.html</code> to customize 6 templates (Book Cover, Gumroad Banner, Proposal Cover, LinkedIn Banner, Case Study Card, Video Thumbnail), upload your own headshot/logo, and export high-res PNG/SVG.</p>
        </div>
        <div style="background:#1E293B; border:1px solid #F59E0B; border-radius:12px; padding:20px;">
          <div style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:#FBBF24; margin-bottom:6px;">UPGRADE 06 // NO-CODE AUTOMATION (.JSON)</div>
          <h3 style="font-size:18px; font-weight:800; color:#fff; margin-bottom:8px;">3 Make.com / Zapier / n8n Workflow Blueprints</h3>
          <p style="font-size:13.5px; color:#CBD5E1;">Importable JSON blueprints connecting your intake form to OpenAI/Claude P.A.C.E. scoring, B.R.I.E.F. proposal drafting, Notion Client Portal provisioning, and Friday CEO Scorecard digests.</p>
        </div>
      </div>
    </div>
  </section>
"""
        if 'id="ultra-premium-expansion"' not in html_txt:
            html_txt = html_txt.replace('<!-- SECTION 7: 5-TIER PRICING LADDER -->', phase9_showcase_banner + '\n  <!-- SECTION 7: 5-TIER PRICING LADDER -->')
            index_path.write_text(html_txt, encoding="utf-8")
            print(f"[Marketing Update] Injected Phase 9 Ultra-Premium Showcase into 10-MARKETING/index.html ({index_path.stat().st_size:,} bytes).")

    # Update Root README.md
    readme_path = BASE_DIR / "README.md"
    readme_txt = readme_path.read_text(encoding="utf-8")
    phase9_readme_section = """
---

## 5. Phase 9 Ultra-Premium Ecosystem Expansion (All 6 Agency & Skimmer Upgrades)

To serve action-takers who prefer visual summaries and editable Microsoft Office / agency deliverables, **Phase 9** expands the ecosystem with six commercial suites:

1. **Upgrade 1 — The 60-Second Visual Shortcut Atlas (`13-VISUAL-CHEAT-SHEETS/` & `09-EXPORTS/PDF/`):**
   * `00-ECOSYSTEM-MASTER-MAP-POSTER.svg` + `.png` (`1600 × 1100 px`) mapping all 5 Lifecycle Gates and tools.
   * `cheat-sheet-ch01.svg`..`cheat-sheet-ch10.svg` + 10 `.png` posters (`1200 × 1600 px`) distilling each chapter into a 60-second 6-panel infographic.
   * `the-ai-freelancer-os-visual-shortcut-atlas.pdf` (`12 full-color pages`).
2. **Upgrade 2 — The 7-Document Editable Microsoft Word (`.docx`) Suite (`12-EDITABLE-OFFICE-SUITE/Word-Docs/`):**
   * `01-Editable-Complete-Book-Manuscript.docx` & `02-Editable-10-Chapter-Action-Workbook.docx`
   * `03-Client-3-Tier-BRIEF-Proposal-Template.docx`, `04-Master-Service-Agreement-and-SOW-Contract.docx`, `05-PVP-Formal-Change-Order-Request-Form.docx`, `06-Client-Welcome-Packet-and-48h-Onboarding-Guide.docx`, and `07-Final-Handover-Certificate-and-90Day-Retainer-Pitch.docx`.
3. **Upgrade 3 — The 3 Editable Widescreen PowerPoint (`.pptx`) Slide Decks (`12-EDITABLE-OFFICE-SUITE/Slide-Decks/`):**
   * `01-Discovery-and-3-Tier-Proposal-Pitch-Deck.pptx` (`12 slides`), `02-Client-Kickoff-and-48h-Alignment-Deck.pptx` (`10 slides`), and `03-ROI-Case-Study-and-90Day-Retainer-Pitch-Deck.pptx` (`10 slides`) with presenter scripts.
4. **Upgrade 4 — The 8-Tab Charted Excel Command Center (`06-NOTION-TEMPLATES/Spreadsheets/`):**
   * Upgraded `the-ai-freelancer-os-financial-and-pricing-matrix.xlsx` to 8 tabs (`00_Executive_Visual_Dashboard` with 3 native OpenPyXL charts, `01_EHR_Leak_Audit` with embedded PieChart, `02_BCR_Scope_Pricing`, `03_Client_80_20_Roster`, `04_90Day_Pipeline_Cashflow`, `05_Client_Invoice_Generator`, `06_Daily_3Block_Time_Log`, and `07_Annual_Tax_Expense_Ledger`).
5. **Upgrade 5 — Interactive Photo & Graphic Design Customizer Studio (`08-COVER-DESIGN/Editable-Design-Kit/`):**
   * `design-customizer-studio.html` (`>= 65 KB`) with 6 visual templates, 5 one-click color themes, local `FileReader` headshot/logo upload, and 1-click `.PNG` / `.SVG` export + `README-DESIGN-KIT.md`.
6. **Upgrade 6 — No-Code Make.com / Zapier / n8n Automation Blueprints (`14-AUTOMATION-BLUEPRINTS/`):**
   * `01-lead-intake-to-ai-brief-and-notion-crm.json`, `02-contract-signed-to-48h-onboarding-gate.json`, `03-friday-ceo-scorecard-and-retainer-alert.json`, and `NO-CODE-AUTOMATION-SETUP-GUIDE.md`.

```bash
# Rebuild and verify the complete Phase 9 Ultra-Premium Ecosystem Expansion
python build_phase9_upgrade.py && python verify_phase9_upgrade.py
```
"""
    if "Phase 9 Ultra-Premium Ecosystem Expansion" not in readme_txt:
        readme_txt = readme_txt.rstrip() + "\n" + phase9_readme_section
        readme_path.write_text(readme_txt, encoding="utf-8")
        print(f"[README Update] Appended Phase 9 inventory to root README.md ({readme_path.stat().st_size:,} bytes).")


# ==============================================================================
# REPACKAGE ALL 5 COMMERCIAL RELEASE .ZIP BUNDLES (TIER 0 .. TIER 4)
# ==============================================================================
def repackage_five_commercial_zips():
    HYBRID_BUNDLE_DIR.mkdir(parents=True, exist_ok=True)

    start_tier0 = """# Welcome to The Freelancer Leak Audit Starter Kit (Tier 0 — Free Edition)

Thank you for downloading **The Freelancer Leak Audit Starter Kit** from **Digital Knowledge Product Studio**.

## Included Files in Your Upgraded Starter Kit
1. **`tier0-free-sample-chapter01-and-audit.pdf`** — Complete Chapter 1 of *The AI Freelancer Operating System* plus the 7-Day Time & Revenue Leak Audit.
2. **`chapter-01-workbook.pdf`** — Standalone Fillable PDF for *Worksheet 1.1: The 7-Day Time & Revenue Leak Audit*.
3. **`freelancer-os-app.html`** — The zero-dependency HTML5 Web Companion App (Module 1 EHR Leak Calculator is 100% open).
4. **`sheet1-ehr-leak-audit.csv`** — Spreadsheet version of the 7-Day Leak Audit for Google Sheets, Excel, or Apple Numbers.
5. **`00-ECOSYSTEM-MASTER-MAP-POSTER.png`** — High-resolution Master 5-Gate Operating System Wall Poster (`1600 x 1100 px`).
6. **`cheat-sheet-ch01.png`** — 60-Second Visual Cheat Sheet Poster for Chapter 1 (`1200 x 1600 px`).
7. **`gumroad-tier0-free-audit-cover.png`** — Official Edition Cover.
"""

    start_tier1 = """# Publisher Upload Checklist — Amazon KDP & Draft2Digital (Tier 1 Retail Pack)

This archive contains the complete, verified master files for publishing **Tier 1 (Essential Edition)** on **Amazon Kindle Direct Publishing (KDP)** and **Draft2Digital (D2D)**.

1. **Amazon KDP Kindle eBook ($9.99 USD):** `the-ai-freelancer-os.epub` + `kdp-ebook-and-d2d-cover.png` (`1600 x 2560 px`).
2. **Amazon KDP 6.0" x 9.0" Print Paperback ($16.99 USD):** `the-ai-freelancer-os-kdp-paperback-6x9.pdf` (`146 pages`) + `kdp-paperback-full-wrap-cover.pdf` (`12.58" x 9.25"`).
3. **Draft2Digital Wide Distribution ($9.99 USD):** `the-ai-freelancer-os.epub` + `kdp-ebook-and-d2d-cover.png`.
4. **Master Listing Copy & Bangladesh 10% Tax Treaty Runbook:** `marketplace-listings-and-bd-launch-runbook.md`.
"""

    start_tier2 = """# Welcome to The Interactive Workbook & Visual Shortcut Edition (Tier 2 — $24 Edition)

Thank you for purchasing **Tier 2: The Interactive Workbook, Tablet Planner & Visual Shortcut Edition** of *The AI Freelancer Operating System*.

## Included Deliverables in Your Upgraded Bundle
1. **`the-ai-freelancer-os-complete-book.pdf`** & **`the-ai-freelancer-os.epub`** — Complete 10-Chapter Operating Manual.
2. **`the-ai-freelancer-os-visual-shortcut-atlas.pdf`** — **NEW:** 12-Page Full-Color 60-Second Visual Shortcut Atlas.
3. **`the-ai-freelancer-os-workbook-us-letter.pdf`** & **`the-ai-freelancer-os-workbook-a4.pdf`** — Fillable PDF Workbooks.
4. **`02-Editable-10-Chapter-Action-Workbook.docx`** — **NEW:** Native Editable Microsoft Word Workbook.
5. **`the-ai-freelancer-os-tablet-planner.pdf`** — 49-Page Landscape Digital Planner for iPad (`GoodNotes / Notability`) and `reMarkable`.
6. **`03-AI-Prompt-and-Script-Vault-62.csv`** — All 50 Tested AI Prompts + 12 Emergency Scripts.
7. **`Mindmaps/`, `Flowcharts/` & `Visual-Cheat-Sheets/`** — All 31 Vector System Diagrams & Cheat Sheet Posters (`.svg`).
"""

    start_tier3 = """# Welcome to The Complete AI Freelancer Operating System (Tier 3 Flagship Bundle — $49)

**Pro Companion Activation Code:** `FREELANCER-OS-PRO-2026`

Thank you for investing in the complete **Ultra-Premium AI Freelancer Operating System Flagship Bundle**.

## Complete Directory of Your 8-Folder Flagship Bundle
1. **`01-BOOK-AND-WORKBOOKS/`** — Complete Book PDF (`168p`), Reflowable `EPUB 3.0`, **12-Page Visual Shortcut Atlas PDF**, `US Letter` & `ISO A4` Fillable Workbooks, and `49-Page Landscape Tablet Planner`.
2. **`02-INTERACTIVE-WEB-APP/`** — Single-file SaaS-Lite Web Companion App (`freelancer-os-app.html`) with all 4 Modules + `README-WEB-APP.md`.
3. **`03-NOTION-OS-KIT/`** — 5-Database Minimalist Notion OS Import Kit (`4 CSV databases + Client Portal + Setup Guide`).
4. **`04-EXCEL-AND-CSV-MATRIX/`** — **Upgraded 8-Tab Charted Excel Command Center** (`the-ai-freelancer-os-financial-and-pricing-matrix.xlsx` with 4 native OpenPyXL charts + 8 CSV mirrors).
5. **`05-VISUAL-SHORTCUT-ATLAS/`** — All 11 Visual Cheat Sheet Posters (`.svg` & `.png`) + `the-ai-freelancer-os-visual-shortcut-atlas.pdf` + 20 Chapter Mindmaps & Flowcharts.
6. **`06-EDITABLE-WORD-AND-PPTX-OFFICE-SUITE/`** — All **7 Editable Microsoft Word (`.docx`) Contracts, Proposals & Manuscripts** + **3 Editable Widescreen PowerPoint (`.pptx`) Pitch Decks (`32 slides`)**.
7. **`07-DESIGN-CUSTOMIZER-STUDIO/`** — Interactive Cover, Thumbnail & Photo Customizer Web App (`design-customizer-studio.html`) + `README-DESIGN-KIT.md`.
8. **`08-AUTOMATION-BLUEPRINTS/`** — 3 Importable Make.com / Zapier / n8n JSON Workflow Blueprints (`01`..`03`) + `NO-CODE-AUTOMATION-SETUP-GUIDE.md`.
"""

    start_tier4 = """# Welcome to The Living OS & Pro Workflow Vault Pass (Tier 4 Membership)

**Pro Companion Activation Code:** `FREELANCER-OS-PRO-2026`  
**Included Monthly Expansion Pack:** `05-LIVING-OS-MONTHLY-DROPS/tier4-monthly-vault-drop-01.md`

Thank you for joining the **Tier 4 Living OS & Pro Workflow Vault Membership**. Your archive contains **100% of the upgraded Tier 3 Flagship Bundle** (including the 12-Page Visual Shortcut Atlas, 7 Editable Word Docs, 3 PowerPoint Slide Decks, 8-Tab Charted Excel Command Center, Design Customizer Studio, and 3 JSON Automation Blueprints) **PLUS** Monthly Expansion Drop #01 (`Prompts V1.1–V1.5` & `Scripts V1–V3`).
"""

    svg_mindmaps = sorted((BASE_DIR / "04-VISUAL-ASSETS" / "Mindmaps").glob("*.svg"))
    svg_flowcharts = sorted((BASE_DIR / "04-VISUAL-ASSETS" / "Flowcharts").glob("*.svg"))
    cheat_svgs = sorted(CHEAT_DIR.glob("*.svg"))
    cheat_pngs = sorted(CHEAT_DIR.glob("*.png"))
    word_docs = sorted((BASE_DIR / "12-EDITABLE-OFFICE-SUITE" / "Word-Docs").glob("*.docx"))
    pptx_decks = sorted((BASE_DIR / "12-EDITABLE-OFFICE-SUITE" / "Slide-Decks").glob("*.pptx"))
    auto_jsons = sorted((BASE_DIR / "14-AUTOMATION-BLUEPRINTS").glob("*.json"))

    # 1. Tier 0 ZIP
    t0_zip = HYBRID_BUNDLE_DIR / "Tier0-Free-Leak-Audit-Starter-Kit.zip"
    with zipfile.ZipFile(t0_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("START-HERE-TIER0.md", start_tier0)
        zf.write(BASE_DIR / "09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf", "tier0-free-sample-chapter01-and-audit.pdf")
        zf.write(BASE_DIR / "05-WORKBOOKS/chapter-01-workbook.pdf", "chapter-01-workbook.pdf")
        zf.write(BASE_DIR / "07-INTERACTIVE-TOOLS/freelancer-os-app.html", "freelancer-os-app.html")
        zf.write(SPREADSHEETS_DIR / "sheet1-ehr-leak-audit.csv", "sheet1-ehr-leak-audit.csv")
        zf.write(CHEAT_DIR / "00-ECOSYSTEM-MASTER-MAP-POSTER.png", "00-ECOSYSTEM-MASTER-MAP-POSTER.png")
        zf.write(CHEAT_DIR / "cheat-sheet-ch01.png", "cheat-sheet-ch01.png")
        zf.write(BASE_DIR / "08-COVER-DESIGN/gumroad-tier0-free-audit-cover.png", "gumroad-tier0-free-audit-cover.png")

    # 2. Tier 1 ZIP
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

    # 3. Tier 2 ZIP
    t2_zip = HYBRID_BUNDLE_DIR / "Tier2-Interactive-Workbook-and-Planner-Edition.zip"
    with zipfile.ZipFile(t2_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("START-HERE-TIER2.md", start_tier2)
        zf.write(BASE_DIR / "09-EXPORTS/PDF/the-ai-freelancer-os-complete-book.pdf", "the-ai-freelancer-os-complete-book.pdf")
        zf.write(BASE_DIR / "09-EXPORTS/EPUB/the-ai-freelancer-os.epub", "the-ai-freelancer-os.epub")
        zf.write(CHEAT_DIR / "the-ai-freelancer-os-visual-shortcut-atlas.pdf", "the-ai-freelancer-os-visual-shortcut-atlas.pdf")
        zf.write(BASE_DIR / "09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-us-letter.pdf", "the-ai-freelancer-os-workbook-us-letter.pdf")
        zf.write(BASE_DIR / "09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-a4.pdf", "the-ai-freelancer-os-workbook-a4.pdf")
        zf.write(BASE_DIR / "12-EDITABLE-OFFICE-SUITE/Word-Docs/02-Editable-10-Chapter-Action-Workbook.docx", "02-Editable-10-Chapter-Action-Workbook.docx")
        zf.write(BASE_DIR / "09-EXPORTS/PDF/the-ai-freelancer-os-tablet-planner.pdf", "the-ai-freelancer-os-tablet-planner.pdf")
        zf.write(BASE_DIR / "06-NOTION-TEMPLATES/03-AI-Prompt-and-Script-Vault-62.csv", "03-AI-Prompt-and-Script-Vault-62.csv")
        for svg_p in svg_mindmaps:
            zf.write(svg_p, f"Mindmaps/{svg_p.name}")
        for svg_p in svg_flowcharts:
            zf.write(svg_p, f"Flowcharts/{svg_p.name}")
        for cs_p in cheat_svgs:
            zf.write(cs_p, f"Visual-Cheat-Sheets/{cs_p.name}")

    def populate_tier3_flagship_files(zf: zipfile.ZipFile):
        # 01 Book, Workbooks & Visual Shortcut Atlas PDF
        zf.write(BASE_DIR / "09-EXPORTS/PDF/the-ai-freelancer-os-complete-book.pdf", "01-BOOK-AND-WORKBOOKS/the-ai-freelancer-os-complete-book.pdf")
        zf.write(BASE_DIR / "09-EXPORTS/EPUB/the-ai-freelancer-os.epub", "01-BOOK-AND-WORKBOOKS/the-ai-freelancer-os.epub")
        zf.write(CHEAT_DIR / "the-ai-freelancer-os-visual-shortcut-atlas.pdf", "01-BOOK-AND-WORKBOOKS/the-ai-freelancer-os-visual-shortcut-atlas.pdf")
        zf.write(BASE_DIR / "09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-us-letter.pdf", "01-BOOK-AND-WORKBOOKS/the-ai-freelancer-os-workbook-us-letter.pdf")
        zf.write(BASE_DIR / "09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-a4.pdf", "01-BOOK-AND-WORKBOOKS/the-ai-freelancer-os-workbook-a4.pdf")
        zf.write(BASE_DIR / "09-EXPORTS/PDF/the-ai-freelancer-os-tablet-planner.pdf", "01-BOOK-AND-WORKBOOKS/the-ai-freelancer-os-tablet-planner.pdf")

        # 02 Interactive Web App
        zf.write(BASE_DIR / "07-INTERACTIVE-TOOLS/freelancer-os-app.html", "02-INTERACTIVE-WEB-APP/freelancer-os-app.html")
        zf.write(BASE_DIR / "07-INTERACTIVE-TOOLS/README-WEB-APP.md", "02-INTERACTIVE-WEB-APP/README-WEB-APP.md")

        # 03 Notion OS Kit
        for nf in [
            "01-Leads-CRM-Pipeline.csv",
            "02-Active-Projects-and-Gates.csv",
            "03-AI-Prompt-and-Script-Vault-62.csv",
            "04-Weekly-CEO-Scorecard-Log.csv",
            "05-Client-Portal-and-Handover-Hub.md",
            "NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md",
        ]:
            zf.write(BASE_DIR / "06-NOTION-TEMPLATES" / nf, f"03-NOTION-OS-KIT/{nf}")

        # 04 Upgraded 8-Tab Excel Command Center & CSV Mirrors
        for sf in sorted(SPREADSHEETS_DIR.glob("*")):
            if sf.is_file():
                zf.write(sf, f"04-EXCEL-AND-CSV-MATRIX/{sf.name}")

        # 05 Visual Shortcut Atlas + Mindmaps + Flowcharts
        zf.write(CHEAT_DIR / "the-ai-freelancer-os-visual-shortcut-atlas.pdf", "05-VISUAL-SHORTCUT-ATLAS/the-ai-freelancer-os-visual-shortcut-atlas.pdf")
        for cs_p in cheat_svgs:
            zf.write(cs_p, f"05-VISUAL-SHORTCUT-ATLAS/{cs_p.name}")
        for cp_p in cheat_pngs:
            zf.write(cp_p, f"05-VISUAL-SHORTCUT-ATLAS/{cp_p.name}")
        for svg_p in svg_mindmaps:
            zf.write(svg_p, f"04-VISUAL-DIAGRAMS/Mindmaps/{svg_p.name}")
        for svg_p in svg_flowcharts:
            zf.write(svg_p, f"04-VISUAL-DIAGRAMS/Flowcharts/{svg_p.name}")

        # 06 Editable Word (.docx) & PowerPoint (.pptx) Office Suite
        for wd in word_docs:
            zf.write(wd, f"06-EDITABLE-WORD-AND-PPTX-OFFICE-SUITE/Word-Docs/{wd.name}")
        for pd in pptx_decks:
            zf.write(pd, f"06-EDITABLE-WORD-AND-PPTX-OFFICE-SUITE/Slide-Decks/{pd.name}")

        # 07 Design Customizer Studio
        zf.write(BASE_DIR / "08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html", "07-DESIGN-CUSTOMIZER-STUDIO/design-customizer-studio.html")
        zf.write(BASE_DIR / "08-COVER-DESIGN/Editable-Design-Kit/README-DESIGN-KIT.md", "07-DESIGN-CUSTOMIZER-STUDIO/README-DESIGN-KIT.md")

        # 08 Automation Blueprints
        for aj in auto_jsons:
            zf.write(aj, f"08-AUTOMATION-BLUEPRINTS/{aj.name}")
        zf.write(BASE_DIR / "14-AUTOMATION-BLUEPRINTS/NO-CODE-AUTOMATION-SETUP-GUIDE.md", "08-AUTOMATION-BLUEPRINTS/NO-CODE-AUTOMATION-SETUP-GUIDE.md")

    # 4. Tier 3 ZIP
    t3_zip = HYBRID_BUNDLE_DIR / "Tier3-Complete-AI-Freelancer-OS-Flagship-Bundle.zip"
    with zipfile.ZipFile(t3_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("START-HERE-TIER3-COMPLETE-OS.md", start_tier3)
        populate_tier3_flagship_files(zf)

    # 5. Tier 4 ZIP
    t4_zip = HYBRID_BUNDLE_DIR / "Tier4-Living-OS-Pro-Vault-Membership-Pack.zip"
    with zipfile.ZipFile(t4_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("START-HERE-TIER4-MEMBERSHIP.md", start_tier4)
        populate_tier3_flagship_files(zf)
        zf.write(MARKETING_DIR / "tier4-monthly-vault-drop-01.md", "05-LIVING-OS-MONTHLY-DROPS/tier4-monthly-vault-drop-01.md")

    for zp in (t0_zip, t1_zip, t2_zip, t3_zip, t4_zip):
        with zipfile.ZipFile(zp, "r") as zcheck:
            corrupt = zcheck.testzip()
            if corrupt is not None:
                raise RuntimeError(f"Corrupt entry {corrupt} in {zp}")
            print(f"[Repackaged ZIP] {zp.name}: {len(zcheck.namelist())} files ({zp.stat().st_size:,} bytes)")


def main() -> int:
    print("=" * 82)
    print("PHASE 9 MASTER BUILDER — ULTRA-PREMIUM ECOSYSTEM EXPANSION (6 SUITES + 5 ZIPS)")
    print("=" * 82)
    build_visual_shortcut_atlas()
    build_word_docx_suite()
    build_powerpoint_decks()
    build_8tab_excel_command_center()
    build_design_customizer_studio()
    build_automation_blueprints()
    update_marketing_and_readme_for_phase9()
    repackage_five_commercial_zips()
    print("=" * 82)
    print("PHASE 9 BUILD COMPLETE — ALL 6 ULTRA-PREMIUM UPGRADES & 5 RELEASE ZIPS READY")
    print("=" * 82)
    return 0


if __name__ == "__main__":
    sys.exit(main())
