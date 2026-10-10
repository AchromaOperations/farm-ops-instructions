DAILY DELIVERY LIST (version 9)
Written for: sheets-spec version 4

Change log
- v9 (2026-10-10): Day, Route and Stop # are refreshed from Customers on unlocked rows before the list is built; a blank Stop # is flagged "!".
- v8 (2026-10-10): skipped stops stay on the route in their place, flagged SKIP, and are listed in a box at the top (with no-milk stops); the text says how many are skipping; a skip added after lock reads "SKIP, no delivery today".
- v7 (2026-10-10): Extra Milk jars are packed with the share jars and shown as "+ N extra" at the stop.
- v6 (2026-10-09): milk is counted in half-gallon jars on the packing list and each stop (Mark: half-gallon jars only).
- v5 (2026-10-09): "(standing order sync)" Changes entries don't flag a stop as CHANGED or put it on the change list.
- v4 (2026-10-09): a customer's weekly share request still open at lock is flagged on the row, never guessed.
- v3 (2026-10-08): share wording on the list and lock text.
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v2 (2026-10-07): empty days count as no delivery (no list, no Harry texts); test customers left out; MORNING EXCEPTIONS part for items added after the list went out.
- v1 (2026-10-07): first version.

HOW TO WORK
A checklist. It locks one delivery day's orders, makes one printable Google Doc for that day, and texts the link. The only judgment is the marked guess in Step 2.

Delivery day = tomorrow (normal run) or today (catch-up run), whichever the operator found due. Use the week tab containing that day. First, on every customer row of that tab whose Locked is blank, copy Day, Route and Stop # from Customers (week rows only hold copies; Customers is the truth). Then: Day rows = customer rows whose Day is that weekday, EXCEPT rows whose Cust ID starts with "T" (test customers), which are always left out.

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
For each Sales item that is not Resolved, whose Question contains "asked to change their weekly share", for a customer in this day's rows, and whose Week is this delivery's week: leave the row as it is (never guess a share change) and add "SHARE REQUEST NOT SETTLED: check with Mark" to that row's Needs attention, exactly this wording (never the customer's words). The item stays open.

STEP 3. LOCK
Fill "Locked" = now on every one of this day's rows that is blank.

STEP 4. BUILD THE DOC
Doc "Delivery list [Ddd Mon D YYYY]" in Delivery Lists. Plain and printable, large text, no colors (bold and symbols only). One section per route (Route column; if blank, one section for the day), each starting on a new page:

[Route] - [Day, date] - Driver: [Routes tab Driver]

SKIPS: DO NOT DELIVER (first thing on the route, in a box)
A skip = a stop whose row has every product at 0 or blank this week, however it got there (the customer asked, Mark or Laura put it in, or someone zeroed it in the sheet by hand). One line each: "Stop [#]: [Name], [Address, City]: SKIP, nothing to deliver this week".
Under it, "NO MILK THIS WEEK": stops whose Milk (gal) is 0 this week while their Customers Milk (gal) is above 0, but who still get add-ons: "Stop [#]: [Name]: NO MILK, add-ons only".
Make it impossible to miss on paper: a one-cell table with a thick border and bold text. If you can't make a box, put a full line of ■ symbols above and below it. If there are none, the box says "No skips this week", so the driver knows it was checked.

PACKING LIST
Product (Column name) | Total for this route
(every product with a total above 0)
Milk goes out in half-gallon jars only (sheets-spec TERMS). Write the milk line as jars first: "Milk: [jars] half-gallon jars ([gallons] gal)", where jars = share jars (gallons x 2) plus Extra Milk jars. If any Extra Milk is on the route, add "including [n] extra".

STOPS (in Stop # order)
Every customer row of the day is listed in its Stop # place, skips included. Never leave a stop off the list.
Stop # | Name | Address, City | Items (only products above 0, e.g. "share 2 jars + 1 extra, 2 Yogurt VM"; share in half-gallon jars = gallons x 2; Extra Milk is already in jars) | Delivery notes | Flags
A skip: Items = "SKIP: NO DELIVERY", Flags = "SKIP". No milk with add-ons: Items start with "NO MILK", Flags include "NO MILK".
Flags: "!" if Stop # is blank (no stop number yet). "GUESS" if Needs attention starts with GUESS, "CHANGED" if Changes has an entry this week, "!" for any other Needs attention text, and "!" if the share isn't a whole number of jars (gallons not a multiple of 0.5; write the gallons as they are). Entries ending "(standing order sync)" never count as a change here: they only copy a customer's every-week order onto the week.

CHANGES THIS WEEK
One line per stop that has a Changes entry (other than "(standing order sync)" entries) or Needs attention text: name, then the text.

PENDING (not packed)
Open Late order items for this day: customer and what they asked for. "Mark hasn't decided; don't pack unless he says so."

STEP 5. SEND
- Text Mark, Laura and Harry: "[Day]'s delivery list is ready: [link]. [n] stops to deliver, [routes]. [s] skipping (boxed at the top). [g] guesses marked. Shares and orders for [Day] are now locked."
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
   - [Name], stop [#]: [what changed, e.g. +2 Yogurt VM; if their whole order is now 0: SKIP, no delivery today]
   Harry, reply GOT IT when you have these."
3. Append the same lines to the day's delivery list doc under a heading "ADDED AFTER LIST WENT OUT".
4. Create a Queue item: Type Driver, Week, Question = "Got today's added items? ([names]) Reply GOT IT", Status = Waiting. (delivery-check sends and re-asks it; the parser records Harry's answer.)
5. Set today's "Exceptions sent" = now. Log each text in the Inbox Log.
