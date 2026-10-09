FARM SETUP (version 4)
Written for: sheets-spec version 4

Change log
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v4 (2026-10-07): written for sheets-spec v4 (also creates Delivery Lists and Invoice Lists folders).
- v3 (2026-10-07): System tab labels per sheets-spec v3.
- v2 (2026-10-07): re-run safe customer matching; cursor only set when blank; dropdowns; Test phones by role; uses sheets-spec v2 names and formats.
- v1 (2026-10-07): first draft.

Purpose: build the Farm Reference and Weekly Deliveries workbooks described in the doc "sheets-spec", starting from the farm's existing customer sheet. Shane is in the chat with you. Confirm with Shane at every CHECKPOINT and wait for the answer before continuing.

Read "sheets-spec" (same folder) first. It is the source of truth for every tab, column and rule. Check that its version matches "Written for" above; if not, stop and tell Shane.

Safety
- Do not send any text messages. Do not reply to or change any Quo message.
- Do not edit or delete the old customer sheet. You may only move it into Archive, and only at Phase 6 after Shane says yes.
- Check before acting: if a file or tab already exists, use it. Never create duplicates. This whole doc is safe to run again; it picks up where it left off.

PHASE 1. Folders
- Find the Ops folder (Shane names it in the setup chat). Inside it, find or create "Archive", "Delivery Lists" and "Invoice Lists".
- Report what existed and what you created.

PHASE 2. Find the current customer sheet
- Search Google Drive for spreadsheets that look like the delivery master: a name containing "Milk", "Delivery", "Master" or "Customer", or a first row containing headers like Name, Day, Gallons, Phone, Address. Ignore anything inside the Ops folder.
- List every candidate, numbered, with: name, owner, last edited, tab names, number of rows, and its header row.
- CHECKPOINT: Shane picks one by number.
- Read it. Propose how each of its columns maps to the Customers columns and product columns in sheets-spec. List any of its columns that don't map anywhere.
- CHECKPOINT: Shane confirms or corrects the mapping.

PHASE 3. Build Farm Reference
If a Google Sheet named "Farm Reference" already exists in the Ops folder, use it and only add what's missing.
Otherwise create it in the Ops folder with tabs, in this order: Customers, Products, Routes, Config, Defaults, Queue, Inbox Log, System. Use the exact headers from sheets-spec.

Products tab:
- One row per product column in the old sheet. Milk is "Milk (gal)", Billed through = Squarespace. Every other product: Billed through = Square, Price blank, Active = Yes.
- If an old column mixes several items (for example "Baked Goods/Other"), make one row for it and write "split into real products" in Notes.

Customers tab:
- One row per customer from the old sheet, sorted by Day (Monday to Friday) then Stop #.
- Re-run safety: before adding a customer, check whether they are already on the tab (same phone, or same name if there's no phone). If so, skip them. Never renumber existing customers.
- Cust IDs C001, C002, ... in that order. New ones continue after the highest existing ID.
- Status = Active for everyone.
- Phones in +1XXXXXXXXXX form. If a phone can't be read with confidence, leave it blank and note the original in Notes.
- Standing orders: copy only the milk amount into "Milk (gal)". Leave every add-on column blank. List every add-on standing order you dropped (customer + what it said) for Shane.
- Route: copy it if the old sheet has it. Otherwise leave blank.

Routes tab: one row per route found in the old sheet. If none, one row per weekday (Monday to Friday) with Driver blank.

Config tab: A1 = RF-OPS REFERENCE v1, then the settings from sheets-spec with their starting values. For the phones:
- Farm Quo number: look it up (list Quo inboxes).
- CHECKPOINT: ask Shane for Mark's, Laura's, Harry's and Shane's cell numbers. Fill them in. Test phones stays as the list of roles.

System tab: create every label listed in sheets-spec. If Message cursor is blank, set it to the current date-time (so the parser never processes old history). If it already has a value, leave it alone. All other System values blank. Run history header below them.

Defaults, Queue, Inbox Log: headers only.

Dropdowns: add data-validation dropdowns everywhere sheets-spec says "(dropdown)", with exactly the listed values. If you can't add dropdowns with your tools, list which ones are missing so Shane can add them by hand.

Read back and report: number of customers per day, number of products, anything left blank that needs a human (phones, routes, prices), and the dropped add-on standing orders.
- CHECKPOINT: Shane looks at Farm Reference and says it's right (or what to fix).

PHASE 4. Build Weekly Deliveries
If a Google Sheet named "Weekly Deliveries" already exists in the Ops folder, use it. Otherwise create it there.
Create week tabs as described in sheets-spec, starting with Delivery week 1 (Sun Oct 11 2026), through the week containing Jan 31 2028.
For each tab:
- Skip it if a tab with that name already exists.
- Tab name: follow the naming rules in sheets-spec (including weeks that cross a month or a year).
- Header block: Week, Dates, Asked-for order cutoff (the Saturday before the week, at the Config time). Every other value blank.
- Day table: Monday to Friday rows, all blank.
- Customer table: every Active customer, sorted by Day, Route, Stop #. Product quantities = their standing orders. All status columns blank.
Work in batches of 10 tabs. After each batch, report how many are done. If the chat is getting long or a tool starts failing, stop after the current batch and tell Shane: "Start a new chat and paste the setup starter prompt again; I'll continue from week N."
- CHECKPOINT after the first batch: Shane opens Delivery week 1 and confirms the layout before you build the rest.

PHASE 5. Record links
Write the IDs of Farm Reference and Weekly Deliveries into Config.

PHASE 6. Archive the old sheet
- CHECKPOINT: ask Shane "Move [old sheet name] into Archive now?" Only on yes, move it. Do not change its contents or sharing.
- If you can't move files, tell Shane to drag it into Archive by hand.

PHASE 7. Final report
List: files created, customer count, products needing prices, phones or routes left blank, dropped add-on standing orders, week tabs created (first and last), and anything that failed.
