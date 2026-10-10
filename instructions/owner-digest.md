OWNER DIGEST (version 6)
Written for: sheets-spec version 4

Change log
- v6 (2026-10-09): list follow-ups resend the list itself as text (sheets-spec rule 10), not a link.
- v5 (2026-10-09): Mark is followed up at every hourly run (Config "Follow-up every (minutes)", default 55), each follow-up lists every unanswered question; half-closed Sales items get one morning follow-up a day; Digest # stays taken until Resolved.
- v4 (2026-10-09): share requests from customers ask Mark for the change to make, or 'no change'.
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v3 (2026-10-08): nudges for read-back lists too.
- v2 (2026-10-07): Sales items remind Mark to reply to the customer directly.
- v1 (2026-10-07): first version.

HOW TO WORK
A checklist over the Queue tab. No judgment needed: the parser already wrote each item's Question. Every text you send: log it in the Inbox Log right away as sheets-spec rule 7 says (Direction "Out (system)", the number, the exact text, Quo message ID "pending"). Never send to anyone but Mark and Laura.

Definitions
- Open batch = Queue items of Type Clarify, Sales, Late order or Other with Status "Sent".
- Urgent = an item whose customer's delivery is today or tomorrow and whose week-tab row has Delivered blank. (Delivery list items need answers before the list locks.)
- Invoice pending = a Queue item of Type Invoice or Read-back with Status "Sent" (an open list approval).
- "Follow-up every" = Config "Follow-up every (minutes)"; missing or blank = 55 (Mark hears again at every hourly run).
- "Laura after" = Config "Laura after (hours)". Batch size = Config "Digest batch size".
- Half-closed = Sales items with Status "Answered" (Mark answered but didn't say sale / no sale / resolved).
- "Daily follow-up time" = Config "Daily follow-up time"; missing or blank = 08:00.
- Driver items are not handled here (delivery-check sends those). Reminder texts are not handled here (send-reminder does).

STEP 1. MOVE STALE INVOICE HOLDS
Any Clarify item whose Question starts with "Invoice" and that has been Sent for 24 hours with no Answer: create a Sales item with the same customer and question (customer service follow-up), then set the Clarify item's Answer = "moved to Sales Q[n]", Status = Resolved, clear its Digest #.

STEP 2. NUDGES (for items already sent)
a. Invoice pending: if (Last nudged, else First sent) is at least Follow-up every minutes ago, text Mark the whole list again from its list doc, as sheets-spec rule 10 says, with the title starting "Still need your OK: " (for example "Still need your OK: 3 customer read-backs"). If First sent is at least Laura after hours ago and Sent to doesn't include Laura, send the same list texts to Laura and add Laura to Sent to. Set Last nudged = now.
b. Open batch: unanswered items = Status Sent and NO Answer. If any of them has (Last nudged, else First sent) at least Follow-up every minutes ago: text Mark one message: "Still waiting on [numbers]:" followed by EVERY unanswered item's "[Digest #]. [Question]", then "([n] more waiting after these)" if any Waiting items exist. If any of them was First sent at least Laura after hours ago and Laura isn't in Sent to: also send the same message to Laura and add Laura to Sent to. Set Last nudged = now on each.
c. Half-closed, once a day: if now is at or after Daily follow-up time and any half-closed item has (Last nudged, else First sent) before today: text Mark one message: "Still open (reply with the number and sale / no sale / resolved):" followed by each such item's "[Digest #]. [Question] (you said: '[Answer]')", quoting at most 120 characters of the answer. Set Last nudged = now on each. Only Mark, never Laura.

STEP 3. NEW ITEMS
Waiting items = Type Clarify, Sales, Late order or Other with Status "Waiting". If there are none, finish.
- If Invoice pending OR an open batch has any unanswered item: send ONLY the urgent Waiting items (if any). Otherwise send the next batch.
- Next batch = up to Batch size Waiting items: urgent first, then oldest Created first.
- Number them: the lowest Digest # values not used by any item that isn't Resolved (half-closed items keep their numbers), starting at 1.
- Text Mark one message:
  "Questions (reply with the number and your answer):
  1. [Question]
  2. [Question]
  [if more are waiting:] ([n] more waiting after these)"
  Mark urgent items with "(for tomorrow)" or "(for today)" after the question.
  After each Sales item add "(reply to the customer yourself; answer here with sale / no sale / resolved)". Except a share request (Question contains "asked to change their weekly share"): add "(reply to the customer yourself; answer here with the change to make, or 'no change')" instead.
- For each item sent: Status = Sent, Digest # = its number, Sent to = Mark, First sent = now.

FINISH
Report to the operator: nudges sent, new items sent, items still waiting.
