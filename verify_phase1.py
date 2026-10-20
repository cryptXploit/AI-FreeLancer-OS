#!/usr/bin/env python3
"""
Phase 1 Automated Quality Assurance & Verification Engine (verify_phase1.py)
Digital Knowledge Product Studio — The AI Freelancer Operating System
"""

import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

BASE_DIR = Path(__file__).resolve().parent

REQUIRED_DIRECTORIES = [
    "01-MARKET-RESEARCH",
    "02-BOOK-METADATA",
    "03-MANUSCRIPT/Front-Matter",
    "03-MANUSCRIPT/Chapters",
    "03-MANUSCRIPT/Back-Matter",
    "04-VISUAL-ASSETS/Illustrations",
    "04-VISUAL-ASSETS/Mindmaps",
    "04-VISUAL-ASSETS/Flowcharts",
    "05-WORKBOOKS",
    "06-NOTION-TEMPLATES",
    "07-INTERACTIVE-TOOLS",
    "08-COVER-DESIGN",
    "09-EXPORTS/PDF",
    "09-EXPORTS/EPUB",
    "09-EXPORTS/PRINT",
    "09-EXPORTS/HYBRID-BUNDLE",
    "10-MARKETING",
    "11-QUALITY-ASSURANCE",
]

REQUIRED_FILES = [
    "README.md",
    "PROJECT_STATE.json",
    "book-config.yaml",
    "verify_phase1.py",
    "01-MARKET-RESEARCH/sources.md",
    "02-BOOK-METADATA/book-config.yaml",
    "02-BOOK-METADATA/style-guide.md",
    "03-MANUSCRIPT/Front-Matter/toc.md",
    "03-MANUSCRIPT/Chapters/chapter-01.md",
    "04-VISUAL-ASSETS/Mindmaps/chapter-01-mindmap.svg",
    "04-VISUAL-ASSETS/Flowcharts/chapter-01-flowchart.svg",
    "05-WORKBOOKS/worksheet-01.md",
]

REQUIRED_14_SECTIONS = [
    "# Chapter 1:",
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

REQUIRED_PROMPTS = [
    "### Prompt 1.1:",
    "### Prompt 1.2:",
    "### Prompt 1.3:",
    "### Prompt 1.4:",
    "### Prompt 1.5:",
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
    r"\[insert content here\]",
    r"\.\.\.rest of chapter omitted\.\.\.",
]


def check_svg_file(svg_path: Path) -> dict:
    result = {
        "file": str(svg_path.relative_to(BASE_DIR)).replace("\\", "/"),
        "exists": svg_path.is_file(),
        "xml_valid": False,
        "non_empty_text_nodes": 0,
        "min_required_text_nodes": 15,
        "passed": False,
        "error": None,
    }
    if not svg_path.is_file():
        result["error"] = "File does not exist"
        return result

    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()
        result["xml_valid"] = True
        text_nodes = []
        for elem in root.iter():
            tag_name = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            if tag_name == "text":
                full_text = "".join(elem.itertext()).strip()
                if full_text:
                    text_nodes.append(full_text)
        result["non_empty_text_nodes"] = len(text_nodes)
        result["passed"] = result["xml_valid"] and len(text_nodes) >= 15
    except Exception as exc:
        result["error"] = str(exc)

    return result


def main() -> int:
    errors = []

    # 1. Verify directories
    missing_dirs = []
    for d in REQUIRED_DIRECTORIES:
        dir_path = BASE_DIR / d
        if not dir_path.is_dir():
            missing_dirs.append(d)
            errors.append(f"Missing required directory: {d}")

    # 2. Verify files exist and are non-empty
    missing_or_empty_files = []
    for f in REQUIRED_FILES:
        file_path = BASE_DIR / f
        if not file_path.is_file() or file_path.stat().st_size == 0:
            missing_or_empty_files.append(f)
            errors.append(f"Missing or empty required file: {f}")

    # 3. Verify PROJECT_STATE.json
    project_state_valid = False
    project_state_path = BASE_DIR / "PROJECT_STATE.json"
    if project_state_path.is_file():
        try:
            state_data = json.loads(project_state_path.read_text(encoding="utf-8"))
            required_keys = {"product_id", "title", "subtitle", "version", "value_ladder", "design_tokens", "roadmap_phases", "chapters_completed"}
            if required_keys.issubset(set(state_data.keys())) and "chapter-01" in state_data.get("chapters_completed", []):
                project_state_valid = True
            else:
                errors.append("PROJECT_STATE.json missing required top-level keys or chapter-01 completion state.")
        except Exception as exc:
            errors.append(f"PROJECT_STATE.json invalid JSON: {exc}")

    # 4. Verify book-config.yaml
    book_config_valid = False
    for cfg_rel in ["book-config.yaml", "02-BOOK-METADATA/book-config.yaml"]:
        cfg_path = BASE_DIR / cfg_rel
        if cfg_path.is_file():
            try:
                raw_cfg = cfg_path.read_text(encoding="utf-8")
                if yaml is not None:
                    parsed = yaml.safe_load(raw_cfg)
                    if isinstance(parsed, dict) and "product_id" in parsed and "commercial_value_ladder" in parsed:
                        book_config_valid = True
                    else:
                        errors.append(f"{cfg_rel} missing required YAML keys.")
                else:
                    book_config_valid = "product_id:" in raw_cfg and "commercial_value_ladder:" in raw_cfg
            except Exception as exc:
                errors.append(f"{cfg_rel} YAML parse error: {exc}")
                book_config_valid = False

    # 5. Verify Chapter 1 Manuscript
    ch1_path = BASE_DIR / "03-MANUSCRIPT/Chapters/chapter-01.md"
    ch1_word_count = 0
    missing_sections = []
    missing_prompts = []
    banned_word_hits = []
    banned_phrase_hits = []
    placeholder_hits = []

    if ch1_path.is_file():
        ch1_text = ch1_path.read_text(encoding="utf-8")
        words = ch1_text.split()
        ch1_word_count = len(words)
        if ch1_word_count < 3500:
            errors.append(f"chapter-01.md word count ({ch1_word_count}) is below minimum 3,500 words.")

        for sec in REQUIRED_14_SECTIONS:
            if sec not in ch1_text:
                missing_sections.append(sec)
                errors.append(f"chapter-01.md missing required section heading: {sec}")

        for pr in REQUIRED_PROMPTS:
            if pr not in ch1_text:
                missing_prompts.append(pr)
                errors.append(f"chapter-01.md missing required prompt heading: {pr}")

        for bw in BANNED_WORDS:
            pattern = re.compile(rf"\b{re.escape(bw)}(?:s|d|ed|ing)?\b", re.IGNORECASE)
            matches = pattern.findall(ch1_text)
            if matches:
                banned_word_hits.append({"word": bw, "count": len(matches)})
                errors.append(f"chapter-01.md contains banned AI word '{bw}' ({len(matches)} occurrences).")

        for bp in BANNED_PHRASES:
            pattern = re.compile(re.escape(bp), re.IGNORECASE)
            matches = pattern.findall(ch1_text)
            if matches:
                banned_phrase_hits.append({"phrase": bp, "count": len(matches)})
                errors.append(f"chapter-01.md contains banned AI phrase '{bp}' ({len(matches)} occurrences).")

        for ph in PLACEHOLDER_TOKENS:
            matches = re.findall(ph, ch1_text, flags=re.IGNORECASE)
            if matches:
                placeholder_hits.append({"pattern": ph, "count": len(matches)})
                errors.append(f"chapter-01.md contains placeholder token '{ph}'.")

    # 6. Verify SVG assets
    mindmap_check = check_svg_file(BASE_DIR / "04-VISUAL-ASSETS/Mindmaps/chapter-01-mindmap.svg")
    flowchart_check = check_svg_file(BASE_DIR / "04-VISUAL-ASSETS/Flowcharts/chapter-01-flowchart.svg")
    if not mindmap_check["passed"]:
        errors.append(f"chapter-01-mindmap.svg failed verification: {mindmap_check}")
    if not flowchart_check["passed"]:
        errors.append(f"chapter-01-flowchart.svg failed verification: {flowchart_check}")

    qa_gate_passed = len(errors) == 0

    report = {
        "phase": "Phase 1 — Studio Foundation, State Lock, QA Engine & Chapter 1 Package",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "qa_gate_passed": qa_gate_passed,
        "directories_verified": {
            "required_count": len(REQUIRED_DIRECTORIES),
            "missing_directories": missing_dirs,
            "passed": len(missing_dirs) == 0,
        },
        "files_verified": {
            "required_count": len(REQUIRED_FILES),
            "missing_or_empty_files": missing_or_empty_files,
            "passed": len(missing_or_empty_files) == 0,
        },
        "metadata_validation": {
            "project_state_json_valid": project_state_valid,
            "book_config_yaml_valid": book_config_valid,
        },
        "chapter_01_audit": {
            "file": "03-MANUSCRIPT/Chapters/chapter-01.md",
            "word_count": ch1_word_count,
            "min_word_count_required": 3500,
            "target_word_count": 3800,
            "required_14_sections_verified": "Pass" if len(missing_sections) == 0 else "Fail",
            "sections_found": f"{len(REQUIRED_14_SECTIONS) - len(missing_sections)}/{len(REQUIRED_14_SECTIONS)}",
            "missing_sections": missing_sections,
            "tested_ai_prompts_verified": f"{len(REQUIRED_PROMPTS) - len(missing_prompts)}/{len(REQUIRED_PROMPTS)}",
            "missing_prompts": missing_prompts,
            "banned_ai_words_count": sum(item["count"] for item in banned_word_hits),
            "banned_ai_phrases_count": sum(item["count"] for item in banned_phrase_hits),
            "banned_word_details": banned_word_hits,
            "banned_phrase_details": banned_phrase_hits,
            "placeholder_tokens_count": len(placeholder_hits),
        },
        "svg_visual_assets_audit": {
            "chapter_01_mindmap_svg": mindmap_check,
            "chapter_01_flowchart_svg": flowchart_check,
        },
        "errors": errors,
    }

    report_path = BASE_DIR / "11-QUALITY-ASSURANCE/qa-phase1-report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if qa_gate_passed else 1


if __name__ == "__main__":
    sys.exit(main())
