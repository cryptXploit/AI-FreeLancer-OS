#!/usr/bin/env python3
"""
Phase 11 Automated Verification Suite (`verify_phase11_gumroad.py`)
Validates:
1. All 3 Square 600x600 SVG thumbnails in `08-COVER-DESIGN/` (valid XML, viewBox="0 0 600 600", "OMAR SUNNY" credit).
2. All 3 rendered 600x600 PNG thumbnails in `08-COVER-DESIGN/` and `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/` (exact 600x600 px via PNG IHDR header).
3. All 5 Gumroad Hybrid Master Setup Markdown guides in `10-MARKETING/Gumroad-Hybrid-Master-Setup/` meet exact minimum word-count gates:
   - 01-LISTING-1-FREE-STARTER-KIT-EXACT-FIELDS.md (>= 1,500 words)
   - 02-LISTING-2-FLAGSHIP-3-VERSION-PRODUCT-EXACT-FIELDS.md (>= 2,500 words)
   - 03-LISTING-3-VIP-RECURRING-MEMBERSHIP-EXACT-FIELDS.md (>= 1,800 words)
   - 04-GUMROAD-CHECKOUT-UPSELLS-COUPONS-AND-WORKFLOWS.md (>= 1,800 words)
   - 05-AI-COVER-AND-THUMBNAIL-IMAGE-GENERATION-PROMPTS.md (>= 1,800 words)
4. Zero banned words (including inflections) and zero banned phrases across all Phase 11 deliverables.
5. Tier 4 ZIP archive integrity (`Tier4-Living-OS-Pro-Vault-Membership-Pack.zip` & `tier4-vip-living-career-vault-edition.zip`) containing `09-GUMROAD-HYBRID-MASTER-SETUP/` and `testzip() is None`.
6. Updates `PROJECT_STATE.json` and writes `11-QUALITY-ASSURANCE/qa-phase11-gumroad-report.json`.
"""

import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

STUDIO_ROOT = Path(__file__).resolve().parent.parent
COVER_DIR = STUDIO_ROOT / "08-COVER-DESIGN"
GUMROAD_DIR = STUDIO_ROOT / "10-MARKETING" / "Gumroad-Hybrid-Master-Setup"
THUMBS_DEST = GUMROAD_DIR / "Thumbnails-and-Covers"
BUNDLE_DIR = STUDIO_ROOT / "09-EXPORTS" / "HYBRID-BUNDLE"
QA_DIR = STUDIO_ROOT / "11-QUALITY-ASSURANCE"
QA_DIR.mkdir(parents=True, exist_ok=True)

BANNED_ROOTS = [
    "delve", "tapestry", "testament", "beacon", "symphony",
    "unlock", "unleash", "skyrocket", "supercharge", "game-changer",
    "pivotal", "realm", "foster", "underscore", "utilize", "leverage"
]

BANNED_PHRASES = [
    "in today's fast-paced world",
    "ever-evolving landscape",
    "it is important to remember",
    "in conclusion",
    "without further ado",
    "let's dive in",
    "look no further",
    "todo",
    "tbd",
    "lorem ipsum"
]


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def scan_banned(text: str, label: str, errors: list):
    lower = text.lower()
    for root in BANNED_ROOTS:
        # Match root and common English inflections
        stem = root[:-1] if root.endswith("e") else root
        pattern = rf"\b{re.escape(stem)}(?:e|es|ed|ing|s|d|r|rs)?\b"
        matches = re.findall(pattern, lower)
        if matches:
            errors.append(f"[{label}] Banned word family '{root}' matched: {set(matches)}")
    for phrase in BANNED_PHRASES:
        if phrase in lower:
            # For todo / tbd, ensure whole word match
            if phrase in ("todo", "tbd"):
                if re.search(rf"\b{phrase}\b", lower):
                    errors.append(f"[{label}] Banned placeholder '{phrase.upper()}' matched")
            else:
                errors.append(f"[{label}] Banned phrase '{phrase}' matched")


def read_png_dimensions(png_path: Path):
    data = png_path.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", data[16:24])
    return (w, h)


def main():
    print("=" * 80)
    print("VERIFYING PHASE 11: GUMROAD HYBRID 3-LISTING MASTER PACK & 600x600 THUMBNAILS")
    print("=" * 80)

    errors = []
    report = {
        "phase": 11,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "author": "OMAR SUNNY",
        "square_thumbnails": {},
        "markdown_guides": {},
        "zip_archives": {},
        "errors": []
    }

    # 1. Verify 3 Square 600x600 SVGs & PNGs
    thumb_bases = [
        "11-gumroad-square-thumb-listing1-free-audit-600x600",
        "12-gumroad-square-thumb-listing2-flagship-os-600x600",
        "13-gumroad-square-thumb-listing3-vip-membership-600x600",
    ]

    for base in thumb_bases:
        svg_path = COVER_DIR / f"{base}.svg"
        png_path = COVER_DIR / f"{base}.png"
        copy_svg_path = THUMBS_DEST / f"{base}.svg"
        copy_png_path = THUMBS_DEST / f"{base}.png"

        if not svg_path.exists():
            errors.append(f"Missing SVG thumbnail: {svg_path}")
            continue
        svg_text = svg_path.read_text(encoding="utf-8")
        try:
            root = ET.fromstring(svg_text)
            vb = root.attrib.get("viewBox", "")
            if vb != "0 0 600 600":
                errors.append(f"[{svg_path.name}] Expected viewBox='0 0 600 600', got '{vb}'")
        except Exception as exc:
            errors.append(f"[{svg_path.name}] XML parse error: {exc}")

        if "OMAR SUNNY" not in svg_text.upper():
            errors.append(f"[{svg_path.name}] Missing 'OMAR SUNNY' author credit")

        scan_banned(svg_text, svg_path.name, errors)

        if not png_path.exists():
            errors.append(f"Missing PNG thumbnail: {png_path}")
            continue
        dims = read_png_dimensions(png_path)
        if dims != (600, 600):
            errors.append(f"[{png_path.name}] Expected 600x600 px, got {dims}")

        if not copy_png_path.exists():
            errors.append(f"Missing copied PNG in Thumbnails-and-Covers: {copy_png_path}")
        else:
            copy_dims = read_png_dimensions(copy_png_path)
            if copy_dims != (600, 600):
                errors.append(f"[{copy_png_path.name}] Expected 600x600 px in copy, got {copy_dims}")

        if not copy_svg_path.exists():
            errors.append(f"Missing copied SVG in Thumbnails-and-Covers: {copy_svg_path}")

        report["square_thumbnails"][base] = {
            "svg_bytes": svg_path.stat().st_size,
            "png_bytes": png_path.stat().st_size,
            "dimensions": f"{dims[0]}x{dims[1]}" if dims else "invalid",
            "author_credit_verified": "OMAR SUNNY" in svg_text.upper(),
            "copied_to_marketing_pack": copy_png_path.exists() and copy_svg_path.exists()
        }
        print(f"  [OK] {base}.svg & .png -> {dims[0]}x{dims[1]} px ({png_path.stat().st_size:,} bytes)")

    # 2. Verify 1280x720 covers copied into Thumbnails-and-Covers
    required_cover_copies = [
        "03-gumroad-cover-tier1-core-1280x720.png",
        "04-gumroad-cover-tier2-pro-os-1280x720.png",
        "05-gumroad-cover-tier3-complete-suite-1280x720.png",
        "06-gumroad-cover-tier0-lead-magnet-1280x720.png",
        "00-ECOSYSTEM-MASTER-MAP-POSTER.png"
    ]
    for cov in required_cover_copies:
        cpath = THUMBS_DEST / cov
        if not cpath.exists() or cpath.stat().st_size < 5000:
            errors.append(f"Missing or empty cover copy in Thumbnails-and-Covers: {cov}")
        else:
            print(f"  [OK] Cover copy verified: {cov} ({cpath.stat().st_size:,} bytes)")

    # 3. Verify 5 Markdown Playbooks & Word-Count Gates
    md_specs = [
        ("01-LISTING-1-FREE-STARTER-KIT-EXACT-FIELDS.md", 1500),
        ("02-LISTING-2-FLAGSHIP-3-VERSION-PRODUCT-EXACT-FIELDS.md", 2500),
        ("03-LISTING-3-VIP-RECURRING-MEMBERSHIP-EXACT-FIELDS.md", 1800),
        ("04-GUMROAD-CHECKOUT-UPSELLS-COUPONS-AND-WORKFLOWS.md", 1800),
        ("05-AI-COVER-AND-THUMBNAIL-IMAGE-GENERATION-PROMPTS.md", 1800),
    ]

    total_md_words = 0
    for fname, min_words in md_specs:
        fpath = GUMROAD_DIR / fname
        if not fpath.exists():
            errors.append(f"Missing Gumroad Markdown playbook: {fpath}")
            continue
        text = fpath.read_text(encoding="utf-8")
        wc = count_words(text)
        total_md_words += wc
        if wc < min_words:
            errors.append(f"[{fname}] Word count {wc} is below minimum gate {min_words}")
        if "OMAR SUNNY" not in text.upper():
            errors.append(f"[{fname}] Missing 'OMAR SUNNY' author credit")
        scan_banned(text, fname, errors)
        report["markdown_guides"][fname] = {
            "word_count": wc,
            "min_required": min_words,
            "bytes": fpath.stat().st_size,
            "passed": wc >= min_words
        }
        status_str = "OK" if wc >= min_words else "FAIL"
        print(f"  [{status_str}] {fname}: {wc:,} words (gate >= {min_words:,} words)")

    report["total_markdown_words"] = total_md_words

    # 4. Verify Tier 4 ZIP Archives
    zip_names = [
        "Tier4-Living-OS-Pro-Vault-Membership-Pack.zip",
        "tier4-vip-living-career-vault-edition.zip"
    ]
    for zname in zip_names:
        zpath = BUNDLE_DIR / zname
        if not zpath.exists():
            errors.append(f"Missing Tier 4 ZIP archive: {zpath}")
            continue
        try:
            with zipfile.ZipFile(zpath, "r") as zf:
                bad = zf.testzip()
                if bad is not None:
                    errors.append(f"[{zname}] Corrupted member in ZIP: {bad}")
                names = zf.namelist()
                has_gumroad = any(n.startswith("09-GUMROAD-HYBRID-MASTER-SETUP/") for n in names)
                if not has_gumroad:
                    errors.append(f"[{zname}] Missing '09-GUMROAD-HYBRID-MASTER-SETUP/' inside ZIP")
                report["zip_archives"][zname] = {
                    "size_bytes": zpath.stat().st_size,
                    "size_mb": round(zpath.stat().st_size / (1024 * 1024), 2),
                    "file_count": len(names),
                    "has_gumroad_pack": has_gumroad,
                    "crc_ok": bad is None
                }
                print(f"  [OK] {zname}: {zpath.stat().st_size / (1024*1024):.2f} MB ({len(names)} files, CRC OK)")
        except Exception as exc:
            errors.append(f"[{zname}] ZIP error: {exc}")

    report["errors"] = errors
    report_path = QA_DIR / "qa-phase11-gumroad-report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    if errors:
        print("\n" + "!" * 80)
        print(f"PHASE 11 VERIFICATION FAILED WITH {len(errors)} ERROR(S):")
        for e in errors:
            print(f"  - {e}")
        print("!" * 80)
        sys.exit(1)

    # Update PROJECT_STATE.json
    state_path = STUDIO_ROOT / "PROJECT_STATE.json"
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
    else:
        state = {}

    state["current_phase"] = 11
    state["phases_completed"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    state["author"] = "OMAR SUNNY"
    state["phase11_gumroad_hybrid_pack"] = {
        "status": "VERIFIED_0_ERRORS",
        "square_thumbnails_600x600": list(report["square_thumbnails"].keys()),
        "markdown_guides": report["markdown_guides"],
        "total_markdown_words": total_md_words,
        "zip_archives": report["zip_archives"]
    }
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    print("\n" + "=" * 80)
    print(f"Total Phase 11 Gumroad Playbook Word Count: {total_md_words:,} words")
    print("PHASE 11 GUMROAD HYBRID MASTER SETUP VERIFICATION PASSED WITH 0 ERRORS")
    print("=" * 80)


if __name__ == "__main__":
    main()
