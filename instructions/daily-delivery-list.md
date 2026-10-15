DAILY DELIVERY LIST (version 13)
Written for: sheets-spec version 4

Change log
- v13 (2026-10-15): the list is now the approved PDF design (logo header in the website's colors, tiles, skip box, packing list and stops with tick boxes), made by tools/delivery_list_pdf.py and saved to Delivery Lists as a PDF. The Google Doc (tools/delivery_list_html.py, restyled to match) is only the fallback when the PDF can't be saved. Shane: the Doc that went out Oct 15 was the wrong design.
- v12 (2026-10-15): the doc's layout is fixed: tools/delivery_list_html.py writes the whole list as HTML and the doc is created from it (HTML converted to a Google Doc), so every day looks the same. Never lay the doc out by hand; plain text only as a reported fallback. (Thursday Oct 15's list came out as plain text.)
- v11 (2026-10-13): every stop shows the customer's phone number next to the address (Phone, plus Phone 2 if filled).
- v10 (2026-10-10): Mark and Laura get the list texts as one family group text; Harry still gets his own.
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
A checklist. It locks one delivery day's orders, makes that day's delivery list as a PDF in Drive, and texts the link. The only judgment is the marked guess in Step 2. The list's layout and counts come from a script (Step 4); you never lay it out yourself.

Delivery day = tomorrow (normal run) or today (catch-up run), whichever the operator found due. Use the week tab containing that day. First, on every customer row of that tab whose Locked is blank, copy Day, Route and Stop # from Customers (week rows only hold copies; Customers is the truth). Then: Day rows = customer rows whose Day is that weekday, EXCEPT rows whose Cust ID starts with "T" (test customers), which are always left out.

STEP 1. CHECK
- If that day's "Delivery list sent" is already filled, finish (nothing to do).
- Empty day (holidays work this way): if the day has no rows, or every product quantity on every day row is 0 or blank, there is no delivery. Fill that day's "Delivery list sent", "Route confirmed", "Invoices drafted", "Invoices approved" and "Invoices sent" with "No delivery", lock nothing, send nothing, and finish. (Mark empties a day by moving or zeroing those customers' orders on the week tab ahead of time.)
- If a file named "Delivery list [Ddd Mon D YYYY].pdf" (or a Google Doc "Delivery list [Ddd Mon D YYYY]") already exists in Delivery Lists, a previous run made it and stopped. Never make a second one: skip Step 4 and send that file's link in Step 5.

STEP 2. SETTLE UNANSWERED QUESTIONS
For each Queue item of Type Clarify (Status Waiting or Sent) for a customer in this day's rows:
- Take the FIRST choice offered in its Question and write it to the row as an order (QUANTITY cells), with a Changes entry "[date-time] [Column name] [old]>[new] (GUESS at lock)" and Needs attention "GUESS: confirm at the door".
- Set the item's Answer = "guessed at lock: [choice]", Answered by = "system", Status = Resolved, clear Digest #.
- If no choice can be taken from the Question, leave the row as it is and put "UNCLEAR ORDER: [original message]" in Needs attention.
Late order items for this day stay open (Mark decides); list them in the doc.
For each Sales item that is not Resolved, whose Question contains "asked to change their weekly share", for a customer in this day's rows, and whose Week is this delivery's week: leave the row as it is (never guess a share change) and add "SHARE REQUEST NOT SETTLED: check with Mark" to that row's Needs attention, exactly this wording (never the customer's words). The item stays open.

STEP 3. LOCK
Fill "Locked" = now on every one of this day's rows that is blank.

STEP 4. MAKE THE LIST (the script makes it; never lay it out yourself)
1. Make a new empty folder `dl` and write `dl/day.json` in exactly the form of tools/sample-delivery-day.json:
   - "farm": "Restoration Farmstead", "day": the weekday name, "date": the delivery date yyyy-mm-dd, "locked_at": when you locked, written like "Sun Oct 11, 7:40pm", "made": the Eastern time now, written like "Oct 11 7:41PM".
   - "drivers": {"[Route]": "[Driver]", ...} from the Routes tab rows for this weekday (leave out a route whose Driver is blank).
   - "products": one {"column": [Column name], "unit": [Unit]} per Products row whose Active is Yes, in Products order.
   - "rows": one per Day row (Step 3's rows, test rows already left out). From the week row: "cust_id", "name", "stop" (Stop #), "route" (Route), "changes" (the whole Changes cell), "needs_attention" (Needs attention), and "quantities": {"[Column name]": [cell], ...} for every product cell that isn't blank. From Customers (same Cust ID): "address", "city", "phone" (Phone), "phone2" (Phone 2), "delivery_notes" (Delivery notes), "standing_milk" (Customers Milk (gal)). Copy every value exactly as the cell reads; "" for a blank. Never add, round or fix anything.
   - "pending": one {"customer": [Customer], "asked_for": [what they asked for]} per open Late order Queue item for this day.
   Count the Day rows and check "rows" has the same number before running.
2. Run `python3 -I ops/tools/delivery_list_pdf.py dl/day.json dl/list.pdf`. It prints one line of JSON. If it prints "error" or "rows_read" isn't your count, fix day.json and run it again; if it still fails, add a Problem and go to 5 (fallback).
3. Save dl/list.pdf into Delivery Lists as a PDF file (type application/pdf) named the script's "file_name". It must stay a PDF: never convert it to a Google Doc. The file is plain text on purpose: if the Drive tool takes the file's contents as text, give it the file's text exactly; if it wants base64, run `base64 -i dl/list.pdf` and give it that output exactly. Never retype, shorten or rearrange either.
4. Check the saved file: if Drive shows its size, it must equal the script's "bytes". If your Drive tool can read the file back, its text must contain every one of the script's "check_words". If a check fails, the file was damaged on the way: leave it (never delete), add a Problem "delivery list PDF damaged: [which check]", and go to 5.
5. Fallback, only if the PDF couldn't be made or saved: run `python3 -I ops/tools/delivery_list_html.py dl/day.json dl/list.html` and create the Google Doc "Delivery list [Ddd Mon D YYYY]" in Delivery Lists from dl/list.html (give the file's contents exactly, source type text/html, so Drive converts it into a Google Doc). If even that fails, make the doc from dl/list.txt's text exactly. Either way add a Problem and, unless it's quiet hours, text Shane (one-to-one) once: "Delivery list for [Day] went out as a Doc, not the PDF: [reason]". Never lay it out yourself.

WHAT THE SCRIPT MAKES (for reference; the script decides, so never change its output to match this)
The approved design, one section per route (Route column; if blank, one section for the day), each starting on a new page:
- A cream header band with the farm logo at the top left (website colors: cream, maroon text, sage lines, navy links): "[WEEKDAY] · [Mon D, YYYY]", then "[Route, or All [Day] stops] · Driver: [Routes tab Driver, or a blank line] · Locked [time]".
- Four tiles: STOPS TO DELIVER, SKIPPING, MILK JARS, ADD-ON ITEMS.
- A box: "X  DO NOT DELIVER" with each skip (a stop whose row has every product at 0 or blank this week, however it got there: "Stop [#]: [Name], [Address, City]: SKIP, nothing to deliver this week"), then "NO MILK THIS WEEK (add-ons only)" (Milk (gal) 0 this week while their Customers Milk (gal) is above 0: "Stop [#]: [Name]: NO MILK, add-ons only"). Thick border when there are any; otherwise "No skips this week".
- PACKING LIST with a tick box per line: Milk first as half-gallon jars (gallons x 2, plus Extra Milk jars, "including [n] extra"), then every add-on above 0 with its unit (sheets-spec TERMS: half-gallon jars only).
- STOPS in Stop # order, every Day row in its place, skips included (shaded): DONE tick box | STOP | CUSTOMER (name, address as a map link, city, then the phone written like (502) 555-1234 as a tap-to-call link, Phone 2 on the line below, "no phone" if both are blank; NO TEXTS customers too, nothing is texted) | DELIVER ("2 jars + 1 extra", then "2 x Yogurt VM" lines; a skip is "SKIP: NO DELIVERY"; "NO MILK" when it applies) | NOTES (Delivery notes) | FLAGS (SKIP, NO MILK, GUESS, CHANGED for a change that isn't "(standing order sync)", "!" for a blank Stop #, other Needs attention text, a share that isn't whole jars, or a cell that isn't a number or an active product, which shows as CHECK).
- CHANGES THIS WEEK: one line per stop with a real Changes entry or Needs attention text.
- PENDING: NOT PACKED, only if there are open Late order items.
The fallback Doc (delivery_list_html.py) has the same sections in the same order.

STEP 5. SEND
- Text the family group (sheets-spec rule 11) and Harry (one-to-one) the same text: the script's "message" with {LINK} replaced by the list's link (the PDF, or the fallback Doc) ("[Day]'s delivery list is ready: [link]. [n] stops to deliver, [routes]. [s] skipping (boxed at the top). [g] guesses marked. Shares and orders for [Day] are now locked.").
- Log each text in the Inbox Log (Out (system)).
- Fill that day's "Delivery list sent" = now.

FINISH
Report to the operator: day, stops, guesses, pending items.

=====================================================
MORNING EXCEPTIONS (run only this part when the operator says so)
=====================================================
Changes approved after the list went out (Mark said "add it" to a Late order) must reach Harry before he leaves.
1. Delivery day = today. New exceptions = today's customer rows with a Changes entry containing "after lock" that is later than today's "Exceptions sent" (all of them if it's blank).
2. Text the family group and Harry (one-to-one) the same message:
   "Changes to today's ([Day]) delivery list:
   - [Name], stop [#]: [what changed, e.g. +2 Yogurt VM; if their whole order is now 0: SKIP, no delivery today]
   Harry, reply GOT IT when you have these."
3. If the day's list is a Google Doc (the fallback), append the same lines to it under a heading "ADDED AFTER LIST WENT OUT". A PDF can't be changed: skip this step (the text is the record).
4. Create a Queue item: Type Driver, Week, Question = "Got today's added items? ([names]) Reply GOT IT", Status = Waiting. (delivery-check sends and re-asks it; the parser records Harry's answer.)
5. Set today's "Exceptions sent" = now. Log each text in the Inbox Log.
