#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 7 Automated Verification Suite (verify_phase7.py)
The AI Freelancer Operating System — Digital Knowledge Product Studio

Verifies:
1. Suite A — 5-Database Minimalist Notion Freelancer OS Import Kit (06-NOTION-TEMPLATES/)
   - 01-Leads-CRM-Pipeline.csv (>= 12 data rows)
   - 02-Active-Projects-and-Gates.csv (>= 10 data rows)
   - 03-AI-Prompt-and-Script-Vault-62.csv (exact 62 data rows: 50 Prompts + 12 Scripts)
   - 04-Weekly-CEO-Scorecard-Log.csv (>= 12 data rows)
   - 05-Client-Portal-and-Handover-Hub.md (>= 1,200 words)
   - NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md (>= 1,200 words)
2. Suite B — Multi-Tab Editable Excel (.xlsx) & CSV Financial & Pricing Matrix (06-NOTION-TEMPLATES/Spreadsheets/)
   - the-ai-freelancer-os-financial-and-pricing-matrix.xlsx (+ synced copy in 09-EXPORTS/HYBRID-BUNDLE/)
   - 4 required tabs: 01_EHR_Leak_Audit, 02_BCR_Scope_Pricing, 03_Client_80_20_Roster, 04_90Day_Pipeline_Cashflow
   - Live Excel formulas starting with '=' and 0 formula error tokens (#REF!, #DIV/0!, #VALUE!, #NAME?)
   - 4 standalone CSV sheets (sheet1..sheet4)
3. Suite C — Commercial Cover Design Suite (08-COVER-DESIGN/)
   - 6 Vector SVG covers (valid XML, >= 20 <text> nodes each)
   - 6 High-Res PNG covers (> 20 KB each, valid PNG signature)
   - kdp-paperback-full-wrap-cover.pdf (valid PDF)
   - COVER-DESIGN-AND-PACKAGING-SPEC.md (>= 600 words)
4. Strict Lexical & Anti-Placeholder Audit across all Phase 7 files
5. Updates PROJECT_STATE.json and writes 11-QUALITY-ASSURANCE/qa-phase7-report.json
"""

import csv
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent
NOTION_DIR = ROOT / "06-NOTION-TEMPLATES"
SPREADSHEETS_DIR = NOTION_DIR / "Spreadsheets"
COVERS_DIR = ROOT / "08-COVER-DESIGN"
HYBRID_BUNDLE_DIR = ROOT / "09-EXPORTS" / "HYBRID-BUNDLE"
PROJECT_STATE_PATH = ROOT / "PROJECT_STATE.json"
QA_REPORT_PATH = ROOT / "11-QUALITY-ASSURANCE" / "qa-phase7-report.json"


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def read_csv_rows(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = list(csv.reader(f))
    if not reader:
        return [], []
    return reader[0], reader[1:]


def main() -> int:
    print("=" * 78)
    print("PHASE 7 QA VERIFICATION SUITE — NOTION OS, EXCEL MATRIX & COVER SUITE")
    print("=" * 78)

    errors = []
    checks = []

    def record_check(name: str, passed: bool, details: str):
        checks.append({"check": name, "passed": passed, "details": details})
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}: {details}")
        if not passed:
            errors.append(f"{name}: {details}")

    if not PROJECT_STATE_PATH.exists():
        print("[FATAL] PROJECT_STATE.json not found.")
        return 1

    state = json.loads(PROJECT_STATE_PATH.read_text(encoding="utf-8"))
    banned_words = state["editorial_guardrails"]["banned_words"]
    banned_phrases = state["editorial_guardrails"]["banned_phrases"]

    # ==========================================================================
    # 1. SUITE A: NOTION OS KIT VERIFICATION
    # ==========================================================================
    csv_specs = [
        ("01-Leads-CRM-Pipeline.csv", 12, False),
        ("02-Active-Projects-and-Gates.csv", 10, False),
        ("03-AI-Prompt-and-Script-Vault-62.csv", 62, True),
        ("04-Weekly-CEO-Scorecard-Log.csv", 12, False),
    ]
    notion_csv_metrics = {}
    for fname, min_rows, exact_match in csv_specs:
        fpath = NOTION_DIR / fname
        if not fpath.exists():
            record_check(f"Notion CSV ({fname})", False, "File missing")
            continue
        headers, rows = read_csv_rows(fpath)
        row_cnt = len(rows)
        notion_csv_metrics[fname] = {"columns": len(headers), "rows": row_cnt, "bytes": fpath.stat().st_size}
        ok = (row_cnt == min_rows) if exact_match else (row_cnt >= min_rows)
        record_check(
            f"Notion CSV ({fname})",
            ok and len(headers) >= 8,
            f"rows={row_cnt} (req={'==' if exact_match else '>='}{min_rows}), cols={len(headers)}, size={fpath.stat().st_size:,} bytes",
        )

    portal_md = NOTION_DIR / "05-Client-Portal-and-Handover-Hub.md"
    portal_text = portal_md.read_text(encoding="utf-8") if portal_md.exists() else ""
    portal_words = count_words(portal_text)
    record_check(
        "Notion Client Portal Template (05-Client-Portal-and-Handover-Hub.md >= 1,200 words)",
        portal_md.exists() and portal_words >= 1200,
        f"words={portal_words} (min 1,200)",
    )

    guide_md = NOTION_DIR / "NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md"
    guide_text = guide_md.read_text(encoding="utf-8") if guide_md.exists() else ""
    guide_words = count_words(guide_text)
    record_check(
        "Notion Setup & Formula 2.0 Guide (NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md >= 1,200 words)",
        guide_md.exists() and guide_words >= 1200,
        f"words={guide_words} (min 1,200)",
    )

    # ==========================================================================
    # 2. SUITE B: 4-TAB EXCEL (.XLSX) & CSV FINANCIAL & PRICING MATRIX
    # ==========================================================================
    xlsx_primary = SPREADSHEETS_DIR / "the-ai-freelancer-os-financial-and-pricing-matrix.xlsx"
    xlsx_bundle = HYBRID_BUNDLE_DIR / "the-ai-freelancer-os-financial-and-pricing-matrix.xlsx"

    xlsx_exists = xlsx_primary.exists() and xlsx_bundle.exists()
    xlsx_synced = xlsx_exists and (xlsx_primary.read_bytes() == xlsx_bundle.read_bytes())
    record_check(
        "Excel Matrix Primary & Hybrid Bundle Sync",
        xlsx_exists and xlsx_synced,
        f"size={xlsx_primary.stat().st_size if xlsx_primary.exists() else 0:,} bytes, synced={xlsx_synced}",
    )

    expected_tabs = [
        "01_EHR_Leak_Audit",
        "02_BCR_Scope_Pricing",
        "03_Client_80_20_Roster",
        "04_90Day_Pipeline_Cashflow",
    ]
    formula_count = 0
    formula_errors = []
    error_tokens = {"#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A"}

    if xlsx_primary.exists():
        wb = openpyxl.load_workbook(xlsx_primary, data_only=False)
        sheet_names = wb.sheetnames
        tabs_ok = sheet_names == expected_tabs
        for sname in sheet_names:
            ws = wb[sname]
            for row in ws.iter_rows(values_only=True):
                for val in row:
                    if isinstance(val, str):
                        if val.startswith("="):
                            formula_count += 1
                        for err_tok in error_tokens:
                            if err_tok in val:
                                formula_errors.append(f"{sname}: {val}")
        record_check(
            "Excel Workbook 4 Tabs & Live Formulas Audit",
            tabs_ok and formula_count >= 35 and len(formula_errors) == 0,
            f"tabs={sheet_names}, live_formulas={formula_count}, formula_errors={len(formula_errors)}",
        )
    else:
        record_check("Excel Workbook 4 Tabs & Live Formulas Audit", False, "Workbook missing")

    standalone_sheet_csvs = [
        "sheet1-ehr-leak-audit.csv",
        "sheet2-bcr-scope-pricing.csv",
        "sheet3-client-80-20-roster.csv",
        "sheet4-90day-pipeline-cashflow.csv",
    ]
    all_sheet_csvs_ok = True
    sheet_csv_details = []
    for scsv in standalone_sheet_csvs:
        spath = SPREADSHEETS_DIR / scsv
        if not spath.exists() or spath.stat().st_size < 200:
            all_sheet_csvs_ok = False
            sheet_csv_details.append(f"{scsv}:MISSING/EMPTY")
        else:
            _, srows = read_csv_rows(spath)
            sheet_csv_details.append(f"{scsv}({len(srows)} rows)")
    record_check(
        "4 Standalone Spreadsheet CSV Mirrors",
        all_sheet_csvs_ok,
        ", ".join(sheet_csv_details),
    )

    # ==========================================================================
    # 3. SUITE C: COMMERCIAL COVER DESIGN SUITE (6 SVGs, 6 PNGs, 1 PDF, 1 SPEC)
    # ==========================================================================
    cover_stems = [
        "kdp-ebook-and-d2d-cover",
        "kdp-paperback-full-wrap-cover",
        "gumroad-tier0-free-audit-cover",
        "gumroad-tier2-workbook-edition-cover",
        "gumroad-tier3-complete-os-cover",
        "gumroad-tier4-living-os-membership-cover",
    ]
    cover_metrics = {}
    for stem in cover_stems:
        svg_p = COVERS_DIR / f"{stem}.svg"
        png_p = COVERS_DIR / f"{stem}.png"

        svg_ok = False
        text_nodes = 0
        if svg_p.exists():
            try:
                root_el = ET.fromstring(svg_p.read_text(encoding="utf-8"))
                text_nodes = sum(
                    1
                    for el in root_el.iter()
                    if el.tag.endswith("text") and (el.text or "").strip()
                )
                svg_ok = text_nodes >= 20
            except Exception as exc:
                svg_ok = False

        png_ok = False
        png_size = 0
        if png_p.exists():
            raw_b = png_p.read_bytes()
            png_size = len(raw_b)
            png_ok = png_size > 20000 and raw_b[:8] == b"\x89PNG\r\n\x1a\n"

        cover_metrics[stem] = {
            "svg_text_nodes": text_nodes,
            "svg_bytes": svg_p.stat().st_size if svg_p.exists() else 0,
            "png_bytes": png_size,
        }
        record_check(
            f"Cover SVG & PNG ({stem})",
            svg_ok and png_ok,
            f"svg_text_nodes={text_nodes} (req >=20), png_size={png_size:,} bytes (valid_png={png_ok})",
        )

    wrap_pdf = COVERS_DIR / "kdp-paperback-full-wrap-cover.pdf"
    wrap_pdf_ok = (
        wrap_pdf.exists()
        and wrap_pdf.stat().st_size > 15000
        and wrap_pdf.read_bytes()[:5] == b"%PDF-"
    )
    record_check(
        "KDP Paperback Full-Wrap Print PDF (kdp-paperback-full-wrap-cover.pdf)",
        wrap_pdf_ok,
        f"size={wrap_pdf.stat().st_size if wrap_pdf.exists() else 0:,} bytes, valid_pdf={wrap_pdf_ok}",
    )

    spec_md = COVERS_DIR / "COVER-DESIGN-AND-PACKAGING-SPEC.md"
    spec_text = spec_md.read_text(encoding="utf-8") if spec_md.exists() else ""
    spec_words = count_words(spec_text)
    record_check(
        "Cover Design & Packaging Spec (COVER-DESIGN-AND-PACKAGING-SPEC.md >= 600 words)",
        spec_md.exists() and spec_words >= 600,
        f"words={spec_words} (min 600)",
    )

    # ==========================================================================
    # 4. STRICT LEXICAL & ANTI-PLACEHOLDER AUDIT
    # ==========================================================================
    files_to_scan = [
        ROOT / "build_phase7.py",
        NOTION_DIR / "01-Leads-CRM-Pipeline.csv",
        NOTION_DIR / "02-Active-Projects-and-Gates.csv",
        NOTION_DIR / "03-AI-Prompt-and-Script-Vault-62.csv",
        NOTION_DIR / "04-Weekly-CEO-Scorecard-Log.csv",
        portal_md,
        guide_md,
        spec_md,
    ] + [COVERS_DIR / f"{s}.svg" for s in cover_stems]

    banned_violations = []
    placeholder_violations = []
    placeholder_patterns = [r"\bTODO\b", r"\bTBD\b", r"\bFIXME\b", r"Lorem Ipsum", r"\[insert text\]"]

    for fpath in files_to_scan:
        if not fpath.exists():
            continue
        content = fpath.read_text(encoding="utf-8")
        rel = str(fpath.relative_to(ROOT))
        for bw in banned_words:
            matches = re.findall(rf"\b{re.escape(bw)}(?:s|ed|ing)?\b", content, flags=re.IGNORECASE)
            if matches:
                banned_violations.append(f"{rel}: '{bw}' ({len(matches)}x)")
        for bp in banned_phrases:
            if bp.lower() in content.lower():
                banned_violations.append(f"{rel}: phrase '{bp}'")
        for pat in placeholder_patterns:
            if re.search(pat, content, flags=re.IGNORECASE):
                placeholder_violations.append(f"{rel}: pattern '{pat}'")

    record_check(
        "Strict Lexical Filter (Zero Banned AI Words & Phrases)",
        len(banned_violations) == 0,
        "0 violations" if not banned_violations else "; ".join(banned_violations),
    )

    record_check(
        "Zero Unfinished Placeholders Audit",
        len(placeholder_violations) == 0,
        "0 violations" if not placeholder_violations else "; ".join(placeholder_violations),
    )

    # ==========================================================================
    # 5. STATE LOCK & QA REPORT
    # ==========================================================================
    all_passed = len(errors) == 0

    if all_passed:
        state["roadmap_phases"]["phase_7"]["status"] = "completed"
        state["roadmap_phases"]["phase_7"]["verified"] = True
        state["compiled_deliverables_phase7"] = {
            "notion_databases": notion_csv_metrics,
            "notion_guides": {
                "05-Client-Portal-and-Handover-Hub.md": portal_words,
                "NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md": guide_words,
            },
            "excel_financial_matrix": {
                "path": "06-NOTION-TEMPLATES/Spreadsheets/the-ai-freelancer-os-financial-and-pricing-matrix.xlsx",
                "bundle_mirror": "09-EXPORTS/HYBRID-BUNDLE/the-ai-freelancer-os-financial-and-pricing-matrix.xlsx",
                "size_bytes": xlsx_primary.stat().st_size,
                "tabs": expected_tabs,
                "live_formulas": formula_count,
            },
            "covers_suite": cover_metrics,
            "paperback_wrap_pdf_bytes": wrap_pdf.stat().st_size,
            "cover_spec_words": spec_words,
        }
        PROJECT_STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        print("\n[STATE LOCK] Updated PROJECT_STATE.json -> phase_7 status='completed', verified=True")

    qa_report = {
        "phase": 7,
        "title": "5-Database Notion Freelancer OS Kit, 4-Tab Excel Pricing Matrix & 6 Commercial Covers",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "qa_gate_passed": all_passed,
        "overall_status": "PASSED" if all_passed else "FAILED",
        "metrics": {
            "notion_csv_databases": notion_csv_metrics,
            "client_portal_words": portal_words,
            "notion_setup_guide_words": guide_words,
            "excel_matrix_bytes": xlsx_primary.stat().st_size if xlsx_primary.exists() else 0,
            "excel_live_formulas": formula_count,
            "covers_verified": len(cover_stems),
            "cover_spec_words": spec_words,
            "banned_word_violations": len(banned_violations),
            "placeholder_violations": len(placeholder_violations),
        },
        "checks": checks,
        "errors": errors,
    }
    QA_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    QA_REPORT_PATH.write_text(json.dumps(qa_report, indent=2) + "\n", encoding="utf-8")
    print(f"[QA REPORT] Wrote {QA_REPORT_PATH.relative_to(ROOT)}")
    print("=" * 78)
    print(f"PHASE 7 VERIFICATION RESULT: {'PASSED (0 ERRORS)' if all_passed else f'FAILED ({len(errors)} ERRORS)'}")
    print("=" * 78)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
