#!/usr/bin/env python3
"""
Phase 4 Automated Quality Assurance & Verification Engine (verify_phase4.py)
Digital Knowledge Product Studio — The AI Freelancer Operating System
Verifies all 10 Chapters (1-10), Front Matter, Back Matter Vault (50 Prompt Index + 12 Emergency Scripts),
20 Vector SVG Diagrams, 10 Standalone Worksheets, and PROJECT_STATE.json.
"""

import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

CHAPTER_NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

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
    ch_tag = f"{n:02d}"
    rel_path = f"03-MANUSCRIPT/Chapters/chapter-{ch_tag}.md"
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

    mindmap_ref = f"../../04-VISUAL-ASSETS/Mindmaps/chapter-{ch_tag}-mindmap.svg"
    flowchart_ref = f"../../04-VISUAL-ASSETS/Flowcharts/chapter-{ch_tag}-flowchart.svg"
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


def check_front_matter(errors: list) -> dict:
    rel_path = "03-MANUSCRIPT/Front-Matter/front-matter.md"
    fm_path = BASE_DIR / rel_path
    result = {
        "file": rel_path,
        "exists": fm_path.is_file(),
        "word_count": 0,
        "min_word_count_required": 1800,
        "lexical_audit": {},
        "passed": False,
    }
    if not fm_path.is_file():
        errors.append(f"Missing required Front Matter file: {rel_path}")
        return result

    text = fm_path.read_text(encoding="utf-8")
    word_count = len(text.split())
    result["word_count"] = word_count
    if word_count < 1800:
        errors.append(f"{rel_path} word count ({word_count}) is below minimum 1,800 words.")

    lex = check_lexical_and_placeholders(text, rel_path, errors)
    result["lexical_audit"] = lex
    result["passed"] = (
        word_count >= 1800
        and lex["banned_words_count"] == 0
        and lex["banned_phrases_count"] == 0
        and lex["placeholder_tokens_count"] == 0
    )
    return result


def check_back_matter(errors: list) -> dict:
    rel_path = "03-MANUSCRIPT/Back-Matter/back-matter.md"
    bm_path = BASE_DIR / rel_path
    result = {
        "file": rel_path,
        "exists": bm_path.is_file(),
        "word_count": 0,
        "min_word_count_required": 2500,
        "indexed_prompts_verified": "0/50",
        "emergency_scripts_verified": "0/12",
        "lexical_audit": {},
        "passed": False,
    }
    if not bm_path.is_file():
        errors.append(f"Missing required Back Matter file: {rel_path}")
        return result

    text = bm_path.read_text(encoding="utf-8")
    word_count = len(text.split())
    result["word_count"] = word_count
    if word_count < 2500:
        errors.append(f"{rel_path} word count ({word_count}) is below minimum 2,500 words.")

    missing_indexed = []
    for n in CHAPTER_NUMBERS:
        for p_idx in range(1, 6):
            token = f"Prompt {n}.{p_idx}"
            if token not in text:
                missing_indexed.append(token)
                errors.append(f"{rel_path} missing indexed prompt reference: {token}")
    result["indexed_prompts_verified"] = f"{50 - len(missing_indexed)}/50"

    missing_scripts = []
    for s_idx in range(1, 13):
        s_token = f"### Script {s_idx}:"
        if s_token not in text:
            missing_scripts.append(s_token)
            errors.append(f"{rel_path} missing required emergency script heading: {s_token}")
    result["emergency_scripts_verified"] = f"{12 - len(missing_scripts)}/12"

    lex = check_lexical_and_placeholders(text, rel_path, errors)
    result["lexical_audit"] = lex
    result["passed"] = (
        word_count >= 2500
        and len(missing_indexed) == 0
        and len(missing_scripts) == 0
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
        "lexical_audit": {},
        "passed": False,
        "error": None,
    }
    if not svg_path.is_file():
        result["error"] = "File does not exist"
        errors.append(f"Missing SVG file: {svg_rel}")
        return result

    raw_svg_text = svg_path.read_text(encoding="utf-8")
    lex = check_lexical_and_placeholders(raw_svg_text, svg_rel, errors)
    result["lexical_audit"] = lex

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
        result["passed"] = (
            result["xml_valid"]
            and len(text_nodes) >= 15
            and lex["banned_words_count"] == 0
            and lex["banned_phrases_count"] == 0
            and lex["placeholder_tokens_count"] == 0
        )
        if len(text_nodes) < 15:
            errors.append(f"{svg_rel} has only {len(text_nodes)} non-empty <text> nodes (min 15 required).")
    except Exception as exc:
        result["error"] = str(exc)
        errors.append(f"{svg_rel} XML parse error: {exc}")

    return result


def check_worksheet(n: int, errors: list) -> dict:
    ws_tag = f"{n:02d}"
    rel_path = f"05-WORKBOOKS/worksheet-{ws_tag}.md"
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

    # 1. Verify Front Matter & Back Matter
    front_matter_audit = check_front_matter(errors)
    back_matter_audit = check_back_matter(errors)

    total_banned_words = (
        front_matter_audit.get("lexical_audit", {}).get("banned_words_count", 0)
        + back_matter_audit.get("lexical_audit", {}).get("banned_words_count", 0)
    )
    total_banned_phrases = (
        front_matter_audit.get("lexical_audit", {}).get("banned_phrases_count", 0)
        + back_matter_audit.get("lexical_audit", {}).get("banned_phrases_count", 0)
    )
    total_placeholders = (
        front_matter_audit.get("lexical_audit", {}).get("placeholder_tokens_count", 0)
        + back_matter_audit.get("lexical_audit", {}).get("placeholder_tokens_count", 0)
    )

    # 2. Verify Chapters 1-10
    chapters_audit = {}
    total_chapter_words = 0
    total_prompts_verified = 0

    for n in CHAPTER_NUMBERS:
        ch_tag = f"{n:02d}"
        ch_res = check_chapter(n, errors)
        chapters_audit[f"chapter_{ch_tag}"] = ch_res
        total_chapter_words += ch_res["word_count"]
        total_prompts_verified += 5 - len(ch_res["missing_prompts"])
        if ch_res["lexical_audit"]:
            total_banned_words += ch_res["lexical_audit"]["banned_words_count"]
            total_banned_phrases += ch_res["lexical_audit"]["banned_phrases_count"]
            total_placeholders += ch_res["lexical_audit"]["placeholder_tokens_count"]

    total_manuscript_words = (
        front_matter_audit["word_count"]
        + total_chapter_words
        + back_matter_audit["word_count"]
    )

    # 3. Verify all 20 SVG diagrams
    svg_audit = {}
    for n in CHAPTER_NUMBERS:
        ch_tag = f"{n:02d}"
        mm_rel = f"04-VISUAL-ASSETS/Mindmaps/chapter-{ch_tag}-mindmap.svg"
        fc_rel = f"04-VISUAL-ASSETS/Flowcharts/chapter-{ch_tag}-flowchart.svg"
        mm_res = check_svg(mm_rel, errors)
        fc_res = check_svg(fc_rel, errors)
        svg_audit[f"chapter_{ch_tag}_mindmap_svg"] = mm_res
        svg_audit[f"chapter_{ch_tag}_flowchart_svg"] = fc_res
        if mm_res["lexical_audit"]:
            total_banned_words += mm_res["lexical_audit"]["banned_words_count"]
            total_banned_phrases += mm_res["lexical_audit"]["banned_phrases_count"]
            total_placeholders += mm_res["lexical_audit"]["placeholder_tokens_count"]
        if fc_res["lexical_audit"]:
            total_banned_words += fc_res["lexical_audit"]["banned_words_count"]
            total_banned_phrases += fc_res["lexical_audit"]["banned_phrases_count"]
            total_placeholders += fc_res["lexical_audit"]["placeholder_tokens_count"]

    # 4. Verify Worksheets 1-10
    worksheets_audit = {}
    total_worksheet_words = 0
    for n in CHAPTER_NUMBERS:
        ws_tag = f"{n:02d}"
        ws_res = check_worksheet(n, errors)
        worksheets_audit[f"worksheet_{ws_tag}"] = ws_res
        total_worksheet_words += ws_res["word_count"]
        if ws_res["lexical_audit"]:
            total_banned_words += ws_res["lexical_audit"]["banned_words_count"]
            total_banned_phrases += ws_res["lexical_audit"]["banned_phrases_count"]
            total_placeholders += ws_res["lexical_audit"]["placeholder_tokens_count"]

    # 5. Verify PROJECT_STATE.json
    state_path = BASE_DIR / "PROJECT_STATE.json"
    project_state_valid = False
    if state_path.is_file():
        try:
            state_data = json.loads(state_path.read_text(encoding="utf-8"))
            p4 = state_data.get("roadmap_phases", {}).get("phase_4", {})
            p4_ok = p4 == "completed" or (isinstance(p4, dict) and p4.get("status") == "completed")
            expected_chapters = [f"chapter-{n:02d}" for n in CHAPTER_NUMBERS]
            ch_ok = state_data.get("chapters_completed") == expected_chapters
            fm_ok = state_data.get("front_matter_completed") is True
            bm_ok = state_data.get("back_matter_completed") is True
            if p4_ok and ch_ok and fm_ok and bm_ok:
                project_state_valid = True
            else:
                errors.append(
                    "PROJECT_STATE.json does not have phase_4 completed, chapters_completed = ['chapter-01'..'chapter-10'], front_matter_completed=true, and back_matter_completed=true."
                )
        except Exception as exc:
            errors.append(f"PROJECT_STATE.json invalid JSON: {exc}")
    else:
        errors.append("Missing PROJECT_STATE.json")

    qa_gate_passed = len(errors) == 0

    report = {
        "phase": "Phase 4 — Final Manuscripts, Vector Diagrams, Worksheets & Front/Back Matter Vault (Chapters 8, 9, 10 + Front & Back Matter)",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "qa_gate_passed": qa_gate_passed,
        "cumulative_summary": {
            "front_matter_verified": front_matter_audit["passed"],
            "chapters_verified": "10/10" if all(c["passed"] for c in chapters_audit.values()) else "Fail",
            "back_matter_verified": back_matter_audit["passed"],
            "total_chapters_word_count_ch1_to_ch10": total_chapter_words,
            "total_manuscript_word_count_with_front_and_back_matter": total_manuscript_words,
            "total_worksheets_word_count_ws1_to_ws10": total_worksheet_words,
            "tested_ai_prompts_verified": f"{total_prompts_verified}/50",
            "back_matter_indexed_prompts_verified": back_matter_audit["indexed_prompts_verified"],
            "back_matter_emergency_scripts_verified": back_matter_audit["emergency_scripts_verified"],
            "svg_diagrams_verified": f"{sum(1 for s in svg_audit.values() if s['passed'])}/20",
            "worksheets_verified": f"{sum(1 for w in worksheets_audit.values() if w['passed'])}/10",
            "banned_ai_words_count": total_banned_words,
            "banned_ai_phrases_count": total_banned_phrases,
            "placeholder_tokens_count": total_placeholders,
            "project_state_locked": project_state_valid,
        },
        "front_matter_audit": front_matter_audit,
        "chapters_audit": chapters_audit,
        "back_matter_audit": back_matter_audit,
        "svg_visual_assets_audit": svg_audit,
        "worksheets_audit": worksheets_audit,
        "errors": errors,
    }

    report_path = BASE_DIR / "11-QUALITY-ASSURANCE/qa-phase4-report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if qa_gate_passed else 1


if __name__ == "__main__":
    sys.exit(main())
