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
