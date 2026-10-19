#!/usr/bin/env python3
"""Weekly master list: a one-page PDF of a delivery week's totals by day.

Usage: python3 -I master_list_pdf.py master.json master.pdf

Standard library only (nothing to install). The routine copies week-tab cells
into master.json; this script does all the counting, decides whether tonight's
list goes out, draws the page and prints one line of JSON describing it.
It also writes [master.pdf].b64, the PDF as one line of base64, ready for Google Drive create_file's base64Content (instructions/save-pdf.md).
See instructions/weekly-master-list.md for the input format; tools/sample-master-list.json is an example.
"""
import base64
import json
import os
import re
import sys
import zlib
from datetime import date, datetime, timedelta

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
SHORT = ["Mon", "Tue", "Wed", "Thu", "Fri"]
MILK = "Milk (gal)"
EXTRA = "Extra Milk"

BLACK = (0.1, 0.1, 0.1)

# Helvetica and Helvetica-Bold widths (1/1000 em) for characters 32-126.
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

PAGE_W, PAGE_H, MARGIN = 612, 792, 36


def width(s, size, bold=False):
    table = _BOLD if bold else _REG
    total = 0
    for b in s.encode("cp1252", errors="replace"):
        total += table[b - 32] if 32 <= b <= 126 else 556
    return total * size / 1000.0


def wrap(s, max_w, size, bold=False):
    lines, cur = [], ""
    for word in s.split(" "):
        trial = word if not cur else cur + " " + word
        if width(trial, size, bold) <= max_w:
            cur = trial
            continue
        if cur:
            lines.append(cur)
        while width(word, size, bold) > max_w:
            cut = len(word)
            while cut > 1 and width(word[:cut], size, bold) > max_w:
                cut -= 1
            lines.append(word[:cut])
            word = word[cut:]
        cur = word
    if cur:
        lines.append(cur)
    return lines or [""]


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


def load_logo():
    """The farm logo as a 1-bit image mask (tools/logo-mask.json). None if it's missing."""
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo-mask.json"), encoding="ascii") as f:
            j = json.load(f)
        return int(j["w"]), int(j["h"]), base64.a85decode(j["a85"].encode("ascii").rstrip(b"~>").rstrip())
    except (OSError, ValueError, KeyError):
        return None


class Page:
    """Top-down coordinates (y grows downward), converted to PDF space on output."""

    def __init__(self):
        self.ops = []
        self.logo = load_logo()

    def image_logo(self, x, y, size, color):
        if not self.logo:
            return False
        self.ops.append("q %s rg %.2f 0 0 %.2f %.2f %.2f cm /Logo Do Q" % (self._c(color), size, size, x, PAGE_H - y - size))
        return True

    def _c(self, rgb):
        return "%.3f %.3f %.3f" % rgb

    def rect(self, x, y, w, h, fill=None, stroke=None, lw=1.0):
        if fill:
            self.ops.append("%s rg %.2f %.2f %.2f %.2f re f" % (self._c(fill), x, PAGE_H - y - h, w, h))
        if stroke:
            self.ops.append("%.2f w %s RG %.2f %.2f %.2f %.2f re S" % (lw, self._c(stroke), x, PAGE_H - y - h, w, h))

    def line(self, x1, y1, x2, y2, color=BLACK, lw=1.0):
        self.ops.append("%.2f w %s RG %.2f %.2f m %.2f %.2f l S" % (lw, self._c(color), x1, PAGE_H - y1, x2, PAGE_H - y2))

    def text(self, x, y, s, size, bold=False, color=BLACK, align="left"):
        if align == "center":
            x -= width(s, size, bold) / 2
        elif align == "right":
            x -= width(s, size, bold)
        self.ops.append("BT /%s %.1f Tf %s rg 1 0 0 1 %.2f %.2f Tm %s Tj ET"
                        % ("F2" if bold else "F1", size, self._c(color), x, PAGE_H - y, pdf_string(s)))

    def save(self, path, title):
        content = zlib.compress("\n".join(self.ops).encode("ascii"), 9)
        objs = [
            b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            ("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] /Resources << /Font << /F1 4 0 R /F2 5 0 R >>%s >> /Contents 6 0 R >>"
             % (PAGE_W, PAGE_H, " /XObject << /Logo 8 0 R >>" if self.logo else "")).encode("ascii"),
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
            b"<< /Length " + str(len(content)).encode("ascii") + b" /Filter /FlateDecode >>\nstream\n" + content + b"\nendstream",
            ("<< /Title %s /Producer (farm-ops master_list_pdf.py) >>" % pdf_string(title)).encode("ascii"),
        ]
        if self.logo:
            w, h, data = self.logo
            objs.append((("<< /Type /XObject /Subtype /Image /Width %d /Height %d /ImageMask true /BitsPerComponent 1 "
                          "/Length %d /Filter /FlateDecode >>\nstream\n" % (w, h, len(data))).encode("ascii")
                         + data + b"\nendstream"))
        out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = []
        for i, body in enumerate(objs, start=1):
            offsets.append(len(out))
            out += b"%d 0 obj\n" % i + body + b"\nendobj\n"
        xref = len(out)
        out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
        for off in offsets:
            out += b"%010d 00000 n \n" % off
        out += b"trailer\n<< /Size %d /Root 1 0 R /Info 7 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
        with open(path, "wb") as f:
            f.write(bytes(out))
        with open(path + ".b64", "w", encoding="ascii") as f:
            f.write(base64.b64encode(bytes(out)).decode("ascii"))
        return len(out)


# ---------- data ----------

ENTRY = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) (.+?) (-?\d+(?:\.\d+)?)>(-?\d+(?:\.\d+)?)(?: \((.*)\))?$")


def parse_time(s):
    return datetime.strptime(s.strip(), "%Y-%m-%d %H:%M")


def friendly(dt):
    h = dt.hour % 12 or 12
    return "%s %s %d, %d:%02d%s" % (dt.strftime("%a"), dt.strftime("%b"), dt.day, h, dt.minute, "am" if dt.hour < 12 else "pm")


def num(x):
    x = round(x, 2)
    return str(int(x)) if x == int(x) else ("%g" % x)


def build(data):
    problems = []
    now = parse_time(data["now"])
    last_sent = parse_time(data["last_sent"]) if (data.get("last_sent") or "").strip() else None
    monday = datetime.strptime(data["monday"], "%Y-%m-%d").date()
    if monday.weekday() != 0:
        raise ValueError("monday %s is not a Monday" % data["monday"])
    day_dates = [monday + timedelta(days=i) for i in range(5)]
    today = now.date()
    done = [d <= today for d in day_dates]
    week = data.get("week", "")

    products = [p["column"] for p in data["products"]]
    units = {p["column"]: (p.get("unit") or "") for p in data["products"]}
    weeks = {p["column"]: (p.get("weeks") or "All") for p in data["products"]}
    cols = data["columns"]
    idx = {c: i for i, c in enumerate(cols)}
    for need in ("Cust ID", "Name", "Day", "Changes"):
        if need not in idx:
            raise ValueError('column "%s" missing from columns' % need)
    for p in products:
        if p not in idx:
            problems.append('Week tab has no "%s" column: counted as none.' % p)

    rows = []
    for r in data["rows"]:
        if len(r) != len(cols):
            raise ValueError("a row has %d cells but there are %d columns: %s" % (len(r), len(cols), r[:2]))
        cell = lambda c: (r[idx[c]] if c in idx else "").strip()
        cid, name = cell("Cust ID"), cell("Name")
        if not cid and not name:
            continue
        if cid.upper().startswith("T"):
            continue
        q = {}
        for p in products:
            raw = cell(p)
            if raw == "":
                q[p] = 0.0
                continue
            try:
                q[p] = float(raw)
            except ValueError:
                q[p] = 0.0
                problems.append('%s: %s says "%s", not a number; not counted.' % (name, p, raw))
        day = cell("Day")
        di = DAYS.index(day) if day in DAYS else None
        entries, bad = [], []
        for part in [e.strip() for e in cell("Changes").split(" ; ") if e.strip()]:
            m = ENTRY.match(part)
            if not m:
                bad.append(part)
                continue
            t, prod, old, new, src = m.groups()
            entries.append({"time": parse_time(t), "product": prod, "old": float(old), "new": float(new),
                            "source": src or "", "sync": (src or "").strip() == "standing order sync"})
        rows.append({"id": cid, "name": name, "day": di, "q": q, "entries": entries, "bad": bad})
        if di is None and any(v > 0 for v in q.values()):
            items = ", ".join("%s %s" % (p, num(v)) for p, v in q.items() if v > 0)
            why = "has no delivery day" if not day else 'has Day "%s", not Monday to Friday' % day
            problems.append("%s (%s) %s: %s not counted in any day." % (name, cid, why, items))
        for b in bad:
            if last_sent is None or b[:16] > last_sent.strftime("%Y-%m-%d %H:%M"):
                problems.append('%s: could not read change entry "%s".' % (name, b))
        last = {}
        for e in sorted(entries, key=lambda e: e["time"]):
            last[e["product"]] = e
        if di is not None and not done[di]:
            for p, e in last.items():
                if p in q and abs(e["new"] - q[p]) > 1e-9:
                    problems.append("%s: %s is %s on the sheet but its last change says %s." % (name, p, num(q[p]), num(e["new"])))

    # totals and changes (changes: after last_sent, not a standing order sync, on days not yet delivered)
    shown = [p for p in products]
    totals = {p: [0.0] * 5 for p in shown}
    deliveries = [0] * 5
    prev_deliveries = [0] * 5
    delta = {p: [0.0] * 5 for p in shown}
    skipping = [[] for _ in range(5)]
    change_lines = [[] for _ in range(5)]
    n_changes = 0
    for row in rows:
        di = row["day"]
        if di is None:
            continue
        q = row["q"]
        for p in shown:
            totals[p][di] += q[p]
        active = any(v > 0 for v in q.values())
        deliveries[di] += 1 if active else 0
        if not active:
            skipping[di].append(row["name"])
        recent = []
        if last_sent is not None and not done[di]:
            recent = [e for e in row["entries"] if e["time"] > last_sent and not e["sync"]]
        prev = dict(q)
        for e in recent:
            if e["product"] in delta:
                delta[e["product"]][di] += e["new"] - e["old"]
                prev[e["product"]] -= e["new"] - e["old"]
        prev_deliveries[di] += 1 if any(v > 0 for v in prev.values()) else 0
        if recent:
            n_changes += 1
            recent.sort(key=lambda e: e["time"])
            what = ", ".join("%s %s>%s" % (e["product"], num(e["old"]), num(e["new"])) for e in recent)
            srcs = []
            for e in recent:
                s = e["source"] or "no source"
                s = "standing order" if s == "standing order change" else s
                if s not in srcs:
                    srcs.append(s)
            line = "%s: %s (%s)" % (row["name"], what, ", ".join(srcs))
            if not active:
                line += " = NO DELIVERY"
            change_lines[di].append(line)

    kind = "update" if last_sent is not None else "first"
    wd = now.weekday()
    if wd == 5:
        send, reason = True, "Saturday: the week's list always goes out"
    elif wd == 4:
        send, reason = False, "Friday: no master list"
    elif kind == "first":
        send, reason = True, "no list has gone out for this week yet"
    elif n_changes:
        send, reason = True, "%d customer%s changed since the last list" % (n_changes, "" if n_changes == 1 else "s")
    else:
        send, reason = False, "no changes since the last list"

    return {
        "now": now, "last_sent": last_sent, "monday": monday, "day_dates": day_dates, "done": done,
        "week": week, "products": products, "units": units, "totals": totals, "delta": delta,
        "deliveries": deliveries, "prev_deliveries": prev_deliveries, "skipping": skipping,
        "weeks": weeks, "first_week": bool(data.get("first_week", False)),
        "change_lines": change_lines, "n_changes": n_changes, "problems": problems, "kind": kind,
        "send": send, "reason": reason, "rows_read": len(data["rows"]), "farm": data.get("farm", ""),
    }


def week_range(m):
    f = m + timedelta(days=4)
    return "Mon %s %d to Fri %s %d, %d" % (m.strftime("%b"), m.day, f.strftime("%b"), f.day, f.year)


def day_label(m, i):
    d = m["day_dates"][i]
    return "%s %s %d" % (SHORT[i], d.strftime("%b"), d.day)


# ---------- drawing ----------

# Colors from restorationfarmsteadky.com (meaning never by color alone)
INK = (0.153, 0.012, 0.027)    # site text maroon #270307
SUB = (0.33, 0.27, 0.26)       # dark brown-gray
MUTED = (0.42, 0.37, 0.36)     # labels
HAIR = (0.718, 0.725, 0.565)   # site sage #B7B990
SHADE = (1.0, 0.973, 0.910)    # site cream #FFF8E8
LOGO = 54
LEFT, RIGHT = 43, PAGE_W - 43
TEXT_X = 60
DASH = "–"


def addon_list(m, days, sep=", "):
    parts = []
    for p in m["products"]:
        if p in (MILK, EXTRA):
            continue
        v = sum(m["totals"][p][i] for i in days)
        if v:
            parts.append("%s %s" % (p, num(v)))
    return sep.join(parts)


def section_label(pg, y, s):
    pg.text(TEXT_X, y, s.upper(), 8, True, MUTED)


def draw(m, path):
    upd = m["kind"] == "update"
    ahead = [i for i in range(5) if not m["done"][i]]
    partial = 0 < len(ahead) < 5
    span = ahead if ahead else list(range(5))
    span_name = "%s to %s" % (SHORT[span[0]], SHORT[span[-1]]) if len(span) > 1 else SHORT[span[0]]
    extra = {i: (m["totals"][EXTRA][i] if EXTRA in m["totals"] else 0) for i in range(5)}
    gal = {i: (m["totals"][MILK][i] if MILK in m["totals"] else 0) for i in range(5)}
    jars = {i: gal[i] * 2 + extra[i] for i in range(5)}
    skips = {i: len(m["skipping"][i]) for i in range(5)}

    blocks = []

    def header(pg, y):
        tx = LEFT + LOGO + 14 if pg.image_logo(LEFT, y + 2, LOGO, INK) else TEXT_X
        pg.text(tx, y + 26, "Master list (updated)" if upd else "Master list", 26, True, INK)
        sub = "Delivery week %s  \xb7  %s  \xb7  sheet as of %s" % (m["week"], week_range(m["monday"]), friendly(m["now"]))
        yy = y + 46
        for l in wrap(sub, RIGHT - tx, 12):
            pg.text(tx, yy, l, 12, False, SUB)
            yy += 15
        return max(yy + 2, y + LOGO + 8)

    def tiles(pg, y):
        suffix = " LEFT" if partial else ""
        vals = [("STOPS" + suffix, sum(m["deliveries"][i] for i in span)),
                (("SHARE GAL" if partial else "SHARE GALLONS") + suffix, sum(gal[i] for i in span)),
                (("JARS" if partial else "HALF-GAL JARS") + suffix, sum(jars[i] for i in span)),
                (("ADD-ONS" if partial else "ADD-ON ITEMS") + suffix,
                 sum(m["totals"][p][i] for p in m["products"] if p not in (MILK, EXTRA) for i in span))]
        w = (RIGHT - LEFT) / 4.0
        for k, (lab, v) in enumerate(vals):
            pg.text(LEFT + k * w, y + 12, lab, 8, True, MUTED)
            pg.text(LEFT + k * w, y + 38, num(v), 26, True, INK)
        pg.line(LEFT, y + 46, RIGHT, y + 46, INK, 1.2)
        notes = []
        if partial:
            done_names = [SHORT[i] for i in range(5) if m["done"][i]]
            notes.append("Numbers are for %s (%s done)." % (span_name, ", ".join(done_names)))
        ex = sum(extra[i] for i in span)
        if ex:
            notes.append("Jars include %s Extra Milk jar%s." % (num(ex), "" if ex == 1 else "s"))
        names = ["%s (%s)" % (n, SHORT[i]) for i in span for n in m["skipping"][i]]
        if names:
            notes.append("%d customer%s skipping (not counted as stops): %s." % (len(names), " is" if len(names) == 1 else "s are", ", ".join(names)))
        yy = y + 59
        for l in wrap(" ".join(notes), RIGHT - TEXT_X, 9):
            pg.text(TEXT_X, yy, l, 9, False, SUB)
            yy += 11.5
        return yy + 4

    def by_day(pg, y):
        section_label(pg, y + 8, "By day")
        y += 14
        xs = [LEFT, LEFT + 77, LEFT + 120, LEFT + 163, LEFT + 224, LEFT + 306, RIGHT]
        for k, h in enumerate(["DAY", "STOPS", "SKIPS", "SHARE GAL", "JARS", "ADD-ONS TO PACK"]):
            pg.text(xs[k] + 6, y + 12, h, 8, True, MUTED)
        y += 17
        pg.line(LEFT, y, RIGHT, y, INK, 1.0)
        aw = RIGHT - xs[5] - 12

        def row(y, label, stops, sk, g, j, ex, adds, bold, color, shade, top_rule):
            lines = wrap(adds or DASH, aw, 11, bold)
            jtxt = num(j) + (" (%s extra)" % num(ex) if ex else "")
            jl = wrap(jtxt, xs[5] - xs[4] - 10, 11, bold)
            h = 6 + 13 * max(len(lines), len(jl))
            if shade:
                pg.rect(LEFT, y, RIGHT - LEFT, h, fill=SHADE)
            if top_rule:
                pg.line(LEFT, y, RIGHT, y, INK, 1.2)
            base = y + 14
            pg.text(xs[0] + 6, base, label, 11, True, color)
            pg.text(xs[1] + 6, base, str(stops), 11, bold, color)
            pg.text(xs[2] + 6, base, str(sk) if sk else DASH, 11, bold, color)
            pg.text(xs[3] + 6, base, num(g), 11, bold, color)
            for k, l in enumerate(jl):
                pg.text(xs[4] + 6, base + 13 * k, l, 11, bold, color)
            for k, l in enumerate(lines):
                pg.text(xs[5] + 6, base + 13 * k, l, 11, bold, color)
            return y + h

        for i in range(5):
            dn = m["done"][i]
            y = row(y, day_label(m, i), m["deliveries"][i], skips[i], gal[i], jars[i], extra[i],
                    ("Done. " if dn else "") + addon_list(m, [i]), False, MUTED if dn else INK, False, False)
            pg.line(LEFT, y, RIGHT, y, HAIR, 0.6)
        y = row(y, "Left" if partial else "Week", sum(m["deliveries"][i] for i in span), sum(skips[i] for i in span),
                sum(gal[i] for i in span), sum(jars[i] for i in span), sum(extra[i] for i in span),
                addon_list(m, span), True, INK, True, True)
        return y + 14

    def by_product(pg, y):
        section_label(pg, y + 8, "Add-ons by product")
        y += 14
        x0 = 79
        xs = [x0, x0 + 113, x0 + 184, x0 + 227, x0 + 270, x0 + 313, x0 + 356, x0 + 399, x0 + 451]
        heads = ["PRODUCT", "UNIT"] + [SHORT[i].upper() for i in range(5)] + ["WEEK"]
        for k, h in enumerate(heads):
            pg.text(xs[k] + 6, y + 12, h, 8, True, MUTED)
        y += 17
        pg.line(x0, y, xs[-1], y, INK, 1.0)
        prods = [p for p in m["products"] if p != MILK and any(m["totals"][p])]
        if not prods:
            pg.text(xs[0] + 6, y + 15, "No add-ons this week.", 11, False, SUB)
            return y + 34
        for p in prods:
            unit = "half-gal jar" if p == EXTRA else m["units"].get(p, "")
            pg.text(xs[0] + 6, y + 13, p, 11, False, INK)
            pg.text(xs[1] + 6, y + 13, unit, 8.5, False, MUTED)
            for i in range(5):
                v = m["totals"][p][i]
                pg.text(xs[2 + i] + 6, y + 13, num(v) if v else DASH, 11, False, MUTED if m["done"][i] else INK)
            pg.text(xs[7] + 6, y + 13, num(sum(m["totals"][p])), 11, True, INK)
            y += 17
            pg.line(x0, y, xs[-1], y, HAIR, 0.6)
        return y + 4

    def footnote(pg, y):
        notes = []
        if any(extra.values()):
            notes.append("Extra Milk jars are already counted in the jar totals above.")
        fw = [p for p in m["products"] if m["weeks"].get(p) == "First week only" and not any(m["totals"][p])]
        if fw and not m["first_week"]:
            notes.append("First-week-only products (%s) aren't offered this week." % ", ".join(fw))
        none = [p for p in m["products"] if p not in fw and p != MILK and not any(m["totals"][p])]
        if none:
            notes.append("Nothing ordered this week: %s." % ", ".join(none))
        yy = y + 8
        for l in wrap(" ".join(notes), RIGHT - TEXT_X, 9):
            pg.text(TEXT_X, yy, l, 9, False, SUB)
            yy += 11.5
        return yy + 2

    def problems(pg, y):
        probs = m["problems"]
        if not probs:
            return y
        lines = []
        for p in probs[:6]:
            lines += wrap("! " + p, RIGHT - TEXT_X, 10)
        if len(probs) > 6:
            lines.append("! %d more: check the week tab." % (len(probs) - 6))
        pg.text(TEXT_X, y + 10, "NEEDS A LOOK", 10, True, INK)
        yy = y + 23
        for l in lines:
            pg.text(TEXT_X, yy, l, 10, False, INK)
            yy += 13
        return yy + 4

    def measure(fn):
        return fn(Page(), 0)

    fixed = [header, tiles, by_day, by_product, footnote, problems]
    top = 36
    bottom = PAGE_H - 42
    used = sum(measure(f) for f in fixed)
    room = bottom - top - used

    changes_shown = 0
    change_block = None
    if upd:
        groups = [(i, m["change_lines"][i]) for i in range(5) if m["change_lines"][i]]
        n = m["n_changes"]
        title = ("Changes since the last list (%s): %d customer%s" % (friendly(m["last_sent"]), n, "" if n == 1 else "s")) if n \
            else "No changes since the last list (%s)" % friendly(m["last_sent"])
        net = []
        for p in m["products"]:
            d = sum(m["delta"][p][i] for i in span) * (2 if p == MILK else 1)
            if abs(d) > 1e-9:
                net.append("%s %s%s" % ("share jars" if p == MILK else p, "+" if d > 0 else "-", num(abs(d))))
        net_lines = wrap("Net change: " + ", ".join(net), RIGHT - LEFT - 24, 9.5, True)[:2] if net else []
        overhead = 26 + 13 * len(net_lines) + (3 if net_lines else 0) + 8 + 12

        def layout(size, ncol):
            colw = (RIGHT - LEFT - 24 - 14 * (ncol - 1)) / ncol
            lines = []
            for i, ls in groups:
                lines.append(("day", day_label(m, i)))
                for l in ls:
                    for k, w in enumerate(wrap(l, colw - 10, size)):
                        lines.append(("item" if k == 0 else "cont", w))
            return colw, lines

        def starts(lines):
            # a unit is one entry with its wrapped lines; a day heading stays with its first entry
            return [k for k, (t, _) in enumerate(lines) if t in ("day", "note") or (t == "item" and (k == 0 or lines[k - 1][0] != "day"))]

        def place(lines, per_col, ncol):
            st = starts(lines) + [len(lines)]
            pos, col, row = [], 0, 0
            for a, b in zip(st, st[1:]):
                size_u = b - a
                if size_u > per_col:
                    return None
                if row + size_u > per_col:
                    col, row = col + 1, 0
                if col >= ncol:
                    return None
                pos += [(col, row + k) for k in range(size_u)]
                row += size_u
            return pos

        def fit(room):
            for size, ncol in ((10, 1), (9.5, 2), (9, 2), (8.5, 2), (8.5, 3), (8, 3)):
                colw, lines = layout(size, ncol)
                lead = size * 1.3
                max_rows = int((room - overhead) // lead)
                for per_col in range(max(1, -(-len(lines) // ncol)), max_rows + 1):
                    pos = place(lines, per_col, ncol)
                    if pos:
                        return (size, ncol, colw, lines, lead, per_col, pos)
            return None

        choice = fit(room)
        if choice is None and by_product in fixed:
            # not enough room: leave out the product table (By day still lists every add-on)
            fixed.remove(by_product)
            room += measure(by_product)
            choice = fit(room)
        if choice is None:
            size, ncol = 8, 3
            colw, lines = layout(size, ncol)
            lead = size * 1.3
            per_col = max(1, int((room - overhead) // lead))
            pos = None
            for keep in reversed(starts(lines) + [len(lines)]):
                kept = lines[:keep]
                while kept and kept[-1][0] == "day":
                    kept = kept[:-1]
                hidden = sum(1 for t, _ in lines[len(kept):] if t == "item")
                note = wrap("%d more not shown: see the week tab's Changes column." % hidden, colw - 10, size)
                trial = kept + [("note", note[0])] + [("cont", w) for w in note[1:]]
                pos = place(trial, per_col, ncol)
                if pos:
                    lines = trial
                    break
            choice = (size, ncol, colw, lines, lead, per_col, pos)
        size, ncol, colw, lines, lead, per_col, pos = choice
        h = overhead - 12 + per_col * lead
        changes_shown = sum(1 for t, _ in lines if t == "item")

        def change_block(pg, y):
            pg.rect(LEFT, y, RIGHT - LEFT, h, fill=SHADE)
            pg.line(LEFT, y, RIGHT, y, INK, 1.2)
            pg.line(LEFT, y + h, RIGHT, y + h, INK, 1.2)
            pg.text(LEFT + 12, y + 18, title, 11, True, INK)
            for (t, s), (col, r) in zip(lines, pos):
                lx = LEFT + 12 + col * (colw + 14)
                ly = y + 22 + (r + 1) * lead
                if t == "day":
                    pg.text(lx, ly, s, size, True, INK)
                elif t == "item":
                    pg.text(lx + 10, ly, s, size, False, INK)
                elif t == "cont":
                    pg.text(lx + 20, ly, s, size, False, INK)
                else:
                    pg.text(lx, ly, s, size, True, INK)
            for k, l in enumerate(net_lines):
                pg.text(LEFT + 12, y + h - 9 - 13 * (len(net_lines) - 1 - k), l, 9.5, True, INK)
            return y + h + 12

    pg = Page()
    y = header(pg, top)
    if change_block:
        y = change_block(pg, y)
    for f in fixed[1:]:
        y = f(pg, y)
    pg.text(TEXT_X, PAGE_H - 26, "%s \xb7 Master list \xb7 Delivery week %s" % (m["farm"], m["week"]), 8, False, MUTED)
    pg.text(RIGHT - 17, PAGE_H - 26, "Page 1", 8, False, MUTED, "right")
    size_bytes = pg.save(path, "Master list week %s" % m["week"])
    return size_bytes, changes_shown, y


def texts(m):
    wr = week_range(m["monday"])
    ahead = [i for i in range(5) if not m["done"][i]]
    tot = []
    milk = sum(m["totals"][MILK][i] for i in ahead) * 2 if MILK in m["totals"] else 0
    extra = sum(m["totals"][EXTRA][i] for i in ahead) if EXTRA in m["totals"] else 0
    tot.append("milk %s jars" % num(milk) + (" + %s extra" % num(extra) if extra else ""))
    for p in m["products"]:
        if p in (MILK, EXTRA):
            continue
        v = sum(m["totals"][p][i] for i in ahead)
        if v:
            tot.append("%s %s" % (p, num(v)))
    span = "week" if len(ahead) == 5 else "%s-%s" % (SHORT[ahead[0]], SHORT[ahead[-1]]) if len(ahead) > 1 else SHORT[ahead[0]] if ahead else "week"
    totals_line = "Totals (%s): %s" % (span, ", ".join(tot))
    if m["kind"] == "update":
        head = "Master list UPDATED for week %s (%s): %d customer%s changed since %s, listed at the top." % (
            m["week"], wr, m["n_changes"], "" if m["n_changes"] == 1 else "s", friendly(m["last_sent"]))
    else:
        head = "Master list for week %s (%s)." % (m["week"], wr)
    message = head + " {LINK}\n" + totals_line
    if m["problems"]:
        message += "\n%d thing%s marked NEEDS A LOOK." % (len(m["problems"]), "" if len(m["problems"]) == 1 else "s")

    # fallback when there is no PDF link: numbers only, one text
    lines = [head.replace(", listed at the top.", ".")]
    if m["kind"] == "update" and m["n_changes"]:
        lines.append("WHAT CHANGED")
        for i in ahead:
            parts = []
            for p in m["products"]:
                d = m["delta"][p][i] * (2 if p == MILK else 1)
                if abs(d) > 1e-9:
                    name = "milk jars" if p == MILK else p
                    parts.append("%s %s%s" % (name, "+" if d > 0 else "-", num(abs(d))))
            if parts:
                lines.append("%s: %s" % (SHORT[i], ", ".join(parts)))
    lines.append(totals_line)
    for i in ahead:
        parts = ["%d stop%s" % (m["deliveries"][i], "" if m["deliveries"][i] == 1 else "s")]
        if MILK in m["totals"]:
            parts.append("%s jars" % num(m["totals"][MILK][i] * 2))
        for p in m["products"]:
            if p != MILK and m["totals"][p][i]:
                parts.append("%s %s" % ("extra jars" if p == EXTRA else p, num(m["totals"][p][i])))
        lines.append("%s: %s" % (SHORT[i], ", ".join(parts)))
    nd = ["%s (%s)" % (n, SHORT[i]) for i in ahead for n in m["skipping"][i]]
    if nd:
        lines.append("Skipping: " + ", ".join(nd))
    for p in m["problems"]:
        lines.append("! " + p)
    fallback = "\n".join(lines)
    if len(fallback) > 1500:
        fallback = fallback[:1400].rsplit("\n", 1)[0] + "\n(The rest didn't fit: check the week tab.)"
    return message, fallback


def main():
    if len(sys.argv) != 3:
        print(json.dumps({"error": "usage: master_list_pdf.py master.json master.pdf"}))
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            data = json.load(f)
        m = build(data)
        size_bytes, shown, _ = draw(m, sys.argv[2])
        message, fallback = texts(m)
    except (KeyError, ValueError, TypeError, OSError) as e:
        print(json.dumps({"error": "%s: %s" % (type(e).__name__, e)}))
        return 1
    ahead = [i for i in range(5) if not m["done"][i]]
    print(json.dumps({
        "pdf": sys.argv[2], "base64_file": sys.argv[2] + ".b64", "bytes": size_bytes, "pages": 1,
        "send": m["send"], "reason": m["reason"], "kind": m["kind"], "week": m["week"],
        "rows_read": m["rows_read"], "changes": m["n_changes"], "changes_shown": shown,
        "deliveries": {SHORT[i]: m["deliveries"][i] for i in range(5)},
        "milk_jars": {SHORT[i]: m["totals"][MILK][i] * 2 for i in range(5)} if MILK in m["totals"] else {},
        "days_left": [SHORT[i] for i in ahead],
        "problems": m["problems"],
        "file_name": "Master list week %s %s %s.pdf" % (m["week"], m["now"].strftime("%Y-%m-%d %H.%M"), "update" if m["kind"] == "update" else "full"),
        "message": message, "fallback_text": fallback,
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
