#!/usr/bin/env python3
"""
Markdown -> professional PDF for company research reports.

Markdown 调研报告 -> 专业 PDF。用 reportlab 内置 CID 字体 STSong-Light，
不依赖系统字体文件，Windows / Linux / macOS 通用（适配本 skill 的多平台目标）。

Supported markdown:
  # / ## / ### / ####    headings
  | a | b |              tables (with --- separator row)
  - x   /   1. x         bullet / ordered lists
  **bold**               inline bold
  > quote                block quote
  ```                    code block (mono)
  blank line             paragraph break

Not supported (per dazhiruoyu's note): pie/line charts. Use tables or prose.

Usage:
  python generate_pdf.py --input report.md --output 报告.pdf
  python generate_pdf.py --input report.md --output 报告.pdf --title "UPG 调研报告"

Dependency:
  pip install reportlab
"""

import argparse
import os
import re
import sys

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        Preformatted,
    )
except ImportError:
    sys.stderr.write(
        "reportlab not installed. Run: pip install reportlab\n"
        "未安装 reportlab，请执行：pip install reportlab\n"
    )
    sys.exit(1)


# CID font shipped with reportlab — no system font file needed, cross-platform.
CN_FONT = "STSong-Light"

# Palette (dazhiruoyu-style professional look).
HEADER_BLUE = colors.HexColor("#1F3A5F")   # table header / H1
SUBTLE_GRAY = colors.HexColor("#4A4A4A")   # H2/H3
ROW_ALT = colors.HexColor("#F2F4F7")       # zebra row
BORDER_GRAY = colors.HexColor("#C8CDD4")
QUOTE_BAR = colors.HexColor("#9AA7B8")
GAP_ORANGE = colors.HexColor("#FFF3E0")    # data-gap banner background
GAP_BORDER = colors.HexColor("#E8A33D")    # data-gap banner border/text


def register_fonts():
    pdfmetrics.registerFont(UnicodeCIDFont(CN_FONT))


def make_styles():
    styles = getSampleStyleSheet()
    base = dict(fontName=CN_FONT)

    styles.add(ParagraphStyle(
        name="CNTitle", parent=styles["Title"],
        fontName=CN_FONT, fontSize=18, alignment=TA_CENTER,
        textColor=HEADER_BLUE, spaceAfter=18, leading=24,
    ))
    styles.add(ParagraphStyle(
        name="H1", fontSize=14, textColor=HEADER_BLUE, spaceBefore=20,
        spaceAfter=8, leading=18, **base,
    ))
    styles.add(ParagraphStyle(
        name="H2", fontSize=12, textColor=SUBTLE_GRAY, spaceBefore=15,
        spaceAfter=6, leading=16, **base,
    ))
    styles.add(ParagraphStyle(
        name="H3", fontSize=11, textColor=SUBTLE_GRAY, spaceBefore=10,
        spaceAfter=5, leading=15, **base,
    ))
    styles.add(ParagraphStyle(
        name="H4", fontSize=10, textColor=SUBTLE_GRAY, spaceBefore=8,
        spaceAfter=4, leading=14, **base,
    ))
    styles.add(ParagraphStyle(
        name="CNBody", fontSize=10, alignment=TA_JUSTIFY, firstLineIndent=20,
        spaceAfter=6, leading=16, **base,
    ))
    styles.add(ParagraphStyle(
        name="CNList", fontSize=10, alignment=TA_LEFT, leftIndent=20,
        spaceAfter=3, leading=16, **base,
    ))
    styles.add(ParagraphStyle(
        name="CNQuote", fontSize=10, alignment=TA_LEFT, leftIndent=16,
        textColor=SUBTLE_GRAY, spaceAfter=6, leading=16, **base,
    ))
    styles.add(ParagraphStyle(
        name="CNGap", fontSize=10, alignment=TA_LEFT, leftIndent=10,
        rightIndent=10, spaceBefore=6, spaceAfter=8, leading=16,
        textColor=GAP_BORDER, backColor=GAP_ORANGE,
        borderColor=GAP_BORDER, borderWidth=1, borderPadding=8, **base,
    ))
    styles.add(ParagraphStyle(
        name="CNCell", fontSize=9, alignment=TA_LEFT, leading=12, **base,
    ))
    styles.add(ParagraphStyle(
        name="CNCellHead", fontSize=9, alignment=TA_LEFT, leading=12,
        textColor=colors.white, fontName=CN_FONT,
    ))
    return styles


def inline_md(text):
    """Convert **bold**, `code`, and ~~strike~~ to reportlab inline tags; escape XML.

    ~~strike~~ renders the data-gap fields struck through (see Data Gap mechanism).
    """
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"~~(.+?)~~", r"<strike>\1</strike>", text)
    text = re.sub(r"`(.+?)`", r'<font face="Courier">\1</font>', text)
    return text


def split_table_row(line):
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def is_separator_row(line):
    cells = split_table_row(line)
    return cells and all(re.fullmatch(r":?-{2,}:?", c or "-") or set(c) <= set("-: ")
                         for c in cells) and any("-" in c for c in cells)


def build_table(rows, styles):
    head, *body = rows
    data = [[Paragraph(inline_md(c), styles["CNCellHead"]) for c in head]]
    for r in body:
        # pad/truncate to header width
        r = (r + [""] * len(head))[:len(head)]
        data.append([Paragraph(inline_md(c), styles["CNCell"]) for c in r])

    table = Table(data, repeatRows=1, hAlign="LEFT")
    ts = [
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BLUE),
        ("FONTNAME", (0, 0), (-1, -1), CN_FONT),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            ts.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    table.setStyle(TableStyle(ts))
    return table


def parse_markdown(md, styles):
    """Return a list of flowables."""
    flow = []
    lines = md.splitlines()
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # code block
        if stripped.startswith("```"):
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            flow.append(Preformatted("\n".join(buf), styles["Code"]))
            flow.append(Spacer(1, 4))
            continue

        # table: current line looks like a row and next line is a separator
        if "|" in line and i + 1 < n and is_separator_row(lines[i + 1]):
            rows = [split_table_row(line)]
            i += 2  # skip header + separator
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(split_table_row(lines[i]))
                i += 1
            flow.append(build_table(rows, styles))
            flow.append(Spacer(1, 8))
            continue

        # headings
        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            text = inline_md(m.group(2))
            style = {1: "H1", 2: "H2", 3: "H3", 4: "H4"}[level]
            flow.append(Paragraph(text, styles[style]))
            i += 1
            continue

        # block quote — a ⚠️-led quote renders as an orange data-gap banner
        if stripped.startswith(">"):
            inner = stripped.lstrip(">").strip()
            text = inline_md(inner)
            style = "CNGap" if inner.startswith("⚠️") else "CNQuote"
            flow.append(Paragraph(text, styles[style]))
            i += 1
            continue

        # bullet / ordered list
        bullet = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", line)
        if bullet:
            mark = "•" if bullet.group(2) in "-*+" else bullet.group(2)
            text = "%s %s" % (mark, inline_md(bullet.group(3)))
            flow.append(Paragraph(text, styles["CNList"]))
            i += 1
            continue

        # blank line
        if not stripped:
            flow.append(Spacer(1, 4))
            i += 1
            continue

        # paragraph
        flow.append(Paragraph(inline_md(stripped), styles["CNBody"]))
        i += 1

    return flow


def main():
    ap = argparse.ArgumentParser(description="Markdown -> professional PDF report")
    ap.add_argument("--input", required=True, help="input markdown path")
    ap.add_argument("--output", required=True, help="output pdf path")
    ap.add_argument("--title", default=None, help="cover title; default = first H1 or filename")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        sys.stderr.write("input not found: %s\n" % args.input)
        sys.exit(1)

    with open(args.input, encoding="utf-8") as f:
        md = f.read()

    register_fonts()
    styles = make_styles()
    # code style uses CJK-safe mono fallback
    styles["Code"].fontName = "Courier"
    styles["Code"].fontSize = 8.5

    flow = []
    title = args.title
    # The first H1 is used as the cover title; strip it from the body so it
    # is not rendered twice.
    m = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
    if title is None:
        title = m.group(1).strip() if m else os.path.splitext(
            os.path.basename(args.input))[0]
    if m:
        md = md[:m.start()] + md[m.end():]
    flow.append(Paragraph(inline_md(title), styles["CNTitle"]))
    flow.append(Spacer(1, 6))
    flow.extend(parse_markdown(md, styles))

    doc = SimpleDocTemplate(
        args.output, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm,
        title=title,
    )
    doc.build(flow)
    print("PDF written: %s" % args.output)


if __name__ == "__main__":
    main()
