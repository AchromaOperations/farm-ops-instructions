#!/usr/bin/env python3
"""Delivery list Google Doc for one delivery day, as fixed HTML: the FALLBACK for when the
PDF (tools/delivery_list_pdf.py, the approved design) can't be saved. Same sections, same order.

Usage: python3 -I delivery_list_html.py day.json list.html

Standard library only (nothing to install). The routine copies the day's rows into
day.json; this script does all the counting and flags and writes the whole doc as
HTML, so every day's list has the same layout. The routine then creates the Google
Doc from list.html (HTML converted to a Google Doc). It also writes list.txt next to
it, the same list as plain text, for when HTML can't be used.
Prints one line of JSON: counts, flags and the text message to send.

Input: the same form as tools/sample-delivery-day.json, plus optional
"drivers": {"[Route]": "[Driver]"} from the Routes tab. Each row may carry "route"
(the week row's Route); rows with different routes get one section each.
"""
import json
import re
import sys
from datetime import datetime
from html import escape

SYNC = "(standing order sync)"
MILK = "Milk (gal)"
EXTRA = "Extra Milk"

FONT = "font-family:Arial,sans-serif;"
P = FONT + "color:#270307;font-size:11pt;margin:0 0 3pt 0;"
H2 = FONT + "color:#270307;font-size:13pt;font-weight:bold;margin:14pt 0 4pt 0;"
TABLE = "border-collapse:collapse;width:100%;"
NOBORDER = "border-top:none;border-left:none;border-right:none;"
# Colors from restorationfarmsteadky.com: cream #FFF8E8, maroon text #270307, sage #B7B990, navy #004990 (links)
LOGO_URL = "https://raw.githubusercontent.com/AchromaOperations/farm-ops-instructions/main/tools/logo.png"
BAND = FONT + "background-color:#FFF8E8;color:#270307;border:none;border-bottom:2pt solid #270307;padding:8pt 10pt;vertical-align:middle;"
TILE = FONT + "color:#270307;border:1pt solid #270307;padding:6pt;vertical-align:middle;"
HEAD = FONT + NOBORDER + "font-size:8pt;font-weight:bold;color:#6B5E5C;border-bottom:0.5pt solid #B7B990;padding:4pt 6pt;text-align:left;vertical-align:bottom;"
ROW = FONT + NOBORDER + "color:#270307;font-size:10pt;border-bottom:0.5pt solid #B7B990;padding:5pt 6pt;vertical-align:top;"
BOXCHAR = '<span style="font-size:15pt;">\u2610</span>'


def num(x):
    try:
        return float(x or 0)
    except (TypeError, ValueError):
        return 0.0


def fmt(x):
    x = round(float(x), 2)
    return str(int(x)) if x.is_integer() else ("%g" % x)


def phone_text(n):
    n = (n or "").strip()
    m = re.fullmatch(r"\+1(\d{3})(\d{3})(\d{4})", n)
    return "(%s) %s-%s" % m.groups() if m else n


def phone_list(row):
    return [phone_text(n) for n in (row.get("phone"), row.get("phone2")) if (n or "").strip()]


def phones(row):
    return " / ".join(phone_list(row)) or "no phone"


def phones_html(row):
    out = [escape(n).replace(" ", "&nbsp;") for n in phone_list(row)]
    return "<br>".join(out) or "no phone"


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
        if skip:
            items = "SKIP: NO DELIVERY"
        else:
            parts = []
            if milk:
                share = "share %s jar%s" % (fmt(milk * 2), "" if milk * 2 == 1 else "s") if (milk * 2).is_integer() \
                    else "share %s gal" % fmt(milk)
                parts.append(share + (" + %s extra" % fmt(extra) if extra else ""))
            elif extra:
                parts.append("%s extra jar%s" % (fmt(extra), "" if extra == 1 else "s"))
            parts += ["%s %s" % (fmt(v), p) for p, v in addons] + odd
            items = ", ".join(parts)
            if no_milk:
                items = "NO MILK, " + items
        stops.append(dict(r, q=q, milk=milk, extra=extra, addons=addons, odd=odd, skip=skip, no_milk=no_milk,
                          flags=flags, items=items))
    stops.sort(key=stop_key)
    return products, stops


def totals_for(stops):
    t = {}
    for s in stops:
        for p, v in s["q"].items():
            t[p] = t.get(p, 0) + v
    return t


def cell(style, inner, extra=""):
    return '<td style="%s%s">%s</td>' % (style, extra, inner)


def section(day, route, stops, products, first):
    d = datetime.strptime(day["date"], "%Y-%m-%d")
    drivers = day.get("drivers") or {}
    driver = drivers.get(route) or day.get("driver") or "____________"
    title = "%s · %s %d, %d" % (day["day"].upper(), d.strftime("%b"), d.day, d.year)
    sub = "%s · Driver: %s · Locked %s" % (route or "All %s stops" % day["day"], driver, day.get("locked_at", ""))
    h, t = [], []
    if not first:
        h.append('<p style="page-break-before:always;%s"></p>' % P)
    h.append('<table style="%s"><tr>%s%s</tr></table>' % (TABLE,
             cell(BAND, '<img src="%s" width="64" height="64" alt="%s">' % (LOGO_URL, escape(day.get("farm", ""))), "width:12%;"),
             cell(BAND, '<p style="%sfont-size:24pt;font-weight:bold;color:#270307;margin:0;">%s</p>'
                        '<p style="%sfont-size:10.5pt;color:#270307;margin:2pt 0 0 0;">%s</p>' % (FONT, escape(title), FONT, escape(sub)),
                  "width:88%;")))
    t += [title, sub, ""]

    tot = totals_for(stops)
    deliver = sum(1 for s in stops if not s["skip"])
    skipping = sum(1 for s in stops if s["skip"])
    jars = tot.get(MILK, 0) * 2 + tot.get(EXTRA, 0)
    addon_items = sum(v for p, v in tot.items() if p not in (MILK, EXTRA))
    tiles = "".join(cell(TILE, '<p style="%sfont-size:22pt;font-weight:bold;text-align:center;margin:0;">%s</p>'
                                '<p style="%sfont-size:8pt;font-weight:bold;color:#6B5E5C;text-align:center;margin:0;">%s</p>'
                         % (FONT, fmt(n), FONT, lab), "width:25%;")
                    for n, lab in zip((deliver, skipping, jars, addon_items),
                                      ("STOPS TO DELIVER", "SKIPPING", "MILK JARS", "ADD-ON ITEMS")))
    h.append('<p style="%s"></p><table style="%s"><tr>%s</tr></table><p style="%s"></p>' % (P, TABLE, tiles, P))
    t.append("%d stops to deliver, %d skipping, %s milk jars, %s add-on items" % (deliver, skipping, fmt(jars), fmt(addon_items)))
    t.append("")

    skips = [s for s in stops if s["skip"]]
    nomilk = [s for s in stops if s["no_milk"]]
    box = []
    if skips:
        box.append('<p style="%sfont-size:14pt;font-weight:bold;margin:0 0 4pt 0;">X&nbsp;&nbsp;DO NOT DELIVER</p>' % FONT)
        t.append("#### X  DO NOT DELIVER ####")
        for s in skips:
            line = "Stop %s: %s, %s, %s: SKIP, nothing to deliver this week" % (
                s.get("stop") or "?", s.get("name", ""), s.get("address", ""), s.get("city", ""))
            box.append('<p style="%s"><b>Stop %s: %s</b>, %s, %s: SKIP, nothing to deliver this week</p>' % (
                P, escape(str(s.get("stop") or "?")), escape(s.get("name", "")), escape(s.get("address", "")), escape(s.get("city", ""))))
            t.append(line)
    if nomilk:
        box.append('<p style="%sfont-size:14pt;font-weight:bold;margin:8pt 0 4pt 0;">NO MILK THIS WEEK (add-ons only)</p>' % FONT)
        t.append("#### NO MILK THIS WEEK (add-ons only) ####")
        for s in nomilk:
            line = "Stop %s: %s: NO MILK, add-ons only" % (s.get("stop") or "?", s.get("name", ""))
            box.append('<p style="%s"><b>Stop %s: %s</b>: NO MILK, add-ons only</p>' % (
                P, escape(str(s.get("stop") or "?")), escape(s.get("name", ""))))
            t.append(line)
    if not box:
        box.append('<p style="%sfont-size:14pt;font-weight:bold;margin:0;">No skips this week</p>' % FONT)
        t.append("No skips this week")
    border = "3pt" if (skips or nomilk) else "1pt"
    h.append('<table style="%s"><tr><td style="%scolor:#270307;border:%s solid #270307;padding:8pt 12pt;">%s</td></tr></table>'
             % (TABLE, FONT, border, "".join(box)))
    t.append("")

    h.append('<p style="%s">PACKING LIST</p>' % H2)
    t.append("PACKING LIST")
    rows = ['<tr>%s%s%s%s</tr>' % (cell(HEAD, "", "width:5%;"), cell(HEAD, "ITEM", "width:35%;"),
                                    cell(HEAD, "QTY", "width:10%;"), cell(HEAD, "UNIT", "width:50%;"))]
    items = []
    if jars:
        ex = tot.get(EXTRA, 0)
        items.append(("Milk", fmt(jars), "half-gallon jars (%s gal%s)" % (fmt(jars / 2), ", including %s extra" % fmt(ex) if ex else ""), "13pt"))
    for p in products:
        if p in (MILK, EXTRA) or not tot.get(p):
            continue
        items.append((p, fmt(tot[p]), (day.get("units") or {}).get(p, "") or next(
            (x.get("unit", "") for x in day["products"] if x["column"] == p), ""), "11pt"))
    for k, (item, qty, unit, size) in enumerate(items):
        z = "background-color:#FFF8E8;" if k % 2 else ""
        rows.append("<tr>%s%s%s%s</tr>" % (cell(ROW + z, BOXCHAR), cell(ROW + z, escape(item), "font-weight:bold;font-size:%s;" % size),
                                           cell(ROW + z, escape(qty), "font-weight:bold;font-size:%s;" % size), cell(ROW + z, escape(unit))))
        t.append("[ ] %s: %s %s" % (item, qty, unit))
    h.append('<table style="%s">%s</table>' % (TABLE, "".join(rows)))
    t.append("")

    h.append('<p style="%s">STOPS</p>' % H2)
    t.append("STOPS")
    heads = [("DONE", "7%"), ("STOP", "7%"), ("CUSTOMER", "27%"), ("DELIVER", "21%"), ("NOTES", "25%"), ("FLAGS", "13%")]
    rows = ["<tr>%s</tr>" % "".join(cell(HEAD + "border-bottom:1.2pt solid #270307;", x, "width:%s;" % w) for x, w in heads)]
    for k, s in enumerate(stops):
        z = "background-color:#DBDCC8;" if s["skip"] else ("background-color:#FFF8E8;" if k % 2 else "")
        addr = "%s, %s" % (s.get("address", ""), s.get("city", ""))
        cust = "<b>%s</b><br>%s, %s<br>%s" % (escape(s.get("name", "")), escape(s.get("address", "")), escape(s.get("city", "")), phones_html(s))
        if s["skip"]:
            deliv = "<b>SKIP: NO DELIVERY</b>"
        else:
            parts = []
            jars_s = s["milk"] * 2
            if s["milk"]:
                if jars_s.is_integer():
                    first_line = '<span style="font-size:13pt;font-weight:bold;">%s jar%s</span>' % (fmt(jars_s), "" if jars_s == 1 else "s")
                else:
                    first_line = '<span style="font-size:13pt;font-weight:bold;">%s gal</span>' % fmt(s["milk"])
                if s["extra"]:
                    first_line += " <b>+ %s extra</b>" % fmt(s["extra"])
                parts.append(first_line)
            elif s["extra"]:
                parts.append("<b>%s extra jar%s</b>" % (fmt(s["extra"]), "" if s["extra"] == 1 else "s"))
            if s["no_milk"]:
                parts.append("<b>NO MILK</b>")
            parts += ["%s x %s" % (fmt(v), escape(p)) for p, v in s["addons"]]
            parts += ["<b>%s</b>" % escape(o) for o in s["odd"]]
            deliv = "<br>".join(parts)
        rows.append("<tr>%s%s%s%s%s%s</tr>" % (
            cell(ROW + z, BOXCHAR),
            cell(ROW + z, escape(str(s.get("stop") or "?")), "font-size:15pt;font-weight:bold;text-align:center;"),
            cell(ROW + z, cust), cell(ROW + z, deliv),
            cell(ROW + z, escape(s.get("delivery_notes", "") or ""), "font-style:italic;"),
            cell(ROW + z, "<br>".join(escape(f) for f in s["flags"]), "font-weight:bold;")))
        t.append("[ ] Stop %s | %s | %s | %s | %s | %s | %s" % (s.get("stop") or "?", s.get("name", ""), addr, phones(s),
                                                             s["items"], s.get("delivery_notes", "") or "", " ".join(s["flags"])))
    h.append('<table style="%s">%s</table>' % (TABLE, "".join(rows)))
    t.append("")

    ch = []
    for s in stops:
        lines = real_changes(s)
        attn = (s.get("needs_attention") or "").strip()
        if lines or attn:
            ch.append((s, "; ".join(lines), attn))
    if ch:
        h.append('<p style="%s">CHANGES THIS WEEK</p>' % H2)
        t.append("CHANGES THIS WEEK")
        for s, lines, attn in ch:
            h.append('<p style="%s"><b>Stop %s · %s:</b> %s%s</p>' % (
                P, escape(str(s.get("stop") or "?")), escape(s.get("name", "")), escape(lines),
                ("; " if lines else "") + "<b>%s</b>" % escape(attn) if attn else ""))
            t.append("Stop %s %s: %s%s" % (s.get("stop") or "?", s.get("name", ""), lines, ("; " if lines else "") + attn if attn else ""))
        t.append("")
    return h, t


def build(day):
    products, stops = analyse(day)
    routes = []
    for s in stops:
        r = (s.get("route") or "").strip()
        if r not in routes:
            routes.append(r)
    if not routes:
        routes = [""]
    html, text = [], []
    for k, r in enumerate(routes):
        h, t = section(day, r, [s for s in stops if (s.get("route") or "").strip() == r], products, k == 0)
        html += h
        text += t
    pending = day.get("pending") or []
    if pending:
        html.append('<p style="%s">PENDING: NOT PACKED (Mark hasn\'t decided; don\'t pack unless he says so)</p>' % H2)
        text += ["PENDING (not packed)", "Mark hasn't decided; don't pack unless he says so."]
        for p in pending:
            line = "%s: %s" % (p.get("customer", ""), p.get("asked_for", ""))
            html.append('<p style="%s">%s</p>' % (P, escape(line)))
            text.append(line)
    doc = '<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>%s</title></head><body>\n%s\n</body></html>\n' % (
        escape("Delivery list %s" % day["date"]), "\n".join(html))
    deliver = sum(1 for s in stops if not s["skip"])
    skipping = sum(1 for s in stops if s["skip"])
    guesses = sum(1 for s in stops if "GUESS" in s["flags"])
    named = [r for r in routes if r]
    route_txt = ", ".join(named) if named else "1 route"
    message = "%s's delivery list is ready: {LINK}. %d stops to deliver, %s. %d skipping (boxed at the top). %d guesses marked. " \
              "Shares and orders for %s are now locked." % (day["day"], deliver, route_txt, skipping, guesses, day["day"])
    summary = {"stops_to_deliver": deliver, "skipping": skipping, "guesses": guesses, "routes": routes,
               "rows_read": len(day["rows"]), "milk_jars": sum(s["milk"] * 2 + s["extra"] for s in stops),
               "flags": {s.get("name", ""): s["flags"] for s in stops if s["flags"]}, "message": message}
    return doc, "\n".join(text).rstrip() + "\n", summary


def main():
    if len(sys.argv) != 3:
        print(json.dumps({"error": "usage: delivery_list_html.py day.json list.html"}))
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            day = json.load(f)
        doc, text, summary = build(day)
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write(doc)
        txt = re.sub(r"\.html?$", "", sys.argv[2]) + ".txt"
        with open(txt, "w", encoding="utf-8") as f:
            f.write(text)
    except (KeyError, ValueError, TypeError, OSError) as e:
        print(json.dumps({"error": "%s: %s" % (type(e).__name__, e)}))
        return 1
    summary.update({"html": sys.argv[2], "text": txt})
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
