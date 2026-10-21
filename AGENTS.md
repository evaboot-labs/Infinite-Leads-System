# Agent instructions

This repo sets up the Evaboot Infinite Leads System: Sales Navigator saved searches with intent filters, Evaboot recurring exports that return only new leads, and lemlist or Instantly campaigns that receive each batch. When the user asks to set it up, add a signal, or refresh their account lists:

1. Check that the Evaboot MCP server is connected (its tools include `verify_token`). If not, give the user the setup line for their client from README.md, step 2, and stop.
2. Follow the skill in `.claude/skills/evaboot-infinite-leads-system/SKILL.md` step by step. Read `ICP.md` first and interview the user if it still holds the example.
3. Use `python3 infinite_leads.py lead-url` to add industry, company size or account-list filters to a search URL. Never put an industry in a people request to the search builder.
4. Confirm with the user before every call that saves a search, a list, a recurring export or a destination.
5. Finish with `python3 infinite_leads.py check` and a table of what was set up.

Never ask for or handle a lemlist, Instantly or other tool's API key: the user connects those in Evaboot. Never commit `.env`.
