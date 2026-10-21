# Interactive Photo, Mockup & Graphic Design Customizer Studio — User & Brand Customization Guide (`README-DESIGN-KIT.md`)

**Studio Application Path:** `08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html`  
**Compatible Operating Tiers:** Tier 3 (Complete Freelancer OS Flagship Bundle) & Tier 4 (Living OS & Pro Vault Pass)  
**Architecture:** Zero-Dependency Single-File HTML5 + SVG + Canvas 2D Visual Design Studio (`100% Offline & Online Ready`)

---

## 1. Overview: Why We Built an Interactive Visual & Photo Customizer Studio

Independent freelancers, consultants, and agency owners frequently need to customize two categories of visual assets without hiring a graphic designer or paying for Adobe Creative Cloud:
1. **Client-Facing Commercial Graphics:** Custom-branded **Proposal Cover Banners (`1600 × 900 px`)**, **3-Tier Productized Service Pricing Menus (`1280 × 720 px`)**, **LinkedIn/X Authority Carousel Cards (`1080 × 1080 px`)**, and **One-Page Client Onboarding Cheat-Sheets (`1080 × 1350 px`)** featuring the freelancer's own studio name, brand color palette, and headshot or company logo.
2. **Product & Book Packaging Graphics:** Custom **3D Flagship Bundle Mockups (`1280 × 720 px`)** and **High-Resolution eBook/Workbook Covers (`1600 × 2560 px`)**.

The **Interactive Photo, Mockup & Graphic Design Customizer Studio (`design-customizer-studio.html`)** lets you customize all six visual formats in real time right inside your web browser, upload your own headshot photo or agency logo via local `FileReader` (nothing is ever uploaded to an external server), switch between **5 Executive Color Themes**, and export lossless **High-Resolution `.PNG` images** or **Editable Vector `.SVG` files** in a single click.

---

## 2. Walkthrough of the 6 Built-In Visual & Mockup Templates

Open `08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html` in Chrome, Edge, Safari, Brave, or Firefox and select any of the **6 Canvas Templates** in the left control panel:

### Template 01: 3D Flagship Bundle & Software Box Mockup (`1280 × 720 px` — 16:9 HD)
- **Best Used For:** Productized service landing pages, Gumroad/Stripe checkout banners, and portfolio hero graphics.
- **Visual Layout:** Displays a composite architectural showcase of a hardcover manual, laptop software dashboard, tablet planner, and 4 modular deliverable cards alongside your custom price badge and brand logo/photo.

### Template 02: High-Resolution Book & Lead-Magnet Cover Designer (`1600 × 2560 px` — 1:1.6 Portrait)
- **Best Used For:** Creating custom vertical covers for your own client-facing Paid Diagnostic Blueprints, Whitepapers, SOP Manuals, or Amazon KDP / Draft2Digital eBooks.
- **Visual Layout:** Includes top imprint header, multi-line display title, subtitle bar, 5-stage architectural schematic diagram, 3 bottom metric badges, and an author/studio attribution footer with optional circular headshot/logo frame.

### Template 03: Client Proposal & Kickoff Cover Banner (`1600 × 900 px` — 16:9 Widescreen)
- **Best Used For:** Pasting at the top of your **Notion Client Portal (`05-Client-Portal-and-Handover-Hub.md`)**, **Word B.R.I.E.F. Proposal (`03-Client-3-Tier-BRIEF-Proposal-Template.docx`)**, or **PowerPoint Pitch Deck (`01-Discovery-and-3-Tier-Proposal-Pitch-Deck.pptx`)**.
- **Visual Layout:** Highlights the client's company name, project North-Star outcome, sprint kickoff date, and your studio branding.

### Template 04: LinkedIn / X Authority Framework Carousel Card (`1080 × 1080 px` — 1:1 Square)
- **Best Used For:** Publishing high-authority social case studies and operational teardown posts on LinkedIn, X/Twitter, and Instagram to attract inbound Stage 1 leads.
- **Visual Layout:** Features a bold problem/solution headline, a 3-step visual system diagram, quantified Before/After ROI telemetry badges, and your circular founder headshot and handle at the bottom.

### Template 05: 60-Second Cheat-Sheet Infographic Poster (`1080 × 1350 px` — 4:5 Portrait)
- **Best Used For:** Sharing one-page client onboarding rules, async communication SLAs, or internal SOP reference cards.
- **Visual Layout:** Structured 4-box vertical poster with header banner, core formula callout, 3-step protocol checklist, and footer verification badge.

### Template 06: 3-Tier Productized Service Pricing Menu Card (`1280 × 720 px` — 16:9 HD)
- **Best Used For:** Embedding directly on your freelance inquiry page or sending inside your initial **P.A.C.E. Lead Triage reply (`Script 1`)** so prospects self-select their budget tier before booking a call.
- **Visual Layout:** Side-by-side comparison of **Tier 1 (Essential Baseline)**, **Tier 2 (Core Transformation — Recommended Anchor)**, and **Tier 3 (Turnkey & Retainer Partner)**.

---

## 3. Customizing Typography, Color Themes & Uploading Photos/Logos

### 3.1 Applying the 5 One-Click Executive Color Themes
Click any of the **5 Theme Presets** in the sidebar (or pick custom hex colors using the native color pickers):
1. **Theme 01 — Studio Slate & Sky (Default):** Primary `#0F172A`, Elevated `#1E293B`, Accent `#0284C7`, Secondary `#0D9488`.
2. **Theme 02 — Emerald Wealth & Forest:** Primary `#064E3B`, Elevated `#065F46`, Accent `#10B981`, Secondary `#34D399`.
3. **Theme 03 — Midnight Indigo & Violet:** Primary `#1E1B4B`, Elevated `#312E81`, Accent `#6366F1`, Secondary `#38BDF8`.
4. **Theme 04 — Executive Crimson & Obsidian:** Primary `#18181B`, Elevated `#27272A`, Accent `#E11D48`, Secondary `#F59E0B`.
5. **Theme 05 — Light Editorial Paper:** Primary `#F8FAFC`, Elevated `#FFFFFF`, Accent `#0284C7`, Secondary `#0F172A` (dark text on crisp light canvas).

### 3.2 Uploading Your Custom Headshot Photo or Studio Logo
1. In the **Photo / Logo / Avatar Upload** panel on the left sidebar, click **Choose Image File (`.png`, `.jpg`, `.webp`, `.svg`)**.
2. The studio uses your browser's local `FileReader` API to convert your image into an inline Data URI and places it inside the circular/rounded brand frame on the active SVG canvas.
3. Toggle the **Image Frame Shape** between `Circle Avatar`, `Rounded Square Logo`, or `Hidden (Typography Only)` and adjust the scale slider as needed.

---

## 4. Exporting to High-Res `.PNG`, Vector `.SVG`, Canva, or Figma

1. **1-Click High-Resolution `.PNG` Export:**
   - Click **`Download High-Res .PNG`**. The application serializes the live vector SVG, renders it onto an HTML5 `<canvas>` at exact native pixel dimensions (`1600×2560`, `1600×900`, `1280×720`, or `1080×1080`), and downloads a crisp, lossless `.png` file ready for immediate upload to Amazon KDP, Gumroad, Notion, Word, PowerPoint, or LinkedIn.
2. **1-Click Editable Vector `.SVG` Export (For Figma, Canva & Illustrator):**
   - Click **`Download Editable .SVG`**. You can drag and drop the downloaded `.svg` file directly into **Figma**, **Canva** (*Uploads ➔ Upload files*), **Adobe Illustrator**, or **Affinity Designer** with 100% of vector shapes, layers, and text nodes preserved.
