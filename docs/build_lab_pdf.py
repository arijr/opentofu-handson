#!/usr/bin/env python3
"""Render the lab slide deck as a 16:9 PDF."""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from build_lab_slides import LABS


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "laboratorios.pdf"
PAGE_W, PAGE_H = 960, 540

NAVY = HexColor("#0B1220")
PANEL = HexColor("#131F32")
PANEL_ALT = HexColor("#17283E")
WHITE = HexColor("#F4F8FC")
MUTED = HexColor("#A8B8CA")
TEAL = HexColor("#3ADCC2")
GOLD = HexColor("#FFC55B")
FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_CODE = "Courier"


def paragraph(canvas, text, x, top, width, height, size, color, bold=False, font=FONT):
    style = ParagraphStyle(
        name=f"p-{size}-{bold}-{font}",
        fontName=FONT_BOLD if bold else font,
        fontSize=size,
        leading=size * 1.22,
        textColor=color,
        alignment=TA_LEFT,
        spaceAfter=0,
        spaceBefore=0,
        allowWidows=0,
        allowOrphans=0,
    )
    obj = Paragraph(text, style)
    _, used = obj.wrap(width, height)
    obj.drawOn(canvas, x, PAGE_H - top - used)


def panel(canvas, x, top, width, height, fill=PANEL, radius=10):
    canvas.setFillColor(fill)
    canvas.roundRect(x, PAGE_H - top - height, width, height, radius, fill=1, stroke=0)


def base(canvas, index, label):
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0, 9, PAGE_H, fill=1, stroke=0)
    paragraph(canvas, "MINICURSO OPENTOFU • LABORATÓRIOS", 41, 512, 510, 18, 8.5, MUTED, True)
    canvas.setFont(FONT_BOLD, 8.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(PAGE_W - 42, 16, f"{label.upper()} • {index:02d}/20")


def header(canvas, kicker, title, subtitle):
    paragraph(canvas, kicker, 52, 29, 850, 18, 9.5, TEAL, True)
    paragraph(canvas, title, 52, 57, 850, 38, 24, WHITE, True)
    if subtitle:
        paragraph(canvas, subtitle, 53, 101, 850, 32, 12.2, MUTED)


def cover(canvas):
    paragraph(canvas, "GUIA DO INSTRUTOR E DOS ALUNOS", 62, 70, 840, 24, 11, TEAL, True)
    paragraph(canvas, "Laboratórios OpenTofu + Floci", 62, 126, 840, 54, 32, WHITE, True)
    paragraph(canvas, "Passo a passo visual • 9 labs • 4h de prática em dois encontros", 64, 202, 830, 30, 16, MUTED)
    cards = [
        ("HOJE • 2h", "Labs 01–04<br/>Preparar, criar, parametrizar e inspecionar state."),
        ("AMANHÃ • 2h30", "Labs 05–09<br/>Reutilizar, expressar, consultar, revisar e desafiar."),
        ("AMBIENTE LOCAL", "OpenTofu + AWS Provider<br/>Floci em localhost:4566."),
    ]
    for i, (title, body) in enumerate(cards):
        x = 63 + i * 294
        panel(canvas, x, 292, 261, 106, PANEL if i != 1 else PANEL_ALT)
        paragraph(canvas, title, x + 16, 311, 229, 23, 13.5, TEAL, True)
        paragraph(canvas, body, x + 16, 343, 229, 47, 10.8, WHITE)


def agenda(canvas):
    header(canvas, "MAPA DA SESSÃO", "Do setup à limpeza", "Quatro horas de laboratório, mantendo a prática segura e revisável.")
    rows = [
        ("HOJE • 120 min", "01 Setup 20’   ·   02 Bucket 30’   ·   03 Variables 30’   ·   04 State 40’"),
        ("AMANHÃ • 150 min", "05 Módulos 25’   ·   06 Expressões 30’   ·   07 Data 30’   ·   08 Qualidade 25’   ·   09 Desafio 40’"),
        ("REGRA DE OURO", "Leia todo plan antes de apply/destroy. Use somente localhost:4566."),
    ]
    for i, (label, body) in enumerate(rows):
        top = 173 + i * 83
        panel(canvas, 61, top, 838, 63, PANEL if i != 1 else PANEL_ALT)
        paragraph(canvas, label, 82, top + 15, 166, 22, 12.4, TEAL, True)
        paragraph(canvas, body, 250, top + 15, 626, 32, 11.5, WHITE)


def intro_slide(canvas, index, lab):
    label = f"DIA {lab['day']} • LAB {lab['number']} • {lab['time']} • {lab['slot']}"
    base(canvas, index, lab["day"])
    header(canvas, label, lab["title"], lab["goal"])
    for i, (title, body) in enumerate(lab["ideas"]):
        top = 165 + i * 82
        panel(canvas, 59, top, 524, 63, PANEL if i % 2 == 0 else PANEL_ALT)
        paragraph(canvas, title, 78, top + 14, 125, 20, 12, TEAL, True)
        paragraph(canvas, body, 207, top + 13, 354, 39, 11, WHITE)
    panel(canvas, 605, 165, 294, 227, PANEL_ALT)
    paragraph(canvas, "PERGUNTA-GUIA", 626, 187, 245, 18, 9.5, GOLD, True)
    paragraph(canvas, lab["prompt"], 626, 225, 245, 124, 16, WHITE, True)
    panel(canvas, 59, 426, 840, 45, PANEL)
    paragraph(canvas, f"<b>RESULTADO ESPERADO</b>   {lab['expected']}", 78, 441, 802, 28, 10.5, WHITE)


def run_slide(canvas, index, lab):
    base(canvas, index, lab["day"])
    header(canvas, f"LAB {lab['number']} • EXECUÇÃO • {lab['slot']}", f"Execute em ordem: {lab['title']}", "Terminal na raiz do workshop, salvo indicação em contrário.")
    panel(canvas, 59, 151, 562, 325, PANEL)
    paragraph(canvas, "COMANDOS", 79, 169, 510, 18, 9.5, TEAL, True)
    code = "<br/>".join(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;") for line in lab["commands"].splitlines())
    paragraph(canvas, code, 79, 198, 520, 265, 8.3, WHITE, font=FONT_CODE)
    panel(canvas, 641, 151, 258, 146, PANEL_ALT)
    paragraph(canvas, "VERIFIQUE", 661, 169, 218, 18, 9.5, TEAL, True)
    paragraph(canvas, lab["expected"], 661, 199, 218, 83, 11.8, WHITE, True)
    panel(canvas, 641, 315, 258, 161, PANEL)
    paragraph(canvas, "TRANSIÇÃO", 661, 334, 218, 18, 9.5, GOLD, True)
    paragraph(canvas, lab["transition"], 661, 364, 218, 94, 11.3, WHITE)


def build():
    canvas = Canvas(str(OUTPUT), pagesize=landscape((PAGE_W, PAGE_H)), pageCompression=1)
    canvas.setTitle("Guia de execução dos laboratórios OpenTofu")
    canvas.setAuthor("Minicurso OpenTofu com Floci")
    canvas.setSubject("Nove laboratórios em dois encontros")
    canvas.setKeywords("OpenTofu, Floci, laboratórios, instrutor")
    index = 1
    base(canvas, index, "GUIA DE EXECUÇÃO")
    cover(canvas)
    canvas.showPage()
    index += 1
    base(canvas, index, "AGENDA")
    agenda(canvas)
    canvas.showPage()
    index += 1
    for lab in LABS:
        intro_slide(canvas, index, lab)
        canvas.showPage()
        index += 1
        run_slide(canvas, index, lab)
        canvas.showPage()
        index += 1
    canvas.save()
    print(f"Generated {OUTPUT} ({index - 1} pages)")


if __name__ == "__main__":
    build()
