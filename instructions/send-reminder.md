SEND REMINDER (version 6)
Written for: sheets-spec version 4

Change log
- v6 (2026-10-08): one text per phone number (shared numbers); NO TEXTS customers skipped; late approval moves the reply-by time.
- v5 (2026-10-08): cutoff line no longer says "your order" (milk is a weekly share).
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v4 (2026-10-08): Laura is asked for the wording after Nudge after hours (3), not 1 hour.
- v3 (2026-10-08): waits for any open list approval (sheets-spec rule 9).
- v2 (2026-10-07): preview waits while an invoice list is waiting on Mark (approvals never both open).
- v1 (2026-10-07): first version.

HOW TO WORK
A checklist. Every stage is decided by cells in the header block of NEXT week's tab (sheets-spec WEEK NAMES; on Fri Oct 9 2026 that is Week 1). Do exactly ONE stage per run: the first one whose condition is true, then finish. The only judgment is the wording check in Stage C.

Every text you send: log it in the Inbox Log right away as sheets-spec rule 7 says (Direction "Out (system)", the number, the exact text, Quo message ID "pending"). Times in texts are friendly ("Sat Oct 10, 6pm").
"Nudge after" = Config "Nudge after (hours)".

STAGE A. ASK FOR WORDING
Condition: "Reminder requested" is blank.
- Text Mark: "Good morning! Please text back this week's reminder for customers (deliveries Mon [date] to Fri [date]). I'll send you a preview before anything goes out."
- Fill "Reminder requested" and "Reminder last asked" = now. Finish.

STAGE B. WAITING FOR WORDING
Condition: "Reminder wording received" is blank.
- If "Reminder asked Laura" is blank and "Reminder last asked" is at least Nudge after hours ago (3 hours: a 9am request reaches Laura at the noon run): text Laura "Hi Laura, Mark hasn't sent this week's customer reminder yet. Could either of you text it back?" Fill "Reminder asked Laura" and "Reminder last asked" = now.
- Else if "Reminder last asked" is at least Nudge after hours ago: text Mark and Laura "Still need this week's customer reminder wording when you get a chance." Set "Reminder last asked" = now.
- Otherwise do nothing. Finish.

STAGE C. CHECK AND PREVIEW
Condition: "Reminder wording" is filled, AND "Reminder approved" is blank, AND ("Reminder preview sent" is blank or older than "Reminder wording updated"), AND ("Reminder check failed" is blank or older than "Reminder wording updated").
0. If a Queue item of Type Invoice or Read-back has Status Sent (Mark has a list open, sheets-spec rule 9), do nothing this run; the preview goes out once that list is answered. Finish.
1. Sanity check the wording. It FAILS if any of these is true:
   - blank, garbled, or cut off mid-sentence
   - mentions a date or weekday that doesn't match next week's delivery days or the asked-for cutoff
   - longer than 300 characters (before the cutoff line is added)
   - reads like a personal reply ("ok sounds good", "call me") rather than a message to customers
   - doesn't make sense as a reminder to order, or is wildly unlike past reminders (past "Reminder final text" values in earlier week tabs, if any)
   If it fails: text whoever sent the wording (Mark or Laura): "This week's reminder didn't look right: [one-line reason]. Can you send it again?" Set "Reminder check failed" = now. Finish.
2. Format it: Mark's wording with spelling mistakes fixed (change nothing else), then a new line: "Reply with any changes for this week by [asked-for cutoff, e.g. Sat Oct 10, 6pm]." No prefix. If the asked-for cutoff is less than 6 hours from now, use "Sun [date], 2pm" instead.
3. Set "Reminder final text" to exactly that.
4. Send the final text, exactly as customers will get it, to Mark and to Laura (one text each).
5. Then send each of them a second text:
   "That's the preview. Reply YES to send it to [N] customers[ if Mode is not LIVE: ' (TEST mode: only the test phones will get it)']. Or text changes."
   If you fixed spelling, add: "Fixed: [wrong] > [right], [wrong] > [right]."
   N = customer rows on next week's tab with a Phone.
6. Set "Reminder preview sent" and "Reminder last asked" = now. Finish.

STAGE D. WAITING FOR APPROVAL
Condition: "Reminder preview sent" is filled and "Reminder approved" is blank.
- If "Reminder last asked" is at least Nudge after hours ago: text Mark and Laura "The customer reminder is still waiting for your YES (preview sent [time])." Set "Reminder last asked" = now.
- Otherwise do nothing. Finish.

STAGE E. SEND
Condition: "Reminder approved" is filled and "Reminder sent" is blank.
Check that "Reminder approved" is later than "Reminder preview sent" and the preview is later than "Reminder wording updated". If not, do nothing, add a Problem "approval is older than the current wording", and finish.

If Config Mode is not LIVE (TEST):
- If "Reminder test sent" is filled: do nothing. Finish.
- Send "Reminder final text" to each test phone (Config "Test phones" roles), once each.
- Set "Reminder test sent" = now. Do not touch customer rows or "Reminder sent". Finish.

If Mode is LIVE:
1. Recipients = customer rows on next week's tab (never Cust IDs starting with "T") where "Reminder sent" is blank and the customer has a Phone (Customers tab). Rows with no phone: skip them and remember their names. Rows whose Customers "Notes" contains "NO TEXTS": skip them, fill their "Reminder sent" with "opted out". Shared numbers: if several rows have the same Phone, send to that number once and stamp every row that shares it. No number may appear twice in a batch.
2. Duplicate guard: fetch the farm number's sent messages since "Reminder approved". Any recipient whose number already received "Reminder final text": fill that row's "Reminder sent" with the time Quo shows, and remove them from the list.
3. Send "Reminder final text" in batches of Config "Bulk send batch size" (individual texts, never a group text). Right after EACH batch, before the next one: fill "Reminder sent" = now on every row in that batch, and log the sends in the Inbox Log.
4. If a send or a sheet write fails: stop sending, add a Problem saying how far it got, and finish. The next run continues from the blank rows (and the duplicate guard catches anything sent but not stamped).
5. When no blank rows with a phone remain: fill "Reminder sent" (header) = now and "Reminder sent count" = "[sent]/[total rows]" plus ", [n] no phone" if any.
6. Text Mark: "Reminder sent to [sent] customers.[ No phone: names.]" Finish.

FINISH
Report to the operator: which stage ran and how many texts were sent.
