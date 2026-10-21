#!/usr/bin/env python3
"""Export the workshop presentation content to a 16:9 PDF slide deck."""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from build_slides import SLIDES


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "apresentacao.pdf"
PAGE_W, PAGE_H = 960, 540

NAVY = HexColor("#0B1220")
PANEL = HexColor("#131F32")
PANEL_ALT = HexColor("#17283E")
WHITE = HexColor("#F4F8FC")
MUTED = HexColor("#A8B8CA")
TEAL = HexColor("#3ADCC2")
BLUE = HexColor("#5FA3FF")
GOLD = HexColor("#FFC55B")
FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"


def inch(value):
    return value * 72


def paragraph(canvas, text, x, top, width, height, size, color, bold=False, align=TA_LEFT):
    style = ParagraphStyle(
        name=f"slide-{size}-{bold}-{align}",
        fontName=FONT_BOLD if bold else FONT,
        fontSize=size,
        leading=size * 1.24,
        textColor=color,
        alignment=align,
        spaceAfter=0,
        spaceBefore=0,
        allowWidows=0,
        allowOrphans=0,
    )
    para = Paragraph(text, style)
    _, actual_height = para.wrap(width, height)
    para.drawOn(canvas, x, PAGE_H - top - actual_height)


def panel(canvas, x, top, width, height, fill=PANEL, radius=12):
    canvas.setFillColor(fill)
    canvas.roundRect(x, PAGE_H - top - height, width, height, radius, fill=1, stroke=0)


def base(canvas, index, time):
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0, 9, PAGE_H, fill=1, stroke=0)
    paragraph(
        canvas,
        f"OPENTOFU  /  FUNDAMENTOS DE IaC",
        40,
        512,
        500,
        18,
        8.5,
        MUTED,
        bold=True,
    )
    right = f"{time.upper()}  •  {index:02d}/{len(SLIDES):02d}"
    canvas.setFont(FONT_BOLD, 8.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(PAGE_W - 42, 16, right)


def header(canvas, title, kicker):
    paragraph(canvas, kicker, 52, 29, 850, 18, 10, TEAL, bold=True)
    paragraph(canvas, title, 52, 58, 850, 46, 27, WHITE, bold=True)


def item_cards(canvas, items):
    if len(items) == 4:
        positions = [(54, 145), (493, 145), (54, 292), (493, 292)]
        card_w, card_h = 412, 124
    else:
        positions = [(54, 145 + i * 107) for i in range(len(items))]
        card_w, card_h = 852, 88
    for i, ((label, body), (x, top)) in enumerate(zip(items, positions)):
        panel(canvas, x, top, card_w, card_h, PANEL if i % 2 == 0 else PANEL_ALT)
        paragraph(canvas, label, x + 20, top + 16, card_w - 40, 26, 15, TEAL, bold=True)
        paragraph(canvas, body, x + 20, top + 47, card_w - 40, card_h - 56, 13.2, WHITE)


def timeline(canvas, items):
    y = 224
    canvas.setFillColor(BLUE)
    canvas.rect(110, PAGE_H - y - 3, 720, 3, fill=1, stroke=0)
    for i, (label, body) in enumerate(items):
        x = 66 + i * 274
        canvas.setFillColor(TEAL if i != 1 else GOLD)
        canvas.circle(x + 127, PAGE_H - y, 13, fill=1, stroke=0)
        panel(canvas, x, 270, 242, 126, PANEL if i != 1 else PANEL_ALT)
        paragraph(canvas, label, x + 16, 286, 210, 24, 14, TEAL, bold=True)
        paragraph(canvas, body, x + 16, 318, 210, 65, 11.8, WHITE)


def flow(canvas, items):
    for i, (label, body) in enumerate(items):
        x = 58 + i * 296
        panel(canvas, x, 194, 256, 162, PANEL if i % 2 == 0 else PANEL_ALT)
        paragraph(canvas, f"0{i + 1}", x + 17, 210, 44, 24, 16, GOLD, bold=True)
        paragraph(canvas, label, x + 17, 247, 224, 27, 15.2, TEAL, bold=True)
        paragraph(canvas, body, x + 17, 286, 224, 58, 12.4, WHITE)
        if i < len(items) - 1:
            paragraph(canvas, "→", x + 260, 253, 30, 30, 22, TEAL, bold=True, align=TA_CENTER)


def questions(canvas, items):
    for i, text in enumerate(items):
        top = 138 + i * 64
        panel(canvas, 59, top, 838, 49, PANEL if i % 2 == 0 else PANEL_ALT, radius=8)
        paragraph(canvas, f"{i + 1:02d}", 78, top + 13, 38, 21, 12, TEAL, bold=True)
        paragraph(canvas, text, 126, top + 12, 748, 27, 13.5, WHITE)


def cover(canvas, content):
    paragraph(canvas, content["kicker"], 62, 61, 840, 25, 12, TEAL, bold=True)
    paragraph(canvas, content["title"], 62, 111, 840, 66, 33, WHITE, bold=True)
    paragraph(
        canvas,
        "Da história do fork ao primeiro plano declarativo",
        64,
        205,
        800,
        32,
        17,
        MUTED,
    )
    for i, (label, body) in enumerate(content["items"]):
        x = 63 + i * 294
        panel(canvas, x, 298, 261, 112, PANEL if i != 1 else PANEL_ALT)
        paragraph(canvas, label, x + 16, 317, 229, 25, 14, TEAL, bold=True)
        paragraph(canvas, body, x + 16, 350, 229, 49, 11.5, WHITE)


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas = Canvas(str(OUTPUT), pagesize=landscape((PAGE_W, PAGE_H)), pageCompression=1)
    canvas.setTitle("OpenTofu e fundamentos de IaC")
    canvas.setAuthor("Minicurso OpenTofu com Floci")
    canvas.setSubject("Apresentação introdutória de 30 minutos")
    canvas.setKeywords("OpenTofu, IaC, Terraform, Floci")

    for index, content in enumerate(SLIDES, start=1):
        base(canvas, index, content["time"])
        if content.get("kind") == "cover":
            cover(canvas, content)
        else:
            header(canvas, content["title"], content["kicker"])
            kind = content.get("kind")
            if kind == "timeline":
                timeline(canvas, content["items"])
            elif kind == "flow":
                flow(canvas, content["items"])
            elif kind == "questions":
                questions(canvas, content["items"])
            else:
                item_cards(canvas, content["items"])
        canvas.showPage()

    canvas.save()
    print(f"Generated {OUTPUT} ({len(SLIDES)} pages)")


if __name__ == "__main__":
    build()
