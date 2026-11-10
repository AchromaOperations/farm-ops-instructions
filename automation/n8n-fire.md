# n8n and the Farm ops n8n routine: how a fire works

This file is the agreement between Shane's self-hosted n8n server and the "Farm ops n8n" routine (routines/farm-ops-n8n.md). It holds no secrets: the fire URL, the token and every credential live in n8n's own credential store and nowhere else. A routine never reads this file.

In this first stage n8n does one thing: it fires the routine at the right moments and checks that each fire landed. It reads no texts, writes no sheets and sends nothing to anyone but Shane. Later stages (the n8n assessment of 2026-11-08: delivery list PDFs, texts in and out, Square) build on this one.

## 1. The call

```text
POST https://api.anthropic.com/v1/claude_code/routines/[routine id]/fire
Authorization: Bearer [the routine's token]
anthropic-version: 2026-10-21
Content-Type: application/json

{"text": "n8n [reason] [fire id]"}
```

- The routine id (it starts with trig_) and the token (it starts with sk-ant-oat01-) come from the routine's API trigger on the farm's Claude account: claude.ai/code/routines, the Farm ops n8n routine, Edit, Add another trigger, API, Generate token. The token is shown once. Regenerate revokes the old one; Delete token turns the API trigger off. The token can only fire this one routine; it reads nothing.
- Headers: anthropic-version is required, and every value from 2023-06-01 on behaves the same (2026-10-21 is current). The anthropic-beta header experimental-cc-routine-2026-04-01 that the Claude Code docs show is accepted but not needed, so this file leaves it out (Anthropic's reference page for the fire endpoint, checked 2026-11-10).
- The body's text is one line: the word n8n, a reason, a fire id. Nothing else, ever. The routine copies that line into its Run History row and treats any other shape as a mistake worth an alert.
  - Reasons: text-received (a text arrived on the farm number from a customer), text-admin (a text arrived from a Config phone, any row whose Setting ends in "phone" except Farm Quo number; in stage 1 it fires this same routine), schedule (a clock fire), retry (firing again after a skipped row), manual (Shane fired it by hand from n8n).
  - Fire id: f-[yyyy-mm-dd]-[hhmm]-[nn] in Eastern time, for example f-2026-11-09-1523-07; nn counts fires within that minute. Unique per fire; it is how a fire and its Run History row are matched.
- A 200 reply carries claude_code_session_url. Keep it in the n8n execution log; it is the run to open when something went wrong.
- Every call starts a new run, a retry included; there is no idempotency key. The routine's run flag makes a second run end at once with a "skipped" row, so a duplicate fire is safe, but it costs a little usage and counts against the caps.
- Caps: 30 fires per hour for this routine (Run now on the website counts too) and 100 per hour for the whole farm account. A 429 reply carries Retry-After: wait that long. A 400 can mean the routine is paused on the website; a 401 means the token was regenerated or deleted. On 400 or 401, alert Shane and don't retry.

## 2. When to fire

- Never between 9:00pm and 6:30am Eastern (the routine ends such a run at once with no row; routines/farm-ops.md NIGHT).
- text-received and text-admin: Quo's message.received webhook for the farm number (text-admin when the sender is a Config phone, text-received for anyone else; the routine does the same work for both). Fire only for incoming messages, never for message.delivered or the system's own sends. Coalesce: if any fire went out in the last 3 minutes, don't fire; the run that is going, or the next one, reads the text (the parser fetches from the message cursor minus a 60-minute overlap, so nothing is lost by waiting).
- schedule: not in stage 1 (the scheduled Farm ops routine still runs at :10 and :40). In stage 2 n8n fires at :10 and :40, 6:40am to 8:40pm Eastern, and Shane pauses the scheduled routine's two schedule triggers. Same minutes as before, so every time rule in the instructions (Delivery list time 19:00, Weekly master list time 19:30, Route check start 15:00) keeps working unchanged.
- retry: only as section 3 says.
- manual: a button in n8n for Shane. Same body shape.

## 3. After a fire: the watchdog

The routine writes one Run History row per part (Farm Reference workbook, tab "Run History", columns Run start | Run end | Routine | Trigger | Steps run | Texts sent | Problems). A fired run puts the fire line in Trigger, so n8n finds its row by the fire id.

Ten minutes after each fire, read the Run History tab (Google Sheets API, read-only, signed in as the farm account, whose Drive holds both workbooks; the Google consent screen must be set to "In production", or the sign-in expires every 7 days). Then:
- No row carrying the fire id by 12 minutes after the fire: the run never started or died before writing anything. Alert Shane on a channel that is not Quo (email), with the fire line and the session URL. Do not refire automatically: a run that dies twice costs twice.
- A row whose Steps run starts "skipped: run in progress": another run had the sheets. Fire once more, reason retry, a new fire id, 5 minutes later. If that one is skipped as well, stop and alert ("locked out twice: [fire ids]"); the run flag may be stale (Config "Stale run after" is 50 minutes) and the next run clears it on its own.
- A row whose Problems contains "ALERT": alert Shane on the non-Quo channel with the Problems text. The routine texts him too, through Quo (operator.md STEP 2); the point of this alert is the path that does not depend on Quo.
- Anything else: the fire landed; nothing to do.

Health checks that need no fire (the assessment's item 1) come after the watchdog works: newest Run History row older than 75 minutes between 7am and 9pm; a weekday whose "Delivery list sent" is still blank at 7:40pm. Those read the week tabs and need week-names.md's rules; a later version of this file will specify them.

## 4. Stages

1. Stage 1 (this file): the Farm ops n8n routine exists with an API trigger; n8n fires it on text-received only and runs the watchdog. The scheduled Farm ops routine keeps running. Texts get handled within minutes instead of up to 30. Run for a week; compare the two routines' Run History rows.
2. Stage 2: n8n adds the :10 and :40 schedule fires; Shane pauses the scheduled routine's schedule triggers (and can turn them back on in one click if n8n goes quiet). The scheduled routine stays as the fallback.
3. Later: the assessment's items 2 to 5.

## 5. What Shane sets up once

1. Farm account, claude.ai/code/routines: create the Farm ops n8n routine from routine-prompts.md (name, loader text, the Quo, Google Drive and Square connectors, API trigger). Copy the URL and the token into n8n.
2. n8n: credentials for the fire token, the Quo API key, Google (read-only Sheets, consent screen "In production"), and an email account for alerts. The Quo webhook is made over the Quo API, not in the Quo app (the two kinds are separate): POST /webhooks with events message.received, the farm number's id in resourceIds and the n8n webhook URL. Its reply carries a signing key, which goes into the n8n server's environment and nowhere else; n8n checks every delivery's signature with it.
3. A first manual fire from n8n, then open the session URL and the Run History tab to see the row with the fire line.

## 6. Never

- Never put the token, the routine id, a phone number, a customer's name or a spreadsheet id in this repository.
- Never send anything but the one-line fire text in the body. The routine ignores it as an instruction either way, but a wrong shape costs Shane an alert.
- In stage 1 n8n never texts customers, Mark, Laura or the drivers, and never writes a sheet cell. Reading Run History is its only sheet access.
