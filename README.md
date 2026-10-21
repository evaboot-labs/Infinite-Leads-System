# The Infinite Leads System

Never run out of qualified leads. Wire LinkedIn Sales Navigator, Evaboot and your outreach tool
into one machine that delivers fresh, in-market prospects every week.

```
Sales Navigator         Evaboot                 Outreach campaign      Closed
saved search      ──>   recurring export  ──>   lemlist / Instantly ──> deals
+ one intent filter     only new leads,         one campaign
                        every week              per signal
```

1. **A Sales Navigator saved search** with one intent filter keeps tracking every new person who matches.
2. **An Evaboot recurring export** re-runs it daily, weekly or monthly. Each run returns only the leads added since the last one.
3. **Your outreach campaign** in lemlist or Instantly receives every new batch, with copy written for the reason you are reaching out now.
4. **You close deals.**

Give this repo to your AI agent (Claude Code, Codex, Cursor) and it sets the whole system up through
the [Evaboot MCP server](https://evaboot.com/mcp). The full guide, with screenshots:
[evaboot.com/guides/infinite-leads](https://evaboot.com/guides/infinite-leads).

Built by [Evaboot](https://evaboot.com). More workflows: [github.com/evaboot-labs](https://github.com/evaboot-labs).

## The fastest way: paste this prompt

Paste it into Claude Code, Codex or Cursor:

```text
Set up the Evaboot Infinite Leads System for me.
Clone https://github.com/evaboot-labs/Infinite-Leads-System, read AGENTS.md and follow the
evaboot-infinite-leads-system skill. Use the Evaboot MCP server at https://mcp.evaboot.com/mcp.
Ask me about my ideal customer and my outreach tool, and confirm with me before you save
any search, list or recurring export.
```

## What you need

- **LinkedIn Sales Navigator**, connected to Evaboot with the [Evaboot Chrome extension](https://evaboot.com).
- **An Evaboot account** with credits. Each recurring run spends credits for the leads it finds.
- **lemlist or Instantly**, connected once in Evaboot under
  [Integrations](https://dash.evaboot.com/dash/integrations/). Evaboot pushes every new batch into the campaign you pick.
- **An AI agent** that speaks MCP: Claude Code, Codex, Cursor, or Claude and ChatGPT with a connector.
- **Python 3.9+** for the weekly account-list refresh. No packages to install.

## Setup

1. **Get the repo.** Click **Use this template** to make your own private copy, then clone it.
2. **Connect the Evaboot MCP server.** Copy your API key from
   [dash.evaboot.com/dash/api/](https://dash.evaboot.com/dash/api/), then:
   ```bash
   cp .env.example .env          # paste the key after EVABOOT_API_KEY=
   export EVABOOT_API_KEY=...    # same key, for your agent
   ```
   - **Claude Code** reads `.mcp.json` in this folder and uses `EVABOOT_API_KEY` from your environment.
   - **Codex:** `codex mcp add evaboot --url https://mcp.evaboot.com/mcp --bearer-token-env-var EVABOOT_API_KEY`
   - **Cursor:** add `https://mcp.evaboot.com/mcp` with the header `Authorization: Bearer <your key>`.
   - **Claude or ChatGPT on the web:** add `https://mcp.evaboot.com/mcp` as a custom connector and sign in.
3. **Describe who you sell to** in [`ICP.md`](ICP.md), or let your agent ask you.
4. **Check:**
   ```bash
   python3 infinite_leads.py check
   ```

Then ask your agent: **"Set up the Infinite Leads System."**

## What the agent does

The skill, [`.claude/skills/evaboot-infinite-leads-system/SKILL.md`](.claude/skills/evaboot-infinite-leads-system/SKILL.md), walks the agent through:

1. **Lead signals.** One Sales Navigator search per intent filter (Following your company, Viewed your
   profile recently, Changed jobs, Posted on LinkedIn), built from your ICP, then made a weekly
   recurring export.
2. **Campaigns.** Each recurring export is sent to its own lemlist or Instantly campaign, with the
   opener and follow-up for that signal from [`intent-filters.md`](.claude/skills/evaboot-infinite-leads-system/references/intent-filters.md).
3. **Company signals.** Hiring on LinkedIn, senior leadership changes, funding events and headcount
   growth go through an account list, and a lead search filtered on that list becomes the recurring export.
4. **Weekly refresh.** Account lists never add the companies that match later, so
   `infinite_leads.py refresh` adds them every week.

It asks before every change to your Sales Navigator seat or Evaboot account.

## Weekly account-list refresh

`signals.json` lists each company signal: its account search, its account list, and a cap. The agent
writes it; [`signals.example.json`](signals.example.json) shows the shape.

```bash
python3 infinite_leads.py refresh --dry-run   # count today's matches, change nothing
python3 infinite_leads.py refresh             # add the new companies to each list
```

Adding a company that is already on the list does nothing, so the refresh is safe to run any time.
Run it every Monday before the weekly exports, one of three ways:

- **GitHub Actions:** in your private copy, add the `EVABOOT_API_KEY` repository secret and commit
  `signals.json`. [`.github/workflows/weekly-refresh.yml`](.github/workflows/weekly-refresh.yml)
  runs every Monday at 06:00 UTC, and **Run workflow** starts it by hand.
- **Cron:** `0 6 * * 1 cd /path/to/Infinite-Leads-System && python3 infinite_leads.py refresh`
- **Your agent's scheduler**, with the same command.

## Commands

| Command | Does |
|---|---|
| `python3 infinite_leads.py check` | API key, quota, recurring exports and their destinations |
| `python3 infinite_leads.py refresh [--dry-run] [--only NAME]` | Adds newly matching companies to each signal's account list |
| `python3 infinite_leads.py lead-url URL [--industry ID] [--headcount CODE] [--account-list ID]` | Adds industry, company size or account-list filters to a lead search URL |

## Do it by hand

No agent? The same system takes ten minutes in the browser:

1. In Sales Navigator, build your lead search (job titles, seniority, company size, geography), add
   **one** intent filter from **Buyer intent** or **Recent updates**, and save it.
2. In Evaboot, open **Sales Nav Exports**, then the **Recurring** tab, and click **Create Recurring
   Export** on that saved search. Pick the frequency.
3. Under **Integrations**, connect lemlist or Instantly and send the recurring export to a campaign.
4. For company signals, save the account search, add its results to an account list, and filter a
   lead search on that list with **Account lists**. Refresh the list every week.

## Cost

Evaboot credits for the leads each run finds. The MCP server, this repo and the refresh are free.

## License

MIT
