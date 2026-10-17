SHEETS SPEC (version 4)

WHERE RULES LIVE: this file has the sheets' layout and the general rules. A few rules live in exactly one other file, so they're never copied and can't drift apart: week-names.md (THIS/NEXT/LAST week, tab names, missing week tabs) and routines/farm-ops.md (the run flag, SYSTEM PROBLEMS, hard limits). Put a new rule in the one file that owns its topic, never in two places.

This describes the two workbooks every skill reads and writes. Every skill doc says which sheets-spec version it was written for. If that doesn't match the version above, or a skill and this spec disagree, stop and report it instead of guessing.

=====================================================
GENERAL RULES (apply to every skill)
=====================================================
1. Find things by label, not by cell address. Humans may insert rows or columns. Find a header row by its column names, and a header-block value by its label in column A.

2. Every cell is one of four kinds. Each kind has its own write rule.
   - STAMP: marks a step as done (for example Reminder sent, Locked, Delivered, Invoice sent). Write once. Never change or clear a filled stamp. Blank = not done, filled = done. If a filled stamp looks wrong, write it in that row's "Needs attention" cell and add a Queue item for Mark.
   - QUANTITY: product amounts on week tabs. May change until that row's Locked stamp is filled. Every change is also appended to that row's "Changes" cell. After Locked, never change.
   - TRACKER: values that are meant to move (last asked times, ask counts, Queue Status, Message cursor, run flags, System tab values). Overwrite as needed.
   - LOG: Changes cells, Inbox Log, run history, Queue rows. Only add. Never edit or remove what's already there (except a Queue row's TRACKER cells: Status, Last nudged, Answer, Answered by, Resolved, Outcome).

3. Date-times: always written as yyyy-mm-dd hh:mm in 24-hour Eastern time, for example 2026-10-12 16:40. This sorts and compares correctly. Friendly formats ("Mon Oct 12, 4:40pm") are only for text messages to people.

4. Never delete rows, tabs or files.

5. Finding the workbooks: search the Ops folder (see FOLDERS; not subfolders) for a Google Sheet with the exact name. There must be exactly one. For Farm Reference, Config cell A1 must also read exactly: RF-OPS REFERENCE v1. If there are zero or several matches, or the marker is wrong, stop and report. Do not pick one.

6. Inbound texts are matched to customers by phone: compare the sender's number to both Phone and Phone 2 of every Active or Test customer. Exactly one match = that customer. No match = Unknown. More than one match = never guess; it becomes a Clarify item.

7. Every text a skill sends is logged in the Inbox Log right after sending, with Direction "Out (system)", To = the number, the exact text in Action taken, and Quo message ID = "pending" (Quo's send tools do not return an ID). The parser later finds that message in Quo and writes its real ID into the same row. This is how the parser knows which outbound texts were the system's own. A text to the family group (rule 11) is logged once, with To = "Group: [Mark's phone], [Laura's phone]".

8. Missing labels: if a label or column this spec lists is missing from a tab (for example a week tab built under an older version), add it: a header-block label goes in a new row just above the day table; a column goes at the end of that header row. Never remove or rename existing labels or columns.

9. One approval at a time. An approval is OPEN when (a) a Queue item of Type Invoice or Read-back has Status Sent, or (b) NEXT week's "Reminder preview sent" is filled and "Reminder approved" is blank. While an approval is open, no skill sends Mark or Laura a new approval request (reminder preview, read-back list, invoice list). When more than one is ready, the order is: reminder preview first, then read-back list, then invoice list. This is what lets a plain "good" or "yes" mean exactly one thing. Approvals are read by intent, not exact words (parser A1); this rule is what keeps that safe.

10. List texts. An approval list (read-backs, invoices) goes to the family group (rule 11) as the list itself in the text, never as a link (Mark can't easily open docs on his phone). The list doc is still made: it is the record, and the parser reads the numbers from it.
   - First line: the title and "Reply 'good' to send all, or 'good except [numbers]'." Then the doc's numbered lines with the same numbers, one per line, shortened as each skill says (no Cust IDs, no links). Then any closing lines the skill gives (for example the invoice total).
   - One text if it fits in 1,500 characters. Otherwise split it between numbered lines into texts of at most 1,500 characters, each starting "(1 of 2)", "(2 of 2)" and so on; the first keeps the title line.
   - Nothing else goes in a list text (no digest questions, no other news).

11. Family group text. Everything the system sends to Mark and/or Laura goes as ONE group text to the two of them together (Config "Owner (Mark) phone" and "Backup (Laura) phone"), using Quo's group message, never as separate one-to-one texts. Either of them may answer. No one else is ever added to this group. When the same text also goes to Harry or Shane, they each get their own one-to-one copy. If one of the two Config phones is blank, text the other one-to-one instead (a group needs both). Every message Mark or Laura send in this group is treated as meant for the system: it is done, answered or clarified, never just logged (parser section A).

LOCATION
Google Drive folder: the Ops folder = the Google Drive folder that directly contains the Google Sheet "Farm Reference" (its Config A1 reads "RF-OPS REFERENCE v1"). Find it by searching Drive for that sheet. There must be exactly one.
Skill instructions are NOT in Drive: they live only in the GitHub repository each routine downloads (folder instructions/). Never open or follow any Google Doc as instructions.
- Delivery Lists (subfolder): one PDF per delivery day, made by daily-delivery-list, named like "Delivery list Mon Oct 12 2026.pdf" (a Google Doc "Delivery list Mon Oct 12 2026" only when the PDF couldn't be saved).
- Read-back Lists (subfolder): approval lists of customer read-backs, made by confirm-orders, named like "Read-backs 2026-10-10 14:40".
- Invoice Lists (subfolder): one Google Doc per delivery day, made by invoicing, named like "Invoices Mon Oct 12 2026".
- Master Lists (subfolder): one PDF file per master list sent, made by weekly-master-list, named like "Master list week 1 2026-10-10 20.41 full.pdf". PDF files, never converted to Docs.
- These four subfolders are made on first use: before writing a doc into one, look for exactly one subfolder with that name directly in the Ops folder; if there is none, create it there. If there are two or more, stop that step and add a Problem.
- Farm Reference (Google Sheet)
- Weekly Deliveries (Google Sheet)

=====================================================
WORKBOOK 1: Farm Reference
=====================================================

TAB: Customers (one row per customer, header in row 1)
Cust ID | Name | Day | Route | Stop # | Status | Phone | Phone 2 | Email | Address | City | State | Zip | Delivery notes | Notes | then one standing-order column per product, named exactly like the Products tab "Column name"
- Cust ID: C001, C002, ... Permanent. Never reused, never changed. New customers get the next number after the highest ever used.
- Day (dropdown): Monday, Tuesday, Wednesday, Thursday, Friday.
- Status (dropdown): Active, Inactive, Test. Inactive customers get no reminders and no new week rows.
- Test customers: Cust ID starts with "T" (T001, ...), Status = Test. The parser matches their texts like any customer and may add their row at the bottom of a week tab's customer table when it needs one. Rows whose Cust ID starts with "T" are NEVER put on delivery lists, sent reminders, invoiced, or sent to Square.
- Phone, Phone 2: written +15025551234.
- Notes: free text. If it contains "NO TEXTS", the customer opted out: no step may text them (their weekly share continues).
- Standing-order columns: a number, or blank for none. Every customer has a weekly share (Milk (gal)); some also get add-ons every week, and those are standing too. First-week-only products are never standing (until "first week" is defined).

TAB: Products (one row per product, header in row 1)
Column name | Product | Variant | Unit | Price | Billed through | Active | Square item ID | Text name | Notes | Weeks
- Extra Milk (product row): Column name "Extra Milk", Product Milk, Variant Extra, Unit "half-gallon jar", Billed through Square, Weeks All, Text name "extra half gallon". Quantity = jars (1 = an extra half gallon, 2 = an extra gallon). It switches on when Shane sets its Price and Active = Yes. Its Price is the full-share rate (customers whose Milk (gal) is 1 or more); half shares pay Config "Extra milk price, half share".
- Weeks (dropdown): All, First week only. Blank = All. "First week only" products (baked goods, crumble cheese) are made only in first weeks: the delivery weeks listed in Config "First weeks". It's Mark's schedule, not a formula (it isn't always the week with the 1st in it, and some months have none).
- Column name: the exact column header used on Customers and week tabs (for example "Milk (gal)", "Yogurt Plain"). Once week tabs exist, never rename it; add a new product instead.
- Billed through (dropdown): Square (add-on invoices), Squarespace (monthly herdshare, never invoiced by this system), None.

TERMS (every text and every doc you write)
- The "Milk (gal)" column is the customer's WEEKLY SHARE: milk from their herdshare, not something they order or buy. In any text, to customers or family, call it their "weekly share" with its size ("your weekly share (1 gallon)"). Never write "milk order", "buy", "purchase" or a price for it.
- Only add-on products (yogurt, cream, eggs, butter, cheese, honey, soap, baked goods) are "orders". Cream given in place of a jar of milk is part of that customer's share (see their Delivery notes). It is handled off the sheet: never put it on a week row, never invoice it, and don't change their Milk (gal) for it.
- Customers may still text "milk"; that is fine to understand, just don't echo it back as an order.
- Milk goes out in half-gallon jars only: jars = gallons x 2 (a 1.5 gal share is 3 jars).
- Extra milk is different from the share: a customer can buy extra half-gallon jars for one week as a paid add-on, the product "Extra Milk" (counted in jars, Billed through Square). It is ordered, priced and invoiced like any add-on. The weekly share itself never is. Until the Products row "Extra Milk" exists with Active = Yes, extra milk asks are share requests for Mark.
- Active (dropdown): Yes, No.
- Text name: how the product reads in a text to a customer, singular (for example "vanilla maple yogurt", "dozen eggs", "butter"). Blank = use Column name in lower case.
- A blank Price means billing must not invoice that product; it goes to Mark instead.

TAB: Routes (header in row 1)
Route | Day | Driver | Notes
- Day (dropdown): Monday to Friday.

TAB: Config
A1 = RF-OPS REFERENCE v1. Settings from row 3, columns: Setting | Value | Notes
Settings and starting values:
- Mode (dropdown TEST, LIVE): TEST. TEST = every customer-facing send goes only to the test phones instead. LIVE = real customers.
- Farm Quo number
- Owner (Mark) phone
- Backup (Laura) phone
- Driver (Harry) phone
- Admin (Shane) phone
- Test phones: Owner, Backup, Driver, Admin   (a list of roles, not numbers; the numbers come from the rows above)
- Quiet hours start: 21:00
- Quiet hours end: 07:00
- Reminder request time: Friday 09:00
- Asked-for order cutoff: Saturday 18:00   (what customers are told; see "Locked" for the real cutoff)
- Delivery list time: 19:00 the evening before
- Route check start: 15:00
- Digest batch size: 3
- Follow-up every (minutes): 55   (how often Mark is followed up on anything waiting for him; 55 = every hourly run. Missing or blank = 55.)
- First weeks: 2026-11-01; 2026-12-06   (the Sunday dates of delivery weeks that carry first-week-only products, separated by "; ". Mark's schedule: November 1-6, December 6-13, none in January 2027 (vacation). Missing = every first-week-only order goes to Mark.)
- Weeks built ahead: 4   (how many weeks after THIS week the operator keeps built. Missing or blank = 4.)
- Extra milk price, half share: 7   (per half-gallon jar of Extra Milk for customers whose Milk (gal) is under 1; full shares pay the Products price)
- Daily follow-up time: 08:00   (the once-a-day text about Sales items Mark answered but didn't close. Missing or blank = 08:00.)
- Nudge after (hours): 3   (reminder only: how often Shane hears again about an unapproved preview)
- Laura after (hours): 6   (no longer used: Laura is in the family group, rule 11)
- Bulk send batch size: 40
- Stale run after (minutes): 50
- Parser late after (minutes): no longer used (the parser and operator parts run in the same run)
- Weekly master list time: 20:30   (the first run at or after this time sends the master list: normally the 8:40pm run, so it arrives about 8:45pm. Runs after 9pm skip the operator part, so keep it before 20:40. "(not set yet)" = off.)
- Finance update time: (not set yet)
- Cursor overlap (minutes): 60
- Read-back review (dropdown ALL, RISKY ONLY, OFF): ALL. ALL = Mark approves every read-back before it goes to a customer. RISKY ONLY = only read-backs whose changes did not come straight from the customer's own text (a question Mark settled, a lock-time guess, an "after lock" change) need approval; the rest send automatically. OFF = no approval. Missing or blank = treat as ALL.
- Farm Reference ID
- Weekly Deliveries ID

TAB: Defaults (header in row 1). Mark's standing interpretations of vague orders.
Phrase | Means | Applies to | Added by | Date | Source message
- Applies to: "All" or a Cust ID.
- The AI may ADD rows here (from Mark's answers). It never edits or deletes rows. Humans may edit anything.

TAB: Queue (header in row 1). Everything waiting on a human.
Q# | Type | Created | Week | Cust ID | Customer | Original message | Question | Status | Digest # | Sent to | First sent | Last nudged | Answer | Answered by | Resolved | Outcome
- Q#: running number, never reused.
- Type (dropdown): Clarify, Sales, Invoice, Read-back, Late order, Reminder, Driver, Other.
  An Other item whose Question starts with "REPLY: " is the system's reply to something Mark or Laura texted in the group (an answer, a confirmation or a clarification). It needs no answer: owner-digest sends it and sets it Resolved.
  Read-back items hold the link to a read-back approval list in Question.
  Driver items are questions for Harry (sent by delivery-check, not the digest). Invoice items hold the link to that day's invoice list doc in Question.
- Digest # (TRACKER): the number Mark sees in the current digest (1, 2, 3). Cleared when the item is Resolved. Never two items that aren't Resolved with the same Digest #.
- Status (dropdown): Waiting, Sent, Answered, Resolved.   (Waiting = not yet sent to anyone. Answered = a Sales item Mark or Laura answered without sale / no sale / resolved; owner-digest follows these up once a day.) Sent to: "Group" for the family group (rule 11), or a name.
- Outcome (dropdown, Sales only): Sale, No sale, Resolved.

TAB: Inbox Log (header in row 1). One row per text the parser handled, in and out.
Time | Direction | From | To | Who | Classified as | Action taken | Written to | Quo message ID
- Direction (dropdown): In, Out (family by hand), Out (system).
- Who: a Cust ID, Mark, Laura, Harry, Shane, or Unknown.
- The Quo message ID is the dedupe key: a message whose ID is already in this log is never processed again.

TAB: System (labels in column A, values in column B; all TRACKER cells)
Message cursor | date-time of the newest message the parser has finished
Run in progress since | date-time the current Farm ops run started; blank when no run is going (routines/farm-ops.md RUN FLAG)
Parser run in progress since | no longer used (leave blank; replaced by "Run in progress since")
Operator run in progress since | no longer used (leave blank)
Last parse finished | no longer updated
Parser late alert sent | no longer used
Last payment check | date-time invoicing last checked Square for payments
Missing doc alerts | date + doc names Shane was told about today, e.g. "2026-10-08: owner-digest, invoicing"
Sunday alert sent | date the "reminder never went out" alert last went out
Daily checks done | "[yyyy-mm-dd] [repo version]" of the operator's last build-ahead and label check (operator Step 0 b, c2)
Problem alerts checked | date-time the operator last checked the run history for ALERT problems (system issues) to text Shane
Problem alerts sent | today's date + the ALERT problems Shane was texted today, e.g. "2026-10-17: Customers Phone not written for C012"
Then a blank row, then the run history (LOG), header row starting with "Run start":
Run start | Run end | Routine | Trigger | Steps run | Texts sent | Problems
- If any label above is missing (for example an older setup), add it as a new row above the run history. Adding labels is allowed; never remove one.
- Reading texts: start from (Message cursor minus Cursor overlap), and skip any message whose ID is already in the Inbox Log (only search Inbox Log rows from the last 2 days; older IDs can't be in the window). The overlap catches texts that arrive late or share a minute.
- Run flag: one Farm ops run at a time. routines/farm-ops.md RUN FLAG sets System "Run in progress since" at the start of a run and clears it at the end; a run that finds it set (and less than Config "Stale run after" minutes old) ends at once and changes nothing. The parser and operator parts run one after the other inside the same run, so they never overlap.
- Week tabs: when a week tab is missing, follow MISSING WEEK TABS in week-names.md.

=====================================================
WORKBOOK 2: Weekly Deliveries
=====================================================
One tab per delivery week, Sunday to Saturday. Week 1 = Sunday Oct 11 2026.
Tabs are built a few weeks ahead, not months: the operator keeps THIS week through Config "Weeks built ahead" weeks later built (BUILDING A WEEK TAB, below). Shane may delete old or far-future tabs by hand; routines never delete tabs.

WEEK NAMES: THIS, NEXT and LAST week, and the tab names, are in week-names.md (moved there so the operator can read them on every run without this whole file).

BUILDING A WEEK TAB (the operator's build-ahead, or the parser when an order names a week that isn't built yet)
1. Name it by the tab name rules in week-names.md. Week number = weeks since Sun Oct 11 2026, plus 1. Put the tab after the previous week's tab.
2. Header block: every label in HEADER BLOCK, in order. Values: Week, Dates, and Asked-for order cutoff (the Saturday before the week, at Config "Asked-for order cutoff" time). Everything else blank.
3. Day table: the DAY TABLE header, then Monday to Friday rows, all blank.
4. Customer table, after one blank row: the CUSTOMER TABLE header, with one column per Products row whose Active is Yes, in Products order, between Stop # and Changes. Then one row per Customers row with Status Active (never Test), sorted by Day, Route, Stop #: Cust ID, Name, Day, Route and Stop # copied from Customers, and each product cell = that customer's standing order (blank if none). Every other cell blank. Starting amounts are not changes: no Changes entries.
5. Never build a second tab with the same name. A tab that exists but has no "Cust ID" header row is unfinished: finish it. An Active customer with no row on an unlocked built tab: add their row in sorted place, built as in step 4.

HEADER BLOCK (labels in column A, values in column B)
Week | N
Dates | Sun Oct 11 - Sat Oct 17 2026
Asked-for order cutoff | 2026-10-10 18:00
Reminder requested |
Reminder last asked |
Reminder asked Laura |
Reminder others last asked |   (TRACKER: when Laura, and Shane for an approval, were last followed up about the reminder)
Reminder wording received |   (STAMP: first time wording arrived)
Reminder wording |   (TRACKER: current wording; replaced if Mark or Laura revises it)
Reminder wording updated |   (TRACKER: when the current wording was set)
Reminder check failed |   (TRACKER: when the wording last failed the sanity check)
Reminder final text |   (TRACKER: the exact formatted text in the latest preview; this is what gets sent)
Reminder preview sent |   (TRACKER: when the latest preview went out)
Reminder approvals |   (TRACKER: who approved the latest preview and when, e.g. "Mark 2026-10-09 10:12; Shane 2026-10-09 10:30". Cleared when a new preview goes out.)
Reminder approved |   (STAMP: filled when two DIFFERENT people (any of Mark, Laura, Harry, Shane) have approved the latest preview. Only valid if given after the latest preview, and the preview is newer than "Reminder wording updated". Never tell anyone that two are needed.)
Reminder sent |
Reminder sent count |   (e.g. 105/107, 2 no phone)
Reminder test sent |   (TRACKER: when the approved text went to the test phones while Mode was TEST)
Weekly master list sent |   (STAMP: when the first master list for this week went out)
Weekly master list last sent |   (TRACKER: the sheet read time of the latest master list; the next update lists changes after it)
Weekly master list checked |   (TRACKER: yyyy-mm-dd of the last night weekly-master-list ran for this week, sent or not)
Finance update sent |

DAY TABLE (directly below, header row starts with "Day")
Day | Delivery list sent | Exceptions sent | Harry last asked | Harry ask count | Mark alerted | Route confirmed | Invoices drafted | Invoices approved | Invoices sent
- A day whose cells say "No delivery" had nothing ordered (for example a holiday); every step skips it.
- Exceptions sent (TRACKER): when the latest morning-of exceptions text went out (see daily-delivery-list).
One row each: Monday, Tuesday, Wednesday, Thursday, Friday.

CUSTOMER TABLE (below the day table after one blank row, header row starts with "Cust ID")
Cust ID | Name | Day | Route | Stop # | one column per product (same names as Products "Column name") | Changes | Needs attention | Not delivered | Reminder sent | Locked | Delivered | Invoice link | Invoice approved | Invoice sent | Paid | Confirm needed | Confirmation sent | Read-back draft | Read-back drafted | Read-back approved
- Read-back draft (TRACKER): the exact read-back text waiting for Mark's approval. Read-back drafted (TRACKER): when it was put on an approval list. Read-back approved (TRACKER): when Mark or Laura approved it.
- Confirm needed (TRACKER): set by the parser to the date-time of the latest change the customer should hear about (their own order text, or Mark settling a question about it).
- Confirmation sent (TRACKER): when confirm-orders last texted this customer a read-back for this row. A read-back is due when Confirm needed is later than Confirmation sent (or Confirmation sent is blank).
- Rows sorted by Day (Mon to Fri), then Route, then Stop #.
- Product cells (QUANTITY): this week's amount. Starts as the standing order.
- Changes (LOG): one entry per change, separated by " ; ", e.g. "2026-10-09 09:14 Yogurt Plain 0>2 (text)". An entry ending "(standing order sync)" only copies the customer's standing order onto that week; it is not a change anyone asked for. Delivery lists, read-back risk checks and sync conflict checks ignore it.
- Not delivered (LOG): product Column name + amount + reason, separated by " ; ", e.g. "Yogurt Plain x2 ran out". Billing subtracts these.
- Locked (STAMP): filled when that day's delivery list goes out. THIS is the real order cutoff. Before Locked, any order for this week counts, even after the asked-for cutoff. After Locked, the row never changes, with one exception: a Late order that Mark answers "add it" (squeeze in) may change a quantity; the Changes entry must say "after lock, approved by Mark" and Needs attention must say "added after list went out". Otherwise new orders become a Late order Queue item for Mark.
- A week tab is frozen when every row with an invoice has Invoice sent filled (or is marked not invoiced). Frozen tabs are never edited.
- Week tabs are built a few weeks ahead from Customers (BUILDING A WEEK TAB). When Reference changes (add/remove customer, standing order change, "run sync"), only rows whose Locked is blank are updated.
- Day, Route and Stop # on a week row are copies of Customers. daily-delivery-list refreshes them on unlocked rows before it builds a list, so a customer moved to another day or stop shows up in the right place.
