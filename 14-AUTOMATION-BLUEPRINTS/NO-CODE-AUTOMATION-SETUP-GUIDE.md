# No-Code AI Automation Blueprints — Setup, API Wiring & Notion Integration Guide (`NO-CODE-AUTOMATION-SETUP-GUIDE.md`)

**Blueprint Directory:** `14-AUTOMATION-BLUEPRINTS/`  
**Compatible Automation Platforms:** Make.com (Integromat), n8n (Self-Hosted or Cloud), and Zapier  
**Compatible AI Models:** Anthropic Claude (`claude-3-7-sonnet` / `claude-3-5-sonnet`), OpenAI (`gpt-4o`), or Google Gemini (`gemini-2.5-pro`)  
**Target Setup Time:** 15 to 20 Minutes per Workflow

---

## 1. Architectural Overview: Automating the 5-Stage Client Lifecycle Without Code

Throughout **The AI Freelancer Operating System**, you learned a foundational rule: **never automate chaos—systematize the gate first, then automate the repetitive handoff**.

Once you have installed your **5-Database Minimalist Notion OS (`06-NOTION-TEMPLATES/`)** and calibrated your **8-Tab Excel Financial Command Center**, the three JSON blueprints in `14-AUTOMATION-BLUEPRINTS/` eliminate the remaining manual copy-pasting between your inquiry forms, your AI assistant, your Notion CRM, your Google Drive folders, and your Friday CEO Scorecard:

| Blueprint File | Lifecycle Gate Automated | Trigger Event | Automated Actions Executed | Time Saved |
| :--- | :--- | :--- | :--- | :--- |
| **`01-lead-intake-to-ai-brief-and-notion-crm.json`** | **Gate 1 & Gate 2:** Attract, Filter & Rapid Proposal | New prospect submits Tally / Typeform / Webflow inquiry form | 1. Runs **Prompt 3.2** (20-pt P.A.C.E. Fit & Red-Flag Scorer)<br>2. Runs **Prompt 3.3** (3-Tier B.R.I.E.F. Proposal Draft)<br>3. Creates row in Notion `01-Leads-CRM-Pipeline`<br>4. Saves Gmail draft reply (`Script 1` or Proposal) | `~2.5 hrs` per inbound lead |
| **`02-contract-signed-to-48h-onboarding-gate.json`** | **Gate 3:** Zero-Friction 48-Hour Client Onboarding | Deposit invoice paid in Stripe / Gumroad (or Lead marked `05 Closed Won`) | 1. Creates project in Notion `02-Active-Projects-and-Gates` with Client Portal template<br>2. Provisions Google Drive Asset Vault folders<br>3. Runs **Prompts 5.1 & 5.2** (Welcome Packet)<br>4. Schedules 48-Hour Asset Check (**Prompt 5.5 / Script 5**) | `~1.8 hrs` per new client |
| **`03-friday-ceo-scorecard-and-retainer-alert.json`** | **Gate 5:** Weekly Friday CEO Review & Rate-Raise Trigger | Scheduled every Friday at `16:00` local time | 1. Aggregates weekly revenue & Bucket A/B/C/D hours<br>2. Calculates True Weekly EHR & Utilization %<br>3. Runs **Prompts 1.5 & 10.1** (Executive Retro)<br>4. Logs row in Notion `04-Weekly-CEO-Scorecard-Log` & fires 85% Capacity Rate-Raise Alert | `~45 mins` every Friday |

---

## 2. How to Import the `.json` Blueprints into Make.com or n8n

Each `.json` file in `14-AUTOMATION-BLUEPRINTS/` is structured as a universal, dual-compatible blueprint containing both a **Make.com Scenario Blueprint (`make_scenario_blueprint`)** and an **n8n Workflow Graph (`n8n_workflow_nodes`)**, plus a human-readable **Zapier 5-Step Mapping Specification (`zapier_step_mapping`)**.

### Option A: Importing into Make.com (Free or Core Plan)
1. Log into your **Make.com** dashboard and click **`Create a new scenario`** in the top-right corner.
2. In the bottom toolbar of the scenario canvas, click the **`•••` (More)** button and select **`Import Blueprint`**.
3. Upload `01-lead-intake-to-ai-brief-and-notion-crm.json` (or extract the `make_scenario_blueprint` object if your workspace requires a strict root Make export) and click **`Save`**.
4. Click each of the 5 visual module circles on the canvas to connect your personal accounts:
   - **Module 1 (Custom Webhook):** Click `Add` to generate your unique webhook URL and paste that URL into your Tally.so, Typeform, Framer, or Webflow contact form settings.
   - **Module 2 & 3 (OpenAI / Anthropic Claude HTTP Module):** Select your API connection. The exact system instructions and user prompt templates for **Prompt 3.2** and **Prompt 3.3** are pre-populated inside the module payload.
   - **Module 4 (Notion — Create a Database Item):** Select your imported **`01-Leads-CRM-Pipeline`** database.
   - **Module 5 (Gmail / Slack):** Connect your email account so the generated proposal or polite decline (`Script 1`) is saved in your **`Drafts`** folder awaiting your 60-second human verification check.

### Option B: Importing into n8n (Self-Hosted Docker or n8n Cloud)
1. Open your **n8n** workflow editor, click **`Workflows ➔ Add Workflow`**, click the top-right **`•••`** menu, and choose **`Import from File...`**.
2. Select the `.json` blueprint file (n8n reads the `nodes` and `connections` arrays at the top level of each blueprint file directly!).
3. Double-click the **Notion** and **LLM (OpenAI / Anthropic)** nodes to select your saved n8n credentials, then toggle the workflow from `Inactive` to **`Active`**.

### Option C: Building in Zapier in 10 Minutes (Using Zapier AI / Copilot)
1. In Zapier, click **`+ Create Zap`**.
2. Copy the **`zapier_step_mapping`** block from any of our 3 `.json` files (or follow the exact field mappings in Section 3 below) to connect your Form Trigger $\rightarrow$ ChatGPT/Claude Action $\rightarrow$ Notion Action $\rightarrow$ Gmail Create Draft Action.

---

## 3. Detailed Walkthrough & Property Mapping for All 3 Blueprints

### Blueprint 01: Inbound Lead Intake ➔ P.A.C.E. Scorer ➔ B.R.I.E.F. Proposal ➔ Notion CRM (`01-lead-intake-to-ai-brief-and-notion-crm.json`)

#### Step 1: Required Form Fields on Your Intake Form
Create a free form on Tally.so, Typeform, or your website with these 6 fields:
1. `contact_name` (*Full Name*)
2. `company_name` (*Company / Brand URL*)
3. `contact_email` (*Work Email*)
4. `service_category` (*Which package or outcome are you inquiring about?*)
5. `core_bottleneck` (*What is the #1 business metric or bottleneck this project needs to solve in the next 60 days?*)
6. `budget_and_timeline` (*Select your target investment tier and desired launch window: e.g., Option 1 [$3k–$4k], Option 2 [$4.5k–$6.5k], Option 3 [$7k+], or Under $2.5k*)

#### Step 2: AI Prompt 3.2 P.A.C.E. Triage Node Output Schema
The first AI node evaluates the form payload against your **Minimum Tier Floor** and outputs structured JSON:
```json
{
  "fit_score": 18,
  "pain_score": 5,
  "authority_score": 5,
  "cash_score": 4,
  "energy_score": 4,
  "red_flags_detected": "None — Clear decision authority and aligned Option 2 budget",
  "recommended_tier": "Option 2: Core Transformation",
  "quoted_price_usd": 4950,
  "win_probability_pct": 65,
  "routing_action": "FAST_TRACK_PROPOSAL"
}
```

#### Step 3: Conditional Router & Human-in-the-Loop Safety Rule
- **If `fit_score >= 15` (`FAST_TRACK_PROPOSAL`):** The workflow automatically triggers the second AI node (**Prompt 3.3 — 10-Minute B.R.I.E.F. 3-Option Proposal Drafter**), logs the prospect in Notion `01-Leads-CRM-Pipeline` under stage `02 B.R.I.E.F. Qualified`, and creates a **Gmail Draft** containing the 3-option proposal.
- **If `fit_score` is `11–14` (`PITCH_PAID_DIAGNOSTIC`):** Creates a **Gmail Draft** populated with **Script 2** (*Pitching a $950 Paid Diagnostic Blueprint before full build*).
- **If `fit_score <= 10` (`POLITE_DECLINE`):** Logs the lead as `07 Disqualified — Red Flag` in Notion and creates a **Gmail Draft** populated with **Script 1** (*Polite Budget Boundary & Partner Referral*).
- **CRITICAL QUALITY GUARDRAIL:** Notice that the automation creates a **Gmail Draft** rather than auto-sending raw AI output directly to the client. You spend 60 seconds reviewing the numbers against your B.C.R. calculator and click **Send** manually.

---

### Blueprint 02: Deposit Cleared ➔ Notion Project & Portal ➔ Drive Asset Vault ➔ 48-Hour Gate (`02-contract-signed-to-48h-onboarding-gate.json`)

1. **Trigger:** Fires when a client pays their 50% Kickoff Deposit invoice in Stripe/Gumroad OR when you drag a deal card in Notion from `04 Verbal Approval` to `05 Closed Won`.
2. **Action 1 — Notion Project Creation:** Automatically creates a new record in `02-Active-Projects-and-Gates` with:
   - `Current Lifecycle Gate` = `Gate 3: Onboard & Align`
   - `Deposit Status` = `50% Deposit Paid`
   - `48h Asset Gate Status` = `Pending Client Upload (48h Window Active)`
   - Applies the default **`05-Client-Portal-and-Handover-Hub.md`** template inside the page body.
3. **Action 2 — Google Drive Asset Folder Tree:** Creates a parent folder named `[PRJ-ID] Client Name — Project Hub` with three sub-folders:
   - `01-Client-Pre-Flight-Assets-Upload-Here`
   - `02-Contracts-and-Invoices`
   - `03-Deliverables-and-Final-Handover-Vault`
4. **Action 3 — Welcome Packet Draft (`Prompts 5.1 & 5.2`):** Generates the personalized Welcome Email containing the single Notion Client Portal link, the Google Drive upload link, and the 48-Hour Asset Checklist.
5. **Action 4 — Delayed 48-Hour Asset Gate Check (`Prompt 5.5 & Script 5`):** Waits 48 hours, checks the Notion `48h Asset Gate Status` property, and if it is not yet marked `100% Verified`, prepares **Script 5** (*Polite Kickoff Hold & Day-for-Day Timeline Shift Notice*) in your drafts so you never start a sprint with missing credentials.

---

### Blueprint 03: Scheduled Friday 16:00 CEO Scorecard & 85% Rate-Raise Alert (`03-friday-ceo-scorecard-and-retainer-alert.json`)

1. **Trigger:** Runs every Friday afternoon at `16:00` (`4:00 PM`) via a built-in Schedule/Cron node.
2. **Action 1 — Weekly Telemetry Aggregation:** Queries your active projects in `02-Active-Projects-and-Gates` (or reads Tab 7 `06_Daily_3Block_Time_Log` of your Excel/Google Sheet) to sum Weekly Gross Revenue and hours logged across Buckets A, B, C, and D.
3. **Action 2 — Automated EHR & Capacity Math:**
   - Computes `True Weekly EHR = Gross Revenue ÷ Total Real Hours`
   - Computes `Billable Utilization % = Bucket A Hours ÷ Total Real Hours`
   - Computes `Capacity Ratio % = Booked Weekly Hours ÷ Weekly Billable Ceiling (30 hrs)`
4. **Action 3 — AI Executive Retrospective (`Prompts 1.5 & 10.1`):** Passes the week's numbers to Claude/GPT to identify the #1 failed lifecycle gate, prescribe one permanent SOP upgrade, and define Monday's 90-Minute Morning Maker Block priority.
5. **Action 4 — Notion Log & 85% Capacity Rate-Raise Notification:** Appends the complete weekly row to `04-Weekly-CEO-Scorecard-Log` and, if `Capacity Ratio >= 85%`, sends you a high-priority Slack/Email alert instructing you to **increase your next 3 proposal quotes by `+15% to +25%`** and issue **Script 12** to your lowest-EHR legacy client.
