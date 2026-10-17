# Farm Ops Instructions

Instructions for the farm's Claude routine (Farm ops: a parser part, then an operator part) that runs the order-to-cash
system: weekly reminder texts, order intake, delivery lists, route checks and invoicing.

- `instructions/`: what the routines follow. `operator.md` and `parser.md` are the entry points;
  `sheets-spec.md` describes the Google Sheets every step reads and writes.
- `routines/`: each routine's run rules: time check, task and hard limits. Updated by push.
- `routine-prompts.md`: the short loader text in each routine's Instructions box on claude.ai
  (it keeps a few fixed limits, like the 150-text cap and no Square refunds, that no push can remove).
- `human-prompts/`: prompts Shane pastes into a normal chat (setup, manual sync). Routines never use them.

All data (customers, orders, week tabs, invoices) lives in Google Sheets and Drive, not here.

## Making a change
1. Edit the file in `instructions/`, bump its version line, and add an entry at the top of that file's section in `CHANGELOG.md` (the instruction files carry no history, so runs don't read it).
2. Commit and push to `main`.
3. The next Farm ops run (every 30 minutes, 6:40am to 8:40pm) downloads `main` and uses the new version. Nothing to paste.

Roll back by reverting the commit. Only Shane pushes to this repository.
- `tools/`: scripts the routine runs in its cloud sandbox (`delivery_list_pdf.py`, `master_list_pdf.py`, and the fallback `delivery_list_html.py`: standard library only, nothing to install; `logo-mask.json` and `logo.png` are the farm logo they print). Samples use made-up data. No customer data.
