INVOICING (version 4)
Written for: sheets-spec version 4

Change log
- v4 (2026-10-08): weekly share wording.
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v3 (2026-10-08): waits for any open approval (sheets-spec rule 9); read-back lists go first.
- v2 (2026-10-08 fix): NEXT week per sheets-spec WEEK NAMES.
- v2 (2026-10-07): never ask for invoice approval while a reminder approval is open; hold invoices for customers with no email.
- v1 (2026-10-07): first version.

HOW TO WORK
A checklist with four parts. Do every part whose condition is true, in order. No judgment: amounts come from the week tab and prices from the Products tab. Every text you send: log it in the Inbox Log right away as sheets-spec rule 7 says (Direction "Out (system)", the number, the exact text, Quo message ID "pending").

Only products whose Products "Billed through" is Square are invoiced. The weekly share (Milk (gal), paid as the monthly herdshare through Squarespace) never is.

PART A. DRAFT
For each day row in LAST or THIS week with "Route confirmed" filled and "Invoices drafted" blank:
1. If any Queue item of Type Driver for that day is not Resolved, skip this day (Harry's answers may still change what was delivered).
2. For each customer row of that day with "Delivered" filled and "Invoice link" blank (skip Cust IDs starting with "T"):
   - Lines = each Square-billed product with quantity above 0, minus any amount for that product in "Not delivered". Drop lines that reach 0.
   - No lines: fill "Invoice link" = "none". Next customer.
   - Any line whose product has a blank Price: do not draft this customer. Create a Clarify item "Invoice for [name] held: no price set for [product]." Put "Invoice held: no price for [product]" in Needs attention. Next customer.
   - No email on the Customers tab: do not draft. Put "Invoice held: no email" in Needs attention (if not already there) and create a Clarify item "No email for [name], so their invoice ($[total]) is held. Text me their email." Next customer.
   - Find the customer in Square by email, then by phone. If not found, create the Square customer with name, email and phone.
   - Create a DRAFT Square invoice (do not publish or send it) with the lines at the current Products prices.
   - Fill "Invoice link" with the Square invoice link.
3. Make (or, if it already exists, rebuild) the Google Doc "Invoices [Ddd Mon D YYYY]" in Invoice Lists. Large plain text, no colors:
   "Invoices for [Day, date]. Reply 'good' to send all, or 'good except [numbers]'."
   Then one numbered line per drafted customer: "[#]. [Name] ([Cust ID]): [items with amounts] = $[total]  [link]"
   Then: "Total: $[sum] for [n] invoices." Then any held customers: "Held: [name], [reason]".
4. Fill "Invoices drafted" = now on the day row. Create a Queue item: Type Invoice, Week, Question = the doc link, Original message = "[Day] invoices: [n], $[sum]", Status = Waiting.
   (If there were no drafted invoices at all, fill "Invoices approved" and "Invoices sent" with "none" instead, and skip the Queue item.)

PART A2. HELD FOR EMAIL
For customer rows in LAST or THIS week whose Needs attention contains "no email", "Invoice link" is blank, and the Customers tab now has an email: draft them as in Part A step 2, then make a supplemental list doc "Invoices [Ddd Mon D YYYY] (added)" and Queue item exactly as in Part A steps 3 and 4 (do not change the day row's "Invoices drafted").

PART B. ASK FOR APPROVAL (one approval open at a time)
Only if ALL of these are true:
- no approval is open (sheets-spec rule 9), AND
- no Queue item of Type Read-back has Status Waiting (read-back lists go before invoice lists), AND
- NEXT week's tab (sheets-spec WEEK NAMES; on Fri Oct 9 2026 that is Week 1) does not have a reminder waiting on approval ("Reminder requested" filled and "Reminder approved" blank).
Then take the oldest Invoice item with Status Waiting:
- Text Mark: "Invoices for [Day, date] are ready: [n] invoices, $[sum]. [doc link] Reply 'good' to send all, or 'good except [numbers]'." Nothing else in that text.
- Status = Sent, Sent to = Mark, First sent = now.
(Nudges and Laura are handled by owner-digest.)

PART C. SEND APPROVED INVOICES
For each customer row in LAST or THIS week with "Invoice approved" filled and "Invoice sent" blank:
- If Config Mode is not LIVE: do not send. Put "TEST: invoice not sent" in Needs attention if it isn't there already. Next.
- Publish and send that Square invoice (Square delivers it to the customer). Then immediately fill "Invoice sent" = now.
- If Square fails: stop Part C, add a Problem, continue to Part D.
Then for each day row with "Invoices drafted" filled and "Invoices sent" blank: if its Invoice Queue item is Resolved, fill "Invoices approved" = the time it was resolved (if blank). If also every customer row of that day with a real Invoice link has "Invoice sent" filled or a "held" or "TEST" note in Needs attention, fill "Invoices sent" = now.

PART D. PAYMENTS (at most once a day)
If System "Last payment check" is blank or at least 24 hours ago:
- For each customer row in the last 8 week tabs with "Invoice sent" filled and "Paid" blank: ask Square for that invoice's status. Paid = fill "Paid" with the payment date.
- Unpaid and sent at least 14 days ago, and Needs attention doesn't already say "overdue": add "overdue since [sent date], $[amount]" to Needs attention and create a Sales item "Unpaid 14+ days: [name], $[amount], sent [date]. Follow up?" (The system never contacts the customer about payment.)
- Set "Last payment check" = now.

FINISH
Report to the operator: invoices drafted, lists sent for approval, invoices sent, payments recorded, overdue flagged.
