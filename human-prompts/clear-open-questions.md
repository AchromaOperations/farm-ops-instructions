# Clearing open questions by hand

Use this when a digest keeps coming back ("Still waiting on these (reply with the number and your answer): ..."), nobody is answering it, and "(n more waiting after these)" keeps growing.

## What is going on

- Every numbered line in a digest is a Queue row waiting for an answer in the family group. The routine asks again every "Follow-up every (minutes)" (Config) until it has one. While any sent question is unanswered, new questions wait behind it; only urgent ones (a delivery today or tomorrow, or a held invoice) go out early. So one ignored question holds up the rest.
- Fixing the thing somewhere else never answers the question. Canceling or deleting an invoice in Square, paying it, or changing the sheet leaves an "Unpaid 14+ days" question open: it was asking Mark whether to follow up with the customer, and only an answer closes it. (One exception since parser v39: a text sent to that customer from the Quo app closes their open customer-service questions.)
- Shane's texts don't count. The parser reads digest answers only from Mark and Laura, in the family group.

## 1. By text (Mark or Laura, in the family group)

Reply with the number and a closing word, one item per line:

    2 resolved

- A customer-service ("Sales") question takes "sale", "no sale" or "resolved". A question that asks something ("which yogurt?", "replacement invoice number?") takes the answer it asks for. A driver question is answered by the driver, not here.
- The next run closes it and sends the next batch with fresh numbers. Answer those the same way. Numbers are reused, so always answer the latest digest, not an old screenshot.
- Done the customer-service part already by texting the customer from the Quo app? Then it is closed on the next run and the group gets a "Closed #n" reply; nothing more to do.

## 2. By hand (Shane, through a chat on the farm's Claude)

Paste this into a normal chat, with the Q# or the customer and digest number, and the reason:

    I'm Shane. Close Queue item Q[number] by hand. Reason: [why it needs nothing more]. Follow CLOSING A QUEUE ITEM BY HAND in https://raw.githubusercontent.com/AchromaOperations/farm-ops-instructions/main/instructions/manual-edits.md and change nothing else.

The chat writes only that row's tracker cells (Answer "closed by hand: ...", Answered by "Shane (chat)", Status and Outcome Resolved, Resolved, Digest # cleared). The question leaves the next digest; Mark and Laura are not told. Shane can write the same cells himself in the sheet instead, using exactly those values.

## 3. The invoice itself (when it was canceled or deleted in Square)

Closing the question does not change the invoice's standing in the sheets. The row still counts as unpaid, the daily payment check keeps looking, and the invoice is listed on that customer's next pay-link text, until its Paid cell is filled.

- Canceled in Square and still visible there: nothing to do. The next daily payment check sees it, puts a "Canceled invoice: ... replacement?" question in the digest; answer it with "none" (or the replacement's invoice number). That fills Paid.
- Deleted (Square no longer shows it), or you want it settled now: paste into a chat

      I'm Shane. [Customer]'s [delivery date] invoice ($[amount], sent [date]) was canceled in Square and won't be replaced. Follow INVOICE CANCELED OR DELETED IN SQUARE in https://raw.githubusercontent.com/AchromaOperations/farm-ops-instructions/main/instructions/manual-edits.md and change nothing else.

  The chat fills Paid = "none: invoice canceled (Shane (chat))" and notes it in Needs attention.
- A replacement invoice was sent by hand: don't close anything. Wait for the "Canceled invoice:" question and answer it with the new invoice number, so the row points at the replacement and its payment is tracked.

## Never

- Delete Queue rows, or edit any Queue cell other than the tracker cells named above.
- Change a filled Paid, "Invoice sent" or "Invoice link".
- Close a question for a customer who is still waiting on an answer: closing it tells no one.
