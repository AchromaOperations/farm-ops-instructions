"""Delivery list PDF for one delivery day.

Run by the Operator routine in its cloud sandbox (never needs anything local):
    pip install reportlab
    python tools/delivery_list_pdf.py day.json out.pdf

day.json is written by the routine from the sheets (see instructions/daily-delivery-list.md).
All counting, flags and layout happen here, so every list looks the same and adds up the same.

Input (JSON):
{
  "farm": "Restoration Farmstead",
  "day": "Monday", "date": "2026-10-12",
  "route": "", "driver": "",
  "locked_at": "Sun Oct 11, 7:40pm",
  "products": [{"column": "Milk (gal)", "unit": "gal"}, {"column": "Eggs", "unit": "dozen"}, ...],  # Products order
  "rows": [{"cust_id": "C001", "name": "...", "stop": "1", "address": "...", "city": "...",
            "delivery_notes": "...", "needs_attention": "...", "changes": "...",
            "standing_milk": 1, "quantities": {"Milk (gal)": 1, "Eggs": 2}}, ...],
  "pending": [{"customer": "...", "asked_for": "..."}]
}
"""
import json
import sys
from datetime import datetime
from urllib.parse import quote_plus

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (Flowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

INK = colors.HexColor("#1A1A1A")
MUTED = colors.HexColor("#5A5A5A")
RULE = colors.HexColor("#BDBDBD")
ZEBRA = colors.HexColor("#F3F3F3")
SKIPFILL = colors.HexColor("#E2E2E2")
ACCENT = colors.HexColor("#0072B2")  # Okabe-Ito blue: decoration only, never the only signal
WHITE = colors.white
SYNC = "(standing order sync)"
MILK = "Milk (gal)"
EXTRA = "Extra Milk"


def style(name, size, bold=False, color=INK, leading=None, align=0, italic=False):
    font = "Helvetica-Bold" if bold else ("Helvetica-Oblique" if italic else "Helvetica")
    return ParagraphStyle(name, fontName=font, fontSize=size, textColor=color,
                          leading=leading or size * 1.22, alignment=align)


S = {
    "day": style("day", 26, True, WHITE, 28),
    "sub": style("sub", 10.5, False, WHITE),
    "farm": style("farm", 10.5, True, WHITE, align=2),
    "h": style("h", 13, True, INK, 16),
    "cell": style("cell", 9.5),
    "cellb": style("cellb", 10.5, True),
    "small": style("small", 8.5, False, MUTED),
    "tiny": style("tiny", 7.5, False, MUTED),
    "flag": style("flag", 9, True, INK, 11),
    "note": style("note", 9, italic=True),
    "big": style("big", 13, True),
    "stopno": style("stopno", 15, True, align=TA_CENTER),
    "tileno": style("tileno", 22, True, align=TA_CENTER, leading=24),
    "tilelbl": style("tilelbl", 8, True, MUTED, align=TA_CENTER),
    "skiph": style("skiph", 14, True, INK, 17),
    "skip": style("skip", 11, False, INK, 14),
}


def num(x):
    try:
        return float(x or 0)
    except (TypeError, ValueError):
        return 0.0


def fmt(x):
    return str(int(x)) if float(x).is_integer() else str(x)


def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Box(Flowable):
    """An empty tick box to mark packed or delivered by hand."""

    def __init__(self, size=12):
        super().__init__()
        self.size = size
        self.width = self.height = size

    def draw(self):
        self.canv.setStrokeColor(INK)
        self.canv.setLineWidth(1.2)
        self.canv.rect(0, 0, self.size, self.size)


def real_changes(row):
    return [c.strip() for c in (row.get("changes") or "").split(" ; ") if c.strip() and not c.strip().endswith(SYNC)]


def analyse(day):
    products = [p["column"] for p in day["products"]]
    units = {p["column"]: p.get("unit", "") for p in day["products"]}
    stops = []
    for r in day["rows"]:
        q = {k: num(v) for k, v in (r.get("quantities") or {}).items() if num(v)}
        milk, extra = q.get(MILK, 0), q.get(EXTRA, 0)
        addons = [(p, q[p]) for p in products if p not in (MILK, EXTRA) and q.get(p)]
        skip = not q
        no_milk = (not skip) and milk == 0 and num(r.get("standing_milk")) > 0
        flags = []
        if skip:
            flags.append("SKIP")
        if no_milk:
            flags.append("NO MILK")
        attn = (r.get("needs_attention") or "").strip()
        if attn.upper().startswith("GUESS"):
            flags.append("GUESS")
        if real_changes(r):
            flags.append("CHANGED")
        if (attn and not attn.upper().startswith("GUESS")) or not str(r.get("stop") or "").strip() \
                or (milk and not (milk * 2).is_integer()):
            flags.append("!")
        stops.append(dict(r, q=q, milk=milk, extra=extra, addons=addons, skip=skip, no_milk=no_milk,
                          flags=flags, jars=milk * 2))
    stops.sort(key=lambda s: (num(s.get("stop")) or 9999, s.get("name", "")))
    totals = {}
    for s in stops:
        for p, v in s["q"].items():
            totals[p] = totals.get(p, 0) + v
    return products, units, stops, totals


def header(day, stops):
    d = datetime.strptime(day["date"], "%Y-%m-%d")
    title = f"{day['day'].upper()} &middot; {d.strftime('%b')} {d.day}, {d.year}"
    route = day.get("route") or f"All {day['day']} stops"
    driver = day.get("driver") or "____________"
    sub = f"{esc(route)} &middot; Driver: {esc(driver)} &middot; Locked {esc(day.get('locked_at', ''))}"
    t = Table([[Paragraph(title, S["day"]), Paragraph(esc(day.get("farm", "")), S["farm"])],
               [Paragraph(sub, S["sub"]), ""]],
              colWidths=[5.6 * inch, 1.9 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT), ("SPAN", (0, 1), (1, 1)),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, 0), 10), ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def tiles(stops, totals):
    deliver = sum(1 for s in stops if not s["skip"])
    skipping = sum(1 for s in stops if s["skip"])
    jars = totals.get(MILK, 0) * 2 + totals.get(EXTRA, 0)
    addon_items = sum(v for p, v in totals.items() if p not in (MILK, EXTRA))
    cells = [[Paragraph(fmt(n), S["tileno"]) for n in (deliver, skipping, jars, addon_items)],
             [Paragraph(l, S["tilelbl"]) for l in ("STOPS TO DELIVER", "SKIPPING", "MILK JARS", "ADD-ON ITEMS")]]
    t = Table(cells, colWidths=[1.875 * inch] * 4)
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (0, -1), 1, INK), ("BOX", (1, 0), (1, -1), 1, INK),
        ("BOX", (2, 0), (2, -1), 1, INK), ("BOX", (3, 0), (3, -1), 1, INK),
        ("TOPPADDING", (0, 0), (-1, 0), 6), ("BOTTOMPADDING", (0, -1), (-1, -1), 6),
        ("LINEBEFORE", (1, 0), (-1, -1), 6, WHITE),
    ]))
    return t


def skip_box(stops):
    skips = [s for s in stops if s["skip"]]
    nomilk = [s for s in stops if s["no_milk"]]
    rows = [[Paragraph("X&nbsp;&nbsp;DO NOT DELIVER" if skips else "No skips this week", S["skiph"])]]
    for s in skips:
        rows.append([Paragraph(f"<b>Stop {esc(str(s.get('stop') or '?'))}: {esc(s['name'])}</b>, "
                               f"{esc(s.get('address', ''))}, {esc(s.get('city', ''))}: SKIP, nothing to deliver this week",
                               S["skip"])])
    if nomilk:
        rows.append([Paragraph("NO MILK THIS WEEK (add-ons only)", S["skiph"])])
        for s in nomilk:
            rows.append([Paragraph(f"<b>Stop {esc(str(s.get('stop') or '?'))}: {esc(s['name'])}</b>: NO MILK, add-ons only",
                                   S["skip"])])
    t = Table(rows, colWidths=[7.5 * inch])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 3 if (skips or nomilk) else 1, INK),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, 0), 8),
    ]))
    return t


def packing(products, units, totals):
    rows = [[Paragraph("", S["small"]), Paragraph("<b>ITEM</b>", S["small"]), Paragraph("<b>QTY</b>", S["small"]),
             Paragraph("<b>UNIT</b>", S["small"])]]
    jars = totals.get(MILK, 0) * 2 + totals.get(EXTRA, 0)
    if jars:
        extra = totals.get(EXTRA, 0)
        detail = f"half-gallon jars ({fmt(jars / 2)} gal{', including ' + fmt(extra) + ' extra' if extra else ''})"
        rows.append([Box(), Paragraph("Milk", S["big"]), Paragraph(fmt(jars), S["big"]), Paragraph(detail, S["cell"])])
    for p in products:
        if p in (MILK, EXTRA) or not totals.get(p):
            continue
        rows.append([Box(), Paragraph(esc(p), S["cellb"]), Paragraph(fmt(totals[p]), S["cellb"]),
                     Paragraph(esc(units.get(p, "")), S["cell"])])
    t = Table(rows, colWidths=[0.35 * inch, 2.6 * inch, 0.7 * inch, 3.85 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, ZEBRA]),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def stops_table(stops, units):
    head = [Paragraph(f"<b>{h}</b>", S["tiny"]) for h in ("DONE", "STOP", "CUSTOMER", "DELIVER", "NOTES", "FLAGS")]
    rows, styles = [head], []
    for i, s in enumerate(stops, start=1):
        maps = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(f"{s.get('address', '')}, {s.get('city', '')} KY")
        cust = Paragraph(f"<b>{esc(s['name'])}</b><br/><link href='{maps}' color='#0072B2'><u>"
                         f"{esc(s.get('address', ''))}</u></link>, {esc(s.get('city', ''))}", S["cell"])
        if s["skip"]:
            deliver = Paragraph("<b>SKIP: NO DELIVERY</b>", S["cellb"])
            styles.append(("BACKGROUND", (0, i), (-1, i), SKIPFILL))
        else:
            parts = []
            if s["jars"]:
                parts.append(f"<font size=13><b>{fmt(s['jars'])} jar{'s' if s['jars'] != 1 else ''}</b></font>"
                             + (f" + <b>{fmt(s['extra'])} extra</b>" if s["extra"] else ""))
            elif s["extra"]:
                parts.append(f"<b>{fmt(s['extra'])} extra jar{'s' if s['extra'] != 1 else ''}</b>")
            if s["no_milk"]:
                parts.append("<b>NO MILK</b>")
            parts += [f"{fmt(v)} x {esc(p)}" for p, v in s["addons"]]
            deliver = Paragraph("<br/>".join(parts), S["cell"])
        flags = Paragraph("<br/>".join(s["flags"]), S["flag"])
        rows.append([Box(13), Paragraph(esc(str(s.get("stop") or "?")), S["stopno"]), cust, deliver,
                     Paragraph(esc(s.get("delivery_notes", "")), S["note"]), flags])
    t = Table(rows, colWidths=[0.5 * inch, 0.5 * inch, 2.05 * inch, 1.55 * inch, 1.9 * inch, 1.0 * inch],
              repeatRows=1)
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE), ("LINEBELOW", (0, 0), (-1, 0), 1.2, INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, ZEBRA]),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ] + styles))
    return t


def changes_list(stops):
    out = []
    for s in stops:
        lines = real_changes(s)
        attn = (s.get("needs_attention") or "").strip()
        if lines or attn:
            text = "; ".join(esc(l) for l in lines)
            if attn:
                text += ("; " if text else "") + "<b>" + esc(attn) + "</b>"
            out.append(Paragraph(f"<b>Stop {esc(str(s.get('stop') or '?'))} &middot; {esc(s['name'])}:</b> {text}", S["cell"]))
    return out


def build(day, out_path):
    products, units, stops, totals = analyse(day)
    d = datetime.strptime(day["date"], "%Y-%m-%d")
    made = datetime.now().strftime("%b %d %I:%M%p").replace(" 0", " ")

    def footer(canv, doc):
        canv.saveState()
        canv.setFont("Helvetica", 8)
        canv.setFillColor(MUTED)
        canv.drawString(0.5 * inch, 0.4 * inch,
                        f"{day.get('farm', '')} delivery list - {day['day']} {d.strftime('%b')} {d.day}, {d.year} - made {made}")
        canv.drawRightString(8.0 * inch, 0.4 * inch, f"Page {doc.page}")
        canv.restoreState()

    doc = SimpleDocTemplate(out_path, pagesize=letter, leftMargin=0.5 * inch, rightMargin=0.5 * inch,
                            topMargin=0.5 * inch, bottomMargin=0.65 * inch,
                            title=f"Delivery list {day['day']} {day['date']}", author=day.get("farm", ""))
    story = [header(day, stops), Spacer(1, 10), tiles(stops, totals), Spacer(1, 12),
             KeepTogether([skip_box(stops)]), Spacer(1, 14),
             Paragraph("PACKING LIST", S["h"]), Spacer(1, 4), packing(products, units, totals), Spacer(1, 16),
             Paragraph("STOPS", S["h"]), Spacer(1, 4), stops_table(stops, units)]
    ch = changes_list(stops)
    if ch:
        story += [Spacer(1, 14), Paragraph("CHANGES THIS WEEK", S["h"]), Spacer(1, 4)] + \
                 [x for c in ch for x in (c, Spacer(1, 3))]
    pending = day.get("pending") or []
    if pending:
        story += [Spacer(1, 14), Paragraph("PENDING: NOT PACKED (Mark hasn't decided; don't pack unless he says so)", S["h"]),
                  Spacer(1, 4)] + [Paragraph(f"<b>{esc(p.get('customer', ''))}:</b> {esc(p.get('asked_for', ''))}", S["cell"])
                                   for p in pending]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return {"stops_to_deliver": sum(1 for s in stops if not s["skip"]),
            "skipping": sum(1 for s in stops if s["skip"]),
            "milk_jars": totals.get(MILK, 0) * 2 + totals.get(EXTRA, 0),
            "flags": {s["name"]: s["flags"] for s in stops if s["flags"]}}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python tools/delivery_list_pdf.py day.json out.pdf")
    with open(sys.argv[1]) as f:
        summary = build(json.load(f), sys.argv[2])
    print(json.dumps(summary))
