# Change log

History of every file in instructions/ and routines/. Each file keeps only its version line, so a routine run doesn't read old history. Newest entries first. Git has the full changes.

## confirm-orders.md (CONFIRM ORDERS (version 11))
- v11 (2026-10-23): the read-back list Doc is made as save-doc.md says; if it fails, the list text goes in the Queue item and the approval still goes out.
- v10 (2026-10-10): the read-back list goes to the family group (sheets-spec rule 11).
- v9 (2026-10-10): read-backs also cover orders placed on later weeks (for example a first-week item), with the date.
- v8 (2026-10-10): read-backs word Extra Milk in gallons right after the share.
- v7 (2026-10-09): "(standing order sync)" entries don't make a read-back risky.
- v6 (2026-10-09): the read-back list goes to Mark as text (sheets-spec rule 10), not a doc link.
- v5 (2026-10-09): read-backs also wait while the customer's weekly share request is open with Mark.
- v4 (2026-10-09): the read-back list waits only on sheets-spec rule 9; a reminder still waiting for wording no longer holds it.
- v3 (2026-10-08): read-backs call milk the customer's weekly share; add-ons follow after "plus".
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v2 (2026-10-08): manual review (Config "Read-back review": ALL, RISKY ONLY, OFF).
- v1 (2026-10-08): first version.

## daily-delivery-list.md (DAILY DELIVERY LIST (version 15))
- v15 (2026-10-23): the fallback Doc is made as save-doc.md says; the morning "Got today's added items?" Driver item starts with its date and is created as already Sent (the morning text asked Harry), so his morning GOT IT counts; lists are never edited after they're made.
- v14 (2026-10-19): the PDF is saved with instructions/save-pdf.md (one fixed create_file call with conversion turned off), replacing the open-ended "text or base64" step that let runs vary.
- 2026-10-19 (tools): delivery_list_pdf.py and master_list_pdf.py write plain compressed PDFs (no ASCII85) plus a one-line .b64 copy for the upload.
- 2026-10-19 (tools/delivery_list_pdf.py): shorter link entries in the PDF (about 3 KB less on a 30-stop day); same look and links.
- v13 (2026-10-15): the list is now the approved PDF design (logo header in the website's colors, tiles, skip box, packing list and stops with tick boxes), made by tools/delivery_list_pdf.py and saved to Delivery Lists as a PDF. The Google Doc (tools/delivery_list_html.py, restyled to match) is only the fallback when the PDF can't be saved. Shane: the Doc that went out Oct 15 was the wrong design.
- v12 (2026-10-15): the doc's layout is fixed: tools/delivery_list_html.py writes the whole list as HTML and the doc is created from it (HTML converted to a Google Doc), so every day looks the same. Never lay the doc out by hand; plain text only as a reported fallback. (Thursday Oct 15's list came out as plain text.)
- v11 (2026-10-13): every stop shows the customer's phone number next to the address (Phone, plus Phone 2 if filled).
- v10 (2026-10-10): Mark and Laura get the list texts as one family group text; Harry still gets his own.
- v9 (2026-10-10): Day, Route and Stop # are refreshed from Customers on unlocked rows before the list is built; a blank Stop # is flagged "!".
- v8 (2026-10-10): skipped stops stay on the route in their place, flagged SKIP, and are listed in a box at the top (with no-milk stops); the text says how many are skipping; a skip added after lock reads "SKIP, no delivery today".
- v7 (2026-10-10): Extra Milk jars are packed with the share jars and shown as "+ N extra" at the stop.
- v6 (2026-10-09): milk is counted in half-gallon jars on the packing list and each stop (Mark: half-gallon jars only).
- v5 (2026-10-09): "(standing order sync)" Changes entries don't flag a stop as CHANGED or put it on the change list.
- v4 (2026-10-09): a customer's weekly share request still open at lock is flagged on the row, never guessed.
- v3 (2026-10-08): share wording on the list and lock text.
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v2 (2026-10-07): empty days count as no delivery (no list, no Harry texts); test customers left out; MORNING EXCEPTIONS part for items added after the list went out.
- v1 (2026-10-07): first version.

## delivery-check.md (DELIVERY CHECK (version 3))
- v3 (2026-10-23): Driver questions carry their day; a "Got today's added items?" item closes itself when its day ends, and any other unsent one 2+ days old is never sent (ALERT to Shane). On Oct 22 an Oct 14 question reached Harry and his "Yes" was misread.
- v2 (2026-10-10): Mark's alert goes to the family group (sheets-spec rule 11).
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v1 (2026-10-07): first version.

## farm-setup.md (FARM SETUP (version 5))
- v5 (2026-10-10): builds week tabs only Config "Weeks built ahead" weeks ahead; the operator builds the rest as they come.
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v4 (2026-10-07): written for sheets-spec v4 (also creates Delivery Lists and Invoice Lists folders).
- v3 (2026-10-07): System tab labels per sheets-spec v3.
- v2 (2026-10-07): re-run safe customer matching; cursor only set when blank; dropdowns; Test phones by role; uses sheets-spec v2 names and formats.
- v1 (2026-10-07): first draft.

## invoicing.md (INVOICING (version 11))
- v11 (2026-10-23): HELD DAYS: a day row's "Invoice hold" stops drafting, lists, sending and pay-link texts for that day until Shane clears it (a hold only in run notes holds nothing). The list Doc is made as save-doc.md says; if it fails, invoicing goes on with the list text in the Queue item. The list includes drafts an earlier run made before stopping. Part D asks Mark about an invoice canceled in Square; Part D2 applies his answer (new Invoice link, or Paid "none"). From the Oct 22-23 Thursday invoices and Cayli's 000049/000050.
- v10 (2026-10-18): Part C2 texts each customer their invoice's payment link once it's published in Square (8am-9pm, LIVE, not NO TEXTS, duplicate guard); the approval list says so.
- v9 (2026-10-18): no-charge items are subtracted from invoices and shown on the approval list; an all-free row gets no invoice.
- v8 (2026-10-10): the invoice list goes to the family group (sheets-spec rule 11).
- v7 (2026-10-10): Extra Milk is priced by share: full share (1 gal or more) at the Products price, half share at Config "Extra milk price, half share".
- v6 (2026-10-09): the invoice list goes to Mark as text (sheets-spec rule 10), not a doc link.
- v5 (2026-10-09): the invoice list waits only on sheets-spec rule 9 (a reminder still waiting for wording no longer holds it), and yields to a reminder preview that is about to go out.
- v4 (2026-10-08): weekly share wording.
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v3 (2026-10-08): waits for any open approval (sheets-spec rule 9); read-back lists go first.
- v2 (2026-10-08 fix): NEXT week per sheets-spec WEEK NAMES.
- v2 (2026-10-07): never ask for invoice approval while a reminder approval is open; hold invoices for customers with no email.
- v1 (2026-10-07): first version.

## manual-edits.md (MANUAL EDITS (version 4))
- v4 (2026-10-23): a chat sets or clears a day's "Invoice hold" only when Shane asks.
- v3 (2026-10-19): Run History tab is routine-owned too.
- v2 (2026-10-18): free items go in the "No charge" column (added if the tab lacks it), not as text in Needs attention or Changes.
- v1 (2026-10-18): new. Rules for chats on the farm account that change the sheets by hand: read whole header rows, check the row's Changes before adding (no doubles), tag changes "(chat)", leave locked rows and routine tabs alone, no texts. Points to sheets-spec, week-names and parser ORDER WRITING/A4 instead of copying them. The farm account's profile preferences tell every chat to fetch it.

## operator.md (OPERATOR (version 17))
- v17 (2026-10-23): a held day doesn't make invoicing due; an Answered Clarify item (a canceled-invoice answer) does; the daily label check also covers the day table header.
- v16 (2026-10-19): reads System A1:B20 only; run history and ALERT checks use the Run History tab.
- v15 (2026-10-18): invoicing is due while a sent invoice (from 2026-10-18 on) still owes its payment-link text, 8am-9pm.
- v14 (2026-10-17): reads week-names.md and only sheets-spec's first line each run; build-ahead and label checks run once a day and after any push (System "Daily checks done"), or when a tab is missing.
- v13 (2026-10-17): no run flag of its own (routines/farm-ops.md RUN FLAG) and no "parser late" check (both parts run in the same run); run history notes "parser: nothing new".
- v12 (2026-10-17): STEP 2 texts Shane every new ALERT problem (system issues like sheet cells not written correctly), from this run and earlier runs, once each per day.
- v11 (2026-10-10): weekly-master-list is due once a night at Config "Weekly master list time": Saturdays for NEXT week, Sunday to Thursday for THIS week (it sends only if something changed).
- v10 (2026-10-10): the Sunday alert is marked in System "Sunday alert sent" so it goes once now that runs are every 30 minutes.
- v9 (2026-10-10): the Sunday alert goes to the family group and Shane.
- v8 (2026-10-10): confirm-orders is due for read-backs on any later built week too.
- v7 (2026-10-10): Step 0 b2 builds week tabs a few weeks ahead (Config "Weeks built ahead") and adds rows for new Active customers; 15 months of prebuilt tabs are no longer needed.
- v6 (2026-10-09): owner-digest is due every hourly run while Mark has an unanswered item (Config "Follow-up every (minutes)"), and once a morning for half-closed Sales items.
- v5 (2026-10-09): Step 0c2 adds missing header labels and columns on THIS and NEXT week's tabs every run.
- v4 (2026-10-08): Eastern time from TZ; catch-up delivery list only from THIS week's tab (never before Week 1); Sunday alert if the reminder never went out.
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v3 (2026-10-08): confirm-orders step.
- v2 (2026-10-07): shared run lock with the parser; morning exceptions; approvals never both open; missing week tab alert; held no-email invoices.
- v1 (2026-10-07): first version.

## owner-digest.md (OWNER DIGEST (version 10))
- v10 (2026-10-23): a list nudge reads the list from the Queue item when there is no Doc.
- v9 (2026-10-17): Step 0 sends the parser's replies (Queue Type Other, Question starting "REPLY: ") to the family group right away, unnumbered, and closes them; replies are never part of a batch or a follow-up.
- v8 (2026-10-10): everything goes to the family group (sheets-spec rule 11), Laura's 6-hour copy is gone; a follow-up tops the open questions back up to Batch size.
- v7 (2026-10-10): quotes go out in full (a Question cut short with "..." is sent with its full Original message instead); texts over 1,500 characters are split.
- v6 (2026-10-09): list follow-ups resend the list itself as text (sheets-spec rule 10), not a link.
- v5 (2026-10-09): Mark is followed up at every hourly run (Config "Follow-up every (minutes)", default 55), each follow-up lists every unanswered question; half-closed Sales items get one morning follow-up a day; Digest # stays taken until Resolved.
- v4 (2026-10-09): share requests from customers ask Mark for the change to make, or 'no change'.
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v3 (2026-10-08): nudges for read-back lists too.
- v2 (2026-10-07): Sales items remind Mark to reply to the customer directly.
- v1 (2026-10-07): first version.

## parser.md (PARSER (version 32))
- v32 (2026-10-23): Harry's reply: words that fit only one question go there (GOT IT to the added-items question, delivery reports to the route); a bare yes/ok answers the question texted most recently, and if two were texted within 20 minutes he's asked which. What a reply meant is decided once. Driver items start with their day. A canceled-invoice answer is left Answered for invoicing. A list stored in the Queue item is read like the Doc.
- v31 (2026-10-19): run history row goes to the Run History tab.
- v30 (2026-10-18): A4 "no charge" command from Mark or Laura (free, comp, on the house, sample).
- v29 (2026-10-17): an Active customer with no row on an unlocked week tab gets their row added before an order is written (build-ahead now runs once a day).
- v28 (2026-10-17): Step 0 and Step 1 (start, fetch, dedupe) moved to parser-check.md, so quiet runs never open this file; the run flags and "Last parse finished" are gone (one run flag in routines/farm-ops.md).
- v27 (2026-10-17): an unclear message from Mark or Laura while something is waiting on them is taken as an answer to it and confirmed with a question before anything changes; with several open and no way to tell which, ask which. System problems are recorded as ALERT problems (Shane gets texted).
- v26 (2026-10-17): every message Mark or Laura sends in the family group is for the system (Shane, Oct 17). Instructions are done (or answered with why not) and confirmed; questions are answered from the sheets; anything unclear is treated as them asking for clarification and gets an explaining reply. Nothing they send is logged and left. Replies go out through the Queue (REPLIES below).
- v25 (2026-10-10): in the family group, a bare OK or a reaction that follows an information-only system text (delivery list, morning exceptions, master list) is about that text, never an approval of an open list or preview.
- v24 (2026-10-10): reads the Mark and Laura family group text (sheets-spec rule 11) by sender; in the group an approval must be meant for the system, not a reply to each other, and chat that fits nothing is ignored.
- v23 (2026-10-10): first-week-only items go to the next first week in Config "First weeks" (Mark's schedule) instead of always asking Mark.
- v22 (2026-10-10): an order for a week that isn't built yet builds that week's tab first.
- v21 (2026-10-10): share-request examples no longer include "extra half gallon" (that's an Extra Milk order now that it's active).
- v20 (2026-10-10): when Harry confirms a route, skipped rows get Delivered = "skipped".
- v19 (2026-10-10): extra milk for one week becomes an Extra Milk add-on order (jars, billed through Square) once its Products row is Active; until then it stays a share request for Mark.
- v18 (2026-10-10): Harry's GOT IT and "good except" are read by intent too ("yep", "got them"; "good except Kim" when Kim is exactly one line).
- v17 (2026-10-10): Queue questions quote the customer's whole message, never cut short with "...".
- v16 (2026-10-10): approvals are read by intent, not exact words ("Good send all", "looks good", "go ahead" all count); a message that also asks, adds or holds something back still isn't one. Shane's decision, Oct 10.
- v15 (2026-10-09): yogurt with no flavor = Yogurt VM (vanilla maple), no longer a question for Mark.
- v14 (2026-10-09): cream is a paid add-on (Products: Billed through Square), so "can I get cream" is an order with the 1-unit default; only cream or whey in place of milk is a share request.
- v13 (2026-10-09): a reaction to any part of a list text (or its resend) counts as approval.
- v12 (2026-10-09): section S: a screenshot of a customer's text conversation sent by Mark, Laura or Shane is read and processed as that customer's order (share changes applied, read-back goes to Mark's list first). Customer pictures are never opened.
- v11 (2026-10-09): digest answers also match half-closed Sales items (Status Answered), so "4 resolved" closes one; closing one is never a conflict.
- v10 (2026-10-09): customers can't change their weekly share by text (milk, cream, whey, skips, pauses, cancelling): it becomes a Sales item, and Mark's digest answer makes or declines the change; add-ons in the same text are still written. Only weekly add-ons (Billed through Square) are orders by text. A dairy add-on with no amount or a vague one = 1 unit (not for "a few" or when the row already has some). Defaults rows win over built-in defaults. CANCEL, REVOKE and OPT OUT are opt-outs like STOP. A share Clarify always offers "no change" first.
- v9 (2026-10-09): "eggs" with no amount = 1 dozen.
- v8 (2026-10-09): before writing to a week tab, add any missing label or column it needs (sheets-spec rule 8).
- v7 (2026-10-08): reminder approval needs two different people (Mark, Laura, Harry, Shane); Harry and Shane can approve the reminder preview.
- v6 (2026-10-08, revised): first-week-only products always go to Mark as a question.
- v6 (2026-10-08): system texts matched by number, text and time (Quo returns no ID on send); Eastern time from TZ; strict approval words; Harry's morning yes never confirms a route; STOP opt-outs; quoted texts kept short; system read-backs are never orders.
- v5 (2026-10-08): share wording in examples.
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v4 (2026-10-08): approval replies also cover read-back lists.
- v3 (2026-10-08): marks rows for an order read-back (Confirm needed).
- v2 (2026-10-07): shared run lock; fetch before reading the spec; conflicting answers; GOT IT from Harry.
- v1 (2026-10-07): first version.

## send-reminder.md (SEND REMINDER (version 9))
- v9 (2026-10-10): Mark and Laura get every reminder text as one family group text (sheets-spec rule 11), followed up hourly; Shane stays one-to-one every Nudge after hours; Laura's separate wording ask is gone.
- v8 (2026-10-09): Mark is followed up at every hourly run while the wording or his YES is missing; Laura and Shane stay at every Nudge after hours (new label "Reminder others last asked"); Laura is first asked Nudge after hours after the request.
- v7 (2026-10-08): preview goes to Mark, Laura, Harry and Shane; the parser needs two different approvals (never mention this in any text).
- v6 (2026-10-08): one text per phone number (shared numbers); NO TEXTS customers skipped; late approval moves the reply-by time.
- v5 (2026-10-08): cutoff line no longer says "your order" (milk is a weekly share).
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v4 (2026-10-08): Laura is asked for the wording after Nudge after hours (3), not 1 hour.
- v3 (2026-10-08): waits for any open list approval (sheets-spec rule 9).
- v2 (2026-10-07): preview waits while an invoice list is waiting on Mark (approvals never both open).
- v1 (2026-10-07): first version.

## save-doc.md (SAVE LIST DOC (version 1))
- v1 (2026-10-23): new. The one way to make a list Google Doc: create_file with text/plain (or text/html for the delivery list fallback) and textContent, conversion on; never base64. If it fails, the work goes on without the Doc. Docs can't be edited, so a second one gets "(2)".

## save-pdf.md (SAVE PDF (version 2))
- v2 (2026-10-23): says it is for PDFs only; list Docs use save-doc.md (the "never textContent" rule had confused an invoice Doc on Oct 23).
- v1 (2026-10-19): new. The one way to save a script-made PDF to Drive: create_file with contentMimeType application/pdf, disableConversionToGoogleType true, base64Content from the script's .b64 file; then check it's a PDF of the right size. Drive's default conversion is what turned master lists into empty Docs on Oct 17-18.

## sheets-spec.md (SHEETS SPEC (version 4))
- v4 (2026-10-23, revised 33): day-table column "Invoice hold" (only Shane clears it); Driver item Questions start with their day; "Canceled invoice:" Clarify items wait Answered for invoicing; Invoice link changes only for a canceled invoice's replacement; Queue list items may hold the list text when the Doc failed; list Docs use save-doc.md.
- v4 (2026-10-19, revised 32): rule 12: log rows are added with appendCells (after the last filled row), never append_values (it lands after the first block, which caused 64 duplicate Inbox Log rows and scattered run history); logs are read by whole column, never "the last rows". Run history moves to its own "Run History" tab; the System tab is read as A1:B20 only.
- v4 (2026-10-18, revised 31): week-tab STAMP column "Pay link texted" (invoices sent from 2026-10-18 on).
- v4 (2026-10-18, revised 30): week-tab column "No charge" (LOG): free items, still in the quantity cell; billing subtracts them. Only Mark, Laura or Shane can make something free.
- v4 (2026-10-17, revised 29): WEEK NAMES and MISSING WEEK TABS moved (not copied) to week-names.md; WHERE RULES LIVE note; System "Daily checks done". send-reminder, parser, confirm-orders, invoicing and operator now point to week-names.md.
- v4 (2026-10-17, revised 28): one run flag, System "Run in progress since"; the parser and operator flags, "Last parse finished", "Parser late alert sent" and Config "Parser late after" are no longer used. Change logs moved to CHANGELOG.md.
- v4 (2026-10-17, revised 27): System "Problem alerts checked" and "Problem alerts sent": ALERT problems (system issues) are texted to Shane.
- v4 (2026-10-17, revised 26): rule 11: every message Mark or Laura send in the family group is for the system and gets acted on, answered or clarified (parser A). Queue: a Type Other item whose Question starts "REPLY: " is the system's reply to them.
- v4 (2026-10-15, revised 25): Delivery Lists holds one PDF per delivery day (a Google Doc only as the fallback).
- v4 (2026-10-10, revised 24): weekly master list: Config "Weekly master list time" 20:30, header labels "Weekly master list last sent" and "Weekly master list checked", Master Lists folder for its PDFs.
- v4 (2026-10-10, revised 23): one Farm ops routine (parser part, then operator part) twice an hour replaces the two routines; System "Sunday alert sent".
- v4 (2026-10-10, revised 22): rule 11: texts for Mark and Laura go to one family group text; Laura after is retired; Nudge after now only paces Shane on the reminder.
- v4 (2026-10-10, revised 21): Config "First weeks" lists which delivery weeks carry first-week-only products.
- v4 (2026-10-10, revised 20): week tabs are built a few weeks ahead (Config "Weeks built ahead", default 4; BUILDING A WEEK TAB) instead of 15 months; Day, Route and Stop # are refreshed from Customers before each delivery list.
- v4 (2026-10-10, revised 19): Extra Milk has two rates: Products price for full shares (1 gal or more), Config "Extra milk price, half share" for half shares.
- v4 (2026-10-10, revised 18): Extra Milk, a paid add-on of extra half-gallon jars for one week, separate from the never-invoiced share; off until its Products row is Active.
- v4 (2026-10-10, revised 17): approvals are read by intent, not exact words.
- v4 (2026-10-09, revised 16): share cream (in place of a jar) is handled off the sheet: not invoiced, not counted.
- v4 (2026-10-09, revised 15): milk goes out in half-gallon jars only.
- v4 (2026-10-09, revised 14): "(standing order sync)" Changes entries are not changes (lists, read-back risk and sync conflicts ignore them).
- v4 (2026-10-09, revised 13): cream is a paid add-on; add-ons can be standing orders.
- v4 (2026-10-09, revised 12): rule 10: approval lists go to Mark as the list in the text, not a doc link.
- v4 (2026-10-09, revised 11): Config "Follow-up every (minutes)" (Mark followed up every hourly run) and "Daily follow-up time"; "Nudge after" now only paces Laura and Shane on the reminder; header label "Reminder others last asked"; a Digest # stays taken until Resolved.
- v4 (2026-10-08, revised 10): reminder preview goes to Mark, Laura, Harry and Shane; "Reminder approvals" records who approved; two different approvers needed.
- v4 (2026-10-08, revised 9): Products "Weeks" column (All, First week only).
- v4 (2026-10-08, revised 8): Quo send tools return no message ID; system texts are logged with ID "pending" and the parser fills it in by matching.
- v4 (2026-10-08, revised 7): Customers "Notes" may start with "NO TEXTS" (customer opted out of texts: never text them).
- v4 (2026-10-08, revised 6): list subfolders are created on first use; no instruction docs or Archive in Drive.
- v4 (2026-10-08, revised 5): the Ops folder is found by the Farm Reference sheet it contains, not by name.
- v4 (2026-10-08, revised 4): TERMS: milk is the customer's weekly share, never an order; only add-ons are orders.
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v4 (2026-10-08, revised 3): manual review of read-backs (Config "Read-back review", Queue type Read-back, Read-back Lists folder, rule 9 one approval at a time).
- v4 (2026-10-08, revised 2): order read-backs (Products "Text name"; week columns "Confirm needed" and "Confirmation sent").
- v4 (2026-10-08, revised): WEEK NAMES defined by dates (fixes Fri/Sat before week 1).
- v4 (2026-10-07, revised after review): routines never run at the same time; approvals never both open; morning exceptions; missing week tab alerts.
- v4 (2026-10-07): every system text logged with its Quo ID; Queue gets Digest # and Driver type; reminder wording can be revised (check failed, final text, test sent fields); Mark-approved late additions; Invoice Lists folder.
- v3 (2026-10-07): System tab tracks two routines (Parser, Operator) with separate run flags and Last parse finished; Config adds Parser late, report times, missing-doc alerts.
- v2 (2026-10-07): cell kinds replace "never overwrite"; one date-time format; file lookup rule; Phone 2 matching; cursor overlap + message ID dedupe; stale run flag; lock time is the real cutoff; structured Not delivered; dropdowns; year-crossing tab names.
- v1 (2026-10-07): first draft.

## parser-check.md (PARSER CHECK (version 2))
- v2 (2026-10-19): dedupe reads the Inbox Log's whole Quo message ID column (the log isn't in time order).
- v1 (2026-10-17): new. The start of every run (fetch, dedupe, match the system's own texts); parser.md is only opened when there are new messages.

## week-names.md (WEEK NAMES (version 1))
- v1 (2026-10-17): new. THIS/NEXT/LAST week, tab names and missing week tabs, moved here from sheets-spec so the operator reads a small file each run.

## weekly-master-list.md (WEEKLY MASTER LIST (version 3))
- v3 (2026-10-19): the PDF is saved with instructions/save-pdf.md.
- v2 (2026-10-17): Sunday to Thursday, a quick look at the Changes column first; no new changes = done without building the input file.
- v1 (2026-10-10): first version. A one-page PDF of a delivery week's totals by day and by product, made by tools/master_list_pdf.py, saved to Drive, and the link texted to the family group. Saturday: next week's list always goes out. Sunday to Thursday: this week's list goes out again only if orders changed since the last one, with the changes listed at the top. Never on Friday.

## routines/farm-ops.md
- 2026-10-23: SYSTEM PROBLEMS: the only way to hold a day's invoicing is that day's "Invoice hold" cell, and only when a write came out wrong and couldn't be fixed; never because an old reply would now be read differently.
- 2026-10-19: reads System A1:B20 only; log rows via appendCells (sheets-spec rule 12); Run History tab.
- 2026-10-18: hard limit 9 allows reading Square payment links (for the invoice text).
- 2026-10-17: write checks: stamps and "sent" cells read back right away; everything else checked once per tab at the end of each part.
- 2026-10-17: NIGHT rule (runs between 9pm and 6:30am end at once); one RUN FLAG for the whole run; Part 1 starts with parser-check.md. Runs are meant for 6:40am to 8:40pm.
- 2026-10-17: SYSTEM PROBLEMS: read back sheet writes; ALERT problems texted to Shane.
- 2026-10-10: one Farm ops routine, parser part then operator part, twice an hour.
