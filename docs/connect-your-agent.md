# Connect your agent by hand

The prompt in the README does all of this for you. These are the same steps, for when you want to do them yourself.

1. **Create your Evaboot account** at [dash.evaboot.com](https://dash.evaboot.com/accounts/signup/?last_click_origin=infinite-leads-repo) and install the [Chrome extension](https://dash.evaboot.com/install/) to connect Sales Navigator.
2. **Get the repo.** Click **[Use this template](https://github.com/evaboot-labs/infinite-leads-system/generate)** to make your own private copy, then clone it.
3. **Connect the Evaboot MCP server.** Copy your API key from
   [dash.evaboot.com/dash/api/](https://dash.evaboot.com/dash/api/), then:
   ```bash
   cp .env.example .env          # paste the key after EVABOOT_API_KEY=
   export EVABOOT_API_KEY=...    # same key, for your agent
   ```
   - **Claude Code** reads `.mcp.json` in this folder and uses `EVABOOT_API_KEY` from your environment.
   - **Codex:** `codex mcp add evaboot --url https://mcp.evaboot.com/mcp --bearer-token-env-var EVABOOT_API_KEY`
   - **Cursor:** add `https://mcp.evaboot.com/mcp` with the header `Authorization: Bearer <your key>`.
   - **Claude or ChatGPT on the web:** add `https://mcp.evaboot.com/mcp` as a custom connector and sign in.
4. **Describe who you sell to** in [`ICP.md`](../ICP.md), or let your agent ask you.
5. **Check** (Python 3.9+, no packages to install):
   ```bash
   python3 infinite_leads.py check
   ```

Then ask your agent: **"Set up the Infinite Leads System."**

Back to the [README](../README.md).
