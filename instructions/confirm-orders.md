CONFIRM ORDERS (version 8)
Written for: sheets-spec version 4

Change log
- v8 (2026-10-10): read-backs word Extra Milk in gallons right after the share.
- v7 (2026-10-09): "(standing order sync)" entries don't make a read-back risky.
- v6 (2026-10-09): the read-back list goes to Mark as text (sheets-spec rule 10), not a doc link.
- v5 (2026-10-09): read-backs also wait while the customer's weekly share request is open with Mark.
- v4 (2026-10-09): the read-back list waits only on sheets-spec rule 9; a reminder still waiting for wording no longer holds it.
- v3 (2026-10-08): read-backs call milk the customer's weekly share; add-ons follow after "plus".
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v2 (2026-10-08): manual review (Config "Read-back review": ALL, RISKY ONLY, OFF).
- v1 (2026-10-08): first version.

HOW TO WORK
A checklist. The parser already decided who needs a read-back; this step only writes the friendly text and sends it. Customer-facing: follow the routine's Mode rule (not LIVE = send to the test phones instead). Every text you send: log it in the Inbox Log right away as sheets-spec rule 7 says (Direction "Out (system)", the number, the exact text, Quo message ID "pending").

STEP 1. WHO
Rows = customer rows in THIS and NEXT week (sheets-spec WEEK NAMES) where "Confirm needed" is filled and later than "Confirmation sent" (or "Confirmation sent" is blank). Test customers (Cust ID starting with "T") get read-backs too, so the flow can be tested.
Skip a row for now (it will be picked up later) if that customer has a Queue item of Type Clarify or Late order that is not Resolved, or a Sales item whose Question contains "asked to change their weekly share" that is not Resolved: they get one read-back once everything is settled.
If the same customer has rows in both weeks, send one text per row (one per delivery).

STEP 2. WRITE THE TEXT (one per row)
Items = every product on the row with a quantity above 0, using Products "Text name" (or Column name in lower case):
- Milk (gal) is the weekly share (sheets-spec TERMS): 0.5 = "your weekly share (half gallon)", 1 = "your weekly share (1 gallon)", 1.5 = "your weekly share (1 and a half gallons)", 2 or more = "your weekly share ([n] gallons)". It always comes first.
- Extra Milk (jars) comes right after the share, in gallons: 1 = "an extra half gallon", 2 = "an extra gallon", 3 = "an extra gallon and a half", 4 or more = "[jars/2] extra gallons".
- Everything else: 1 = "a [text name]" (or just the name if "a" sounds wrong, e.g. "butter"), more = "[n] [text name, plural]".
- Add-ons follow after "plus", joined as a natural list: "your weekly share (1 gallon), plus 2 vanilla maple yogurts, butter and a crumble cheese". No share this week: just the add-ons ("2 vanilla maple yogurts and butter").
Day = the customer's delivery day on that row. Add the date ("Wednesday the 21st") when the row is NEXT week; just the day name when it is THIS week.

Text:
- First read-back for this row ("Confirmation sent" blank): "Got it! See you [Day] with [items]."
- Later read-backs: "Got it, updated! We're now delivering [items] on [Day]."
- Everything on the row is 0 (a skip): "Got it, no delivery for you this week. See you [next delivery day and date]!"
No other wording, no questions, no prices.

STEP 3. DECIDE: SEND NOW OR NEEDS APPROVAL
Review = Config "Read-back review" (blank or missing = ALL).
Risky = since this row's last "Confirmation sent", its Changes has any entry whose source is not "(text)" (for example "(Mark)", "(Laura)", "(Mark (by hand))", "(GUESS at lock)", or "after lock"). Entries ending "(standing order sync)" don't count (sheets-spec Changes).
- Review OFF: send now (Step 4).
- Review RISKY ONLY: risky rows need approval (Step 5); others send now (Step 4).
- Review ALL: every row needs approval (Step 5).
Rows already approved: if "Read-back approved" is later than "Read-back drafted", AND "Confirm needed" is not later than "Read-back drafted" (nothing changed since), send "Read-back draft" exactly as approved (Step 4). If something changed since it was drafted, it needs a new draft and approval (Step 5).

STEP 4. SEND
Send the text to the customer's Phone (Customers tab). No phone: skip it and put "no phone for read-back" in Needs attention. After each send, set that row's "Confirmation sent" = now.

STEP 5. APPROVAL LIST
Rows needing approval, EXCEPT rows already waiting on a list ("Read-back drafted" is later than "Confirm needed", and "Read-back approved" is blank or earlier than "Read-back drafted"). If there are none, skip to the last line of this step.
1. Set each row's "Read-back draft" = the text from Step 2, and "Read-back drafted" = now.
2. Make a Google Doc in Read-back Lists named "Read-backs [yyyy-mm-dd hh:mm]". Large plain text:
   "Read-backs waiting for your OK. Reply 'good' to send all, or 'good except [numbers]'."
   Then one numbered line per row: "[#]. [Name] ([Cust ID], [week]): [exact text]"
3. Create a Queue item: Type Read-back, Question = the doc link, Original message = "[n] read-backs", Status = Waiting.
4. Send it only if no approval is open (sheets-spec rule 9; a reminder still waiting for wording does NOT count): text Mark the list as sheets-spec rule 10 says. Title: "[n] customer read-backs need your OK". Lines: "[#]. [Name]: [exact text]". Then Status = Sent, Sent to = Mark, First sent = now.
   Otherwise leave it Waiting; a later run sends it. (Nudges and Laura are handled by owner-digest.)
Last line: if a Read-back Queue item is still Waiting (made by an earlier run), send the oldest one the same way, under the same conditions as item 4.

FINISH
Report to the operator: read-backs sent, rows put on an approval list, rows skipped (waiting on Mark, or no phone).
