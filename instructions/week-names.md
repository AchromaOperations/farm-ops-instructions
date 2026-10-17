WEEK NAMES (version 1)
Written for: sheets-spec version 4

The only place these rules live. sheets-spec and every step doc point here. The operator reads this small file every run instead of the whole sheets-spec.

WEEK NAMES (every step uses these)
- THIS week = the tab whose Sunday-to-Saturday dates include today. Before Week 1 starts (before Sun Oct 11 2026) there is no THIS week; that is normal, not missing.
- NEXT week = the tab whose Sunday is the first Sunday after today. (On Fri Oct 9 2026, NEXT week is Week 1.)
- LAST week = the tab whose Saturday is the last Saturday before today (none before Week 1).
- Whenever a skill says "this week's row" and there is no THIS week, use NEXT week's row.
Tab names:
- Same month: "Delivery week 1 Oct 11-17 2026"
- Two months: "Delivery week 3 Oct 25-31 2026", "Delivery week 4 Nov 1-7 2026", "Delivery week 8 Nov 29-Dec 5 2026"
- Two years: "Delivery week 12 Dec 27 2026-Jan 2 2027"

MISSING WEEK TABS
- The operator builds missing tabs first (sheets-spec BUILDING A WEEK TAB). If NEXT week's tab still can't be found, or THIS week's tab can't be found on or after Sun Oct 11 2026, add "Week tab missing: [name]" to "Missing doc alerts" handling (text Shane once per day) and skip every step that needs that tab.
