PARSER CHECK (version 1)
Written for: sheets-spec version 4

JOB
The first part of every run: find texts that haven't been handled yet. Most runs find none and stop here, without opening parser.md or sheets-spec. You never send texts.

STEP 0. START
a. Now: run `TZ=America/New_York date '+%a %Y-%m-%d %H:%M'` and use that output as now for every time you write or compare. (The computer clock is UTC; never use plain `date`.)
b. Use the Config and System values the RUN FLAG step already read (routines/farm-ops.md). Read no other tab yet.

STEP 1. FETCH
a. Fetch messages on the farm Quo number, incoming and outgoing, from (System "Message cursor" minus Config "Cursor overlap") to now, oldest first. Include group conversations. The family group (exactly Mark's and Laura's numbers, Config "Owner (Mark) phone" and "Backup (Laura) phone") is one of them; each of its messages shows who sent it.
b. Drop any message whose Quo message ID is already in the Inbox Log (only search Inbox Log rows from the last 2 days; older IDs can't be in the window).
   Then match the system's own texts: for each OUTGOING message left, look for an Inbox Log row with Direction "Out (system)", Quo message ID "pending" or "(not returned by Quo)", the same To (a number, or "Group: ..." for a family group text), the same text, and a Time within 15 minutes of the message. If found: write the message's real ID into that row's Quo message ID and drop the message. Do not add a new row. Each log row matches at most one message.

STEP 2. DECIDE
- Nothing left: Part 1 is done. Write nothing else (no run history row; Part 2's row notes "parser: nothing new"). Do not read anything else.
- Messages left: open ops/instructions/parser.md and follow it from its STEP 1, with these messages, now, and the Config and System values you already read.
