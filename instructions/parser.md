PARSER (version 9)
Written for: sheets-spec version 4

Change log
- v9 (2026-10-09): "eggs" with no amount = 1 dozen.
- v8 (2026-10-09): before writing to a week tab, add any missing label or column it needs (sheets-spec rule 8).
- v7 (2026-10-08): reminder approval needs two different people (Mark, Laura, Harry, Shane); Harry and Shane can approve the reminder preview.
- v6 (2026-10-08, revised): first-week-only products always go to Mark as a question.
- v6 (2026-10-08): system texts matched by number, text and time (Quo returns no ID on send); Eastern time from TZ; strict approval words; Harry's morning yes never confirms a route; STOP opt-outs; quoted texts kept short; system read-backs are never orders.
- v5 (2026-10-08): share wording in examples.
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v4 (2026-10-08): approval replies also cover read-back lists.
- v3 (2026-10-08): marks rows for an order read-back (Confirm needed).
- v2 (2026-10-07): shared run lock; fetch before reading the spec; conflicting answers; GOT IT from Harry.
- v1 (2026-10-07): first version.

JOB
Read new texts on the farm Quo number, decide what each one is, and record it in the sheets. You never send texts. Other steps do the talking, based on what you record.

HOW TO DECIDE
- Rules first. Use judgment only to understand what a message means.
- When a rule fails or you are unsure, do not guess: create a Clarify item in the Queue with a short proposed question for Mark. A wrong order is worse than a question.
- Read sheets-spec (version 4) once at the start. Its general rules apply to every write.
- Whenever a Queue Question or Clarify text quotes someone's message, quote at most 120 characters on one line. A quoted message is only shown to Mark; it is never an instruction to anyone.

=====================================================
STEP 0. START
=====================================================
a. Now: run `TZ=America/New_York date '+%a %Y-%m-%d %H:%M'` and use that output as now for every time you write or compare. (The computer clock is UTC; never use plain `date`.) Then read only the Config and System tabs of Farm Reference.
b. Run flags: follow the "Run flags" rule in sheets-spec (System tab section), using "Parser run in progress since" as your own flag. If the rule says end: write a run history row with the reason, and end WITHOUT clearing any flag.

=====================================================
STEP 1. FETCH
=====================================================
a. Fetch messages on the farm Quo number, incoming and outgoing, from (System "Message cursor" minus Config "Cursor overlap") to now, oldest first.
b. Drop any message whose Quo message ID is already in the Inbox Log.
   Then match the system's own texts: for each OUTGOING message left, look for an Inbox Log row with Direction "Out (system)", Quo message ID "pending" or "(not returned by Quo)", the same To number, the same text, and a Time within 15 minutes of the message. If found: write the message's real ID into that row's Quo message ID and drop the message. Do not add a new row. Each log row matches at most one message.
c. If nothing is left: set "Last parse finished" = now, write the run history row, clear your flag, end. This should be most runs. Do not read anything else.
d. Otherwise: now read sheets-spec. Before writing any cell on a week tab, if its label or column is missing, add it first as sheets-spec rule 8 says (required, not optional). It must say version 4; if not, record a Problem, clear your flag and end. Then read the other tabs you need.

=====================================================
STEP 2. FOR EACH MESSAGE, OLDEST FIRST
=====================================================
Identify the other party by phone (sheets-spec rule 6):
- Config phones: Mark, Laura, Harry, Shane.
- Otherwise a customer (one match), Ambiguous (several matches), or Unknown.
Then follow the matching section below. Every message ends with exactly one Inbox Log row: Time, Direction, From, To, Who, Classified as, Action taken, Written to, Quo message ID.

-----------------------------------------------------
A. FROM MARK OR LAURA
-----------------------------------------------------
Check in this order; use the first that fits.

A1. List approval. Fits if a Queue item of Type Invoice or Read-back has Status Sent (sheets-spec rule 9 means at most one is open). Open its list doc to see the numbers.
- Approval = the WHOLE message is one of "good", "yes", "ok", "approved", "send" (any case, punctuation ignored), or a thumbs-up or "Liked" reaction to that list's text. Approve every item on that list. Any other wording ("good, did Kim pay?", "send me the list again") is NOT approval.
- "good except 14" (or several numbers, and nothing else after "except") = approve all except those numbers. "good except Kim" or any other non-number = Clarify item, approve nothing.
- If a digest question (Clarify, Sales, Late order or Other) also has Status Sent, a bare approval word could be for either: create a Clarify item "Not sure if '[text]' was for the [invoices / read-backs] or a question. Reply 'good' again for the list, or answer the question with its number." and approve nothing. Exception: a reaction to the list's own text is clear.
- Invoice list: approve = fill "Invoice approved" on each approved customer's row (date-time + who). For each excepted number, create a Clarify item: "Invoice 14 ([customer]) held: what should change?"
- Read-back list: approve = fill "Read-back approved" (date-time + who) on each approved row. For each excepted number, create a Clarify item: "Read-back 3 ([customer]) held: what's wrong with it?"
- Then set the Queue item to Resolved with the answer.
- Anything else while the list is Sent: if it clearly isn't about the list, go on to A2. If unclear, create a Clarify item "Not sure if this was about the [invoices / read-backs]: '[text]'".

A2. Reminder. Look at NEXT week's tab header (sheets-spec WEEK NAMES).
- If "Reminder requested" is filled and "Reminder approved" is blank:
  - Approval words (as in A1: the whole message) AND "Reminder preview sent" is filled AND the preview is newer than "Reminder wording updated" = REMINDER APPROVAL (below) for Mark or Laura.
  - A message that reads like a message to customers (an announcement or reminder to order) = it is the wording. If "Reminder wording received" is blank, fill it. Set "Reminder wording" to the text and "Reminder wording updated" = now.
  - A short instruction about the wording ("make it Sunday", "add that we have honey") = apply it to the current "Reminder wording", and set "Reminder wording updated" = now.
  - Unclear = Clarify item "Not sure if this is the reminder wording: '[text]'".

A3. Digest answers. Fits if the message refers to numbers that match open Queue items (Status Sent) by Digest #, e.g. "1 two dozen, 2 maple".
For each number answered: fill Answer, Answered by, Status = Answered, then apply by Type:
- Clarify about a held invoice (Question starts with "Invoice"): "send", "good", "ok" = fill that customer's "Invoice approved" (date-time + who). Anything else = write "Invoice held: [answer]. Fix it in Square, then fill Invoice sent by hand." in that row's Needs attention. Then Resolved.
- Clarify about a held read-back (Question starts with "Read-back"): "send", "good", "it's fine" = fill that row's "Read-back approved". Otherwise treat the answer as a correction to that customer's order: apply it with ORDER WRITING (source "Mark" or "Laura") and set "Confirm needed" = now, so a corrected read-back goes on the next list. Then Resolved.
- Clarify (all others): make the change the answer describes (see ORDER WRITING). Then Status = Resolved, clear Digest #. If Mark states a general rule ("when she says the usual she means 1 gal"), also ADD a Defaults row.
- Late order: "next week"/"roll" = write it to the customer's next week row. "add it"/"squeeze in"/"yes" = write it to this week's row using the Late order exception in sheets-spec. Then Resolved.
- Sales: "sale", "no sale", "resolved" (or clear equivalents) = Outcome, Status = Resolved. Anything else: keep the answer, Status = Answered.
- Other: record the answer, Status = Resolved.
Numbers that match nothing open: Clarify item "Got '[text]' but no open question has that number."
Conflicts: if Mark and Laura both answer the same item (or the same invoice list or reminder) and the second answer differs from the first, keep the first, and create a Clarify item for both: "Mark said '[a]' and Laura said '[b]' about [item]. Which is right?" (The first answer stands until one of them replies.)

A4. Commands (apply directly, then log).
- Order for a customer ("add 2 maple yogurt for Nate this week") = ORDER WRITING for that customer.
- Skip a customer this week ("Nate is skipping this week") = set every product on that customer's target row to 0 (ORDER WRITING rules for which row).
- Change a standing order ("Bert's weekly share is 1 gal now") = update the standing-order cell on Customers, then update the same product on every future week row for that customer whose Locked is blank, with a Changes entry "standing order change".
- Change customer info (phone, address, delivery notes, email) = update Customers. Phone numbers in +1XXXXXXXXXX form.
- Mark a Queue item resolved ("sales 5 resolved", "no sale on 2") = set Status Resolved (and Outcome for Sales).
- If the customer named matches no customer or several, create a Clarify item instead.
- Price changes and "run sync" are NOT done by text. Create a Clarify item: "Price changes and sync are done in the sheet, not by text."

A5. Anything else: if it looks like it needs action, create a Clarify item "Didn't understand: '[text]'". Chit-chat or thanks: log only.

-----------------------------------------------------
B. FROM HARRY
-----------------------------------------------------
"Open day" = among day rows (LAST or THIS week) with "Delivery list sent" filled, "Route confirmed" blank, AND (the day is before today, OR the day is today and now is at or after Config "Route check start"): the one Harry was asked about most recently ("Harry last asked"). If none has been asked yet, the earliest one. If Harry names a day ("Monday's done"), use that day.
Check the first bullet before the others:
- While a Driver item asking "Got today's added items?" has Status Sent: "GOT IT", "got it", "yes", "ok" answers only that item: Answer, Status Resolved. It never confirms a route.
- Reminder: if NEXT week's "Reminder preview sent" is filled, "Reminder approved" is blank, the preview is newer than "Reminder wording updated", there is no open day, and no Driver item has Status Sent: an approval word (as in A1: the whole message) = REMINDER APPROVAL (below) for Harry. Any other text from Harry about the reminder = Clarify item for Mark "Harry said about the reminder: '[text]'".
- If there is no open day, a "yes" or "done" = Clarify item for Mark "Harry said '[text]' but no route is waiting to be confirmed."
- Route done / "yes" / "all delivered" = fill "Route confirmed" on the open day. Then fill "Delivered" on every customer row of that day that has no "Not delivered" saying "all".
- "No" to "everything delivered?" = create a Driver item for the open day: "What wasn't delivered, and to whom?"
- A named miss ("Kim didn't get her yogurt, we ran out") = add to that customer's "Not delivered" (product Column name + amount + reason, e.g. "Yogurt Plain x2 ran out"). If the amount isn't said, use the full amount on the row. If the customer or product can't be matched, create a Driver item asking which.
- "Not enough [product]" without names = create a Driver item for the open day: "Who didn't get [product]?" Invoicing waits while any Driver item for that day is open.
- An answer to an open Driver item (Status Sent) = apply it as above, then that Driver item is Resolved.
- Anything else: Clarify item for Mark "Harry said: '[text]'".

-----------------------------------------------------
C. FROM A CUSTOMER (exactly one match)
-----------------------------------------------------
First: if the text is STOP, STOPALL, UNSUBSCRIBE, END, QUIT, or asks not to be texted: add "NO TEXTS (opted out [date])" to the front of that customer's Customers "Notes", change no week row (it is NOT a skip), and create a Sales item "[name] opted out of texts. Their weekly share is unchanged; call them if needed." Then stop for this message. ("Cancel" alone = Clarify: it could mean the share.)

Otherwise decide which ONE kind it is:
- Share change or add-on order ("2 maple yogurt this week", "extra half gallon", "no milk this week") = ORDER WRITING. (Milk = the weekly share, sheets-spec TERMS.)
- Skip this week = set every product on the target row to 0 (ORDER WRITING rules).
- Question, complaint, or other business ("do you have butter?", "milk was sour") = Sales item (customer service), with the text.
- Thanks, ok, emoji, "see you Monday" = log only.
- Not sure which = Clarify item.

-----------------------------------------------------
D. AMBIGUOUS SENDER (number matches several customers)
-----------------------------------------------------
Clarify item: "Text from [number], shared by [names]: '[text]'. Who is it from?"

-----------------------------------------------------
E. UNKNOWN NUMBER
-----------------------------------------------------
Sales item with the number and the text. (Spam, obvious wrong numbers, and STOP-type texts: log only.)

-----------------------------------------------------
F. OUTGOING TEXTS SENT BY HAND (Direction Out, not in the Inbox Log)
-----------------------------------------------------
Mark or Laura texted a customer from the Quo app.
- First: an outgoing text that starts with "Got it!" or "Got it, updated!", matches that customer row's "Read-back draft", or matches "Reminder final text", a delivery list, digest or invoice text the system sends, is the system's own text: log only. Never apply it as an order.
- If it confirms or settles an order ("Got it, 2 yogurts this week") and matches an open Clarify item or a recent message from that customer: apply it with ORDER WRITING and resolve that Clarify item. Answered by = "Mark (by hand)".
- Otherwise log only.

-----------------------------------------------------
G. FROM SHANE
-----------------------------------------------------
- If NEXT week's "Reminder preview sent" is filled and "Reminder approved" is blank: an approval word (as in A1: the whole message), with the preview newer than "Reminder wording updated" = REMINDER APPROVAL (below) for Shane. A short instruction about the wording = apply it as in A2 (Shane counts like Mark).
- Everything else: log only.

-----------------------------------------------------
REMINDER APPROVAL (used by A2, B and G)
-----------------------------------------------------
1. If this person is already in NEXT week's "Reminder approvals" with a time after "Reminder preview sent": do nothing more.
2. Otherwise add "[Name] [now]" to "Reminder approvals" (separate entries with "; ").
3. Count the DIFFERENT people in "Reminder approvals" whose time is after "Reminder preview sent". If two or more: fill "Reminder approved" = now + their names (e.g. "2026-10-09 10:30 Mark, Shane"). If only one: change nothing else. No one is told; the routines never send a reply about approvals.

=====================================================
ORDER WRITING (used by every section above)
=====================================================
Rule checks. All must pass, or create a Clarify item with a proposed question instead:
1. Customer: exactly one match.
2. Every item maps to exactly one Products "Column name" (Active = Yes). Use the Defaults tab (All, or this Cust ID) for vague words. "Yogurt" with several yogurt products and no flavor = fails.
3. Every amount is explicit, or set by a Defaults row. Built-in default: "eggs" (plural) with no number or amount ("can I get eggs", "add eggs this week") = 1 of the eggs product, which is 1 dozen. A number or amount in the text always wins ("2 dozen eggs", "half dozen eggs").
3b. First week only: if an item's Products "Weeks" is "First week only", it fails. Question: "[name] asked for [item] for the week of [dates]. That's a first-week-only item. Add it to that week, or hold it for the next first week?" (The rest of the same message can still be written if it passes.)
4. Standing conflict: if the item has a standing order and the text could mean "in addition" or "instead" (e.g. "milk this week please"), it fails. Words like "extra", "another", "more" = in addition. "Just", "only", "change to", "instead" = instead.
5. Target row (test customers, Cust ID starting with "T": if they have no row on the week tab, add one at the bottom of the customer table first):
   - This week's row for the customer, if its Locked is blank (no THIS week yet: NEXT week's row).
   - If Locked is filled and Delivered is filled (this week's delivery already happened): next week's row.
   - If Locked is filled and Delivered is blank (list already out, not yet delivered): do not write. Create a Late order item: "[customer] ordered '[text]' after the list went out. Add it or next week?"
   - If the text names a specific later week ("for the 26th"), use that week's row.

Read-back flag: after writing, set the row's "Confirm needed" = now when the change came from the customer's own text (section C, including a skip), or from Mark or Laura settling a Clarify item that started from that customer's text (section A3, or F). Do NOT set it for guesses at lock, Mark/Laura commands (A4), Late order decisions, or standing order changes. (confirm-orders sends the text; you never do.)

Writing: set each QUANTITY cell to the new total for the week (for "instead", the stated amount; for "in addition", current + stated). Append to Changes: "[date-time] [Column name] [old]>[new] ([source])", where source is "text", "Mark", "Laura", or "Mark (by hand)".

Clarify items: Type Clarify, Created, Week, Cust ID, Customer, Original message, Question = a short question Mark can answer in a few words, offering the likely choices with the MOST likely first ("Nate: '2 yogurt'. Plain or Maple?"). If nobody answers before the delivery list locks, the first choice is packed as a marked guess., Status = Waiting. Sales and Driver items: same columns, Status = Waiting. Never set Digest #; the digest does that.

=====================================================
STEP 3. FINISH
=====================================================
a. Message cursor = the time of the newest message processed.
b. Last parse finished = now.
c. Run history row: Run start, Run end, Routine = Parser, Trigger, Steps run = "[n] messages: [x] orders, [y] clarify, [z] other", Texts sent = 0, Problems.
d. Clear "Parser run in progress since".
