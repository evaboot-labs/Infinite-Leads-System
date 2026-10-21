# Company signals

Hiring on LinkedIn, senior leadership changes, funding events and headcount growth belong to the
company, so they live in a Sales Navigator **account** search. A lead search can filter on an account
list, but an account list is a snapshot: it never adds the companies that match later. That makes
company signals harder to keep running than lead signals, so the skill sets up lead signals first
and offers company signals only when you ask for them.

By hand: save the account search, add its results to an account list, filter a lead search on that
list with **Account lists**, make that lead search a recurring export, and add the new matching
companies to the list every week.

This repo can do the weekly part for you. `signals.json` lists each company signal: its account
search, its account list, and a cap; [`signals.example.json`](../signals.example.json) shows the shape.

```bash
python3 infinite_leads.py refresh --dry-run   # count today's matches, change nothing
python3 infinite_leads.py refresh             # add the new companies to each list
```

Adding a company that is already on the list does nothing, so the refresh is safe to run any time.
Run it every Monday before the weekly exports:

- **GitHub Actions:** in your private copy, add the `EVABOOT_API_KEY` repository secret and commit
  `signals.json`. [`.github/workflows/weekly-refresh.yml`](../.github/workflows/weekly-refresh.yml)
  runs every Monday at 06:00 UTC, and **Run workflow** starts it by hand.
- **Cron:** `0 6 * * 1 cd /path/to/infinite-leads-system && python3 infinite_leads.py refresh`
- **Your agent's scheduler**, with the same command.

## Commands

| Command | Does |
|---|---|
| `python3 infinite_leads.py check` | API key, quota, recurring exports and their destinations |
| `python3 infinite_leads.py lead-url URL [--industry ID] [--headcount CODE] [--account-list ID]` | Adds industry, company size or account-list filters to a lead search URL |
| `python3 infinite_leads.py refresh [--dry-run] [--only NAME]` | Company signals: adds newly matching companies to each signal's account list |

Back to the [README](../README.md).
