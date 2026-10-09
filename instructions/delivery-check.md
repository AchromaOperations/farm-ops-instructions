DELIVERY CHECK (version 1)
Written for: sheets-spec version 4

Change log
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v1 (2026-10-07): first version.

HOW TO WORK
A checklist. No judgment: the parser reads Harry's replies; this step only asks. Every text you send: log it in the Inbox Log right away (Direction "Out (system)", Quo message ID). Only text Harry and Mark.

Open days = day rows in LAST or THIS week with "Delivery list sent" filled, "Route confirmed" blank, and (the day is before today, or it is today and now is at or after "Route check start").
Last hour = the hour before Config "Quiet hours start" (20:00 when quiet hours start at 21:00).

STEP 1. HARRY'S OPEN QUESTIONS (Driver items)
For each Queue item of Type Driver:
- Status Waiting: text Harry its Question. Status = Sent, Sent to = Harry, First sent = now.
- Status Sent, no Answer, and (Last nudged, else First sent) at least 55 minutes ago: text Harry "Still need this: [Question]". Last nudged = now.

STEP 2. ROUTE QUESTION
For the open days whose "Harry last asked" is blank or at least 55 minutes ago:
- One text to Harry. One open day: "Route done for [Day]? Everything delivered? Yes/No". Several: "Routes done for [Day] and [Day]? Everything delivered? Yes/No (tell me which if only some)".
- On each of those day rows: "Harry last asked" = now, "Harry ask count" = count + 1.
(Skip a day in this step if Step 1 just texted Harry a Driver question about that same day; the Driver question comes first.)

STEP 3. TELL MARK
For each open day whose "Mark alerted" is blank, where the day is before today, OR it is today and this run is in the Last hour:
- Text Mark: "Haven't heard from Harry about [Day]'s route. Asked [count] times."
- Fill "Mark alerted" = now.

FINISH
Report to the operator: days still open, texts sent.
