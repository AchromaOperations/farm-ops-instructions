OWNER DIGEST (version 8)
Written for: sheets-spec version 4

Change log
- v8 (2026-10-10): everything goes to the family group (sheets-spec rule 11), Laura's 6-hour copy is gone; a follow-up tops the open questions back up to Batch size.
- v7 (2026-10-10): quotes go out in full (a Question cut short with "..." is sent with its full Original message instead); texts over 1,500 characters are split.
- v6 (2026-10-09): list follow-ups resend the list itself as text (sheets-spec rule 10), not a link.
- v5 (2026-10-09): Mark is followed up at every hourly run (Config "Follow-up every (minutes)", default 55), each follow-up lists every unanswered question; half-closed Sales items get one morning follow-up a day; Digest # stays taken until Resolved.
- v4 (2026-10-09): share requests from customers ask Mark for the change to make, or 'no change'.
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v3 (2026-10-08): nudges for read-back lists too.
- v2 (2026-10-07): Sales items remind Mark to reply to the customer directly.
- v1 (2026-10-07): first version.

HOW TO WORK
A checklist over the Queue tab. No judgment needed: the parser already wrote each item's Question. Every text you send: log it in the Inbox Log right away as sheets-spec rule 7 says (Direction "Out (system)", the number, the exact text, Quo message ID "pending"). Every text goes to the family group (sheets-spec rule 11), never to anyone else.

Definitions
- Open batch = Queue items of Type Clarify, Sales, Late order or Other with Status "Sent".
- Urgent = an item whose customer's delivery is today or tomorrow and whose week-tab row has Delivered blank. (Delivery list items need answers before the list locks.)
- Invoice pending = a Queue item of Type Invoice or Read-back with Status "Sent" (an open list approval).
- "Follow-up every" = Config "Follow-up every (minutes)"; missing or blank = 55 (Mark hears again at every hourly run).
- Batch size = Config "Digest batch size".
- Half-closed = Sales items with Status "Answered" (Mark or Laura answered but didn't say sale / no sale / resolved).
- "Daily follow-up time" = Config "Daily follow-up time"; missing or blank = 08:00.
- Driver items are not handled here (delivery-check sends those). Reminder texts are not handled here (send-reminder does).
- Quotes in full: every quoted message goes out whole. If a Question's quote was cut short (it ends with "..." or "…" inside the quote marks) and the item's Original message has the full text, send the full Original message in its place. Never shorten a quote yourself.
- Long texts: if a text would be over 1,500 characters, split it between questions into texts of at most 1,500 characters, each starting "(1 of 2)", "(2 of 2)" and so on; the first keeps the opening line.

STEP 1. MOVE STALE INVOICE HOLDS
Any Clarify item whose Question starts with "Invoice" and that has been Sent for 24 hours with no Answer: create a Sales item with the same customer and question (customer service follow-up), then set the Clarify item's Answer = "moved to Sales Q[n]", Status = Resolved, clear its Digest #.

STEP 2. NUDGES (for items already sent)
a. Invoice pending: if (Last nudged, else First sent) is at least Follow-up every minutes ago, text the family group the whole list again from its list doc, as sheets-spec rule 10 says, with the title starting "Still need your OK: " (for example "Still need your OK: 3 customer read-backs"). Set Last nudged = now.
b. Open batch: unanswered items = Status Sent and NO Answer. If any of them has (Last nudged, else First sent) at least Follow-up every minutes ago, send one follow-up:
   - Top up first: if fewer than Batch size items are unanswered, add Waiting items (urgent first, then oldest Created) until there are Batch size, or none are left. While Invoice pending, add only urgent ones. Number them as Step 3 does, and set each added item's Status = Sent, Digest #, Sent to = Group, First sent = now.
   - Text the family group one message: "Still waiting on these (reply with the number and your answer):" then every unanswered item's "[Digest #]. [Question]", the added ones last with "(new)" after each, with the same urgent and Sales notes as Step 3, then "([n] more waiting after these)" if Waiting items remain.
   - Set Last nudged = now on each item that was already sent before this follow-up.
c. Half-closed, once a day: if now is at or after Daily follow-up time and any half-closed item has (Last nudged, else First sent) before today: text the family group one message: "Still open (reply with the number and sale / no sale / resolved):" followed by each such item's "[Digest #]. [Question] (answer so far: '[Answer]')", quoting the answer in full. Set Last nudged = now on each.

STEP 3. NEW ITEMS
Waiting items = Type Clarify, Sales, Late order or Other with Status "Waiting". If there are none, finish.
- If Invoice pending OR an open batch has any unanswered item: send ONLY the urgent Waiting items (if any). Otherwise send the next batch.
- Next batch = up to Batch size Waiting items: urgent first, then oldest Created first.
- Number them: the lowest Digest # values not used by any item that isn't Resolved (half-closed items keep their numbers), starting at 1.
- Text the family group one message:
  "Questions (reply with the number and your answer):
  1. [Question]
  2. [Question]
  [if more are waiting:] ([n] more waiting after these)"
  Mark urgent items with "(for tomorrow)" or "(for today)" after the question.
  After each Sales item add "(reply to the customer yourself; answer here with sale / no sale / resolved)". Except a share request (Question contains "asked to change their weekly share"): add "(reply to the customer yourself; answer here with the change to make, or 'no change')" instead.
- For each item sent: Status = Sent, Digest # = its number, Sent to = Group, First sent = now.

FINISH
Report to the operator: nudges sent, new items sent, items still waiting.
