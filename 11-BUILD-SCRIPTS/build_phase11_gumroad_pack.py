#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 11 Deterministic Builder Script (11-BUILD-SCRIPTS/build_phase11_gumroad_pack.py)
The AI Freelancer Operating System — Digital Knowledge Product Studio
Author & System Architect: OMAR SUNNY

Builds:
1. 3 Gumroad 600x600 (1:1 Square) Discover & Profile Grid Thumbnails (.svg + .png) in 08-COVER-DESIGN/:
   - 11-gumroad-square-thumb-listing1-free-audit-600x600.svg & .png (600 x 600 px)
   - 12-gumroad-square-thumb-listing2-flagship-os-600x600.svg & .png (600 x 600 px)
   - 13-gumroad-square-thumb-listing3-vip-membership-600x600.svg & .png (600 x 600 px)
2. Copies all 600x600 Square Thumbnails and 1280x720 16:9 Covers into:
   - 10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/
3. Generates 5 Exhaustive, Field-by-Field Gumroad Master Setup & AI Image Prompt Playbooks in
   10-MARKETING/Gumroad-Hybrid-Master-Setup/:
   - 01-LISTING-1-FREE-STARTER-KIT-EXACT-FIELDS.md (>= 1,500 words)
   - 02-LISTING-2-FLAGSHIP-3-VERSION-PRODUCT-EXACT-FIELDS.md (>= 2,500 words)
   - 03-LISTING-3-VIP-RECURRING-MEMBERSHIP-EXACT-FIELDS.md (>= 1,800 words)
   - 04-GUMROAD-CHECKOUT-UPSELLS-COUPONS-AND-WORKFLOWS.md (>= 1,800 words)
   - 05-AI-COVER-AND-THUMBNAIL-IMAGE-GENERATION-PROMPTS.md (>= 1,800 words)
4. Updates Tier4-Living-OS-Pro-Vault-Membership-Pack.zip (and creates alias
   tier4-vip-living-career-vault-edition.zip if needed by external scripts) with the Phase 11 Gumroad pack.
"""

import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
COVERS_DIR = BASE_DIR / "08-COVER-DESIGN"
MARKETING_DIR = BASE_DIR / "10-MARKETING"
GUMROAD_SETUP_DIR = MARKETING_DIR / "Gumroad-Hybrid-Master-Setup"
THUMBS_COVERS_DIR = GUMROAD_SETUP_DIR / "Thumbnails-and-Covers"
HYBRID_BUNDLE_DIR = BASE_DIR / "09-EXPORTS" / "HYBRID-BUNDLE"
CHEAT_DIR = BASE_DIR / "13-VISUAL-CHEAT-SHEETS"


def find_headless_browser() -> str:
    """Locate Microsoft Edge or Google Chrome on Windows for exact 600x600 PNG rendering."""
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path_str in candidates:
        if Path(path_str).exists():
            return path_str
    raise RuntimeError("No headless Chromium browser (msedge.exe or chrome.exe) found on system.")


def render_svg_to_exact_png(browser_exe: str, svg_path: Path, png_path: Path, width: int = 600, height: int = 600):
    """Render an SVG file to an exact width x height PNG via headless Edge/Chrome."""
    svg_content = svg_path.read_text(encoding="utf-8")
    html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: {width}px; height: {height}px; overflow: hidden; background: #0B1120; }}
  svg {{ width: {width}px; height: {height}px; display: block; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""
    png_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_html = Path(tmpdir) / "thumb_render.html"
        tmp_html.write_text(html_doc, encoding="utf-8")
        cmd = [
            browser_exe,
            "--headless",
            "--disable-gpu",
            f"--window-size={width},{height}",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--screenshot={str(png_path)}",
            tmp_html.as_uri(),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ==============================================================================
# STEP 1: GENERATE 3 SQUARE 600x600 (1:1) GUMROAD DISCOVER THUMBNAIL SVGs & PNGs
# ==============================================================================
def build_square_thumb_listing1_svg() -> str:
    """600 x 600 px (1:1 Square) Thumbnail for Listing 1 ($0 Free 7-Day Leak Audit Starter Kit)."""
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <defs>
    <linearGradient id="bg1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070B14"/>
      <stop offset="55%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
    <linearGradient id="tealGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0D9488"/>
      <stop offset="100%" stop-color="#0284C7"/>
    </linearGradient>
  </defs>

  <!-- Canvas Background -->
  <rect width="600" height="600" fill="url(#bg1)"/>
  <rect x="10" y="10" width="580" height="580" rx="22" fill="none" stroke="#1E293B" stroke-width="2"/>
  <rect x="0" y="0" width="600" height="10" fill="url(#tealGrad)"/>

  <!-- Top Badge Bar -->
  <rect x="32" y="30" width="320" height="40" rx="8" fill="#0D9488"/>
  <text x="192" y="56" font-family="JetBrains Mono, Consolas, monospace" font-size="16" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="1.5">$0 FREE AUDIT STARTER KIT</text>
  <rect x="368" y="30" width="200" height="40" rx="8" fill="#1E293B" stroke="#0284C7" stroke-width="1.5"/>
  <text x="468" y="55" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="700" fill="#38BDF8" text-anchor="middle">8 FILES INCLUDED</text>

  <!-- Headline Hierarchy -->
  <text x="32" y="108" font-family="Inter, Arial, sans-serif" font-size="15" font-weight="800" fill="#2DD4BF" letter-spacing="2.5">15-MINUTE DIAGNOSTIC SYSTEM</text>
  <text x="32" y="154" font-family="Inter, Arial, sans-serif" font-size="42" font-weight="900" fill="#FFFFFF" letter-spacing="-1">7-DAY TIME &amp;</text>
  <text x="32" y="200" font-family="Inter, Arial, sans-serif" font-size="42" font-weight="900" fill="#38BDF8" letter-spacing="-1">EHR LEAK AUDIT</text>
  <text x="32" y="232" font-family="Inter, Arial, sans-serif" font-size="15.5" font-weight="600" fill="#CBD5E1">Calculate True Effective Hourly Rate + Stop Shadow Labor</text>

  <!-- Center 3D Stack / Diagnostic Card Graphic -->
  <rect x="32" y="254" width="536" height="238" rx="16" fill="#0B1120" stroke="#0D9488" stroke-width="2"/>
  <rect x="32" y="254" width="536" height="38" rx="16" fill="#162238"/>
  <text x="52" y="278" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#2DD4BF">STARTER KIT STACK // INSTANT DOWNLOAD</text>
  <text x="548" y="278" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#38BDF8" text-anchor="end">EHR CALCULATOR</text>

  <!-- 3 Visual Deliverable Pills Inside Stack -->
  <g transform="translate(50, 306)">
    <rect x="0" y="0" width="500" height="48" rx="8" fill="#1E293B" stroke="#0284C7" stroke-width="1.5"/>
    <rect x="0" y="0" width="96" height="48" rx="8" fill="#0284C7"/>
    <text x="48" y="30" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#FFFFFF" text-anchor="middle">BOOK + PDF</text>
    <text x="112" y="23" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="800" fill="#FFFFFF">Chapter 1 Operating Manual + Fillable Workbook</text>
    <text x="112" y="40" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="500" fill="#94A3B8">5-Stage Operating Model &amp; 4-Bucket Shadow Labor Audit</text>
  </g>

  <g transform="translate(50, 364)">
    <rect x="0" y="0" width="500" height="48" rx="8" fill="#1E293B" stroke="#0D9488" stroke-width="1.5"/>
    <rect x="0" y="0" width="96" height="48" rx="8" fill="#0D9488"/>
    <text x="48" y="30" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#FFFFFF" text-anchor="middle">WEB APP</text>
    <text x="112" y="23" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="800" fill="#FFFFFF">Offline HTML5 EHR Leak Calculator + Daily Planner</text>
    <text x="112" y="40" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="500" fill="#94A3B8">Runs in Any Browser (`freelancer-os-app.html`) + CSV Sheet</text>
  </g>

  <g transform="translate(50, 422)">
    <rect x="0" y="0" width="500" height="48" rx="8" fill="#1E293B" stroke="#F59E0B" stroke-width="1.5"/>
    <rect x="0" y="0" width="96" height="48" rx="8" fill="#D97706"/>
    <text x="48" y="30" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#FFFFFF" text-anchor="middle">2 POSTERS</text>
    <text x="112" y="23" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="800" fill="#FFFFFF">Master 5-Gate Ecosystem Map + Ch 1 Visual Cheat Sheet</text>
    <text x="112" y="40" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="500" fill="#94A3B8">High-Res Infographics for Desk Reference (`1600x1100` &amp; `1200x1600`)</text>
  </g>

  <!-- Bottom Author & System Architect Attribution Bar -->
  <rect x="32" y="510" width="536" height="62" rx="12" fill="#1E293B" stroke="#334155" stroke-width="1.5"/>
  <text x="300" y="535" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="800" fill="#38BDF8" text-anchor="middle" letter-spacing="2">THE AI FREELANCER OPERATING SYSTEM</text>
  <text x="300" y="557" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="3">BY OMAR SUNNY • SYSTEM ARCHITECT: OMAR SUNNY</text>

  <rect x="0" y="590" width="600" height="10" fill="url(#tealGrad)"/>
</svg>"""


def build_square_thumb_listing2_svg() -> str:
    """600 x 600 px (1:1 Square) Thumbnail for Listing 2 ($19 / $39 / $59 Flagship 3-Tier AI Freelancer OS)."""
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <defs>
    <linearGradient id="bg2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070B14"/>
      <stop offset="50%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284C7"/>
      <stop offset="50%" stop-color="#0D9488"/>
      <stop offset="100%" stop-color="#F59E0B"/>
    </linearGradient>
  </defs>

  <!-- Canvas Background -->
  <rect width="600" height="600" fill="url(#bg2)"/>
  <rect x="10" y="10" width="580" height="580" rx="22" fill="none" stroke="#334155" stroke-width="2"/>
  <rect x="0" y="0" width="600" height="10" fill="url(#goldGrad)"/>

  <!-- Top Gold & Sky Badges -->
  <rect x="32" y="28" width="334" height="40" rx="8" fill="#D97706"/>
  <text x="199" y="54" font-family="JetBrains Mono, Consolas, monospace" font-size="15.5" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="1.5">COMPLETE AI FREELANCER OS</text>
  <rect x="380" y="28" width="188" height="40" rx="8" fill="#0284C7"/>
  <text x="474" y="53" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#FFFFFF" text-anchor="middle">3 TIER EDITIONS</text>

  <!-- Main Headline Block -->
  <text x="32" y="102" font-family="Inter, Arial, sans-serif" font-size="14.5" font-weight="800" fill="#FBBF24" letter-spacing="2.2">5-GATE CLIENT, PRICING &amp; EXECUTION SYSTEM</text>
  <text x="32" y="148" font-family="Inter, Arial, sans-serif" font-size="42" font-weight="900" fill="#FFFFFF" letter-spacing="-1">THE AI FREELANCER</text>
  <text x="32" y="192" font-family="Inter, Arial, sans-serif" font-size="40" font-weight="900" fill="#38BDF8" letter-spacing="-1">OPERATING SYSTEM</text>
  <text x="32" y="222" font-family="JetBrains Mono, Consolas, monospace" font-size="12.5" font-weight="700" fill="#2DD4BF">50 AI PROMPTS • WEB APP • 8-TAB EXCEL • NOTION OS</text>

  <!-- Center 3D Multi-Device & 8-Pillar Grid -->
  <rect x="32" y="242" width="536" height="252" rx="16" fill="#0B1120" stroke="#0284C7" stroke-width="2"/>
  <rect x="32" y="242" width="536" height="36" rx="16" fill="#1E293B"/>
  <text x="52" y="265" font-family="JetBrains Mono, Consolas, monospace" font-size="12.5" font-weight="800" fill="#38BDF8">FLAGSHIP 83-FILE HYBRID BUNDLE</text>
  <text x="548" y="265" font-family="JetBrains Mono, Consolas, monospace" font-size="12.5" font-weight="800" fill="#FBBF24" text-anchor="end">$19 • $39 • $59</text>

  <!-- 2x2 Feature Cards Inside Center Box -->
  <g transform="translate(48, 290)">
    <rect x="0" y="0" width="244" height="88" rx="10" fill="#1E293B" stroke="#0284C7" stroke-width="1.5"/>
    <text x="14" y="24" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="800" fill="#38BDF8">01 // BOOKS &amp; VISUAL ATLAS</text>
    <text x="14" y="46" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">168p Manual + 12p Visual Atlas</text>
    <text x="14" y="66" font-family="Inter, Arial, sans-serif" font-size="11.5" fill="#CBD5E1">EPUB 3.0 + US Letter/A4 + iPad Planner</text>

    <rect x="260" y="0" width="244" height="88" rx="10" fill="#1E293B" stroke="#0D9488" stroke-width="1.5"/>
    <text x="274" y="24" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="800" fill="#2DD4BF">02 // PRO SAAS-LITE WEB APP</text>
    <text x="274" y="46" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">4 Interactive Browser Modules</text>
    <text x="274" y="66" font-family="Inter, Arial, sans-serif" font-size="11.5" fill="#CBD5E1">EHR Audit, B.C.R. Pricer &amp; 62 Prompts</text>

    <rect x="0" y="100" width="244" height="88" rx="10" fill="#1E293B" stroke="#F59E0B" stroke-width="1.5"/>
    <rect x="0" y="100" width="244" height="88" rx="10" fill="#1E293B" stroke="#F59E0B" stroke-width="1.5"/>
    <text x="14" y="124" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="800" fill="#FBBF24">03 // 8-TAB EXCEL + NOTION OS</text>
    <text x="14" y="146" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">299 Formulas + 4 Live Charts</text>
    <text x="14" y="166" font-family="Inter, Arial, sans-serif" font-size="11.5" fill="#CBD5E1">5 Notion Databases + Invoice &amp; Tax</text>

    <rect x="260" y="100" width="244" height="88" rx="10" fill="#1E293B" stroke="#38BDF8" stroke-width="1.5"/>
    <text x="274" y="124" font-family="JetBrains Mono, Consolas, monospace" font-size="12" font-weight="800" fill="#38BDF8">04 // WORD, PPTX &amp; AUTOMATION</text>
    <text x="274" y="146" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">7 Word Docs + 3 PPTX Decks</text>
    <text x="274" y="166" font-family="Inter, Arial, sans-serif" font-size="11.5" fill="#CBD5E1">MSA Contract, Proposal + 3 JSON Flows</text>
  </g>

  <!-- Bottom Author & System Architect Attribution Bar -->
  <rect x="32" y="510" width="536" height="62" rx="12" fill="#1E293B" stroke="#0284C7" stroke-width="1.5"/>
  <text x="300" y="535" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="800" fill="#FBBF24" text-anchor="middle" letter-spacing="2">DIGITAL KNOWLEDGE PRODUCT STUDIO • FLAGSHIP EDITION</text>
  <text x="300" y="557" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="3">BY OMAR SUNNY • SYSTEM ARCHITECT: OMAR SUNNY</text>

  <rect x="0" y="590" width="600" height="10" fill="url(#goldGrad)"/>
</svg>"""


def build_square_thumb_listing3_svg() -> str:
    """600 x 600 px (1:1 Square) Thumbnail for Listing 3 ($9/mo or $49/yr VIP Living OS Membership Vault)."""
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <defs>
    <linearGradient id="bg3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#060B16"/>
      <stop offset="50%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#162238"/>
    </linearGradient>
    <linearGradient id="vipGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="50%" stop-color="#0284C7"/>
      <stop offset="100%" stop-color="#0D9488"/>
    </linearGradient>
  </defs>

  <!-- Canvas Background -->
  <rect width="600" height="600" fill="url(#bg3)"/>
  <rect x="10" y="10" width="580" height="580" rx="22" fill="none" stroke="#F59E0B" stroke-width="2" opacity="0.65"/>
  <rect x="0" y="0" width="600" height="10" fill="url(#vipGrad)"/>

  <!-- Top VIP Membership Badges -->
  <rect x="32" y="28" width="310" height="40" rx="8" fill="#D97706"/>
  <text x="187" y="54" font-family="JetBrains Mono, Consolas, monospace" font-size="16" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="1.5">VIP MONTHLY VAULT PASS</text>
  <rect x="358" y="28" width="210" height="40" rx="8" fill="#1E293B" stroke="#F59E0B" stroke-width="1.5"/>
  <text x="463" y="53" font-family="JetBrains Mono, Consolas, monospace" font-size="14" font-weight="800" fill="#FBBF24" text-anchor="middle">$9/MO OR $49/YR</text>

  <!-- Main Headline Block -->
  <text x="32" y="104" font-family="Inter, Arial, sans-serif" font-size="14.5" font-weight="800" fill="#38BDF8" letter-spacing="2.2">CONTINUOUS AI WORKFLOW &amp; SCRIPT EXPANSION</text>
  <text x="32" y="150" font-family="Inter, Arial, sans-serif" font-size="42" font-weight="900" fill="#FFFFFF" letter-spacing="-1">LIVING FREELANCER</text>
  <text x="32" y="194" font-family="Inter, Arial, sans-serif" font-size="42" font-weight="900" fill="#FBBF24" letter-spacing="-1">PRO VAULT PASS</text>
  <text x="32" y="224" font-family="JetBrains Mono, Consolas, monospace" font-size="12.5" font-weight="700" fill="#2DD4BF">MONTHLY NICHE WORKFLOWS, SCRIPTS &amp; FULL FLAGSHIP OS</text>

  <!-- Center Membership Benefits Stack -->
  <rect x="32" y="246" width="536" height="248" rx="16" fill="#0B1120" stroke="#F59E0B" stroke-width="2"/>
  <rect x="32" y="246" width="536" height="36" rx="16" fill="#1E293B"/>
  <text x="52" y="269" font-family="JetBrains Mono, Consolas, monospace" font-size="12.5" font-weight="800" fill="#FBBF24">VIP MEMBER ACCESS // 84 FILES + MONTHLY DROPS</text>
  <text x="548" y="269" font-family="JetBrains Mono, Consolas, monospace" font-size="12.5" font-weight="800" fill="#2DD4BF" text-anchor="end">SAVE 55% YEARLY</text>

  <g transform="translate(50, 296)">
    <rect x="0" y="0" width="500" height="54" rx="8" fill="#1E293B" stroke="#F59E0B" stroke-width="1.5"/>
    <rect x="0" y="0" width="110" height="54" rx="8" fill="#D97706"/>
    <text x="55" y="33" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#FFFFFF" text-anchor="middle">FULL OS KIT</text>
    <text x="126" y="24" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="800" fill="#FFFFFF">Instant Access to Entire 83-File Tier 3 Flagship OS</text>
    <text x="126" y="43" font-family="Inter, Arial, sans-serif" font-size="12" fill="#CBD5E1">All Books, Workbooks, Web App, 8-Tab Excel, Word &amp; PPTX</text>
  </g>

  <g transform="translate(50, 360)">
    <rect x="0" y="0" width="500" height="54" rx="8" fill="#1E293B" stroke="#0284C7" stroke-width="1.5"/>
    <rect x="0" y="0" width="110" height="54" rx="8" fill="#0284C7"/>
    <text x="55" y="33" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#FFFFFF" text-anchor="middle">MONTHLY DROP</text>
    <text x="126" y="24" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="800" fill="#FFFFFF">5 New High-Ticket AI Workflows + 3 Scripts Monthly</text>
    <text x="126" y="43" font-family="Inter, Arial, sans-serif" font-size="12" fill="#CBD5E1">Includes Drop #01: Paid Diagnostic &amp; Retainer Expansion Pack</text>
  </g>

  <g transform="translate(50, 424)">
    <rect x="0" y="0" width="500" height="54" rx="8" fill="#1E293B" stroke="#0D9488" stroke-width="1.5"/>
    <rect x="0" y="0" width="110" height="54" rx="8" fill="#0D9488"/>
    <text x="55" y="33" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#FFFFFF" text-anchor="middle">PRO TOOLS</text>
    <text x="126" y="24" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="800" fill="#FFFFFF">Continuous LLM Calibration &amp; All New Web Calculators</text>
    <text x="126" y="43" font-family="Inter, Arial, sans-serif" font-size="12" fill="#CBD5E1">Tuned for Claude, GPT &amp; Gemini + Priority Template Updates</text>
  </g>

  <!-- Bottom Author & System Architect Attribution Bar -->
  <rect x="32" y="510" width="536" height="62" rx="12" fill="#1E293B" stroke="#F59E0B" stroke-width="1.5"/>
  <text x="300" y="535" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="800" fill="#38BDF8" text-anchor="middle" letter-spacing="2">THE AI FREELANCER OPERATING SYSTEM • VIP VAULT</text>
  <text x="300" y="557" font-family="JetBrains Mono, Consolas, monospace" font-size="13" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="3">BY OMAR SUNNY • SYSTEM ARCHITECT: OMAR SUNNY</text>

  <rect x="0" y="590" width="600" height="10" fill="url(#vipGrad)"/>
</svg>"""


def build_square_thumbnails_and_copy_covers():
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    THUMBS_COVERS_DIR.mkdir(parents=True, exist_ok=True)
    browser_exe = find_headless_browser()

    thumbs_spec = [
        ("11-gumroad-square-thumb-listing1-free-audit-600x600", build_square_thumb_listing1_svg()),
        ("12-gumroad-square-thumb-listing2-flagship-os-600x600", build_square_thumb_listing2_svg()),
        ("13-gumroad-square-thumb-listing3-vip-membership-600x600", build_square_thumb_listing3_svg()),
    ]

    for base_name, svg_str in thumbs_spec:
        svg_path = COVERS_DIR / f"{base_name}.svg"
        png_path = COVERS_DIR / f"{base_name}.png"
        svg_path.write_text(svg_str, encoding="utf-8")
        render_svg_to_exact_png(browser_exe, svg_path, png_path, 600, 600)
        shutil.copy2(svg_path, THUMBS_COVERS_DIR / svg_path.name)
        shutil.copy2(png_path, THUMBS_COVERS_DIR / png_path.name)

    # Copy existing 1280x720 Gumroad covers + Ecosystem Master Poster into Thumbnails-and-Covers/
    cover_mappings = [
        (COVERS_DIR / "gumroad-tier0-free-audit-cover.png", [
            "gumroad-tier0-free-audit-cover.png",
            "03-gumroad-tier0-free-audit-cover.png",
            "06-gumroad-cover-tier0-lead-magnet-1280x720.png",
            "03-gumroad-cover-tier1-core-1280x720.png",
        ]),
        (COVERS_DIR / "gumroad-tier2-workbook-edition-cover.png", [
            "gumroad-tier2-workbook-edition-cover.png",
            "04-gumroad-tier2-workbook-edition-cover.png",
            "04-gumroad-cover-tier2-pro-os-1280x720.png",
        ]),
        (COVERS_DIR / "gumroad-tier3-complete-os-cover.png", [
            "gumroad-tier3-complete-os-cover.png",
            "05-gumroad-tier3-flagship-bundle-cover.png",
            "05-gumroad-cover-tier3-complete-suite-1280x720.png",
        ]),
        (COVERS_DIR / "gumroad-tier4-living-os-membership-cover.png", [
            "gumroad-tier4-living-os-membership-cover.png",
            "06-gumroad-tier4-vip-vault-cover.png",
        ]),
    ]
    for src_p, target_names in cover_mappings:
        if src_p.exists():
            for tname in target_names:
                shutil.copy2(src_p, THUMBS_COVERS_DIR / tname)

    poster_src = CHEAT_DIR / "00-ECOSYSTEM-MASTER-MAP-POSTER.png"
    if poster_src.exists():
        shutil.copy2(poster_src, THUMBS_COVERS_DIR / "00-ECOSYSTEM-MASTER-MAP-POSTER.png")

    print("[Step 1] Built 3 Square 600x600 SVG/PNG Thumbnails and synced all covers to 10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/.")


# ==============================================================================
# STEP 2: GENERATE THE 5 MASTER GUMROAD CONFIGURATION & PROMPT PLAYBOOKS
# ==============================================================================
def build_gumroad_playbooks():
    GUMROAD_SETUP_DIR.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------------------------
    # FILE 1: 01-LISTING-1-FREE-STARTER-KIT-EXACT-FIELDS.md (>= 1,500 words)
    # --------------------------------------------------------------------------
    file1_md = """# GUMROAD HYBRID MASTER SETUP — LISTING 1: FREE `$0+` 7-DAY TIME & REVENUE LEAK AUDIT STARTER KIT
**Product Ecosystem:** *The AI Freelancer Operating System: A Practical System to Organize Clients, Automate Repetitive Work, Manage Projects, and Build a More Productive Freelance Business*  
**Author & System Architect:** `OMAR SUNNY` (`BY OMAR SUNNY` / `SYSTEM ARCHITECT: OMAR SUNNY`)  
**Target Gumroad Architecture:** Listing 1 of 3 (Top-of-Funnel Lead Magnet & Pay-What-You-Want Acquisition Engine)

---

## 1. STRATEGIC ROLE OF LISTING 1 IN YOUR 3-LISTING GUMROAD ECOSYSTEM

In Gumroad's marketplace algorithm, a standalone `$0+` (*Pay What You Want*) product listing serves three critical commercial functions that cannot be achieved by hiding a free tier inside a paid listing:

1. **Frictionless Email List & Customer Record Capture:** Every person who downloads **Listing 1** at `$0` is permanently added to your Gumroad **Audience / Customers** database, enabling your automated 5-Email Gumroad Workflow sequence and future product broadcast launches.
2. **Accelerated 5-Star Social Proof Velocity:** Free and `$5` tip downloaders leave verified `5.0 ★` Gumroad ratings at `4x–6x` the rate of cold `$59` buyers, rapidly building authority across your entire Gumroad creator profile (`BY OMAR SUNNY`) and boosting your placement in the **Gumroad Discover** feed.
3. **Instant Checkout Cross-Sell Trigger:** The moment a visitor clicks **`I want this!`** on Listing 1, Gumroad's native **Checkout Upsell** modal fires automatically, offering them a `$10 OFF` instant upgrade to **Listing 2 -> Version 3 (Complete Flagship AI Freelancer OS Bundle)**.

---

## 2. STEP 1 — NEW PRODUCT CREATION SCREEN (INITIAL SETUP)

Log into your Gumroad Creator Dashboard (`https://app.gumroad.com/products`), click **`New product`** in the top-right corner, and enter these exact values:

| Gumroad Field Name | Exact Value to Enter / Select | Operational Notes |
| :--- | :--- | :--- |
| **Name** | `Free 7-Day Freelancer Time, EHR & Revenue Leak Audit (AI Freelancer OS Starter Kit — By OMAR SUNNY)` | Includes primary search keywords (`Freelancer`, `EHR`, `Revenue Leak Audit`, `AI Freelancer OS`, `OMAR SUNNY`). |
| **Type** | Select **`Digital product`** | Standard downloadable bundle with instant browser access. |
| **Price** | Enter **`0`** (USD `$`) | Activates `$0` free download mode; configured as Pay-What-You-Want on the next screen. |
| **Action** | Click **`Next: Customize`** | Opens the main Product Editor tab. |

---

## 3. STEP 2 — PRODUCT TAB: EXACT FIELD-BY-FIELD CONFIGURATION

Inside the **Product** tab of the Gumroad editor, copy and paste the exact values below into each corresponding field:

### A. Name & URL Slug (`General` Section)
- **Name:**
  ```text
  Free 7-Day Freelancer Time, EHR & Revenue Leak Audit (AI Freelancer OS Starter Kit — By OMAR SUNNY)
  ```
- **URL (`gumroad.com/l/...`):**
  ```text
  ai-freelancer-audit-kit
  ```
  *(Your clean public share URL becomes `https://[your-username].gumroad.com/l/ai-freelancer-audit-kit`)*

### B. Thumbnail (`600 × 600 px` `1:1` Square Discover Card)
- **Where It Appears:** Gumroad Discover marketplace search results, your public Creator Profile grid, and checkout cart previews.
- **Exact File to Upload:**
  ```text
  10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/11-gumroad-square-thumb-listing1-free-audit-600x600.png
  ```
  *(Also located in `08-COVER-DESIGN/11-gumroad-square-thumb-listing1-free-audit-600x600.png` — verified exact `600 × 600 px` PNG with `$0 FREE AUDIT STARTER KIT` badge and `BY OMAR SUNNY` micro-typography).*

### C. Cover (`1280 × 720 px` `16:9` Product Header Banner)
- **Where It Appears:** Top hero banner of the product landing page.
- **Exact File to Upload:**
  ```text
  10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/03-gumroad-tier0-free-audit-cover.png
  ```
  *(Also available as `gumroad-tier0-free-audit-cover.png` in the same folder).*

### D. Pricing & Pay-What-You-Want Configuration
- **Amount:** `$0`
- **Toggle ON:** `[x] Allow customers to pay what they want`
  - **Minimum amount:** `$0`
  - **Suggested amount:** `$5`
  *(Setting `$0` minimum and `$5` suggested allows 100% free downloads while capturing voluntary `$5–$15` coffee tips from appreciative freelancers).*

### E. Product Info — Call to Action, Summary & Additional Details (Right Sidebar)
- **Call to action:** Select **`I want this!`** from the dropdown.
- **Summary (Right Sidebar Callout Box — Copy-Paste Exactly):**
  ```text
  Diagnose your hidden shadow-labor leaks in 15 minutes flat. Includes Complete Sample Chapter 1 PDF, Fillable Worksheet 1.1 PDF, Offline HTML5 EHR Leak Calculator Web App, Google Sheets/Excel Audit CSV, and 2 High-Resolution System Posters. Architected by OMAR SUNNY.
  ```
- **Additional details (Click `Add detail` 5 times and enter these exact `Attribute` : `Value` pairs):**

| Attribute (Left Box) | Value (Right Box) |
| :--- | :--- |
| `Author & Architect` | `OMAR SUNNY` |
| `Edition` | `2026 Starter Diagnostic Kit (v1.0)` |
| `Included Formats` | `PDF + Offline HTML5 Web App + CSV + 2 High-Res Posters` |
| `License` | `Personal & Freelance Studio Use` |
| `Instant Access` | `8 Verified Files (1.76 MB ZIP + Direct Files)` |

---

## 4. STEP 3 — FULL COPY-PASTE RICH-TEXT DESCRIPTION (PRODUCT BODY)

Copy and paste the entire formatted copy block below directly into the Gumroad **Description** editor:

```markdown
### Why Do Skilled Freelancers Working 50 Hours a Week Still Plateau at $26.80/Hour?

If you bill clients **$75 to $100/hour** (or **$3,000 to $5,000 per project**), why does your bank account at the end of the month look like you are earning **$26/hour**?

Because **45.4% of the average independent freelancer's workweek is consumed by Unbilled Shadow Labor**:
* **Bucket B (Client Friction & Scope Creep):** Chasing missing client logins, clarifying vague feedback across 4 stakeholders, and executing "quick 15-minute favors" for free.
* **Bucket C (Unpaid Sales & Proposal Drag):** Sitting on 45-minute discovery calls with low-budget shoppers and spending 3.5 hours writing custom proposals that get ghosted.
* **Bucket D (Admin & Context-Switching Drag):** Answering reactive Slack and email messages every 20 minutes during your peak morning cognitive hours.

Before you write another proposal or take another discovery call, run this **15-Minute 7-Day Time, Effective Hourly Rate (EHR) & Revenue Leak Audit** architected by **OMAR SUNNY**.

---

### What You Get Inside This Free 8-File Starter Kit (`$0+` Instant Download)

1. **`tier0-free-sample-chapter01-and-audit.pdf` (Complete Chapter 1 Operating Manual):**
   Read Chapter 1 of *The AI Freelancer Operating System* (`7,235 words`), including the **5-Stage Client Lifecycle Model**, the **Marcus Vance Case Study** (`$26.80/hr` to `$49.33/hr` in 30 days), the **Daily 3-Block Operating Rhythm**, and **5 Tested AI Prompts (`Prompts 1.1–1.5`)**.
2. **`chapter-01-workbook.pdf` (Fillable Action Workbook for Chapter 1):**
   Interactive AcroForm fillable PDF containing *Worksheet 1.1: The 7-Day Time & Revenue Leak Audit*, the **5-Gate Bottleneck Scorecard**, and the **90-Minute Morning Maker Block Charter**.
3. **`freelancer-os-app.html` (Offline/Online SaaS-Lite Web Companion App):**
   Double-click to open in Chrome, Edge, Safari, or Firefox with zero installation or cloud login required. **Module 1 (7-Day EHR Leak Calculator & Daily 3-Block Priority Planner)** is 100% open in Free Mode!
4. **`sheet1-ehr-leak-audit.csv` (Spreadsheet Diagnostic Template):**
   Ready for Google Sheets, Microsoft Excel, or Apple Numbers to log your 4 weekly time buckets and compute your annualized revenue leak automatically.
5. **`00-ECOSYSTEM-MASTER-MAP-POSTER.png` (`1600 × 1100 px` Master Wall Poster):**
   High-resolution visual map of all **5 Lifecycle Gates**, **10 Chapters**, **50 AI Prompts**, **12 Client Boundary Scripts**, and plug-and-play software tools.
6. **`cheat-sheet-ch01.png` (`1200 × 1600 px` 60-Second Visual Cheat Sheet):**
   One-page infographic distilling Chapter 1's formulas, 4-step execution pipeline, 5 AI prompt triggers, and red-flag circuit breakers.
7. **`START-HERE-TIER0.md` & Official Edition Cover:**
   Step-by-step 15-minute quickstart instructions.

---

### How to Run Your 15-Minute Leak Audit Today

* **Step 1 (3 Minutes):** Open `freelancer-os-app.html` in your browser and enter your last 7 days of working hours across **Buckets A, B, C, and D** alongside your weekly gross revenue.
* **Step 2 (2 Minutes):** Read your **Realized Effective Hourly Rate (EHR)** and your **Annualized 48-Week Unbilled Revenue Leak** (`$79,200/year` for the average practitioner).
* **Step 3 (5 Minutes):** Score your business from `1 to 5` across the **5 Client Lifecycle Gates** (`Attract`, `Scope & Price`, `Onboard`, `Execute & Defend`, `Offboard & Retain`) to pinpoint your #1 failing gate.
* **Step 4 (5 Minutes):** Copy and run **Prompt 1.1 (The 7-Day Time & Revenue Leak Auditor)** and **Prompt 1.5 (The Async Communication Boundary Setter)** in Claude, ChatGPT, or Gemini.

---

### Ready for the Complete 83-File Flagship Operating System?

When you are ready to install all **5 Lifecycle Gates**, **50 Tested AI Prompts**, **12 Emergency Client Boundary Scripts**, the **Full Pro Web App**, the **8-Tab Charted Excel Command Center**, the **5-Database Notion OS Kit**, **7 Editable Word Contracts/Proposals**, and **3 PowerPoint Pitch Decks**, upgrade to the full edition here:

👉 **[Get The Complete AI Freelancer Operating System Flagship Bundle (`Listing 2`)](https://gumroad.com/l/ai-freelancer-os)**

---
**System Architect & Author:** `OMAR SUNNY`  
*Digital Knowledge Product Studio — Engineered for Independent Freelancers, Consultants, Designers, Developers & Solopreneurs in the US, UK, Canada, and Australia.*
```

---

## 5. STEP 4 — CONTENT TAB CONFIGURATION (DELIVERABLE UPLOAD & RECEIPT NOTE)

Click the **`Content`** tab at the top of the Gumroad Product Editor and configure the delivery view that customers see immediately after checkout:

1. **Upload the Master Starter Kit Archive:**
   - Click **`Upload files`** -> **`Computer files`** and select:
     ```text
     09-EXPORTS/HYBRID-BUNDLE/Tier0-Free-Leak-Audit-Starter-Kit.zip
     ```
2. **Optional Individual File Uploads (For 1-Click Mobile Preview Inside Gumroad Library):**
   - You may also upload `09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf`, `05-WORKBOOKS/chapter-01-workbook.pdf`, and `13-VISUAL-CHEAT-SHEETS/cheat-sheet-ch01.png` directly beneath the `.zip` archive so mobile readers can preview the PDFs directly inside the Gumroad app.
3. **Add Welcome & Upgrade Note Above the File Download Box (Copy-Paste Into Content Editor):**
   ```markdown
   ### Welcome to The AI Freelancer Operating System Starter Kit! (By OMAR SUNNY)

   Thank you for downloading the **Free 7-Day Time, EHR & Revenue Leak Audit Starter Kit**.

   **Quickstart Instructions:**
   1. Download and unzip `Tier0-Free-Leak-Audit-Starter-Kit.zip` on your computer.
   2. Double-click **`freelancer-os-app.html`** to launch the interactive **EHR Leak Calculator & Daily 3-Block Priority Planner** in any browser.
   3. Open **`tier0-free-sample-chapter01-and-audit.pdf`** and **`cheat-sheet-ch01.png`** to run your 15-minute diagnostic.

   ---
   **Want to Activate All 4 Pro Web App Modules + All 83 Flagship Files ($10 OFF)?**
   Your Web Companion App (`freelancer-os-app.html`) already contains Module 2 (*B.C.R. 3-Tier Proposal Pricing Engine*), Module 3 (*62-Item AI Prompt & Script Builder*), and Module 4 (*20-Min Friday CEO Scorecard*).
   Upgrade to the **Tier 3 Complete Flagship OS Bundle** using code **`SUBSCRIBER15`** (15% OFF) at:
   https://gumroad.com/l/ai-freelancer-os
   ```

---

## 6. STEP 5 — SHARE TAB & GUMROAD DISCOVER MARKETPLACE SETTINGS

Click **`Save and continue`** to advance to the **Share** tab, and configure your **Gumroad Discover** settings at the bottom of the page:

| Discover Setting | Exact Value / Selection |
| :--- | :--- |
| **Category** | `Business & Money > Careers` (or `Education > How-To`) |
| **Tags (Max 5 Tags)** | `freelance`, `ai prompts`, `notion template`, `consulting`, `productivity` |
| **Display your product's 1-5 star rating** | **Toggle ON `[x]`** |
| **Show this product on your Gumroad profile** | **Toggle ON `[x]`** (`Pin to top of profile` alongside Listing 2) |

Click **`Publish and continue`** to make **Listing 1** live!
"""
    (GUMROAD_SETUP_DIR / "01-LISTING-1-FREE-STARTER-KIT-EXACT-FIELDS.md").write_text(file1_md, encoding="utf-8")

    # --------------------------------------------------------------------------
    # FILE 2: 02-LISTING-2-FLAGSHIP-3-VERSION-PRODUCT-EXACT-FIELDS.md (>= 2,500 words)
    # --------------------------------------------------------------------------
    file2_md = """# GUMROAD HYBRID MASTER SETUP — LISTING 2: FLAGSHIP 3-VERSION PRODUCT (`$19` / `$39` / `$59` OR `$19` / `$24` / `$49`)
**Product Ecosystem:** *The AI Freelancer Operating System: A Practical System to Organize Clients, Automate Repetitive Work, Manage Projects, and Build a More Productive Freelance Business*  
**Author & System Architect:** `OMAR SUNNY` (`BY OMAR SUNNY` / `SYSTEM ARCHITECT: OMAR SUNNY`)  
**Target Gumroad Architecture:** Listing 2 of 3 (Primary Commercial Revenue Engine Using Gumroad's Native 3-Version Tier Selector)

---

## 1. WHY LISTING 2 USES GUMROAD'S 3-VERSION PRICING ARCHITECTURE

Rather than scattering your paid editions across three separate Gumroad pages—which splits your customer reviews, fragments your conversion traffic, and forces buyers to click back and forth to compare features—**Listing 2 consolidates all three one-time commercial tiers onto a single high-converting flagship product page**:

1. **Unified Social Proof & Discover Authority:** Every sale across Tier 1, Tier 2, and Tier 3 accumulates on **one product URL (`gumroad.com/l/ai-freelancer-os`)**, rapidly pushing your listing to the top of Gumroad Discover's *Best Selling* sort filter.
2. **Built-In Decoy Anchoring Psychology:** When buyers land on Listing 2, they see all three versions stacked side-by-side above the **`I want this!`** button:
   - **Version 1 (Base Entry Tier — `$19` [or `$15`]):** *Tier 1: Core Book, Print & EPUB Edition* (`9 files`)
   - **Version 2 (Mid Decoy Tier — `$39` [or `$24`]):** *Tier 2: Interactive Workbook, 12-Page Visual Atlas & Tablet Planner Edition* (`40 files`)
   - **Version 3 (Hero Flagship Tier — `$59` [or `$49`]):** *⭐ Tier 3: Complete Flagship AI Freelancer OS Bundle — MOST POPULAR* (`83 files`)
3. **65%+ Hero Tier Selection Rate:** Because moving from Version 2 (`$39`) to Version 3 (`$59`) is only `+$20` (or moving from `$24` to `$49` is `+$25`) and adds the **Pro Offline Web App (`freelancer-os-app.html`)**, the **8-Tab Charted Excel Command Center**, the **5-Database Notion OS Kit**, **7 Editable Word Contracts/Proposals**, **3 PowerPoint Pitch Decks**, the **Design Customizer Studio**, and **3 JSON Automation Blueprints**, over 65% of buyers select **Version 3**.

---

## 2. STEP 1 — NEW PRODUCT CREATION SCREEN (INITIAL SETUP)

In your Gumroad Dashboard (`https://app.gumroad.com/products`), click **`New product`** and enter these exact initial fields:

| Gumroad Field Name | Exact Value to Enter / Select | Operational Notes |
| :--- | :--- | :--- |
| **Name** | `The AI Freelancer Operating System: Complete Client, Pricing, Project & Automation System (By OMAR SUNNY)` | High-authority flagship title with author attribution. |
| **Type** | Select **`Digital product`** | Enables multi-version tiered pricing (`Versions` section). |
| **Price** | Enter **`19`** (USD `$`) | Sets the base entry price for Version 1 (`+$0`). Versions 2 and 3 add `+$20` and `+$40` (or `+$5` and `+$30` for `$19/$24/$49`). |
| **Action** | Click **`Next: Customize`** | Opens the main Product Editor tab. |

---

## 3. STEP 2 — PRODUCT TAB: EXACT VISUALS, PRICING & CALLOUT ATTRIBUTES

### A. Name & URL Slug (`General` Section)
- **Name:**
  ```text
  The AI Freelancer Operating System: Complete Client, Pricing, Project & Automation System (By OMAR SUNNY)
  ```
- **URL (`gumroad.com/l/...`):**
  ```text
  ai-freelancer-os
  ```

### B. Thumbnail (`600 × 600 px` `1:1` Square Discover Card)
- **Exact File to Upload:**
  ```text
  10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/12-gumroad-square-thumb-listing2-flagship-os-600x600.png
  ```
  *(Also located at `08-COVER-DESIGN/12-gumroad-square-thumb-listing2-flagship-os-600x600.png` — verified exact `600 × 600 px` square thumbnail with gold `COMPLETE AI FREELANCER OS` badge and `BY OMAR SUNNY` credit).*

### C. Multi-Slide Cover Carousel (`1280 × 720 px` `16:9` Order)
Upload these three `1280 × 720` / high-res visuals in this exact sequence so buyers can swipe through your ecosystem at the top of the page:
1. **Slide 1 (Hero Flagship Cover):**
   `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/05-gumroad-tier3-flagship-bundle-cover.png`
2. **Slide 2 (Workbook, Planner & Visual Atlas Cover):**
   `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/04-gumroad-tier2-workbook-edition-cover.png`
3. **Slide 3 (Master 5-Gate Ecosystem Architecture Map):**
   `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/00-ECOSYSTEM-MASTER-MAP-POSTER.png`

### D. Base Price & Purchasing Power Parity (PPP) Settings
- **Price:** `$19`
- **Allow customers to pay what they want:** Leave **OFF `[ ]`**
- **Purchasing Power Parity (Under `Settings -> Payments` or Product Pricing):** Toggle **ON `[x]`** with a maximum discount cap of **`40%`** so international freelancers outside the US/UK/CA/AU convert at high volume without eroding your core Western pricing.

### E. Call to Action, Summary & 8 Additional Details (Right Sidebar)
- **Call to action:** Select **`I want this!`**
- **Summary (Right Sidebar Callout Box — Copy-Paste Exactly):**
  ```text
  The complete 5-Gate Operating System for independent freelancers, consultants & solo agencies. Includes 75,158-Word Manual, 12-Page Visual Shortcut Atlas, 50 AI Prompts, 12 Boundary Scripts, Offline SaaS Web App, 8-Tab Charted Excel Matrix, 5-DB Notion OS, 7 Editable Word Contracts/Proposals & 3 PowerPoint Decks. By OMAR SUNNY.
  ```
- **Additional details (Click `Add detail` 8 times and enter these exact `Attribute` : `Value` pairs):**

| Attribute (Left Box) | Value (Right Box) |
| :--- | :--- |
| `System Architect & Author` | `OMAR SUNNY` |
| `Core Operating Manual` | `168 Pages (75,158 Words) in PDF, EPUB 3.0, Print & Word .DOCX` |
| `Visual Shortcut Atlas` | `12-Page Full-Color Infographic Atlas PDF + 31 Vector SVGs/PNGs` |
| `AI Prompts & Scripts` | `50 Tested AI Workflow Prompts + 12 Client Boundary Scripts` |
| `Interactive Software` | `Offline HTML5 Web App (freelancer-os-app.html) + Design Studio` |
| `Excel & Notion Systems` | `8-Tab Charted Excel Command Center (299 Formulas) + 5-DB Notion OS` |
| `Agency Office Suite` | `7 Editable Word (.docx) Contracts/Proposals + 3 PPTX Decks (32 Slides)` |
| `Automation Blueprints` | `3 Importable Make.com / Zapier / n8n JSON Workflow Files` |

---

## 4. STEP 3 — FULL COPY-PASTE RICH-TEXT DESCRIPTION (FLAGSHIP SALES PAGE)

Copy and paste the complete sales copy below into the Gumroad **Description** editor:

```markdown
### Stop Running a High-Skill Freelance Practice on Reactive Inbox Chaos

Most independent freelancers, consultants, designers, developers, and copywriters earning **$2,000 to $8,000/month** do not have a craft problem. They have an **operating system problem**.

Without deterministic client gates, nearly half of your workweek disappears into **Unbilled Shadow Labor**:
* **Unqualified Discovery Calls & 3.5-Hour Custom Proposals** that get ghosted or haggled down on price.
* **Underquoted Fixed-Scope Projects** priced on optimistic hours with zero complexity or risk buffer.
* **Week-1 Onboarding Stalls** where you wait 11 days for missing client logos, copy decks, and platform logins.
* **Informal Slack Scope Creep** (*"Hey, quick 10-minute favor?"*) and contradictory revisions from 4 different client stakeholders.
* **The Feast-or-Famine Revenue Rollercoaster** because completed projects end with a messy zip file instead of a structured **48-Hour Offboard-to-Retainer Bridge**.

**The AI Freelancer Operating System** (architected by **OMAR SUNNY**) replaces ad-hoc freelancing with a **5-Gate Commercial Operating System** combining books, visual cheat sheets, interactive browser software, charted Excel models, Notion databases, editable Microsoft Word contracts, PowerPoint pitch decks, and no-code automation blueprints.

---

### The 5-Gate Client Lifecycle & Margin Protection Architecture

1. **GATE 01 — Attract, Diagnose & Productize (`Chapters 1–2`):**
   Audit your 4 weekly time buckets, calculate your **True Effective Hourly Rate (EHR)**, lock your daily **90-Minute Morning Maker Block**, and replace custom hourly quotes with a **3-Tier Productized Offer Matrix** (`Option 1 Baseline`, `Option 2 Core Transformation`, `Option 3 Turnkey Partner`).
2. **GATE 02 — 10-Minute Lead Triage, Rapid Proposals & B.C.R. Pricing (`Chapters 3–4`):**
   Filter every inbound lead asynchronously with the **20-Point P.A.C.E. Lead Scorer**, draft complete **3-Tier B.R.I.E.F. Proposals** in 10 minutes, price every project with the **B.C.R. Formula (`Base + Complexity + Risk Buffer`)**, and defeat discount requests using the **Zero-Discount Scope Trade-Down Protocol**.
3. **GATE 03 — Zero-Friction 48-Hour Client Onboarding (`Chapter 5`):**
   Provision your single-link **Notion Client Command Portal** in 3 minutes and enforce the **48-Hour Pre-Flight Asset Gate** and **Day-for-Day Timeline Shift Rule** so you never start production before 50% deposit clearance and 100% asset verification.
4. **GATE 04 — 20/60/20 AI Execution, 4-Gate QA & P.V.P. Scope Defense (`Chapters 6–8`):**
   Execute deliverables 42% faster using the **20/60/20 Sandwich Protocol** (`20% Human Architecture -> 60% AI Build -> 20% 4-Gate Red-Team QA`), convert out-of-scope requests into **$450–$950 paid Change Orders** via **Pause-Validate-Price (P.V.P.)**, and eliminate 85% of status meetings with the **3-Pillar Friday Digest & 3-Minute Loom Walkthrough**.
5. **GATE 05 — Executive Offboarding, Retainer Conversion & Weekly CEO Scaling (`Chapters 9–10`):**
   Deliver a branded **Final Handover Certificate + 3 Custom Video SOPs**, pitch the **3-Tier Monthly Retainer Menu (`$1,250 / $2,400 / $4,200/mo`)** within 48 hours of launch, and run the **20-Minute Friday CEO Review** to prune low-EHR "Whale-Trap" clients and trigger automatic **+20% rate increases** whenever booked capacity crosses `85%`.

---

### Everything Inside the Flagship Ecosystem (8 Integrated Product Suites)

#### 1. The 10-Chapter Operating Manual & 12-Page Visual Shortcut Atlas
* **Complete 168-Page Digital Book PDF (`75,158 words`)**, **Reflowable EPUB 3.0**, and **146-Page KDP 6"×9" Print Interior PDF**.
* **NEW — The 12-Page 60-Second Visual Shortcut Atlas PDF (`13-VISUAL-CHEAT-SHEETS/`):** Don't want to read 75,000 words first? Scan the giant **`00-ECOSYSTEM-MASTER-MAP-POSTER`** plus **10 One-Page Chapter Visual Cheat Sheets** (`.PDF`, `.SVG` & `.PNG`) to master every formula, 4-step pipeline, and AI prompt trigger in 60 seconds flat.

#### 2. The 50 Tested AI Workflow Prompts & 12 Emergency Boundary Scripts
* **50 Copy-Ready AI Prompts (`Prompts 1.1–10.5`)** engineered for Claude, ChatGPT, and Gemini with `[BRACKETED VARIABLES]`, operational objectives, execution triggers, and mandatory human QA verification rules.
* **12 Word-for-Word Emergency Client Scripts (`Scripts 1–12`)** for deflecting unpaid discovery calls, defending prices without discounting, enforcing missing-asset holds, pricing mid-sprint Change Orders, pausing work on overdue invoices (`Day +3 / +7 / +14`), and resetting legacy client rates by `+25%`.

#### 3. Offline/Online SaaS-Lite Interactive Web Companion App (`freelancer-os-app.html`)
* Zero-dependency, single-file HTML5 application (`318 KB`) that runs offline in any desktop or mobile browser (`Pro Key Included: FREELANCER-OS-PRO-2026`):
  * **Module 1:** *7-Day EHR Leak Calculator & Daily 3-Block Priority Planner*
  * **Module 2:** *8-Line WBS Estimator, B.C.R. 3-Tier Proposal Pricing Engine & Zero-Discount Scope Trade-Down Generator*
  * **Module 3:** *Dynamic 62-Item AI Prompt & Boundary Script Studio Builder with Live Variable Interpolation*
  * **Module 4:** *20-Minute Friday CEO Dashboard, 80/20 Client Profitability Matrix & 85% Capacity Rate-Raise Trigger* (`localStorage` + `.JSON` / `.CSV` / Print-PDF export)

#### 4. The 8-Tab Charted Excel Command Center (`299 Live Formulas` + `4 Native Charts`)
* **`the-ai-freelancer-os-financial-and-pricing-matrix.xlsx`** (+ 8 standalone CSV sheets for Google Sheets / Numbers):
  * **Tab 00 (`00_Executive_Visual_Dashboard`):** Master KPI Command Center with **3 Embedded Native Excel Charts** (`12-Week Cashflow BarChart`, `4-Bucket Hours PieChart`, `12-Month Profit LineChart`).
  * **Tab 01 (`01_EHR_Leak_Audit`):** 7-Day Leak Audit + 5-Gate Bottleneck Scorecard + embedded `PieChart`.
  * **Tab 02 (`02_BCR_Scope_Pricing`):** 8-Row WBS Estimator + B.C.R. 3-Tier Pricing Engine + 50/25/25 Milestone Split.
  * **Tab 03 (`03_Client_80_20_Roster`):** 8-Client Profitability Roster + Whale-Trap Detector + 85% Capacity Trigger.
  * **Tab 04 (`04_90Day_Pipeline_Cashflow`):** 12-Week Rolling Cashflow, Retainer Baseline & 25% Tax Reserve Forecaster.
  * **Tab 05 (`05_Client_Invoice_Generator`):** Print-ready Client Milestone & Change Order Invoice (`#INV-2026-104`).
  * **Tab 06 (`06_Daily_3Block_Time_Log`):** 30-Day Daily Maker Block, Deep-Work Ratio & Realized EHR Tracker.
  * **Tab 07 (`07_Annual_Tax_Expense_Ledger`):** 12-Month Business Expense, Deduction & Quarterly Tax Ledger (`US Schedule C / UK Self-Assessment / CA T2125 / AU Sole Trader`).

#### 5. The 5-Database Minimalist Notion Freelancer OS Import Kit
* Sub-15-minute weekly maintenance Notion system: `01-Leads-CRM-Pipeline.csv`, `02-Active-Projects-and-Gates.csv`, `03-AI-Prompt-and-Script-Vault-62.csv`, `04-Weekly-CEO-Scorecard-Log.csv`, `05-Client-Portal-and-Handover-Hub.md`, and the complete `NOTION-OS-SETUP-AND-FORMULAS-GUIDE.md`.

#### 6. The 7-Document Editable Microsoft Word (`.docx`) Suite
* `01-Editable-Complete-Book-Manuscript.docx` (`72,558 words`)
* `02-Editable-10-Chapter-Action-Workbook.docx` (`9,969 words`)
* `03-Client-3-Tier-BRIEF-Proposal-Template.docx` (`1,462 words`)
* `04-Master-Service-Agreement-and-SOW-Contract.docx` (`2,031 words` — Full MSA + SOW legal contract)
* `05-PVP-Formal-Change-Order-Request-Form.docx` (`659 words` — Formal `CO-#` addendum)
* `06-Client-Welcome-Packet-and-48h-Onboarding-Guide.docx` (`1,186 words`)
* `07-Final-Handover-Certificate-and-90Day-Retainer-Pitch.docx` (`1,038 words`)

#### 7. The 3 Editable Widescreen `16:9` PowerPoint (`.pptx`) Pitch Decks (`32 Slides + Notes`)
* `01-Discovery-and-3-Tier-Proposal-Pitch-Deck.pptx` (`12 slides` with word-for-word presenter scripts)
* `02-Client-Kickoff-and-48h-Alignment-Deck.pptx` (`10 slides` with presenter scripts)
* `03-ROI-Case-Study-and-90Day-Retainer-Pitch-Deck.pptx` (`10 slides` with presenter scripts)

#### 8. Interactive Photo/Cover Design Customizer Studio & 3 JSON Automation Blueprints
* **`design-customizer-studio.html` (`80.6 KB`):** Customize 6 visual templates (`eBook Cover`, `Gumroad Banner`, `Proposal Cover`, `LinkedIn Header`, `Case Study Card`, `Video Thumbnail`), upload your own headshot or agency logo via `FileReader`, switch across 5 brand color themes, and export high-resolution `.PNG` & `.SVG` graphics in 1 click.
* **3 Importable Make.com / Zapier / n8n JSON Automation Blueprints (`01`..`03`):** Automate inbound P.A.C.E. lead scoring + B.R.I.E.F. proposal drafting, Stripe deposit -> Notion Client Portal provisioning, and Friday 14:00 CEO Scorecard digests.

---

### Compare the 3 Editions (Select Your Tier in the Sidebar)

| Ecosystem Component | Tier 1: Core Book Edition (`$19`) | Tier 2: Workbook & Visual Atlas (`$39` / `$24`) | ⭐ Tier 3: Complete Flagship OS (`$59` / `$49`) |
| :--- | :---: | :---: | :---: |
| **168-Page Manual PDF + EPUB 3.0 + Print PDF** | ✅ Included | ✅ Included | ✅ Included |
| **50 Tested AI Prompts + 12 Boundary Scripts** | ✅ Included | ✅ Included | ✅ Included |
| **12-Page Visual Shortcut Atlas PDF + 31 SVGs** | ❌ | ✅ Included | ✅ Included |
| **US Letter & A4 Fillable PDF + Word Workbooks** | ❌ | ✅ Included | ✅ Included |
| **49-Page Landscape iPad / Tablet Digital Planner** | ❌ | ✅ Included | ✅ Included |
| **Pro Offline SaaS Web App (`FREELANCER-OS-PRO-2026`)** | ❌ | ❌ | ✅ **Included (Full Pro)** |
| **8-Tab Charted Excel Command Center (`299 Formulas`)** | ❌ | ❌ | ✅ **Included** |
| **5-Database Minimalist Notion OS Import Kit** | ❌ | ❌ | ✅ **Included** |
| **7 Editable Word Contracts, Proposals & Docs (`.docx`)** | ❌ | Workbook Only | ✅ **All 7 Docs Included** |
| **3 Widescreen PowerPoint Pitch Decks (`32 Slides`)** | ❌ | ❌ | ✅ **All 3 Decks Included** |
| **Photo/Cover Design Studio + 3 JSON Automations** | ❌ | ❌ | ✅ **Included** |

---
**System Architect & Author:** `OMAR SUNNY`  
*Select **Tier 3: Complete Flagship AI Freelancer OS Bundle** on the right and click **I want this!** for instant lifetime access to all 83 files.*
```

---

## 5. STEP 4 — EXACT "VERSIONS" CONFIGURATION (PRODUCT TAB -> VERSIONS)

Scroll down to the **`Versions`** section inside the **Product** tab, click **`Add version`** three times, and enter these exact configurations.

> **Pricing Flexibility Note:** Below is the primary **`$19 / $39 / $59`** high-margin pricing matrix (with the alternative **`$19 / $24 / $49`** matrix shown in parentheses if you prefer a sub-`$50` anchor price).

### Version 1 — Base Entry Tier (`$19` Total)
- **Version Name:**
  ```text
  Tier 1: Core Book, EPUB 3.0 & Print-Ready Edition ($19)
  ```
- **Version Description:**
  ```text
  Complete 168-Page Flagship Digital Book (PDF) + Reflowable EPUB 3.0 eBook + 146-Page 6"x9" Print Paperback Interior PDF + High-Res Covers. Includes all 10 Chapters (75,158 words), 50 Tested AI Workflow Prompts & 12 Emergency Client Boundary Scripts.
  ```
- **Additional amount:** Enter **`0`** (`$19` Base + `$0` = **`$19 Total`**)
- **Quantity:** Leave blank (unlimited)

### Version 2 — Mid Decoy Tier (`$39` Total [or `$24` Total])
- **Version Name:**
  ```text
  Tier 2: Interactive Workbook, 12-Page Visual Shortcut Atlas & Tablet Planner Edition ($39)
  ```
- **Version Description:**
  ```text
  Everything in Tier 1 PLUS: 12-Page Full-Color 60-Second Visual Shortcut Atlas PDF, US Letter & ISO A4 Fillable Action Workbooks, Editable Microsoft Word 10-Chapter Workbook (.docx), 49-Page Landscape iPad/Tablet Digital Planner PDF, 62-Item Prompt Vault CSV & 31 Vector Diagrams/Cheat-Sheet SVGs (40 Files Total).
  ```
- **Additional amount:** Enter **`20`** (`$19` Base + `$20` = **`$39 Total`**; or enter **`5`** for **`$24 Total`**)

### Version 3 — Hero Flagship Tier (`$59` Total [or `$49` Total] — Default Top Recommendation)
- **Version Name:**
  ```text
  ⭐ Tier 3: Complete Flagship AI Freelancer OS Bundle — MOST POPULAR ($59)
  ```
- **Version Description:**
  ```text
  Complete 83-File Agency & Freelancer Ecosystem: Everything in Tier 2 + Full Pro Offline Web Companion App (Pro Key: FREELANCER-OS-PRO-2026) + 8-Tab Charted Excel Command Center (299 Formulas + 4 Charts) + 5-Database Notion OS Kit + All 7 Editable Word Contracts & Proposals (MSA/SOW, 3-Tier BRIEF Proposal, Change Order, Welcome Packet, Handover Certificate) + 3 PowerPoint Pitch Decks (32 Slides) + Interactive Photo/Cover Customizer Studio + 3 Make/Zapier/n8n JSON Automation Blueprints.
  ```
- **Additional amount:** Enter **`40`** (`$19` Base + `$40` = **`$59 Total`**; or enter **`30`** for **`$49 Total`**)

---

## 6. STEP 5 — CONTENT TAB SETUP (MAPPING THE 3 ZIP BUNDLES TO EACH VERSION)

Click the **`Content`** tab at the top of the Gumroad Product Editor. Because you created 3 versions, Gumroad displays a version selector dropdown on the left side of the Content editor so each buyer receives the exact files for the version they purchased:

| Selected Version in Content Editor | Exact ZIP Archive to Upload (`09-EXPORTS/HYBRID-BUNDLE/`) | File Count & Size | Custom Welcome Note & License Key to Paste Above Download Box |
| :--- | :--- | :---: | :--- |
| **Version 1 (`Tier 1: Core Book Edition`)** | `Tier1-KDP-and-D2D-Publisher-Upload-Pack.zip` *(or upload `the-ai-freelancer-os-complete-book.pdf` + `the-ai-freelancer-os.epub`)* | `9 files` (`8.02 MB`) | *"Welcome to Tier 1 of The AI Freelancer Operating System (By OMAR SUNNY)! Download your complete 168-page Digital Manual PDF and Reflowable EPUB 3.0 below."* |
| **Version 2 (`Tier 2: Workbook & Visual Atlas`)** | `Tier2-Interactive-Workbook-and-Planner-Edition.zip` | `40 files` (`5.70 MB`) | *"Welcome to Tier 2 (Workbook, 12-Page Visual Shortcut Atlas & Tablet Planner Edition — By OMAR SUNNY)! Start by opening `the-ai-freelancer-os-visual-shortcut-atlas.pdf` and `02-Editable-10-Chapter-Action-Workbook.docx`."* |
| **Version 3 (`⭐ Tier 3: Complete Flagship OS`)** | `Tier3-Complete-AI-Freelancer-OS-Flagship-Bundle.zip` | `83 files` (`9.87 MB`) | *"Welcome to Tier 3: The Complete Flagship AI Freelancer Operating System (By OMAR SUNNY)! **Your Pro Web App Activation Key:** `FREELANCER-OS-PRO-2026`. Unzip the archive and open `START-HERE-TIER3-COMPLETE-OS.md` and `02-INTERACTIVE-WEB-APP/freelancer-os-app.html` to begin!"* |

---

## 7. STEP 6 — SHARE TAB & GUMROAD DISCOVER MARKETPLACE SETTINGS

Click **`Save and continue`** to open the **Share** tab and configure Discover:
- **Category:** `Business & Money > Management & Leadership` (or `Business & Money > Entrepreneurship`)
- **Tags (5 Tags):** `freelancer`, `notion template`, `ai prompts`, `proposal template`, `business system`
- **Display your product's 1-5 star rating:** **Toggle ON `[x]`**
- **Show this product on your Gumroad profile:** **Toggle ON `[x]`**

Click **`Publish and continue`** to launch **Listing 2**!
"""
    (GUMROAD_SETUP_DIR / "02-LISTING-2-FLAGSHIP-3-VERSION-PRODUCT-EXACT-FIELDS.md").write_text(file2_md, encoding="utf-8")

    # --------------------------------------------------------------------------
    # FILE 3: 03-LISTING-3-VIP-RECURRING-MEMBERSHIP-EXACT-FIELDS.md (>= 1,800 words)
    # --------------------------------------------------------------------------
    file3_md = """# GUMROAD HYBRID MASTER SETUP — LISTING 3: VIP LIVING FREELANCER OS & PRO WORKFLOW VAULT MEMBERSHIP (`$9/MO` OR `$49/YR`)
**Product Ecosystem:** *The AI Freelancer Operating System: A Practical System to Organize Clients, Automate Repetitive Work, Manage Projects, and Build a More Productive Freelance Business*  
**Author & System Architect:** `OMAR SUNNY` (`BY OMAR SUNNY` / `SYSTEM ARCHITECT: OMAR SUNNY`)  
**Target Gumroad Architecture:** Listing 3 of 3 (Recurring Monthly & Annual Subscription MRR Engine)

---

## 1. STRATEGIC ROLE OF LISTING 3 (RECURRING SUBSCRIPTION ENGINE)

In Gumroad's platform architecture, a **`Membership`** product operates on recurring Stripe/PayPal subscription billing (`Monthly` and `Yearly` cycles) whereas a **`Digital product`** operates on one-time checkout. Creating **Listing 3** as a dedicated Gumroad **`Membership`** gives your studio three powerful recurring revenue advantages:

1. **Compounding Monthly & Annual Recurring Revenue (MRR / ARR):** Every subscriber who selects the `$9/month` or `$49/year` plan generates predictable recurring cashflow for your digital publishing studio.
2. **The `$49/Year` Annual Anchor Conversion Play:** By setting the monthly plan at `$9/month` (`$108/year` annualized) and the annual plan at **`$49/year` (`Save 55%`)** with `Yearly` set as the default billing frequency, a large percentage of buyers choose the `$49/year` recurring membership because it costs the same upfront as a one-time flagship purchase while including **12 months of continuous monthly prompt drops, negotiation scripts, and new web micro-tools**.
3. **Post-Purchase Checkout Add-On for Listing 1 & Listing 2 Buyers:** Using Gumroad's **Checkout Upsells**, you can offer Listing 3 as a 1-click add-on at checkout so one-time book/workbook buyers upgrade into recurring VIP members.

---

## 2. STEP 1 — NEW PRODUCT CREATION SCREEN (INITIAL SETUP)

In your Gumroad Dashboard (`https://app.gumroad.com/products`), click **`New product`** and enter these exact initial fields:

| Gumroad Field Name | Exact Value to Enter / Select | Operational Notes |
| :--- | :--- | :--- |
| **Name** | `VIP Living Freelancer OS & Pro Workflow Vault Membership (Full Flagship OS + Monthly AI Drops — By OMAR SUNNY)` | Explicitly communicates that members get the Full OS + Monthly Drops. |
| **Type** | Select **`Membership`** | Activates recurring Monthly (`$9/mo`) and Yearly (`$49/yr`) billing schedules. |
| **Price** | Enter **`9`** (USD `$` / `per month`) | We will add the `$49 / year` (Save 55%) billing option on the next screen. |
| **Action** | Click **`Next: Customize`** | Opens the Membership Product Editor tab. |

---

## 3. STEP 2 — PRODUCT TAB: VISUALS, TIERS & BILLING FREQUENCY SETUP

### A. Name & URL Slug (`General` Section)
- **Name:**
  ```text
  VIP Living Freelancer OS & Pro Workflow Vault Membership (Full Flagship OS + Monthly AI Drops — By OMAR SUNNY)
  ```
- **URL (`gumroad.com/l/...`):**
  ```text
  ai-freelancer-vip-vault
  ```

### B. Thumbnail (`600 × 600 px` `1:1` Square Discover Card)
- **Exact File to Upload:**
  ```text
  10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/13-gumroad-square-thumb-listing3-vip-membership-600x600.png
  ```
  *(Also located at `08-COVER-DESIGN/13-gumroad-square-thumb-listing3-vip-membership-600x600.png` — verified exact `600 × 600 px` square thumbnail with gold `VIP MONTHLY VAULT PASS` badge and `BY OMAR SUNNY` credit).*

### C. Cover Banner (`1280 × 720 px` `16:9` Product Header)
- **Exact File to Upload:**
  ```text
  10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/06-gumroad-tier4-vip-vault-cover.png
  ```
  *(Also available as `gumroad-tier4-living-os-membership-cover.png` in the same folder).*

### D. Membership Tiers & Dual Billing Frequency Configuration (`Tiers` Section)
Under the **`Tiers`** section of the Membership editor, click the default tier card and enter these exact settings:

| Membership Tier Setting | Exact Value to Enter / Select |
| :--- | :--- |
| **Tier Name** | `VIP Executive Freelancer Vault Pass (Full 84-File OS + Monthly AI Drops)` |
| **Tier Description** | `Instant access to the entire 84-File Flagship AI Freelancer Operating System Bundle (Pro Web App, 8-Tab Charted Excel, 5-DB Notion OS, 7 Word Contracts/Proposals, 3 PPTX Decks, 12-Page Visual Atlas & 3 JSON Automations) PLUS Monthly Role-Specific AI Workflow Packs, Advanced Client Negotiation Scripts & All Future Studio Web Micro-Tools.` |
| **Monthly Price (`every month`)** | **`$9`** |
| **Yearly Price (`every year`)** | Toggle ON **`[x] Yearly`** and enter **`$49`** *(Automatically displays `Save 55%` badge to buyers)* |
| **Default payment frequency** | Select **`Yearly`** *(or `Monthly` if you want a lower `$9` entry sticker price on your profile grid)* |
| **Free Trial** | Leave **OFF `[ ]`** *(Because members receive immediate download access to all 84 files on Day 1, never enable a $0 trial on downloadable digital vaults).* |

### E. Membership Settings Checkboxes
- **`[x] New members will have access to all previous posts`:** Toggle **ON** so every new subscriber immediately gets `Drop #01` (`tier4-monthly-vault-drop-01.md`) and all future monthly drops inside their Gumroad Library.
- **`[x] Show number of members`:** Toggle **ON** once you pass 25 active members.

### F. Summary & 6 Additional Details (Right Sidebar)
- **Call to action:** Select **`Join`** or **`Subscribe`**
- **Summary (Right Sidebar Callout Box — Copy-Paste Exactly):**
  ```text
  Get instant access to the entire 84-File Flagship AI Freelancer Operating System PLUS monthly high-ticket AI workflow drops, niche-calibrated prompt chains, enterprise negotiation scripts, and lifetime updates to all studio web tools. Architected by OMAR SUNNY.
  ```
- **Additional details (Click `Add detail` 6 times):**

| Attribute (Left Box) | Value (Right Box) |
| :--- | :--- |
| `System Architect & Author` | `OMAR SUNNY` |
| `Day-1 Instant Vault` | `All 84 Flagship Files Included (Books, Web App, Excel, Notion, Word, PPTX)` |
| `Monthly Expansion Drops` | `5 New Niche AI Workflows + 3 Negotiation Scripts Every Month` |
| `Included Drop #01` | `High-Ticket Paid Diagnostic & Retainer Expansion Pack (2,804 Words)` |
| `Pro Web App License` | `FREELANCER-OS-PRO-2026 (Full 4-Module Pro Access)` |
| `Billing Flexibility` | `$9/Month or $49/Year (Save 55% — Cancel Anytime in 1 Click)` |

---

## 4. STEP 3 — FULL COPY-PASTE RICH-TEXT DESCRIPTION (VIP MEMBERSHIP PAGE)

Copy and paste the complete membership sales copy below into the Gumroad **Description** editor:

```markdown
### Keep Your Freelance Operating System Calibrated as AI Models & Client Markets Evolve

When you join the **VIP Living Freelancer OS & Pro Workflow Vault Membership** (architected by **OMAR SUNNY**), you do not just get a monthly newsletter—you get **immediate Day-1 access to the entire 84-file Flagship AI Freelancer Operating System Bundle** PLUS continuous monthly expansion packs engineered to help you close higher-ticket diagnostic sprints and recurring retainers.

---

### Part 1: What You Get Instantly on Day 1 (The Complete 84-File Flagship Vault)

The moment you join (at **`$9/month`** or **`$49/year — Save 55%`**), you receive immediate download access to every single asset in our flagship ecosystem:

1. **All Book, Workbook & Visual Shortcut Editions (`01-BOOK-AND-WORKBOOKS/`):**
   * Complete 168-Page Operating Manual PDF (`75,158 words`) & Reflowable EPUB 3.0.
   * **12-Page 60-Second Visual Shortcut Atlas PDF** + **31 Vector Diagrams & Cheat-Sheet Posters (`.SVG` & `.PNG`)**.
   * **US Letter (`8.5"×11"`) & ISO A4 Fillable Workbooks** + **49-Page Landscape iPad/Tablet Digital Planner**.
2. **Full Pro Offline/Online SaaS Web Companion App (`02-INTERACTIVE-WEB-APP/`):**
   * `freelancer-os-app.html` (`318 KB`) with your Pro Activation Key (**`FREELANCER-OS-PRO-2026`**) activating all 4 interactive modules (*EHR Leak Audit*, *B.C.R. 3-Tier Proposal Pricer*, *62-Item Prompt/Script Studio*, and *20-Minute Friday CEO Dashboard*).
3. **The 5-Database Minimalist Notion Freelancer OS (`03-NOTION-OS-KIT/`):**
   * `01-Leads-CRM-Pipeline.csv`, `02-Active-Projects-and-Gates.csv`, `03-AI-Prompt-and-Script-Vault-62.csv`, `04-Weekly-CEO-Scorecard-Log.csv`, `05-Client-Portal-and-Handover-Hub.md` & Setup Guide.
4. **The 8-Tab Charted Excel Command Center (`04-EXCEL-AND-CSV-MATRIX/`):**
   * `the-ai-freelancer-os-financial-and-pricing-matrix.xlsx` (`299 live formulas` + `4 embedded native Excel charts`) covering Executive Dashboard, EHR Audit, B.C.R. Pricing, 80/20 Client Roster, 90-Day Cashflow, Client Invoice Generator, 30-Day Time Log & 12-Month Tax Ledger.
5. **The 7 Editable Microsoft Word Contracts & Proposals + 3 PowerPoint Decks (`06-EDITABLE-WORD-AND-PPTX-OFFICE-SUITE/`):**
   * Editable Book Manuscript (`.docx`), Editable 10-Ch Workbook (`.docx`), 3-Tier B.R.I.E.F. Proposal (`.docx`), Master Service Agreement & SOW Contract (`.docx`), P.V.P. Change Order Form (`.docx`), Client Welcome Packet (`.docx`), Final Handover Certificate (`.docx`), plus **3 Widescreen `16:9` PowerPoint Pitch Decks (`32 slides` with presenter notes)**.
6. **Interactive Photo & Cover Design Customizer Studio + 3 JSON Automations (`07` & `08`):**
   * `design-customizer-studio.html` (`6 templates`, custom headshot/logo uploader, 1-click `.PNG`/`.SVG` export) + 3 Make.com / Zapier / n8n JSON workflow blueprints.

---

### Part 2: Included Day-1 Expansion Pack — Monthly Drop #01 (`05-LIVING-OS-MONTHLY-DROPS/`)

Included immediately inside your membership download is **`tier4-monthly-vault-drop-01.md` (*Drop #01: The High-Ticket Paid Diagnostic & Retainer Expansion Pack — 2,804 Words*)**, containing **8 advanced high-ticket assets**:

* **Prompt V1.1 — The `$750–$1,500` Paid Discovery & Architecture Sprint Builder:** Convert hesitant `$5,000+` prospects into a paid 5-day diagnostic engagement with a 100% credit window toward the full build.
* **Prompt V1.2 — The 3-Minute Cold/Warm Loom Audit Teardown Script Generator:** Book high-margin consultations without cold pitching by sending a structured 3-minute visual bottleneck teardown.
* **Prompt V1.3 — The Monthly Retainer Scope & Zero-Rollover Capacity Charter:** Structure `$1,500–$4,000/month` retainers with strict zero-rollover hour rules and async turnaround SLAs.
* **Prompt V1.4 — The Quarterly Executive ROI Review & Retainer Upsell Generator:** Present a 1-page 90-day ROI scorecard that naturally bridges `$1,250/mo` retainers into `$2,400/mo` growth tiers.
* **Prompt V1.5 — The Subcontractor / Junior Specialist 4-Gate QA Handoff Brief:** Delegate overflow execution hours while protecting your 65%+ gross margin and studio quality standard.
* **Scripts V1, V2 & V3 — Advanced Executive Negotiation Scripts:**
  * *Script V1:* Converting "Can We Start With a Small Hourly Test?" into a `$950` Paid Diagnostic Blueprint.
  * *Script V2:* Proactive Day-22 Retainer Capacity Alert & Overflow Sprint Pitch.
  * *Script V3:* The 90-Day Past-Client Reactivation & Phase-2 Audit Ping.

---

### Part 3: What You Receive Every Month as an Active VIP Member

1. **5 New Role-Calibrated AI Workflow Prompts:** Fresh prompt chains tuned for UI/UX & Webflow designers, full-stack & AI developers, B2B copywriters, marketing consultants, and executive virtual assistants.
2. **3 New Commercial Boundary & Enterprise Procurement Scripts:** Word-for-word responses for procurement reviews, scope expansions, and retainer renewals.
3. **Multi-Model LLM Calibration Updates:** Updated system prompt parameters tested against the latest releases of Claude, GPT, and Gemini.
4. **Complimentary Access to All New Studio Micro-Tools:** Every new HTML5 calculator, Excel tab, or Word/PPTX template released by Digital Knowledge Product Studio is added to your library automatically.

---
**System Architect & Author:** `OMAR SUNNY`  
*Choose **Yearly (`$49/year — Save 55%`)** or **Monthly (`$9/month`)** in the sidebar and click **Subscribe** for instant access to all 84 files.*
```

---

## 5. STEP 4 — CONTENT TAB SETUP FOR LISTING 3

Click the **`Content`** tab in the Gumroad Membership editor:
1. **Upload the Complete Tier 4 Membership Archive:**
   - Upload **`09-EXPORTS/HYBRID-BUNDLE/Tier4-Living-OS-Pro-Vault-Membership-Pack.zip`** (`84 files`, `10.36 MB`).
   - Also upload **`10-MARKETING/tier4-monthly-vault-drop-01.md`** as a standalone file beneath the ZIP so members can read Drop #01 directly inside the Gumroad web/mobile reader.
2. **Paste the VIP Welcome Note & Pro Activation Key Above the Download Box:**
   ```markdown
   ### Welcome to the VIP Living Freelancer OS & Pro Workflow Vault! (By OMAR SUNNY)

   **Your Pro Web Companion Activation Key:** `FREELANCER-OS-PRO-2026`

   1. Download **`Tier4-Living-OS-Pro-Vault-Membership-Pack.zip`** (`84 files`) to access the entire Flagship Operating System plus **`05-LIVING-OS-MONTHLY-DROPS/tier4-monthly-vault-drop-01.md`**.
   2. Double-click **`02-INTERACTIVE-WEB-APP/freelancer-os-app.html`** to run all 4 Pro Modules in your browser.
   3. Watch your inbox on the 1st of every month for your new **VIP Workflow & Negotiation Script Drop**!
   ```
"""
    (GUMROAD_SETUP_DIR / "03-LISTING-3-VIP-RECURRING-MEMBERSHIP-EXACT-FIELDS.md").write_text(file3_md, encoding="utf-8")

    # --------------------------------------------------------------------------
    # FILE 4: 04-GUMROAD-CHECKOUT-UPSELLS-COUPONS-AND-WORKFLOWS.md (>= 1,800 words)
    # --------------------------------------------------------------------------
    file4_md = """# GUMROAD CHECKOUT UPSELLS, DISCOUNT COUPONS & AUTOMATED 5-EMAIL WORKFLOWS PLAYBOOK
**Product Ecosystem:** *The AI Freelancer Operating System: A Practical System to Organize Clients, Automate Repetitive Work, Manage Projects, and Build a More Productive Freelance Business*  
**Author & System Architect:** `OMAR SUNNY` (`BY OMAR SUNNY` / `SYSTEM ARCHITECT: OMAR SUNNY`)  
**Target Gumroad Modules:** `Checkout -> Upsells`, `Checkout -> Discounts`, and `Workflows`

---

## 1. HOW GUMROAD'S NATIVE CHECKOUT UPSELLS MULTIPLY AVERAGE ORDER VALUE (AOV)

Once your three Gumroad listings are published (`Listing 1: Free Starter Kit`, `Listing 2: 3-Version Flagship OS`, and `Listing 3: VIP Membership Vault`), connecting them via **Gumroad Checkout Upsells (`https://app.gumroad.com/checkout/upsells`)** creates an automated conversion funnel right inside the Gumroad cart:

1. **Upsell #1 (Cross-Sell from Listing 1 `$0` -> Listing 2 `Version 3 Flagship OS` with `$10 OFF`):** Turns 4%–8% of free lead-magnet downloaders into immediate paid customers before they even leave the checkout screen.
2. **Upsell #2 (In-Cart Version Upgrade from Listing 2 `Version 1 [$19]` or `Version 2 [$39]` -> `Version 3 Flagship OS [$59]`):** Captures buyers who initially clicked a lower tier and shows them that for just a few dollars more they get the **Pro Offline Web App**, **8-Tab Charted Excel Command Center**, **7 Editable Word Contracts/Proposals**, and **3 PowerPoint Pitch Decks**.
3. **Upsell #3 (Post-Selection Add-On from Listing 2 -> Listing 3 `VIP Yearly Membership`):** Invites flagship buyers to add ongoing monthly workflow and negotiation script drops.

---

## 2. EXACT CONFIGURATION FOR ALL 3 GUMROAD CHECKOUT UPSELLS

Navigate to **`Checkout`** -> **`Upsells`** (`https://app.gumroad.com/checkout/upsells`) and click **`New upsell`** three times to create the following exact rules:

### Checkout Upsell #1 — Free Audit Kit Downloader -> Complete Flagship OS Bundle (`$10 OFF`)
- **Name (Internal Label):** `Free Audit Starter Kit -> Tier 3 Complete Flagship OS ($10 OFF)`
- **Type of Upsell:** Select **`Add another product to the cart`**
- **Apply to these products (Trigger):** Check **`Free 7-Day Freelancer Time, EHR & Revenue Leak Audit (AI Freelancer OS Starter Kit — By OMAR SUNNY)`** (`Listing 1`)
- **Product to offer:** Select **`The AI Freelancer Operating System (By OMAR SUNNY)`** -> **`⭐ Tier 3: Complete Flagship AI Freelancer OS Bundle — MOST POPULAR`**
- **Discount to apply to the offered product:** Check **`[x] Add a discount to the offered product`** -> Select **`Fixed amount`** -> Enter **`10`** (`$10 OFF` instant checkout bonus)
- **Upsell Text / Headline & Pitch (Copy-Paste Exactly — Zero Banned Words):**
  ```text
  Add the Complete 83-File Flagship AI Freelancer OS Bundle Right Now & Save $10 Instantly!
  ```
- **Upsell Description (Copy-Paste Exactly):**
  ```text
  Want to fix your shadow-labor leaks today instead of just diagnosing them? Upgrade your order right now to include all 10 Chapters, the 12-Page Visual Shortcut Atlas, 50 Tested AI Prompts, 12 Emergency Client Scripts, the Full Pro Web App (Key: FREELANCER-OS-PRO-2026), the 8-Tab Charted Excel Command Center, the 5-Database Notion OS, 7 Editable Word Contracts/Proposals (MSA, 3-Tier Proposal, Change Order) & 3 PowerPoint Pitch Decks. Click "Add to cart" below to claim your $10 instant checkout discount!
  ```

---

### Checkout Upsell #2 — Tier 1 (`$19`) or Tier 2 (`$39`) Buyer -> Tier 3 Complete Flagship OS Upgrade
- **Name (Internal Label):** `Version 1/2 Buyer -> Upgrade to Version 3 Complete Flagship OS`
- **Type of Upsell:** Select **`Replace the version selected with another version of the same product`**
- **Product:** Select **`The AI Freelancer Operating System: Complete Client, Pricing, Project & Automation System (By OMAR SUNNY)`** (`Listing 2`)
- **Versions to trigger on:** Check **`Tier 1: Core Book, EPUB 3.0 & Print-Ready Edition`** AND **`Tier 2: Interactive Workbook, 12-Page Visual Shortcut Atlas & Tablet Planner Edition`**
- **Version to offer instead:** Select **`⭐ Tier 3: Complete Flagship AI Freelancer OS Bundle — MOST POPULAR`**
- **Upsell Text / Headline (Copy-Paste Exactly):**
  ```text
  Upgrade to the Complete 83-File Flagship Agency & Freelancer Suite (Pays for Itself in 1 Client Change Order!)
  ```
- **Upsell Description (Copy-Paste Exactly):**
  ```text
  You selected the book/workbook edition—would you like to upgrade to Tier 3 (Complete Flagship OS) so you also receive the Full Pro Offline Web App (B.C.R. 3-Tier Proposal Pricer + 62-Item Prompt Builder), the 8-Tab Charted Excel Command Center, the 5-Database Notion OS Kit, all 7 Editable Microsoft Word Contracts & Proposals (Master Service Agreement, 3-Tier BRIEF Proposal, P.V.P. Change Order Form), and all 3 Widescreen PowerPoint Pitch Decks? Converting just ONE informal client request into a paid Change Order recovers 10x this upgrade cost!
  ```

---

### Checkout Upsell #3 — Flagship Buyer -> VIP Living Vault Pass Add-On
- **Name (Internal Label):** `Flagship OS Buyer -> Add VIP Monthly/Yearly Workflow Vault`
- **Type of Upsell:** Select **`Add another product to the cart`**
- **Apply to these products (Trigger):** Check **`The AI Freelancer Operating System (By OMAR SUNNY)`** (`Listing 2`)
- **Product to offer:** Select **`VIP Living Freelancer OS & Pro Workflow Vault Membership (By OMAR SUNNY)`** (`Listing 3`)
- **Discount to apply:** Optional `20% OFF` first billing period
- **Upsell Text / Headline (Copy-Paste Exactly):**
  ```text
  Add the VIP Living Workflow Vault Pass (Includes Drop #01: Paid Diagnostic & Retainer Expansion Pack)
  ```
- **Upsell Description (Copy-Paste Exactly):**
  ```text
  Want continuous monthly AI workflow packs, niche prompt chains, and advanced negotiation scripts delivered to your Gumroad Library every month? Add the VIP Living Vault Pass to receive Drop #01 (The $750-$1,500 Paid Diagnostic & Retainer Expansion Pack — 5 bonus prompts + 3 executive scripts) immediately alongside your bundle!
  ```

---

## 3. EXACT DISCOUNT COUPON CODES SETUP (`Checkout -> Discounts`)

Navigate to **`Checkout`** -> **`Discounts`** (`https://app.gumroad.com/checkout/discounts`) and create these four strategic discount codes for your email funnel, social launches, and bundle upgrades:

| Coupon Code | Discount Type & Value | Target Products | Max Uses / Expiry | Strategic Use Case |
| :--- | :---: | :--- | :---: | :--- |
| **`LAUNCH20`** | **`20% OFF`** (Percentage) | Listing 2 (All 3 Versions) & Listing 3 | First `100` buyers | Public launch week announcement on LinkedIn, X, YouTube & Product Hunt. |
| **`SUBSCRIBER15`** | **`15% OFF`** (Percentage) | Listing 2 (All 3 Versions) | Unlimited (Evergreen) | Embedded inside `START-HERE-TIER0.md` and Email #4/#5 of the automated lead-magnet sequence. |
| **`UPGRADE25`** | **`$25 OFF`** (Fixed USD) | Listing 2 -> `Version 3 (Tier 3 Flagship)` | Unlimited | Sent to existing Tier 2 (`$24/$39`) workbook buyers who want to upgrade to the full `83-file` Flagship Bundle without paying twice. |
| **`VIPANNUAL10`** | **`$10 OFF`** (Fixed USD) | Listing 3 (`VIP Membership Yearly`) | Unlimited | Seasonal promotion bringing the `$49/year` VIP Pass down to `$39/year`. |

---

## 4. AUTOMATED 5-EMAIL GUMROAD WORKFLOWS SETUP (`Workflows` Tab)

Gumroad includes a built-in email automation engine under **`Workflows`** (`https://app.gumroad.com/workflows`) with zero monthly Mailchimp or ConvertKit fees. Set up this exact **5-Step Post-Download Conversion Workflow** triggered whenever someone downloads **Listing 1 (Free Starter Kit)**:

### Step A — Create the Workflow Trigger & Purchase Suppression Filter
1. Click **`New workflow`** in the Gumroad **Workflows** tab.
2. **Workflow Name:** `Free 7-Day Leak Audit Kit -> 10-Day Flagship OS Conversion Sequence (OMAR SUNNY)`
3. **Trigger:** Select **`Audience` / `Customer buys`** -> Select **`Free 7-Day Freelancer Time, EHR & Revenue Leak Audit (Listing 1)`**.
4. **Suppression Filter (Crucial so buyers stop receiving pitch emails once they upgrade):**
   - Click **`Add filter`** -> **`Has not bought`** -> Select **`The AI Freelancer Operating System (Listing 2)`** AND **`VIP Living Freelancer OS & Pro Workflow Vault Membership (Listing 3)`**.

### Step B — Add the 5 Automated Emails (`10-MARKETING/email-funnel-and-upsell-sequence.md`)
Open [`10-MARKETING/email-funnel-and-upsell-sequence.md`](file:///e:/Ebook-Makaer/AI%20FreeLancer%20OS/DIGITAL-PUBLISHING-STUDIO/10-MARKETING/email-funnel-and-upsell-sequence.md) and paste the 5 complete emails into your Gumroad Workflow using these exact delay timers:

| Workflow Email # | Send Delay Timer | Email Subject Line (`Copy-Paste`) | Primary CTA Link & Goal |
| :--- | :---: | :--- | :--- |
| **Email #01** | **`0 Hours` (Immediate)** | `Your Freelancer Leak Audit Kit (+ How to calculate your real hourly rate in 15 mins)` | Delivers `Tier0-Free-Leak-Audit-Starter-Kit.zip` + instructs user to run Module 1 inside `freelancer-os-app.html`. |
| **Email #02** | **`2 Days` after purchase** | `Why a $75/hr freelancer actually takes home $26.80/hr (Marcus's 30-day fix)` | Walks through Marcus Vance's 4-Bucket audit and introduces the **3-Tier Productized Offer Matrix**. |
| **Email #03** | **`4 Days` after purchase** | `Copy-paste this exact script next time a client asks for a "quick favor"` | Gives away **Script 7 (The P.V.P. Change Order Script)** + introduces **Tier 2 (`$24/$39` Workbook & Visual Atlas Edition)**. |
| **Email #04** | **`7 Days` after purchase** | `Inside the 10-Minute B.R.I.E.F. Proposal & B.C.R. Pricing Engine` | Demonstrates **Module 2 of `freelancer-os-app.html`**, the **8-Tab Charted Excel Matrix**, and the **7 Editable Word Contracts** (`Listing 2 -> Version 3`). |
| **Email #05** | **`10 Days` after purchase** | `Ready to install the full 5-Gate AI Freelancer Operating System?` | Complete 5-Tier value recap + **`SUBSCRIBER15` (`15% OFF`)** direct checkout link to `gumroad.com/l/ai-freelancer-os`. |

Click **`Publish workflow`** in the top-right corner. Every single free download of **Listing 1** will now enter this automated 10-day nurture and conversion engine!

---

## 5. GUMROAD AFFILIATE PROGRAM (`30%–50%` PARTNER COMMISSION) & CREATOR COLLABORATION SETUP

Because digital knowledge products carry near-100% gross delivery margin after payment processing fees, activating Gumroad's built-in **Affiliates (`Collaborators -> Affiliates`)** engine turns happy customers, freelance newsletter writers, YouTube educators, and Notion template creators into a commission-only sales team for **`OMAR SUNNY`**:

### Step A — Enable Self-Serve Affiliate Applications (`https://app.gumroad.com/affiliates`)
1. In the left navigation sidebar, click **`Collaborators`** -> **`Affiliates`** -> **`Affiliate Signup Form`**.
2. Toggle **ON `[x] Enable affiliate signup form`**.
3. Set your default affiliate commission structure across the three listings:
   - **Listing 1 (`Free 7-Day Leak Audit Starter Kit — $0+`):** Check **`[x] Enable`** at **`50%` commission** *(when an affiliate refers a free downloader who later buys Listing 2 or Listing 3 within the 30-day browser cookie window, Gumroad automatically credits the affiliate)*.
   - **Listing 2 (`The AI Freelancer Operating System 3-Version Flagship — $19 / $39 / $59`):** Check **`[x] Enable`** at **`35%` default commission** *(earns partners `$20.65` per `$59` Tier 3 Flagship sale)*.
   - **Listing 3 (`VIP Living Freelancer OS & Pro Workflow Vault Membership — $9/mo or $49/yr`):** Check **`[x] Enable`** at **`30%` recurring commission** *(earns partners `$14.70/year` on every annual VIP pass)*.

### Step B — Automated Post-Purchase Affiliate Recruitment Workflow
Create a second Gumroad Workflow (`Workflows -> New workflow`) titled **`Paid Customer -> Day-14 Affiliate Partner Invitation (OMAR SUNNY)`**:
- **Trigger:** `Customer buys` -> `The AI Freelancer Operating System (Listing 2)` OR `VIP Living Freelancer OS & Pro Workflow Vault Membership (Listing 3)`.
- **Delay Timer:** `14 Days after purchase` *(right after the buyer has used the B.C.R. Proposal Engine and P.V.P. Change Order scripts with a real client)*.
- **Email Subject Line:** `Earn 35% ($20.65 per sale) sharing The AI Freelancer Operating System`
- **Email Copy Summary:** Invite verified buyers to apply via your Gumroad Affiliate Signup URL in 1 click and provide them with the `600×600` square thumbnails and `1280×720` covers from `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/`.

---

## 6. PURCHASING POWER PARITY (PPP), GLOBAL TAX HANDLING & 60-SECOND SUPPORT SOP

To maximize global conversion rate while maintaining zero administrative overhead for your studio:

1. **Purchasing Power Parity (PPP) Guardrails (`Settings -> Advanced / Product Pricing`):**
   - Enable **Purchasing Power Parity** on **Listing 2** with a maximum regional discount cap of **`40%`**. Buyers in Tier-1 Western markets (`US`, `UK`, `Canada`, `Australia`, `Western Europe`) always see the full `$19 / $39 / $59` pricing, while independent freelancers in developing economies receive an automatic location-verified discount at checkout.
2. **Automated Global VAT & Digital Sales Tax Compliance:**
   - Gumroad operates as your **Merchant of Record (MoR)** globally. Gumroad automatically calculates, collects, and remits EU/UK VAT, Canadian GST/HST, Australian GST, and US state digital sales taxes on every single transaction—requiring zero manual tax filings across foreign jurisdictions.
3. **14-Day Action-Based Refund & License Key Replacement Policy:**
   - If a Tier 1 or Tier 2 customer emails asking to upgrade to **Version 3 (`Tier 3 Complete Flagship OS`)**, send them your **`UPGRADE25` (`$25 OFF`)** coupon link (`https://gumroad.com/l/ai-freelancer-os/UPGRADE25`) so they only pay the net tier difference.
   - Remind all Tier 3 and VIP Vault buyers that their offline/online Web Companion App (`freelancer-os-app.html`) activation key is **`FREELANCER-OS-PRO-2026`**, which activates Modules 2, 3, and 4 permanently in their local browser storage.
"""
    (GUMROAD_SETUP_DIR / "04-GUMROAD-CHECKOUT-UPSELLS-COUPONS-AND-WORKFLOWS.md").write_text(file4_md, encoding="utf-8")

    # --------------------------------------------------------------------------
    # FILE 5: 05-AI-COVER-AND-THUMBNAIL-IMAGE-GENERATION-PROMPTS.md (>= 1,800 words)
    # --------------------------------------------------------------------------
    file5_md = """# 12 HIGH-PRECISION AI COVER, 3D BOX & THUMBNAIL IMAGE GENERATION PROMPTS
**Product Ecosystem:** *The AI Freelancer Operating System: A Practical System to Organize Clients, Automate Repetitive Work, Manage Projects, and Build a More Productive Freelance Business*  
**Author & System Architect:** `OMAR SUNNY` (`BY OMAR SUNNY` / `SYSTEM ARCHITECT: OMAR SUNNY`)  
**Compatible AI Generators:** Ideogram 2.0 (Best for Exact Typography), DALL-E 3 / ChatGPT Plus, Midjourney v6.1, Flux.1 Pro, and Leonardo AI  
**Companion Local Studio:** [`08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html`](file:///e:/Ebook-Makaer/AI%20FreeLancer%20OS/DIGITAL-PUBLISHING-STUDIO/08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html)

---

## 1. HOW TO USE THESE 12 AI PROMPTS WITH YOUR DESIGN CUSTOMIZER STUDIO

Your repository already includes **9 deterministic vector/raster covers and square thumbnails** in `08-COVER-DESIGN/` (`6` widescreen/print covers + `3` square `600×600` thumbnails). However, if you want to test **photorealistic 3D hardware mockups, isometric glassmorphic software stacks, or custom executive desk scenes** in **Ideogram 2.0, Midjourney v6.1, or DALL-E 3**, you can:

1. **Generate the Photorealistic Visual Directly** using the 12 prompts below (Ideogram 2.0 and DALL-E 3 render the exact title and `"BY OMAR SUNNY"` typography automatically).
2. **Or Combine with `design-customizer-studio.html`:** Generate a clean 3D background scene in Midjourney, double-click [`design-customizer-studio.html`](file:///e:/Ebook-Makaer/AI%20FreeLancer%20OS/DIGITAL-PUBLISHING-STUDIO/08-COVER-DESIGN/Editable-Design-Kit/design-customizer-studio.html), upload your AI image via the **`FileReader` Background Photo Uploader**, and export a razor-sharp `.PNG` with vector badges in 10 seconds!

---

## 2. PROMPTS 1–3: SQUARE `1:1` (`600 × 600` / `1024 × 1024`) GUMROAD DISCOVER THUMBNAILS

### Prompt 01 — Listing 1 Square Thumbnail (`$0 Free 7-Day EHR & Revenue Leak Audit Kit`)
* **Target Aspect Ratio:** `1:1` (`--ar 1:1` in Midjourney / `1024x1024` in Ideogram 2.0 & DALL-E 3, then resize or upload directly to Gumroad Thumbnail).
* **Copy-Paste Prompt:**
  ```text
  Ultra-crisp 1:1 square digital product thumbnail for a B2B SaaS and executive publishing brand, dark slate navy background (#0F172A) with subtle architectural blueprint grid lines. Top glowing emerald-teal pill badge reading "$0 FREE AUDIT KIT". Bold geometric sans-serif white and sky-blue headline reading "7-DAY EHR & REVENUE LEAK AUDIT". In the center, a sleek 3D isometric floating glassmorphic dashboard card displaying an Effective Hourly Rate gauge ($26.80/hr to $85.00/hr), a 4-bucket time allocation pie chart, and a clean PDF workbook binder. At the bottom, a sleek dark metallic footer bar with crisp white micro-typography reading "BY OMAR SUNNY • SYSTEM ARCHITECT: OMAR SUNNY" with wide letter-spacing. Studio lighting, Stripe and Linear design aesthetic, high contrast, 8k resolution --ar 1:1 --v 6.1 --style raw
  ```

### Prompt 02 — Listing 2 Square Thumbnail (`$19 / $39 / $59 Complete Flagship AI Freelancer OS`)
* **Target Aspect Ratio:** `1:1` (`--ar 1:1` / `1024x1024`)
* **Copy-Paste Prompt:**
  ```text
  High-converting 1:1 square Gumroad Discover product thumbnail on a deep obsidian and slate navy background (#0B1120). Top warm amber-gold badge reading "COMPLETE AI FREELANCER OS". Bold white and electric sky-blue headline reading "THE AI FREELANCER OPERATING SYSTEM" with a monospace subtitle bar reading "50 AI PROMPTS • WEB APP • 8-TAB EXCEL • NOTION OS". Center composition features an isometric 3D multi-device product ecosystem mockup: a MacBook Pro displaying a dark-mode SaaS pricing calculator, an iPad Pro showing a landscape digital planner, a floating 8-tab Excel financial chart card, a hardcover executive manual book, and Word/PowerPoint document icons glowing with cyan and teal accents. Bottom bar features crisp wide-tracked typography reading "BY OMAR SUNNY • SYSTEM ARCHITECT: OMAR SUNNY". Photorealistic product render, sharp vector UI details --ar 1:1 --v 6.1 --style raw
  ```

### Prompt 03 — Listing 3 Square Thumbnail (`$9/mo or $49/yr VIP Living Workflow Vault Membership`)
* **Target Aspect Ratio:** `1:1` (`--ar 1:1` / `1024x1024`)
* **Copy-Paste Prompt:**
  ```text
  Premium 1:1 square membership pass thumbnail on a dark sapphire and obsidian gradient background (#090D16) with a glowing gold border frame. Top gold and teal badge reading "VIP MONTHLY VAULT PASS • $9/MO OR $49/YR". Bold white and gold headline reading "LIVING FREELANCER PRO VAULT PASS". Center visual shows a futuristic 3D brushed-titanium and sapphire vault card opening to reveal glowing holographic workflow cards labeled "PAID DIAGNOSTIC SPRINT", "RETAINER BRIDGE SCRIPTS", and "50+ AI PROMPT VAULT". Bottom attribution strip in crisp white monospace font reading "BY OMAR SUNNY • SYSTEM ARCHITECT: OMAR SUNNY". Executive fintech aesthetic, volumetric lighting, ultra-sharp --ar 1:1 --v 6.1 --style raw
  ```

---

## 3. PROMPTS 4–7: WIDESCREEN `16:9` (`1280 × 720`) GUMROAD HEADER COVERS

### Prompt 04 — Listing 1 Header Banner (`16:9` Free 7-Day Leak Audit Starter Kit)
* **Target Aspect Ratio:** `16:9` (`1280 × 720 px`)
* **Copy-Paste Prompt:**
  ```text
  Widescreen 16:9 commercial product banner (1280x720) on a deep slate navy architectural background (#0F172A). Left side features a teal pill badge "$0 FREE DOWNLOAD • 15-MINUTE DIAGNOSTIC", bold white headline "The 7-Day Freelancer Time & Revenue Leak Audit", and subtitle "Calculate Your True Effective Hourly Rate (EHR) & Stop Shadow Labor". Right side showcases a 3D angled product bundle: an open Chapter 1 Operating Manual PDF, a fillable worksheet clipboard, a laptop running an interactive EHR Leak Calculator web app, and two wall poster infographics. Bottom footer bar reads "THE AI FREELANCER OPERATING SYSTEM • BY OMAR SUNNY". Clean B2B SaaS editorial style, high contrast --ar 16:9 --v 6.1 --style raw
  ```

### Prompt 05 — Listing 2 Hero Header Banner (`16:9` Complete 83-File Flagship OS Bundle)
* **Target Aspect Ratio:** `16:9` (`1280 × 720 px`)
* **Copy-Paste Prompt:**
  ```text
  Flagship 16:9 hero product showcase banner (1280x720) on an executive dark slate desk environment with glowing sky-blue (#0284C7), teal (#0D9488), and amber-gold (#F59E0B) rim lighting. Left side displays a gold badge "TIER 3 FLAGSHIP BUNDLE • 83 FILES INCLUDED", bold headline "The Complete AI Freelancer Operating System", and 4 feature pills ("168p Manual + 12p Visual Atlas", "Pro Offline Web App", "8-Tab Charted Excel + 5-DB Notion OS", "7 Word Contracts + 3 PPTX Pitch Decks"). Right side displays a studio 3D hardware and document flat-lay: MacBook Pro running the Freelancer OS Web App, second monitor showing an 8-tab Excel dashboard with bar and pie charts, iPad Pro with Apple Pencil on a digital planner, hardcover book, and printed Word MSA contracts. Bottom right credit in sleek micro-typography: "SYSTEM ARCHITECT: OMAR SUNNY" --ar 16:9 --v 6.1 --style raw
  ```

### Prompt 06 — Listing 2 Carousel Slide 2 (`16:9` Interactive Workbook, 12-Page Visual Atlas & Planner)
* **Target Aspect Ratio:** `16:9` (`1280 × 720 px`)
* **Copy-Paste Prompt:**
  ```text
  Widescreen 16:9 product showcase banner (1280x720) highlighting "The 60-Second Visual Shortcut Atlas & Interactive Workbook Suite". Dark navy background with cyan blueprint grid. Center showcase displays an iPad Pro running GoodNotes with a hyperlinked dark-slate digital planner, fanned-out full-color infographic cheat sheet pages ("5-Gate Master Map", "B.C.R. Pricing Formula", "48-Hour Asset Gate"), and US Letter & A4 fillable workbooks. Bottom attribution bar reads "ARCHITECTED BY OMAR SUNNY • DIGITAL KNOWLEDGE PRODUCT STUDIO" --ar 16:9 --v 6.1 --style raw
  ```

### Prompt 07 — Listing 3 Header Banner (`16:9` VIP Living OS & Pro Workflow Vault Membership)
* **Target Aspect Ratio:** `16:9` (`1280 × 720 px`)
* **Copy-Paste Prompt:**
  ```text
  Widescreen 16:9 executive membership banner (1280x720) on a deep obsidian and sapphire background with gold accents. Top badge reads "TIER 4 VIP MEMBERSHIP • $9/MO OR $49/YR (SAVE 55%)". Headline reads "Living Freelancer OS & Pro Workflow Vault Pass". Visual composition shows a glowing digital vault streaming monthly expansion modules: "Drop #01: High-Ticket Paid Diagnostic Sprint", "3-Min Loom Teardown Scripts", "Zero-Rollover Retainer Charter", and "Multi-Model Claude/GPT/Gemini Prompt Packs". Footer credit reads "BY OMAR SUNNY • SYSTEM ARCHITECT: OMAR SUNNY" --ar 16:9 --v 6.1 --style raw
  ```

---

## 4. PROMPTS 8–12: AMAZON KDP, PAYHIP, YOUTUBE, LINKEDIN & NOTION HEADERS

### Prompt 08 — Amazon KDP & Draft2Digital 2D/3D Vertical Book Cover (`1:1.6` / `1600 × 2560 px`)
* **Copy-Paste Prompt:**
  ```text
  Bestselling non-fiction business and technology book cover (1600x2560 vertical 1:1.6 ratio), Penguin Business and Stripe Press editorial aesthetic. Deep slate navy background (#0F172A) with a precision geometric 5-gate flowchart diagram in glowing cyan (#38BDF8), emerald teal (#2DD4BF), and gold (#FBBF24). Top imprint header: "PRACTITIONER SYSTEMS PRESS • EDITION v1.0". Bold stacked title: "THE AI FREELANCER OPERATING SYSTEM" and subtitle "A Practical System to Organize Clients, Automate Repetitive Work, Manage Projects, and Build a More Productive Freelance Business". Bottom author credit in bold white tracked capitals: "BY OMAR SUNNY" --ar 10:16 --v 6.1 --style raw
  ```

### Prompt 09 — Payhip & LemonSqueezy `4:3` Storefront Showcase Card (`1200 × 900 px`)
* **Copy-Paste Prompt:**
  ```text
  Clean 4:3 e-commerce product showcase card (1200x900) displaying an isometric 3D software box and multi-device bundle for "The AI Freelancer Operating System". Includes hardcover manual, 12-page visual atlas, laptop with SaaS web app, Excel financial charts, Notion CRM cards, and Word/PowerPoint icons. Crisp top badge "$49 COMPLETE OS BUNDLE" and bottom footer "BY OMAR SUNNY" --ar 4:3 --v 6.1 --style raw
  ```

### Prompt 10 — YouTube & 3-Minute Loom Walkthrough High-CTR Thumbnail (`16:9` / `1280 × 720 px`)
* **Copy-Paste Prompt:**
  ```text
  High-CTR YouTube and Loom video thumbnail (1280x720) on a dark slate studio background. Left side shows two high-contrast metric cards: a red card "$26.80/HR (BEFORE: 48.5 HRS/WK)" with a glowing cyan arrow pointing to an emerald green card "$58.40/HR (AFTER: 36.5 HRS/WK)". Bold yellow and white headline text: "THE 5-GATE AI FREELANCER OS". Bottom corner badge reads "BY OMAR SUNNY" --ar 16:9 --v 6.1 --style raw
  ```

### Prompt 11 — LinkedIn & X Personal Brand Authority Header Banner (`4:1` / `1584 × 396 px`)
* **Copy-Paste Prompt:**
  ```text
  Ultra-wide LinkedIn profile banner (1584x396, 4:1 aspect ratio) on a dark slate navy background (#0F172A). Left 25% kept clean for profile avatar overlay. Right 75% features a sleek horizontal 5-Gate diagram ("01 Attract -> 02 B.C.R. Price -> 03 48h Onboard -> 04 20/60/20 Execute -> 05 Retainer Scale"), bold white title "THE AI FREELANCER OPERATING SYSTEM", and right-aligned badge "SYSTEM ARCHITECT: OMAR SUNNY • 50 AI PROMPTS + WEB APP + NOTION OS" --ar 4:1 --v 6.1 --style raw
  ```

### Prompt 12 — Notion Workspace & Client Command Portal Header Cover (`1500 × 600 px`)
* **Copy-Paste Prompt:**
  ```text
  Minimalist dark-mode Notion workspace header cover (1500x600) with a deep slate navy and obsidian gradient (#0B1120 to #1E293B), subtle cyan architectural grid lines, a centered glowing geometric 5-Gate circuit emblem, and clean monospace label "THE AI FREELANCER OPERATING SYSTEM // COMMAND HUB • BY OMAR SUNNY" --ar 5:2 --v 6.1 --style raw
  ```
"""
    (GUMROAD_SETUP_DIR / "05-AI-COVER-AND-THUMBNAIL-IMAGE-GENERATION-PROMPTS.md").write_text(file5_md, encoding="utf-8")

    # --------------------------------------------------------------------------
    # FILE 00 (LOCKED MASTER BLUEPRINT): UNIFIED 2-LINK ARCHITECTURE
    # Link 1: 4 Versions ($0 / $19 / $39 / $59 in 1 Single Product Link)
    # Link 2: VIP Recurring Membership ($9/mo or $49/yr) + Cross-Linked
    # --------------------------------------------------------------------------
    file0_locked_md = """# LOCKED MASTER SETUP — UNIFIED 2-LINK GUMROAD ARCHITECTURE (`$0 / $19 / $39 / $59` IN 1 LINK + `VIP MEMBERSHIP` IN LINK 2)
**Product Ecosystem:** *The AI Freelancer Operating System: A Practical System to Organize Clients, Automate Repetitive Work, Manage Projects, and Build a More Productive Freelance Business*  
**Author & System Architect:** `OMAR SUNNY` (`BY OMAR SUNNY` / `SYSTEM ARCHITECT: OMAR SUNNY`)  
**Architecture Status:** `LOCKED — CONSOLIDATED 4-VERSION FLAGSHIP + RECURRING VIP MEMBERSHIP`

---

## 1. RESEARCH VERDICT: WHY THIS 2-LINK CONSOLIDATED ARCHITECTURE IS LOCKED

Putting **all 4 One-Time Tiers (`$0`, `$19`, `$39`, `$59`) inside ONE main Gumroad Product Link (`gumroad.com/l/ai-freelancer-os`)** using Gumroad's native **`Versions`** selector—while keeping the **Recurring VIP Membership (`$9/mo` or `$49/yr`)** as your second linked product (`gumroad.com/l/ai-freelancer-vip-vault`)—delivers **5 major algorithmic and conversion advantages**:

1. **100% Unified Social Proof & Review Accumulation (`Cold-Start Rocket`):**
   - Gumroad Discover indexes a **product URL**, not separate versions.
   - When `$0`, `$19`, `$39`, and `$59` live inside the **same product link**, every single `$0` download counts toward your total sales velocity on that URL, and every `5.0 ★` review left by `$0` starter-kit users appears **directly on your `$59` Flagship page**!
2. **Gumroad Understands It Is One Unified Product Ecosystem:**
   - Because all 4 versions (`Tier 0 Free`, `Tier 1 Book`, `Tier 2 Workbook`, `Tier 3 Complete OS`) are inside one product entity, Gumroad's recommendation engine treats them as one authoritative product rather than competing duplicate listings.
   - Connecting **Product Link #1 (`4-Version Flagship`)** and **Product Link #2 (`VIP Membership`)** via **Gumroad Checkout Upsells**, **Profile Pinning**, and **Bidirectional Description Links** tells Gumroad's recommendation graph that buyers of Product #1 should immediately be suggested Product #2.
3. **Eliminates the "Freebie Seeker Trap" via Strategic Top-Down Version Ordering:**
   - In Gumroad's **Versions** editor, you can drag and drop the display order of versions!
   - By placing **`⭐ Tier 3: Complete Flagship AI Freelancer OS Bundle ($59)` at the TOP (Position #1 — Default Selected)**, followed by **`Tier 2 ($39)`**, **`Tier 1 ($19)`**, and placing **`Tier 0: Free 7-Day Leak Audit Starter Kit ($0)` at the BOTTOM (Position #4)**, serious buyers immediately see the `$59` Flagship Bundle selected by default, while hesitant visitors who aren't ready to pay yet can choose the `$0` starter option at the bottom instead of bouncing!
4. **Native In-Cart Version Replacement Upsell (`$0 -> $59` with `$10 OFF`):**
   - Whenever a user selects **`Tier 0 ($0)`**, **`Tier 1 ($19)`**, or **`Tier 2 ($39)`** and clicks **`I want this!`**, Gumroad's native **Checkout Upsell (`Replace the version selected with another version of the same product`)** pops up inside the cart and offers to swap their selection to **`⭐ Tier 3: Complete Flagship OS Bundle ($59)`** in 1 click!
5. **Version-Filtered Automated 5-Email Gumroad Workflow:**
   - Gumroad Workflows allows you to trigger your 5-Email sequence **exclusively** for people who selected `Tier 0 ($0 Free Starter Kit)` (`Customer bought: Tier 0` AND `Has NOT bought: Tier 1, Tier 2, Tier 3, or VIP Membership`), bringing them right back to the exact same link (`gumroad.com/l/ai-freelancer-os`) to upgrade!

---

## 2. EXACT SETUP FOR PRODUCT LINK #1 (UNIFIED 4-VERSION FLAGSHIP PRODUCT: `$0 / $19 / $39 / $59`)

### Step 1 — Create Product #1 (`https://app.gumroad.com/products`)
- **Name:**
  ```text
  The AI Freelancer Operating System: Complete Client, Pricing, Project & Automation System (By OMAR SUNNY)
  ```
- **Type:** Select **`Digital product`**
- **Base Price (Initial Screen):** Enter **`0`** (USD `$`)
  *(Why Base Price = `$0`? Because Gumroad calculates each Version's price as `Base Price + Additional Amount`. Setting Base Price to `$0` allows your 4 Versions to be priced at `+$0 = $0`, `+$19 = $19`, `+$39 = $39`, and `+$59 = $59`!)*

### Step 2 — Upload Visuals (Thumbnail & 4-Slide Cover Carousel)
- **Square Thumbnail (`600 × 600 px` `1:1`):**
  Upload `10-MARKETING/Gumroad-Hybrid-Master-Setup/Thumbnails-and-Covers/12-gumroad-square-thumb-listing2-flagship-os-600x600.png`
- **Cover Carousel (`1280 × 720 px` `16:9` — Upload all 4 in this exact order so all 4 tiers are visually represented on the same page):**
  1. `05-gumroad-tier3-flagship-bundle-cover.png` (*Slide 1: Tier 3 Complete Flagship OS*)
  2. `04-gumroad-tier2-workbook-edition-cover.png` (*Slide 2: Tier 2 Workbook, Visual Atlas & Planner*)
  3. `00-ECOSYSTEM-MASTER-MAP-POSTER.png` (*Slide 3: Complete 5-Gate Ecosystem Architecture Map*)
  4. `03-gumroad-tier0-free-audit-cover.png` (*Slide 4: Tier 0 Free 7-Day Leak Audit Starter Kit*)

### Step 3 — Configure the 4 Versions in Exact Top-Down Conversion Order (`Product Tab -> Versions`)
Scroll down to **`Versions`**, click **`Add version`** four times, and arrange them in this **exact Top-to-Bottom order** (so `Tier 3 [$59]` is at the very top as the default selection, and `Tier 0 [$0]` is at the bottom):

| Display Order (Top to Bottom) | Exact Version Name (`Copy-Paste`) | Additional Amount (`+$`) | Final Checkout Price | Exact Version Description (`Copy-Paste`) | Exact ZIP File to Attach in `Content` Tab |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **#1 (TOP — Default Selected)** | `⭐ Tier 3: Complete Flagship AI Freelancer OS Bundle — MOST POPULAR ($59)` | **`59`** *(or `49`)* | **`$59`** *(or `$49`)* | `Complete 83-File Agency & Freelancer Ecosystem: All Books (PDF/EPUB/Print) + 12-Page Visual Shortcut Atlas + Fillable Workbooks & iPad Planner + Full Pro Offline Web App (Key: FREELANCER-OS-PRO-2026) + 8-Tab Charted Excel Command Center (299 Formulas + 4 Charts) + 5-DB Notion OS Kit + All 7 Editable Word Contracts & Proposals + 3 PowerPoint Pitch Decks (32 Slides) + Photo/Cover Design Studio + 3 JSON Automation Blueprints.` | `Tier3-Complete-AI-Freelancer-OS-Flagship-Bundle.zip` (`83 files`) |
| **#2 (Second Option)** | `Tier 2: Interactive Workbook, 12-Page Visual Shortcut Atlas & Tablet Planner Edition ($39)` | **`39`** *(or `24`)* | **`$39`** *(or `$24`)* | `Everything in Tier 1 PLUS: 12-Page Full-Color 60-Second Visual Shortcut Atlas PDF, US Letter & ISO A4 Fillable Action Workbooks, Editable Microsoft Word 10-Chapter Workbook (.docx), 49-Page Landscape iPad/Tablet Digital Planner PDF, 62-Item Prompt Vault CSV & 31 Vector Diagrams/Cheat-Sheet SVGs (40 Files Total).` | `Tier2-Interactive-Workbook-and-Planner-Edition.zip` (`40 files`) |
| **#3 (Third Option)** | `Tier 1: Core Book, EPUB 3.0 & Print-Ready Edition ($19)` | **`19`** | **`$19`** | `Complete 168-Page Flagship Digital Book (PDF) + Reflowable EPUB 3.0 eBook + 146-Page 6"x9" Print Paperback Interior PDF + High-Res Covers. Includes all 10 Chapters (75,158 words), 50 Tested AI Workflow Prompts & 12 Emergency Client Boundary Scripts.` | `Tier1-KDP-and-D2D-Publisher-Upload-Pack.zip` (`9 files`) |
| **#4 (BOTTOM — Free Starter Option)** | `Tier 0: Free 7-Day Time, EHR & Revenue Leak Audit Starter Kit ($0)` | **`0`** | **`$0`** | `Free 8-File Diagnostic Starter Kit: Complete Sample Chapter 1 PDF (7,235 words) + Fillable Worksheet 1.1 PDF + Offline HTML5 Web App (Module 1 EHR Leak Calculator Open) + Spreadsheet Audit CSV + 1600x1100 Master Ecosystem Poster + Ch 1 Visual Cheat Sheet.` | `Tier0-Free-Leak-Audit-Starter-Kit.zip` (`8 files`) |

> **Why Top-to-Bottom Ordering (`$59 -> $39 -> $19 -> $0`) Is Critical:**  
> On Gumroad, **the #1 top version in your Versions list is automatically pre-selected** when a visitor lands on your page! By putting **`⭐ Tier 3 ($59)`** first, your main price badge and default checkout selection stay anchored on your flagship `$59` bundle, while anyone who wants to try the free sample can click **`Tier 0 ($0)`** at the bottom of the list.

---

## 3. EXACT SETUP FOR PRODUCT LINK #2 (RECURRING VIP MEMBERSHIP: `$9/MO` OR `$49/YR`)

Follow the exact fields in [`03-LISTING-3-VIP-RECURRING-MEMBERSHIP-EXACT-FIELDS.md`](file:///e:/Ebook-Makaer/AI%20FreeLancer%20OS/DIGITAL-PUBLISHING-STUDIO/10-MARKETING/Gumroad-Hybrid-Master-Setup/03-LISTING-3-VIP-RECURRING-MEMBERSHIP-EXACT-FIELDS.md):
- **URL:** `https://[your-username].gumroad.com/l/ai-freelancer-vip-vault`
- **Square Thumbnail (`600 × 600 px`):** `13-gumroad-square-thumb-listing3-vip-membership-600x600.png`
- **Cover (`1280 × 720 px`):** `06-gumroad-tier4-vip-vault-cover.png`
- **Pricing:** **`$9 / month`** and **`$49 / year` (`Save 55%` — set `Yearly` as Default)**
- **Content Upload:** `09-EXPORTS/HYBRID-BUNDLE/Tier4-Living-OS-Pro-Vault-Membership-Pack.zip`

---

## 4. HOW TO LINK PRODUCT #1 & PRODUCT #2 SO GUMROAD'S ALGORITHM CONNECTS THEM TOGETHER

To make sure Gumroad's internal recommendation graph and checkout funnel treat **Link #1 (`4-Version Flagship`)** and **Link #2 (`VIP Membership`)** as one connected system:

1. **In-Cart Version Replacement Upsell (`Checkout -> Upsells -> New upsell`):**
   - **Type:** `Replace the version selected with another version of the same product`
   - **Product:** `The AI Freelancer Operating System (Link #1)`
   - **Trigger Versions:** Check `Tier 0 ($0)`, `Tier 1 ($19)`, and `Tier 2 ($39)`
   - **Offered Version:** `⭐ Tier 3: Complete Flagship AI Freelancer OS Bundle ($59)`
   - **Discount:** `$10 OFF` fixed discount (`$59 -> $49` instant checkout upgrade!)
2. **Cross-Product VIP Membership Upsell (`Checkout -> Upsells -> New upsell`):**
   - **Type:** `Add another product to the cart`
   - **Trigger Product:** `The AI Freelancer Operating System (Link #1)`
   - **Offered Product:** `VIP Living Freelancer OS & Pro Workflow Vault Membership (Link #2)`
3. **Identical Discover Category & Shared Primary Tags (`Share` Tab on Both Listings):**
   - Set **both** Product #1 and Product #2 to Category: `Business & Money > Management & Leadership` and share the core tags `freelancer`, `ai prompts`, `notion template`, `business system`. Gumroad Discover uses shared creator + shared tags + cross-checkout activity to display your second listing under **"More from OMAR SUNNY / Customers also bought"**!
4. **Bidirectional Footer Links Inside Both Product Descriptions:**
   - At the bottom of **Product #1's Description**, include:
     `👉 Want Monthly Niche AI Workflow Drops + All 84 Files in a Living Subscription? Join the VIP Living Freelancer OS Membership ($9/mo or $49/yr): https://gumroad.com/l/ai-freelancer-vip-vault`
   - At the bottom of **Product #2's Description**, include:
     `👉 Prefer a One-Time Purchase ($0 Starter Kit / $19 / $39 / $59)? View the One-Time Tiers Here: https://gumroad.com/l/ai-freelancer-os`
"""
    (GUMROAD_SETUP_DIR / "00-LOCKED-UNIFIED-4-VERSION-AND-MEMBERSHIP-SETUP.md").write_text(file0_locked_md, encoding="utf-8")
    print("[Step 2] Generated all 6 Master Gumroad Playbooks (including 00-LOCKED-UNIFIED-4-VERSION-AND-MEMBERSHIP-SETUP.md) inside 10-MARKETING/Gumroad-Hybrid-Master-Setup/.")


# ==============================================================================
# STEP 3: UPDATE TIER 4 VIP MEMBERSHIP ZIP ARCHIVE WITH PHASE 11 GUMROAD PACK
# ==============================================================================
def update_tier4_zip_with_gumroad_pack():
    HYBRID_BUNDLE_DIR.mkdir(parents=True, exist_ok=True)
    t4_primary = HYBRID_BUNDLE_DIR / "Tier4-Living-OS-Pro-Vault-Membership-Pack.zip"
    t4_alias = HYBRID_BUNDLE_DIR / "tier4-vip-living-career-vault-edition.zip"

    if not t4_primary.exists():
        raise RuntimeError(f"Expected {t4_primary} to exist before Phase 11 packaging.")

    # Append or rebuild Tier 4 ZIP so it contains all existing files + 09-GUMROAD-HYBRID-MASTER-SETUP/
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_zip = Path(tmpdir) / "t4_updated.zip"
        with zipfile.ZipFile(t4_primary, "r") as zin, zipfile.ZipFile(tmp_zip, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            existing_names = set()
            for item in zin.infolist():
                if not item.filename.startswith("09-GUMROAD-HYBRID-MASTER-SETUP/"):
                    zout.writestr(item, zin.read(item.filename))
                    existing_names.add(item.filename)

            for md_file in sorted(GUMROAD_SETUP_DIR.glob("*.md")):
                arc_name = f"09-GUMROAD-HYBRID-MASTER-SETUP/{md_file.name}"
                zout.write(md_file, arc_name)

            for tc_file in sorted(THUMBS_COVERS_DIR.glob("*")):
                if tc_file.is_file():
                    arc_name = f"09-GUMROAD-HYBRID-MASTER-SETUP/Thumbnails-and-Covers/{tc_file.name}"
                    zout.write(tc_file, arc_name)

        shutil.copy2(tmp_zip, t4_primary)
        shutil.copy2(tmp_zip, t4_alias)

    for zp in (t4_primary, t4_alias):
        with zipfile.ZipFile(zp, "r") as zcheck:
            corrupt = zcheck.testzip()
            if corrupt is not None:
                raise RuntimeError(f"Corrupt entry {corrupt} in {zp}")
            print(f"[Step 3] Updated {zp.name}: {len(zcheck.namelist())} files ({zp.stat().st_size:,} bytes)")


def main() -> int:
    print("=" * 84)
    print("PHASE 11 BUILDER — GUMROAD HYBRID 3-LISTING MASTER PACK & 600x600 SQUARE THUMBNAILS")
    print("=" * 84)
    build_square_thumbnails_and_copy_covers()
    build_gumroad_playbooks()
    update_tier4_zip_with_gumroad_pack()
    print("=" * 84)
    print("PHASE 11 BUILD COMPLETE — ALL THUMBNAILS, 5 PLAYBOOKS & ZIP ARCHIVES READY")
    print("=" * 84)
    return 0


if __name__ == "__main__":
    sys.exit(main())
