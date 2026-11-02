#!/usr/bin/env python3
"""
inject_funnel_links.py
======================
Reads funnel-links-config.json and replaces placeholder tokens
in target HTML files with live URLs.

Usage:
  python inject_funnel_links.py [--dry-run]
"""
import os
import re
import json
import sys
import shutil
from datetime import datetime

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
STUDIO_ROOT = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SCRIPT_DIR, "funnel-links-config.json")

TARGET_FILES = [
    os.path.join(STUDIO_ROOT, "10-MARKETING", "index.html"),
    os.path.join(STUDIO_ROOT, "07-INTERACTIVE-TOOLS", "freelancer-os-app.html"),
    os.path.join(STUDIO_ROOT, "START-HERE-LAUNCHPAD.html"),
    os.path.join(SCRIPT_DIR, "web-live-demo", "index.html"),
]

PLACEHOLDER_MAP = {
    "GUMROAD_TIER0_URL":    "gumroad_tier0_free_url",
    "GUMROAD_TIER1_URL":    "gumroad_tier1_book_url",
    "GUMROAD_TIER2_URL":    "gumroad_tier2_workbook_url",
    "GUMROAD_TIER3_URL":    "gumroad_tier3_flagship_url",
    "GUMROAD_VIP_URL":      "gumroad_tier4_vip_url",
    "PAYHIP_URL":           "payhip_store_url",
    "AMAZON_EBOOK_URL":     "amazon_kdp_ebook_url",
    "AMAZON_PAPERBACK_URL": "amazon_kdp_paperback_url",
    "LIVE_DEMO_URL":        "live_web_app_demo_url",
    "COUPON_SUBSCRIBER15":  "coupon_subscriber15",
    "COUPON_LAUNCH20":      "coupon_launch20",
    "COUPON_UPGRADE25":     "coupon_upgrade25",
    "PRO_KEY_TIER3":        "pro_activation_key_tier3",
    "TIER2_KEY":            "tier2_activation_key",
}

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def inject_file(path, config, dry_run=False):
    if not os.path.isfile(path):
        print(f"  ⚠️  Skipped (not found): {os.path.relpath(path, STUDIO_ROOT)}")
        return 0

    with open(path, "r", encoding="utf-8") as f:
        original = f.read()

    content = original
    replacements = 0

    for placeholder, config_key in PLACEHOLDER_MAP.items():
        value = config.get(config_key, "")
        pattern = re.compile(re.escape(placeholder))
        count = len(pattern.findall(content))
        if count:
            content = pattern.sub(value, content)
            replacements += count
            print(f"    🔁 {placeholder!r:30s} → {value!r}  (×{count})")

    if replacements and not dry_run:
        # Backup original
        backup = path + ".bak." + datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(path, backup)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ {os.path.relpath(path, STUDIO_ROOT)} — {replacements} replacement(s) made (backup: .bak)")
    elif replacements and dry_run:
        print(f"  🔍 [DRY-RUN] {os.path.relpath(path, STUDIO_ROOT)} — {replacements} would be replaced")
    else:
        print(f"  ℹ️  {os.path.relpath(path, STUDIO_ROOT)} — No placeholders found")

    return replacements

def main():
    dry_run = "--dry-run" in sys.argv
    print("=" * 60)
    print("  inject_funnel_links.py — AI Freelancer OS")
    print(f"  Mode: {'DRY-RUN' if dry_run else 'LIVE'}")
    print("=" * 60)

    config = load_config()
    print(f"\n📋 Config loaded: {len(config)} keys\n")

    total = 0
    for path in TARGET_FILES:
        print(f"\n📄 Processing: {os.path.relpath(path, STUDIO_ROOT)}")
        total += inject_file(path, config, dry_run)

    print(f"\n{'='*60}")
    print(f"  ✅ DONE — Total replacements: {total}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
