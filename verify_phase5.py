#!/usr/bin/env python3
"""
Phase 5 Automated Verification & Quality Gate Suite (verify_phase5.py)
Digital Knowledge Product Studio — The AI Freelancer Operating System (v1.0.0)

Programmatically verifies all 7 compiled deliverables:
1. 09-EXPORTS/PDF/the-ai-freelancer-os-complete-book.pdf (>= 100 pages, 612x792pt, 10/10 chapters, 50/50 prompts)
2. 09-EXPORTS/PRINT/the-ai-freelancer-os-kdp-paperback-6x9.pdf (>= 120 pages, 432x648pt KDP 6x9 trim)
3. 09-EXPORTS/EPUB/the-ai-freelancer-os.epub (OCF mimetype first uncompressed, all XML/XHTML/OPF/NCX valid, 20 SVGs, 50 prompts)
4. 09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-us-letter.pdf & 05-WORKBOOKS/ copy (>= 20 pages, 612x792pt, /AcroForm)
5. 09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-a4.pdf & 05-WORKBOOKS/ copy (>= 20 pages, ~595x842pt, /AcroForm)
6. 09-EXPORTS/PDF/the-ai-freelancer-os-tablet-planner.pdf & 05-WORKBOOKS/ copy (>= 20 pages, 792x612pt Landscape)
7. 09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf (>= 12 pages) + chapter-01-workbook.pdf (>= 2 pages)
Updates PROJECT_STATE.json and writes 11-QUALITY-ASSURANCE/qa-phase5-report.json.
"""

import json
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parent


def inspect_pdf(
    rel_path: str,
    min_pages: int,
    expected_w_pt: float,
    expected_h_pt: float,
    tolerance_pt: float = 5.0,
    extract_full_text: bool = False,
    require_acroform: bool = False,
) -> tuple[dict, str, list[str]]:
    """Inspect a PDF file for header validity, page count, MediaBox dimensions, metadata, and optional text."""
    errors = []
    abs_path = BASE_DIR / rel_path
    if not abs_path.exists():
        return (
            {"path": rel_path, "exists": False, "passed": False},
            "",
            [f"Missing required PDF deliverable: {rel_path}"],
        )

    size_bytes = abs_path.stat().st_size
    if size_bytes == 0:
        return (
            {"path": rel_path, "exists": True, "size_bytes": 0, "passed": False},
            "",
            [f"Empty PDF file (0 bytes): {rel_path}"],
        )

    with open(abs_path, "rb") as f_in:
        header = f_in.read(5)
    if header != b"%PDF-":
        errors.append(f"{rel_path}: Invalid PDF magic header {header!r}")

    reader = PdfReader(str(abs_path))
    num_pages = len(reader.pages)
    if num_pages < min_pages:
        errors.append(f"{rel_path}: Page count {num_pages} is below required floor ({min_pages} pages)")

    first_box = reader.pages[0].mediabox
    w_pt = float(first_box.width)
    h_pt = float(first_box.height)
    if abs(w_pt - expected_w_pt) > tolerance_pt or abs(h_pt - expected_h_pt) > tolerance_pt:
        errors.append(
            f"{rel_path}: MediaBox ({w_pt:.1f}pt x {h_pt:.1f}pt) does not match expected "
            f"({expected_w_pt:.1f}pt x {expected_h_pt:.1f}pt ± {tolerance_pt}pt)"
        )

    has_acroform = "/AcroForm" in reader.trailer.get("/Root", {})
    if require_acroform and not has_acroform:
        errors.append(f"{rel_path}: Missing /AcroForm interactive dictionary in PDF root catalog")

    full_text = ""
    if extract_full_text:
        text_parts = []
        for page in reader.pages:
            text_parts.append(page.extract_text() or "")
        full_text = "\n".join(text_parts)

    info = {
        "path": rel_path,
        "exists": True,
        "size_bytes": size_bytes,
        "size_kb": round(size_bytes / 1024, 1),
        "size_mb": round(size_bytes / (1024 * 1024), 2),
        "page_count": num_pages,
        "min_pages_required": min_pages,
        "dimensions_pt": f"{w_pt:.1f}pt x {h_pt:.1f}pt",
        "dimensions_in": f"{w_pt / 72.0:.2f}in x {h_pt / 72.0:.2f}in",
        "pdf_header_valid": header == b"%PDF-",
        "acroform_initialized": has_acroform,
        "passed": len(errors) == 0,
    }
    return info, full_text, errors


def inspect_epub(rel_path: str) -> tuple[dict, list[str]]:
    """Verify OCF EPUB 3.0 structure, uncompressed mimetype, XML well-formedness, 20 SVGs, and 50 prompts."""
    errors = []
    abs_path = BASE_DIR / rel_path
    if not abs_path.exists():
        return (
            {"path": rel_path, "exists": False, "passed": False},
            [f"Missing EPUB deliverable: {rel_path}"],
        )

    size_bytes = abs_path.stat().st_size
    if not zipfile.is_zipfile(abs_path):
        return (
            {"path": rel_path, "exists": True, "size_bytes": size_bytes, "passed": False},
            [f"{rel_path}: Not a valid ZIP archive"],
        )

    xml_files_checked = 0
    xml_syntax_errors = 0
    combined_xhtml_text = []

    with zipfile.ZipFile(abs_path, "r") as zf:
        infolist = zf.infolist()
        namelist = zf.namelist()

        # 1. Check mimetype is first entry and uncompressed
        if not infolist or infolist[0].filename != "mimetype":
            errors.append(f"{rel_path}: First entry in ZIP must be 'mimetype', found {infolist[0].filename if infolist else 'empty'}")
        else:
            if infolist[0].compress_type != zipfile.ZIP_STORED:
                errors.append(f"{rel_path}: 'mimetype' entry must use ZIP_STORED (0), found {infolist[0].compress_type}")
            mime_bytes = zf.read("mimetype")
            if mime_bytes != b"application/epub+zip":
                errors.append(f"{rel_path}: 'mimetype' content invalid: {mime_bytes!r}")

        # 2. Check required core files
        required_entries = [
            "META-INF/container.xml",
            "OEBPS/content.opf",
            "OEBPS/nav.xhtml",
            "OEBPS/toc.ncx",
            "OEBPS/styles.css",
            "OEBPS/front-matter.xhtml",
            "OEBPS/toc.xhtml",
            "OEBPS/back-matter.xhtml",
        ]
        for n in range(1, 11):
            required_entries.append(f"OEBPS/chapter-{n:02d}.xhtml")
            required_entries.append(f"OEBPS/chapter-{n:02d}-mindmap.svg")
            required_entries.append(f"OEBPS/chapter-{n:02d}-flowchart.svg")

        for req in required_entries:
            if req not in namelist:
                errors.append(f"{rel_path}: Missing required OCF entry '{req}'")

        # 3. Parse every .xhtml, .opf, .ncx, .xml, and .svg file via xml.etree.ElementTree.fromstring
        for entry_name in namelist:
            if entry_name.endswith((".xhtml", ".opf", ".ncx", ".xml", ".svg")):
                xml_files_checked += 1
                raw_bytes = zf.read(entry_name)
                try:
                    ET.fromstring(raw_bytes)
                except Exception as exc:
                    xml_syntax_errors += 1
                    errors.append(f"{rel_path} -> {entry_name}: XML syntax error: {exc}")
                if entry_name.endswith(".xhtml"):
                    combined_xhtml_text.append(raw_bytes.decode("utf-8", errors="replace"))

    full_epub_text = "\n".join(combined_xhtml_text)
    chapters_found = 0
    for n in range(1, 11):
        if f"Chapter {n}:" in full_epub_text:
            chapters_found += 1
        else:
            errors.append(f"{rel_path}: Missing 'Chapter {n}:' heading in EPUB XHTML spine")

    prompts_found = 0
    for ch in range(1, 11):
        for p in range(1, 6):
            pid = f"Prompt {ch}.{p}"
            if pid in full_epub_text:
                prompts_found += 1
            else:
                errors.append(f"{rel_path}: Missing '{pid}' in EPUB XHTML spine")

    info = {
        "path": rel_path,
        "exists": True,
        "size_bytes": size_bytes,
        "size_kb": round(size_bytes / 1024, 1),
        "mimetype_first_and_uncompressed": len(infolist) > 0
        and infolist[0].filename == "mimetype"
        and infolist[0].compress_type == zipfile.ZIP_STORED,
        "xhtml_documents_count": 13,  # front-matter, toc, 10 chapters, back-matter (+ nav.xhtml = 14)
        "embedded_svg_diagrams_count": 20,
        "xml_files_parsed": xml_files_checked,
        "xml_syntax_errors": xml_syntax_errors,
        "chapters_verified": f"{chapters_found}/10",
        "prompts_verified": f"{prompts_found}/50",
        "passed": len(errors) == 0,
    }
    return info, errors


def main() -> int:
    errors: list[str] = []
    deliverables_audit: dict = {}

    # 1. Full Digital Book PDF (US Letter 612pt x 792pt, >= 100 pages)
    d1_info, d1_text, d1_errs = inspect_pdf(
        "09-EXPORTS/PDF/the-ai-freelancer-os-complete-book.pdf",
        min_pages=100,
        expected_w_pt=612.0,
        expected_h_pt=792.0,
        extract_full_text=True,
    )
    errors.extend(d1_errs)

    # Check all 10 chapters and all 50 prompts in Full Book PDF text
    pdf_chapters_found = 0
    for n in range(1, 11):
        if f"Chapter {n}:" in d1_text:
            pdf_chapters_found += 1
        else:
            errors.append(f"Full Book PDF missing 'Chapter {n}:'")

    pdf_prompts_found = 0
    for ch in range(1, 11):
        for p in range(1, 6):
            pid = f"Prompt {ch}.{p}"
            if pid in d1_text:
                pdf_prompts_found += 1
            else:
                errors.append(f"Full Book PDF missing '{pid}'")

    d1_info["chapters_verified"] = f"{pdf_chapters_found}/10"
    d1_info["prompts_verified"] = f"{pdf_prompts_found}/50"
    d1_info["passed"] = d1_info["passed"] and pdf_chapters_found == 10 and pdf_prompts_found == 50
    deliverables_audit["complete_book_pdf"] = d1_info

    # 2. Amazon KDP 6" x 9" Print-Ready Paperback Interior PDF (432pt x 648pt, >= 120 pages)
    d2_info, _, d2_errs = inspect_pdf(
        "09-EXPORTS/PRINT/the-ai-freelancer-os-kdp-paperback-6x9.pdf",
        min_pages=120,
        expected_w_pt=432.0,
        expected_h_pt=648.0,
    )
    errors.extend(d2_errs)
    deliverables_audit["kdp_paperback_6x9_pdf"] = d2_info

    # 3. Reflowable EPUB 3.0 eBook
    d3_info, d3_errs = inspect_epub("09-EXPORTS/EPUB/the-ai-freelancer-os.epub")
    errors.extend(d3_errs)
    deliverables_audit["reflowable_epub3"] = d3_info

    # 4. US Letter 10-Chapter Workbook PDF (612pt x 792pt, >= 20 pages) + 05-WORKBOOKS copy
    d4_info, _, d4_errs = inspect_pdf(
        "09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-us-letter.pdf",
        min_pages=20,
        expected_w_pt=612.0,
        expected_h_pt=792.0,
        require_acroform=True,
    )
    d4_copy_info, _, d4_copy_errs = inspect_pdf(
        "05-WORKBOOKS/the-ai-freelancer-os-workbook-us-letter.pdf",
        min_pages=20,
        expected_w_pt=612.0,
        expected_h_pt=792.0,
        require_acroform=True,
    )
    errors.extend(d4_errs)
    errors.extend(d4_copy_errs)
    d4_info["synced_workbook_copy"] = d4_copy_info["path"]
    d4_info["synced_copy_verified"] = d4_copy_info["passed"]
    deliverables_audit["workbook_us_letter_pdf"] = d4_info

    # 5. ISO A4 10-Chapter Workbook PDF (~595.3pt x 841.9pt, >= 20 pages) + 05-WORKBOOKS copy
    d5_info, _, d5_errs = inspect_pdf(
        "09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-a4.pdf",
        min_pages=20,
        expected_w_pt=595.0,
        expected_h_pt=842.0,
        tolerance_pt=6.0,
        require_acroform=True,
    )
    d5_copy_info, _, d5_copy_errs = inspect_pdf(
        "05-WORKBOOKS/the-ai-freelancer-os-workbook-a4.pdf",
        min_pages=20,
        expected_w_pt=595.0,
        expected_h_pt=842.0,
        tolerance_pt=6.0,
        require_acroform=True,
    )
    errors.extend(d5_errs)
    errors.extend(d5_copy_errs)
    d5_info["synced_workbook_copy"] = d5_copy_info["path"]
    d5_info["synced_copy_verified"] = d5_copy_info["passed"]
    deliverables_audit["workbook_a4_pdf"] = d5_info

    # 6. Hyperlinked Landscape Tablet Digital Planner (792pt x 612pt, >= 20 pages) + 05-WORKBOOKS copy
    d6_info, _, d6_errs = inspect_pdf(
        "09-EXPORTS/PDF/the-ai-freelancer-os-tablet-planner.pdf",
        min_pages=20,
        expected_w_pt=792.0,
        expected_h_pt=612.0,
        require_acroform=True,
    )
    d6_copy_info, _, d6_copy_errs = inspect_pdf(
        "05-WORKBOOKS/the-ai-freelancer-os-tablet-planner.pdf",
        min_pages=20,
        expected_w_pt=792.0,
        expected_h_pt=612.0,
        require_acroform=True,
    )
    errors.extend(d6_errs)
    errors.extend(d6_copy_errs)
    d6_info["synced_workbook_copy"] = d6_copy_info["path"]
    d6_info["synced_copy_verified"] = d6_copy_info["passed"]
    deliverables_audit["tablet_planner_landscape_pdf"] = d6_info

    # 7. Tier-0 Free Sample Bundle PDF (>= 12 pages) + Standalone Chapter 1 Workbook PDF (>= 2 pages)
    d7a_info, _, d7a_errs = inspect_pdf(
        "09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf",
        min_pages=12,
        expected_w_pt=612.0,
        expected_h_pt=792.0,
    )
    d7b_info, _, d7b_errs = inspect_pdf(
        "05-WORKBOOKS/chapter-01-workbook.pdf",
        min_pages=2,
        expected_w_pt=612.0,
        expected_h_pt=792.0,
        require_acroform=True,
    )
    d7b_export_info, _, d7b_export_errs = inspect_pdf(
        "09-EXPORTS/PRINT/chapter-01-workbook.pdf",
        min_pages=2,
        expected_w_pt=612.0,
        expected_h_pt=792.0,
        require_acroform=True,
    )
    errors.extend(d7a_errs)
    errors.extend(d7b_errs)
    errors.extend(d7b_export_errs)
    deliverables_audit["tier0_lead_magnet_sample_pdf"] = d7a_info
    deliverables_audit["chapter_01_standalone_workbook_pdf"] = {
        **d7b_info,
        "synced_export_copy": d7b_export_info["path"],
        "synced_export_verified": d7b_export_info["passed"],
    }

    qa_gate_passed = len(errors) == 0

    # Update PROJECT_STATE.json if QA gate passed
    state_path = BASE_DIR / "PROJECT_STATE.json"
    if state_path.exists():
        state_data = json.loads(state_path.read_text(encoding="utf-8"))
        if qa_gate_passed:
            state_data["roadmap_phases"]["phase_5"]["status"] = "completed"
            state_data["roadmap_phases"]["phase_5"]["verified"] = True
            state_data["compiled_deliverables_phase5"] = {
                "complete_book_pdf": {
                    "path": d1_info["path"],
                    "pages": d1_info["page_count"],
                    "size_kb": d1_info["size_kb"],
                },
                "kdp_paperback_6x9_pdf": {
                    "path": d2_info["path"],
                    "pages": d2_info["page_count"],
                    "size_kb": d2_info["size_kb"],
                },
                "reflowable_epub3": {
                    "path": d3_info["path"],
                    "xhtml_files": d3_info["xhtml_documents_count"],
                    "svg_diagrams": d3_info["embedded_svg_diagrams_count"],
                    "size_kb": d3_info["size_kb"],
                },
                "workbook_us_letter_pdf": {
                    "path": d4_info["path"],
                    "pages": d4_info["page_count"],
                    "size_kb": d4_info["size_kb"],
                },
                "workbook_a4_pdf": {
                    "path": d5_info["path"],
                    "pages": d5_info["page_count"],
                    "size_kb": d5_info["size_kb"],
                },
                "tablet_planner_landscape_pdf": {
                    "path": d6_info["path"],
                    "pages": d6_info["page_count"],
                    "size_kb": d6_info["size_kb"],
                },
                "tier0_lead_magnet_sample_pdf": {
                    "path": d7a_info["path"],
                    "pages": d7a_info["page_count"],
                    "size_kb": d7a_info["size_kb"],
                },
                "chapter_01_standalone_workbook_pdf": {
                    "path": d7b_info["path"],
                    "pages": d7b_info["page_count"],
                    "size_kb": d7b_info["size_kb"],
                },
            }
            state_path.write_text(json.dumps(state_data, indent=2) + "\n", encoding="utf-8")
    else:
        errors.append("Missing PROJECT_STATE.json")
        qa_gate_passed = False

    report = {
        "phase": "Phase 5 — Single-Source Multi-Format Compiler (build.py — 7 Commercial Book, Print, EPUB & Workbook Editions)",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "qa_gate_passed": qa_gate_passed,
        "summary": {
            "deliverables_verified": "7/7" if qa_gate_passed else "FAIL",
            "complete_book_pdf_pages": d1_info.get("page_count", 0),
            "kdp_6x9_paperback_pages": d2_info.get("page_count", 0),
            "epub3_xml_syntax_errors": d3_info.get("xml_syntax_errors", -1),
            "workbook_us_letter_pages": d4_info.get("page_count", 0),
            "workbook_a4_pages": d5_info.get("page_count", 0),
            "tablet_planner_pages": d6_info.get("page_count", 0),
            "tier0_sample_pages": d7a_info.get("page_count", 0),
            "chapter_01_workbook_pages": d7b_info.get("page_count", 0),
            "chapters_in_book_and_epub": f"{pdf_chapters_found}/10",
            "prompts_in_book_and_epub": f"{pdf_prompts_found}/50",
        },
        "deliverables_audit": deliverables_audit,
        "errors": errors,
    }

    report_path = BASE_DIR / "11-QUALITY-ASSURANCE/qa-phase5-report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if qa_gate_passed else 1


if __name__ == "__main__":
    sys.exit(main())
