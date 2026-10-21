# Agent instructions

This repo sets up the Evaboot Infinite Leads System: Sales Navigator saved searches with intent filters, Evaboot recurring exports that return only new leads, and lemlist or Instantly campaigns that receive each batch. Lead signals come first; company signals through account lists are an optional extra. When the user asks to set it up, add a signal, or refresh their account lists:

1. If the Evaboot MCP tools (such as `verify_token`) are not available, the user most likely has no Evaboot account yet. Follow step 0 of the skill: create the account at https://dash.evaboot.com/accounts/signup/?last_click_origin=infinite-leads-repo, install the Chrome extension, put the API key in `.env`, connect the MCP server, restart the session.
2. Follow the skill in `skills/evaboot-infinite-leads-system/SKILL.md` step by step. Read `ICP.md` first and interview the user if it still holds the example.
3. Use `python3 infinite_leads.py lead-url` to add industry, company size or account-list filters to a search URL. Never put an industry in a people request to the search builder.
4. Confirm with the user before every call that saves a search, a list, a recurring export or a destination.
5. If the user sends leads through Make or n8n, follow the skill's step 2, "Through Make" or "Through n8n", and the matching README.md section. The user pastes the webhook URL to you and their lemlist key into Make or n8n, never to you.
6. Finish with `python3 infinite_leads.py check` and a table of what was set up.

Never ask for or handle a lemlist, Instantly or other tool's API key: the user connects those in Evaboot, Make or n8n. Never commit `.env`.
