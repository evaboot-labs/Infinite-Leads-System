---
name: evaboot-infinite-leads-system
description: Set up the Evaboot Infinite Leads System for the user - Sales Navigator saved searches with intent filters, Evaboot recurring exports that return only new leads, and lemlist or Instantly campaigns that receive each batch - then keep the account-signal lists fresh every week. Use when the user asks to set up infinite leads, a lead machine, recurring Sales Navigator exports into an outreach campaign, or to refresh their signal account lists.
---

# Evaboot Infinite Leads System

The system is three pieces wired together, and the fourth is the result:

1. **Sales Navigator saved search** with one intent filter: it keeps tracking every new person who matches.
2. **Evaboot recurring export** of that search: daily, weekly or monthly, each run returns only the leads added since the last one.
3. **Outreach campaign** in lemlist or Instantly: every new batch lands there automatically.
4. **Close deals.**

You do it all through the Evaboot MCP server (`https://mcp.evaboot.com/mcp`). Every tool named below is an Evaboot MCP tool.

## Rules

- Confirm with the user before every call that writes to their Sales Navigator seat or account: `create_recurring_export`, `connect_integration`, `attach_recurring_export`, `create_account_list`, `add_accounts_to_list`, `save_search`. Show what you will create, then wait for a yes.
- Never invent `max_results`. Ask the user how many results they want before `build_sn_search_from_prompt`.
- Call `build_sn_search_from_prompt` once per request, then poll `get_search_build` with the `build_id` until the status is no longer `building`. Never call the builder again for the same request while it builds.
- Never ask for, read or paste an API key of lemlist, Instantly or any other tool. The user connects those in Evaboot at https://dash.evaboot.com/dash/integrations/.
- Print every Sales Navigator URL as a Markdown link with the URL in angle brackets: `[Open the search in Sales Navigator](<url>)`.
- Each recurring run spends Evaboot credits for the leads it finds. Say so before the first one is created.

## Step 0: check the setup

1. Call `verify_token` and `get_daily_export_quota`. `has_valid_salesnav` must be true. If it is false, the user has to connect Sales Navigator with the Evaboot Chrome extension first; stop and tell them.
2. Call `list_integrations`. Look for a row of type `lemlist` or `instantly`. If neither is there, send the user to https://dash.evaboot.com/dash/integrations/providers/lemlist/connect/ (or `/instantly/connect/`) to connect it with their own API key, and wait.
3. Read `ICP.md` in this repo. If it still holds the example, interview the user and rewrite it: who they sell to (job titles, seniority, company size, industry, geography), what they sell, and which outreach tool they use.

## Step 1: one saved search per lead signal

Read [references/intent-filters.md](references/intent-filters.md). Propose the four lead signals (Following your company, Viewed your profile recently, Changed jobs, Posted on LinkedIn) and let the user pick.

**Industry and company size never go in the builder request.** A people request that names an industry or vertical makes the builder start a company-first crawl that writes account lists on the user's seat. Resolve them separately and add them to the URL yourself:

1. If the ICP has an industry or a company size, call `build_sn_search_from_prompt` once for companies only, for example `Companies in France in the Software Development industry with 51-200 employees`. A company request is read-only and returns `strategy: "accounts"`. Keep `filters_used.industries[].id` and `filters_used.companySize` (codes such as `D` for 51-200).

For each picked signal:

1. Call `build_sn_search_from_prompt` with people only: job titles, seniority, geography and the signal in plain words, for example `Heads of Sales in France who changed jobs recently`, and the user's `max_results`.
2. Poll `get_search_build`. The result must have `strategy: "leads"`. If it says `company-first` or returns a `job_id`, call `cancel_sales_nav_job` once with `kind: "account_based_search"`, drop the words that sounded like an industry, and build again. Check `filters_used` carries the signal (for example `recently_changed_jobs: true`).
3. Add the industry and size: `python3 infinite_leads.py lead-url "<url>" --industry 4 --headcount D` (repeat a flag for several values). Call `search_sn_leads` on the new URL and check the total and the first companies look right.
4. Show the link, the total and the builder's assumptions. Ask for a yes.
5. Call `create_recurring_export` with `url` and the cadence (default `weekly`). It saves the search on the user's seat and schedules it. The next run is one interval later and includes only new leads.
6. Call `update_recurring_export` with `name` set to `Infinite Leads · <signal>`.

## Step 2: send each run to its campaign

One campaign per signal, so the copy matches the reason for reaching out.

1. Call `list_integration_targets` with `type` `lemlist` or `instantly` and show the campaigns.
2. For each recurring export, ask which campaign gets it. Then call `connect_integration` with `type`, `auto: true`, `target_id` (the campaign id), `source: "recurring"` and `recurring_ids: [<recurring export id>]`.
3. If the user prefers one campaign for every signal and a matching destination already exists, call `attach_recurring_export` with its `integration_id` instead.

Give the user the opener and follow-up for each signal from [references/intent-filters.md](references/intent-filters.md) to paste into that campaign's sequence. You cannot write the sequence for them.

## Step 3: company signals through an account list

Hiring, senior leadership changes, funding events and headcount growth belong to the company, so they live in the account search. A lead search can filter on an account list, but an account list is a snapshot: it never adds the companies that match later. This repo's `refresh` command keeps it fresh.

For each picked account signal:

1. Call `build_sn_search_from_prompt` and ask for companies, not people, for example: `Companies in France with 51-200 employees that are hiring on LinkedIn`. A company request returns `strategy: "accounts"` and an account search `url`. Do not name people in this request: a people request with a vertical starts a company-first crawl that writes lists on the seat.
2. After a yes, call `create_account_list` with `name` set to `Infinite Leads · <signal>`.
3. Add this signal to `signals.json` (see `signals.example.json`): `name`, `account_search_url`, `account_list_id`, `max_accounts` (default 1000, the list's useful ceiling).
4. Fill the list: run `python3 infinite_leads.py refresh --only "<name>"`, or call `search_sn_accounts` page by page and `add_accounts_to_list` with the company ids from each `entityUrn`.
5. Build the lead search on that list: call `build_sn_search_from_prompt` for the ICP people with no signal (job titles, seniority, geography only), then run `python3 infinite_leads.py lead-url "<url>" --account-list <account_list_id>`. Call `search_sn_leads` on the result to check it returns people at those companies.
6. Call `create_recurring_export` with that `url` (a people search filtered on an account list stays that lead search), name it, and route it as in step 2.

## Step 4: keep the account lists fresh every week

Offer the user one of these, in this order:

1. **GitHub Actions** (no machine to keep on): push this repo to a private GitHub repository, add the `EVABOOT_API_KEY` secret, and commit `signals.json`. `.github/workflows/weekly-refresh.yml` runs `refresh` every Monday at 06:00 UTC, before the weekly exports.
2. **Cron**: `0 6 * * 1 cd /path/to/repo && python3 infinite_leads.py refresh`.
3. **Their agent's scheduler**, running `python3 infinite_leads.py refresh` weekly.

Run `python3 infinite_leads.py refresh --dry-run` first and show the counts.

## Finish

Run `python3 infinite_leads.py check` and give the user a table: signal, recurring export, cadence, campaign, next run. Remind them to paste the copy into each campaign and to read the replies: the last step, closing deals, is theirs.
