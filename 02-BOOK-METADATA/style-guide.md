# Digital Knowledge Product Studio — Master Editorial & Production Style Guide

**Product Ecosystem:** *The AI Freelancer Operating System: A Practical System to Organize Clients, Automate Repetitive Work, Manage Projects, and Build a More Productive Freelance Business*  
**Version:** 1.0.0  
**Governance Scope:** All 10 Core Chapters, 20 Vector SVG Diagrams, 10 Standalone Workbooks, Notion OS Schemas, and Web Companion App Modules.

---

## 1. Studio Editorial Philosophy: *System Over Theory*

Every page in *The AI Freelancer Operating System* is engineered as an operational manual for working practitioners—never as an academic treatise or motivational essay. Independent freelancers, consultants, and solopreneurs in the $2,000–$8,000/month revenue band do not suffer from a lack of inspiration; they suffer from missing operational gates, unpriced scope expansion, and fragmented administrative workflows.

1. **Actionable Mechanics First:** Every concept must immediately translate into a concrete formula, a circuit-breaker decision rule, a client boundary script, or a variable-driven AI workflow prompt.
2. **Quantified Operational Grounding:** Replace vague productivity claims with transparent operational math (for example, `Actual Effective Hourly Rate [EHR] = Gross Revenue ÷ Total Real Working Hours`) and realistic practitioner financial walkthroughs.
3. **Zero Placeholder Tolerance:** Never output `TODO`, `TBD`, `Lorem Ipsum`, `[insert content here]`, or truncated sections. Every table, prompt, and checklist must be 100% production-ready upon creation.

---

## 2. Strict Lexical Filter & Anti-Cliché Governance

To guarantee an authentic, battle-tested practitioner voice across the entire manuscript, the automated QA engine (`verify_phase1.py` and subsequent phase verifiers) enforces a strict zero-tolerance regex check against synthetic AI filler vocabulary.

### 2.1 Banned Single Words (Case-Insensitive Word-Boundary Match)
The following 16 words are strictly prohibited across all manuscript chapters:
* `delve`
* `tapestry`
* `testament`
* `beacon`
* `symphony`
* `unlock`
* `unleash`
* `skyrocket`
* `supercharge`
* `game-changer`
* `pivotal`
* `realm`
* `foster`
* `underscore`
* `utilize` *(Always use `use` or `apply` instead)*
* `leverage` *(Strictly prohibited as a verb or noun in manuscript prose; use `apply`, `deploy`, or `use`)*

### 2.2 Banned Phrases (Case-Insensitive Substring Match)
The following 7 synthetic transitional phrases are strictly prohibited:
* `in today's fast-paced world`
* `ever-evolving landscape`
* `it is important to remember`
* `in conclusion`
* `without further ado`
* `let's dive in`
* `look no further`

---

## 3. Sentence Rhythm, Paragraph Cadence & American English Conventions

1. **Orthography & Spelling:** Write in crisp, direct, practitioner-grade American English (`optimize`, `systematize`, `organization`, `canceled`, `program`, `analyze`, `prioritize`, `monetize`). Use the Oxford comma consistently in all series (`scope, timeline, and payment schedule`).
2. **Sentence Rhythm Alternation:** Alternate between analytical 18–25 word sentences that explain operational cause-and-effect and punchy 4–8 word declarative statements that lock in rules (e.g., *Unpriced favors destroy freelance margins.* / *Install the gate before work begins.*).
3. **Paragraph Length Ceiling:** Keep prose paragraphs under **65 words** (typically 2 to 4 sentences). Long walls of text cause cognitive fatigue and fail both print readability and tablet skimming tests.
4. **Active Imperative Voice:** Address the reader directly (`you`, `your practice`, `your client pipeline`) using imperative verbs (`Audit`, `Calculate`, `Pause`, `Route`, `Execute`).

---

## 4. Standardized 14-Part Chapter Architecture

Every chapter (`chapter-01.md` through `chapter-10.md`) must exceed **3,500 words** (`>= 3,800 words` target for Chapter 1) and contain these exact **14 required structural headings** in sequential order:

1. `# Chapter N: [Chapter Title]` *(plus descriptive operational subtitle)*
2. `## 1. Learning Objectives` *(4 measurable operational outcomes the reader will install)*
3. `## 2. The Real-World Friction Point` *(Concrete timestamped practitioner scenario illustrating the exact revenue and time leak)*
4. `## 3. Why Standard Approaches Fail` *(3 structural failure modes of conventional advice, bloated templates, or generic prompt packs)*
5. `## 4. Core Framework: [Named System]` *(Deep architectural breakdown of the chapter's named operating model)*
6. `### Visual Architecture: System Mindmap` *(Embedded link to `../../04-VISUAL-ASSETS/Mindmaps/chapter-0N-mindmap.svg` + 5-gate/component Markdown comparison table)*
7. `## 5. Step-by-Step Implementation Protocol` *(4 sequential execution steps with concrete metrics and rules)*
8. `### Operational Decision Tree` *(Embedded link to `../../04-VISUAL-ASSETS/Flowcharts/chapter-0N-flowchart.svg` + routing walkthrough)*
9. `## 6. Tested AI Workflow Prompts` *(5 complete, copy-paste-ready system prompts `Prompt N.1` to `Prompt N.5` inside fenced code blocks with `[BRACKETED VARIABLES]`, **Operational Objective**, **When to Run**, and **Verification Rule**)*
10. `## 7. Real-World Implementation Case Study` *(Realistic named freelancer walkthrough with exact baseline vs. 30-day post-implementation metrics and a Before/After Markdown table)*
11. `## 8. Common Operational Pitfalls & Fixes` *(4-row diagnostic table pairing failure modes with immediate operational fixes)*
12. `## 9. Chapter Action Worksheet` *(In-chapter interactive audit & scorecard tables, paired with the expanded standalone 5-part worksheet in `05-WORKBOOKS/worksheet-0N.md`)*
13. `## 10. Executive Summary & Implementation Checklist` *(Core operational synthesis + 5-item `[ ]` action checklist)*
14. `## 11. Sources & Operational References` *(Verified platform, tax, contract, and empirical research citations matching `01-MARKET-RESEARCH/sources.md`)*

---

## 5. Visual Design Tokens, Typography & Table Standards

### 5.1 Locked Color Palette
| Token Role | Hex Code | Usage Specification |
| :--- | :--- | :--- |
| **Primary (Deep Navy Slate)** | `#0F172A` | Primary headings, SVG central hubs, table header backgrounds, high-emphasis banners |
| **Accent (Precision Sky Blue)** | `#0284C7` | Primary decision gates, interactive callouts, SVG stage headers, active links |
| **Secondary (Operational Teal)** | `#0D9488` | Positive KPI badges, AI execution nodes, verification rules, completion states |
| **Body Text (Charcoal Slate)** | `#1E293B` | Main body copy, table cell contents, SVG descriptive labels on light surfaces |
| **Muted Text (Neutral Slate)** | `#64748B` | Captions, footnotes, secondary labels, subtle borders, axis annotations |
| **Background (Pure White)** | `#FFFFFF` | Page canvas, card interiors, high-contrast text on `#0F172A` / `#0284C7` / `#0D9488` fills |

### 5.2 Typography Hierarchy & Minimum Print/Digital Floors
* **Heading Font:** `Inter` (Bold 700 / Semi-Bold 600, tight tracking `-0.02em`)
* **Body Font:** `Inter` (Regular 400 / Medium 500, line-height `1.55` for digital, `1.38` for `6.0" x 9.0"` print)
* **Monospace / Prompt Font:** `JetBrains Mono` (Regular 400, used inside all AI prompt blocks and formula callouts)
* **Strict Readability Floors:**
  * Main body text must never render below **`10.5pt`**.
  * Markdown tables, fenced prompt code blocks, and footnotes must never render below **`9.5pt`**.

### 5.3 Booktabs Table Rules
* Every table must use clean Markdown syntax with explicit column alignment (`:---`, `:---:`, `---:`).
* In PDF/Print compilation, tables follow academic `booktabs` styling: heavy top rule (`1.5pt #0F172A`), medium header rule (`0.75pt #CBD5E1`), alternating subtle row tint (`#F8FAFC`), and zero vertical grid lines to maximize legibility.

### 5.4 SVG Vector Diagram Standards
1. **Valid Self-Contained XML:** Every `.svg` file in `04-VISUAL-ASSETS/Mindmaps/` and `04-VISUAL-ASSETS/Flowcharts/` must parse cleanly via Python's `xml.etree.ElementTree` with explicit `xmlns="http://www.w3.org/2000/svg"` and `viewBox` attributes (`0 0 960 540` for Mindmaps; `0 0 960 560` for Flowcharts).
2. **Explicit Visible `<text>` Elements:** Every diagram must contain at least **15 non-empty `<text>` nodes** with explicit inline `font-family: 'Inter', Arial, sans-serif;` and high-contrast hex fills (`#0F172A`, `#FFFFFF`, `#0284C7`, `#0D9488`, `#1E293B`) so text never disappears in browser, WeasyPrint, or EPUB renderers.
3. **No External Font or Image Dependencies:** All shapes, connectors, arrowheads (`<marker>`), badges, and typography must be self-contained vector primitives.
