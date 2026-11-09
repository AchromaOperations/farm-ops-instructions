DELIVERY CHECK (version 5)
Written for: sheets-spec version 4

HOW TO WORK
A checklist. No judgment: the parser reads the drivers' replies; this step only asks. Every text you send: log it in the Inbox Log right away as sheets-spec rule 7 says (Direction "Out (system)", the number, the exact text, Quo message ID "pending"). Only text the drivers and the family group (Mark and Laura, sheets-spec rule 11).
The drivers = Harry (Config "Driver (Harry) phone") and Zi (Config "Driver 2 (Zi) phone"; Shane's rule, 2026-11-09). Every text to the drivers below goes to each of them as his own one-to-one text, the same words, each logged; a blank phone is skipped. Either driver may answer; the parser decides what a reply meant (parser B).

Open days = day rows in LAST or THIS week with "Delivery list sent" filled, "Route confirmed" blank, and (the day is before today, or it is today and now is at or after "Route check start").
Last hour = the hour before Config "Quiet hours start" (20:00 when quiet hours start at 21:00).

STEP 1. THE DRIVERS' OPEN QUESTIONS (Driver items)
A Driver item's day is the date its Question starts with ("Thu Oct 22: ..."), or for an older item without one, the date of its Created (sheets-spec Queue). Never text the drivers a question about a day long past: they can't tell it from today's. (On Oct 22 an Oct 14 question reached Harry and his "Yes" was misread.)
For each Queue item of Type Driver that is not Resolved, check these in order and use the first that fits:
- Expired: a "Got today's added items?" item whose day is before today. Don't text it. Set Answer = "expired: the day ended", Answered by = "system", Status = Resolved, Resolved = now. (Its changes were already texted that morning.)
- Too old to send: any other item with Status Waiting whose day is 2 or more days before today. Don't text it. Record an ALERT Problem "Driver question Q[n] for [day] was never sent: [Question]". Leave it Waiting, so that day's invoicing keeps waiting until Shane settles it.
- Status Waiting: text the drivers its Question. Status = Sent, Sent to = "Harry, Zi" (the drivers texted), First sent = now.
- Status Sent, no Answer, and (Last nudged, else First sent) at least 55 minutes ago: text the drivers "Still need this: [Question]". Last nudged = now.

STEP 2. ROUTE QUESTION
For the open days whose "Harry last asked" is blank or at least 55 minutes ago:
- One text to the drivers (the same text to each). One open day: "Route done for [Day]? Everything delivered? Yes/No. If anyone paid you cash, tell me who and how much." Several: "Routes done for [Day] and [Day]? Everything delivered? Yes/No (tell me which if only some). If anyone paid you cash, tell me who, which day and how much." (Shane's rule from 2026-11-03: a customer who paid a driver cash is marked paid and never invoiced; the parser records it.)
- On each of those day rows: "Harry last asked" = now, "Harry ask count" = count + 1 (the columns keep their names; they cover both drivers).
(Skip a day in this step if Step 1 just texted the drivers a Driver question about that same day; the Driver question comes first.)

STEP 3. TELL MARK
For each open day whose "Mark alerted" is blank, where the day is before today, OR it is today and this run is in the Last hour:
- Text the family group: "Haven't heard from Harry or Zi about [Day]'s route. Asked [count] times."
- Fill "Mark alerted" = now.

FINISH
Report to the operator: days still open, texts sent.
