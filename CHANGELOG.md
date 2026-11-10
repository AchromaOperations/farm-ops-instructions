# Change log

History of every file in instructions/ and routines/. Each file keeps only its version line, so a routine run doesn't read old history. Newest entries first. Git has the full changes.

## confirm-orders.md (CONFIRM ORDERS (version 13))
- v13 (2026-11-06): a read-back for a week after NEXT week gives the month too ("Friday, Dec 11"). On Nov 6 a Dec 11 read-back said "Friday the 11th" and the customer took it for the next week.
- v12 (2026-10-30): read-backs go to whichever of the customer's two numbers (Phone or Phone 2) they last texted from, found in the Inbox Log; Phone if they've never texted. A customer who orders from Phone 2 was getting read-backs on Phone.
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

## daily-delivery-list.md (DAILY DELIVERY LIST (version 18))
- v18 (2026-11-09): the list text and the morning changes text go to both drivers, Harry and Zi, one-to-one each (Config "Driver 2 (Zi) phone"); the morning text says "Reply GOT IT" with no name; the Driver item's Sent to = "Harry, Zi". Shane: every delivery text Harry gets goes to Zi as well.
- v17 (2026-11-02): the links are back (Shane: build the compressed link version). tools/delivery_list_pdf.py writes PDF 1.5 with the small objects (pages, fonts, link entries) packed into one compressed object stream: a 27-stop list is about 14,600 base64 characters with all its map and tap-to-call links (25,000 before). It also writes dl/list-no-links.pdf (about 12,200), which save-pdf.md uploads as the second try if the first upload fails.
- v16 (2026-11-02): with tools/delivery_list_pdf.py, addresses and phones on the PDF are plain text, not map and tap-to-call links (Shane: they don't need to be links). The link entries were about a third of the file; a 27-stop list drops from about 25,000 to 13,400 base64 characters for the run to copy into the upload. Three of eight uploads since Oct 19 failed on that copy (Oct 19, Oct 25, Nov 1).
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

## delivery-check.md (DELIVERY CHECK (version 6))
- v6 (2026-11-09): the route question goes only to the drivers who haven't confirmed that day ("Confirmed by"), and Mark's alert says who has and offers "[Driver]'s done" for a driver who can't be reached. Shane: a two-route day waits for two confirmations, a one-route day for one.
- v5 (2026-11-09): every driver text (Driver questions, nudges, the route question) goes to both drivers, Harry and Zi, one-to-one each; Mark's alert reads "Haven't heard from Harry or Zi". The day-table columns keep their "Harry" names. Shane's rule.
- v4 (2026-11-03): the route question also asks Harry who paid him cash and how much (Shane: a customer who paid cash is marked paid and never invoiced).
- v3 (2026-10-23): Driver questions carry their day; a "Got today's added items?" item closes itself when its day ends, and any other unsent one 2+ days old is never sent (ALERT to Shane). On Oct 22 an Oct 14 question reached Harry and his "Yes" was misread.
- v2 (2026-10-10): Mark's alert goes to the family group (sheets-spec rule 11).
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v1 (2026-10-07): first version.

## farm-setup.md (FARM SETUP (version 7))
- v7 (2026-11-09): the phone checkpoint asks for Zi's number too (Config "Driver 2 (Zi) phone").
- v6 (2026-10-27): marked as the original build doc (sheets-spec wins); adds the Run History tab and builds headers in the spec's column order.
- v5 (2026-10-10): builds week tabs only Config "Weeks built ahead" weeks ahead; the operator builds the rest as they come.
- (2026-10-08) moved from Google Docs to the GitHub repository; other docs are files in instructions/.
- v4 (2026-10-07): written for sheets-spec v4 (also creates Delivery Lists and Invoice Lists folders).
- v3 (2026-10-07): System tab labels per sheets-spec v3.
- v2 (2026-10-07): re-run safe customer matching; cursor only set when blank; dropdowns; Test phones by role; uses sheets-spec v2 names and formats.
- v1 (2026-10-07): first draft.

## invoicing.md (INVOICING (version 17))
- v17 (2026-11-09): Part A notes that "Route confirmed" now waits for every route's driver; Part B lists a draft Mark or Laura changed by hand with the lines it has now; Part C never sends a row while an "Invoice ..." question about it is open (a miss reported after approval); a Needs attention note alone never stops an approved row. On Nov 9 Zi's "Yes" confirmed Monday alone, the drafts were made in the same run, and Harry's "extra half gallon not delivered" came 27 minutes later: the Reynolds draft kept the $7 line.
- v16 (2026-11-09): cash wording names the driver in the Paid cell (Harry or Zi) instead of always Harry.
- v15 (2026-11-06): Part A: a customer whose Customers Notes say NO INVOICE is never drafted ("Invoice link" = "none", no Square customer); any add-on goes to Mark and Laura as a Clarify item (Shane's Oct 10 rule, which no doc held). On Nov 3 Hannah Fabish got a $21 draft and a Square customer.
- v14 (2026-11-03): a row whose Paid starts with "cash" (Harry was paid cash) is never drafted, listed for approval, sent or texted a payment link; it shows as a "Paid cash:" line on the lists, and Mark gets a Clarify item if Harry's amount is below the items' total. Cash reported after drafting leaves the Square draft unsent ("Invoice sent" = "not sent: paid cash").
- v13 (2026-10-28): a customer's new pay-link text also lists their earlier invoices that are still owed (last 8 weeks, checked in Square right before texting), each with its amount due and payment link. Paid ones found on the way get "Paid" filled. The approval list's closing line says so. Shane's rule.
- v12 (2026-10-28): every invoice waiting for an OK goes to Mark and Laura in one approval list, whatever day it's from. When a new day's invoices are drafted while a list is open, a new list with everything still waiting (same numbers, new ones added) replaces it, so new invoices never wait behind an unanswered list. Day items only mark a day's drafts as ready; the day's drafted Doc is unnumbered. Day-row "Invoices approved" follows the customer rows. Lists sent before 2026-10-29 aren't replaced (Shane: don't resend Tuesday Oct 27's list). Shane's rule.
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

## manual-edits.md (MANUAL EDITS (version 6))
- v6 (2026-11-08): the person in a farm-account chat is Laura unless they say they are Shane or Mark (Shane's rule), so "[who]" in Changes, No charge and other tags defaults to "Laura (chat)"; the Invoice hold exception applies when the person says they are Shane.
- v5 (2026-11-08): the three files a chat must read are linked in full, not as a "[name]" pattern. A chat's web tool opens only links that already appear in the conversation and refuses links it assembled itself; on Nov 8 a chat on the farm account built the sheets-spec and week-names links from the pattern, was refused, and stopped (correctly) without making the Monday list it was asked for. Also: a chat never saves a delivery or master list into the Drive folders the routine sends from; chat-made lists are previews (new skills/delivery-list-pdf).
- v4 (2026-10-23): a chat sets or clears a day's "Invoice hold" only when Shane asks.
- v3 (2026-10-19): Run History tab is routine-owned too.
- v2 (2026-10-18): free items go in the "No charge" column (added if the tab lacks it), not as text in Needs attention or Changes.
- v1 (2026-10-18): new. Rules for chats on the farm account that change the sheets by hand: read whole header rows, check the row's Changes before adding (no doubles), tag changes "(chat)", leave locked rows and routine tabs alone, no texts. Points to sheets-spec, week-names and parser ORDER WRITING/A4 instead of copying them. The farm account's profile preferences tell every chat to fetch it.

## skills/delivery-list-pdf/SKILL.md (version 1)
- (2026-11-09) wording: the official list reaches the drivers, Harry and Zi.
- v1 (2026-11-08): new. A chat-side skill for the farm's Claude account (Shane uploads it under Settings, Capabilities, Skills; the repository copy is the source). On "Monday delivery sheet in pdf" it clones this repository with git (no web fetching, no GitHub sign-in), reads the sheets by name, builds day.json as daily-delivery-list.md Step 4 says and runs tools/delivery_list_pdf.py, then hands the PDF to the person as a preview marked "PREVIEW, not locked". It never writes a cell, texts anyone, or saves into Delivery Lists: the routine's 7:17pm run makes and sends the official list, and a file in that folder would be taken for it.

## operator.md (OPERATOR (version 19))
- v19 (2026-11-06): the daily label check covers every built week tab, not just THIS and NEXT (weeks 6 to 12 were built under an older layout; on Nov 6 the parser added 18 columns to week 9 itself). Every evening run at or after the master list time records weekly-master-list as done, failed or not due in Steps run (on Nov 3 it was due, skipped, and nothing said so).
- v18 (2026-10-30): a "no email" customer row makes invoicing due only once the Customers tab has an email for them (invoicing Part A2's condition). A customer still waiting for an email had made invoicing due every run with nothing to do.
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

## owner-digest.md (OWNER DIGEST (version 11))
- v11 (2026-11-09): a Clarify item whose Question starts with "Invoice " is urgent, so it goes out even while an invoice list is open, marked "(before the invoices go out)". On Nov 9 the warning about the Reynolds draft waited behind the list it was about.
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

## parser.md (PARSER (version 38))
- v38 (2026-11-09): ROUTE CONFIRMATIONS: each driver's "yes" is recorded in the day row's "Confirmed by", and "Route confirmed" (with the Delivered stamps) is filled only when the day has one confirmation per Routes tab route (Monday, Thursday and Friday two; Tuesday and Wednesday one), so the second driver's miss lands before any draft; a driver's answer to his own "what wasn't delivered" question counts as his confirmation. SECOND ANSWERS: a miss reported after the route is confirmed makes an "Invoice for [name] held" question when the draft is unsent (invoicing holds it) or a fix-by-hand note when it was sent. A3: "fixed" on a held-invoice question marks the row "draft changed by hand" (and drops the list's "waiting for an answer" note) so it is listed again with the draft's lines. A4: Mark or Laura can confirm a route for a driver who can't be reached ("Harry's done"). Shane's rule after Nov 9.
- v37 (2026-11-09): section B reads texts from either driver, Harry or Zi (Zi is a Config phone and an Inbox Log Who); Clarify texts and the Paid cash stamp name the driver who spoke; SECOND ANSWERS: a plain agreement from the second driver after the first answered is logged only, while a named miss or cash report is still recorded and Mark is told; the reminder paragraph stays Harry-only. Shane: every delivery text Harry gets goes to Zi as well.
- v36 (2026-11-06): a first-week item moved to a later week keeps the plain "(text)" source and says why in Needs attention (a note inside the source broke the read-back risk check); a share change Mark or Laura make for a customer's request (A3) sets Confirm needed, so the customer hears back (Victoria Gilmour's Nov 5 skip got no reply and she asked again Nov 6).
- v35 (2026-11-03): CASH: when Harry says a customer paid him cash, fill that row's Paid with "cash $[amount] (Harry, [time])"; a name that doesn't match one row becomes a Driver question; if the invoice already went out, Mark is asked to cancel it in Square.
- v34 (2026-10-28): invoice approval lists name each line's delivery date; an excepted line gets "Invoice held: waiting for an answer" so later lists leave it off; an answer sent before a replacement list went out applies only to the list it answered, and the rest goes out again.
- v33 (2026-10-27): "send me Monday's list again" is only a question (answered with the link), no longer also listed as an instruction the system can't do.
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

## save-doc.md (SAVE LIST DOC (version 2))
- v2 (2026-10-30): after a Drive quota error, check the folder for a file of that title made in the last 10 minutes, and if none, make the same call once more; only a second failure is an ALERT. A read-back list Doc failed once on Oct 30 with "Resource has been exhausted (e.g. check quota)".
- v1 (2026-10-23): new. The one way to make a list Google Doc: create_file with text/plain (or text/html for the delivery list fallback) and textContent, conversion on; never base64. If it fails, the work goes on without the Doc. Docs can't be edited, so a second one gets "(2)".

## save-pdf.md (SAVE PDF (version 4))
- v4 (2026-11-02): when the script's JSON has "no_links" (the delivery list), the second try uploads that smaller copy instead of the same file. A second try that passes is noted in Steps run, not an ALERT.
- v3 (2026-11-02): a failed or damaged upload gets one more try from a fresh copy of the .b64 file (titled "(2)" if the first try left a file); only a second failure is an ALERT and falls back. Nov 1's delivery list failed because Drive said the base64 wasn't valid.
- v2 (2026-10-23): says it is for PDFs only; list Docs use save-doc.md (the "never textContent" rule had confused an invoice Doc on Oct 23).
- v1 (2026-10-19): new. The one way to save a script-made PDF to Drive: create_file with contentMimeType application/pdf, disableConversionToGoogleType true, base64Content from the script's .b64 file; then check it's a PDF of the right size. Drive's default conversion is what turned master lists into empty Docs on Oct 17-18.

## sheets-spec.md (SHEETS SPEC (version 4))
- v4 (2026-11-09, revised 40): day table "Confirmed by" (each driver's route confirmation; "Route confirmed" waits for one per route and reads "[time] [names]"); Routes tab: the rows per Day set how many confirmations a weekday needs.
- v4 (2026-11-09, revised 39): Run History: Routine and Trigger values written by the Farm ops n8n routine ("Parser (n8n)", "Operator (n8n)", the fire line, the "skipped: run in progress" row).
- v4 (2026-11-09, revised 38): Config "Driver 2 (Zi) phone"; rule 11: one-to-one copies for both drivers; Driver items are for both drivers; Inbox Log Who includes Zi; "Harry last asked" and "Harry ask count" described (names kept, both drivers); Paid cash names the driver.
- v4 (2026-11-06, revised 37): rule 1: Cust ID is not a row key (a customer can have two rows on one week tab); a cell is written on the row it was read from, by row number. On Nov 6 Friday's invoice links landed one row up from the second C010 row down, and Friday's invoices were held.
- v4 (2026-11-03, revised 36): customer-table column Paid described: Square's paid date, "none: invoice canceled", or "cash $[amount] (Harry, [time])" (never invoiced).
- v4 (2026-10-28, revised 35): rule 9: an open invoice list may be replaced by one that adds newly drafted invoices (still one open). Invoice items are day items (Waiting until listed) or approval list items (the only ones Sent); Invoice Lists also holds "Invoices to approve" Docs.
- v4 (2026-10-26, revised 34): Queue columns listed in the sheet's real order (Digest # last); rule 12: build appended log rows from the tab's header row, and find log columns by label. Oct 26 Queue rows Q93-Q98 had shifted one column right (fixed by hand).
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

## parser-check.md (PARSER CHECK (version 3))
- v3 (2026-10-30): the Quo fetch gives createdAfter with the Eastern offset (from `date -d ... -Iseconds`; Quo reads a time without one as UTC) and converts Quo's UTC times to Eastern. A conversation Quo flags as having more than 10 messages is fetched on its own, page by page, and an incomplete whole-inbox read is continued with its token, so a busy conversation (most likely the family group) can't lose texts past Quo's 10-per-conversation limit. If a fetch call fails, nothing is handled and the cursor stays put. From an Oct 30 run that saw Quo return only the 10 newest messages per conversation.
- v2 (2026-10-19): dedupe reads the Inbox Log's whole Quo message ID column (the log isn't in time order).
- v1 (2026-10-17): new. The start of every run (fetch, dedupe, match the system's own texts); parser.md is only opened when there are new messages.

## week-names.md (WEEK NAMES (version 1))
- v1 (2026-10-17): new. THIS/NEXT/LAST week, tab names and missing week tabs, moved here from sheets-spec so the operator reads a small file each run.

## weekly-master-list.md (WEEKLY MASTER LIST (version 4))
- v4 (2026-11-06): the input file is built by tools/master_list_input.py from the sheet's answers saved as files (the week tab in 50-row chunks, Products, Config), never typed by the run. Nov 2 the run couldn't build the file before quiet hours; Nov 4 it wrote null for a list and master_list_pdf.py failed with TypeError; nothing went out Nov 1 to 6.
- 2026-11-06 (tools): master_list_input.py added; master_list_pdf.py names an incomplete input key instead of a bare TypeError, and treats a null cell as blank.
- v3 (2026-10-19): the PDF is saved with instructions/save-pdf.md.
- v2 (2026-10-17): Sunday to Thursday, a quick look at the Changes column first; no new changes = done without building the input file.
- v1 (2026-10-10): first version. A one-page PDF of a delivery week's totals by day and by product, made by tools/master_list_pdf.py, saved to Drive, and the link texted to the family group. Saturday: next week's list always goes out. Sunday to Thursday: this week's list goes out again only if orders changed since the last one, with the changes listed at the top. Never on Friday.

## routines/farm-ops-n8n.md
- 2026-11-10: text-admin listed among the reasons that change nothing.
- 2026-11-09: new. Run rules for the Farm ops n8n routine, fired over the API by Shane's n8n server: follows routines/farm-ops.md; puts n8n's one-line fire payload in the Run History Trigger column; writes a "skipped: run in progress" row when the run flag is held; treats the payload as data (an unexpected payload is an ALERT); the fire reason never changes the work.

## automation/n8n-fire.md
- 2026-11-10: headers (anthropic-version required, any value from 2023-06-01 on; the beta header is optional and left out); reason text-admin for texts from Config phones; the Quo webhook is made over the Quo API and its signing key lives only in the n8n server's environment.
- 2026-11-09: new. The agreement with n8n: the fire call (URL shape, headers, the one-line body), when to fire (text-received now, the :10 and :40 schedule in stage 2), the watchdog (find the row by fire id within 12 minutes, one retry on a skipped row, alerts on a channel that is not Quo), stages, Shane's one-time setup. No secrets.

## routine-prompts.md
- 2026-11-09: section for the Farm ops n8n routine (API trigger only; a loader text that opts in to reading the fire payload as the fire line and nothing more).

## routines/farm-ops.md
- 2026-11-09: notes that Farm ops n8n follows this file through routines/farm-ops-n8n.md.
- 2026-11-09: SYSTEM PROBLEMS wording: "the drivers' old replies" (Harry and Zi).
- 2026-10-27: removed the retired routines/parser.md and routines/operator.md (replaced by this file on Oct 10), and human-prompts/pdf-cloud-test.txt (needed pip and reportlab; the scripts are stdlib now). setup-starter-prompt.md fetches farm-setup.md instead of naming a Google Doc.
- 2026-10-27: hard limit 8: tools/ scripts run as a command of their own (no cd, &&, ; or pipes) so the routine's permission allow rule matches; if denied, alert and use the fallback, never another way. The permission classifier had been denying the list scripts since Oct 24.
- 2026-10-23: SYSTEM PROBLEMS: the only way to hold a day's invoicing is that day's "Invoice hold" cell, and only when a write came out wrong and couldn't be fixed; never because an old reply would now be read differently.
- 2026-10-19: reads System A1:B20 only; log rows via appendCells (sheets-spec rule 12); Run History tab.
- 2026-10-18: hard limit 9 allows reading Square payment links (for the invoice text).
- 2026-10-17: write checks: stamps and "sent" cells read back right away; everything else checked once per tab at the end of each part.
- 2026-10-17: NIGHT rule (runs between 9pm and 6:30am end at once); one RUN FLAG for the whole run; Part 1 starts with parser-check.md. Runs are meant for 6:40am to 8:40pm.
- 2026-10-17: SYSTEM PROBLEMS: read back sheet writes; ALERT problems texted to Shane.
- 2026-10-10: one Farm ops routine, parser part then operator part, twice an hour.
