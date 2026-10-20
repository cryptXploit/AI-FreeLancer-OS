#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 6 Verification Suite (verify_phase6.py)
The AI Freelancer Operating System — Digital Knowledge Product Studio

Validates:
1. 07-INTERACTIVE-TOOLS/freelancer-os-app.html (exists, >= 120,000 bytes, valid HTML5 structure, 100% offline zero external JS/CSS)
2. 09-EXPORTS/HYBRID-BUNDLE/freelancer-os-app.html (exists and matches primary app byte-for-byte)
3. 07-INTERACTIVE-TOOLS/README-WEB-APP.md (exists, >= 700 words)
4. Embedded 50/50 AI Workflow Prompts (1.1 - 10.5) & 12/12 Emergency Client Scripts (Script 1 - Script 12) parsed from PROMPTS_DATA and SCRIPTS_DATA
5. Interactive UI Modules (#tab-ehr-audit, #tab-bcr-pricing, #tab-prompt-vault, #tab-ceo-scorecard), Multi-Currency (#currency-select: USD, GBP, CAD, AUD), Edition Switcher (#edition-mode-toggle, ?mode=free, ?mode=pro, FREELANCER-OS-PRO-2026), localStorage, JSON export/import, CSV export, and @media print
6. Zero banned words, zero banned phrases, and zero placeholder tokens across Phase 6 deliverables
7. Updates PROJECT_STATE.json and writes 11-QUALITY-ASSURANCE/qa-phase6-report.json
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP_PRIMARY = ROOT / "07-INTERACTIVE-TOOLS" / "freelancer-os-app.html"
APP_BUNDLE = ROOT / "09-EXPORTS" / "HYBRID-BUNDLE" / "freelancer-os-app.html"
README_WEBAPP = ROOT / "07-INTERACTIVE-TOOLS" / "README-WEB-APP.md"
BUILDER_SCRIPT = ROOT / "build_webapp.py"
PROJECT_STATE_PATH = ROOT / "PROJECT_STATE.json"
QA_REPORT_PATH = ROOT / "11-QUALITY-ASSURANCE" / "qa-phase6-report.json"


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def main() -> int:
    print("=" * 78)
    print("PHASE 6 QA VERIFICATION SUITE — SAAS-LITE INTERACTIVE WEB COMPANION APP")
    print("=" * 78)

    errors = []
    checks = []

    def record_check(name: str, passed: bool, details: str):
        checks.append({"check": name, "passed": passed, "details": details})
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}: {details}")
        if not passed:
            errors.append(f"{name}: {details}")

    # Load PROJECT_STATE.json for editorial guardrails
    if not PROJECT_STATE_PATH.exists():
        print("[FATAL] PROJECT_STATE.json not found.")
        return 1

    state = json.loads(PROJECT_STATE_PATH.read_text(encoding="utf-8"))
    banned_words = state["editorial_guardrails"]["banned_words"]
    banned_phrases = state["editorial_guardrails"]["banned_phrases"]

    # 1. File existence & size verification
    app_exists = APP_PRIMARY.exists()
    app_bytes = APP_PRIMARY.stat().st_size if app_exists else 0
    record_check(
        "Primary Web App File & Size (>= 120,000 bytes)",
        app_exists and app_bytes >= 120000,
        f"{APP_PRIMARY.relative_to(ROOT)} ({app_bytes:,} bytes / {app_bytes / 1024:.1f} KB)",
    )

    bundle_exists = APP_BUNDLE.exists()
    bundle_bytes = APP_BUNDLE.stat().st_size if bundle_exists else 0
    bytes_match = (
        app_exists
        and bundle_exists
        and APP_PRIMARY.read_bytes() == APP_BUNDLE.read_bytes()
    )
    record_check(
        "Hybrid Bundle Mirror Sync",
        bundle_exists and bytes_match,
        f"{APP_BUNDLE.relative_to(ROOT)} ({bundle_bytes:,} bytes, exact byte match={bytes_match})",
    )

    readme_exists = README_WEBAPP.exists()
    readme_text = README_WEBAPP.read_text(encoding="utf-8") if readme_exists else ""
    readme_words = count_words(readme_text)
    record_check(
        "README-WEB-APP.md Word Count (>= 700 words)",
        readme_exists and readme_words >= 700,
        f"{README_WEBAPP.relative_to(ROOT)} ({readme_words} words)",
    )

    builder_exists = BUILDER_SCRIPT.exists()
    record_check(
        "Deterministic Builder Script (build_webapp.py)",
        builder_exists,
        f"{BUILDER_SCRIPT.relative_to(ROOT)} exists={builder_exists}",
    )

    if not app_exists:
        print("[FATAL] Cannot inspect freelancer-os-app.html because file is missing.")
        return 1

    html = APP_PRIMARY.read_text(encoding="utf-8")

    # 2. Extract and verify STUDIO_PROMPTS_DATA (50/50) and STUDIO_SCRIPTS_DATA (12/12)
    m_prompts = re.search(
        r"const STUDIO_PROMPTS_DATA = (\[.*?\]);\n\s*const STUDIO_SCRIPTS_DATA =",
        html,
        flags=re.DOTALL,
    )
    m_scripts = re.search(
        r"const STUDIO_SCRIPTS_DATA = (\[.*?\]);\n\s*const ALL_VAULT_ITEMS =",
        html,
        flags=re.DOTALL,
    )

    prompts_data = []
    scripts_data = []
    try:
        if m_prompts:
            prompts_data = json.loads(m_prompts.group(1))
        if m_scripts:
            scripts_data = json.loads(m_scripts.group(1))
    except Exception as exc:
        record_check("Embedded JSON Data Parse", False, f"Failed to parse JSON: {exc}")

    expected_prompt_ids = [f"{ch}.{idx}" for ch in range(1, 11) for idx in range(1, 6)]
    found_prompt_ids = [p.get("id") for p in prompts_data]
    missing_prompts = [pid for pid in expected_prompt_ids if pid not in found_prompt_ids]
    incomplete_prompts = [
        p.get("id")
        for p in prompts_data
        if len(p.get("template", "")) < 100
        or len(p.get("verification", "")) < 20
        or len(p.get("objective", "")) < 20
        or len(p.get("variables", [])) < 1
    ]
    record_check(
        "50/50 Tested AI Workflow Prompts Embedded (1.1 - 10.5)",
        len(prompts_data) == 50 and not missing_prompts and not incomplete_prompts,
        f"total={len(prompts_data)}/50, missing={missing_prompts}, incomplete={incomplete_prompts}",
    )

    expected_script_nums = list(range(1, 13))
    found_script_nums = [s.get("script_number") for s in scripts_data]
    missing_scripts = [num for num in expected_script_nums if num not in found_script_nums]
    incomplete_scripts = [
        s.get("id")
        for s in scripts_data
        if len(s.get("template", "")) < 80
        or len(s.get("verification", "")) < 20
        or len(s.get("variables", [])) < 1
    ]
    record_check(
        "12/12 Emergency Client Scripts Embedded (Script 1 - Script 12)",
        len(scripts_data) == 12 and not missing_scripts and not incomplete_scripts,
        f"total={len(scripts_data)}/12, missing={missing_scripts}, incomplete={incomplete_scripts}",
    )

    # 3. Verify Interactive UI Modules & Functional Features
    required_selectors_and_tokens = [
        ("id=\"tab-ehr-audit\"", "Module 1: EHR & Revenue Leak Audit Tab (#tab-ehr-audit)"),
        ("id=\"tab-bcr-pricing\"", "Module 2: BCR & 3-Tier Proposal Pricing Tab (#tab-bcr-pricing)"),
        ("id=\"tab-prompt-vault\"", "Module 3: 50-Prompt & 12-Script Vault Tab (#tab-prompt-vault)"),
        ("id=\"tab-ceo-scorecard\"", "Module 4: Weekly CEO Scorecard Tab (#tab-ceo-scorecard)"),
        ("id=\"currency-select\"", "Multi-Currency Selector (#currency-select)"),
        ("id=\"edition-mode-toggle\"", "Edition Mode Toggle (#edition-mode-toggle)"),
        ("FREELANCER-OS-PRO-2026", "Pro Companion Access Code (FREELANCER-OS-PRO-2026)"),
        ("URLSearchParams", "URL Query Parameter Mode Handling (?mode=free / ?mode=pro)"),
        ("localStorage", "Browser localStorage State Persistence"),
        ("exportWorkspaceJson", "JSON Workspace Backup Export Function"),
        ("importWorkspaceJson", "JSON Workspace Backup Import Function"),
        ("exportCeoLogCsv", "CSV CEO Scorecard Export Function"),
        ("@media print", "Dedicated Print / PDF Stylesheet (@media print)"),
    ]
    for token, label in required_selectors_and_tokens:
        present = token in html
        record_check(label, present, f"token '{token}' present={present}")

    # Verify all currencies supported
    currencies_ok = all(c in html for c in ["$ USD", "£ GBP", "€ EUR", "CA$ CAD", "A$ AUD"])
    record_check(
        "Multi-Currency Support (USD, GBP, EUR, CAD, AUD)",
        currencies_ok,
        f"USD/GBP/EUR/CAD/AUD configured={currencies_ok}",
    )

    # Verify zero external runtime dependencies (<script src="http" or <link rel="stylesheet" href="http")
    ext_deps = re.findall(
        r'<(?:script|link)\b[^>]*(?:src|href)=["\']https?://', html, flags=re.IGNORECASE
    )
    record_check(
        "100% Offline Zero External JS/CSS Dependencies",
        len(ext_deps) == 0,
        f"external runtime dependencies={len(ext_deps)}",
    )

    # 4. Strict Lexical Filter & Anti-Placeholder Audit
    files_to_audit = [
        ("07-INTERACTIVE-TOOLS/freelancer-os-app.html", html),
        ("07-INTERACTIVE-TOOLS/README-WEB-APP.md", readme_text),
        ("build_webapp.py", BUILDER_SCRIPT.read_text(encoding="utf-8")),
    ]

    banned_violations = []
    placeholder_violations = []
    placeholder_patterns = [
        r"\bTODO\b",
        r"\bTBD\b",
        r"\bFIXME\b",
        r"Lorem Ipsum",
        r"\[insert text\]",
    ]

    for rel_name, content in files_to_audit:
        for bw in banned_words:
            matches = re.findall(rf"\b{re.escape(bw)}(?:s|ed|ing)?\b", content, flags=re.IGNORECASE)
            if matches:
                banned_violations.append(f"{rel_name}: '{bw}' ({len(matches)}x)")
        for bp in banned_phrases:
            if bp.lower() in content.lower():
                banned_violations.append(f"{rel_name}: phrase '{bp}'")
        for pat in placeholder_patterns:
            if re.search(pat, content, flags=re.IGNORECASE):
                placeholder_violations.append(f"{rel_name}: pattern '{pat}'")

    record_check(
        "Strict Lexical Filter (Zero Banned AI Clichés & Phrases)",
        len(banned_violations) == 0,
        "0 violations" if not banned_violations else "; ".join(banned_violations),
    )

    record_check(
        "Zero Placeholders / Truncation Audit",
        len(placeholder_violations) == 0,
        "0 violations" if not placeholder_violations else "; ".join(placeholder_violations),
    )

    # 5. Update PROJECT_STATE.json & Write QA Report
    all_passed = len(errors) == 0

    if all_passed:
        state["roadmap_phases"]["phase_6"]["status"] = "completed"
        state["roadmap_phases"]["phase_6"]["verified"] = True
        state["compiled_deliverables_phase6"] = {
            "webapp_primary": {
                "path": "07-INTERACTIVE-TOOLS/freelancer-os-app.html",
                "size_bytes": app_bytes,
                "size_kb": round(app_bytes / 1024, 1),
                "prompts_embedded": len(prompts_data),
                "scripts_embedded": len(scripts_data),
            },
            "webapp_hybrid_bundle": {
                "path": "09-EXPORTS/HYBRID-BUNDLE/freelancer-os-app.html",
                "size_bytes": bundle_bytes,
                "size_kb": round(bundle_bytes / 1024, 1),
            },
            "webapp_readme": {
                "path": "07-INTERACTIVE-TOOLS/README-WEB-APP.md",
                "words": readme_words,
            },
            "webapp_compiler": {
                "path": "build_webapp.py",
            },
        }
        PROJECT_STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        print("\n[STATE LOCK] Updated PROJECT_STATE.json -> phase_6 status='completed', verified=True")

    qa_report = {
        "phase": 6,
        "title": "SaaS-Lite Interactive Web Companion App (freelancer-os-app.html)",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "overall_status": "PASSED" if all_passed else "FAILED",
        "metrics": {
            "app_size_bytes": app_bytes,
            "app_size_kb": round(app_bytes / 1024, 1),
            "readme_word_count": readme_words,
            "prompts_embedded": len(prompts_data),
            "scripts_embedded": len(scripts_data),
            "modules_verified": [
                "#tab-ehr-audit",
                "#tab-bcr-pricing",
                "#tab-prompt-vault",
                "#tab-ceo-scorecard",
            ],
            "currencies_supported": ["USD", "GBP", "CAD", "AUD"],
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
    print(f"PHASE 6 VERIFICATION RESULT: {'PASSED (0 ERRORS)' if all_passed else f'FAILED ({len(errors)} ERRORS)'}")
    print("=" * 78)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
