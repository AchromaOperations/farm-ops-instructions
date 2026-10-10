OPERATOR (version 8)
Written for: sheets-spec version 4

Change log
- v8 (2026-10-10): confirm-orders is due for read-backs on any later built week too.
- v7 (2026-10-10): Step 0 b2 builds week tabs a few weeks ahead (Config "Weeks built ahead") and adds rows for new Active customers; 15 months of prebuilt tabs are no longer needed.
- v6 (2026-10-09): owner-digest is due every hourly run while Mark has an unanswered item (Config "Follow-up every (minutes)"), and once a morning for half-closed Sales items.
- v5 (2026-10-09): Step 0c2 adds missing header labels and columns on THIS and NEXT week's tabs every run.
- v4 (2026-10-08): Eastern time from TZ; catch-up delivery list only from THIS week's tab (never before Week 1); Sunday alert if the reminder never went out.
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v3 (2026-10-08): confirm-orders step.
- v2 (2026-10-07): shared run lock with the parser; morning exceptions; approvals never both open; missing week tab alert; held no-email invoices.
- v1 (2026-10-07): first version.

HOW TO WORK
This is a checklist, not a judgment task. Every check below is a yes/no answer from values in the sheets. Do not deliberate, summarize, or read anything not listed. Do not read customer tables, the Inbox Log, or any other skill doc unless its check below says it is due. Do not read text messages; the Parser routine does that.

READ ONLY THESE
- sheets-spec: the version line (it must say version 4; if not, record a Problem, text Shane once, end) and the System tab section (run flag and week tab rules).
- Farm Reference: Config tab, System tab, Queue tab (Type, Status, First sent, Last nudged columns only). Customers and Products only for Step 0 b2 (build ahead), when something needs building.
- Weekly Deliveries: header block and day table of three tabs only: LAST, THIS and NEXT week as defined in sheets-spec WEEK NAMES (read that section too).

STEP 0. START
a. Now: run `TZ=America/New_York date '+%a %Y-%m-%d %H:%M'` and use that output as now for every time you write or compare. (The computer clock is UTC; never use plain `date`.)
b. Run flags: follow the "Run flags" rule in sheets-spec (System tab section) exactly, using "Operator run in progress since" as your own flag. If the rule says end: write a run history row with the reason in Problems, and end WITHOUT clearing any flag (the flag belongs to the other run).
b2. Build ahead (runs during quiet hours too; it sends nothing): for THIS week (or NEXT week if there is no THIS week yet) and each of the following Config "Weeks built ahead" weeks (missing or blank = 4), if its tab is missing or unfinished, build or finish it as sheets-spec BUILDING A WEEK TAB says. Also add a row for any Active customer missing from those unlocked tabs. At most 2 tab builds per run (the next run continues). Note what you built in run history. Read Customers and Products only when something needs building or adding.
c. Week tabs: find LAST, THIS and NEXT week's tabs (sheets-spec WEEK NAMES). If one is missing in the way the "Week tabs" rule describes, follow the "Week tabs" rule in sheets-spec, and skip every check below that needs the missing tab.
c2. Labels: on THIS and NEXT week's tabs, compare the header block to sheets-spec HEADER BLOCK and the customer table header to the week-tab customer columns. Add every missing label or column now, as sheets-spec rule 8 says (header label: a new row in the spec's order, value blank; column: at the end of the header row). This is required, not optional. Never change, move or remove existing labels, columns or values. Note what you added in run history.
d. Quiet = now is at or after "Quiet hours start" or before "Quiet hours end". If Quiet, go to STEP 2. (Nothing is sent or started during quiet hours.)
e. Parser late: if "Last parse finished" is blank or older than "Parser late after" minutes, AND "Parser late alert sent" is blank or more than 24 hours ago: text Shane "Operator: the parser hasn't finished since [Last parse finished]." Set "Parser late alert sent" = now. Continue.

STEP 1. DUE CHECKS (in this order; run every one that is due)
For each due step: open the file instructions/[name].md in this repository (for example instructions/send-reminder.md) and follow it. It reads the sheets itself. When it finishes, add "[doc]: done" or "[doc]: failed, [short reason]" to Steps run, then go on to the next check. A failure in one step never stops the others.

1. daily-delivery-list
   Due if EITHER:
   - tomorrow is Monday to Friday, AND now is at or after "Delivery list time", AND tomorrow's row "Delivery list sent" is blank (in the tab containing tomorrow); OR
   - today is Monday to Friday AND a THIS week tab exists AND today's row in THIS week's tab has "Delivery list sent" blank (missed last night; catch-up). Before Sun Oct 11 2026 there is no THIS week tab, so this part is never due. Never use the NEXT-week fallback for this check.

1b. daily-delivery-list (morning exceptions)
   Due if today is Monday to Friday, a THIS week tab exists, today's row in THIS week's tab has "Delivery list sent" filled, AND some customer row for today has a Changes entry containing "after lock" that is later than today's "Exceptions sent" (or "Exceptions sent" is blank). Read only the Day and Changes columns of THIS week's customer table for this check. Run the doc's MORNING EXCEPTIONS part only.

2. delivery-check
   Due if any day row in LAST or THIS week has "Delivery list sent" filled AND "Route confirmed" blank, AND that day is before today OR now is at or after "Route check start".

3. invoicing
   Due if ANY of these:
   - a day row in LAST or THIS week has "Route confirmed" filled and "Invoices drafted" blank;
   - a Queue item of Type Invoice has Status "Waiting";
   - a customer row in LAST or THIS week has "Needs attention" containing "no email" and "Invoice link" blank (read only those two columns);
   - a customer row in LAST or THIS week has "Invoice approved" filled and "Invoice sent" blank (read only those two columns);
   - System "Last payment check" is blank or at least 24 hours ago (invoicing then checks for unpaid invoices itself).

4. send-reminder
   Due if today is Friday and now is at or after the "Reminder request time", OR today is Saturday; AND NEXT week's "Reminder sent" is blank.
   Not due on Sunday. Instead, if today is Sunday, now is before 08:00, Config Mode is LIVE, and THIS week's "Reminder sent" is blank: text Mark and Shane "This week's customer reminder never went out. Text customers by hand if needed." (Only the 7:40 run matches, so this goes once.)

4b. confirm-orders
   Due if any customer row in THIS week or any later built week has "Confirm needed" filled and later than "Confirmation sent" (or "Confirmation sent" blank). Read only those two columns.

5. owner-digest
   Only count Queue rows whose Type is not Driver or Reminder. Due if any such row:
   - has Status "Waiting"; OR
   - has Status "Sent" and (Last nudged, or First sent if Last nudged is blank) is at least Config "Follow-up every (minutes)" ago (missing or blank = 55); OR
   - is Type Sales with Status "Answered", now is at or after Config "Daily follow-up time" (missing or blank = 08:00), and (Last nudged, or First sent if Last nudged is blank) is before today.

6. weekly-master-list: skip while Config "Weekly master list time" says "(not set yet)".
7. finance-update: skip while Config "Finance update time" says "(not set yet)".

MISSING DOC
If a step is due but no file instructions/[name].md exists in this repository:
- Add "[doc]: due, doc missing" to Steps run.
- If System "Missing doc alerts" does not already list that doc for today's date: text Shane "Operator: [doc] is due but its doc doesn't exist yet." Then update "Missing doc alerts" to today's date plus every doc alerted today.

STEP 2. FINISH
a. Add one row to the System run history: Run start (from Step 0), Run end = now, Routine = Operator, Trigger = Scheduled (or Manual if this run was started with Run now text), Steps run, Texts sent (total this run, including texts sent by the steps), Problems.
b. Clear "Operator run in progress since".
c. End with one line: steps run, texts sent, problems.
