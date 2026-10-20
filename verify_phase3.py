#!/usr/bin/env python3
"""
Phase 3 Automated Quality Assurance & Verification Engine (verify_phase3.py)
Digital Knowledge Product Studio — The AI Freelancer Operating System
Verifies Chapters 1 through 7 manuscripts, 14 SVG diagrams, 7 standalone worksheets, and PROJECT_STATE.json.
"""

import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

CHAPTER_NUMBERS = [1, 2, 3, 4, 5, 6, 7]

REQUIRED_SECTION_TEMPLATES = [
    "# Chapter {n}:",
    "## 1. Learning Objectives",
    "## 2. The Real-World Friction Point",
    "## 3. Why Standard Approaches Fail",
    "## 4. Core Framework:",
    "### Visual Architecture: System Mindmap",
    "## 5. Step-by-Step Implementation Protocol",
    "### Operational Decision Tree",
    "## 6. Tested AI Workflow Prompts",
    "## 7. Real-World Implementation Case Study",
    "## 8. Common Operational Pitfalls & Fixes",
    "## 9. Chapter Action Worksheet",
    "## 10. Executive Summary & Implementation Checklist",
    "## 11. Sources & Operational References",
]

REQUIRED_WORKSHEET_PARTS = [
    "## Part A:",
    "## Part B:",
    "## Part C:",
    "## Part D:",
    "## Part E:",
]

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

PLACEHOLDER_TOKENS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"Lorem Ipsum",
    r"\[insert text\]",
    r"\[insert content here\]",
    r"\.\.\.rest of chapter omitted\.\.\.",
]


def check_lexical_and_placeholders(text: str, file_label: str, errors: list) -> dict:
    banned_word_hits = []
    banned_phrase_hits = []
    placeholder_hits = []

    for bw in BANNED_WORDS:
        pattern = re.compile(rf"\b{re.escape(bw)}(?:s|d|ed|ing)?\b", re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            banned_word_hits.append({"word": bw, "count": len(matches)})
            errors.append(f"{file_label} contains banned AI word '{bw}' ({len(matches)} occurrences).")

    for bp in BANNED_PHRASES:
        pattern = re.compile(re.escape(bp), re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            banned_phrase_hits.append({"phrase": bp, "count": len(matches)})
            errors.append(f"{file_label} contains banned AI phrase '{bp}' ({len(matches)} occurrences).")

    for ph in PLACEHOLDER_TOKENS:
        matches = re.findall(ph, text, flags=re.IGNORECASE)
        if matches:
            placeholder_hits.append({"pattern": ph, "count": len(matches)})
            errors.append(f"{file_label} contains placeholder token '{ph}'.")

    return {
        "banned_words_count": sum(item["count"] for item in banned_word_hits),
        "banned_phrases_count": sum(item["count"] for item in banned_phrase_hits),
        "placeholder_tokens_count": sum(item["count"] for item in placeholder_hits),
        "banned_word_details": banned_word_hits,
        "banned_phrase_details": banned_phrase_hits,
        "placeholder_details": placeholder_hits,
    }


def check_chapter(n: int, errors: list) -> dict:
    rel_path = f"03-MANUSCRIPT/Chapters/chapter-0{n}.md"
    ch_path = BASE_DIR / rel_path
    result = {
        "chapter": n,
        "file": rel_path,
        "exists": ch_path.is_file(),
        "word_count": 0,
        "min_word_count_required": 3800,
        "required_14_sections_verified": "Fail",
        "sections_found": "0/14",
        "missing_sections": [],
        "tested_ai_prompts_verified": "0/5",
        "missing_prompts": [],
        "mindmap_link_present": False,
        "flowchart_link_present": False,
        "lexical_audit": {},
        "passed": False,
    }

    if not ch_path.is_file():
        errors.append(f"Missing required chapter file: {rel_path}")
        return result

    text = ch_path.read_text(encoding="utf-8")
    word_count = len(text.split())
    result["word_count"] = word_count
    if word_count < 3800:
        errors.append(f"{rel_path} word count ({word_count}) is below minimum 3,800 words.")

    missing_sections = []
    for tmpl in REQUIRED_SECTION_TEMPLATES:
        sec = tmpl.format(n=n)
        if sec not in text:
            missing_sections.append(sec)
            errors.append(f"{rel_path} missing required section heading: {sec}")
    result["missing_sections"] = missing_sections
    result["sections_found"] = f"{14 - len(missing_sections)}/14"
    result["required_14_sections_verified"] = "Pass" if len(missing_sections) == 0 else "Fail"

    missing_prompts = []
    for p_idx in range(1, 6):
        pr_heading = f"### Prompt {n}.{p_idx}:"
        if pr_heading not in text:
            missing_prompts.append(pr_heading)
            errors.append(f"{rel_path} missing required prompt heading: {pr_heading}")
    result["missing_prompts"] = missing_prompts
    result["tested_ai_prompts_verified"] = f"{5 - len(missing_prompts)}/5"

    mindmap_ref = f"../../04-VISUAL-ASSETS/Mindmaps/chapter-0{n}-mindmap.svg"
    flowchart_ref = f"../../04-VISUAL-ASSETS/Flowcharts/chapter-0{n}-flowchart.svg"
    result["mindmap_link_present"] = mindmap_ref in text
    result["flowchart_link_present"] = flowchart_ref in text
    if not result["mindmap_link_present"]:
        errors.append(f"{rel_path} missing embedded mindmap link: {mindmap_ref}")
    if not result["flowchart_link_present"]:
        errors.append(f"{rel_path} missing embedded flowchart link: {flowchart_ref}")

    lex = check_lexical_and_placeholders(text, rel_path, errors)
    result["lexical_audit"] = lex

    result["passed"] = (
        word_count >= 3800
        and len(missing_sections) == 0
        and len(missing_prompts) == 0
        and result["mindmap_link_present"]
        and result["flowchart_link_present"]
        and lex["banned_words_count"] == 0
        and lex["banned_phrases_count"] == 0
        and lex["placeholder_tokens_count"] == 0
    )
    return result


def check_svg(svg_rel: str, errors: list) -> dict:
    svg_path = BASE_DIR / svg_rel
    result = {
        "file": svg_rel,
        "exists": svg_path.is_file(),
        "xml_valid": False,
        "non_empty_text_nodes": 0,
        "min_required_text_nodes": 15,
        "passed": False,
        "error": None,
    }
    if not svg_path.is_file():
        result["error"] = "File does not exist"
        errors.append(f"Missing SVG file: {svg_rel}")
        return result

    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()
        result["xml_valid"] = True
        text_nodes = []
        for elem in root.iter():
            tag_name = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            if tag_name == "text":
                content = "".join(elem.itertext()).strip()
                if content:
                    text_nodes.append(content)
        result["non_empty_text_nodes"] = len(text_nodes)
        result["passed"] = result["xml_valid"] and len(text_nodes) >= 15
        if not result["passed"]:
            errors.append(f"{svg_rel} has only {len(text_nodes)} non-empty <text> nodes (min 15 required).")
    except Exception as exc:
        result["error"] = str(exc)
        errors.append(f"{svg_rel} XML parse error: {exc}")

    return result


def check_worksheet(n: int, errors: list) -> dict:
    rel_path = f"05-WORKBOOKS/worksheet-0{n}.md"
    ws_path = BASE_DIR / rel_path
    result = {
        "worksheet": n,
        "file": rel_path,
        "exists": ws_path.is_file(),
        "word_count": 0,
        "parts_verified": "0/5",
        "missing_parts": [],
        "lexical_audit": {},
        "passed": False,
    }
    if not ws_path.is_file():
        errors.append(f"Missing required worksheet: {rel_path}")
        return result

    text = ws_path.read_text(encoding="utf-8")
    result["word_count"] = len(text.split())
    missing_parts = []
    for part in REQUIRED_WORKSHEET_PARTS:
        if part not in text:
            missing_parts.append(part)
            errors.append(f"{rel_path} missing required worksheet section: {part}")
    result["missing_parts"] = missing_parts
    result["parts_verified"] = f"{5 - len(missing_parts)}/5"

    lex = check_lexical_and_placeholders(text, rel_path, errors)
    result["lexical_audit"] = lex
    result["passed"] = (
        len(missing_parts) == 0
        and lex["banned_words_count"] == 0
        and lex["banned_phrases_count"] == 0
        and lex["placeholder_tokens_count"] == 0
    )
    return result


def main() -> int:
    errors = []

    # 1. Verify Chapters 1-7
    chapters_audit = {}
    total_word_count = 0
    total_prompts_verified = 0
    total_banned_words = 0
    total_banned_phrases = 0
    total_placeholders = 0

    for n in CHAPTER_NUMBERS:
        ch_res = check_chapter(n, errors)
        chapters_audit[f"chapter_0{n}"] = ch_res
        total_word_count += ch_res["word_count"]
        total_prompts_verified += 5 - len(ch_res["missing_prompts"])
        if ch_res["lexical_audit"]:
            total_banned_words += ch_res["lexical_audit"]["banned_words_count"]
            total_banned_phrases += ch_res["lexical_audit"]["banned_phrases_count"]
            total_placeholders += ch_res["lexical_audit"]["placeholder_tokens_count"]

    # 2. Verify all 14 SVG diagrams
    svg_audit = {}
    for n in CHAPTER_NUMBERS:
        mm_rel = f"04-VISUAL-ASSETS/Mindmaps/chapter-0{n}-mindmap.svg"
        fc_rel = f"04-VISUAL-ASSETS/Flowcharts/chapter-0{n}-flowchart.svg"
        svg_audit[f"chapter_0{n}_mindmap_svg"] = check_svg(mm_rel, errors)
        svg_audit[f"chapter_0{n}_flowchart_svg"] = check_svg(fc_rel, errors)

    # 3. Verify Worksheets 1-7
    worksheets_audit = {}
    for n in CHAPTER_NUMBERS:
        ws_res = check_worksheet(n, errors)
        worksheets_audit[f"worksheet_0{n}"] = ws_res
        if ws_res["lexical_audit"]:
            total_banned_words += ws_res["lexical_audit"]["banned_words_count"]
            total_banned_phrases += ws_res["lexical_audit"]["banned_phrases_count"]
            total_placeholders += ws_res["lexical_audit"]["placeholder_tokens_count"]

    # 4. Verify PROJECT_STATE.json
    state_path = BASE_DIR / "PROJECT_STATE.json"
    project_state_valid = False
    if state_path.is_file():
        try:
            state_data = json.loads(state_path.read_text(encoding="utf-8"))
            p3 = state_data.get("roadmap_phases", {}).get("phase_3", {})
            p3_ok = p3 == "completed" or (isinstance(p3, dict) and p3.get("status") == "completed")
            expected_chapters = [
                "chapter-01",
                "chapter-02",
                "chapter-03",
                "chapter-04",
                "chapter-05",
                "chapter-06",
                "chapter-07",
            ]
            ch_ok = state_data.get("chapters_completed") == expected_chapters
            if p3_ok and ch_ok:
                project_state_valid = True
            else:
                errors.append(
                    "PROJECT_STATE.json does not have phase_3 marked completed or chapters_completed = ['chapter-01'..'chapter-07']."
                )
        except Exception as exc:
            errors.append(f"PROJECT_STATE.json invalid JSON: {exc}")
    else:
        errors.append("Missing PROJECT_STATE.json")

    qa_gate_passed = len(errors) == 0

    report = {
        "phase": "Phase 3 — Part III & IV Manuscripts, Vector Diagrams & Worksheets (Chapters 5, 6 & 7)",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "qa_gate_passed": qa_gate_passed,
        "cumulative_summary": {
            "chapters_verified": "7/7" if all(c["passed"] for c in chapters_audit.values()) else "Fail",
            "cumulative_manuscript_word_count_ch1_to_ch7": total_word_count,
            "tested_ai_prompts_verified": f"{total_prompts_verified}/35",
            "svg_diagrams_verified": f"{sum(1 for s in svg_audit.values() if s['passed'])}/14",
            "worksheets_verified": f"{sum(1 for w in worksheets_audit.values() if w['passed'])}/7",
            "banned_ai_words_count": total_banned_words,
            "banned_ai_phrases_count": total_banned_phrases,
            "placeholder_tokens_count": total_placeholders,
            "project_state_locked": project_state_valid,
        },
        "chapters_audit": chapters_audit,
        "svg_visual_assets_audit": svg_audit,
        "worksheets_audit": worksheets_audit,
        "errors": errors,
    }

    report_path = BASE_DIR / "11-QUALITY-ASSURANCE/qa-phase3-report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if qa_gate_passed else 1


if __name__ == "__main__":
    sys.exit(main())
