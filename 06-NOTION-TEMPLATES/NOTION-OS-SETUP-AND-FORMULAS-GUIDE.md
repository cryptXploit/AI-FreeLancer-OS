# The 5-Database Minimalist Notion Freelancer OS — Setup, Relational Schema & Formula 2.0 Implementation Guide

**Edition:** 2026 Commercial Studio Build (`v1.0.0`)  
**Target Setup Time:** 12 to 15 Minutes  
**Anti-Bloat Guarantee:** Zero decorative widgets, zero 19-database dependency chains, and zero manual double-entry. Every database in this kit maps directly to the **5-Stage Client Lifecycle** and **20-Minute Friday CEO Ritual** taught in *The AI Freelancer Operating System*.

---

## 1. Architectural Philosophy: Why a 5-Component Notion OS Beats 20-Tab Templates

Most commercial Notion templates fail independent service providers within 14 days because they suffer from **structural maintenance bloat**. When a template requires you to log every 15-minute sub-task across five linked databases just to send an invoice, the workspace itself becomes a source of Bucket D administrative drag.

The **Minimalist Notion Freelancer OS** enforces a strict **5-Component Architecture**:
1. **Database 01 — `01-Leads-CRM-Pipeline.csv` (Stage 1 & Stage 2 Gate):** Captures inbound prospects, computes the 20-point **P.A.C.E. Fit Score**, flags toxic scope/budget signals early, and tracks weighted pipeline revenue across 7 deterministic stages.
2. **Database 02 — `02-Active-Projects-and-Gates.csv` (Stage 3, Stage 4 & Stage 5 Gate):** Tracks active client sprints and monthly retainers, enforces the **48-Hour Pre-Flight Asset Gate**, compares quoted B.C.R. hours against actual logged hours, calculates live **Project Effective Hourly Rate ($\text{EHR}$)**, and flags **80/20 Client Actions** (*Retain & Expand*, *Re-Price +20%*, or *Prune / Replace*).
3. **Database 03 — `03-AI-Prompt-and-Script-Vault-62.csv` (All 50 AI Workflows + 12 Emergency Scripts):** Gives you an instant, searchable in-workspace library of all 50 tested AI workflow prompts (`Prompts 1.1–10.5`) and all 12 word-for-word client boundary scripts (`Scripts 1–12`).
4. **Database 04 — `04-Weekly-CEO-Scorecard-Log.csv` (Chapter 10 Friday Executive Ritual):** Logs your 20-minute Friday review across a 12-week rolling quarter, tracking weekly revenue, Buckets A/B/C/D time allocation, Billable Utilization %, True Weekly EHR, and the single permanent system upgrade installed each week.
5. **Component 05 — `05-Client-Portal-and-Handover-Hub.md` (Reusable Client-Facing Command Center):** A single-page Markdown template imported as the default **Database Template** inside `02-Active-Projects-and-Gates` so every new client project automatically spawns a complete, shareable portal containing the 48-Hour Asset Checklist, Async SLA rules, Milestone Tracker, Revision Ledger, and Final Handover Vault.

---

## 2. Step-by-Step 15-Minute Notion Import & Workspace Assembly

Follow these five sequential steps to deploy the entire operating system inside a free or paid Notion account:

### Step 1: Create Your Master Command Page
1. Open Notion and create a new top-level page titled **`⚡ AI Freelancer OS — Command Center`**.
2. Set the page width to **Full Width** (click the **`•••`** menu in the top-right corner and toggle **Full width** on).
3. Create two side-by-side columns at the top of the page:
   - **Left Column (`30%` width):** Quick navigation callout box with links to your **Daily 3-Block Priority Plan**, **Interactive Web Companion App (`freelancer-os-app.html`)**, and **Friday CEO Checklist**.
   - **Right Column (`70%` width):** Linked views of your active pipeline and active client sprints.

### Step 2: Import the 4 Core CSV Databases
1. In your Notion sidebar or inside the Command Center page, click **`•••` (Top Right) → Import → CSV** (or **Markdown & CSV**).
2. Select and import these four files one by one:
   - `01-Leads-CRM-Pipeline.csv`
   - `02-Active-Projects-and-Gates.csv`
   - `03-AI-Prompt-and-Script-Vault-62.csv`
   - `04-Weekly-CEO-Scorecard-Log.csv`
3. Once imported, convert each property column to its proper Notion property type using the **Property Configuration Matrix** in Section 3 below.

### Step 3: Install `05-Client-Portal-and-Handover-Hub.md` as an Automated Project Template
1. Open your newly imported **`02-Active-Projects-and-Gates`** database.
2. Click the dropdown arrow next to the blue **`New`** button in the top-right corner of the database and click **`+ New template`**.
3. Title the template **`[CLIENT PORTAL] Standard 5-Gate Sprint & Handover Hub`**.
4. Inside the template body, click **`•••` → Import → Markdown & CSV** and select **`05-Client-Portal-and-Handover-Hub.md`** (or paste its Markdown contents directly into the template canvas).
5. Click the **`•••`** icon next to your new template in the **`New`** dropdown menu and select **`Set as default` → `For all views`**. Now, every time you create a new client project, Notion automatically populates the entire 6-section Client Portal inside that project record.

---

## 3. Database Property Configuration & Relational Schema Matrix

After importing the four CSV files, verify that the following columns are set to the right Notion property types and configure the **3 Core Two-Way Relations**:

### 3.1 Property Types by Database

| Database Name | Column Name | Target Notion Property Type | Number / Select Format |
| :--- | :--- | :--- | :--- |
| **`01-Leads-CRM-Pipeline`** | `Pipeline Stage` | `Status` or `Select` | `01 Discovery Intake` .. `07 Disqualified` |
| **`01-Leads-CRM-Pipeline`** | `Fit Score (0-20)` | `Number` | `Number` (`0` to `20`) |
| **`01-Leads-CRM-Pipeline`** | `Quoted Package Price ($)` | `Number` | `U.S. Dollar` (`$#,##0`) |
| **`01-Leads-CRM-Pipeline`** | `Win Probability (%)` | `Number` | `Percent` (`0%` to `100%`) |
| **`02-Active-Projects-and-Gates`** | `Current Lifecycle Gate` | `Select` | `Gate 1` through `Gate 5` |
| **`02-Active-Projects-and-Gates`** | `Contract Value ($)` | `Number` | `U.S. Dollar` (`$#,##0`) |
| **`02-Active-Projects-and-Gates`** | `Quoted B.C.R. Hours` | `Number` | `Number with commas` (`0.0`) |
| **`02-Active-Projects-and-Gates`** | `Actual Hours Logged` | `Number` | `Number with commas` (`0.0`) |
| **`02-Active-Projects-and-Gates`** | `Target EHR ($/hr)` | `Number` | `U.S. Dollar` (`$#,##0.00`) |
| **`02-Active-Projects-and-Gates`** | `Captured Change Orders ($)` | `Number` | `U.S. Dollar` (`$#,##0`) |
| **`02-Active-Projects-and-Gates`** | `Friction Score (1-5)` | `Number` | `Number` (`1` to `5`) |
| **`03-AI-Prompt-and-Script-Vault-62`** | `Asset Type` | `Select` | `AI Workflow Prompt` / `Emergency Script` |
| **`03-AI-Prompt-and-Script-Vault-62`** | `Lifecycle Stage / Category` | `Select` | `Stage 1` .. `Stage 5` / `Scripts` |
| **`04-Weekly-CEO-Scorecard-Log`** | `Gross Revenue ($)` | `Number` | `U.S. Dollar` (`$#,##0`) |
| **`04-Weekly-CEO-Scorecard-Log`** | `Bucket A..D Hours` | `Number` | `Number` (`0.0`) |

### 3.2 Connecting the 3 Two-Way Relational Links
1. **Relation 1 (`Leads CRM` $\leftrightarrow$ `Active Projects`):**
   - In `01-Leads-CRM-Pipeline`, add a **Relation** property named `Converted Project` linked to `02-Active-Projects-and-Gates` (toggle **Show on Active Projects** as `Source Lead`). When a prospect moves to `05 Closed Won`, link their lead record to their active project in one click.
2. **Relation 2 (`Active Projects` $\leftrightarrow$ `AI Prompt & Script Vault`):**
   - In `02-Active-Projects-and-Gates`, add a **Relation** property named `Active Gate Prompts` linked to `03-AI-Prompt-and-Script-Vault-62`. Link the exact onboarding (`Prompt 5.1`), execution (`Prompt 6.1`), or boundary (`Script 7`) templates you are using on that account.
3. **Relation 3 (`Active Projects` $\leftrightarrow$ `Weekly CEO Scorecard Log`):**
   - In `04-Weekly-CEO-Scorecard-Log`, add a **Relation** property named `Audited Projects` linked to `02-Active-Projects-and-Gates` so your Friday review can pull rollups of total active retainer fees and hours.

---

## 4. Copy-Paste Notion Formula 2.0 Code Library

Note that CSV imports bring calculated columns in as static values so you can immediately see the sample data. To make those columns calculate dynamically on every new row you add in Notion, change the column type from `Number` or `Text` to **`Formula`** and paste the exact **Notion Formula 2.0** expressions below.

### Formula 1: Weighted Pipeline Value (`01-Leads-CRM-Pipeline`)
Calculates the probability-adjusted value of each prospect in your sales pipeline. *(Note: If your `Win Probability (%)` column is formatted as a whole number `0–100` from the CSV import, divide by `100`; if formatted as a Notion Percent `0.00–1.00`, omit `/ 100`.)*

```javascript
round(prop("Quoted Package Price ($)") * (prop("Win Probability (%)") / 100))
```

### Formula 2: Automated P.A.C.E. Lead Triage Routing Badge (`01-Leads-CRM-Pipeline`)
Evaluates the prospect's `Fit Score (0-20)` and outputs an immediate commercial routing instruction matching Chapter 3 (`Worksheet 3.1`):

```javascript
if(
  prop("Fit Score (0-20)") >= 16,
  "🟢 FAST-TRACK: Send 3-Tier B.R.I.E.F. Proposal (Prompt 3.3)",
  if(
    prop("Fit Score (0-20)") >= 11,
    "🟡 CONDITIONAL: Pitch Paid Diagnostic Blueprint Only (Script 2)",
    "🔴 DISQUALIFY: Send Polite Referral Decline (Script 1)"
  )
)
```

### Formula 3: Live Project Effective Hourly Rate — EHR (`02-Active-Projects-and-Gates`)
Computes your real-time realized hourly yield on any fixed-price project or monthly retainer, including revenue recovered through paid **P.V.P. Change Orders**:

```javascript
if(
  prop("Actual Hours Logged") > 0,
  round(((prop("Contract Value ($)") + prop("Captured Change Orders ($)")) / prop("Actual Hours Logged")) * 100) / 100,
  round((prop("Contract Value ($)") / max(prop("Quoted B.C.R. Hours"), 1)) * 100) / 100
)
```

### Formula 4: Automated 80/20 Client Action Flag (`02-Active-Projects-and-Gates`)
Implements the **Chapter 10 Client Profitability & Friction Matrix**, automatically classifying every active client into a concrete executive action based on their realized EHR vs. Target EHR and their Friction Score (`1–5`):

```javascript
lets(
  realEhr,
  if(prop("Actual Hours Logged") > 0, (prop("Contract Value ($)") + prop("Captured Change Orders ($)")) / prop("Actual Hours Logged"), prop("Target EHR ($/hr)")),
  targetEhr,
  prop("Target EHR ($/hr)"),
  friction,
  prop("Friction Score (1-5)"),
  if(
    realEhr >= targetEhr and friction <= 2,
    "🟢 RETAIN & EXPAND (Pitch Retainer / Upsell)",
    if(
      realEhr < (targetEhr * 0.80) and friction >= 4,
      "🔴 PRUNE / REPLACE NEXT QUARTER (Whale Trap)",
      "🟡 RE-PRICE +20% AT RENEWAL (Enforce Script 7 & 12)"
    )
  )
)
```

### Formula 5: Weekly Total Hours, Billable Utilization % & True Weekly EHR (`04-Weekly-CEO-Scorecard-Log`)
Paste these three formulas into your `04-Weekly-CEO-Scorecard-Log` database to automate the **20-Minute Friday CEO Ritual**:

**5A — `Total Real Hours` Formula:**
```javascript
prop("Bucket A Billable Craft Hours") + prop("Bucket B Client Friction Hours") + prop("Bucket C Unpaid Admin Hours") + prop("Bucket D Context-Switching Hours")
```

**5B — `Billable Utilization (%)` Formula:**
```javascript
lets(
  totalHrs,
  prop("Bucket A Billable Craft Hours") + prop("Bucket B Client Friction Hours") + prop("Bucket C Unpaid Admin Hours") + prop("Bucket D Context-Switching Hours"),
  if(totalHrs > 0, round((prop("Bucket A Billable Craft Hours") / totalHrs) * 1000) / 10, 0)
)
```

**5C — `True Weekly EHR ($/hr)` & Health Indicator Formula:**
```javascript
lets(
  totalHrs,
  prop("Bucket A Billable Craft Hours") + prop("Bucket B Client Friction Hours") + prop("Bucket C Unpaid Admin Hours") + prop("Bucket D Context-Switching Hours"),
  ehr,
  if(totalHrs > 0, round((prop("Gross Revenue ($)") / totalHrs) * 100) / 100, 0),
  utilPct,
  if(totalHrs > 0, (prop("Bucket A Billable Craft Hours") / totalHrs) * 100, 0),
  "$" + format(ehr) + "/hr (" + if(utilPct >= 65, "🟢 Healthy >=65% Craft", "🟠 Leak Detected <65% Craft") + ")"
)
```

### Formula 6: The 85% Capacity Rate-Raise Trigger Alert (`04-Weekly-CEO-Scorecard-Log`)
Add a formula column titled `Rate-Raise Trigger Status` in your Weekly CEO Scorecard (assuming a `30.0 hr/wk` sustainable billable craft ceiling; adjust `30` to match your personal ceiling):

```javascript
lets(
  weeklyCeiling,
  30,
  capRatio,
  (prop("Bucket A Billable Craft Hours") / weeklyCeiling) * 100,
  if(
    capRatio >= 85,
    "⚡ TRIGGER ACTIVE (" + format(round(capRatio)) + "% Booked): Raise Next 3 Proposals by +15% to +25% & Send Script 12",
    "✅ CAPACITY OPEN (" + format(round(capRatio)) + "% Booked): Focus on Stage 1-2 Pipeline Conversion"
  )
)
```

---

## 5. Recommended Saved Database Views for Daily & Weekly Execution

To keep your cognitive load near zero during the workweek, configure these **4 filtered views** on your Master Command Page:
1. **`[Pipeline] Action Required Today` (`01-Leads-CRM-Pipeline`):** Filtered where `Pipeline Stage` is `01 Discovery Intake`, `02 B.R.I.E.F. Qualified`, or `03 3-Tier Proposal Sent`, sorted by `Weighted Pipeline Value ($)` descending.
2. **`[Delivery] Active Sprint Board` (`02-Active-Projects-and-Gates`):** Kanban board grouped by `Current Lifecycle Gate` (`Gate 1` through `Gate 5`) showing `48h Asset Gate Status`, `Live Project EHR ($/hr)`, and `Target Delivery Date`.
3. **`[Friday CEO] 80/20 Profitability Matrix` (`02-Active-Projects-and-Gates`):** Table view sorted by `Live Project EHR ($/hr)` ascending so your lowest-margin or highest-friction account always appears at the top during your Friday review.
4. **`[Prompt Vault] Quick Stage Lookup` (`03-AI-Prompt-and-Script-Vault-62`):** Gallery or Table view grouped by `Lifecycle Stage / Category` so you can copy any of the 50 AI prompts or 12 emergency boundary scripts in two clicks.
