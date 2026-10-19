MANUAL EDITS (version 3)
Written for: sheets-spec version 4

WHO THIS IS FOR
Any chat on the farm's Claude account (not the Farm ops routine) that reads or changes the Google Sheets "Farm Reference" or "Weekly Deliveries", usually because Shane, Mark or Laura asked. The routine has its own rules. In a chat, follow these.

FIRST
1. Fetch and read these, from the same place as this file (https://raw.githubusercontent.com/AchromaOperations/farm-ops-instructions/main/instructions/[name]):
   - sheets-spec.md: GENERAL RULES, and the layout of the tab you'll touch.
   - week-names.md: which tab is THIS, NEXT and LAST week.
   - For an order or a command: parser.md, only the sections ORDER WRITING and A4 (Commands).
   If you can't fetch them, change nothing and say so.
2. Times: Eastern, written yyyy-mm-dd hh:mm. If you don't know the exact time now, ask.

READING THE SHEETS
- Read each tab's whole header row and find every column by its name. Week tabs have about 35 columns, and columns added later sit at the far right (Extra Milk is one of them). Never read a fixed range such as A:Z and decide a column is missing.
- Find customers by name. A request may misspell one ("Carli" for "Cayli"): if exactly one customer is a close match, use it and say which; if several could be, ask.

BEFORE CHANGING AN ORDER
- Read that customer's row on the target week tab (ORDER WRITING rule 5 says which week), including its Changes cell.
- If the change is already there (the same product and amount for that week, recorded by the routine from the customer's own text or by someone else), don't add it again. Tell the person it's already in, when, and from where. If you can't tell whether they mean in addition to what's there, ask.
- If the row's Locked is filled, the list has gone out: don't change the row. Tell the person; a change after the list is Mark's call.

MAKING A CHANGE
- Follow ORDER WRITING (which row and week, product names and built-in defaults, Extra Milk in jars on that week's row only, never Milk (gal) or Customers for a one-week change, first-week-only products) and A4 for commands (skips, standing order changes, customer info). If a rule there says to ask Mark, ask the person you're talking to instead.
- Quantity cells hold the new total for the week. Append to Changes: "[yyyy-mm-dd hh:mm] [Column name] [old]>[new] ([who] (chat))", for example "2026-10-18 09:40 Eggs 0>1 (Shane (chat))".
- No charge (free items: "no charge", "free", "comp", "on the house", "sample"): write the item as an order if it isn't on the row yet, then append "[Column name] x[n] ([who] (chat))" to that row's "No charge" column (sheets-spec). If the tab has no "No charge" column, add it at the end of the header row (sheets-spec rule 8). Don't write "NO CHARGE" anywhere else; invoicing reads only that column.
- Don't set "Confirm needed" (no read-back text to the customer) unless the person asks for the customer to get one.
- After writing, read the cells back. If one didn't land right, fix it once; if it's still wrong, tell the person.

NEVER
- Delete rows, tabs or files. Rename, move or remove headers or labels.
- Change a filled STAMP cell, or edit or remove anything in a LOG cell (only append, to Changes and No charge).
- Edit the System, Queue, Inbox Log or Run History tabs: the routine owns them.
- Change prices, or run a sync.
- Send a text or message, unless the person asks for that exact message to that exact person.

FINISH
Say in one or two lines what changed (customer, week, cells, old > new), or why nothing changed.
