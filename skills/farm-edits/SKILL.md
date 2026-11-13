---
name: farm-edits
description: Change the Restoration Farmstead sheets by hand from a chat, under the repository's manual-edits rules. Use when someone asks to add, change, skip, note or close something for a customer ("add 2 dozen eggs for Kim this week", "Jennifer Grove: add to delivery notes ...", "Nate is skipping this week", "Bert's share is 1 gallon now", "no charge on her butter", "close Queue item Q204", "that invoice was canceled in Square"). It writes sheet cells only. It never sends a text, never touches Drive files, and never edits the routine's own tabs beyond what manual-edits.md allows.
---

FARM EDITS (version 1)
Written for: manual-edits version 8, sheets-spec version 4

WHO THIS IS FOR
A chat on the farm's Claude account asked to change the sheets "Farm Reference" or "Weekly Deliveries". The person is Laura unless they say they are Shane or Mark (manual-edits.md says so); don't ask who they are.

STEP 1. GET THE INSTRUCTIONS WITH GIT (first, before anything else)
Run these two commands in the chat's sandbox:
    rm -rf ops
    git clone --depth 1 https://github.com/AchromaOperations/farm-ops-instructions.git ops
Check: `head -1 ops/instructions/manual-edits.md` must print a line starting "MANUAL EDITS (version", and `head -1 ops/instructions/sheets-spec.md` must print "SHEETS SPEC (version 4)".
- The repository is public; git needs no sign-in. Never add a GitHub repository or connector to the chat, and never sign the farm account in to GitHub.
- Don't fetch these files with curl, wget or the web tool. The web tool opens only links that already appear in the conversation, and it refused the manual-edits link kept in the account's preferences (that is what stopped a chat from adding a delivery note on 2026-11-13).
- If git fails: try the clone once more, then stop and say what git printed. Change nothing without the clone. The person can instead paste the full manual-edits link into the chat, which the web tool can then open; follow it from there.

STEP 2. READ, FROM THE CLONE
- ops/instructions/manual-edits.md: the authority for everything this skill does. Follow it exactly, section by section: FIRST, READING THE SHEETS, BEFORE CHANGING AN ORDER, MAKING A CHANGE, the two sections that apply only when the person says they are Shane, NEVER, FINISH.
- The files its FIRST step names (sheets-spec.md, week-names.md, and parser.md's ORDER WRITING and A4 sections): read them from ops/instructions/. Reading them from the clone satisfies that step; its links are for chats that have no clone.

STEP 3. DO WHAT MANUAL-EDITS SAYS
- Time is Eastern: `TZ=America/New_York date '+%Y-%m-%d %H:%M'`.
- Find the workbooks as sheets-spec rule 5 says (a Drive search for the Google Sheet "Farm Reference", whose Config A1 reads "RF-OPS REFERENCE v1", and "Weekly Deliveries" in the same folder).
- An order, a skip, a standing order change, customer info (phone, address, email, delivery notes) or a free item: manual-edits MAKING A CHANGE.
- "Close Queue item ..." or "the invoice was canceled or deleted in Square": manual-edits' two Shane-only sections, and only when the person has said they are Shane. Otherwise say those two need Shane, and change nothing.
- Mention, once, that a command like this texted to the family group is done by the routine within minutes (parser A4); then do what was asked here anyway.

NEVER (manual-edits NEVER, and these)
- Fetch repository files with curl, wget or the web tool, or add a GitHub repository or connector.
- Send a text or message, or create or edit a Drive file.
- Do a change manual-edits says to leave alone (a locked row, a filled stamp, the routine's tabs beyond the Shane-only sections, prices, sync). Say why instead.

IF SOMETHING FAILS
One line: which step, which tool, what it said. No more than one retry per step. A change that didn't land is reported, never redone from memory.
