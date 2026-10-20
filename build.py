#!/usr/bin/env python3
"""
Master Single-Source Multi-Format Publishing Compiler (build.py)
Digital Knowledge Product Studio — The AI Freelancer Operating System (v1.0.0)

Compiles the verified single-source Markdown + YAML + SVG repository into 7 commercial deliverables:
1. 09-EXPORTS/PDF/the-ai-freelancer-os-complete-book.pdf (US Letter 8.5" x 11" Digital Book Edition)
2. 09-EXPORTS/PRINT/the-ai-freelancer-os-kdp-paperback-6x9.pdf (Amazon KDP 6" x 9" Print Interior PDF)
3. 09-EXPORTS/EPUB/the-ai-freelancer-os.epub (OCF EPUB 3.0 Reflowable eBook with 20 Vector SVGs)
4. 09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-us-letter.pdf (+ copy in 05-WORKBOOKS/)
5. 09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-a4.pdf (+ copy in 05-WORKBOOKS/)
6. 09-EXPORTS/PDF/the-ai-freelancer-os-tablet-planner.pdf (+ copy in 05-WORKBOOKS/)
7. 09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf (+ chapter-01-workbook.pdf in 05-WORKBOOKS/ & 09-EXPORTS/PRINT/)
"""

import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import markdown
import yaml
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, BooleanObject, DictionaryObject, NameObject, TextStringObject

BASE_DIR = Path(__file__).resolve().parent

CHAPTER_TITLES = {
    1: "Chapter 1: The Overwhelmed Freelancer's Bottleneck (The 5-Stage Operating Model)",
    2: "Chapter 2: Positioning & Productized Service Packaging",
    3: "Chapter 3: The 10-Minute Lead Triage & Proposal Engine",
    4: "Chapter 4: Precision Pricing, Estimation & Margin Defense",
    5: "Chapter 5: Zero-Friction Client Onboarding & Kickoff Architecture",
    6: "Chapter 6: AI-Assisted Project Execution & Quality Control",
    7: "Chapter 7: Defeating Scope Creep & Difficult Client Conversations",
    8: "Chapter 8: Async Client Updates & Revision Minimization",
    9: "Chapter 9: Smooth Offboarding, Case Studies & The Retainer Bridge",
    10: "Chapter 10: The Weekly CEO Review & 90-Day Scaling Roadmap",
}

WORKSHEET_TITLES = {
    1: "Worksheet 1.1: The 7-Day Time & Revenue Leak Audit",
    2: "Worksheet 2.1: The 3-Tier Productized Offer & Scope Boundary Matrix",
    3: "Worksheet 3.1: The P.A.C.E. Lead Triage & 10-Minute B.R.I.E.F. Proposal Builder",
    4: "Worksheet 4.1: The B.C.R. Precision Pricing & Margin Defense Calculator",
    5: "Worksheet 5.1: The 48-Hour Onboarding & Asset Gate Checklist",
    6: "Worksheet 6.1: The 20/60/20 Sandwich Execution & 4-Gate Quality Assurance Workbook",
    7: "Worksheet 7.1: The P.V.P. Scope Boundary, Change Order & Late-Payment Escalation Log",
    8: "Worksheet 8.1: The 3-Pillar Async Status, Loom Walkthrough & Guided Feedback Tracker",
    9: "Worksheet 9.1: Executive Handover, Testimonial Capture & Offboard-to-Retainer Bridge",
    10: "Worksheet 10.1: The 20-Minute Friday CEO Scorecard, Client EHR Pruning & 90-Day Scaling Roadmap",
}


def find_headless_browser() -> str:
    """Locate Microsoft Edge or Google Chrome on Windows for high-precision CSS @page PDF rendering."""
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


def load_svg_clean(svg_filename: str) -> str:
    """Load an SVG file from 04-VISUAL-ASSETS and strip XML/DOCTYPE declarations for inline HTML5 embedding."""
    if "mindmap" in svg_filename:
        svg_path = BASE_DIR / "04-VISUAL-ASSETS" / "Mindmaps" / svg_filename
    else:
        svg_path = BASE_DIR / "04-VISUAL-ASSETS" / "Flowcharts" / svg_filename

    if not svg_path.exists():
        raise FileNotFoundError(f"Missing SVG asset: {svg_path}")

    raw_svg = svg_path.read_text(encoding="utf-8")
    raw_svg = re.sub(r"<\?xml[^>]*\?>", "", raw_svg, flags=re.IGNORECASE).strip()
    raw_svg = re.sub(r"<!DOCTYPE[^>]*>", "", raw_svg, flags=re.IGNORECASE).strip()
    # Ensure responsive scaling inside figure containers
    if 'width="100%"' not in raw_svg:
        raw_svg = re.sub(
            r"<svg\b([^>]*?)>",
            lambda m: "<svg" + re.sub(r'\s+(width|height)="[^"]*"', "", m.group(1)) + ' width="100%" height="auto">',
            raw_svg,
            count=1,
        )
    return raw_svg


def preprocess_markdown_for_html(md_text: str, inline_svg: bool = True) -> str:
    """
    Prepare Markdown text for HTML/XHTML conversion:
    - Convert display/inline LaTeX math formulas into clean styled formula blocks
    - Replace Markdown SVG image embeds with inline <figure><svg>...</svg></figure> (or EPUB <img> tags)
    - Convert prose relative links to .svg files into internal figure anchor links
    - Convert [ ] checkboxes into crisp visual checkbox symbols
    """
    # 1. Convert display math $$...$$ into styled formula callout
    def replace_display_math(match: re.Match) -> str:
        expr = match.group(1).strip()
        expr = re.sub(r"\\text\{([^}]*)\}", r"\1", expr)
        expr = re.sub(
            r"\\frac\{([^}]*)\}\{([^}]*)\}",
            r"(\1) ÷ (\2)",
            expr,
        )
        expr = expr.replace(r"\times", "×").replace(r"\div", "÷").replace(r"\approx", "≈")
        return f'\n<div class="formula-callout"><code>{html.escape(expr)}</code></div>\n'

    md_text = re.sub(r"\$\$(.*?)\$\$", replace_display_math, md_text, flags=re.DOTALL)

    # 2. Replace ![Alt](...chapter-XX-mindmap.svg) image embeds
    def replace_svg_image(match: re.Match) -> str:
        alt_text = match.group(1).strip()
        rel_path = match.group(2).strip()
        svg_name = Path(rel_path).name
        fig_id = f"fig-{svg_name.replace('.svg', '')}"
        if inline_svg:
            svg_xml = load_svg_clean(svg_name)
            return (
                f'\n<figure class="diagram-figure" id="{fig_id}">\n'
                f'  <div class="svg-wrapper">{svg_xml}</div>\n'
                f"  <figcaption>{html.escape(alt_text)} ({html.escape(svg_name)})</figcaption>\n"
                f"</figure>\n"
            )
        else:
            return (
                f'\n<figure class="diagram-figure" id="{fig_id}">\n'
                f'  <img src="{html.escape(svg_name)}" alt="{html.escape(alt_text)}" class="epub-diagram"/>\n'
                f"  <figcaption>{html.escape(alt_text)}</figcaption>\n"
                f"</figure>\n"
            )

    md_text = re.sub(
        r"!\[([^\]]*)\]\(([^)]+\.svg)\)",
        replace_svg_image,
        md_text,
    )

    # 3. Replace inline prose links [chapter-XX-mindmap.svg](../../04-VISUAL-ASSETS/.../chapter-XX-mindmap.svg)
    def replace_svg_prose_link(match: re.Match) -> str:
        label = match.group(1).strip()
        rel_path = match.group(2).strip()
        svg_name = Path(rel_path).name
        fig_id = f"fig-{svg_name.replace('.svg', '')}"
        return f'<a href="#{fig_id}" class="diagram-ref"><code>{html.escape(label)}</code></a>'

    md_text = re.sub(
        r"(?<!!)\[([^\]]+)\]\(([^)]+\.svg)\)",
        replace_svg_prose_link,
        md_text,
    )

    # 4. Replace interactive Markdown checkboxes "- [ ]" or "* [ ]"
    md_text = re.sub(r"^(\s*[-*]\s+)\[\s\]\s+", r"\1☐ ", md_text, flags=re.MULTILINE)
    md_text = re.sub(r"^(\s*[-*]\s+)\[[xX]\]\s+", r"\1☑ ", md_text, flags=re.MULTILINE)

    return md_text


def md_to_html(md_text: str, inline_svg: bool = True) -> str:
    """Convert single-source Markdown into semantic HTML5 with tables and fenced code blocks."""
    prepared = preprocess_markdown_for_html(md_text, inline_svg=inline_svg)
    html_out = markdown.markdown(
        prepared,
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html",
    )
    return html_out


def sanitize_to_strict_xhtml(html_fragment: str) -> str:
    """
    Convert HTML fragment into 100% strict XML-parseable XHTML for EPUB 3.0:
    - Self-close all HTML void elements (<br/>, <hr/>, <img .../>, <meta .../>, <link .../>, <input .../>, <col .../>)
    - Convert any named HTML entities into Unicode characters, preserving only XML standard entities
    """
    # Self-close void tags
    html_fragment = re.sub(r"<br\s*/?>", "<br/>", html_fragment, flags=re.IGNORECASE)
    html_fragment = re.sub(r"<hr\s*/?>", "<hr/>", html_fragment, flags=re.IGNORECASE)
    html_fragment = re.sub(r"<img\b([^>]*?)(?<!/)>", r"<img\1/>", html_fragment, flags=re.IGNORECASE)
    html_fragment = re.sub(r"<col\b([^>]*?)(?<!/)>", r"<col\1/>", html_fragment, flags=re.IGNORECASE)
    html_fragment = re.sub(r"<input\b([^>]*?)(?<!/)>", r"<input\1/>", html_fragment, flags=re.IGNORECASE)

    # Replace named entities (except amp, lt, gt, quot, apos) with their Unicode characters
    def fix_entity(match: re.Match) -> str:
        ent = match.group(0)
        name = match.group(1)
        if name in ("amp", "lt", "gt", "quot", "apos"):
            return ent
        return html.unescape(ent)

    html_fragment = re.sub(r"&([a-zA-Z0-9]+);", fix_entity, html_fragment)
    # Escape any bare ampersands not part of a valid XML entity
    html_fragment = re.sub(r"&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)", "&amp;", html_fragment)
    return html_fragment


def get_book_css(mode: str = "digital_letter") -> str:
    """Return CSS stylesheet tailored for Digital US Letter PDF, KDP 6x9 Print Paperback, Workbooks, or Tablet Planner."""
    if mode == "digital_letter":
        page_rule = "@page { size: letter; margin: 18mm 19mm; }"
        body_font_size = "10pt"
        body_line_height = "1.58"
        code_font_size = "8.8pt"
        table_font_size = "8.8pt"
        accent_color = "#0284C7"
        primary_color = "#0F172A"
        secondary_color = "#0D9488"
        code_border = "3px solid #0284C7"
    elif mode == "kdp_6x9":
        page_rule = "@page { size: 6in 9in; margin: 0.7in 0.6in 0.75in 0.8in; }"
        body_font_size = "9.5pt"
        body_line_height = "1.5"
        code_font_size = "8pt"
        table_font_size = "8.2pt"
        accent_color = "#000000"
        primary_color = "#000000"
        secondary_color = "#1E293B"
        code_border = "1.5px solid #0F172A"
    elif mode == "workbook_letter":
        page_rule = "@page { size: letter; margin: 15mm 16mm; }"
        body_font_size = "9.8pt"
        body_line_height = "1.55"
        code_font_size = "8.6pt"
        table_font_size = "8.8pt"
        accent_color = "#0284C7"
        primary_color = "#0F172A"
        secondary_color = "#0D9488"
        code_border = "2.5px solid #0284C7"
    elif mode == "workbook_a4":
        page_rule = "@page { size: A4; margin: 15mm 16mm; }"
        body_font_size = "9.8pt"
        body_line_height = "1.55"
        code_font_size = "8.6pt"
        table_font_size = "8.8pt"
        accent_color = "#0284C7"
        primary_color = "#0F172A"
        secondary_color = "#0D9488"
        code_border = "2.5px solid #0284C7"
    elif mode == "tablet_landscape":
        page_rule = "@page { size: 11in 8.5in; margin: 12mm 15mm; }"
        body_font_size = "9.8pt"
        body_line_height = "1.52"
        code_font_size = "8.6pt"
        table_font_size = "8.8pt"
        accent_color = "#0284C7"
        primary_color = "#0F172A"
        secondary_color = "#0D9488"
        code_border = "2.5px solid #0D9488"
    else:
        raise ValueError(f"Unknown CSS mode: {mode}")

    return f"""
{page_rule}
* {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}}
html, body {{
    margin: 0;
    padding: 0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
    font-size: {body_font_size};
    line-height: {body_line_height};
    color: #1E293B;
    background-color: #FFFFFF;
}}
h1, h2, h3, h4 {{
    color: {primary_color};
    font-weight: 700;
    line-height: 1.25;
    margin-top: 1.2em;
    margin-bottom: 0.45em;
    page-break-after: avoid;
    break-after: avoid;
}}
h1 {{
    font-size: 1.65em;
    border-bottom: 2px solid {primary_color};
    padding-bottom: 6px;
    margin-top: 0;
}}
h2 {{
    font-size: 1.28em;
    border-bottom: 1px solid #CBD5E1;
    padding-bottom: 4px;
}}
h3 {{
    font-size: 1.08em;
    color: {accent_color};
}}
p {{
    margin-top: 0;
    margin-bottom: 0.72em;
    text-align: left;
}}
ul, ol {{
    margin-top: 0;
    margin-bottom: 0.8em;
    padding-left: 1.4em;
}}
li {{
    margin-bottom: 0.32em;
}}
hr {{
    border: none;
    border-top: 1px solid #E2E8F0;
    margin: 1.2em 0;
}}
a {{
    color: {accent_color};
    text-decoration: none;
}}
a:hover {{
    text-decoration: underline;
}}
code {{
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    font-size: 0.9em;
    background-color: #F1F5F9;
    color: #0F172A;
    padding: 1px 4px;
    border-radius: 3px;
}}
pre {{
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    font-size: {code_font_size};
    line-height: 1.45;
    background-color: #F8FAFC;
    color: #0F172A;
    border: 1px solid #CBD5E1;
    border-left: {code_border};
    border-radius: 5px;
    padding: 10px 12px;
    margin: 0.85em 0;
    white-space: pre-wrap;
    word-wrap: break-word;
    overflow-wrap: anywhere;
    page-break-inside: auto;
}}
pre code {{
    background: transparent;
    padding: 0;
    font-size: inherit;
    color: inherit;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 0.9em 0;
    font-size: {table_font_size};
    line-height: 1.38;
    table-layout: auto;
    page-break-inside: auto;
}}
tr {{
    page-break-inside: avoid;
    break-inside: avoid;
}}
thead th {{
    background-color: {primary_color};
    color: #FFFFFF;
    font-weight: 700;
    text-align: left;
    padding: 6px 8px;
    border-top: 2px solid {primary_color};
    border-bottom: 2px solid {primary_color};
}}
tbody td {{
    padding: 6px 8px;
    border-bottom: 1px solid #E2E8F0;
    vertical-align: top;
    overflow-wrap: break-word;
}}
tbody tr:nth-child(even) {{
    background-color: #F8FAFC;
}}
figure.diagram-figure {{
    width: 100%;
    margin: 1.0em 0;
    padding: 8px;
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    page-break-inside: avoid;
    break-inside: avoid;
    text-align: center;
}}
figure.diagram-figure .svg-wrapper {{
    width: 100%;
    max-width: 100%;
    overflow: hidden;
}}
figure.diagram-figure svg {{
    width: 100% !important;
    height: auto !important;
    max-height: 410px;
    display: block;
    margin: 0 auto;
}}
figure.diagram-figure figcaption {{
    font-size: 8.5pt;
    color: #64748B;
    font-weight: 600;
    margin-top: 6px;
}}
.formula-callout {{
    background-color: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-left: 3px solid {secondary_color};
    padding: 8px 12px;
    margin: 0.8em 0;
    border-radius: 4px;
    font-weight: 600;
    text-align: center;
}}
.chapter-section {{
    page-break-before: always;
    break-before: page;
}}
.cover-page {{
    page-break-after: always;
    break-after: page;
}}
.cover-banner {{
    background-color: {primary_color};
    color: #FFFFFF;
    padding: 28px 26px;
    border-radius: 8px;
    border-bottom: 5px solid {accent_color};
    margin-bottom: 18px;
}}
.cover-badge {{
    display: inline-block;
    background-color: {accent_color};
    color: #FFFFFF;
    font-size: 8.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 4px 10px;
    border-radius: 4px;
    margin-bottom: 12px;
}}
.cover-title {{
    font-size: 24pt;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.15;
    margin: 0 0 10px 0;
    border: none;
}}
.cover-subtitle {{
    font-size: 11.5pt;
    font-weight: 500;
    color: #E2E8F0;
    line-height: 1.45;
    margin: 0 0 14px 0;
}}
.cover-meta {{
    font-size: 9pt;
    color: #94A3B8;
}}
.nav-directory-box {{
    background-color: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 14px 18px;
    margin: 14px 0;
}}
.planner-navbar {{
    background-color: #0F172A;
    color: #FFFFFF;
    padding: 7px 10px;
    border-radius: 6px;
    margin-bottom: 12px;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    align-items: center;
    justify-content: space-between;
}}
.planner-navbar a.pill-tab {{
    display: inline-block;
    background-color: #1E293B;
    color: #F8FAFC;
    font-size: 7.8pt;
    font-weight: 600;
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid #334155;
    text-decoration: none;
}}
.planner-navbar a.pill-tab.active {{
    background-color: #0284C7;
    border-color: #38BDF8;
    color: #FFFFFF;
}}
"""


def build_cover_html(config: dict, edition_label: str) -> str:
    """Create the Page 1 Cover & Executive Architecture Imprint page."""
    bib = config.get("bibliographic_metadata", {})
    title = bib.get("title", "The AI Freelancer Operating System")
    subtitle = bib.get(
        "subtitle",
        "A Practical System to Organize Clients, Automate Repetitive Work, Manage Projects, and Build a More Productive Freelance Business",
    )
    publisher = bib.get("publisher", "Digital Knowledge Product Studio")
    imprint = bib.get("imprint", "Practitioner Systems Press")
    copyright_notice = bib.get("copyright_notice", "")
    ai_statement = bib.get("kdp_ai_disclosure", {}).get("statement", "")

    chapter_links_rows = []
    for n in range(1, 11):
        ch_id = f"chapter-{n:02d}"
        ch_title = CHAPTER_TITLES[n]
        stage_map = {
            1: "Stage 01: Foundation Gate",
            2: "Stage 01: Packaging Gate",
            3: "Stage 02: Lead Triage Gate",
            4: "Stage 02: Commercial Pricing Gate",
            5: "Stage 03: 48-Hr Kickoff Gate",
            6: "Stage 04: 20/60/20 Execution Gate",
            7: "Stage 04: P.V.P. Scope Defense Gate",
            8: "Stage 04: Async Delivery Gate",
            9: "Stage 05: Retainer Bridge Gate",
            10: "Stage 05: Friday CEO Scaling Gate",
        }[n]
        chapter_links_rows.append(
            f"<tr>"
            f"<td><strong><a href='#{ch_id}'>Chapter {n:02d}</a></strong></td>"
            f"<td><a href='#{ch_id}'>{html.escape(ch_title.split(': ', 1)[1])}</a></td>"
            f"<td><code>{stage_map}</code></td>"
            f"<td>Prompts {n}.1–{n}.5 + 2 Vector SVGs + Worksheet {n}.1</td>"
            f"</tr>"
        )

    return f"""
<section id="book-cover" class="cover-page">
  <div class="cover-banner">
    <div class="cover-badge">{html.escape(edition_label)}</div>
    <h1 class="cover-title">{html.escape(title)}</h1>
    <div class="cover-subtitle">{html.escape(subtitle)}</div>
    <div class="cover-meta">
      <strong>{html.escape(publisher)}</strong> • {html.escape(imprint)} • Version 1.0.0 (2026)<br/>
      United States (US) • United Kingdom (UK) • Canada (CA) • Australia (AU)
    </div>
  </div>

  <div class="nav-directory-box">
    <h3 style="margin-top:0;">Interactive Quick-Jump Navigation Directory</h3>
    <p style="margin-bottom:8px; font-size:9pt;">
      Click any section link below to jump directly to that operational unit:
      <a href="#front-matter"><strong>[Front Matter &amp; Manifesto]</strong></a> •
      <a href="#toc-section"><strong>[Master Table of Contents]</strong></a> •
      <a href="#back-matter"><strong>[Back Matter: 50-Prompt Index &amp; 12 Emergency Scripts]</strong></a>
    </p>
    <table>
      <thead>
        <tr>
          <th style="width:13%;">Unit</th>
          <th style="width:37%;">Operational Module Title</th>
          <th style="width:23%;">Lifecycle Gate</th>
          <th style="width:27%;">Included Systems</th>
        </tr>
      </thead>
      <tbody>
        {''.join(chapter_links_rows)}
      </tbody>
    </table>
  </div>

  <div style="font-size:8.2pt; color:#64748B; margin-top:12px; line-height:1.4;">
    <p><strong>Publication &amp; Copyright Governance:</strong> {html.escape(copyright_notice)}</p>
    <p><strong>Editorial &amp; Technical Verification Disclosure:</strong> {html.escape(ai_statement)}</p>
  </div>
</section>
"""


def render_html_to_pdf(browser_exe: str, html_content: str, output_pdf_path: Path) -> None:
    """Render an HTML5 document with inline SVGs and CSS @page rules to PDF via headless Chromium."""
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_html = Path(tmp_dir) / "compile_source.html"
        tmp_html.write_text(html_content, encoding="utf-8")
        profile_dir = Path(tmp_dir) / "edge_profile"
        profile_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            browser_exe,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-extensions",
            f"--user-data-dir={profile_dir}",
            "--no-pdf-header-footer",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={output_pdf_path}",
            tmp_html.as_uri(),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if not output_pdf_path.exists() or output_pdf_path.stat().st_size == 0:
            raise RuntimeError(
                f"Failed to compile PDF {output_pdf_path}. Return code={res.returncode}, stderr={res.stderr}"
            )


def stamp_pdf_metadata(
    pdf_path: Path,
    title: str,
    subject: str,
    keywords: str,
    init_acroform: bool = False,
) -> int:
    """Inject bibliographic PDF metadata and optional /AcroForm interactive dictionary via pypdf."""
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    writer.add_metadata(
        {
            "/Title": title,
            "/Author": "Digital Knowledge Product Studio",
            "/Subject": subject,
            "/Keywords": keywords,
            "/Creator": "Digital Knowledge Product Studio — Single-Source Compiler (build.py)",
            "/Producer": "Practitioner Systems Press PDF Engine v1.0",
        }
    )

    if init_acroform:
        acroform = DictionaryObject()
        acroform.update(
            {
                NameObject("/Fields"): ArrayObject(),
                NameObject("/NeedAppearances"): BooleanObject(True),
                NameObject("/DA"): TextStringObject("/Helv 10 Tf 0 g"),
            }
        )
        writer._root_object[NameObject("/AcroForm")] = acroform

    tmp_pdf = pdf_path.with_suffix(".stamped.pdf")
    with open(tmp_pdf, "wb") as f_out:
        writer.write(f_out)
    shutil.move(str(tmp_pdf), str(pdf_path))
    return len(reader.pages)


def build_full_book_html(config: dict, mode: str, edition_label: str) -> str:
    """Assemble the complete book HTML5 document (Cover + Front Matter + TOC + Chapters 1-10 + Back Matter)."""
    css = get_book_css(mode)
    cover_html = build_cover_html(config, edition_label)

    fm_md = (BASE_DIR / "03-MANUSCRIPT/Front-Matter/front-matter.md").read_text(encoding="utf-8")
    toc_md = (BASE_DIR / "03-MANUSCRIPT/Front-Matter/toc.md").read_text(encoding="utf-8")
    bm_md = (BASE_DIR / "03-MANUSCRIPT/Back-Matter/back-matter.md").read_text(encoding="utf-8")

    # Enhance TOC Markdown with clickable anchor links to each chapter
    for n in range(1, 11):
        ch_anchor = f"#chapter-{n:02d}"
        toc_md = re.sub(
            rf"(###\s+Chapter\s+{n}:\s+[^\n]+)",
             lambda m, a=ch_anchor: f"{m.group(1)} ([Jump to Chapter]({a}))",
            toc_md,
        )

    fm_html = md_to_html(fm_md, inline_svg=True)
    toc_html = md_to_html(toc_md, inline_svg=True)
    bm_html = md_to_html(bm_md, inline_svg=True)

    chapters_html_blocks = []
    for n in range(1, 11):
        ch_path = BASE_DIR / "03-MANUSCRIPT/Chapters" / f"chapter-{n:02d}.md"
        ch_md = ch_path.read_text(encoding="utf-8")
        ch_html = md_to_html(ch_md, inline_svg=True)
        chapters_html_blocks.append(
            f'<section id="chapter-{n:02d}" class="chapter-section">\n{ch_html}\n</section>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>The AI Freelancer Operating System — {html.escape(edition_label)}</title>
  <style>{css}</style>
</head>
<body>
  {cover_html}
  <section id="front-matter" class="chapter-section">
    {fm_html}
  </section>
  <section id="toc-section" class="chapter-section">
    {toc_html}
  </section>
  {''.join(chapters_html_blocks)}
  <section id="back-matter" class="chapter-section">
    {bm_html}
  </section>
</body>
</html>
"""


def build_epub_3(config: dict, epub_path: Path) -> dict:
    """
    Build a 100% standards-compliant Reflowable EPUB 3.0 package:
    - First entry: uncompressed `mimetype` (`application/epub+zip`)
    - META-INF/container.xml
    - OEBPS/content.opf, OEBPS/nav.xhtml, OEBPS/toc.ncx, OEBPS/styles.css
    - OEBPS/front-matter.xhtml, toc.xhtml, chapter-01.xhtml..chapter-10.xhtml, back-matter.xhtml
    - OEBPS/chapter-01-mindmap.svg..chapter-10-flowchart.svg (all 20 SVGs)
    - Validates every XML/XHTML/OPF/NCX file via xml.etree.ElementTree.fromstring() during build.
    """
    epub_path.parent.mkdir(parents=True, exist_ok=True)
    bib = config.get("bibliographic_metadata", {})
    book_title = bib.get("title", "The AI Freelancer Operating System")
    book_subtitle = bib.get("subtitle", "")
    publisher = bib.get("publisher", "Digital Knowledge Product Studio")
    book_uuid = "urn:uuid:a1f4ee10-2026-4000-9000-010203040506"
    modified_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    epub_css = """
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #1E293B;
    background-color: #FFFFFF;
    margin: 1em;
}
h1, h2, h3, h4 {
    color: #0F172A;
    font-weight: 700;
    line-height: 1.3;
    margin-top: 1.2em;
    margin-bottom: 0.4em;
}
h1 { font-size: 1.5em; border-bottom: 2px solid #0F172A; padding-bottom: 0.25em; }
h2 { font-size: 1.25em; border-bottom: 1px solid #CBD5E1; padding-bottom: 0.2em; }
h3 { font-size: 1.08em; color: #0284C7; }
pre {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85em;
    background-color: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-left: 3px solid #0284C7;
    padding: 0.8em;
    white-space: pre-wrap;
    word-wrap: break-word;
}
code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9em;
    background-color: #F1F5F9;
    padding: 0.1em 0.3em;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 0.85em;
}
th {
    background-color: #0F172A;
    color: #FFFFFF;
    padding: 0.45em;
    text-align: left;
}
td {
    padding: 0.45em;
    border-bottom: 1px solid #E2E8F0;
    vertical-align: top;
}
figure.diagram-figure {
    margin: 1.2em 0;
    padding: 0.5em;
    border: 1px solid #CBD5E1;
    text-align: center;
}
img.epub-diagram {
    max-width: 100%;
    height: auto;
}
figcaption {
    font-size: 0.8em;
    color: #64748B;
    margin-top: 0.4em;
}
.formula-callout {
    background-color: #F8FAFC;
    border-left: 3px solid #0D9488;
    padding: 0.6em;
    margin: 0.8em 0;
    text-align: center;
}
"""

    def wrap_xhtml_doc(doc_title: str, body_inner: str) -> str:
        clean_body = sanitize_to_strict_xhtml(body_inner)
        xhtml_str = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">\n'
            "<head>\n"
            '  <meta charset="UTF-8"/>\n'
            f"  <title>{html.escape(doc_title)}</title>\n"
            '  <link rel="stylesheet" type="text/css" href="styles.css"/>\n'
            "</head>\n"
            "<body>\n"
            f"{clean_body}\n"
            "</body>\n"
            "</html>\n"
        )
        # Validate XML well-formedness immediately
        ET.fromstring(xhtml_str.encode("utf-8"))
        return xhtml_str

    xhtml_files = {}
    spine_items = []

    # 1. Front Matter
    fm_md = (BASE_DIR / "03-MANUSCRIPT/Front-Matter/front-matter.md").read_text(encoding="utf-8")
    xhtml_files["front-matter.xhtml"] = wrap_xhtml_doc(
        "Front Matter — The AI Freelancer Operating System",
        md_to_html(fm_md, inline_svg=False),
    )
    spine_items.append(("front-matter", "front-matter.xhtml", "Front Matter & System Quick-Start"))

    # 2. Master TOC
    toc_md = (BASE_DIR / "03-MANUSCRIPT/Front-Matter/toc.md").read_text(encoding="utf-8")
    xhtml_files["toc.xhtml"] = wrap_xhtml_doc(
        "Master Table of Contents & System Architecture",
        md_to_html(toc_md, inline_svg=False),
    )
    spine_items.append(("toc-doc", "toc.xhtml", "Master Table of Contents & Architecture"))

    # 3. Chapters 1–10
    for n in range(1, 11):
        ch_fname = f"chapter-{n:02d}.xhtml"
        ch_md = (BASE_DIR / "03-MANUSCRIPT/Chapters" / f"chapter-{n:02d}.md").read_text(encoding="utf-8")
        ch_title = CHAPTER_TITLES[n]
        xhtml_files[ch_fname] = wrap_xhtml_doc(ch_title, md_to_html(ch_md, inline_svg=False))
        spine_items.append((f"chapter-{n:02d}", ch_fname, ch_title))

    # 4. Back Matter Vault
    bm_md = (BASE_DIR / "03-MANUSCRIPT/Back-Matter/back-matter.md").read_text(encoding="utf-8")
    xhtml_files["back-matter.xhtml"] = wrap_xhtml_doc(
        "Back Matter Vault — 50-Prompt Index & Emergency Client Scripts",
        md_to_html(bm_md, inline_svg=False),
    )
    spine_items.append(("back-matter", "back-matter.xhtml", "Back Matter Vault: 50 Prompts & 12 Scripts"))

    # Build OEBPS/nav.xhtml
    nav_lis = "\n".join(
        f'        <li><a href="{fname}">{html.escape(label)}</a></li>'
        for _, fname, label in spine_items
    )
    nav_xhtml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">\n'
        "<head>\n"
        '  <meta charset="UTF-8"/>\n'
        f"  <title>{html.escape(book_title)} — Navigation</title>\n"
        '  <link rel="stylesheet" type="text/css" href="styles.css"/>\n'
        "</head>\n"
        "<body>\n"
        '  <nav epub:type="toc" id="toc">\n'
        "    <h1>Table of Contents</h1>\n"
        "    <ol>\n"
        f"{nav_lis}\n"
        "    </ol>\n"
        "  </nav>\n"
        "</body>\n"
        "</html>\n"
    )
    ET.fromstring(nav_xhtml.encode("utf-8"))

    # Build OEBPS/toc.ncx
    nav_points = []
    for idx, (item_id, fname, label) in enumerate(spine_items, start=1):
        nav_points.append(
            f'    <navPoint id="navPoint-{idx}" playOrder="{idx}">\n'
            f"      <navLabel><text>{html.escape(label)}</text></navLabel>\n"
            f'      <content src="{fname}"/>\n'
            f"    </navPoint>"
        )
    toc_ncx = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n'
        "  <head>\n"
        f'    <meta name="dtb:uid" content="{book_uuid}"/>\n'
        '    <meta name="dtb:depth" content="1"/>\n'
        '    <meta name="dtb:totalPageCount" content="0"/>\n'
        '    <meta name="dtb:maxPageNumber" content="0"/>\n'
        "  </head>\n"
        f"  <docTitle><text>{html.escape(book_title)}</text></docTitle>\n"
        "  <navMap>\n"
        f"{chr(10).join(nav_points)}\n"
        "  </navMap>\n"
        "</ncx>\n"
    )
    ET.fromstring(toc_ncx.encode("utf-8"))

    # Collect all 20 SVG files
    svg_manifest_items = []
    svg_files_map = {}
    for n in range(1, 11):
        mm_name = f"chapter-{n:02d}-mindmap.svg"
        fc_name = f"chapter-{n:02d}-flowchart.svg"
        mm_path = BASE_DIR / "04-VISUAL-ASSETS/Mindmaps" / mm_name
        fc_path = BASE_DIR / "04-VISUAL-ASSETS/Flowcharts" / fc_name
        svg_files_map[mm_name] = mm_path.read_text(encoding="utf-8")
        svg_files_map[fc_name] = fc_path.read_text(encoding="utf-8")
        svg_manifest_items.append(
            f'    <item id="svg-mm-{n:02d}" href="{mm_name}" media-type="image/svg+xml"/>'
        )
        svg_manifest_items.append(
            f'    <item id="svg-fc-{n:02d}" href="{fc_name}" media-type="image/svg+xml"/>'
        )

    doc_manifest_items = [
        '    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
        '    <item id="css" href="styles.css" media-type="text/css"/>',
    ]
    spine_itemrefs = ['    <itemref idref="nav" linear="yes"/>']
    for item_id, fname, _ in spine_items:
        props = ' properties="svg"' if fname.startswith("chapter-") else ""
        doc_manifest_items.append(
            f'    <item id="{item_id}" href="{fname}" media-type="application/xhtml+xml"{props}/>'
        )
        spine_itemrefs.append(f'    <itemref idref="{item_id}"/>')

    content_opf = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" version="3.0" unique-identifier="pub-id">\n'
        "  <metadata>\n"
        f'    <dc:identifier id="pub-id">{book_uuid}</dc:identifier>\n'
        f"    <dc:title>{html.escape(book_title)}: {html.escape(book_subtitle)}</dc:title>\n"
        f"    <dc:creator>{html.escape(publisher)}</dc:creator>\n"
        f"    <dc:publisher>{html.escape(publisher)}</dc:publisher>\n"
        "    <dc:language>en-US</dc:language>\n"
        "    <dc:description>A Practical System to Organize Clients, Automate Repetitive Work, Manage Projects, and Build a More Productive Freelance Business.</dc:description>\n"
        f'    <meta property="dcterms:modified">{modified_utc}</meta>\n'
        "  </metadata>\n"
        "  <manifest>\n"
        f"{chr(10).join(doc_manifest_items)}\n"
        f"{chr(10).join(svg_manifest_items)}\n"
        "  </manifest>\n"
        '  <spine toc="ncx">\n'
        f"{chr(10).join(spine_itemrefs)}\n"
        "  </spine>\n"
        "</package>\n"
    )
    ET.fromstring(content_opf.encode("utf-8"))

    container_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
        "  <rootfiles>\n"
        '    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n'
        "  </rootfiles>\n"
        "</container>\n"
    )
    ET.fromstring(container_xml.encode("utf-8"))

    with zipfile.ZipFile(epub_path, "w") as zf:
        # 1. mimetype MUST be first and uncompressed (ZIP_STORED)
        zf.writestr("mimetype", b"application/epub+zip", compress_type=zipfile.ZIP_STORED)
        # 2. META-INF/container.xml
        zf.writestr("META-INF/container.xml", container_xml.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        # 3. Core OEBPS package files
        zf.writestr("OEBPS/content.opf", content_opf.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/nav.xhtml", nav_xhtml.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/toc.ncx", toc_ncx.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr("OEBPS/styles.css", epub_css.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        # 4. XHTML content files
        for fname, xhtml_str in xhtml_files.items():
            zf.writestr(f"OEBPS/{fname}", xhtml_str.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
        # 5. All 20 SVG diagrams
        for svg_name, svg_str in svg_files_map.items():
            zf.writestr(f"OEBPS/{svg_name}", svg_str.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)

    return {
        "xhtml_count": len(xhtml_files),
        "svg_count": len(svg_files_map),
        "file_size_bytes": epub_path.stat().st_size,
    }


def build_workbook_html(mode: str, edition_label: str) -> str:
    """Assemble the 10-Chapter Printable & Fillable Action Workbook HTML (US Letter or ISO A4)."""
    css = get_book_css(mode)
    index_rows = []
    for n in range(1, 11):
        ws_id = f"ws-{n:02d}"
        index_rows.append(
            f"<tr>"
            f"<td><strong><a href='#{ws_id}'>Worksheet {n}.1</a></strong></td>"
            f"<td><a href='#{ws_id}'>{html.escape(WORKSHEET_TITLES[n].split(': ', 1)[1])}</a></td>"
            f"<td>Chapter {n:02d} • Prompts {n}.1–{n}.5</td>"
            f"<td><code>☐ Pending  ☐ Installed</code></td>"
            f"<td><code>____ / ____ / 2026</code></td>"
            f"</tr>"
        )

    cover_html = f"""
<section id="workbook-cover" class="cover-page">
  <div class="cover-banner">
    <div class="cover-badge">{html.escape(edition_label)}</div>
    <h1 class="cover-title">The AI Freelancer Operating System — Interactive Action Workbook</h1>
    <div class="cover-subtitle">
      10 Standalone 5-Part Operational Worksheets (Worksheets 1.1 through 10.1) for Auditing Effective Hourly Rate, Packaging 3-Tier Offers, Pricing with B.C.R., Defending Scope Boundaries, and Scaling as a Weekly CEO
    </div>
    <div class="cover-meta">
      <strong>Digital Knowledge Product Studio</strong> • Tier 2 &amp; Tier 3 Interactive Workbook Suite • Print &amp; AcroForm Edition
    </div>
  </div>

  <div class="nav-directory-box">
    <h3 style="margin-top:0;">Practitioner 10-Stage Implementation Index &amp; Sign-Off Tracker</h3>
    <p style="font-size:9pt; margin-bottom:8px;">
      Click any worksheet title below to jump directly to its five-part execution template (`Part A` through `Part E`):
    </p>
    <table>
      <thead>
        <tr>
          <th style="width:14%;">Worksheet</th>
          <th style="width:38%;">Operational Audit &amp; Execution Template</th>
          <th style="width:20%;">Paired Chapter</th>
          <th style="width:16%;">Installation Status</th>
          <th style="width:12%;">Sign-Off Date</th>
        </tr>
      </thead>
      <tbody>
        {''.join(index_rows)}
      </tbody>
    </table>
  </div>
</section>
"""

    ws_sections = []
    for n in range(1, 11):
        ws_path = BASE_DIR / "05-WORKBOOKS" / f"worksheet-{n:02d}.md"
        ws_md = ws_path.read_text(encoding="utf-8")
        ws_html = md_to_html(ws_md, inline_svg=True)
        ws_sections.append(
            f'<section id="ws-{n:02d}" class="chapter-section">\n{ws_html}\n</section>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>The AI Freelancer Operating System — {html.escape(edition_label)}</title>
  <style>{css}</style>
</head>
<body>
  {cover_html}
  {''.join(ws_sections)}
</body>
</html>
"""


def render_planner_navbar(active_tab: str) -> str:
    """Render the persistent top hyperlinked pill navigation bar for the Landscape Tablet Planner."""
    tabs = [
        ("home", "Home Dashboard", "#planner-home"),
        ("gate1", "Gate 1: Attract (WS 1–2)", "#ws-01"),
        ("gate2", "Gate 2: Scope & Price (WS 3–4)", "#ws-03"),
        ("gate3", "Gate 3: Onboard (WS 5)", "#ws-05"),
        ("gate4", "Gate 4: Execute & Defend (WS 6–8)", "#ws-06"),
        ("gate5", "Gate 5: Retain & Scale (WS 9–10)", "#ws-09"),
        ("ceo", "12-Week CEO Tracker", "#ceo-tracker"),
        ("vault", "50-Prompt Quick Vault", "#prompt-vault"),
    ]
    pills = []
    for key, label, href in tabs:
        cls = "pill-tab active" if key == active_tab else "pill-tab"
        pills.append(f'<a href="{href}" class="{cls}">{html.escape(label)}</a>')
    return f'<div class="planner-navbar">{"".join(pills)}</div>'


def build_tablet_planner_html() -> str:
    """
    Assemble Deliverable 6: Landscape 11in x 8.5in Hyperlinked Tablet Digital Planner
    (iPad GoodNotes / Notability / reMarkable Edition) with persistent top pill navigation bar.
    """
    css = get_book_css("tablet_landscape")

    # 1. Home Dashboard (#planner-home)
    ws_grid_rows = []
    for n in range(1, 11):
        ws_id = f"#ws-{n:02d}"
        gate_badge = {
            1: "Gate 1: Attract",
            2: "Gate 1: Attract",
            3: "Gate 2: Scope & Price",
            4: "Gate 2: Scope & Price",
            5: "Gate 3: Onboard",
            6: "Gate 4: Execute & Defend",
            7: "Gate 4: Execute & Defend",
            8: "Gate 4: Execute & Defend",
            9: "Gate 5: Retain & Scale",
            10: "Gate 5: Retain & Scale",
        }[n]
        ws_grid_rows.append(
            f"<tr>"
            f"<td><strong><a href='{ws_id}'>Worksheet {n:02d}</a></strong></td>"
            f"<td><code>{gate_badge}</code></td>"
            f"<td><a href='{ws_id}'>{html.escape(WORKSHEET_TITLES[n].split(': ', 1)[1])}</a></td>"
            f"<td><a href='#prompt-vault'>Prompts {n}.1–{n}.5</a></td>"
            f"<td><code>☐ Q1  ☐ Q2  ☐ Q3  ☐ Q4</code></td>"
            f"</tr>"
        )

    home_html = f"""
<section id="planner-home">
  {render_planner_navbar("home")}
  <div class="cover-banner" style="padding:18px 22px; margin-bottom:12px;">
    <div class="cover-badge">Hyperlinked Landscape Tablet Planner (11" × 8.5" • GoodNotes / Notability / reMarkable)</div>
    <h1 class="cover-title" style="font-size:20pt;">The AI Freelancer Operating System — Executive Digital Planner</h1>
    <div class="cover-subtitle" style="font-size:10pt; margin-bottom:6px;">
      Tap any pill tab in the top navigation bar or any worksheet link below to jump across the 5 Lifecycle Gates, 10 Action Workbooks, 12-Week CEO Scorecard, and 50-Prompt Quick Vault.
    </div>
  </div>
  <table>
    <thead>
      <tr>
        <th style="width:13%;">Quick Link</th>
        <th style="width:18%;">Lifecycle Gate</th>
        <th style="width:41%;">Interactive Tablet Worksheet Title</th>
        <th style="width:14%;">AI Workflows</th>
        <th style="width:14%;">Quarterly Audit</th>
      </tr>
    </thead>
    <tbody>
      {''.join(ws_grid_rows)}
    </tbody>
  </table>
</section>
"""

    # 2. All 10 Worksheets with top pill navbar
    ws_blocks = []
    for n in range(1, 11):
        active_key = {
            1: "gate1",
            2: "gate1",
            3: "gate2",
            4: "gate2",
            5: "gate3",
            6: "gate4",
            7: "gate4",
            8: "gate4",
            9: "gate5",
            10: "gate5",
        }[n]
        ws_md = (BASE_DIR / "05-WORKBOOKS" / f"worksheet-{n:02d}.md").read_text(encoding="utf-8")
        ws_html = md_to_html(ws_md, inline_svg=True)
        sub_links = (
            f'<div style="font-size:8.2pt; margin-bottom:8px; color:#475569;">'
            f'<strong>Direct Worksheet Jump:</strong> '
            + " • ".join(f'<a href="#ws-{i:02d}">WS {i:02d}</a>' for i in range(1, 11))
            + "</div>"
        )
        ws_blocks.append(
            f'<section id="ws-{n:02d}" class="chapter-section">\n'
            f"{render_planner_navbar(active_key)}\n"
            f"{sub_links}\n"
            f"{ws_html}\n"
            f"</section>"
        )

    # 3. Dedicated 12-Week Friday CEO Scorecard & EHR Log (#ceo-tracker)
    ceo_rows = []
    for wk in range(1, 13):
        ceo_rows.append(
            f"<tr>"
            f"<td><strong>Week {wk:02d}</strong></td>"
            f"<td><code>____/____/26</code></td>"
            f"<td><code>$__________</code></td>"
            f"<td><code>_____ hrs</code></td>"
            f"<td><code>_____ hrs</code></td>"
            f"<td><code>$______ / hr</code></td>"
            f"<td><code>____ / +$______</code></td>"
            f"<td><code>☐ Yes  ☐ No</code></td>"
            f"<td><code>__________________________</code></td>"
            f"</tr>"
        )

    ceo_tracker_html = f"""
<section id="ceo-tracker" class="chapter-section">
  {render_planner_navbar("ceo")}
  <h1>12-Week Friday CEO Scorecard &amp; Effective Hourly Rate (EHR) Log</h1>
  <p>
    Complete one row every Friday at 3:00 PM during your <strong>20-Minute CEO Operating Cadence</strong> (paired with <a href="#ws-10">Worksheet 10.1</a> and <code>Prompt 10.1</code>). Track your realized Effective Hourly Rate (`Gross Weekly Revenue ÷ Total Real Working Hours`) across a full 90-day operating quarter.
  </p>
  <table>
    <thead>
      <tr>
        <th style="width:8%;">Week</th>
        <th style="width:10%;">Friday Date</th>
        <th style="width:12%;">Gross Revenue</th>
        <th style="width:10%;">Bucket A Hrs</th>
        <th style="width:10%;">Total Real Hrs</th>
        <th style="width:12%;">Realized EHR</th>
        <th style="width:13%;">Change Orders</th>
        <th style="width:10%;">Retainer Pitch</th>
        <th style="width:15%;">Top System Constraint Fixed</th>
      </tr>
    </thead>
    <tbody>
      {''.join(ceo_rows)}
    </tbody>
  </table>
</section>
"""

    # 4. Hyperlinked 50-Prompt Quick-Reference Index (#prompt-vault) extracted from back-matter.md
    bm_md = (BASE_DIR / "03-MANUSCRIPT/Back-Matter/back-matter.md").read_text(encoding="utf-8")
    # Extract Section 1 from back-matter.md
    sec1_match = re.search(
        r"(## Section 1: Master Index of All 50 Tested AI Workflows.*?)(?=\n## Section 2:)",
        bm_md,
        flags=re.DOTALL,
    )
    sec1_md = sec1_match.group(1) if sec1_match else bm_md
    vault_html = md_to_html(sec1_md, inline_svg=True)

    prompt_vault_section = f"""
<section id="prompt-vault" class="chapter-section">
  {render_planner_navbar("vault")}
  <h1>50-Prompt Quick-Reference Vault &amp; Worksheet Cross-Index</h1>
  {vault_html}
</section>
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>The AI Freelancer Operating System — Hyperlinked Tablet Digital Planner</title>
  <style>{css}</style>
</head>
<body>
  {home_html}
  {''.join(ws_blocks)}
  {ceo_tracker_html}
  {prompt_vault_section}
</body>
</html>
"""


def build_tier0_lead_magnet_html(config: dict) -> str:
    """
    Assemble Deliverable 7A: Tier-0 Free Lead-Magnet Sample Bundle PDF
    (Complete Front Matter + Master TOC + Full Chapter 1 with inline Mindmap 1.1 & Flowchart 1.2 +
    Complete Worksheet 1.1 + Upgrade Callout to Tier 2 & Tier 3 Complete Operating System).
    """
    css = get_book_css("digital_letter")
    cover_html = build_cover_html(config, "Tier 0 — The Freelancer Leak Audit Kit (Free Sample Edition)")
    fm_md = (BASE_DIR / "03-MANUSCRIPT/Front-Matter/front-matter.md").read_text(encoding="utf-8")
    toc_md = (BASE_DIR / "03-MANUSCRIPT/Front-Matter/toc.md").read_text(encoding="utf-8")
    ch1_md = (BASE_DIR / "03-MANUSCRIPT/Chapters/chapter-01.md").read_text(encoding="utf-8")
    ws1_md = (BASE_DIR / "05-WORKBOOKS/worksheet-01.md").read_text(encoding="utf-8")

    upgrade_callout_html = """
<section id="tier-upgrade-callout" class="chapter-section">
  <div class="cover-banner">
    <div class="cover-badge">Next Step: Install All 5 Stages Across Your Practice</div>
    <h1 class="cover-title" style="font-size:20pt;">Ready to Install Chapters 2–10, All 50 AI Prompts &amp; The Interactive Web Companion App?</h1>
    <div class="cover-subtitle" style="font-size:10.5pt;">
      You have just audited your Effective Hourly Rate (EHR) and installed Stage 01 with Chapter 1 and Worksheet 1.1. Choose your complete operating edition below to install the remaining 45 AI workflows, 18 vector diagrams, 9 action workbooks, 5-Database Notion OS, and the Offline/Online Web Companion App.
    </div>
  </div>
  <table>
    <thead>
      <tr>
        <th style="width:22%;">Commercial Tier</th>
        <th style="width:14%;">Investment</th>
        <th style="width:64%;">Included Operational Deliverables</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Tier 1: Essential Edition</strong><br/><em>(KDP &amp; Draft2Digital)</em></td>
        <td><strong>$9.99 eBook</strong><br/><em>$16.99 Print</em></td>
        <td>Complete 10-Chapter Practical Operating Manual (PDF, Reflowable EPUB 3.0, Print Paperback), all 50 Tested AI Workflow Prompts, 20 Vector Architecture Diagrams, and Back-Matter Emergency Script Vault.</td>
      </tr>
      <tr>
        <td><strong>Tier 2: Interactive Workbook Edition</strong><br/><em>(Gumroad Direct)</em></td>
        <td><strong>$24.00</strong><br/><em>One-Time</em></td>
        <td>Everything in Tier 1 + Complete 10-Chapter Printable &amp; Fillable Action Workbooks (US Letter &amp; ISO A4 Editions) + Hyperlinked Landscape Tablet Digital Planner (iPad GoodNotes / Notability / reMarkable).</td>
      </tr>
      <tr>
        <td><strong>Tier 3: Complete Freelancer OS</strong><br/><em>(Flagship Bundle)</em></td>
        <td><strong>$49.00</strong><br/><em>One-Time</em></td>
        <td>Everything in Tiers 1 &amp; 2 + Full Pro Interactive Web Companion App (<code>freelancer-os-app.html</code> with B.C.R. Pricing Calculator, Dynamic 50-Prompt Builder &amp; Weekly CEO Scorecard) + 5-Database Minimalist Notion OS + Editable Pricing &amp; Onboarding Spreadsheets.</td>
      </tr>
    </tbody>
  </table>
</section>
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>The AI Freelancer Operating System — Tier 0 Free Sample &amp; 7-Day Leak Audit Kit</title>
  <style>{css}</style>
</head>
<body>
  {cover_html}
  <section id="front-matter" class="chapter-section">{md_to_html(fm_md, inline_svg=True)}</section>
  <section id="toc-section" class="chapter-section">{md_to_html(toc_md, inline_svg=True)}</section>
  <section id="chapter-01" class="chapter-section">{md_to_html(ch1_md, inline_svg=True)}</section>
  <section id="ws-01" class="chapter-section">{md_to_html(ws1_md, inline_svg=True)}</section>
  {upgrade_callout_html}
</body>
</html>
"""


def build_chapter01_standalone_workbook_html() -> str:
    """Assemble Deliverable 7B: Standalone Printable & Fillable Chapter 1 Worksheet 1.1 PDF."""
    css = get_book_css("workbook_letter")
    ws1_md = (BASE_DIR / "05-WORKBOOKS/worksheet-01.md").read_text(encoding="utf-8")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Worksheet 1.1: The 7-Day Time &amp; Revenue Leak Audit</title>
  <style>{css}</style>
</head>
<body>
  <section id="ws-01">
    {md_to_html(ws1_md, inline_svg=True)}
  </section>
</body>
</html>
"""


def main() -> int:
    print("=" * 78)
    print("THE AI FREELANCER OPERATING SYSTEM — SINGLE-SOURCE COMPILER (build.py)")
    print("=" * 78)

    browser_exe = find_headless_browser()
    print(f"[Engine] Headless Chromium Browser: {browser_exe}")

    config_path = BASE_DIR / "book-config.yaml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    # Ensure output directories exist
    (BASE_DIR / "09-EXPORTS/PDF").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "09-EXPORTS/PRINT").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "09-EXPORTS/EPUB").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "05-WORKBOOKS").mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------
    # Deliverable 1: Full Digital Book Edition PDF (US Letter 8.5in x 11in)
    # -------------------------------------------------------------------------
    d1_path = BASE_DIR / "09-EXPORTS/PDF/the-ai-freelancer-os-complete-book.pdf"
    print(f"[1/7] Compiling Full Digital Book PDF -> {d1_path.relative_to(BASE_DIR)} ...")
    d1_html = build_full_book_html(
        config,
        mode="digital_letter",
        edition_label="First Commercial Hybrid Edition • Complete Digital Operating Manual",
    )
    render_html_to_pdf(browser_exe, d1_html, d1_path)
    d1_pages = stamp_pdf_metadata(
        d1_path,
        title="The AI Freelancer Operating System — Complete Digital Edition",
        subject="A Practical System to Organize Clients, Automate Repetitive Work, Manage Projects, and Build a More Productive Freelance Business",
        keywords="freelance business management system, ai workflow automation, scope creep defense, productized services",
    )
    print(f"      -> Done ({d1_pages} pages, {d1_path.stat().st_size / 1024:.1f} KB)")

    # -------------------------------------------------------------------------
    # Deliverable 2: Amazon KDP 6" x 9" Print-Ready Paperback Interior PDF
    # -------------------------------------------------------------------------
    d2_path = BASE_DIR / "09-EXPORTS/PRINT/the-ai-freelancer-os-kdp-paperback-6x9.pdf"
    print(f"[2/7] Compiling Amazon KDP 6\"x9\" Print Paperback PDF -> {d2_path.relative_to(BASE_DIR)} ...")
    d2_html = build_full_book_html(
        config,
        mode="kdp_6x9",
        edition_label="Amazon KDP Print Paperback Edition (6.0\" × 9.0\" Trim)",
    )
    render_html_to_pdf(browser_exe, d2_html, d2_path)
    d2_pages = stamp_pdf_metadata(
        d2_path,
        title="The AI Freelancer Operating System — KDP 6x9 Print Interior",
        subject="Amazon KDP 6x9 Print-Ready Paperback Interior (No Bleed, High-Contrast Monochrome)",
        keywords="freelance operating system, kdp 6x9 interior, consulting pricing, client onboarding",
    )
    print(f"      -> Done ({d2_pages} pages, {d2_path.stat().st_size / 1024:.1f} KB)")

    # -------------------------------------------------------------------------
    # Deliverable 3: Standards-Compliant Reflowable EPUB 3.0 eBook
    # -------------------------------------------------------------------------
    d3_path = BASE_DIR / "09-EXPORTS/EPUB/the-ai-freelancer-os.epub"
    print(f"[3/7] Compiling Reflowable EPUB 3.0 eBook -> {d3_path.relative_to(BASE_DIR)} ...")
    epub_info = build_epub_3(config, d3_path)
    print(
        f"      -> Done ({epub_info['xhtml_count']} XHTML spine docs, "
        f"{epub_info['svg_count']} SVGs, {epub_info['file_size_bytes'] / 1024:.1f} KB)"
    )

    # -------------------------------------------------------------------------
    # Deliverable 4: 10-Chapter Printable & Fillable Workbook (US Letter)
    # -------------------------------------------------------------------------
    d4_export_path = BASE_DIR / "09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-us-letter.pdf"
    d4_wb_copy = BASE_DIR / "05-WORKBOOKS/the-ai-freelancer-os-workbook-us-letter.pdf"
    print(f"[4/7] Compiling 10-Chapter Workbook (US Letter) -> {d4_export_path.relative_to(BASE_DIR)} ...")
    d4_html = build_workbook_html(
        mode="workbook_letter",
        edition_label="US Letter (8.5\" × 11.0\") Printable & Fillable Action Workbook",
    )
    render_html_to_pdf(browser_exe, d4_html, d4_export_path)
    d4_pages = stamp_pdf_metadata(
        d4_export_path,
        title="The AI Freelancer Operating System — 10-Chapter Action Workbook (US Letter)",
        subject="10-Chapter Printable and Interactive Fillable Action Workbook (US Letter 8.5x11)",
        keywords="freelance workbook, ehr leak audit, bcr pricing worksheet, scope creep log",
        init_acroform=True,
    )
    shutil.copy2(d4_export_path, d4_wb_copy)
    print(f"      -> Done ({d4_pages} pages, {d4_export_path.stat().st_size / 1024:.1f} KB + synced to 05-WORKBOOKS/)")

    # -------------------------------------------------------------------------
    # Deliverable 5: 10-Chapter Printable & Fillable Workbook (ISO A4)
    # -------------------------------------------------------------------------
    d5_export_path = BASE_DIR / "09-EXPORTS/PRINT/the-ai-freelancer-os-workbook-a4.pdf"
    d5_wb_copy = BASE_DIR / "05-WORKBOOKS/the-ai-freelancer-os-workbook-a4.pdf"
    print(f"[5/7] Compiling 10-Chapter Workbook (ISO A4) -> {d5_export_path.relative_to(BASE_DIR)} ...")
    d5_html = build_workbook_html(
        mode="workbook_a4",
        edition_label="ISO A4 (210mm × 297mm) International Printable & Fillable Action Workbook",
    )
    render_html_to_pdf(browser_exe, d5_html, d5_export_path)
    d5_pages = stamp_pdf_metadata(
        d5_export_path,
        title="The AI Freelancer Operating System — 10-Chapter Action Workbook (ISO A4)",
        subject="10-Chapter Printable and Interactive Fillable Action Workbook (ISO A4 210x297mm)",
        keywords="freelance workbook a4, uk au ca freelancer system, action worksheets",
        init_acroform=True,
    )
    shutil.copy2(d5_export_path, d5_wb_copy)
    print(f"      -> Done ({d5_pages} pages, {d5_export_path.stat().st_size / 1024:.1f} KB + synced to 05-WORKBOOKS/)")

    # -------------------------------------------------------------------------
    # Deliverable 6: Hyperlinked Tablet Digital Planner (Landscape 11in x 8.5in)
    # -------------------------------------------------------------------------
    d6_export_path = BASE_DIR / "09-EXPORTS/PDF/the-ai-freelancer-os-tablet-planner.pdf"
    d6_wb_copy = BASE_DIR / "05-WORKBOOKS/the-ai-freelancer-os-tablet-planner.pdf"
    print(f"[6/7] Compiling Hyperlinked Tablet Digital Planner -> {d6_export_path.relative_to(BASE_DIR)} ...")
    d6_html = build_tablet_planner_html()
    render_html_to_pdf(browser_exe, d6_html, d6_export_path)
    d6_pages = stamp_pdf_metadata(
        d6_export_path,
        title="The AI Freelancer Operating System — Hyperlinked Tablet Digital Planner",
        subject="Landscape 11x8.5 Hyperlinked Tablet Planner for iPad GoodNotes, Notability, and reMarkable",
        keywords="digital planner, goodnotes freelancer planner, remarkable workbook, hyperlinked pdf",
        init_acroform=True,
    )
    shutil.copy2(d6_export_path, d6_wb_copy)
    print(f"      -> Done ({d6_pages} pages, {d6_export_path.stat().st_size / 1024:.1f} KB + synced to 05-WORKBOOKS/)")

    # -------------------------------------------------------------------------
    # Deliverable 7: Tier-0 Free Lead-Magnet Sample Bundle PDF + Ch 1 Workbook PDF
    # -------------------------------------------------------------------------
    d7a_path = BASE_DIR / "09-EXPORTS/PDF/tier0-free-sample-chapter01-and-audit.pdf"
    d7b_wb_path = BASE_DIR / "05-WORKBOOKS/chapter-01-workbook.pdf"
    d7b_export_path = BASE_DIR / "09-EXPORTS/PRINT/chapter-01-workbook.pdf"
    print(f"[7/7] Compiling Tier-0 Lead Magnet PDF & Standalone Ch1 Workbook -> {d7a_path.relative_to(BASE_DIR)} ...")
    d7a_html = build_tier0_lead_magnet_html(config)
    render_html_to_pdf(browser_exe, d7a_html, d7a_path)
    d7a_pages = stamp_pdf_metadata(
        d7a_path,
        title="The AI Freelancer Operating System — Tier 0 Free Sample & 7-Day Leak Audit Kit",
        subject="Sample Chapter 1 + 7-Day Time & Revenue Leak Audit Worksheet 1.1",
        keywords="free freelancer audit, effective hourly rate calculator, chapter 1 sample",
    )

    d7b_html = build_chapter01_standalone_workbook_html()
    render_html_to_pdf(browser_exe, d7b_html, d7b_wb_path)
    d7b_pages = stamp_pdf_metadata(
        d7b_wb_path,
        title="Worksheet 1.1: The 7-Day Time & Revenue Leak Audit",
        subject="Standalone Printable & Fillable Chapter 1 Worksheet 1.1",
        keywords="worksheet 1.1, 7-day time leak audit, effective hourly rate",
        init_acroform=True,
    )
    shutil.copy2(d7b_wb_path, d7b_export_path)
    print(
        f"      -> Done (Tier-0 Sample: {d7a_pages} pages, {d7a_path.stat().st_size / 1024:.1f} KB | "
        f"Ch1 Workbook: {d7b_pages} pages, {d7b_wb_path.stat().st_size / 1024:.1f} KB)"
    )

    print("=" * 78)
    print("ALL 7 COMMERCIAL DELIVERABLES COMPILED SUCCESSFULLY.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
