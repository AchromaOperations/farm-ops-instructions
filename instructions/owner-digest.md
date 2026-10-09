OWNER DIGEST (version 3)
Written for: sheets-spec version 4

Change log
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
- "Nudge after" and "Laura after" = Config hours. Batch size = Config "Digest batch size".
- Driver items are not handled here (delivery-check sends those). Reminder texts are not handled here (send-reminder does).

STEP 1. MOVE STALE INVOICE HOLDS
Any Clarify item whose Question starts with "Invoice" and that has been Sent for 24 hours with no Answer: create a Sales item with the same customer and question (customer service follow-up), then set the Clarify item's Answer = "moved to Sales Q[n]", Status = Resolved, clear its Digest #.

STEP 2. NUDGES (for items already sent)
a. Invoice pending: if (Last nudged, else First sent) is at least Nudge after hours ago, text Mark: "[Invoices for [day] / Customer read-backs] still need your OK: [link]. Reply 'good' or 'good except [numbers]'." If First sent is at least Laura after hours ago and Sent to doesn't include Laura, send the same text to Laura and add Laura to Sent to. Set Last nudged = now.
b. Open batch: items with Status Sent and NO Answer, where (Last nudged, else First sent) is at least Nudge after hours ago. Text Mark one message: "Still waiting on [numbers]:" followed by each item's "[Digest #]. [Question]". If any of them was First sent at least Laura after hours ago and Laura isn't in Sent to: also send the same message to Laura and add Laura to Sent to. Set Last nudged = now on each.
   (Items with an Answer but not Resolved, such as Sales answers without an outcome, are not nudged.)

STEP 3. NEW ITEMS
Waiting items = Type Clarify, Sales, Late order or Other with Status "Waiting". If there are none, finish.
- If Invoice pending OR an open batch has any unanswered item: send ONLY the urgent Waiting items (if any). Otherwise send the next batch.
- Next batch = up to Batch size Waiting items: urgent first, then oldest Created first.
- Number them: the lowest Digest # values not used by any open item, starting at 1.
- Text Mark one message:
  "Questions (reply with the number and your answer):
  1. [Question]
  2. [Question]
  [if more are waiting:] ([n] more waiting after these)"
  Mark urgent items with "(for tomorrow)" or "(for today)" after the question.
  After each Sales item add "(reply to the customer yourself; answer here with sale / no sale / resolved)".
- For each item sent: Status = Sent, Digest # = its number, Sent to = Mark, First sent = now.

FINISH
Report to the operator: nudges sent, new items sent, items still waiting.
