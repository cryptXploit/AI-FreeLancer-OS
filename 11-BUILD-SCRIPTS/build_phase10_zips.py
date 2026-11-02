import sys
sys.stdout.reconfigure(encoding='utf-8')
import os, zipfile, shutil, tempfile

STUDIO = r"e:\Ebook-Makaer\AI FreeLancer OS\DIGITAL-PUBLISHING-STUDIO"
BUNDLE_DIR = os.path.join(STUDIO, "09-EXPORTS", "HYBRID-BUNDLE")

# Assets to add to ALL ZIPs
COMMON_ASSETS = [
    (os.path.join(STUDIO, "START-HERE-LAUNCHPAD.html"), "START-HERE-LAUNCHPAD.html"),
    (os.path.join(STUDIO, "07-INTERACTIVE-TOOLS", "freelancer-os-app.html"), "07-INTERACTIVE-TOOLS/freelancer-os-app.html"),
]

# Assets to add ONLY to Tier0 ZIP
TIER0_EXTRA = [
    (os.path.join(STUDIO, "06-NOTION-TEMPLATES", "Spreadsheets", "tier0-free-lite-command-sheet.xlsx"),
     "04-EXCEL-FREE-LITE/tier0-free-lite-command-sheet.xlsx"),
    (os.path.join(STUDIO, "06-NOTION-TEMPLATES", "Tier0-Free-Notion-Quickstart", "FREE-NOTION-QUICKSTART-GUIDE.md"),
     "06-NOTION-QUICKSTART/FREE-NOTION-QUICKSTART-GUIDE.md"),
    (os.path.join(STUDIO, "14-AUTOMATION-BLUEPRINTS", "Tier0-Free-Starter-Automation", "free-automation-blueprint-01.json"),
     "14-AUTOMATION/free-automation-blueprint-01.json"),
    (os.path.join(STUDIO, "14-AUTOMATION-BLUEPRINTS", "Tier0-Free-Starter-Automation", "FREE-AUTOMATION-1CLICK-TEST-GUIDE.md"),
     "14-AUTOMATION/FREE-AUTOMATION-1CLICK-TEST-GUIDE.md"),
]

TIER0_ZIP_NAME = "Tier0-Free-Leak-Audit-Starter-Kit.zip"

zip_files = [f for f in os.listdir(BUNDLE_DIR) if f.lower().endswith('.zip')]
print(f"Found {len(zip_files)} ZIP files to rebuild")

for zip_name in zip_files:
    zip_path = os.path.join(BUNDLE_DIR, zip_name)
    is_tier0 = (zip_name == TIER0_ZIP_NAME)
    assets_to_add = COMMON_ASSETS + (TIER0_EXTRA if is_tier0 else [])

    print(f"\nRebuilding: {zip_name}")

    # Read existing entries
    with zipfile.ZipFile(zip_path, 'r') as zin:
        existing_names = set(zin.namelist())
        existing_data = {name: zin.read(name) for name in existing_names}
        existing_info = {info.filename: info for info in zin.infolist()}

    # Determine which new assets are actually new
    added = []
    skipped = []
    for src_path, arc_name in assets_to_add:
        if arc_name in existing_names:
            skipped.append(arc_name)
        elif not os.path.exists(src_path):
            print(f"  WARNING: source file not found: {src_path}")
        else:
            added.append((src_path, arc_name))

    # Write new ZIP via temp file
    tmp_fd, tmp_path = tempfile.mkstemp(dir=BUNDLE_DIR, suffix='.tmp')
    os.close(tmp_fd)
    try:
        with zipfile.ZipFile(tmp_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            # Preserve original entries
            for name, data in existing_data.items():
                info = existing_info[name]
                zout.writestr(info, data)
            # Add new entries
            for src_path, arc_name in added:
                zout.write(src_path, arc_name)
                print(f"  + Added: {arc_name}")
        if skipped:
            print(f"  ~ Skipped (already present): {[s for s in skipped]}")

        # Replace original
        os.replace(tmp_path, zip_path)
        print(f"  -> Rebuilt: {zip_name} ({os.path.getsize(zip_path):,} bytes)")
    except Exception as e:
        os.remove(tmp_path)
        print(f"  ERROR rebuilding {zip_name}: {e}")
        raise

# Verify START-HERE-LAUNCHPAD.html inside each ZIP
print("\n=== VERIFICATION ===")
all_ok = True
for zip_name in zip_files:
    zip_path = os.path.join(BUNDLE_DIR, zip_name)
    with zipfile.ZipFile(zip_path, 'r') as z:
        names = z.namelist()
    has_launchpad = "START-HERE-LAUNCHPAD.html" in names
    has_app = "07-INTERACTIVE-TOOLS/freelancer-os-app.html" in names
    status = "OK" if (has_launchpad and has_app) else "MISSING"
    if status != "OK":
        all_ok = False
    print(f"  {status}: {zip_name} | LAUNCHPAD={has_launchpad} | APP={has_app}")

if all_ok:
    print("\nAll ZIPs verified successfully.")
else:
    print("\nWARNING: Some ZIPs are missing required files!")
