# The AI Freelancer Operating System — Interactive Web Companion App (`freelancer-os-app.html`)

**Edition:** 2026 Enterprise Studio Build (`v1.0.0`)  
**Architecture:** Zero-Dependency Single-File SaaS-Lite Application (HTML5 + CSS3 + Vanilla ES6 JavaScript)  
**Primary App Path:** `07-INTERACTIVE-TOOLS/freelancer-os-app.html`  
**Hybrid Bundle Mirror:** `09-EXPORTS/HYBRID-BUNDLE/freelancer-os-app.html`

---

## 1. Architectural Overview & Zero-Dependency Design

The **Interactive Web Companion Application** (`freelancer-os-app.html`) is Pillar 3 of **The AI Freelancer Operating System** product ecosystem. Engineered as a self-contained, single-file SaaS-Lite software suite, it requires **zero external CDNs, zero node_modules, zero build steps for end users, and zero server-side databases**.

Every stylesheet, vector icon, interactive financial algorithm, `localStorage` state controller, and all **62 practitioner templates** (**50 Tested AI Workflow Prompts** extracted deterministically from Chapters 1–10 and **12 Emergency Client Scripts** extracted from Appendix B) are compiled directly into one portable `.html` file via `build_webapp.py`.

### Supported Execution Environments
1. **100% Offline Local Execution (`file://` Protocol):**
   - Double-click `freelancer-os-app.html` on Windows, macOS, Linux, iOS/iPadOS, or Android to open the application directly in Chrome, Edge, Safari, Brave, or Firefox.
   - All calculations, variable interpolations, clipboard operations, and browser `localStorage` persistence work offline without an internet connection.
2. **Static Web Hosting & Lead-Magnet Deployment (`https://` Protocol):**
   - Host `freelancer-os-app.html` as an `index.html` or standalone route on **GitHub Pages, Cloudflare Pages, Netlify, Vercel, or Amazon S3**.
   - Use URL query parameters (`?mode=free` or `?mode=pro`) to serve either the gated Tier-0 Lead Magnet experience or the full Pro/OS Edition experience from a single deployment file.

---

## 2. Global Controls: Multi-Currency Engine & Edition Mode Switcher

Located in the sticky top application header, four global controls govern your workspace session:

1. **Multi-Currency Selector (`#currency-select`):**
   - Dynamically switches all financial inputs, rate tables, targets, and executive outputs between **USD (`$`)**, **GBP (`£`)**, **CAD (`CA$`)**, and **AUD (`A$`)** to support independent service providers across the United States, United Kingdom, Canada, and Australia.
2. **Edition Mode Switcher (`#edition-mode-toggle`):**
   - Toggles between **Pro / OS Edition (Full Access)** and **Free Tier (Lead Magnet Mode)**.
   - **URL Query Parameter Override:**
     - Append `?mode=free` to load the app in **Tier-0 Lead Magnet Mode**: Module 1 (*EHR & Leak Audit*) is 100% open, Module 3 (*Prompt & Script Vault*) provides full interactive access to the 5 Chapter 1 diagnostic prompts (`Prompts 1.1–1.5`) while displaying a clean Pro Activation banner on Chapters 2–10 (`Prompts 2.1–10.5`) and Emergency Scripts (`Scripts 1–12`), and Modules 2 and 4 provide a one-click activation gate.
     - Append `?mode=pro` or enter the Companion Access Code **`FREELANCER-OS-PRO-2026`** in the header modal to activate all 4 modules, all 50 AI workflows, and all 12 emergency scripts immediately.
3. **Export / Import JSON Workspace Backup:**
   - **Export JSON:** Downloads a timestamped `freelancer-os-workspace-YYYY-MM-DD.json` file containing your currency preferences, EHR audit sliders, custom BCR deliverables, Prompt Vault variable dictionary, and 12-week CEO Scorecard history.
   - **Import JSON:** Restores a previously exported `.json` workspace snapshot with instant validation and state hydration.
4. **Print / Save PDF Report (`window.print()`):**
   - Uses a dedicated `@media print` stylesheet that hides navigation chrome and formats the active module into a clean, client-ready or executive-ready **US Letter / A4 PDF report**.

---

## 3. Walkthrough of the 4 Operational Modules

### Module 1: Effective Hourly Rate (EHR) & Revenue Leak Audit (`#tab-ehr-audit`)
Implements the diagnostic equations from **Chapter 1** and **Worksheet 1.1**:
- **Core Inputs:** Monthly Gross Revenue ($R_{\text{gross}}$), Monthly Software & Subcontractor Overhead ($C_{\text{overhead}}$), Direct Client Delivery Hours ($H_{\text{billable}}$), Unbilled Admin/Sales/Revision Hours ($H_{\text{admin}}$), Target Billable Rate ($R_{\text{target}}$), and Weekly AI Automation Recovery Percentage (default `55%`).
- **6-Category Weekly Unbilled Shadow Labor Sliders:** Granular sliders for *Lead Triage & Proposal Drafting*, *Client Onboarding & Asset Chasing*, *Status Updates & Meeting Recaps*, *Async Feedback & Revision Wrangling*, *SOP Documentation & File Hygiene*, and *Invoicing & Payment Follow-Ups*.
- **Real-Time Telemetry:** Computes True Net Income, Total Monthly Working Hours, **True Effective Hourly Rate ($\text{EHR}$)**, **Hourly Rate Erosion ($\Delta R$)**, **Shadow Labor Overhead Ratio ($\text{SLOR}$)**, **Annualized Unbilled Revenue Leak**, and **90-Day AI OS Recovery Projection**, accompanied by an interactive SVG stacked visual breakdown and dynamic diagnostic prescription banner.

### Module 2: Base Cost Rate (BCR) & 3-Tier Proposal Pricing Matrix (`#tab-bcr-pricing`)
Implements the pricing and scope-engineering frameworks from **Chapters 2 and 8**:
- **BCR Floor Calculator:** Computes your non-negotiable hourly cost floor from Target Annual Net Take-Home Pay, Annual Business Overhead, Self-Employment Tax Reserve (`%`), Realistic Billable Weeks per Year, and Weekly Billable Capacity Ceiling:
  $$\text{BCR} = \frac{\text{Target Net Income} + \text{Annual Overhead}}{1 - \text{Tax Rate}} \div (\text{Billable Weeks} \times \text{Weekly Billable Hours})$$
- **Interactive Scope Builder & 3-Tier Anchor Matrix:** Add custom deliverables, assign estimated delivery hours, complexity risk buffers (`1.0x` to `1.5x`), and AI acceleration factors (`15%` to `35%`). The engine automatically calculates **Tier 1 (Essential Baseline — `1.0x`)**, **Tier 2 (Accelerated Growth — `1.45x` Anchor Recommended)**, and **Tier 3 (Executive Turnkey — `2.15x`)**, complete with effective hourly yield per tier, recommended payment milestones (`50/50` or `40/30/30`), and a **One-Click Copy Markdown Proposal Table** button.

### Module 3: Interactive 50-Prompt & 12-Script Execution Vault (`#tab-prompt-vault`)
Houses the complete operational library of **50 Tested AI Workflows (`Prompts 1.1–10.5`)** and **12 Emergency Client Scripts (`Scripts 1–12`)**:
- **Search & Multi-Faceted Filtering:** Filter instantaneously by keyword, Chapter (`Chapter 1` through `Chapter 10`), Emergency Scripts (`Scripts 1–12`), or Free vs. Pro tier.
- **Dynamic `[VARIABLE]` Auto-Detection & Live Interpolation:** Selecting any prompt or script automatically scans its template for bracketed placeholders (such as `[INSERT NICHE]`, `[CLIENT NAME]`, `[PROJECT FEE]`) and generates dedicated input fields. Typing into any field highlights and replaces the variable in the live preview pane in real time.
- **One-Click Execution Controls:** Copy the interpolated prompt to your clipboard for immediate execution in Claude, ChatGPT, or Gemini, copy the raw template, or inspect the built-in **Verification & QA Rule** and **Sample Practitioner Output** before sending any client-facing message.

### Module 4: Weekly Friday CEO Scorecard & Retainer Capacity Tracker (`#tab-ceo-scorecard`)
Implements the executive review system from **Chapter 10**:
- **30-Minute Friday CEO Ritual Checklist:** Interactive 6-step checklist with live completion progress bar covering Invoice Hygiene, Pipeline Triage, Scope Boundary Audit, Retainer Burn-Rate Review, Automation Maintenance, and Next-Week Deep-Work Calendar Blocking.
- **Retainer & Project Capacity Utilization Gauge:** Visualizes weekly committed client hours against your maximum sustainable billable ceiling (`25`–`35 hrs/wk`), triggering color-coded utilization alerts (`Optimal <80%`, `Watch 80–90%`, `Over-Capacity >90%`).
- **12-Week Historical Trend Ledger & CSV Export:** Log weekly snapshots of Gross Revenue, Billable Hours, Admin Hours, Computed EHR, Active Retainers, and CEO Notes. Export your entire historical log to a spreadsheet-ready `.csv` file with one click.

---

## 4. Rebuilding the Application from Single-Source Manuscript Files

Whenever you update a prompt in `03-MANUSCRIPT/Chapters/chapter-01.md`..`chapter-10.md` or an emergency script in `03-MANUSCRIPT/Back-Matter/back-matter.md`, recompile and verify the web application by running:

```bash
python build_webapp.py
python verify_phase6.py
```
