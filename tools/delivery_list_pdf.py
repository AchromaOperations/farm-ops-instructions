#!/usr/bin/env python3
"""Delivery list PDF for one delivery day (the approved design: blue header, tiles,
skip box, packing list with tick boxes, stops table with DONE boxes).

Usage: python3 -I delivery_list_pdf.py day.json list.pdf

Standard library only (nothing to install). The routine copies the day's rows into
day.json; this script does all the counting, flags and layout, so every list looks
the same. It also writes [list.pdf].b64, the PDF as one line of base64, ready for Google Drive
create_file's base64Content (instructions/save-pdf.md).
Prints one line of JSON: counts, flags, page count, file name and the text message.

Input: the same form as tools/sample-delivery-day.json, plus optional
"drivers": {"[Route]": "[Driver]"} from the Routes tab. Each row may carry "route"
(the week row's Route); rows with different routes get one section each, each
starting on a new page.
"""
import base64
import json
import os
import re
import sys
import zlib
from datetime import datetime
from urllib.parse import quote_plus

SYNC = "(standing order sync)"
MILK = "Milk (gal)"
EXTRA = "Extra Milk"

# Colors from restorationfarmsteadky.com. Meaning is never carried by color alone (words and shapes do it).
INK = (0.153, 0.012, 0.027)      # site text maroon #270307
MUTED = (0.42, 0.37, 0.36)       # soft brown-gray for labels
RULE = (0.718, 0.725, 0.565)     # site sage #B7B990
ZEBRA = (1.0, 0.973, 0.910)      # site cream #FFF8E8
SKIPFILL = (0.859, 0.863, 0.784) # light sage
ACCENT = (0.0, 0.286, 0.565)     # site navy #004990: links only
BAND = (1.0, 0.973, 0.910)       # cream header band
WHITE = (1.0, 1.0, 1.0)
LOGO_SIZE = 56


def load_logo():
    """The farm logo as a 1-bit image mask (tools/logo-mask.json). None if it's missing."""
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo-mask.json"), encoding="ascii") as f:
            j = json.load(f)
        return int(j["w"]), int(j["h"]), base64.a85decode(j["a85"].encode("ascii").rstrip(b"~>").rstrip())
    except (OSError, ValueError, KeyError):
        return None

PAGE_W, PAGE_H = 612, 792
LEFT, RIGHT, TOP, BOTTOM = 36, 576, 36, 792 - 47
WIDTH = RIGHT - LEFT

# Helvetica (also used for Oblique) and Helvetica-Bold widths (1/1000 em), characters 32-126.
_REG = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278,
        556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556,
        1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
        667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556,
        333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556,
        556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584]
_BOLD = [278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278,
         556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 333, 333, 584, 584, 584, 611,
         975, 722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722, 778,
         667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584, 556,
         333, 556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611,
         611, 611, 389, 556, 333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584]
FONTS = {"r": "F1", "b": "F2", "i": "F3"}


def width(s, size, font="r"):
    table = _BOLD if font == "b" else _REG
    return sum(table[b - 32] if 32 <= b <= 126 else 556 for b in s.encode("cp1252", errors="replace")) * size / 1000.0


def pdf_string(s):
    out = []
    for b in s.encode("cp1252", errors="replace"):
        if b in (0x28, 0x29, 0x5C):
            out.append("\\" + chr(b))
        elif 32 <= b <= 126:
            out.append(chr(b))
        else:
            out.append("\\%03o" % b)
    return "(" + "".join(out) + ")"


def wrap_runs(runs, max_w):
    """runs: list of (text, font, size, color, link). Returns lines of runs, wrapped at spaces."""
    words = []
    for text, font, size, color, link in runs:
        parts = text.split(" ")
        for k, p in enumerate(parts):
            words.append([p, font, size, color, link, k < len(parts) - 1])
    lines, cur, cur_w = [], [], 0.0
    for word, font, size, color, link, space_after in words:
        w = width(word, size, font)
        sp = width(" ", size, font)
        if cur and cur_w + w > max_w:
            lines.append(cur)
            cur, cur_w = [], 0.0
        while w > max_w and len(word) > 1:
            cut = len(word)
            while cut > 1 and width(word[:cut], size, font) > max_w:
                cut -= 1
            lines.append([(word[:cut], font, size, color, link)])
            word = word[cut:]
            w = width(word, size, font)
        cur.append((word + (" " if space_after else ""), font, size, color, link))
        cur_w += w + (sp if space_after else 0)
    if cur:
        lines.append(cur)
    out = []
    for line in lines:
        merged = []
        for r in line:
            if merged and merged[-1][1:] == r[1:]:
                merged[-1] = (merged[-1][0] + r[0],) + r[1:]
            else:
                merged.append(r)
        if merged:
            merged[-1] = (merged[-1][0].rstrip(" "),) + merged[-1][1:]
        out.append(merged)
    return out or [[("", "r", 9.5, INK, None)]]


class Doc:
    def __init__(self, footer_left):
        self.logo = load_logo()
        self.pages = []
        self.page_names = {}
        self.footer_left = footer_left
        self.new_page()

    def new_page(self):
        self.ops, self.annots = [], []
        self.pages.append((self.ops, self.annots))
        self.y = TOP

    def c(self, rgb):
        return "%.3f %.3f %.3f" % rgb

    def rect(self, x, y, w, h, fill=None, stroke=None, lw=1.0):
        if fill:
            self.ops.append("%s rg %.2f %.2f %.2f %.2f re f" % (self.c(fill), x, PAGE_H - y - h, w, h))
        if stroke:
            self.ops.append("%.2f w %s RG %.2f %.2f %.2f %.2f re S" % (lw, self.c(stroke), x, PAGE_H - y - h, w, h))

    def line(self, x1, y1, x2, y2, color=INK, lw=1.0):
        self.ops.append("%.2f w %s RG %.2f %.2f m %.2f %.2f l S" % (lw, self.c(color), x1, PAGE_H - y1, x2, PAGE_H - y2))

    def text(self, x, y, s, size, font="r", color=INK, align="left", link=None):
        w = width(s, size, font)
        if align == "center":
            x -= w / 2
        elif align == "right":
            x -= w
        self.ops.append("BT /%s %.1f Tf %s rg 1 0 0 1 %.2f %.2f Tm %s Tj ET"
                        % (FONTS[font], size, self.c(color), x, PAGE_H - y, pdf_string(s)))
        if link:
            self.line(x, y + 1.5, x + w, y + 1.5, color, 0.6)
            self.annots.append((x, PAGE_H - y - size * 0.25, x + w, PAGE_H - y + size * 0.85, link))
        return w

    def runs_line(self, x, y, runs):
        for text, font, size, color, link in runs:
            x += self.text(x, y, text, size, font, color, link=link)

    def image_logo(self, x, y, size, color):
        if not self.logo:
            return False
        self.ops.append("q %s rg %.2f 0 0 %.2f %.2f %.2f cm /Logo Do Q" % (self.c(color), size, size, x, PAGE_H - y - size))
        return True

    def box(self, x, y, size):
        self.rect(x, y, size, size, stroke=INK, lw=1.2)

    def save(self, path, title):
        n = len(self.pages)
        objs = {}
        # 1 catalog, 2 pages, 3-5 fonts, 6 info, then per page: page, content, link annotations
        objs[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
        objs[3] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
        objs[4] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
        objs[5] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>"
        objs[6] = ("<< /Title %s /Producer (farm-ops delivery_list_pdf.py) >>" % pdf_string(title)).encode("ascii")
        nxt = 7
        xobj = ""
        if self.logo:
            w, h, data = self.logo
            objs[7] = (("<< /Type /XObject /Subtype /Image /Width %d /Height %d /ImageMask true /BitsPerComponent 1 "
                        "/Length %d /Filter /FlateDecode >>\nstream\n" % (w, h, len(data))).encode("ascii")
                       + data + b"\nendstream")
            xobj = " /XObject << /Logo 7 0 R >>"
            nxt = 8
        kids = []
        for k, (ops, annots) in enumerate(self.pages, start=1):
            ops = list(ops)
            ops.append("BT /F1 8.0 Tf %s rg 1 0 0 1 %.2f %.2f Tm %s Tj ET"
                       % (self.c(MUTED), LEFT, 28.8, pdf_string(self.footer_left)))
            pn = "Page %d" % k
            ops.append("BT /F1 8.0 Tf %s rg 1 0 0 1 %.2f %.2f Tm %s Tj ET"
                       % (self.c(MUTED), RIGHT - width(pn, 8), 28.8, pdf_string(pn)))
            raw = "\n".join(ops).encode("ascii")
            content = zlib.compress(raw, 9)
            page_id, content_id = nxt, nxt + 1
            nxt += 2
            annot_ids = []
            for (x1, y1, x2, y2, url) in annots:
                objs[nxt] = ("<</Subtype/Link/Rect[%.0f %.0f %.0f %.0f]/Border[0 0 0]/A<</S/URI/URI%s>>>>"
                             % (x1, y1, x2, y2, pdf_string(url))).encode("ascii")
                annot_ids.append(nxt)
                nxt += 1
            ann = (" /Annots [%s]" % " ".join("%d 0 R" % a for a in annot_ids)) if annot_ids else ""
            objs[page_id] = ("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] /Resources << /Font << /F1 3 0 R "
                             "/F2 4 0 R /F3 5 0 R >>%s >> /Contents %d 0 R%s >>"
                             % (PAGE_W, PAGE_H, xobj, content_id, ann)).encode("ascii")
            objs[content_id] = (b"<< /Length " + str(len(content)).encode("ascii")
                                + b" /Filter /FlateDecode >>\nstream\n" + content + b"\nendstream")
            kids.append(page_id)
        objs[2] = ("<< /Type /Pages /Kids [%s] /Count %d >>" % (" ".join("%d 0 R" % p for p in kids), n)).encode("ascii")
        out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = {}
        for i in range(1, nxt):
            offsets[i] = len(out)
            out += b"%d 0 obj\n" % i + objs[i] + b"\nendobj\n"
        xref = len(out)
        out += b"xref\n0 %d\n0000000000 65535 f \n" % nxt
        for i in range(1, nxt):
            out += b"%010d 00000 n \n" % offsets[i]
        out += b"trailer\n<< /Size %d /Root 1 0 R /Info 6 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (nxt, xref)
        with open(path, "wb") as f:
            f.write(bytes(out))
        with open(path + ".b64", "w", encoding="ascii") as f:
            f.write(base64.b64encode(bytes(out)).decode("ascii"))
        return len(out), n


# ---------- data ----------

def num(x):
    try:
        return float(x or 0)
    except (TypeError, ValueError):
        return 0.0


def fmt(x):
    x = round(float(x), 2)
    return str(int(x)) if x.is_integer() else ("%g" % x)


def phone_text(n):
    m = re.fullmatch(r"\+1(\d{3})(\d{3})(\d{4})", (n or "").strip())
    return ("(%s) %s-%s" % m.groups(), "tel:" + n.strip()) if m else ((n or "").strip(), None)


def real_changes(row):
    return [c.strip() for c in (row.get("changes") or "").split(" ; ") if c.strip() and not c.strip().endswith(SYNC)]


def stop_key(s):
    v = num(s.get("stop"))
    return (0, v, s.get("name", "")) if str(s.get("stop") or "").strip() and v else (1, 0, s.get("name", ""))


def analyse(day):
    products = [p["column"] for p in day["products"]]
    stops = []
    for r in day["rows"]:
        if str(r.get("cust_id", "")).upper().startswith("T"):
            continue
        q, odd = {}, []
        for k, v in (r.get("quantities") or {}).items():
            raw = str(v if v is not None else "").strip()
            if not raw:
                continue
            try:
                val = float(raw)
            except ValueError:
                odd.append('%s "%s" (CHECK: not a number)' % (k, raw))
                continue
            if k not in products:
                if val:
                    odd.append("%s %s (CHECK: not an active product)" % (k, fmt(val)))
                continue
            if val:
                q[k] = val
        milk, extra = q.get(MILK, 0), q.get(EXTRA, 0)
        addons = [(p, q[p]) for p in products if p not in (MILK, EXTRA) and q.get(p)]
        skip = not q and not odd
        no_milk = (not skip) and milk == 0 and num(r.get("standing_milk")) > 0
        attn = (r.get("needs_attention") or "").strip()
        flags = []
        if skip:
            flags.append("SKIP")
        if no_milk:
            flags.append("NO MILK")
        if attn.upper().startswith("GUESS"):
            flags.append("GUESS")
        if real_changes(r):
            flags.append("CHANGED")
        if (attn and not attn.upper().startswith("GUESS")) or not str(r.get("stop") or "").strip() \
                or (milk and not (milk * 2).is_integer()) or odd:
            flags.append("!")
        stops.append(dict(r, q=q, milk=milk, extra=extra, addons=addons, odd=odd, skip=skip, no_milk=no_milk,
                          flags=flags, jars=milk * 2))
    stops.sort(key=stop_key)
    return products, stops


def totals_for(stops):
    t = {}
    for s in stops:
        for p, v in s["q"].items():
            t[p] = t.get(p, 0) + v
    return t


# ---------- drawing ----------

def ensure(d, h):
    if d.y + h > BOTTOM:
        d.new_page()
        return True
    return False


def draw_header(d, day, route):
    dt = datetime.strptime(day["date"], "%Y-%m-%d")
    drivers = day.get("drivers") or {}
    driver = drivers.get(route) or day.get("driver") or "____________"
    title = "%s \xb7 %s %d, %d" % (day["day"].upper(), dt.strftime("%b"), dt.day, dt.year)
    sub = "%s \xb7 Driver: %s \xb7 Locked %s" % (route or "All %s stops" % day["day"], driver, day.get("locked_at", ""))
    tx = LEFT + 12 + (LOGO_SIZE + 14 if d.logo else 0)
    sub_lines = wrap_runs([(sub, "r", 10.5, INK, None)], RIGHT - 12 - tx)
    h = max(10 + 28 + 12.8 * len(sub_lines) + 10, LOGO_SIZE + 16)
    d.rect(LEFT, d.y, WIDTH, h, fill=BAND)
    d.line(LEFT, d.y + h, RIGHT, d.y + h, INK, 2)
    d.image_logo(LEFT + 10, d.y + (h - LOGO_SIZE) / 2, LOGO_SIZE, INK)
    top = d.y + (h - (28 + 12.8 * len(sub_lines))) / 2
    d.text(tx, top + 22, title, 26, "b", INK)
    for k, l in enumerate(sub_lines):
        d.runs_line(tx, top + 28 + 10 + 12.8 * k, l)
    d.y += h + 10


def draw_tiles(d, stops, totals):
    deliver = sum(1 for s in stops if not s["skip"])
    skipping = sum(1 for s in stops if s["skip"])
    jars = totals.get(MILK, 0) * 2 + totals.get(EXTRA, 0)
    addon_items = sum(v for p, v in totals.items() if p not in (MILK, EXTRA))
    w, h = WIDTH / 4.0, 50
    for k, (n, lab) in enumerate(zip((deliver, skipping, jars, addon_items),
                                     ("STOPS TO DELIVER", "SKIPPING", "MILK JARS", "ADD-ON ITEMS"))):
        x0 = LEFT + k * w + (3 if k else 0)
        x1 = LEFT + (k + 1) * w - (3 if k < 3 else 0)
        d.rect(x0, d.y, x1 - x0, h, stroke=INK, lw=1)
        cx = (x0 + x1) / 2
        d.text(cx, d.y + 28, fmt(n), 22, "b", INK, "center")
        d.text(cx, d.y + 42, lab, 8, "b", MUTED, "center")
    d.y += h + 12


def draw_skip_box(d, stops):
    skips = [s for s in stops if s["skip"]]
    nomilk = [s for s in stops if s["no_milk"]]
    inner = WIDTH - 24
    lines = [("h", wrap_runs([("X  DO NOT DELIVER" if skips else "No skips this week", "b", 14, INK, None)], inner))]
    for s in skips:
        lines.append(("l", wrap_runs([("Stop %s: %s" % (s.get("stop") or "?", s.get("name", "")), "b", 11, INK, None),
                                      (", %s, %s: SKIP, nothing to deliver this week" % (s.get("address", ""), s.get("city", "")),
                                       "r", 11, INK, None)], inner)))
    if nomilk:
        lines.append(("h", wrap_runs([("NO MILK THIS WEEK (add-ons only)", "b", 14, INK, None)], inner)))
        for s in nomilk:
            lines.append(("l", wrap_runs([("Stop %s: %s" % (s.get("stop") or "?", s.get("name", "")), "b", 11, INK, None),
                                          (": NO MILK, add-ons only", "r", 11, INK, None)], inner)))
    h = 8 + sum((17 if t == "h" else 14) * len(ls) + 4 for t, ls in lines) + 4
    ensure(d, h)
    thick = 3 if (skips or nomilk) else 1
    d.rect(LEFT, d.y, WIDTH, h, stroke=INK, lw=thick)
    yy = d.y + 8
    for t, ls in lines:
        lead = 17 if t == "h" else 14
        for l in ls:
            d.runs_line(LEFT + 12, yy + lead - 3.5, l)
            yy += lead
        yy += 4
    d.y += h + 14


def heading(d, s):
    ensure(d, 40)
    d.text(LEFT + 6, d.y + 13, s, 13, "b", INK)
    d.y += 20


def draw_packing(d, products, units, totals):
    heading(d, "PACKING LIST")
    xs = [LEFT, LEFT + 25.2, LEFT + 212.4, LEFT + 262.8, RIGHT]
    ensure(d, 22)
    for k, h in ((1, "ITEM"), (2, "QTY"), (3, "UNIT")):
        d.text(xs[k] + 6, d.y + 13, h, 8.5, "b", MUTED)
    d.y += 20
    d.line(LEFT, d.y, RIGHT, d.y, RULE, 0.5)
    rows = []
    jars = totals.get(MILK, 0) * 2 + totals.get(EXTRA, 0)
    if jars:
        extra = totals.get(EXTRA, 0)
        detail = "half-gallon jars (%s gal%s)" % (fmt(jars / 2), ", including %s extra" % fmt(extra) if extra else "")
        rows.append(("Milk", fmt(jars), detail, 13))
    for p in products:
        if p in (MILK, EXTRA) or not totals.get(p):
            continue
        rows.append((p, fmt(totals[p]), units.get(p, ""), 10.5))
    for k, (item, qty, unit, size) in enumerate(rows):
        ul = wrap_runs([(unit, "r", 9.5, INK, None)], xs[4] - xs[3] - 12)
        h = max(size * 1.22, 11.6 * len(ul), 12) + 10
        if ensure(d, h):
            d.line(LEFT, d.y, RIGHT, d.y, RULE, 0.5)
        d.rect(LEFT, d.y, WIDTH, h, fill=ZEBRA if k % 2 else WHITE)
        mid = d.y + h / 2
        d.box(xs[0] + 6, mid - 6, 12)
        d.text(xs[1] + 6, mid + size * 0.35, item, size, "b")
        d.text(xs[2] + 6, mid + size * 0.35, qty, size, "b")
        for j, l in enumerate(ul):
            d.runs_line(xs[3] + 6, mid + 3.3 - 5.8 * (len(ul) - 1) + 11.6 * j, l)
        d.y += h
        d.line(LEFT, d.y, RIGHT, d.y, RULE, 0.5)
    d.y += 16


STOP_X = [LEFT, LEFT + 36, LEFT + 72, LEFT + 219.6, LEFT + 331.2, LEFT + 468, RIGHT]


def stops_header(d):
    for k, h in enumerate(("DONE", "STOP", "CUSTOMER", "DELIVER", "NOTES", "FLAGS")):
        d.text(STOP_X[k] + 6, d.y + 13, h, 7.5, "b", MUTED)
    d.y += 19
    d.line(LEFT, d.y, RIGHT, d.y, INK, 1.2)


def stop_cells(s):
    cw = [STOP_X[k + 1] - STOP_X[k] - 12 for k in range(6)]
    maps = "https://maps.google.com/?q=" + quote_plus("%s, %s KY" % (s.get("address", ""), s.get("city", "")), safe=",")
    cust = wrap_runs([(s.get("name", ""), "b", 9.5, INK, None)], cw[2])
    cust += wrap_runs([(s.get("address", ""), "r", 9.5, ACCENT, maps), (", " + s.get("city", ""), "r", 9.5, INK, None)], cw[2])
    nums = [phone_text(n) for n in (s.get("phone"), s.get("phone2")) if (n or "").strip()]
    if nums:
        for label, tel in nums:
            cust += wrap_runs([(label, "r", 9.5, ACCENT if tel else INK, tel)], cw[2])
    else:
        cust += wrap_runs([("no phone", "r", 9.5, INK, None)], cw[2])
    deliver = []
    if s["skip"]:
        deliver += wrap_runs([("SKIP: NO DELIVERY", "b", 10.5, INK, None)], cw[3])
    else:
        if s["jars"]:
            first = [("%s jar%s" % (fmt(s["jars"]), "" if s["jars"] == 1 else "s"), "b", 13, INK, None)]
            if s["extra"]:
                first.append((" + %s extra" % fmt(s["extra"]), "b", 9.5, INK, None))
            deliver += wrap_runs(first, cw[3])
        elif s["extra"]:
            deliver += wrap_runs([("%s extra jar%s" % (fmt(s["extra"]), "" if s["extra"] == 1 else "s"), "b", 9.5, INK, None)], cw[3])
        if s["no_milk"]:
            deliver += wrap_runs([("NO MILK", "b", 9.5, INK, None)], cw[3])
        for p, v in s["addons"]:
            deliver += wrap_runs([("%s x %s" % (fmt(v), p), "r", 9.5, INK, None)], cw[3])
        for o in s["odd"]:
            deliver += wrap_runs([(o, "b", 9.5, INK, None)], cw[3])
    notes = wrap_runs([(s.get("delivery_notes", "") or "", "i", 9, INK, None)], cw[4]) if s.get("delivery_notes") else []
    flags = [[(f, "b", 9, INK, None)] for f in s["flags"]]
    return cust, deliver, notes, flags


def lines_height(lines):
    return sum(max(r[2] for r in l) * 1.22 for l in lines)


def draw_lines(d, x, y, lines):
    for l in lines:
        size = max(r[2] for r in l)
        y += size * 1.22
        d.runs_line(x, y - size * 0.22, l)


def draw_stops(d, stops):
    heading(d, "STOPS")
    ensure(d, 80)
    stops_header(d)
    for k, s in enumerate(stops):
        cust, deliver, notes, flags = stop_cells(s)
        h = max(lines_height(cust), lines_height(deliver), lines_height(notes), lines_height(flags), 18.3, 13) + 12
        if ensure(d, h):
            stops_header(d)
        d.page_names.setdefault(len(d.pages), s.get("name", ""))
        fill = SKIPFILL if s["skip"] else (ZEBRA if k % 2 else WHITE)
        d.rect(LEFT, d.y, WIDTH, h, fill=fill)
        d.box(STOP_X[0] + 6, d.y + 6, 13)
        d.text((STOP_X[1] + STOP_X[2]) / 2, d.y + 6 + 15, str(s.get("stop") or "?"), 15, "b", INK, "center")
        draw_lines(d, STOP_X[2] + 6, d.y + 6, cust)
        draw_lines(d, STOP_X[3] + 6, d.y + 6, deliver)
        draw_lines(d, STOP_X[4] + 6, d.y + 6, notes)
        draw_lines(d, STOP_X[5] + 6, d.y + 6, flags)
        d.y += h
        d.line(LEFT, d.y, RIGHT, d.y, RULE, 0.5)


def draw_changes(d, stops):
    out = []
    for s in stops:
        lines = real_changes(s)
        attn = (s.get("needs_attention") or "").strip()
        if lines or attn:
            runs = [("Stop %s \xb7 %s: " % (s.get("stop") or "?", s.get("name", "")), "b", 9.5, INK, None),
                    ("; ".join(lines), "r", 9.5, INK, None)]
            if attn:
                runs += [("; " if lines else "", "r", 9.5, INK, None), (attn, "b", 9.5, INK, None)]
            out.append(wrap_runs(runs, WIDTH - 12))
    if not out:
        return
    d.y += 14
    heading(d, "CHANGES THIS WEEK")
    for ls in out:
        ensure(d, 11.6 * len(ls) + 3)
        for l in ls:
            d.y += 11.6
            d.runs_line(LEFT + 6, d.y - 2, l)
        d.y += 3


def build(day, path):
    products, stops = analyse(day)
    units = {p["column"]: p.get("unit", "") for p in day["products"]}
    dt = datetime.strptime(day["date"], "%Y-%m-%d")
    made = day.get("made") or day.get("locked_at") or ""
    d = Doc("%s delivery list - %s %s %d, %d - made %s" % (day.get("farm", ""), day["day"], dt.strftime("%b"), dt.day, dt.year, made))
    routes = []
    for s in stops:
        r = (s.get("route") or "").strip()
        if r not in routes:
            routes.append(r)
    routes = routes or [""]
    for k, r in enumerate(routes):
        if k:
            d.new_page()
        rs = [s for s in stops if (s.get("route") or "").strip() == r]
        tot = totals_for(rs)
        draw_header(d, day, r)
        draw_tiles(d, rs, tot)
        draw_skip_box(d, rs)
        draw_packing(d, products, units, tot)
        draw_stops(d, rs)
        draw_changes(d, rs)
    pending = day.get("pending") or []
    if pending:
        d.y += 14
        ensure(d, 60)
        for l in wrap_runs([("PENDING: NOT PACKED (Mark hasn't decided; don't pack unless he says so)", "b", 13, INK, None)], WIDTH - 12):
            d.y += 16
            d.runs_line(LEFT + 6, d.y - 3, l)
        d.y += 4
        for p in pending:
            ls = wrap_runs([("%s: " % p.get("customer", ""), "b", 9.5, INK, None), (p.get("asked_for", ""), "r", 9.5, INK, None)], WIDTH - 12)
            ensure(d, 11.6 * len(ls))
            for l in ls:
                d.y += 11.6
                d.runs_line(LEFT + 6, d.y - 2, l)
    size_bytes, pages = d.save(path, "Delivery list %s %s" % (day["day"], day["date"]))
    tot = totals_for(stops)
    deliver = sum(1 for s in stops if not s["skip"])
    skipping = sum(1 for s in stops if s["skip"])
    guesses = sum(1 for s in stops if "GUESS" in s["flags"])
    named = [r for r in routes if r]
    message = ("%s's delivery list is ready: {LINK}. %d stops to deliver, %s. %d skipping (boxed at the top). %d guesses marked. "
               "Shares and orders for %s are now locked." % (day["day"], deliver, ", ".join(named) if named else "1 route",
                                                              skipping, guesses, day["day"]))
    check = [day["day"].upper()] + [d.page_names[k] for k in sorted(d.page_names)]
    return {"pdf": path, "base64_file": path + ".b64", "base64_chars": len(open(path + ".b64").read()), "bytes": size_bytes, "pages": pages, "rows_read": len(day["rows"]), "check_words": check,
            "stops_to_deliver": deliver, "skipping": skipping, "guesses": guesses, "routes": routes,
            "milk_jars": tot.get(MILK, 0) * 2 + tot.get(EXTRA, 0),
            "flags": {s.get("name", ""): s["flags"] for s in stops if s["flags"]},
            "file_name": "Delivery list %s %s %d %d.pdf" % (dt.strftime("%a"), dt.strftime("%b"), dt.day, dt.year),
            "message": message}


def main():
    if len(sys.argv) != 3:
        print(json.dumps({"error": "usage: delivery_list_pdf.py day.json list.pdf"}))
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            day = json.load(f)
        summary = build(day, sys.argv[2])
    except (KeyError, ValueError, TypeError, OSError) as e:
        print(json.dumps({"error": "%s: %s" % (type(e).__name__, e)}))
        return 1
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
