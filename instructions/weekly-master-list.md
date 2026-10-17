WEEKLY MASTER LIST (version 2)
Written for: sheets-spec version 4

HOW TO WORK
A checklist. A script does all the counting and draws the page. Your job is to copy cells into its input file exactly, run it, save the PDF and text the link. Never add up, round, fix or reword anything yourself, and never change the numbers or text the script gives you.

Which week:
- Saturday: NEXT week's tab.
- Sunday to Thursday: THIS week's tab.
- Friday: never (the operator doesn't call this doc on Fridays; if it does, finish without doing anything).

STEP 1. CHECK
- If that week tab's "Weekly master list checked" is today's date (yyyy-mm-dd), finish. Tonight's check is already done.
- Get the time now: `TZ=America/New_York date '+%Y-%m-%d %H:%M'`. This is "read time". Use it below, not the time the run started.
- Quick check, Sunday to Thursday only, when the tab's "Weekly master list last sent" is filled: read only the Day and Changes columns of the customer table. Look for a Changes entry with a time later than "Weekly master list last sent" that doesn't end "(standing order sync)", on a row whose delivery day this week is after today. If there is none, nothing changed: set "Weekly master list checked" = today's date, add "weekly-master-list: done, nothing sent (no changes)" to Steps run, and finish without reading or writing anything else. If there is one (or you aren't sure), go on to Step 2. (Saturday, and a week with no list sent yet, always go on.)

STEP 2. READ
- That week tab: the header-block values "Week" and "Weekly master list last sent", and the whole customer table (the "Cust ID" header row and every row below it).
- Farm Reference Products tab: Column name, Unit and Weeks of every row whose Active is Yes, in the tab's order.
- Farm Reference Config "First weeks".

STEP 3. WRITE THE INPUT FILE
Make a new empty folder `ml` and write `ml/master.json` in exactly this form (tools/sample-master-list.json is a full example):
{
  "farm": "Restoration Farmstead",
  "week": [the tab's "Week" value, a number],
  "monday": "[that week's Monday, yyyy-mm-dd]",
  "now": "[read time, yyyy-mm-dd hh:mm]",
  "last_sent": "[the tab's \"Weekly master list last sent\" exactly, or \"\" if blank]",
  "first_week": [true if Config "First weeks" lists this week's Sunday date, otherwise false],
  "products": [ {"column": "[Column name]", "unit": "[Unit]", "weeks": "[Weeks, or \"All\" if blank]"}, ... one per Active product, in Products order ],
  "columns": ["Cust ID", "Name", "Day", [every product Column name, same order as products], "Changes"],
  "rows": [ ["[Cust ID]", "[Name]", "[Day]", [each product cell], "[Changes]"], ... ]
}
Rules for rows:
- One row for every row of the customer table, in sheet order, test rows (Cust ID starting "T") included (the script leaves them out). Skip only rows whose Cust ID and Name are both blank.
- Each cell copied exactly as it reads in the sheet, as a string. A blank cell is "". Never put 0 for a blank, never round, never fix a typo or a strange value (the script reports those on the page).
- The Changes cell is copied whole, every entry, exactly.
- If a product column is missing from the week tab, use "" for it in every row (the script reports it).
- Before running: count the customer rows on the tab (excluding fully blank rows) and check that "rows" has the same number. If not, fix the file. Never run it with rows missing.

STEP 4. RUN
`python3 -I ops/tools/master_list_pdf.py ml/master.json ml/master.pdf`
It prints one line of JSON.
- If it prints "error" or fails: add "weekly-master-list: failed, [error]" to Steps run and a Problem. Unless now is in quiet hours, text Shane (one-to-one) "Master list failed: [error]" once. Leave "Weekly master list checked" blank (a Run now can retry). Finish.
- If "rows_read" isn't your row count: same as a failure ("rows_read [n], expected [m]").
- If "send" is false: set the tab's "Weekly master list checked" = today's date, add "weekly-master-list: done, nothing sent ([reason])" to Steps run, and finish. Send nothing.
- If "changes_shown" is less than "changes": add a Problem "master list: [changes - changes_shown] changes didn't fit on the page" (the page itself says so too) and go on.

STEP 5. SAVE THE PDF
- In the Ops folder, find the subfolder "Master Lists" (sheets-spec LOCATION; made on first use). If you had to create it, add a Problem: "Made the Master Lists folder: Shane, set its sharing to anyone with the link can view."
- Save ml/master.pdf into it as a PDF file (type application/pdf), named the script's "file_name". It must stay a PDF: never convert it to a Google Doc. Never replace, rename or delete an older master list.
- The file is plain text on purpose. If the Drive tool takes the file's contents as text, give it the file's text exactly. If it wants base64, run `base64 -i ml/master.pdf` and give it that output exactly. Never retype or shorten either.
- If your Drive tool can set sharing, set the file to "anyone with the link can view".
- Get the file's link.

STEP 6. SEND
- If you have the link: text the family group (sheets-spec rule 11) the script's "message" with {LINK} replaced by the link. Nothing else in that text.
- If saving failed (no link): text the family group the script's "fallback_text" instead, exactly, and add a Problem "master list PDF not saved: [reason]".
- Log the text in the Inbox Log (Out (system)).
- Never send it during quiet hours. If now is in quiet hours, send nothing and leave "Weekly master list checked" blank.

STEP 7. RECORD (on the same week tab)
- "Weekly master list sent" = read time, only if it is blank (STAMP: the first list for this week).
- "Weekly master list last sent" = read time (the script's "now", not the time the text went out). The next update lists changes after this time.
- "Weekly master list checked" = today's date.

FINISH
Report to the operator: week, "full" or "update", customers changed, texts sent, problems.
