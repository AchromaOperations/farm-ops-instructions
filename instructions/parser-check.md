PARSER CHECK (version 3)
Written for: sheets-spec version 4

JOB
The first part of every run: find texts that haven't been handled yet. Most runs find none and stop here, without opening parser.md or sheets-spec. You never send texts.

STEP 0. START
a. Now: run `TZ=America/New_York date '+%a %Y-%m-%d %H:%M'` and use that output as now for every time you write or compare. (The computer clock is UTC; never use plain `date`.)
b. Use the Config and System values the RUN FLAG step already read (routines/farm-ops.md). Read no other tab yet.

STEP 1. FETCH
a. Fetch messages on the farm Quo number, incoming and outgoing, from start = (System "Message cursor" minus Config "Cursor overlap") to now. Quo's fetch-messages works like this, so follow every point:
   - Quo reads a time with no offset as UTC, 4 or 5 hours off. Run `TZ=America/New_York date -d '[start, as yyyy-mm-dd hh:mm]' -Iseconds` (it prints, for example, 2026-10-30T18:09:00-04:00) and pass that output exactly as createdAfter. Quo's own message times are UTC too: convert each one to Eastern before you compare or write it (sheets-spec rule 3).
   - Fetch the whole inbox (no participant filter), so group conversations are included. The family group (exactly Mark's and Laura's numbers, Config "Owner (Mark) phone" and "Backup (Laura) phone") is one of them; each of its messages shows who sent it.
   - Quo returns at most 10 messages per conversation. A conversation it flags "[more than 10 ...]" has more: fetch that conversation on its own with the parameter the flag names (one number, or the group's whole member list), the same createdAfter and maxResults 100, following each pageToken until there is none or a page reaches messages older than start. Use those messages for that conversation instead of its 10.
   - If a reply has an "[incomplete: ...]" line with a "[next_conversations: ...]" token, make the same call again with that token as conversationPageToken, until no token is left.
   - One call at a time, never several at once (Quo then returns incomplete results).
   - If any of these calls fails, handle nothing this run: record an ALERT Problem "Quo fetch incomplete: [what the reply said]" and end Part 1 (the cursor doesn't move, so the next run fetches the same texts again).
   Then keep only messages after start and put them all in time order, oldest first.
b. Read the Inbox Log's whole Quo message ID column (that one column, every row: the log is not in time order, so never just the last rows; sheets-spec rule 12). Drop any message whose ID is already there.
   Then match the system's own texts: for each OUTGOING message left, look among the Inbox Log rows whose Quo message ID is "pending" or "(not returned by Quo)" (find them in that column) for one with Direction "Out (system)", the same To (a number, or "Group: ..." for a family group text), the same text, and a Time within 15 minutes of the message. If found: write the message's real ID into that row's Quo message ID and drop the message. Do not add a new row. Each log row matches at most one message.

STEP 2. DECIDE
- Nothing left: Part 1 is done. Write nothing else (no run history row; Part 2's row notes "parser: nothing new"). Do not read anything else.
- Messages left: open ops/instructions/parser.md and follow it from its STEP 1, with these messages, now, and the Config and System values you already read.
