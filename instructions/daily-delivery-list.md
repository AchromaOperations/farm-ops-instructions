DAILY DELIVERY LIST (version 3)
Written for: sheets-spec version 4

Change log
- v3 (2026-10-08): share wording on the list and lock text.
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v2 (2026-10-07): empty days count as no delivery (no list, no Harry texts); test customers left out; MORNING EXCEPTIONS part for items added after the list went out.
- v1 (2026-10-07): first version.

HOW TO WORK
A checklist. It locks one delivery day's orders, makes one printable Google Doc for that day, and texts the link. The only judgment is the marked guess in Step 2.

Delivery day = tomorrow (normal run) or today (catch-up run), whichever the operator found due. Use the week tab containing that day. Day rows = customer rows whose Day is that weekday, EXCEPT rows whose Cust ID starts with "T" (test customers), which are always left out.

STEP 1. CHECK
- If that day's "Delivery list sent" is already filled, finish (nothing to do).
- Empty day (holidays work this way): if the day has no rows, or every product quantity on every day row is 0 or blank, there is no delivery. Fill that day's "Delivery list sent", "Route confirmed", "Invoices drafted", "Invoices approved" and "Invoices sent" with "No delivery", lock nothing, send nothing, and finish. (Mark empties a day by moving or zeroing those customers' orders on the week tab ahead of time.)
- If a Google Doc named "Delivery list [Ddd Mon D YYYY]" already exists in Delivery Lists, reuse it (a previous run made it and stopped): clear its content and rebuild it below. Never make a second one.

STEP 2. SETTLE UNANSWERED QUESTIONS
For each Queue item of Type Clarify (Status Waiting or Sent) for a customer in this day's rows:
- Take the FIRST choice offered in its Question and write it to the row as an order (QUANTITY cells), with a Changes entry "[date-time] [Column name] [old]>[new] (GUESS at lock)" and Needs attention "GUESS: confirm at the door".
- Set the item's Answer = "guessed at lock: [choice]", Answered by = "system", Status = Resolved, clear Digest #.
- If no choice can be taken from the Question, leave the row as it is and put "UNCLEAR ORDER: [original message]" in Needs attention.
Late order items for this day stay open (Mark decides); list them in the doc.

STEP 3. LOCK
Fill "Locked" = now on every one of this day's rows that is blank.

STEP 4. BUILD THE DOC
Doc "Delivery list [Ddd Mon D YYYY]" in Delivery Lists. Plain and printable, large text, no colors (bold and symbols only). One section per route (Route column; if blank, one section for the day), each starting on a new page:

[Route] - [Day, date] - Driver: [Routes tab Driver]

PACKING LIST
Product (Column name) | Total for this route
(every product with a total above 0)

STOPS (in Stop # order)
Stop # | Name | Address, City | Items (only products above 0, e.g. "share 1 gal, 2 Yogurt Maple") | Delivery notes | Flags
Flags: "GUESS" if Needs attention starts with GUESS, "CHANGED" if Changes has an entry this week, "!" for any other Needs attention text.

CHANGES THIS WEEK
One line per stop that has a Changes entry or Needs attention text: name, then the text.

PENDING (not packed)
Open Late order items for this day: customer and what they asked for. "Mark hasn't decided; don't pack unless he says so."

STEP 5. SEND
- Text Mark, Laura and Harry: "[Day]'s delivery list is ready: [link]. [n] stops, [routes]. [g] guesses marked. Shares and orders for [Day] are now locked."
- Log each text in the Inbox Log (Out (system)).
- Fill that day's "Delivery list sent" = now.

FINISH
Report to the operator: day, stops, guesses, pending items.

=====================================================
MORNING EXCEPTIONS (run only this part when the operator says so)
=====================================================
Changes approved after the list went out (Mark said "add it" to a Late order) must reach Harry before he leaves.
1. Delivery day = today. New exceptions = today's customer rows with a Changes entry containing "after lock" that is later than today's "Exceptions sent" (all of them if it's blank).
2. Text Mark, Laura and Harry one message:
   "Changes to today's ([Day]) delivery list:
   - [Name], stop [#]: [what changed, e.g. +2 Yogurt Maple]
   Harry, reply GOT IT when you have these."
3. Append the same lines to the day's delivery list doc under a heading "ADDED AFTER LIST WENT OUT".
4. Create a Queue item: Type Driver, Week, Question = "Got today's added items? ([names]) Reply GOT IT", Status = Waiting. (delivery-check sends and re-asks it; the parser records Harry's answer.)
5. Set today's "Exceptions sent" = now. Log each text in the Inbox Log.
