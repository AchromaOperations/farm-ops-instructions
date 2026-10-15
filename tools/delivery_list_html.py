#!/usr/bin/env python3
"""Delivery list Google Doc for one delivery day, as fixed HTML.

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
P = FONT + "font-size:12pt;margin:0 0 4pt 0;"
H1 = FONT + "font-size:22pt;font-weight:bold;margin:0 0 10pt 0;"
H2 = FONT + "font-size:15pt;font-weight:bold;margin:16pt 0 6pt 0;"
TABLE = "border-collapse:collapse;width:100%;"
TH = FONT + "font-size:11pt;font-weight:bold;border:1pt solid #000000;padding:4pt 6pt;background-color:#E6E6E6;text-align:left;vertical-align:top;"
TD = FONT + "font-size:12pt;border:1pt solid #000000;padding:4pt 6pt;vertical-align:top;"
BOX = FONT + "font-size:13pt;border:3pt solid #000000;padding:8pt 10pt;"


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
        stops.append(dict(r, q=q, milk=milk, extra=extra, skip=skip, no_milk=no_milk, flags=flags, items=items))
    stops.sort(key=stop_key)
    return products, stops


def totals_for(stops):
    t = {}
    for s in stops:
        for p, v in s["q"].items():
            t[p] = t.get(p, 0) + v
    return t


def section(day, route, stops, products, first):
    d = datetime.strptime(day["date"], "%Y-%m-%d")
    drivers = day.get("drivers") or {}
    driver = drivers.get(route) or day.get("driver") or "(not set)"
    title = "%s - %s, %s %d %d - Driver: %s" % (route or day["day"], d.strftime("%a"), d.strftime("%b"), d.day, d.year, driver)
    h, t = [], []
    if not first:
        h.append('<p style="page-break-before:always;%s"></p>' % P)
    h.append('<p style="%s">%s</p>' % (H1, escape(title)))
    t.append(title.upper())
    t.append("")

    skips = [s for s in stops if s["skip"]]
    nomilk = [s for s in stops if s["no_milk"]]
    box = []
    if skips:
        box.append('<p style="%sfont-size:14pt;font-weight:bold;margin:0 0 4pt 0;">SKIPS: DO NOT DELIVER</p>' % FONT)
        t.append("#### SKIPS: DO NOT DELIVER ####")
        for s in skips:
            line = "Stop %s: %s, %s, %s: SKIP, nothing to deliver this week" % (
                s.get("stop") or "?", s.get("name", ""), s.get("address", ""), s.get("city", ""))
            box.append('<p style="%s">%s</p>' % (P, escape(line)))
            t.append(line)
    if nomilk:
        box.append('<p style="%sfont-size:14pt;font-weight:bold;margin:8pt 0 4pt 0;">NO MILK THIS WEEK</p>' % FONT)
        t.append("#### NO MILK THIS WEEK ####")
        for s in nomilk:
            line = "Stop %s: %s: NO MILK, add-ons only" % (s.get("stop") or "?", s.get("name", ""))
            box.append('<p style="%s">%s</p>' % (P, escape(line)))
            t.append(line)
    if not box:
        box.append('<p style="%sfont-weight:bold;">No skips this week</p>' % P)
        t.append("No skips this week")
    h.append('<table style="%s"><tr><td style="%s">%s</td></tr></table>' % (TABLE, BOX, "".join(box)))
    t.append("")

    tot = totals_for(stops)
    h.append('<p style="%s">PACKING LIST</p>' % H2)
    t.append("PACKING LIST")
    rows = ['<tr><th style="%s">Product</th><th style="%s">Total for this route</th></tr>' % (TH, TH)]
    jars = tot.get(MILK, 0) * 2 + tot.get(EXTRA, 0)
    if jars:
        ex = tot.get(EXTRA, 0)
        val = "%s half-gallon jars (%s gal)%s" % (fmt(jars), fmt(jars / 2), ", including %s extra" % fmt(ex) if ex else "")
        rows.append('<tr><td style="%sfont-weight:bold;">Milk</td><td style="%sfont-weight:bold;">%s</td></tr>' % (TD, TD, escape(val)))
        t.append("Milk: " + val)
    for p in products:
        if p in (MILK, EXTRA) or not tot.get(p):
            continue
        rows.append('<tr><td style="%s">%s</td><td style="%s">%s</td></tr>' % (TD, escape(p), TD, fmt(tot[p])))
        t.append("%s: %s" % (p, fmt(tot[p])))
    h.append('<table style="%s">%s</table>' % (TABLE, "".join(rows)))
    t.append("")

    h.append('<p style="%s">STOPS</p>' % H2)
    t.append("STOPS")
    heads = ["Stop #", "Name", "Address, City, Phone", "Items", "Delivery notes", "Flags"]
    widths = ["7%", "17%", "24%", "24%", "18%", "10%"]
    rows = ["<tr>%s</tr>" % "".join('<th style="%swidth:%s;">%s</th>' % (TH, w, x) for x, w in zip(heads, widths))]
    for s in stops:
        fill = "background-color:#D9D9D9;" if s["skip"] else ""
        addr = "%s, %s" % (s.get("address", ""), s.get("city", ""))
        cells = [
            '<td style="%s%sfont-size:16pt;font-weight:bold;">%s</td>' % (TD, fill, escape(str(s.get("stop") or "?"))),
            '<td style="%s%sfont-weight:bold;">%s</td>' % (TD, fill, escape(s.get("name", ""))),
            '<td style="%s%s">%s<br>%s</td>' % (TD, fill, escape(addr), phones_html(s)),
            '<td style="%s%s%s">%s</td>' % (TD, fill, "font-weight:bold;" if s["skip"] or s["no_milk"] else "", escape(s["items"])),
            '<td style="%s%s">%s</td>' % (TD, fill, escape(s.get("delivery_notes", "") or "")),
            '<td style="%s%sfont-weight:bold;">%s</td>' % (TD, fill, "<br>".join(escape(f) for f in s["flags"])),
        ]
        rows.append("<tr>%s</tr>" % "".join(cells))
        t.append("Stop %s | %s | %s | %s | %s | %s | %s" % (s.get("stop") or "?", s.get("name", ""), addr, phones(s),
                                                         s["items"], s.get("delivery_notes", "") or "", " ".join(s["flags"])))
    h.append('<table style="%s">%s</table>' % (TABLE, "".join(rows)))
    t.append("")

    ch = []
    for s in stops:
        lines = real_changes(s)
        attn = (s.get("needs_attention") or "").strip()
        if lines or attn:
            ch.append("%s: %s" % (s.get("name", ""), "; ".join(lines + ([attn] if attn else []))))
    h.append('<p style="%s">CHANGES THIS WEEK</p>' % H2)
    t.append("CHANGES THIS WEEK")
    for c in ch or ["No changes this week."]:
        h.append('<p style="%s">%s</p>' % (P, escape(c)))
        t.append(c)
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
        html.append('<p style="%s">PENDING (not packed)</p>' % H2)
        html.append('<p style="%sfont-weight:bold;">Mark hasn\'t decided; don\'t pack unless he says so.</p>' % P)
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
