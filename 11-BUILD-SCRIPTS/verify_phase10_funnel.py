import sys
sys.stdout.reconfigure(encoding='utf-8')
import os, json

STUDIO = r"e:\Ebook-Makaer\AI FreeLancer OS\DIGITAL-PUBLISHING-STUDIO"
errors = 0

def check(label, condition):
    global errors
    if condition:
        print(f"PASS: {label}")
    else:
        print(f"FAIL: {label}")
        errors += 1

def word_count(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return len(f.read().split())
    except:
        return 0

def file_contains(path, text):
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return text in f.read()
    except:
        return False

def file_size(path):
    try:
        return os.path.getsize(path)
    except:
        return 0

# 1. audit_report_phase10.md exists (>800 words)
p1 = os.path.join(STUDIO, "15-DEPLOY-AND-FUNNEL-BRIDGE", "audit_report_phase10.md")
check("audit_report_phase10.md exists >800 words", os.path.exists(p1) and word_count(p1) > 800)

# 2. freelancer-os-app.html size >360000 bytes AND contains specific strings
p2 = os.path.join(STUDIO, "07-INTERACTIVE-TOOLS", "freelancer-os-app.html")
sz2 = file_size(p2)
has_addEhrRow = file_contains(p2, "addEhrRow")
has_exportWorkspace = file_contains(p2, "exportWorkspace")
has_tier2teaser = file_contains(p2, "tier2teaser")
check("freelancer-os-app.html size >360000 bytes", sz2 > 360000)
check("freelancer-os-app.html contains addEhrRow", has_addEhrRow)
check("freelancer-os-app.html contains exportWorkspace", has_exportWorkspace)
check("freelancer-os-app.html contains tier2teaser", has_tier2teaser)

# 3. tier0-free-lite-command-sheet.xlsx exists (>5000 bytes)
p3 = os.path.join(STUDIO, "06-NOTION-TEMPLATES", "Spreadsheets", "tier0-free-lite-command-sheet.xlsx")
check("tier0-free-lite-command-sheet.xlsx exists >5000 bytes", os.path.exists(p3) and file_size(p3) > 5000)

# 4. START-HERE-LAUNCHPAD.html in studio root (>10000 bytes)
p4 = os.path.join(STUDIO, "START-HERE-LAUNCHPAD.html")
check("START-HERE-LAUNCHPAD.html exists in studio root >10000 bytes", os.path.exists(p4) and file_size(p4) > 10000)

# 5. funnel-links-config.json exists and is valid JSON
p5 = os.path.join(STUDIO, "15-DEPLOY-AND-FUNNEL-BRIDGE", "funnel-links-config.json")
valid_json = False
if os.path.exists(p5):
    try:
        with open(p5, 'r', encoding='utf-8') as f:
            json.load(f)
        valid_json = True
    except:
        pass
check("funnel-links-config.json exists and valid JSON", valid_json)

# 6. inject_funnel_links.py exists
p6 = os.path.join(STUDIO, "15-DEPLOY-AND-FUNNEL-BRIDGE", "inject_funnel_links.py")
check("inject_funnel_links.py exists", os.path.exists(p6))

# 7. web-live-demo/index.html exists (>5000 bytes)
p7 = os.path.join(STUDIO, "15-DEPLOY-AND-FUNNEL-BRIDGE", "web-live-demo", "index.html")
check("web-live-demo/index.html exists >5000 bytes", os.path.exists(p7) and file_size(p7) > 5000)

# 8. VIRAL-TRAFFIC-AND-FUNNEL-PLAYBOOK.md exists (>1500 words)
p8 = os.path.join(STUDIO, "15-DEPLOY-AND-FUNNEL-BRIDGE", "VIRAL-TRAFFIC-AND-FUNNEL-PLAYBOOK.md")
wc8 = word_count(p8)
print(f"  [info] VIRAL playbook word count: {wc8}")
check("VIRAL-TRAFFIC-AND-FUNNEL-PLAYBOOK.md exists >1500 words", os.path.exists(p8) and wc8 > 1500)

# 9. OWNER-MANUAL-SETUP-GUIDE-BANGLA.md exists (>1500 words)
p9 = os.path.join(STUDIO, "15-DEPLOY-AND-FUNNEL-BRIDGE", "OWNER-MANUAL-SETUP-GUIDE-BANGLA.md")
wc9 = word_count(p9)
print(f"  [info] Bangla guide word count: {wc9}")
check("OWNER-MANUAL-SETUP-GUIDE-BANGLA.md exists >1500 words", os.path.exists(p9) and wc9 > 1500)

# 10. OMAR SUNNY present in START-HERE-LAUNCHPAD.html
check("OMAR SUNNY present in START-HERE-LAUNCHPAD.html", file_contains(p4, "OMAR SUNNY"))

# 11. Zero banned words in VIRAL playbook and Bangla guide
BANNED = ['delve', 'tapestry', 'testament', 'beacon', 'symphony', 'unleash', 'supercharge',
          'game-changer', 'game changer', 'pivotal', 'foster']

def check_banned(path, label):
    if not os.path.exists(path):
        check(f"No banned words in {label}", False)
        return
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read().lower()
    found = [w for w in BANNED if w in text]
    if found:
        print(f"  [info] Banned words found in {label}: {found}")
    check(f"No banned words in {label}", len(found) == 0)

check_banned(p8, "VIRAL-TRAFFIC-AND-FUNNEL-PLAYBOOK.md")
check_banned(p9, "OWNER-MANUAL-SETUP-GUIDE-BANGLA.md")

print(f"\nVERIFICATION COMPLETE: {errors} ERRORS")
