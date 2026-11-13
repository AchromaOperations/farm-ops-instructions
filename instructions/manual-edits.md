MANUAL EDITS (version 7)
Written for: sheets-spec version 4

WHO THIS IS FOR
Any chat on the farm's Claude account (not the Farm ops routine) that reads or changes the Google Sheets "Farm Reference" or "Weekly Deliveries", usually because Shane, Mark or Laura asked. The routine has its own rules. In a chat, follow these.
WHO YOU ARE TALKING TO: the person in a farm-account chat is Laura unless they say they are Shane or Mark (Shane's rule, 2026-11-08). "[who]" in every tag below is that name, so the default tag is "(Laura (chat))". Don't ask who they are; if they say, use that name for the rest of the chat.

FIRST
1. Fetch and read these (each link is written out in full on purpose: a chat's web tool opens only links that already appear in the conversation, and it refuses a link it assembled itself from a pattern; that is what stopped a chat on 2026-11-08). A skill that has already cloned the repository (skills/) reads the same files from its clone instead.
   - https://raw.githubusercontent.com/AchromaOperations/farm-ops-instructions/main/instructions/sheets-spec.md : GENERAL RULES, and the layout of the tab you'll touch.
   - https://raw.githubusercontent.com/AchromaOperations/farm-ops-instructions/main/instructions/week-names.md : which tab is THIS, NEXT and LAST week.
   - For an order or a command: https://raw.githubusercontent.com/AchromaOperations/farm-ops-instructions/main/instructions/parser.md , only the sections ORDER WRITING and A4 (Commands).
   If you can't fetch one, change nothing and say which link failed and what the tool said. Never rebuild a rule from memory.
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
- Quantity cells hold the new total for the week. Append to Changes: "[yyyy-mm-dd hh:mm] [Column name] [old]>[new] ([who] (chat))", for example "2026-10-18 09:40 Eggs 0>1 (Laura (chat))".
- No charge (free items: "no charge", "free", "comp", "on the house", "sample"): write the item as an order if it isn't on the row yet, then append "[Column name] x[n] ([who] (chat))" to that row's "No charge" column (sheets-spec). If the tab has no "No charge" column, add it at the end of the header row (sheets-spec rule 8). Don't write "NO CHARGE" anywhere else; invoicing reads only that column.
- Don't set "Confirm needed" (no read-back text to the customer) unless the person asks for the customer to get one.
- After writing, read the cells back. If one didn't land right, fix it once; if it's still wrong, tell the person.

CLOSING A QUEUE ITEM BY HAND (only when the person says they are Shane; Shane's rule, 2026-11-13)
The Queue is the routine's. Mark and Laura close a digest question by answering it in the family group ("2 resolved"); Shane isn't in that group and his texts are logged only, so a stuck question (settled some other way, or not needed any more) is closed for him here. Only these cells (sheets-spec rule 2 names them as a Queue row's TRACKER cells; Digest # is one too), and nothing else:
- Find the row by the Q# he gives, or by the customer and the digest number he quotes. If more than one open row fits, ask. The row must have Status Waiting, Sent or Answered; never touch a row that is already Resolved, and never a reply (Question starting "REPLY: ").
- Write: Answer = "closed by hand: [his reason] (Shane (chat))" (if Answer already has text, add it after " ; "), Answered by = "Shane (chat)", Status = Resolved, Resolved = now, Outcome = Resolved (Sales items only), Digest # = blank.
- Never add or delete rows, and change no other cell. Mark and Laura don't hear about it: the question just leaves the next digest.
- Closing a question fixes nothing else. An "Unpaid 14+ days" question closed here leaves the invoice counted as unpaid until its row's Paid is filled (next section).

INVOICE CANCELED OR DELETED IN SQUARE (only when the person says they are Shane; Shane's rule, 2026-11-13)
The routine's payment check (invoicing Part D) notices an invoice Square reports canceled and asks Mark and Laura about a replacement. When Square no longer returns the invoice at all, nothing is asked: the check runs again every day, and the row keeps counting as unpaid (it is listed on that customer's next pay-link text). When Shane says a sent invoice was canceled or deleted in Square and won't be replaced:
- Find the row: the customer, the week tab (the delivery date or "Invoice sent" date he gives), and the "Invoice link" if he names it. It must have "Invoice sent" filled and "Paid" blank; if not, change nothing and tell him what the row shows.
- Fill Paid = "none: invoice canceled (Shane (chat))" and add "invoice canceled in Square (Shane (chat), [yyyy-mm-dd hh:mm])" to Needs attention (after " ; " if it has text). That stops the daily check and keeps the invoice off the customer's next pay-link text.
- If he names a replacement invoice, don't do it here: leave the row alone and tell him the routine asks about replacements itself (invoicing Part D) when Square shows the old one canceled.
- Never clear or change a filled Paid, and never change "Invoice link", "Invoice sent" or "Pay link texted".

NEVER
- Delete rows, tabs or files. Rename, move or remove headers or labels.
- Change a filled STAMP cell, or edit or remove anything in a LOG cell (only append, to Changes and No charge).
- Edit the System, Queue, Inbox Log or Run History tabs: the routine owns them. One exception: CLOSING A QUEUE ITEM BY HAND above, when the person says they are Shane.
- Touch a day's "Invoice hold" (week tab day table) unless the person says they are Shane and asks for it. When he asks to hold a day: fill it as "[yyyy-mm-dd hh:mm] [reason] (Shane (chat))", or add that after " ; " if it's already filled. When he asks to lift it: clear the cell.
- Change prices, or run a sync.
- Send a text or message, unless the person asks for that exact message to that exact person.
- Save a delivery list or master list into the Delivery Lists or Master Lists folders, or make one by hand. The routine makes and sends those; a list made for a person in a chat is a preview that stays in the chat (skills/delivery-list-pdf/SKILL.md).

FINISH
Say in one or two lines what changed (customer, week, cells, old > new), or why nothing changed.
