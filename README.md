# Farm Ops Instructions

Instructions for the farm's Claude routines (Farm ops on a schedule, and Farm ops n8n fired by Shane's n8n server; each run is a parser part, then an operator part) that run the order-to-cash
system: weekly reminder texts, order intake, delivery lists, route checks and invoicing.

- `instructions/`: what the routines follow. `operator.md` and `parser.md` are the entry points;
  `sheets-spec.md` describes the Google Sheets every step reads and writes.
- `routines/`: each routine's run rules: time check, task and hard limits. Updated by push. `farm-ops.md` is the scheduled routine; `farm-ops-n8n.md` is the same work fired over the API by Shane's n8n server (it follows `farm-ops.md` and lists its few differences).
- `routine-prompts.md`: the short loader text in each routine's Instructions box on claude.ai
  (it keeps a few fixed limits, like the 150-text cap and no Square refunds, that no push can remove).
- `human-prompts/`: prompts Shane pastes into a normal chat (setup, manual sync). Routines never use them.
- `automation/`: what Shane's n8n server does around the routines (`n8n-fire.md`: how it fires the Farm ops n8n routine and checks that each fire landed). No secrets live here. Routines never read it.
- `skills/`: skills for normal chats on the farm account (one folder per skill, each with a `SKILL.md`). Shane uploads them under Settings, Capabilities, Skills; this is the source copy. Routines never use them.
- `instructions/manual-edits.md`: rules for any normal chat on the farm account that changes the sheets by hand. The account's profile preferences tell every chat to fetch it first. Routines never use it.

All data (customers, orders, week tabs, invoices) lives in Google Sheets and Drive, not here.

## Making a change
1. Edit the file in `instructions/`, bump its version line, and add an entry at the top of that file's section in `CHANGELOG.md` (the instruction files carry no history, so runs don't read it).
2. Commit and push to `main`.
3. The next Farm ops run (every 30 minutes, 6:40am to 8:40pm) downloads `main` and uses the new version. Nothing to paste.

Roll back by reverting the commit. Only Shane pushes to this repository.
- `tools/`: scripts the routine runs in its cloud sandbox (`delivery_list_pdf.py`, `master_list_pdf.py`, and the fallback `delivery_list_html.py`: standard library only, nothing to install; `logo-mask.json` and `logo.png` are the farm logo they print). Samples use made-up data. No customer data.
