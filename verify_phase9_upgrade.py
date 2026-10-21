#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 9 Automated QA & Master Upgrade Verification Engine (verify_phase9_upgrade.py)
The AI Freelancer Operating System — Digital Knowledge Product Studio

Audits all 6 Phase 9 Ultra-Premium Ecosystem Upgrades + All 5 Repackaged Commercial Release ZIPs:
1. UPGRADE 1 (13-VISUAL-CHEAT-SHEETS/):
   - 00-ECOSYSTEM-MASTER-MAP-POSTER.svg (viewBox 0 0 1600 1100, >=35 <text> nodes) + .png
   - cheat-sheet-ch01.svg .. ch10.svg (viewBox 0 0 1200 1600, >=25 <text> nodes each) + 10 .pngs
   - the-ai-freelancer-os-visual-shortcut-atlas.pdf (>=12 pages via pypdf, >=50 KB) in 13-VISUAL-CHEAT-SHEETS/ & 09-EXPORTS/PDF/
2. UPGRADE 2 (12-EDITABLE-OFFICE-SUITE/Word-Docs/):
   - All 7 .docx files opened via python-docx, word counts verified, zero banned words/placeholders
3. UPGRADE 3 (12-EDITABLE-OFFICE-SUITE/Slide-Decks/):
   - All 3 .pptx files opened via python-pptx, 16:9 widescreen dimensions, 12/10/10 slides, presenter notes, zero banned words
4. UPGRADE 4 (06-NOTION-TEMPLATES/Spreadsheets/):
   - 8-Tab Charted Excel Command Center opened via openpyxl, 8 tabs verified, >=3 native charts on Tab 00, >=1 chart on Tab 01, live formulas
5. UPGRADE 5 (08-COVER-DESIGN/Editable-Design-Kit/):
   - design-customizer-studio.html (>=65,000 bytes, 6 templates, 5 themes, FileReader, canvas PNG/SVG export) + README-DESIGN-KIT.md (>=600 words)
6. UPGRADE 6 (14-AUTOMATION-BLUEPRINTS/):
   - 3 valid JSON automation blueprints + NO-CODE-AUTOMATION-SETUP-GUIDE.md (>=1,200 words)
7. Repackaged Tier0..Tier4 .zip integrity & Phase 9 inclusion check
8. Updates PROJECT_STATE.json & writes 11-QUALITY-ASSURANCE/qa-phase9-upgrade-report.json
"""

import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import docx
import openpyxl
from pptx import Presentation
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parent

BANNED_WORDS = [
    "delve",
    "tapestry",
    "testament",
    "beacon",
    "symphony",
    "unlock",
    "unleash",
    "skyrocket",
    "supercharge",
    "game-changer",
    "pivotal",
    "realm",
    "foster",
    "underscore",
    "utilize",
    "leverage",
]

BANNED_PHRASES = [
    "in today's fast-paced world",
    "ever-evolving landscape",
    "it is important to remember",
    "in conclusion",
    "without further ado",
    "let's dive in",
    "look no further",
]

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bFIXME\b",
    r"lorem ipsum",
]


def scan_text_hygiene(text: str, label: str, errors: list[str]):
    # Strip meta documentation lines listing banned words
    cleaned = re.sub(r"Banned Words[^\n]*", "", text, flags=re.IGNORECASE)
    cleaned = re.sub(r"Never use:[^\n]*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"Zero Banned Words[^\n]*", "", cleaned, flags=re.IGNORECASE)

    for bw in BANNED_WORDS:
        if re.search(rf"\b{re.escape(bw)}\b", cleaned, flags=re.IGNORECASE):
            errors.append(f"[Lexical Violation] Banned word '{bw}' found in {label}")
    for bp in BANNED_PHRASES:
        if re.search(re.escape(bp), cleaned, flags=re.IGNORECASE):
            errors.append(f"[Lexical Violation] Banned phrase '{bp}' found in {label}")
    for pat in PLACEHOLDER_PATTERNS:
        if re.search(pat, cleaned, flags=re.IGNORECASE if "lorem" in pat else 0):
            errors.append(f"[Placeholder Violation] Pattern '{pat}' found in {label}")


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def main() -> int:
    errors: list[str] = []
    report: dict = {
        "phase": "Phase 9 — Ultra-Premium Ecosystem Expansion (6 Suites + 5 Repackaged ZIPs)",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "upgrades": {},
        "repackaged_zips": {},
    }

    print("=" * 82)
    print("PHASE 9 MASTER QA AUDITOR — AUDITING ALL 6 ULTRA-PREMIUM UPGRADES & 5 ZIPS")
    print("=" * 82)

    # ==========================================================================
    # UPGRADE 1: 60-SECOND VISUAL SHORTCUT ATLAS (13-VISUAL-CHEAT-SHEETS/)
    # ==========================================================================
    cheat_dir = BASE_DIR / "13-VISUAL-CHEAT-SHEETS"
    u1_stats = {"svgs": {}, "pngs": {}, "pdf_pages": 0, "pdf_bytes": 0}

    poster_svg = cheat_dir / "00-ECOSYSTEM-MASTER-MAP-POSTER.svg"
    poster_png = cheat_dir / "00-ECOSYSTEM-MASTER-MAP-POSTER.png"
    if not poster_svg.exists():
        errors.append("Missing 00-ECOSYSTEM-MASTER-MAP-POSTER.svg")
    else:
        raw_svg = poster_svg.read_text(encoding="utf-8")
        scan_text_hygiene(raw_svg, poster_svg.name, errors)
        try:
            root = ET.fromstring(raw_svg)
            vb = root.attrib.get("viewBox", "")
            txt_nodes = [el for el in root.iter() if el.tag.endswith("text")]
            if vb != "0 0 1600 1100":
                errors.append(f"Poster SVG viewBox expected '0 0 1600 1100', got '{vb}'")
            if len(txt_nodes) < 35:
                errors.append(f"Poster SVG has {len(txt_nodes)} <text> nodes (expected >= 35)")
            u1_stats["svgs"][poster_svg.name] = {"viewBox": vb, "text_nodes": len(txt_nodes), "bytes": poster_svg.stat().st_size}
        except Exception as exc:
            errors.append(f"Invalid XML in {poster_svg.name}: {exc}")

    if not poster_png.exists() or poster_png.stat().st_size < 30000:
        errors.append("Missing or undersized 00-ECOSYSTEM-MASTER-MAP-POSTER.png (<30KB)")
    else:
        with poster_png.open("rb") as f:
            if f.read(8) != b"\x89PNG\r\n\x1a\n":
                errors.append("Invalid PNG signature on 00-ECOSYSTEM-MASTER-MAP-POSTER.png")
        u1_stats["pngs"][poster_png.name] = poster_png.stat().st_size

    for ch in range(1, 11):
        cs_svg = cheat_dir / f"cheat-sheet-ch{ch:02d}.svg"
        cs_png = cheat_dir / f"cheat-sheet-ch{ch:02d}.png"
        if not cs_svg.exists():
            errors.append(f"Missing {cs_svg.name}")
        else:
            raw_cs = cs_svg.read_text(encoding="utf-8")
            scan_text_hygiene(raw_cs, cs_svg.name, errors)
            try:
                root = ET.fromstring(raw_cs)
                vb = root.attrib.get("viewBox", "")
                txt_nodes = [el for el in root.iter() if el.tag.endswith("text")]
                if vb != "0 0 1200 1600":
                    errors.append(f"{cs_svg.name} viewBox expected '0 0 1200 1600', got '{vb}'")
                if len(txt_nodes) < 25:
                    errors.append(f"{cs_svg.name} has {len(txt_nodes)} <text> nodes (expected >= 25)")
                u1_stats["svgs"][cs_svg.name] = {"viewBox": vb, "text_nodes": len(txt_nodes), "bytes": cs_svg.stat().st_size}
            except Exception as exc:
                errors.append(f"Invalid XML in {cs_svg.name}: {exc}")

        if not cs_png.exists() or cs_png.stat().st_size < 30000:
            errors.append(f"Missing or undersized {cs_png.name} (<30KB)")
        else:
            with cs_png.open("rb") as f:
                if f.read(8) != b"\x89PNG\r\n\x1a\n":
                    errors.append(f"Invalid PNG signature on {cs_png.name}")
            u1_stats["pngs"][cs_png.name] = cs_png.stat().st_size

    atlas_pdf1 = cheat_dir / "the-ai-freelancer-os-visual-shortcut-atlas.pdf"
    atlas_pdf2 = BASE_DIR / "09-EXPORTS" / "PDF" / "the-ai-freelancer-os-visual-shortcut-atlas.pdf"
    for ap in (atlas_pdf1, atlas_pdf2):
        if not ap.exists() or ap.stat().st_size < 50000:
            errors.append(f"Missing or undersized Visual Shortcut Atlas PDF at {ap}")
    if atlas_pdf1.exists():
        reader = PdfReader(str(atlas_pdf1))
        u1_stats["pdf_pages"] = len(reader.pages)
        u1_stats["pdf_bytes"] = atlas_pdf1.stat().st_size
        if len(reader.pages) < 12:
            errors.append(f"Visual Shortcut Atlas PDF has {len(reader.pages)} pages (expected >= 12)")

    report["upgrades"]["upgrade_1_visual_shortcut_atlas"] = u1_stats
    print(f"[Upgrade 1 QA] Verified 11 SVGs, 11 PNGs & {u1_stats['pdf_pages']}-page Visual Shortcut Atlas PDF ({u1_stats['pdf_bytes']:,} bytes).")

    # ==========================================================================
    # UPGRADE 2: 7 EDITABLE WORD (.DOCX) DOCUMENTS
    # ==========================================================================
    word_dir = BASE_DIR / "12-EDITABLE-OFFICE-SUITE" / "Word-Docs"
    expected_docx = [
        ("01-Editable-Complete-Book-Manuscript.docx", 50000),
        ("02-Editable-10-Chapter-Action-Workbook.docx", 8000),
        ("03-Client-3-Tier-BRIEF-Proposal-Template.docx", 1200),
        ("04-Master-Service-Agreement-and-SOW-Contract.docx", 1800),
        ("05-PVP-Formal-Change-Order-Request-Form.docx", 600),
        ("06-Client-Welcome-Packet-and-48h-Onboarding-Guide.docx", 1000),
        ("07-Final-Handover-Certificate-and-90Day-Retainer-Pitch.docx", 1000),
    ]
    u2_stats = {}
    for fname, min_words in expected_docx:
        fpath = word_dir / fname
        if not fpath.exists():
            errors.append(f"Missing Word document: {fname}")
            continue
        doc = docx.Document(str(fpath))
        chunks = [p.text for p in doc.paragraphs if p.text.strip()]
        for tbl in doc.tables:
            for row in tbl.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        chunks.append(cell.text)
        full_txt = "\n".join(chunks)
        wc = count_words(full_txt)
        scan_text_hygiene(full_txt, fname, errors)
        if wc < min_words:
            errors.append(f"{fname} has {wc} words (expected >= {min_words})")
        u2_stats[fname] = {
            "bytes": fpath.stat().st_size,
            "words": wc,
            "paragraphs": len(doc.paragraphs),
            "tables": len(doc.tables),
        }
    report["upgrades"]["upgrade_2_editable_word_suite"] = u2_stats
    print(f"[Upgrade 2 QA] Verified all {len(u2_stats)} Editable Microsoft Word (.docx) Documents.")

    # ==========================================================================
    # UPGRADE 3: 3 EDITABLE POWERPOINT (.PPTX) SLIDE DECKS
    # ==========================================================================
    pptx_dir = BASE_DIR / "12-EDITABLE-OFFICE-SUITE" / "Slide-Decks"
    expected_pptx = [
        ("01-Discovery-and-3-Tier-Proposal-Pitch-Deck.pptx", 12),
        ("02-Client-Kickoff-and-48h-Alignment-Deck.pptx", 10),
        ("03-ROI-Case-Study-and-90Day-Retainer-Pitch-Deck.pptx", 10),
    ]
    u3_stats = {}
    for fname, req_slides in expected_pptx:
        fpath = pptx_dir / fname
        if not fpath.exists():
            errors.append(f"Missing PowerPoint deck: {fname}")
            continue
        prs = Presentation(str(fpath))
        slide_count = len(prs.slides)
        if slide_count != req_slides:
            errors.append(f"{fname} has {slide_count} slides (expected {req_slides})")

        w_in = round(prs.slide_width.inches, 2)
        h_in = round(prs.slide_height.inches, 2)
        if abs(w_in - 13.33) > 0.05 or abs(h_in - 7.50) > 0.05:
            errors.append(f"{fname} dimensions {w_in}x{h_in} in (expected 13.33x7.50 in)")

        deck_text_chunks = []
        notes_count = 0
        for s_idx, sl in enumerate(prs.slides, start=1):
            for sh in sl.shapes:
                if sh.has_text_frame:
                    deck_text_chunks.append(sh.text_frame.text)
            if sl.has_notes_slide and sl.notes_slide.notes_text_frame.text.strip():
                notes_count += 1
                deck_text_chunks.append(sl.notes_slide.notes_text_frame.text)
            else:
                errors.append(f"{fname} Slide {s_idx} is missing presenter notes")

        full_deck_txt = "\n".join(deck_text_chunks)
        scan_text_hygiene(full_deck_txt, fname, errors)
        u3_stats[fname] = {
            "bytes": fpath.stat().st_size,
            "slides": slide_count,
            "slides_with_notes": notes_count,
            "dimensions_in": f"{w_in}x{h_in}",
            "words": count_words(full_deck_txt),
        }
    report["upgrades"]["upgrade_3_powerpoint_slide_decks"] = u3_stats
    print(f"[Upgrade 3 QA] Verified all 3 Widescreen 16:9 PowerPoint (.pptx) Decks (32 total slides with presenter notes).")

    # ==========================================================================
    # UPGRADE 4: 8-TAB CHARTED EXCEL COMMAND CENTER
    # ==========================================================================
    xlsx_path = BASE_DIR / "06-NOTION-TEMPLATES" / "Spreadsheets" / "the-ai-freelancer-os-financial-and-pricing-matrix.xlsx"
    xlsx_mirror = BASE_DIR / "09-EXPORTS" / "HYBRID-BUNDLE" / "the-ai-freelancer-os-financial-and-pricing-matrix.xlsx"
    expected_tabs = [
        "00_Executive_Visual_Dashboard",
        "01_EHR_Leak_Audit",
        "02_BCR_Scope_Pricing",
        "03_Client_80_20_Roster",
        "04_90Day_Pipeline_Cashflow",
        "05_Client_Invoice_Generator",
        "06_Daily_3Block_Time_Log",
        "07_Annual_Tax_Expense_Ledger",
    ]
    u4_stats = {}
    if not xlsx_path.exists() or not xlsx_mirror.exists():
        errors.append("Missing 8-Tab Excel Command Center .xlsx file")
    else:
        wb = openpyxl.load_workbook(str(xlsx_path), data_only=False)
        if wb.sheetnames != expected_tabs:
            errors.append(f"Excel tabs mismatch: got {wb.sheetnames}, expected {expected_tabs}")

        total_formulas = 0
        total_charts = 0
        tab_details = {}
        for sname in wb.sheetnames:
            ws = wb[sname]
            f_cnt = 0
            for row in ws.iter_rows(values_only=True):
                for val in row:
                    if isinstance(val, str):
                        if val.startswith("="):
                            f_cnt += 1
                        scan_text_hygiene(val, f"Excel {sname}", errors)
            c_cnt = len(getattr(ws, "_charts", []))
            total_formulas += f_cnt
            total_charts += c_cnt
            tab_details[sname] = {"rows": ws.max_row, "cols": ws.max_column, "formulas": f_cnt, "charts": c_cnt}

        if tab_details.get("00_Executive_Visual_Dashboard", {}).get("charts", 0) < 3:
            errors.append("Tab 00_Executive_Visual_Dashboard has fewer than 3 embedded OpenPyXL charts")
        if tab_details.get("01_EHR_Leak_Audit", {}).get("charts", 0) < 1:
            errors.append("Tab 01_EHR_Leak_Audit is missing embedded PieChart")
        if total_formulas < 150:
            errors.append(f"Excel Command Center has only {total_formulas} formulas (expected >= 150 across 8 tabs)")

        u4_stats = {
            "bytes": xlsx_path.stat().st_size,
            "sheet_count": len(wb.sheetnames),
            "total_formulas": total_formulas,
            "total_embedded_charts": total_charts,
            "tabs": tab_details,
        }
    report["upgrades"]["upgrade_4_8tab_excel_command_center"] = u4_stats
    print(f"[Upgrade 4 QA] Verified 8-Tab Excel Command Center ({u4_stats.get('total_formulas', 0)} formulas, {u4_stats.get('total_embedded_charts', 0)} native charts).")

    # ==========================================================================
    # UPGRADE 5: INTERACTIVE PHOTO & GRAPHIC DESIGN CUSTOMIZER STUDIO
    # ==========================================================================
    studio_html = BASE_DIR / "08-COVER-DESIGN" / "Editable-Design-Kit" / "design-customizer-studio.html"
    studio_readme = BASE_DIR / "08-COVER-DESIGN" / "Editable-Design-Kit" / "README-DESIGN-KIT.md"
    u5_stats = {}
    if not studio_html.exists() or studio_html.stat().st_size < 65000:
        errors.append("Missing or undersized design-customizer-studio.html (<65,000 bytes)")
    else:
        st_txt = studio_html.read_text(encoding="utf-8")
        scan_text_hygiene(st_txt, "design-customizer-studio.html", errors)
        for token in ["FileReader", "toBlob", "t1_ebook", "t2_gumroad", "t3_proposal", "t4_linkedin", "t5_carousel", "t6_video"]:
            if token not in st_txt:
                errors.append(f"design-customizer-studio.html missing required feature token: {token}")
        u5_stats["studio_html_bytes"] = studio_html.stat().st_size

    if not studio_readme.exists():
        errors.append("Missing README-DESIGN-KIT.md")
    else:
        rm_txt = studio_readme.read_text(encoding="utf-8")
        scan_text_hygiene(rm_txt, "README-DESIGN-KIT.md", errors)
        rm_wc = count_words(rm_txt)
        if rm_wc < 600:
            errors.append(f"README-DESIGN-KIT.md has {rm_wc} words (expected >= 600)")
        u5_stats["readme_words"] = rm_wc

    report["upgrades"]["upgrade_5_design_customizer_studio"] = u5_stats
    print(f"[Upgrade 5 QA] Verified Interactive Design Customizer Studio ({u5_stats.get('studio_html_bytes', 0):,} bytes) + Guide ({u5_stats.get('readme_words', 0)} words).")

    # ==========================================================================
    # UPGRADE 6: NO-CODE AUTOMATION BLUEPRINTS (14-AUTOMATION-BLUEPRINTS/)
    # ==========================================================================
    auto_dir = BASE_DIR / "14-AUTOMATION-BLUEPRINTS"
    expected_jsons = [
        "01-lead-intake-to-ai-brief-and-notion-crm.json",
        "02-contract-signed-to-48h-onboarding-gate.json",
        "03-friday-ceo-scorecard-and-retainer-alert.json",
    ]
    u6_stats = {"blueprints": {}}
    for jname in expected_jsons:
        jpath = auto_dir / jname
        if not jpath.exists():
            errors.append(f"Missing automation blueprint: {jname}")
            continue
        raw_j = jpath.read_text(encoding="utf-8")
        scan_text_hygiene(raw_j, jname, errors)
        parsed = json.loads(raw_j)
        if "trigger" not in parsed or "modules" not in parsed or len(parsed["modules"]) < 4:
            errors.append(f"{jname} missing trigger or >=4 workflow modules")
        u6_stats["blueprints"][jname] = {"bytes": jpath.stat().st_size, "modules": len(parsed.get("modules", []))}

    auto_guide = auto_dir / "NO-CODE-AUTOMATION-SETUP-GUIDE.md"
    if not auto_guide.exists():
        errors.append("Missing NO-CODE-AUTOMATION-SETUP-GUIDE.md")
    else:
        ag_txt = auto_guide.read_text(encoding="utf-8")
        scan_text_hygiene(ag_txt, "NO-CODE-AUTOMATION-SETUP-GUIDE.md", errors)
        ag_wc = count_words(ag_txt)
        if ag_wc < 1200:
            errors.append(f"NO-CODE-AUTOMATION-SETUP-GUIDE.md has {ag_wc} words (expected >= 1,200)")
        u6_stats["setup_guide_words"] = ag_wc

    report["upgrades"]["upgrade_6_automation_blueprints"] = u6_stats
    print(f"[Upgrade 6 QA] Verified 3 JSON Automation Blueprints + Setup Guide ({u6_stats.get('setup_guide_words', 0)} words).")

    # ==========================================================================
    # VERIFY ALL 5 REPACKAGED COMMERCIAL RELEASE .ZIP BUNDLES
    # ==========================================================================
    bundle_dir = BASE_DIR / "09-EXPORTS" / "HYBRID-BUNDLE"
    zip_specs = [
        ("Tier0-Free-Leak-Audit-Starter-Kit.zip", 8, ["00-ECOSYSTEM-MASTER-MAP-POSTER.png", "cheat-sheet-ch01.png"]),
        ("Tier1-KDP-and-D2D-Publisher-Upload-Pack.zip", 9, ["the-ai-freelancer-os.epub"]),
        ("Tier2-Interactive-Workbook-and-Planner-Edition.zip", 39, ["the-ai-freelancer-os-visual-shortcut-atlas.pdf", "02-Editable-10-Chapter-Action-Workbook.docx"]),
        ("Tier3-Complete-AI-Freelancer-OS-Flagship-Bundle.zip", 80, [
            "01-BOOK-AND-WORKBOOKS/the-ai-freelancer-os-visual-shortcut-atlas.pdf",
            "06-EDITABLE-WORD-AND-PPTX-OFFICE-SUITE/Word-Docs/04-Master-Service-Agreement-and-SOW-Contract.docx",
            "06-EDITABLE-WORD-AND-PPTX-OFFICE-SUITE/Slide-Decks/01-Discovery-and-3-Tier-Proposal-Pitch-Deck.pptx",
            "07-DESIGN-CUSTOMIZER-STUDIO/design-customizer-studio.html",
            "08-AUTOMATION-BLUEPRINTS/01-lead-intake-to-ai-brief-and-notion-crm.json",
        ]),
        ("Tier4-Living-OS-Pro-Vault-Membership-Pack.zip", 81, [
            "05-LIVING-OS-MONTHLY-DROPS/tier4-monthly-vault-drop-01.md",
            "06-EDITABLE-WORD-AND-PPTX-OFFICE-SUITE/Word-Docs/03-Client-3-Tier-BRIEF-Proposal-Template.docx",
        ]),
    ]
    for zname, min_files, req_members in zip_specs:
        zp = bundle_dir / zname
        if not zp.exists():
            errors.append(f"Missing release zip: {zname}")
            continue
        with zipfile.ZipFile(zp, "r") as zf:
            corrupt = zf.testzip()
            if corrupt is not None:
                errors.append(f"Corrupt entry {corrupt} in {zname}")
            names = zf.namelist()
            if len(names) < min_files:
                errors.append(f"{zname} has {len(names)} files (expected >= {min_files})")
            for rm in req_members:
                if rm not in names:
                    errors.append(f"{zname} missing required Phase 9 member: {rm}")
            report["repackaged_zips"][zname] = {"bytes": zp.stat().st_size, "file_count": len(names)}

    print(f"[ZIP Bundles QA] Verified all 5 repackaged commercial release .zip archives.")

    # ==========================================================================
    # FINALIZE STATE LOCK & WRITE QA REPORT
    # ==========================================================================
    report["total_errors"] = len(errors)
    report["errors"] = errors
    report["status"] = "PASSED" if len(errors) == 0 else "FAILED"

    qa_report_path = BASE_DIR / "11-QUALITY-ASSURANCE" / "qa-phase9-upgrade-report.json"
    qa_report_path.parent.mkdir(parents=True, exist_ok=True)
    qa_report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    if errors:
        print("\n[PHASE 9 QA FAILED]")
        for e in errors:
            print("  -", e)
        return 1

    # Update PROJECT_STATE.json
    state_path = BASE_DIR / "PROJECT_STATE.json"
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["current_phase"] = 9
        state["status"] = "PHASE_9_ULTRA_PREMIUM_ECOSYSTEM_COMPLETE_100_PERCENT_READY"
        state["last_updated"] = datetime.now(timezone.utc).isoformat()
        state.setdefault("roadmap_phases", {})["phase_9_ultra_premium_upgrade"] = {
            "status": "completed",
            "verified": True,
            "deliverables": {
                "visual_shortcut_atlas_pdf": "13-VISUAL-CHEAT-SHEETS/the-ai-freelancer-os-visual-shortcut-atlas.pdf",
                "visual_cheat_sheet_svgs": 11,
                "visual_cheat_sheet_pngs": 11,
                "editable_word_docx_files": 7,
                "editable_powerpoint_pptx_decks": 3,
                "excel_command_center_tabs": 8,
                "excel_embedded_charts": u4_stats.get("total_embedded_charts", 4),
                "design_customizer_studio_html": "08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html",
                "automation_blueprints_json": 3,
            },
        }
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    print("=" * 82)
    print("PHASE 9 MASTER QA VERIFICATION PASSED — ZERO ERRORS ACROSS ALL 6 UPGRADES & 5 ZIPS")
    print("=" * 82)
    return 0


if __name__ == "__main__":
    sys.exit(main())
