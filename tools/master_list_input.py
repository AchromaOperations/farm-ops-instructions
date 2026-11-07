#!/usr/bin/env python3
"""Build the master list input file from saved Google Sheets tool answers.

Usage (one command, no pipes):
  python3 -I ops/tools/master_list_input.py --out ml/master.json \
      --products ml/products.json --config ml/config.json \
      --week ml/week1.json --week ml/week2.json ...

Each input file is the JSON a Sheets get_values call returned, saved exactly as
it came back: {"range": "...", "values": [[...], ...]}. A chunk past the last
row has no "values" and is fine. A file may also hold a list of such answers,
or a bare list of rows. Week chunks are joined in the order given.

It finds everything by label (sheets-spec rule 1): the header block's "Week",
"Dates" and "Weekly master list last sent" in column A, the customer table's
"Cust ID" header row, the Products tab's "Column name", "Unit", "Weeks" and
"Active" columns, and Config "First weeks". It writes master.json in the form
master_list_pdf.py reads (tools/sample-master-list.json) and prints one line of
JSON: {"out", "rows", "first_row", "last_row", ...} or {"error": "..."}.
Never add up, round or fix anything here: the PDF script reports oddities.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime

MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}


def cell(x):
    """A sheet cell as the string the sheet shows. Nothing is ever None."""
    if x is None:
        return ""
    if isinstance(x, bool):
        return "TRUE" if x else "FALSE"
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    return str(x)


def rows_of(obj, path):
    """The rows inside one saved tool answer (or a list of them)."""
    if isinstance(obj, dict):
        if "values" in obj:
            v = obj["values"]
            if v is None:
                return []
            if not isinstance(v, list):
                raise ValueError('%s: "values" is not a list' % path)
            return [list(r) if isinstance(r, list) else [] for r in v]
        if "range" in obj:
            return []  # an empty chunk (past the last row)
        raise ValueError('%s has no "values" (save the tool answer exactly as it came back)' % path)
    if isinstance(obj, list):
        if obj and all(isinstance(x, dict) for x in obj):
            out = []
            for x in obj:
                out.extend(rows_of(x, path))
            return out
        return [list(r) if isinstance(r, list) else [] for r in obj]
    raise ValueError("%s: not a tool answer (expected {\"range\": ..., \"values\": [...]})" % path)


def load_rows(path):
    with open(path, encoding="utf-8") as f:
        text = f.read().strip()
    if not text:
        return []
    try:
        obj = json.loads(text)
    except ValueError:
        starts = [i for i in (text.find("{"), text.find("[")) if i >= 0]
        if not starts:
            raise ValueError("%s is not JSON" % path)
        try:
            obj = json.loads(text[min(starts):])
        except ValueError as e:
            raise ValueError("%s is not valid JSON (%s)" % (path, e))
    return [[cell(c) for c in r] for r in rows_of(obj, path)]


def header_value(rows, label):
    """Value next to a column-A label; None when the label isn't there."""
    for r in rows:
        if r and r[0].strip() == label:
            return r[1].strip() if len(r) > 1 else ""
    return None


def sunday_from_dates(s):
    """'Sun Nov 8 - Sat Nov 14 2026' or 'Sun Dec 27 2026 - Sat Jan 2 2027' -> that Sunday."""
    pairs = re.findall(r"([A-Z][a-z]{2})\.? (\d{1,2})(?:,? (\d{4}))?", s)
    years = re.findall(r"\b(20\d{2})\b", s)
    if not pairs or pairs[0][0] not in MONTHS or not years:
        raise ValueError('Dates "%s" not understood' % s)
    mon, day, yr = pairs[0]
    year = int(yr) if yr else int(years[-1])
    if not yr and len(pairs) > 1 and pairs[1][0] in MONTHS and MONTHS[mon] > MONTHS[pairs[1][0]]:
        year -= 1  # the week starts in December and ends in January
    d = date(year, MONTHS[mon], int(day))
    if d.weekday() != 6:
        raise ValueError('Dates "%s": %s is not a Sunday' % (s, d.isoformat()))
    return d


def eastern_now():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M")
    except Exception:
        out = subprocess.run(["date", "+%Y-%m-%d %H:%M"], capture_output=True, text=True,
                             env={"TZ": "America/New_York", "PATH": "/usr/bin:/bin"})
        return out.stdout.strip()


def build(week_rows, product_rows, config_rows, now):
    notes = []
    # Header block and customer table header
    head = None
    for i, r in enumerate(week_rows):
        if r and r[0].strip() == "Cust ID":
            head = i
            break
    if head is None:
        raise ValueError('no "Cust ID" header row in the week chunks (a chunk is missing or saved short)')
    above = [r[0] for r in week_rows[:head] if r and re.match(r"^[CT]\d{3}$", r[0].strip())]
    if above:
        raise ValueError("customer rows (%s ...) come before the Cust ID header: the week chunks are out of order" % above[0])
    block = week_rows[:head]
    week = header_value(block, "Week")
    dates = header_value(block, "Dates")
    if week is None or dates is None or not dates:
        raise ValueError('header block has no "Week" or "Dates" label (is ml/week1.json the top of the tab?)')
    last_sent = header_value(block, "Weekly master list last sent")
    if last_sent is None:
        notes.append('Tab has no "Weekly master list last sent" label: treated as never sent.')
        last_sent = ""
    sunday = sunday_from_dates(dates)
    monday = date.fromordinal(sunday.toordinal() + 1)

    # Products
    if not product_rows:
        raise ValueError("Products file has no rows")
    ph = [c.strip() for c in product_rows[0]]
    pidx = {c: i for i, c in enumerate(ph)}
    for need in ("Column name", "Active"):
        if need not in pidx:
            raise ValueError('Products header has no "%s" column' % need)
    for opt in ("Unit", "Weeks"):
        if opt not in pidx:
            notes.append('Products header has no "%s" column: left blank.' % opt)

    def pcell(r, name):
        i = pidx.get(name)
        return r[i].strip() if i is not None and i < len(r) else ""

    products = []
    for r in product_rows[1:]:
        if pcell(r, "Active").lower() != "yes":
            continue
        col = pcell(r, "Column name")
        if not col:
            notes.append("An Active product row has no Column name: left out.")
            continue
        products.append({"column": col, "unit": pcell(r, "Unit"), "weeks": pcell(r, "Weeks") or "All"})
    if not products:
        raise ValueError("no Active product on the Products tab")

    # Config "First weeks"
    first_weeks = header_value(config_rows, "First weeks")
    if first_weeks is None:
        notes.append('Config has no "First weeks" label: first_week set to false.')
        first_week = False
    else:
        listed = [x.strip() for x in first_weeks.split(";") if x.strip()]
        first_week = sunday.isoformat() in listed

    # Customer table
    cols = [c.strip() for c in week_rows[head]]
    cidx = {}
    for i, c in enumerate(cols):
        cidx.setdefault(c, i)  # the first of a duplicated header wins
    for need in ("Cust ID", "Name", "Day", "Changes"):
        if need not in cidx:
            raise ValueError('customer table header has no "%s" column' % need)
    missing = [p["column"] for p in products if p["column"] not in cidx]
    if missing:
        notes.append("Week tab has no column for %d product%s (%s): blank for every row; the PDF says so too."
                     % (len(missing), "" if len(missing) == 1 else "s", ", ".join(missing)))
    out_cols = ["Cust ID", "Name", "Day"] + [p["column"] for p in products] + ["Changes"]

    def wcell(r, name):
        i = cidx.get(name)
        return r[i] if i is not None and i < len(r) else ""

    rows = []
    for r in week_rows[head + 1:]:
        cid, name = wcell(r, "Cust ID").strip(), wcell(r, "Name").strip()
        if not cid and not name:
            continue
        rows.append([wcell(r, c) for c in out_cols])
    if not rows:
        raise ValueError("no customer rows under the Cust ID header (a chunk is missing)")

    data = {
        "farm": "Restoration Farmstead",
        "week": int(week) if week.isdigit() else week,
        "monday": monday.isoformat(),
        "now": now,
        "last_sent": last_sent,
        "first_week": first_week,
        "products": products,
        "columns": out_cols,
        "rows": rows,
    }
    report = {
        "rows": len(rows),
        "first_row": " ".join(x for x in rows[0][:2] if x),
        "last_row": " ".join(x for x in rows[-1][:2] if x),
        "week": data["week"], "sunday": sunday.isoformat(), "monday": data["monday"],
        "first_week": first_week, "last_sent": last_sent, "now": now,
        "products": len(products), "missing_columns": missing, "notes": notes,
    }
    return data, report


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--out", required=True)
    ap.add_argument("--products", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--week", action="append", required=True)
    ap.add_argument("--now", default=None)
    try:
        a = ap.parse_args()
    except SystemExit:
        print(json.dumps({"error": "usage: master_list_input.py --out ml/master.json --products ml/products.json --config ml/config.json --week ml/week1.json [--week ml/week2.json ...]"}))
        return 2
    try:
        week_rows = []
        for p in a.week:
            week_rows.extend(load_rows(p))
        product_rows = load_rows(a.products)
        config_rows = load_rows(a.config)
        now = a.now or eastern_now()
        if not re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$", now):
            raise ValueError('now "%s" is not yyyy-mm-dd hh:mm' % now)
        data, report = build(week_rows, product_rows, config_rows, now)
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
    except Exception as e:
        print(json.dumps({"error": "%s: %s" % (type(e).__name__, e)}))
        return 1
    report["out"] = a.out
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
