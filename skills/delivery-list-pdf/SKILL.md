---
name: delivery-list-pdf
description: Preview PDF of one day's Restoration Farmstead delivery list, built from the farm's Google Sheets by the farm-ops-instructions repository's own script. Use when someone asks for a delivery sheet, delivery list, route sheet or packing list for a day ("Monday delivery sheet in pdf", "create delivery list for Thursday", "what's going out tomorrow"). Read-only. It never changes a sheet, texts anyone or saves anything to Drive.
---

DELIVERY LIST PDF (version 1)
Written for: daily-delivery-list version 17, sheets-spec version 4

WHO THIS IS FOR
A chat on the farm's Claude account, asked by Shane, Mark or Laura for one day's delivery list.

WHAT IT MAKES, AND WHAT IT IS NOT
The same PDF the Farm ops routine makes, built by the repository's script from the same sheet data, handed to the person in this chat. It is a PREVIEW. The official list is made and sent by the routine the evening before (Config "Delivery list time" is 19:00, so the 7:17pm run; the link reaches the family group and the drivers (Harry and Zi) about 7:25pm), and that is the moment the day's orders lock. Two official lists for one day would conflict, so this skill never writes a cell, never texts, and never saves to Drive.

STEP 1. GET THE INSTRUCTIONS WITH GIT (first, before anything else)
Run these two commands in the chat's sandbox:
    rm -rf ops
    git clone --depth 1 https://github.com/AchromaOperations/farm-ops-instructions.git ops
Check: `head -1 ops/instructions/sheets-spec.md` must print "SHEETS SPEC (version 4)" and `ls ops/tools/delivery_list_pdf.py` must find the script.
- The repository is public; git needs no sign-in. Never add a GitHub repository or connector to the chat, and never sign the farm account in to GitHub.
- Don't use curl or wget for GitHub, and don't fetch the files one by one with the web tool: the web tool opens only links that already appear in the conversation and refuses links it assembled itself (that is what stopped a chat on 2026-11-08), and a script copied through it can't be trusted to be byte-exact.
- If git fails: try the clone once more, then stop. Say what git printed. Without the clone there is no script, and the list is never laid out by hand (see NEVER). The official list still comes from the routine at 7:17pm.

STEP 2. READ, FROM THE CLONE
- ops/instructions/daily-delivery-list.md: the authority. Step 4.1 is the exact form of day.json; WHAT THE SCRIPT MAKES is the design (the script decides it, never you).
- ops/instructions/week-names.md: how week tabs are named and which one holds a date.
- ops/instructions/sheets-spec.md: GENERAL RULES, the Customers, Products and Routes tabs, the week tab's customer table, TERMS.
- ops/instructions/manual-edits.md: the rules for any chat that reads the sheets (whole header rows, columns by name).
- ops/tools/sample-delivery-day.json: the input form.

STEP 3. WHICH DAY, WHICH TAB
- Time is Eastern: `TZ=America/New_York date`.
- The day = the date they named; otherwise the next date that falls on the weekday they named, today included. Deliveries are Monday to Friday; for Saturday or Sunday, say there is no delivery that day and stop.
- The tab = the Weekly Deliveries tab whose Sunday-to-Saturday dates include that day (week-names.md gives the names, for example "Delivery week 5 Nov 8-14 2026").

STEP 4. IS THE OFFICIAL LIST ALREADY OUT?
Search Drive for the exact name "Delivery list [Ddd Mon D YYYY].pdf" (for example "Delivery list Mon Nov 9 2026.pdf") and for a Google Doc "Delivery list [Ddd Mon D YYYY]" (the routine's fallback). If either exists, it is the official list and the day is locked: give its link, https://drive.google.com/file/d/[file ID]/view, and stop. Make a preview anyway only if the person says they want one knowing the official list is out, and say in the summary that the official list is the one the drivers have.

STEP 5. READ THE DATA (nothing is written)
- Find the workbooks as sheets-spec rule 5 says: a Drive search for the Google Sheet named exactly "Farm Reference" (its Config A1 reads "RF-OPS REFERENCE v1") and, in the same folder, "Weekly Deliveries". Exactly one of each; if not, stop and say so.
- Read each tab's whole header row and find every column by its name. Week tabs have 28 to 50 columns, and Extra Milk and the baked goods sit at the far right. Never read a fixed range such as A:Z and decide a column is missing.
- Read the week tab's whole customer table (from the "Cust ID" header row down), and Customers, Products, Routes and Queue in Farm Reference.
- Day rows, the routine's own rule (daily-delivery-list.md HOW TO WORK): for a week row whose Locked is blank, take Day, Route and Stop # from the Customers tab (the week row's copies may be stale; the routine refreshes them at lock). For a locked row, use the week row. Day rows = rows whose Day is that weekday, leaving out every Cust ID that starts with "T" (test customers).
- Count the Day rows. You will check this count twice.

STEP 6. BUILD day.json, EXACTLY AS STEP 4.1 SAYS
Make a new empty folder `dl` and write `dl/day.json` in the form of ops/tools/sample-delivery-day.json, following daily-delivery-list.md Step 4.1 field by field ("farm", "day", "date", "drivers" from Routes, "products" from Products rows with Active = Yes in Products order, "rows", "pending" from open Late order Queue items for that day). Two differences for a preview:
- "locked_at": "NOT YET (PREVIEW)" (the routine writes its lock time here; the header then reads "Locked NOT YET (PREVIEW)").
- "made": the Eastern time now, written like "Nov 8 6:40PM".
Settle nothing: the routine's Step 2 (guessing the first choice of an open Clarify item at lock) is not yours. Leave such a row as it reads; its Needs attention text shows on the list as a flag.
Copy every value exactly as the cell reads, "" for a blank. Never add, round or fix anything. Check that "rows" has the Day-row count before running.

STEP 7. RUN THE SCRIPT (it makes the list; never lay it out yourself)
    python3 -I ops/tools/delivery_list_pdf.py dl/day.json "dl/Delivery list [Ddd Mon D YYYY] PREVIEW.pdf"
It prints one line of JSON. "rows_read" must equal your Day-row count. If it prints "error", or the count differs, fix dl/day.json and run it once more. If it still fails, stop and quote what it printed. It also writes a "-no-links" copy and two .b64 files; ignore them (they are for the routine's upload).

STEP 8. CHECK AND HAND OVER
- If `pdftoppm` exists in the sandbox, render page 1 (`pdftoppm -r 50 -png -f 1 -l 1 "[pdf]" dl/page`) and look at it. Otherwise rely on the script's JSON.
- Compare the script's "stops_to_deliver", "skipping" and "guesses" with your own count from the sheet. Milk is counted in half-gallon jars (gallons x 2, plus Extra Milk jars; sheets-spec TERMS). Report jars, never gallons.
- Give the person the PDF file itself, the way this chat hands over files (its file-sending tool or outputs folder). Not a Drive link: nothing goes to Drive.
- Close with one or two lines: stops per route, jars, skips, flags (GUESS, CHECK, blank Stop #), open Late orders, and anything that didn't match (a day row with no Stop #, a customer with no Day, a Clarify item still open). Say it is a preview and when the official list comes if it isn't out yet.

NEVER
- Write any cell (no Locked, no "Delivery list sent", no Changes), create or edit any Drive file or Google Doc, text or message anyone.
- Save a list into Delivery Lists or Master Lists: the routine treats a file there as the official list and would send it.
- Lay out a list by hand, from memory, in HTML, or with any tool other than ops/tools/delivery_list_pdf.py. If the script can't run, there is no list from this chat.
- Fetch repository files with curl, wget or the web tool, or add a GitHub repository or connector.
- Rebuild a list that already exists in Delivery Lists, except as Step 4 allows.

IF SOMETHING FAILS
One line: which step, which tool, what it said. No more than one retry per step. The official list still comes from the routine at 7:17pm the evening before; if it is later than that and nothing is in Delivery Lists, say so and tell Shane (the routine texts him as well).
