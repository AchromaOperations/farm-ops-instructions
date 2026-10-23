INVOICING (version 11)
Written for: sheets-spec version 4

HOW TO WORK
A checklist in parts. Do every part whose condition is true, in order. No judgment: amounts come from the week tab and prices from the Products tab. Every text you send: log it in the Inbox Log right away as sheets-spec rule 7 says (Direction "Out (system)", the number, the exact text, Quo message ID "pending").

Only products whose Products "Billed through" is Square are invoiced. The weekly share (Milk (gal), paid as the monthly herdshare through Squarespace) never is.

HELD DAYS
A day is held when its day row's "Invoice hold" is filled (sheets-spec DAY TABLE; a tab without that column has no holds). For a held day, Parts A, A2, B, C and C2 do nothing: no drafts, no list, no sending, no payment-link texts, for that day or its customer rows. Part D still checks payments. Never clear or change "Invoice hold"; only Shane does. If you think a day should be held, follow routines/farm-ops.md SYSTEM PROBLEMS. A hold that's only in run notes or a Problem holds nothing, so never skip a day for any other reason this doc doesn't give.

PART A. DRAFT
For each day row in LAST or THIS week with "Route confirmed" filled, "Invoices drafted" blank and "Invoice hold" blank:
1. If any Queue item of Type Driver whose day (sheets-spec Queue) is that day is not Resolved, skip this day (Harry's answers may still change what was delivered).
2. For each customer row of that day with "Delivered" filled and "Invoice link" blank (skip Cust IDs starting with "T"):
   - Lines = each Square-billed product with quantity above 0, minus any amount for that product in "Not delivered" and any in "No charge" (a tab without a "No charge" column has none). Drop lines that reach 0 or less. Remember the no-charge items for the list (step 3).
   - No lines: fill "Invoice link" = "none". Next customer.
   - Any line whose product has a blank Price: do not draft this customer. Create a Clarify item "Invoice for [name] held: no price set for [product]." Put "Invoice held: no price for [product]" in Needs attention. Next customer.
   - No email on the Customers tab: do not draft. Put "Invoice held: no email" in Needs attention (if not already there) and create a Clarify item "No email for [name], so their invoice ($[total]) is held. Text me their email." Next customer.
   - Find the customer in Square by email, then by phone. If not found, create the Square customer with name, email and phone.
   - Extra Milk is priced by the customer's share (their Customers "Milk (gal)"): 1 gallon or more = the Products Price for Extra Milk; less than 1 gallon (a half share) = Config "Extra milk price, half share". If that Config value is missing or blank and this customer has a half share, hold this customer the same way as a blank Price.
   - Create a DRAFT Square invoice (do not publish or send it) with the lines at the current Products prices (Extra Milk as above, per half-gallon jar).
   - Fill "Invoice link" with the Square invoice link.
3. The list text. The drafted customers = every customer row of that day with a real Square link in "Invoice link" and "Invoice sent" blank, whether drafted just now or by an earlier run that stopped part way (never draft those again). Write it in this form (large plain text in the Doc, no colors):
   "Invoices for [Day, date]. Reply 'good' to send all, or 'good except [numbers]'."
   Then one numbered line per drafted customer: "[#]. [Name] ([Cust ID]): [items with amounts] = $[total]  [link]", adding " (no charge: [items])" when the row had no-charge items. A customer whose items were all no charge has no invoice ("Invoice link" = "none"); list them at the end as "No charge: [name] ([items])".
   Then: "Total: $[sum] for [n] invoices." Then any held customers: "Held: [name], [reason]".
   Make the Google Doc "Invoices [Ddd Mon D YYYY]" in Invoice Lists from it, exactly as instructions/save-doc.md says. If save-doc.md says it failed, go on to step 4 anyway, with the list text in place of the link.
4. Fill "Invoices drafted" = now on the day row. Create a Queue item: Type Invoice, Week, Question = the doc link (or, if the Doc failed, the whole list text), Original message = "[Day] invoices: [n], $[sum]", Status = Waiting.
   (If there were no drafted invoices at all, fill "Invoices approved" and "Invoices sent" with "none" instead, and skip the Queue item.)

PART A2. HELD FOR EMAIL
For customer rows in LAST or THIS week whose Needs attention contains "no email", "Invoice link" is blank, and the Customers tab now has an email (skip rows of a held day): draft them as in Part A step 2, then make a supplemental list doc "Invoices [Ddd Mon D YYYY] (added)" and Queue item exactly as in Part A steps 3 and 4, listing only the customers drafted in this part (do not change the day row's "Invoices drafted").

PART B. ASK FOR APPROVAL (one approval open at a time)
Only if ALL of these are true:
- no approval is open (sheets-spec rule 9), AND
- no Queue item of Type Read-back has Status Waiting (read-back lists go before invoice lists), AND
- NEXT week's reminder preview is not about to go out (week-names.md): NOT the case that "Reminder wording" is filled, "Reminder approved" is blank, and "Reminder preview sent" is blank or older than "Reminder wording updated". (A reminder still waiting for wording does not block invoices.)
Then take the oldest Invoice item with Status Waiting whose day isn't held (its day = the weekday its Original message starts with, in its Week's tab):
- Text the family group the list as sheets-spec rules 10 and 11 say, from its list doc (or from its Question, when that holds the list text instead of a link). Title: "Invoices for [Day, date]: [n], $[sum]". Lines: "[#]. [Name]: [items with amounts] = $[total]" (no Square links), with " (no charge: [items])" as in the list doc. Closing lines: "Total: $[sum] for [n] invoices." and, if any, "Held: [name] ([reason])". Then "Approved invoices are emailed by Square and each customer gets a text with their payment link."
- Status = Sent, Sent to = Group, First sent = now.
(Nudges and Laura are handled by owner-digest.)

PART C. SEND APPROVED INVOICES
For each customer row in LAST or THIS week with "Invoice approved" filled and "Invoice sent" blank (skip rows of a held day; they send once Shane clears the hold):
- If Config Mode is not LIVE: do not send. Put "TEST: invoice not sent" in Needs attention if it isn't there already. Next.
- Publish and send that Square invoice (Square delivers it to the customer). Then immediately fill "Invoice sent" = now.
- If Square fails: stop Part C, add a Problem, continue to Part D.
Then for each day row with "Invoices drafted" filled, "Invoices sent" blank and "Invoice hold" blank: if its Invoice Queue item is Resolved, fill "Invoices approved" = the time it was resolved (if blank). If also every customer row of that day with a real Invoice link has "Invoice sent" filled or a "held" or "TEST" note in Needs attention, fill "Invoices sent" = now.

PART C2. TEXT THE PAYMENT LINK (Shane's rule from 2026-10-18)
For each customer row in LAST or THIS week with "Invoice sent" filled on or after 2026-10-18 00:00 and "Pay link texted" blank, not on a held day (if the tab has no "Pay link texted" column, add it at the end of the customer table's header row first, sheets-spec rule 8):
- Only between 8:00am and 9:00pm Eastern and while Config Mode is LIVE. Outside those hours, leave it blank: a later run sends it.
- No phone on the Customers tab: fill "Pay link texted" = "skipped: no phone". Customers "Notes" contains "NO TEXTS": fill "skipped: opted out". Next.
- Link = that invoice's public payment page from Square (the invoice's public URL, which exists once it is published). Never the Square dashboard link in "Invoice link". If Square gives no public URL, add an ALERT Problem and leave it blank so a later run tries again; once that invoice was sent more than 24 hours ago, fill "skipped: no payment link from Square" instead, so it stops retrying.
- Duplicate guard: if the farm number already sent that customer a text containing this link (Quo sent messages since "Invoice sent"), just fill "Pay link texted" with that time.
- Text the customer's Phone exactly: "Hi from Restoration Farmstead! Your invoice for [Weekday]'s delivery ([Mon D]) is $[total] for [items]. You can pay here: [link] Thank you!"
  Items = the invoice's lines as in read-backs (Products "Text name", e.g. "2 vanilla maple yogurts and a dozen eggs"; Extra Milk as "an extra half gallon" / "an extra gallon"). Total with cents ($14.00). Never mention the weekly share.
- Right after sending, fill "Pay link texted" = now and read it back (routines/farm-ops.md: a cell that records a text went out). Log the text in the Inbox Log (sheets-spec rule 7).

PART D. PAYMENTS (at most once a day)
If System "Last payment check" is blank or at least 24 hours ago:
- For each customer row in the last 8 week tabs with "Invoice sent" filled and "Paid" blank: ask Square for that invoice's status. Paid = fill "Paid" with the payment date.
- Canceled in Square (Shane's rule from 2026-10-23: Mark sometimes cancels an invoice and sends a corrected one by hand, as with Cayli's 000049 and 000050). Never mark it overdue. If its Needs attention doesn't already contain "invoice #[this invoice's number] canceled in Square":
  - Add "invoice #[number] canceled in Square" to Needs attention.
  - Look in Square for that customer's invoices created after this one that aren't canceled.
  - Create a Clarify item (Week, Cust ID and Customer from the row). Exactly one found: Question = "Canceled invoice: [name]'s [Ddd Mon D] invoice #[number] ($[amount]) was canceled in Square. Is #[new number] ($[its amount]) the replacement? Reply yes, another invoice number, or 'none'." None or several found: Question = "Canceled invoice: [name]'s [Ddd Mon D] invoice #[number] ($[amount]) was canceled in Square. What's the replacement's invoice number? Reply with it, or 'none'."
- Unpaid (not canceled) and sent at least 14 days ago, and Needs attention doesn't already say "overdue": add "overdue since [sent date], $[amount]" to Needs attention and create a Sales item "Unpaid 14+ days: [name], $[amount], sent [date]. Follow up?" (The system never contacts the customer about payment.)
- Set "Last payment check" = now.

PART D2. CANCELED INVOICE ANSWERS (every time invoicing runs)
For each Queue item of Type Clarify with Status Answered whose Question starts "Canceled invoice:" (the parser leaves these Answered for this part). The row = its customer's row on its Week's tab that has the canceled invoice.
- Which invoice the Answer means: an OK ("yes", "ok", "that's it") = the number its Question offered; an invoice number = that one; "none", "no", "no replacement" = none. Anything else: add "canceled invoice: fix by hand ('[Answer]')" to the row's Needs attention.
- An invoice: find it in Square. It must be the same customer's and not canceled. If so: set the row's "Invoice link" to its link, add "replaced by #[number] ([Answered by])" to Needs attention, and if Square shows it paid, fill "Paid" with the payment date (if not, Part D checks it from now on). If it isn't found, is another customer's, or is canceled: add "canceled invoice: #[number] not usable, fix by hand" to Needs attention.
- None: fill "Paid" = "none: invoice canceled ([Answered by])", so the payment check stops looking at it.
- Then set the item's Status = Resolved and Resolved = now. Never change "Invoice sent" or "Pay link texted" here, and never text the customer.

FINISH
Report to the operator: invoices drafted, lists sent for approval, invoices sent, payment links texted, payments recorded, canceled invoices asked about or settled, overdue flagged, days skipped because they're held.
