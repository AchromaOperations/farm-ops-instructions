OPERATOR (version 16)
Written for: sheets-spec version 4

HOW TO WORK
This is a checklist, not a judgment task. Every check below is a yes/no answer from values in the sheets. Do not deliberate, summarize, or read anything not listed. Do not read customer tables, the Inbox Log, or any other skill doc unless its check below says it is due. Do not read text messages; the Parser routine does that.

READ ONLY THESE
- week-names.md (THIS, NEXT and LAST week, tab names, missing week tabs). Read it every run.
- sheets-spec: only its first line, for the version: run `head -1 ops/instructions/sheets-spec.md`. It must say version 4; if not, record an ALERT Problem, text Shane once, end. Open the rest of sheets-spec only when Step 0's daily checks run or a due step's doc needs it.
- Farm Reference: Config tab, System tab (A1:B20 only), Queue tab (Type, Status, First sent, Last nudged columns only). Customers and Products only for Step 0 b (build ahead), when something needs building.
- Weekly Deliveries: header block and day table of three tabs only: LAST, THIS and NEXT week as week-names.md defines them.

STEP 0. START
a. Now: run `TZ=America/New_York date '+%a %Y-%m-%d %H:%M'` and use that output as now for every time you write or compare. (The computer clock is UTC; never use plain `date`.)
Daily checks (b and c2): do them only if System "Daily checks done" isn't "[today's date] [repo version]" (get the version with `git -C ops rev-parse --short HEAD`), or this run built a week tab. Otherwise skip b and c2. After doing them, set "Daily checks done" = "[today's date] [repo version]". So they run in the first operator run of each day, and again on the first run after any push.
b. Build ahead (it sends nothing): for THIS week (or NEXT week if there is no THIS week yet) and each of the following Config "Weeks built ahead" weeks (missing or blank = 4), if its tab is missing or unfinished, build or finish it as sheets-spec BUILDING A WEEK TAB says. Also add a row for any Active customer missing from those unlocked tabs. At most 2 tab builds per run (the next run continues). Note what you built in run history. Read Customers and Products only when something needs building or adding.
c. Week tabs: find LAST, THIS and NEXT week's tabs (week-names.md). If one is missing, follow MISSING WEEK TABS in week-names.md (if it says to build a tab, run b now even if the daily checks were done), and skip every check below that needs the missing tab.
c2. Labels (daily checks; read sheets-spec HEADER BLOCK and CUSTOMER TABLE for this): on THIS and NEXT week's tabs, compare the header block to sheets-spec HEADER BLOCK and the customer table header to the week-tab customer columns. Add every missing label or column now, as sheets-spec rule 8 says (header label: a new row in the spec's order, value blank; column: at the end of the header row). This is required, not optional. Never change, move or remove existing labels, columns or values. Note what you added in run history.
d. Quiet = now is at or after "Quiet hours start" or before "Quiet hours end". If Quiet, go to STEP 2. (Nothing is sent or started during quiet hours.)

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
   - now is 8:00am to 9:00pm and a customer row in LAST or THIS week has "Invoice sent" filled on or after 2026-10-18 and "Pay link texted" blank or missing (read only those two columns);
   - System "Last payment check" is blank or at least 24 hours ago (invoicing then checks for unpaid invoices itself).

4. send-reminder
   Due if today is Friday and now is at or after the "Reminder request time", OR today is Saturday; AND NEXT week's "Reminder sent" is blank.
   Not due on Sunday. Instead, if today is Sunday, now is before 09:00, Config Mode is LIVE, THIS week's "Reminder sent" is blank, and System "Sunday alert sent" is not today's date: text the family group (sheets-spec rule 11) and Shane (one-to-one) "This week's customer reminder never went out. Text customers by hand if needed." Then set System "Sunday alert sent" = today's date, so it goes once.

4b. confirm-orders
   Due if any customer row in THIS week or any later built week has "Confirm needed" filled and later than "Confirmation sent" (or "Confirmation sent" blank). Read only those two columns.

5. owner-digest
   Only count Queue rows whose Type is not Driver or Reminder. Due if any such row:
   - has Status "Waiting"; OR
   - has Status "Sent" and (Last nudged, or First sent if Last nudged is blank) is at least Config "Follow-up every (minutes)" ago (missing or blank = 55); OR
   - is Type Sales with Status "Answered", now is at or after Config "Daily follow-up time" (missing or blank = 08:00), and (Last nudged, or First sent if Last nudged is blank) is before today.

6. weekly-master-list
   Never due on Friday, and skipped while Config "Weekly master list time" says "(not set yet)". Otherwise due if now is at or after that time AND either:
   - today is Saturday, a NEXT week tab exists, and NEXT week's "Weekly master list checked" is not today's date; or
   - today is Sunday to Thursday, a THIS week tab exists, and THIS week's "Weekly master list checked" is not today's date.
   Read only those header-block cells for this check. The doc itself decides whether anything is sent.
7. finance-update: skip while Config "Finance update time" says "(not set yet)".

MISSING DOC
If a step is due but no file instructions/[name].md exists in this repository:
- Add "[doc]: due, doc missing" to Steps run.
- If System "Missing doc alerts" does not already list that doc for today's date: text Shane "Operator: [doc] is due but its doc doesn't exist yet." Then update "Missing doc alerts" to today's date plus every doc alerted today.

STEP 2. FINISH
a0. Problem alerts (skip if Quiet): collect the ALERT problems (routines/farm-ops.md SYSTEM PROBLEMS) from this run so far and from every Run History row whose Run start is after System "Problem alerts checked" (blank = the last 24 hours). Leave out any a step already texted Shane about in this run, and any already listed in System "Problem alerts sent" for today. If any are left, text Shane (one-to-one, Config "Admin (Shane) phone") one message: "Farm ops problem: [problem]", or for several "Farm ops problems:" then one per line (at most 10, then "+[n] more in the Run History tab"). Then set "Problem alerts sent" = today's date + every problem alerted today (a few words each), e.g. "2026-10-17: Customers Phone not written for C012; Drive save failed". Set "Problem alerts checked" = now (also when there was nothing to send).
a. Add one row to the Run History tab (sheets-spec rule 12; create the tab if it's missing): Run start (from Step 0), Run end = now, Routine = Operator, Trigger = Scheduled (or Manual if this run was started with Run now text), Steps run (start with "parser: nothing new" if Part 1 found no new texts), Texts sent (total this run, including texts sent by the steps), Problems.
b. End with one line: steps run, texts sent, problems.
