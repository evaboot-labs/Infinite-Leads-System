---
name: evaboot-infinite-leads-system
description: Set up the Evaboot Infinite Leads System for the user - Sales Navigator saved searches with intent filters, Evaboot recurring exports that return only new leads, and lemlist or Instantly campaigns that receive each batch, directly or through a Make scenario. Company signals through account lists are an optional extra. Use when the user asks to set up infinite leads, a lead machine, recurring Sales Navigator exports into an outreach campaign, or to refresh their signal account lists.
---

# Evaboot Infinite Leads System

This skill runs inside a clone of https://github.com/evaboot-labs/Infinite-Leads-System: it uses the repo's `infinite_leads.py`, `ICP.md`, README.md and the Make and n8n files. If `infinite_leads.py` is not in the working directory, clone the repo and work from there.

The system is three pieces wired together, and the fourth is the result:

1. **Sales Navigator saved search** with one intent filter: it keeps tracking every new person who matches.
2. **Evaboot recurring export** of that search: daily, weekly or monthly, each run returns only the leads added since the last one.
3. **Outreach campaign** in lemlist or Instantly: every new batch lands there automatically.
4. **Close deals.**

You do it all through the Evaboot MCP server (`https://mcp.evaboot.com/mcp`). Every tool named below is an Evaboot MCP tool.

Set up lead signals (steps 1 and 2) first: they need nothing but a saved search and a recurring export. Offer company signals (the extra at the end) only when the user asks for them or picks one.

## Rules

- Confirm with the user before every call that writes to their Sales Navigator seat or account: `create_recurring_export`, `connect_integration`, `attach_recurring_export`, `create_account_list`, `add_accounts_to_list`, `save_search`. Show what you will create, then wait for a yes.
- Never invent `max_results`. Ask the user how many results they want before `build_sn_search_from_prompt`.
- Call `build_sn_search_from_prompt` once per request, then poll `get_search_build` with the `build_id` until the status is no longer `building`. Never call the builder again for the same request while it builds.
- Never ask for, read or paste an API key of lemlist, Instantly or any other tool. The user connects those in Evaboot at https://dash.evaboot.com/dash/integrations/.
- Print every Sales Navigator URL as a Markdown link with the URL in angle brackets: `[Open the search in Sales Navigator](<url>)`.
- Each recurring run spends Evaboot credits for the leads it finds. Say so before the first one is created.

## Step 0: get the user an Evaboot account and connect it

Most users start without an Evaboot account. Ask first: "Do you already have an Evaboot account with Sales Navigator connected?" If the Evaboot MCP tools are not available in this session, assume the answer is no.

If they have no account, walk them through it one step at a time and wait for each "done":

1. **Create the account:** send them to [https://dash.evaboot.com/accounts/signup/?last_click_origin=infinite-leads-repo](https://dash.evaboot.com/accounts/signup/?last_click_origin=infinite-leads-repo).
2. **Connect Sales Navigator:** they install the Evaboot Chrome extension from [dash.evaboot.com/install/](https://dash.evaboot.com/install/) and follow its steps to connect their Sales Navigator account. They need an active Sales Navigator seat.
3. **Get the API key:** they copy it from [dash.evaboot.com/dash/api/](https://dash.evaboot.com/dash/api/) and paste it after `EVABOOT_API_KEY=` in `.env` (copy `.env.example` first). Do not ask them to paste the key in the chat.
4. **Connect the MCP server:** give them the line for their client from README.md, step 3, then ask them to restart the agent session in this folder so the Evaboot tools load. Claude and ChatGPT on the web sign in through the browser instead and need no key.

Then check the setup:

1. Call `verify_token` and `get_daily_export_quota`. `has_valid_salesnav` must be true; if it is false, send them back to step 2 above. If `credits` is 0, tell them each recurring run spends credits for the leads it finds and send them to [dash.evaboot.com/dash/pricing/](https://dash.evaboot.com/dash/pricing/).
2. Ask how the leads should reach the campaign: **directly** (Evaboot's lemlist or Instantly integration, the default), or **through Make** or **through n8n** (when they want to filter, enrich or route leads there first). For directly, call `list_integrations` and look for a row of type `lemlist` or `instantly`. If neither is there, send the user to https://dash.evaboot.com/dash/integrations/providers/lemlist/connect/ (or `/instantly/connect/`) to connect it with their own API key, and wait. For Make or n8n, nothing to connect yet: step 2 covers it.
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

### Directly to lemlist or Instantly

1. Call `list_integration_targets` with `type` `lemlist` or `instantly` and show the campaigns.
2. For each recurring export, ask which campaign gets it. Then call `connect_integration` with `type`, `auto: true`, `target_id` (the campaign id), `source: "recurring"` and `recurring_ids: [<recurring export id>]`.
3. If the user prefers one campaign for every signal and a matching destination already exists, call `attach_recurring_export` with its `integration_id` instead.

### Through Make

One Make scenario per signal, from `make/infinite-leads-to-lemlist.blueprint.json` (https://raw.githubusercontent.com/evaboot-labs/Infinite-Leads-System/main/make/infinite-leads-to-lemlist.blueprint.json). It receives each run on a webhook and adds every lead with an email to one lemlist campaign. For each recurring export:

1. Walk the user through README.md, section "Make", steps 1 and 2: import the blueprint, add the webhook on **New leads from Evaboot**, and paste you the webhook URL (`https://hook.<zone>.make.com/...`). A webhook URL is not a secret.
2. After a yes, call `connect_integration` with `type: "make"`, `url` (the webhook URL), `auto: true`, `label: "Infinite Leads · <signal>"`, `source: "recurring"` and `recurring_ids: [<recurring export id>]`. If `next` is `test`, ask the user to switch the scenario on, then call `test_integration`.
3. The user fills in **Your settings** in Make: their lemlist API key and the campaign id (`cam_...` in the campaign's URL). Never ask them to paste the lemlist key to you.
4. The user switches the scenario on. Make's free plan runs two active scenarios, so with more than two signals they need a paid plan or one shared campaign.

The blueprint targets lemlist. For another tool, the user swaps **Add the lead to the campaign** for that tool's module in Make.

### Through n8n

One n8n workflow per signal, from `n8n/infinite-leads-to-lemlist.n8n.json` (https://raw.githubusercontent.com/evaboot-labs/Infinite-Leads-System/main/n8n/infinite-leads-to-lemlist.n8n.json). It does what the Make scenario does. For each recurring export:

1. Run `python3 n8n/new_workflow.py "<signal>"` (add the lemlist campaign id if the user gives it). It writes `n8n/infinite-leads-<signal>.n8n.json` with a random webhook path: the path is the only lock on that webhook, so never reuse the template's path, never commit the copy, and never print the Production URL anywhere but your call. Then walk the user through README.md, section "n8n": import that file, fill in **Your settings**, connect lemlist on **Add the lead to the campaign**, and paste you the **Production URL** of **New leads from Evaboot**. Never ask them to paste the lemlist key to you.
2. After a yes, call `connect_integration` with `type: "n8n"`, `url` (the Production URL), `auto: true`, `label: "Infinite Leads · <signal>"`, `source: "recurring"` and `recurring_ids: [<recurring export id>]`. If `next` is `test`, ask the user to activate the workflow, then call `test_integration`.

Give the user the opener and follow-up for each signal from [references/intent-filters.md](references/intent-filters.md) to paste into that campaign's sequence. You cannot write the sequence for them.

## Finish

Run `python3 infinite_leads.py check` and give the user a table: signal, recurring export, cadence, campaign, next run. Remind them to paste the copy into each campaign and to read the replies: the last step, closing deals, is theirs.

## Extra: company signals through an account list

Only when the user asks for a company signal.

Hiring, senior leadership changes, funding events and headcount growth belong to the company, so they live in the account search. A lead search can filter on an account list, but an account list is a snapshot: it never adds the companies that match later. This repo's `refresh` command keeps it fresh.

For each picked account signal:

1. Call `build_sn_search_from_prompt` and ask for companies, not people, for example: `Companies in France with 51-200 employees that are hiring on LinkedIn`. A company request returns `strategy: "accounts"` and an account search `url`. Do not name people in this request: a people request with a vertical starts a company-first crawl that writes lists on the seat.
2. After a yes, call `create_account_list` with `name` set to `Infinite Leads · <signal>`.
3. Add this signal to `signals.json` (see `signals.example.json`): `name`, `account_search_url`, `account_list_id`, `max_accounts` (default 1000, the list's useful ceiling).
4. Fill the list: run `python3 infinite_leads.py refresh --only "<name>"`, or call `search_sn_accounts` page by page and `add_accounts_to_list` with the company ids from each `entityUrn`.
5. Build the lead search on that list: call `build_sn_search_from_prompt` for the ICP people with no signal (job titles, seniority, geography only), then run `python3 infinite_leads.py lead-url "<url>" --account-list <account_list_id>`. Call `search_sn_leads` on the result to check it returns people at those companies.
6. Call `create_recurring_export` with that `url` (a people search filtered on an account list stays that lead search), name it, and route it as in step 2.

Then add the signal to the finish table.

### Keep the account lists fresh every week

Offer the user one of these, in this order:

1. **GitHub Actions** (no machine to keep on): push this repo to a private GitHub repository, add the `EVABOOT_API_KEY` secret, and commit `signals.json`. `.github/workflows/weekly-refresh.yml` runs `refresh` every Monday at 06:00 UTC, before the weekly exports.
2. **Cron**: `0 6 * * 1 cd /path/to/repo && python3 infinite_leads.py refresh`.
3. **Their agent's scheduler**, running `python3 infinite_leads.py refresh` weekly.

Run `python3 infinite_leads.py refresh --dry-run` first and show the counts.
