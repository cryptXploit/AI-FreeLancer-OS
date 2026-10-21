# Commercial Cover Design, KDP Paperback Wrap & Gumroad Tier Packaging Specification

**Product Ecosystem:** *The AI Freelancer Operating System: A Practical System to Organize Clients, Automate Repetitive Work, Manage Projects, and Build a More Productive Freelance Business*  
**Imprint:** Practitioner Systems Press — Digital Knowledge Product Studio  
**Version:** `1.0.0` (2026 Commercial Hybrid Edition)

---

## 1. Visual Architecture & Brand Identity System

Unlike generic AI-generated eBook covers that rely on abstract sci-fi stock illustrations, the **AI Freelancer Operating System** cover suite is engineered as an **executive technical manual and software suite identity**. Every cover asset in `08-COVER-DESIGN/` uses vector architectural schematics, precision typography, node-and-gate diagrams, and tier-specific value badges that communicate immediate operational authority at both thumbnail scale (`120px` wide on Amazon search results) and full print resolution (`300 DPI`).

### 1.1 Locked Studio Color Tokens

| Token Name | Hex Code | RGB Value | Cover Application |
| :--- | :--- | :--- | :--- |
| **Primary Deep Navy Slate** | `#0F172A` | `rgb(15, 23, 42)` | Primary structural canvas, spine background, high-contrast authority panels |
| **Elevated Slate Surface** | `#1E293B` | `rgb(30, 41, 59)` | Architectural blueprint cards, schematic node containers, back-cover table rows |
| **Precision Sky Blue** | `#0284C7` | `rgb(2, 132, 199)` | Primary accent bars, stage gate connectors, Tier 2/3 highlight badges |
| **Operational Teal** | `#0D9488` | `rgb(13, 148, 136)` | Verified KPI telemetry nodes, AI workflow badges, Tier 0/4 accent highlights |
| **Executive Amber Gold** | `#F59E0B` | `rgb(245, 158, 11)` | Flagship Bundle callouts, price anchor tags, high-margin indicators |
| **Pure White & Crisp Slate** | `#FFFFFF` / `#F8FAFC` | `rgb(255, 255, 255)` | Main display title typography, KDP ISBN barcode safety box, high-contrast labels |

### 1.2 Typography & Thumbnail Legibility Rules
- **Display Title Font:** `Inter` (`800 ExtraBold` / `900 Black`, uppercase tracking `-0.02em`), sized so the core words **`THE AI FREELANCER OPERATING SYSTEM`** remain 100% legible at `120 × 192 px` mobile retail thumbnail dimensions.
- **Technical Monospace Accents:** `JetBrains Mono` (`600 SemiBold`) for system telemetry tags (`EHR = $85/HR`, `5-GATE OS`, `50 WORKFLOWS`, `B.C.R. PRICING`).

---

## 2. Master Cover Asset Inventory & Platform Dimensions

All six cover compositions are authored as self-contained, resolution-independent **Vector SVGs (`.svg`)** and compiled via headless Chromium (`msedge.exe` / `chrome.exe`) into **300 DPI lossless PNGs (`.png`)** and **Print-Ready PDF (`.pdf`)**:

| Cover ID | Vector Source File | Rendered Output File(s) | Exact Dimensions | Target Retail Platform |
| :--- | :--- | :--- | :--- | :--- |
| **Cover 01** | `kdp-ebook-and-d2d-cover.svg` | `kdp-ebook-and-d2d-cover.png` | `1600 × 2560 px` (`1:1.6` Ratio) | Amazon KDP Kindle eBook, Draft2Digital, Apple Books, Kobo, Barnes & Noble |
| **Cover 02** | `kdp-paperback-full-wrap-cover.svg` | `kdp-paperback-full-wrap-cover.pdf` + `.png` | `3774 × 2775 px` (`12.58" × 9.25"` @ 300 DPI) | Amazon KDP `6.0" × 9.0"` Print Paperback Full Wrap (Back + Spine + Front + Bleed) |
| **Cover 03** | `gumroad-tier0-free-audit-cover.svg` | `gumroad-tier0-free-audit-cover.png` | `1280 × 720 px` (`16:9` HD) | Gumroad & Web Landing Page — **Tier 0 Free Leak Audit Kit ($0)** |
| **Cover 04** | `gumroad-tier2-workbook-edition-cover.svg` | `gumroad-tier2-workbook-edition-cover.png` | `1280 × 720 px` (`16:9` HD) | Gumroad Product Listing — **Tier 2 Interactive Workbook & Planner Edition ($24)** |
| **Cover 05** | `gumroad-tier3-complete-os-cover.svg` | `gumroad-tier3-complete-os-cover.png` | `1280 × 720 px` (`16:9` HD) | Gumroad Flagship Listing — **Tier 3 Complete AI Freelancer OS Bundle ($49)** |
| **Cover 06** | `gumroad-tier4-living-os-membership-cover.svg` | `gumroad-tier4-living-os-membership-cover.png` | `1280 × 720 px` (`16:9` HD) | Gumroad Membership Listing — **Tier 4 Living OS & Pro Vault Pass ($9/mo • $49/yr)** |

---

## 3. Amazon KDP 6.0" × 9.0" Paperback Full-Wrap Engineering Math

Our compiled print interior (`09-EXPORTS/PRINT/the-ai-freelancer-os-kdp-paperback-6x9.pdf`) is **146 pages** on standard white uncoated paper (`0.002252"` per page per Amazon KDP Print Specifications).

### 3.1 Exact Horizontal & Vertical Wrap Calculations
- **Front Cover Trim Width:** `6.000 in` (`1800 px` @ 300 DPI)
- **Back Cover Trim Width:** `6.000 in` (`1800 px` @ 300 DPI)
- **Calculated Spine Width (`146 pages × 0.002252"`):** `0.3288 in` $\rightarrow$ Engineered at **`0.330 in`** (`99 px` @ 300 DPI)
- **Outer Bleed (`0.125 in` Top, Bottom, Left, and Right):** `0.250 in` total horizontal bleed (`75 px`) and `0.250 in` total vertical bleed (`75 px`)
- **Total Full-Wrap Width:**
  $$\text{Width} = 0.125\text{ in (Left Bleed)} + 6.000\text{ in (Back)} + 0.330\text{ in (Spine)} + 6.000\text{ in (Front)} + 0.125\text{ in (Right Bleed)} = 12.580\text{ in } (3,774\text{ px})$$
- **Total Full-Wrap Height:**
  $$\text{Height} = 0.125\text{ in (Top Bleed)} + 9.000\text{ in (Trim Height)} + 0.125\text{ in (Bottom Bleed)} = 9.250\text{ in } (2,775\text{ px})$$

### 3.2 Safety Zones & KDP Barcode Placement
1. **Live Text Safety Margin:** All text, tables, and badges sit at least `0.25 in` (`75 px`) inside the trim edges and `0.0625 in` (`19 px`) clear of the spine fold hinges.
2. **Reserved White KDP ISBN Barcode Box:** Positioned on the lower-right quadrant of the Back Cover (`2.00" × 1.20"` / `600 × 360 px` pure `#FFFFFF` rectangle) at least `0.25 in` clear of the bottom trim and spine hinge so Amazon KDP's automated print prepress engine stamps the ISBN-13 barcode without overlapping any back-cover copy.

---

## 4. Optional AI Visual Prompt Templates for Seasonal Promotional Banners

While our master retail covers use crisp vector geometry for maximum legibility, marketing teams running seasonal social ads (LinkedIn, X, Meta, YouTube thumbnails) can generate photorealistic 3D hardware-and-book lifestyle composites using these tested Midjourney v6 / Flux Pro prompts:

### Prompt A: Flagship Hybrid Product Ecosystem Desk Flat-Lay (`16:9`)
```text
 Overhead architectural studio photograph of a minimalist dark slate desk (#0F172A aesthetic) featuring a matte navy hardcover technical manual titled "THE AI FREELANCER OPERATING SYSTEM", alongside a sleek 16-inch laptop displaying a dark-mode financial dashboard with teal (#0D9488) and sky blue (#0284C7) KPI charts, and an iPad Pro with Apple Pencil showing a clean wireframe checklist workbook. Directional softbox studio lighting, crisp typography, industrial design photography, 85mm lens, f/4, ultra-sharp --ar 16:9 --v 6.1
```

### Prompt B: Isometric SaaS-Lite & Workbook Hardware Stack (`4:3`)
```text
 Clean 3D isometric product showcase render on a deep navy background (#0F172A) with subtle blueprint grid lines (#1E293B). Central floating MacBook Pro displaying a SaaS pricing calculator UI, flanked by a 6x9 trade paperback book and three floating glassmorphic database cards labeled "LEADS CRM", "B.C.R. PRICING", and "50 AI WORKFLOWS" glowing with subtle cyan (#0284C7) and emerald teal (#0D9488) rim lighting. Stripe Press and Linear design aesthetic, octane render, 8k resolution --ar 4:3 --v 6.1
```
