#!/usr/bin/env python3
"""The Infinite Leads System: check your setup and refresh account lists from their signal searches.

Sales Navigator account lists are snapshots: they never add the companies that start matching
later. Every lead search filtered on such a list therefore goes stale. `refresh` re-reads each
saved account search and adds the new companies to its list, so the recurring Evaboot export on
the lead search picks up the people at those companies on its next run.

Talks to the hosted Evaboot MCP server (https://mcp.evaboot.com/mcp) with your Evaboot API key.
Python 3.9+, no packages to install.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

MCP_URL = "https://mcp.evaboot.com/mcp"
ROOT = Path(__file__).resolve().parent
SIGNALS_FILE = ROOT / "signals.json"
PAGE = 100
DESCRIPTION = "Check your Infinite Leads setup and refresh account lists from their signal searches."
ADD_BATCH = 999


def load_env():
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def call(tool, arguments):
    """Call one Evaboot MCP tool and return its result payload."""
    key = os.environ.get("EVABOOT_API_KEY")
    if not key:
        sys.exit("EVABOOT_API_KEY is missing. Copy .env.example to .env and add your key (README, step 2).")
    body = json.dumps(
        {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": tool, "arguments": arguments}}
    ).encode()
    request = urllib.request.Request(
        MCP_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    try:
        text = urllib.request.urlopen(request, timeout=180).read().decode()
    except urllib.error.HTTPError as error:
        sys.exit(f"{tool}: HTTP {error.code}. Check that EVABOOT_API_KEY is valid.")
    # The server answers as a server-sent event stream; the JSON-RPC message is the last data line.
    data_lines = [line[5:] for line in text.splitlines() if line.startswith("data:")]
    message = json.loads(data_lines[-1] if data_lines else text)
    if "error" in message:
        raise RuntimeError(f"{tool}: {message['error'].get('message')}")
    result = message["result"]
    if result.get("isError"):
        raise RuntimeError(f"{tool}: " + "".join(c.get("text", "") for c in result.get("content", [])))
    payload = result.get("structuredContent") or {}
    payload = payload.get("result", payload)
    return payload.get("data", payload) if isinstance(payload, dict) else payload


def company_id(urn):
    return urn.rsplit(":", 1)[-1]


def account_ids(search_url, limit):
    ids, start = [], 0
    while len(ids) < limit:
        page = call("search_sn_accounts", {"search_url": search_url, "start": start, "count": PAGE})
        elements = page.get("elements", [])
        ids += [company_id(e["entityUrn"]) for e in elements if e.get("entityUrn")]
        total = page.get("paging", {}).get("total", 0)
        start += PAGE
        if not elements or start >= total:
            break
    return ids[:limit]


def read_signals(only):
    if not SIGNALS_FILE.exists():
        sys.exit("signals.json is missing. Ask your agent to set up the system, or copy signals.example.json.")
    signals = json.loads(SIGNALS_FILE.read_text()).get("account_signals", [])
    if only:
        signals = [s for s in signals if s["name"] == only]
        if not signals:
            sys.exit(f'No account signal named "{only}" in signals.json.')
    return signals


def refresh(dry_run, only):
    signals = read_signals(only)
    if not signals:
        print("No account signals in signals.json: nothing to refresh.")
        return
    lists = {}
    start = 0
    while True:
        page = call("list_account_lists", {"start": start, "count": 100})
        for element in page.get("elements", []):
            lists[str(element["id"])] = element
        start += 100
        if start >= page.get("paging", {}).get("total", 0) or not page.get("elements"):
            break

    for signal in signals:
        list_id = str(signal["account_list_id"])
        current = lists.get(list_id)
        if current is None:
            print(f"SKIP  {signal['name']}: account list {list_id} no longer exists in Sales Navigator.")
            continue
        ids = account_ids(signal["account_search_url"], int(signal.get("max_accounts", 1000)))
        if dry_run:
            print(f"DRY   {signal['name']}: {len(ids)} companies match today, the list holds {current['entityCount']}.")
            continue
        # Adding a company that is already on the list is a no-op, so the whole match set is sent each week.
        for i in range(0, len(ids), ADD_BATCH):
            call("add_accounts_to_list", {"list_id": list_id, "company_ids": ids[i : i + ADD_BATCH]})
        after = next(
            (e for e in call("list_account_lists", {"count": 100}).get("elements", []) if str(e["id"]) == list_id),
            current,
        )
        print(
            f"OK    {signal['name']}: {len(ids)} companies match, list went from "
            f"{current['entityCount']} to {after['entityCount']} companies."
        )


def lead_url(base_url, industries, headcounts, account_list):
    """Add industry, company size or account-list filters to a Sales Navigator lead search URL."""
    parts = urllib.parse.urlsplit(base_url)
    params = urllib.parse.parse_qs(parts.query, keep_blank_values=True)
    if "/sales/search/people" not in parts.path or "query" not in params:
        sys.exit("Pass a Sales Navigator lead search URL (/sales/search/people?query=...).")
    query = params["query"][0]
    added = []
    if industries:
        values = ",".join(f"(id:{i},selectionType:INCLUDED)" for i in industries)
        added.append(f"(type:INDUSTRY,values:List({values}))")
    if headcounts:
        values = ",".join(f"(id:{h},selectionType:INCLUDED)" for h in headcounts)
        added.append(f"(type:COMPANY_HEADCOUNT,values:List({values}))")
    if account_list:
        added.append(f"(type:ACCOUNT_LIST,values:List((id:{account_list},selectionType:INCLUDED)))")
    marker = "filters:List("
    if marker not in query:
        sys.exit("The URL has no filters:List(...) to extend.")
    query = query.replace(marker, marker + "".join(f + "," for f in added), 1)
    # Free-text values stay percent-encoded inside the decoded query, so % must be encoded again.
    encoded = urllib.parse.quote(query, safe="(),:")
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path, f"query={encoded}", ""))


def check():
    token = call("verify_token", {})
    print("API key      OK" if token else "API key      unknown")
    quota = call("get_daily_export_quota", {})
    print("Quota        " + json.dumps(quota)[:200])
    recurring = call("list_recurring_exports", {})
    rows = recurring if isinstance(recurring, list) else recurring.get("results") or recurring.get("items") or []
    print(f"Recurring    {len(rows)} recurring export(s)")
    for row in rows:
        state = "paused" if row.get("paused") else "active"
        print(f"             - {row.get('name')} · {row.get('frequency')} · {state} · {len(row.get('destinations', []))} destination(s)")
    integrations = call("list_integrations", {})
    rows = integrations if isinstance(integrations, list) else integrations.get("integrations") or integrations.get("results") or []
    print(f"Destinations {len(rows)} connected")
    for row in rows:
        print(f"             - {row.get('type')} · {row.get('target_name') or row.get('label')} · source {row.get('source')}")
    if SIGNALS_FILE.exists():
        print(f"Signals      {len(read_signals(None))} account signal(s) in signals.json")


def main():
    load_env()
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="Show the API key status, quota, recurring exports and destinations")
    refresh_parser = sub.add_parser("refresh", help="Add newly matching companies to each signal's account list")
    refresh_parser.add_argument("--dry-run", action="store_true", help="Count matches, change nothing")
    refresh_parser.add_argument("--only", help="Refresh one account signal by name")
    url_parser = sub.add_parser("lead-url", help="Add industry, company size or account-list filters to a lead search URL")
    url_parser.add_argument("url", help="Sales Navigator lead search URL")
    url_parser.add_argument("--industry", action="append", default=[], help="LinkedIn industry id (repeatable)")
    url_parser.add_argument("--headcount", action="append", default=[], help="Company headcount code, e.g. D for 51-200 (repeatable)")
    url_parser.add_argument("--account-list", help="Sales Navigator account list id")
    args = parser.parse_args()
    if args.command == "check":
        check()
    elif args.command == "lead-url":
        print(lead_url(args.url, args.industry, args.headcount, args.account_list))
    else:
        refresh(args.dry_run, args.only)


if __name__ == "__main__":
    main()
