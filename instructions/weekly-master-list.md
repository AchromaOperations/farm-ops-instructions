WEEKLY MASTER LIST (version 4)
Written for: sheets-spec version 4

HOW TO WORK
A checklist. Two scripts do all the work: one builds the input file from the sheet's answers, one counts and draws the page. Your job is to save the sheet's answers as files exactly as they come back, run the scripts, save the PDF and text the link. Never type sheet contents into a file, never add up, round, fix or reword anything yourself, and never change the numbers or text the scripts give you.

Which week:
- Saturday: NEXT week's tab.
- Sunday to Thursday: THIS week's tab.
- Friday: never (the operator doesn't call this doc on Fridays; if it does, finish without doing anything).

STEP 1. CHECK
- If that week tab's "Weekly master list checked" is today's date (yyyy-mm-dd), finish. Tonight's check is already done.
- Quick check, Sunday to Thursday only, when the tab's "Weekly master list last sent" is filled: read only the Day and Changes columns of the customer table. Look for a Changes entry with a time later than "Weekly master list last sent" that doesn't end "(standing order sync)", on a row whose delivery day this week is after today. If there is none, nothing changed: set "Weekly master list checked" = today's date, add "weekly-master-list: done, nothing sent (no changes)" to Steps run, and finish without reading or writing anything else. If there is one (or you aren't sure), go on to Step 2. (Saturday, and a week with no list sent yet, always go on.)

STEP 2. READ (save the sheet's answers as files)
Make a new empty folder `ml`. Fetch each range below with the Sheets tool, one call each, and save the answer to the named file exactly as it came back: the JSON that starts {"range": .... If the tool says it saved a large answer to a file, copy that file to the name below instead. Never type a sheet's contents into a file from memory, never reshape an answer, never leave a chunk out.
- The week tab, in 50-row chunks so no answer is too long: A1:ZZ50 to ml/week1.json, A51:ZZ100 to ml/week2.json, A101:ZZ150 to ml/week3.json, A151:ZZ200 to ml/week4.json. A chunk past the last row comes back with no values; save it anyway. If the tab has more than 200 rows, keep going in 50-row chunks (ml/week5.json, ...). ZZ is further than any tab reaches; the tool trims it to the tab's last column.
- Farm Reference Products!A1:Z60 to ml/products.json.
- Farm Reference Config!A1:C60 to ml/config.json.

STEP 3. BUILD THE INPUT FILE
Run, as one command of its own (routines/farm-ops.md hard limit 8), with every week chunk in order:
`python3 -I ops/tools/master_list_input.py --out ml/master.json --products ml/products.json --config ml/config.json --week ml/week1.json --week ml/week2.json --week ml/week3.json --week ml/week4.json`
(add --week ml/week5.json and so on if you saved more). It finds the header block, the "Cust ID" header row, the Active products and Config "First weeks" by their labels, works out the week's Monday, sets "now" to the Eastern time it ran at, and writes ml/master.json in the form tools/master_list_pdf.py reads (tools/sample-master-list.json is an example). It prints one line of JSON:
- "error": add "weekly-master-list: failed, [error]" to Steps run and a Problem. Unless now is in quiet hours, text Shane (one-to-one) "Master list failed: [error]" once. Leave "Weekly master list checked" blank (a Run now can retry). Finish.
- Otherwise check "last_row" against the tab: it must name the last customer row in the chunks you saved (Cust ID and Name). If it doesn't, a chunk is missing or was saved short: fix that and run it again. "rows" is the number of customer rows written. Read time = its "now"; use that below.
- "notes" (a label or column it couldn't find): add each as a Problem and go on; the page reports the same.
Never edit ml/master.json by hand.

STEP 4. RUN
`python3 -I ops/tools/master_list_pdf.py ml/master.json ml/master.pdf`
It prints one line of JSON.
- If it prints "error" or fails: the same as a Step 3 error (Steps run, Problem, text Shane unless quiet hours, leave "Weekly master list checked" blank). Finish.
- If "rows_read" isn't Step 3's "rows": same as a failure ("rows_read [n], expected [m]").
- If "send" is false: set the tab's "Weekly master list checked" = today's date, add "weekly-master-list: done, nothing sent ([reason])" to Steps run, and finish. Send nothing.
- If "changes_shown" is less than "changes": add a Problem "master list: [changes - changes_shown] changes didn't fit on the page" (the page itself says so too) and go on.

STEP 5. SAVE THE PDF
- In the Ops folder, find the subfolder "Master Lists" (sheets-spec LOCATION; made on first use). If you had to create it, add a Problem: "Made the Master Lists folder: Shane, set its sharing to anyone with the link can view."
- Save ml/master.pdf into it exactly as instructions/save-pdf.md says (Google Drive create_file with contentMimeType application/pdf, disableConversionToGoogleType true, and the script's "base64_file" as base64Content), named the script's "file_name". Never replace, rename or delete an older master list. If save-pdf.md says it failed, there's no link: Step 6 sends the fallback text.
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
