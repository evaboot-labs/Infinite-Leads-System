# Infinite Leads System to the evaboot-labs repo standard (P1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring `evaboot-labs/infinite-leads-system` to the repo standard by hand: a visual README under 5 KB, setup detail moved to `docs/`, a Claude Code plugin manifest, real screenshots, a recorded demo, and a draft PR that JB reviews.

**Architecture:** This is P1 of three plans for the spec `docs/specs/2026-10-21-evaboot-labs-repo-standard-design.md`. P2 (the global `evaboot-labs-repo` skill in `~/agent-setup`) and P3 (the four other repos) are written only after this PR merges, from the approved result. Every change here is Markdown, JSON, HTML image sources and binary images; no Python changes. Images are rendered with headless Chrome and processed with `ffmpeg` and `sips`, all already installed.

**Tech Stack:** Markdown (GitHub-flavoured), Claude Code plugin manifests, headless Google Chrome, `ffmpeg`, `sips`, the `browser-screen-control`, `use-interactive-terminal` and `desktop-control` skills, `gh`.

**Dependency Graph:**
- Wave 1: Task 1, Task 3, Task 4 (parallel)
- Wave 2: Task 2
- Wave 3: Task 5
- Wave 4: Task 6
- Wave 5: Task 7

---

## Context the executor needs

- **Repo:** `evaboot-labs/infinite-leads-system`, public, template mode on, default branch `main`. Main checkout: `~/.superset/projects/Infinite-Leads-System`. Repo names are always lowercase.
- **The spec and this plan must not reach the public repo.** They are committed on the checkout's local `main` only so `executing-plans` can seed them. Task 7 removes `docs/specs/` and `docs/plans/` from the work branch before the PR. The durable copies live in `~/.superset/projects/evaboot-website-v2/docs/specs/` and `docs/plans/`.
- **Copy rules** (from the spec; apply to every line of copy you write):
  - Product links go to `dash.evaboot.com` only, never `app.evaboot.com`.
  - Say "AI Agent", never "AI Assistant".
  - Outreach is "any outreach tool", with lemlist as the example. Never present lemlist (or lemlist and Instantly) as the only option.
  - No claim of a free trial. "The MCP server and this repo are free" is fine: that is not a trial.
- **GitHub settings are already complete for this repo** (checked 2026-10-21): description, homepage `https://evaboot.com/guides/infinite-leads`, 7 topics, MIT, template mode. Only the social preview is missing; it is set after the merge (see Rollout).
- **The Evaboot API key:** the demo (Task 5) needs JB's existing `EVABOOT_API_KEY` in `.env` at the workspace root. There is no `.env` in the main checkout. If it is missing, collect it with the `env-prompt` skill; never ask for it in chat and never print it.
- **Skills to invoke:** `browser-screen-control` (screenshots, Sales Navigator and Evaboot UI, README render check), `use-interactive-terminal` (the agent sessions in Tasks 5 and 7), `desktop-control` (Terminal window placement for the recording, if `osascript` is blocked), `codex-review` mode=docs on the README and docs pages in Task 7. TDD here means each task starts with a shell check that fails, then makes it pass.
- **Verified on 2026-10-21 in a scratch clone:** the two manifests in Task 3 pass `claude plugin validate`, and `/plugin marketplace add ./` + `/plugin install infinite-leads-system@evaboot-labs-infinite-leads-system` install one skill (`evaboot-infinite-leads-system`) and one MCP server (`evaboot`). The banner and signals HTML in Task 4 render to 1280×640 PNGs of about 90 KB each with the command given there.

---

### Task 1: Move setup detail out of the README into docs pages

**Blocked by:** none

**Files:**
- Reuse: `README.md:57-186` *(source text, moved verbatim with the edits listed below; README.md itself is rewritten in Task 6)*
- Create: `docs/connect-your-agent.md`
- Create: `docs/make.md`
- Create: `docs/n8n.md`
- Create: `docs/manual-setup.md`
- Create: `docs/company-signals.md`

`docs/connect-your-agent.md` is a fifth page the spec's list does not name: the README's "Setup" section (account, template, MCP connection per client, `ICP.md`, `check`) has no other home once the README follows the new section order, and the skill's step 0 points users to it.

- [ ] **Step 1: Write the failing check**

```bash
for f in connect-your-agent make n8n manual-setup company-signals; do test -s docs/$f.md || echo "missing docs/$f.md"; done
```

- [ ] **Step 2: Run it; expect five failures**

Expected output, exactly:
```
missing docs/connect-your-agent.md
missing docs/make.md
missing docs/n8n.md
missing docs/manual-setup.md
missing docs/company-signals.md
```

- [ ] **Step 3: Create `docs/connect-your-agent.md`**

Title `# Connect your agent by hand`. One intro line: "The prompt in the README does all of this for you. These are the same steps, for when you want to do them yourself." Then `README.md:59-77` verbatim (the five numbered setup steps and the closing "Then ask your agent" line), with these edits:
- Relative links gain `../`: `[\`ICP.md\`](../ICP.md)`.
- Step 2 keeps "Click **Use this template**", linking it to `https://github.com/evaboot-labs/infinite-leads-system/generate`.
- End with a "Back to the [README](../README.md)" line.

- [ ] **Step 4: Create `docs/make.md`**

Title `# Send leads through Make`. Body: `README.md:94-113` verbatim. Then append: "The blueprint targets lemlist. For any other outreach tool, swap the **Add the lead to the campaign** module for that tool's module in Make." (the same fact the skill states at `skills/evaboot-infinite-leads-system/SKILL.md:83`). End with "Back to the [README](../README.md)".

- [ ] **Step 5: Create `docs/n8n.md`**

Title `# Send leads through n8n`. Body: `README.md:117-131` verbatim. Append the same any-tool sentence, adapted: "swap the **Add the lead to the campaign** node for that tool's node in n8n." End with the back link.

- [ ] **Step 6: Create `docs/manual-setup.md`**

Title `# Do it by hand`. Body: `README.md:135-141` verbatim. In step 3, change "connect lemlist or Instantly and send the recurring export to a campaign" to "connect your outreach tool (lemlist or Instantly connect directly; any other tool through [Make](make.md) or [n8n](n8n.md)) and send the recurring export to a campaign." End with the back link.

- [ ] **Step 7: Create `docs/company-signals.md`**

Title `# Company signals`. Body: `README.md:145-170` verbatim, then a `## Commands` section with the table at `README.md:174-178` verbatim. Fix the relative links: `[\`signals.example.json\`](../signals.example.json)` and `[\`.github/workflows/weekly-refresh.yml\`](../.github/workflows/weekly-refresh.yml)`. End with the back link.

- [ ] **Step 8: Run the check again; expect no output**

Run the Step 1 command. Expected: no output. Then check every relative link in the new pages resolves:

```bash
cd docs && for f in *.md; do grep -o '](\.\{0,2\}/\{0,1\}[^)#:]*)' "$f" | sed 's/^](//; s/)$//' | while read -r p; do test -e "$p" || echo "$f: broken link $p"; done; done; cd ..
```

Expected: no output.

- [ ] **Step 9: Commit**

```bash
git add docs/connect-your-agent.md docs/make.md docs/n8n.md docs/manual-setup.md docs/company-signals.md
git commit -m "docs: move Make, n8n, manual setup and company signals out of the README"
```

---

### Task 2: Point AGENTS.md and the skill at the new docs pages

**Blocked by:** Task 1

**Files:**
- Modify: `AGENTS.md:9`
- Modify: `skills/evaboot-infinite-leads-system/SKILL.md:8,39,78,89`

- [ ] **Step 1: Write the failing check**

```bash
grep -n 'README' AGENTS.md skills/evaboot-infinite-leads-system/SKILL.md
```

- [ ] **Step 2: Run it; expect five hits**

Expected: lines `AGENTS.md:9`, `SKILL.md:8`, `SKILL.md:39`, `SKILL.md:78`, `SKILL.md:89`, each naming README.md.

- [ ] **Step 3: Edit the five lines**

- `AGENTS.md:9` (step 5): replace "and the matching README.md section" with "and `docs/make.md` or `docs/n8n.md`".
- `SKILL.md:8`: replace "`ICP.md`, README.md and the Make and n8n files" with "`ICP.md`, the `docs/` pages and the Make and n8n files".
- `SKILL.md:39`: replace "the line for their client from README.md, step 3" with "the line for their client from `docs/connect-your-agent.md`, step 3".
- `SKILL.md:78`: replace "README.md, section \"Make\", steps 1 and 2" with "`docs/make.md`, steps 1 and 2".
- `SKILL.md:89`: replace "README.md, section \"n8n\"" with "`docs/n8n.md`".

- [ ] **Step 4: Run the check again; expect no output**

Run the Step 1 command. Expected: no output. Then confirm AGENTS.md stays under 60 lines: `wc -l < AGENTS.md` prints a number below 60 (it is 13 today).

- [ ] **Step 5: Commit**

```bash
git add AGENTS.md skills/evaboot-infinite-leads-system/SKILL.md
git commit -m "Point AGENTS.md and the skill at the new docs pages"
```

---

### Task 3: Add the Claude Code plugin and marketplace manifests

**Blocked by:** none

**Files:**
- Reuse: `.mcp.json` *(unchanged; referenced by plugin.json)*
- Create: `.claude-plugin/marketplace.json`
- Create: `.claude-plugin/plugin.json`

- [ ] **Step 1: Run the failing check**

```bash
claude plugin validate .claude-plugin/marketplace.json
```

Expected: exit 1 with `✘ Found 1 error:` and `file: File not found: …/.claude-plugin/marketplace.json`. (Do not use `claude plugin validate .` as the red check: it passes without a manifest, because a `skills/` tree alone is accepted as a plugin.)

- [ ] **Step 2: Create `.claude-plugin/marketplace.json`**

```json
{
  "name": "evaboot-labs-infinite-leads-system",
  "owner": { "name": "Evaboot", "url": "https://evaboot.com" },
  "metadata": {
    "description": "Evaboot Labs: the Infinite Leads System as a Claude Code plugin."
  },
  "plugins": [
    {
      "name": "infinite-leads-system",
      "source": "./",
      "description": "Sales Navigator saved searches with intent filters, Evaboot recurring exports and outreach campaigns, set up by your agent through the Evaboot MCP server."
    }
  ]
}
```

- [ ] **Step 3: Create `.claude-plugin/plugin.json`**

```json
{
  "name": "infinite-leads-system",
  "version": "1.0.0",
  "description": "Sales Navigator saved searches with intent filters, Evaboot recurring exports and outreach campaigns, set up by your agent through the Evaboot MCP server.",
  "author": { "name": "Evaboot", "url": "https://evaboot.com" },
  "homepage": "https://evaboot.com/guides/infinite-leads",
  "repository": "https://github.com/evaboot-labs/infinite-leads-system",
  "license": "MIT",
  "privacyPolicyUrl": "https://evaboot.com/privacy-policy",
  "keywords": ["sales-navigator", "lead-generation", "evaboot", "mcp"],
  "skills": "./skills/",
  "mcpServers": "./.mcp.json"
}
```

- [ ] **Step 4: Run both validations; expect PASS**

```bash
claude plugin validate .claude-plugin/marketplace.json && claude plugin validate .
```

Expected: `✔ Validation passed` for the marketplace, and `✔ Validation passed with warnings` for the folder, both exit 0. Accepted warnings: `ICON_MISSING` (no listing icon; the plugin directory is not a target) and, until Task 6 lands, "This README has no line that installs \"infinite-leads-system\"". Any `✘` is a failure.

- [ ] **Step 5: Install it in a throwaway Claude config; expect the skill and the MCP server**

```bash
C=$(mktemp -d) && CLAUDE_CONFIG_DIR="$C" claude plugin marketplace add ./ \
  && CLAUDE_CONFIG_DIR="$C" claude plugin install infinite-leads-system@evaboot-labs-infinite-leads-system \
  && CLAUDE_CONFIG_DIR="$C" claude plugin details infinite-leads-system@evaboot-labs-infinite-leads-system | grep -E 'Skills|MCP servers'
```

Expected: `Successfully installed plugin`, then `Skills (1)  evaboot-infinite-leads-system` and `MCP servers (1)  evaboot`. The temp config dir keeps JB's real Claude settings untouched.

- [ ] **Step 6: Commit**

```bash
git add .claude-plugin/marketplace.json .claude-plugin/plugin.json
git commit -m "Add the Claude Code plugin and marketplace manifests"
```

---

### Task 4: Render the banner and the signals figure

**Blocked by:** none

**Files:**
- Create: `.github/assets/src/banner.html`
- Create: `.github/assets/src/signals.html`
- Create: `.github/assets/banner-light.png`
- Create: `.github/assets/banner-dark.png`
- Create: `.github/assets/signals-light.png`
- Create: `.github/assets/signals-dark.png`

The two HTML sources are committed under `.github/assets/src/` so the PNGs can be re-rendered and so P2 can turn them into the skill's parameterized template. This folder is not in the spec's file layout; P2 decides whether the standard keeps it.

- [ ] **Step 1: Write the failing check**

```bash
for f in banner-light banner-dark signals-light signals-dark; do
  p=.github/assets/$f.png
  test -f "$p" || { echo "missing $p"; continue; }
  sips -g pixelWidth -g pixelHeight "$p" | awk 'NR>1{print $2}' | paste -sd x - | grep -qx 1280x640 || echo "wrong size $p"
done
test -f .github/assets/banner-light.png && [ "$(wc -c < .github/assets/banner-light.png)" -lt 1048576 ] || echo "banner-light.png missing or over 1 MB"
```

- [ ] **Step 2: Run it; expect five failures**

Expected: `missing .github/assets/banner-light.png`, `missing …banner-dark.png`, `missing …signals-light.png`, `missing …signals-dark.png`, and `banner-light.png missing or over 1 MB`.

- [ ] **Step 3: Create `.github/assets/src/banner.html`**

This is the approved v3 mockup (`evaboot-website-v2/.superpowers/brainstorm/80259-1792583240/content/hero-banner-v3.html`) at a fixed 1280×640, with a dark palette switched on by `?theme=dark`.

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Infinite Leads System banner</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<script>if (new URLSearchParams(location.search).get("theme") === "dark") document.documentElement.classList.add("dark");</script>
<style>
  :root { --brand: #5719D9; --ink: #1A1A2E; --muted: #6B6B80; --line: #D9CCF7; --surface: #F9F7FF; --card: #FFFFFF;
          --dot: rgba(87, 25, 217, .16); --rail: #E4DBFA; --screw: #CDBDF5; --eyebrow: #5719D9; --dash: rgba(87, 25, 217, .45); --arrow: rgba(87, 25, 217, .6);
          --shadow: rgba(87, 25, 217, .08); }
  .dark { --ink: #F3F0FF; --muted: #A9A3C2; --line: #2F2752; --surface: #110E1C; --card: #1A1630;
          --dot: rgba(139, 92, 246, .22); --rail: #261F42; --screw: #3D3170; --eyebrow: #A78BFA; --dash: rgba(167, 139, 250, .5); --arrow: rgba(167, 139, 250, .7);
          --shadow: rgba(0, 0, 0, .35); }
  * { box-sizing: border-box; }
  html, body { margin: 0; width: 1280px; height: 640px; overflow: hidden; }
  body { font-family: Manrope, system-ui, sans-serif; color: var(--ink); }
  .art { width: 1280px; height: 640px; position: relative; overflow: hidden;
         background-color: var(--surface);
         background-image: radial-gradient(var(--dot) 1.4px, transparent 1.4px);
         background-size: 24px 24px; background-position: 12px 12px; }
  .rails { position: absolute; top: 0; bottom: 0; left: 64px; right: 64px; border-left: 1px solid var(--rail); border-right: 1px solid var(--rail); }
  .screw { position: absolute; width: 8px; height: 8px; border-radius: 50%; background: var(--screw); }
  .tl { left: 20px; top: 20px; } .tr { right: 20px; top: 20px; } .bl { left: 20px; bottom: 20px; } .br { right: 20px; bottom: 20px; }
  .mono { font-family: "JetBrains Mono", ui-monospace, monospace; text-transform: uppercase; letter-spacing: .14em; }
  .eyebrow { position: absolute; left: 112px; top: 80px; display: flex; align-items: center; gap: 12px; font-size: 15px; font-weight: 600; color: var(--eyebrow); }
  .eyebrow i { width: 10px; height: 10px; border-radius: 2px; background: var(--brand); }
  h1 { position: absolute; left: 112px; top: 120px; margin: 0; font-size: 64px; line-height: 1.05; font-weight: 800; letter-spacing: -.03em; white-space: nowrap; }
  .sub { position: absolute; left: 112px; top: 208px; margin: 0; font-size: 24px; font-weight: 500; color: var(--muted); }
  .flow { position: absolute; left: 112px; right: 112px; top: 328px; display: grid; grid-template-columns: 1fr 48px 1fr 48px 1fr 48px 1fr; align-items: center; }
  .node { height: 200px; background: var(--card); border: 1px solid var(--line); border-radius: 4px; padding: 24px; position: relative;
          box-shadow: 0 10px 30px var(--shadow); display: flex; flex-direction: column; }
  .node .k { font-size: 12px; font-weight: 600; color: var(--eyebrow); }
  .node b { margin-top: 16px; min-height: 2.2em; font-size: 26px; font-weight: 800; letter-spacing: -.02em; line-height: 1.1; }
  .node span { margin-top: 12px; font-size: 16px; color: var(--muted); line-height: 1.35; }
  .node .led { position: absolute; right: 20px; top: 24px; width: 8px; height: 8px; border-radius: 50%; background: #22C55E; box-shadow: 0 0 0 4px rgba(34, 197, 94, .15); }
  .node.last { background: var(--brand); border-color: var(--brand); color: #fff; box-shadow: 0 14px 36px rgba(87, 25, 217, .35); }
  .node.last .k, .node.last span { color: #E3D8FF; }
  .link { height: 2px; position: relative; border-top: 2px dashed var(--dash); }
  .link::after { content: ""; position: absolute; right: -2px; top: -7px; border-left: 10px solid var(--arrow); border-top: 6px solid transparent; border-bottom: 6px solid transparent; }
  .spec { position: absolute; left: 112px; bottom: 56px; display: flex; align-items: center; gap: 12px; font-size: 13px; color: var(--muted); }
  .spec i { width: 8px; height: 8px; border-radius: 50%; background: #22C55E; }
  .spec em { font-style: normal; text-transform: none; letter-spacing: .02em; color: var(--ink); }
</style>
</head>
<body>
<div class="art">
  <div class="rails"></div>
  <div class="screw tl"></div><div class="screw tr"></div><div class="screw bl"></div><div class="screw br"></div>
  <div class="eyebrow mono"><i></i>evaboot-labs · infinite-leads-system</div>
  <h1>Never run out of qualified leads.</h1>
  <p class="sub">Fresh, in-market prospects from Sales Navigator, delivered every week.</p>
  <div class="flow">
    <div class="node"><div class="led"></div><div class="k mono">01 · Search</div><b>Sales Navigator</b><span>Saved search with one intent filter</span></div>
    <div class="link"></div>
    <div class="node"><div class="led"></div><div class="k mono">02 · Export</div><b>Evaboot</b><span>Recurring export, only new leads</span></div>
    <div class="link"></div>
    <div class="node"><div class="led"></div><div class="k mono">03 · Outreach</div><b>Any outreach tool</b><span>lemlist, Instantly or your own</span></div>
    <div class="link"></div>
    <div class="node last"><div class="k mono">04 · Result</div><b>Closed deals</b><span>A new batch, every week</span></div>
  </div>
  <div class="spec mono"><i></i>server <em>mcp.evaboot.com/mcp</em> · give this repo to your agent</div>
</div>
</body>
</html>
```

- [ ] **Step 4: Create `.github/assets/src/signals.html`**

Copy `banner.html`, then make exactly these changes:
- `<title>` becomes `Infinite Leads System signals`.
- Delete the `.flow`, `.node*`, `.link*` and `.spec*` CSS rules, and add before `</style>`:

```css
  .cards { position: absolute; left: 112px; right: 112px; top: 296px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
  .card { height: 264px; background: var(--card); border: 1px solid var(--line); border-radius: 4px; padding: 24px; box-shadow: 0 10px 30px var(--shadow); display: flex; flex-direction: column; }
  .card .k { font-size: 12px; font-weight: 600; color: var(--eyebrow); }
  .card b { margin-top: 14px; font-size: 24px; font-weight: 800; letter-spacing: -.02em; line-height: 1.1; min-height: 2.2em; }
  .card q { margin-top: auto; font-size: 15px; line-height: 1.4; color: var(--muted); quotes: "\201C" "\201D"; }
  .card q u { text-decoration: none; color: var(--eyebrow); font-weight: 700; }
```

- Replace everything inside `<div class="art">` after the four screws with:

```html
  <div class="eyebrow mono"><i></i>evaboot-labs · lead signals</div>
  <h1>Four signals, four campaigns.</h1>
  <p class="sub">One intent filter per search, one opener per campaign.</p>
  <div class="cards">
    <div class="card"><div class="k mono">01 · Buyer intent</div><b>Following your company</b><q>You follow <u>{{companyName}}</u> on LinkedIn, so you have probably seen what we do with <u>{{yourTopic}}</u>.</q></div>
    <div class="card"><div class="k mono">02 · Buyer intent</div><b>Viewed your profile</b><q>Saw you checked my profile, so I'll keep this short.</q></div>
    <div class="card"><div class="k mono">03 · Recent updates</div><b>Changed jobs</b><q>Congrats on the new role at <u>{{companyName}}</u>. The first 90 days are when most <u>{{jobTitle}}</u>s rethink <u>{{yourTopic}}</u>.</q></div>
    <div class="card"><div class="k mono">04 · Recent updates</div><b>Posted on LinkedIn</b><q>Your recent post on <u>{{postTopic}}</u> made me think of a problem we solve for <u>{{jobTitle}}</u>s.</q></div>
  </div>
```

The openers are the ones in `skills/evaboot-infinite-leads-system/references/intent-filters.md:14,21,28,35`. If that file changes, change these too.

- [ ] **Step 5: Render the four PNGs**

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for name in banner signals; do for t in light dark; do
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --window-size=1280,640 --virtual-time-budget=8000 \
    --screenshot="$PWD/.github/assets/$name-$t.png" "file://$PWD/.github/assets/src/$name.html?theme=$t"
done; done
```

`--virtual-time-budget` lets Google Fonts load; without network access the text falls back to system fonts, which is a failure (check in Step 7).

- [ ] **Step 6: Run the Step 1 check again; expect no output**

If `banner-light.png` is ever 1 MB or more (expected size is about 90 KB), re-encode and check again:

```bash
ffmpeg -y -loglevel error -i .github/assets/banner-light.png -vf "format=rgb24" -compression_level 100 /tmp/banner-light.png && mv /tmp/banner-light.png .github/assets/banner-light.png
```

If it is still 1 MB or more, stop and report: the banner cannot be the social preview.

- [ ] **Step 7: Look at all four images**

Open each PNG with the Read tool. Each must show Manrope headings and JetBrains Mono labels (not Times or Helvetica), nothing clipped at the edges, the purple fourth node on the banner, and in the dark versions light text on the near-black dot grid.

- [ ] **Step 8: Commit**

```bash
git add .github/assets/src/banner.html .github/assets/src/signals.html .github/assets/banner-light.png .github/assets/banner-dark.png .github/assets/signals-light.png .github/assets/signals-dark.png
git commit -m "Add the Blueprint banner and the four-signals figure"
```

---

### Task 5: Record the demo, capture the screenshots, then remove what the demo created

**Blocked by:** Task 2

**Files:**
- Create: `.github/assets/demo.gif`
- Create: `.github/assets/demo.mp4`
- Create: `.github/assets/screenshots/1-saved-search.png`
- Create: `.github/assets/screenshots/2-recurring-export.png`
- Create: `.github/assets/screenshots/3-outreach-tool.png`

This task spends a few Evaboot credits and creates a real saved search and a real recurring export on JB's accounts. Both are deleted in Step 11, whatever happens before it. If any step fails, jump to Step 11 before stopping.

- [ ] **Step 1: Write the failing check**

```bash
for f in demo.gif demo.mp4 screenshots/1-saved-search.png screenshots/2-recurring-export.png screenshots/3-outreach-tool.png; do test -f .github/assets/$f || echo "missing $f"; done
test -f .github/assets/demo.gif && [ "$(wc -c < .github/assets/demo.gif)" -lt 5242880 ] || echo "demo.gif missing or over 5 MB"
for f in .github/assets/screenshots/*.png; do [ "$(sips -g pixelWidth "$f" 2>/dev/null | awk 'NR>1{print $2}')" = 1600 ] || echo "not 1600 px: $f"; done
```

- [ ] **Step 2: Run it; expect failures**

Expected: five `missing …` lines, `demo.gif missing or over 5 MB`, and `not 1600 px: .github/assets/screenshots/*.png` (the glob matches nothing yet).

- [ ] **Step 3: Record the starting state, so the cleanup can be proven**

```bash
python3 infinite_leads.py check > /tmp/ils-check-before.txt; cat /tmp/ils-check-before.txt
```

Needs `.env` with `EVABOOT_API_KEY` (see Context). Expected: `API key      OK` and the current list of recurring exports. Then, with `browser-screen-control` in JB's signed-in Chrome profile, open `https://www.linkedin.com/sales/search/saved-searches/people` and note the saved searches already there (screenshot to `/tmp/ils-saved-searches-before.png`).

- [ ] **Step 4: Prepare the recording window**

1. Make a clean clone for the demo agent so the recording shows a real first run: `git clone -q "$PWD" /tmp/ils-demo && cp .env /tmp/ils-demo/.env`. The `.env` copy is never shown on screen and is deleted in Step 11.
2. Start an agent terminal session with the `use-interactive-terminal` skill, `cd /tmp/ils-demo`, and set a large, readable font (at least 16 pt).
3. Open it in its own Terminal.app window at a fixed size: `osascript -e 'tell application "Terminal" to do script "tmux attach -t <agent-term session>"' -e 'tell application "Terminal" to set bounds of front window to {0, 25, 1280, 825}'` (use `desktop-control` if AppleScript is blocked).
4. Find the screen device: `ffmpeg -f avfoundation -list_devices true -i "" 2>&1 | grep -i "capture screen"`. Note its index `<N>`.

- [ ] **Step 5: Record a real agent run**

Start the capture in the background (Retina doubles pixels, so the crop is twice the window bounds):

```bash
ffmpeg -y -loglevel error -f avfoundation -capture_cursor 0 -framerate 30 -i "<N>:none" \
  -vf "crop=2560:1600:0:50" -c:v libx264 -preset veryfast -crf 20 /tmp/ils-demo-raw.mp4
```

Grab one frame after 3 seconds (`ffmpeg -sseof -1 -i /tmp/ils-demo-raw.mp4 -frames:v 1 /tmp/frame.png` from a copy, or a `desktop-control` screenshot) and check the crop shows only the terminal window. Fix the crop and restart if not.

In the agent terminal, run `claude` and paste exactly:

```text
Set up the Evaboot Infinite Leads System for me. Read AGENTS.md and follow the
evaboot-infinite-leads-system skill. My ideal customer: VP of Sales at software
companies with 51-200 employees in Luxembourg. Set up one lead signal only,
Changed jobs, as a weekly recurring export named "Infinite Leads demo · Changed jobs".
Send it to no campaign for now. Confirm with me before you save anything.
```

Answer "yes" to each confirmation question for the saved search and the recurring export. Decline anything else (a destination, an account list, more signals). When it reports done, ask it to run `python3 infinite_leads.py check`. Stop the capture (`q` to ffmpeg, or kill it with SIGINT) once the check table is on screen for 3 seconds.

Write down, from the transcript, the saved search's name and the recurring export's id and name. Step 11 needs them.

The key must never appear on screen. If it does, discard the recording and start again from Step 5.

- [ ] **Step 6: Make the MP4 and the GIF**

```bash
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 /tmp/ils-demo-raw.mp4)
F=$(python3 -c "print(max(1.0, $D / 20))")
ffmpeg -y -loglevel error -i /tmp/ils-demo-raw.mp4 -vf "scale=1280:-2" -c:v libx264 -crf 28 -pix_fmt yuv420p -movflags +faststart .github/assets/demo.mp4
ffmpeg -y -loglevel error -i /tmp/ils-demo-raw.mp4 \
  -vf "setpts=PTS/$F,fps=12,scale=1200:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" \
  .github/assets/demo.gif
ls -l .github/assets/demo.gif .github/assets/demo.mp4
```

The MP4 is the full run at real speed; the GIF is the same run sped up to about 20 s. If the GIF is 5 MB or more, rerun the GIF command with `scale=960` and `fps=10`. If the MP4 is over 25 MB, raise `-crf` to 32. Look at the GIF's first and last frames: the prompt must be readable at the start and the `check` table at the end.

- [ ] **Step 7: Capture screenshot 1, the saved search**

With `browser-screen-control` in JB's Chrome profile, open the saved search the demo created in Sales Navigator, with the filter panel open so "Changed jobs" is visible next to the results. Take a full-window screenshot to `/tmp/shot1.png`. Crop to the filter panel plus the first results and resize:

```bash
ffmpeg -y -loglevel error -i /tmp/shot1.png -vf "crop=<w>:<h>:<x>:<y>" /tmp/shot1-crop.png
sips --resampleWidth 1600 /tmp/shot1-crop.png --out .github/assets/screenshots/1-saved-search.png
```

Pick `<w>:<h>:<x>:<y>` from the screenshot. The crop must be at least 1600 px wide before resampling (on Retina it is). No blur: real captures are the decision (spec, Decisions).

- [ ] **Step 8: Capture screenshot 2, the recurring export**

Open `https://dash.evaboot.com`, then **Sales Nav Exports**, then the **Recurring** tab, with "Infinite Leads demo · Changed jobs" visible in the list. Same crop and resize, to `.github/assets/screenshots/2-recurring-export.png`.

- [ ] **Step 9: Capture screenshot 3, the outreach tool**

Open `https://dash.evaboot.com/dash/integrations/` with lemlist visible among the providers (lemlist is the example; the caption says any outreach tool). Same crop and resize, to `.github/assets/screenshots/3-outreach-tool.png`. Do not open a connect form or show any key.

- [ ] **Step 10: Run the Step 1 check again; expect no output**

Then look at the three screenshots with the Read tool: each is sharp, cropped to the panel, and readable at 800 px wide.

- [ ] **Step 11: Delete everything the demo created (always runs)**

1. **Recurring export:** if the Evaboot MCP `tools/list` offers a delete tool for recurring exports, call it with the id from Step 5. Otherwise, with `browser-screen-control`, open **Sales Nav Exports → Recurring** in `dash.evaboot.com`, open the row menu of "Infinite Leads demo · Changed jobs" and delete it.
2. **Saved search:** with `browser-screen-control`, open `https://www.linkedin.com/sales/search/saved-searches/people` and delete the saved search named in Step 5.
3. **Local copies:** `rm -f /tmp/ils-demo/.env` and remove the `/tmp/ils-demo` clone.
4. **Prove it (spec Verification 10):**

```bash
python3 infinite_leads.py check > /tmp/ils-check-after.txt; diff /tmp/ils-check-before.txt /tmp/ils-check-after.txt && echo CLEAN
```

Expected: `CLEAN`. A quota line that differs because credits were spent is the only accepted difference; a recurring export line containing "Infinite Leads demo" is a failure. Then screenshot the Sales Navigator saved searches page again to `/tmp/ils-saved-searches-after.png` and compare it with the "before" screenshot: no search created by the demo remains. Keep both "after" artefacts for the PR description (Task 7).

- [ ] **Step 12: Commit**

```bash
git add .github/assets/demo.gif .github/assets/demo.mp4 .github/assets/screenshots/1-saved-search.png .github/assets/screenshots/2-recurring-export.png .github/assets/screenshots/3-outreach-tool.png
git commit -m "Add the demo recording and the three How it works screenshots"
```

---

### Task 6: Rewrite the README in the approved section order

**Blocked by:** Task 1, Task 3, Task 4, Task 5

**Files:**
- Modify: `README.md` *(full rewrite)*

- [ ] **Step 1: Write the failing check**

```bash
python3 - <<'EOF'
import os, re, sys
t = open("README.md").read()
errors = []
if len(t.encode()) >= 5120: errors.append(f"README is {len(t.encode())} bytes")
if "app.evaboot.com" in t: errors.append("links app.evaboot.com")
if "prefers-color-scheme: dark" not in t: errors.append("no dark <picture> source")
for path in re.findall(r'(?:src|srcset)="([^"]+)"|\]\(([^)#\s]+)\)', t):
    p = path[0] or path[1]
    if not p.startswith(("http", "mailto:")) and not os.path.exists(p): errors.append(f"broken {p}")
for heading in ["## Set it up in one prompt", "## How it works", "## Four signals, four campaigns", "## What you need", "## Go further"]:
    if heading not in t: errors.append(f"missing {heading}")
print("\n".join(errors)); sys.exit(1 if errors else 0)
EOF
```

- [ ] **Step 2: Run it; expect FAIL**

Expected: exit 1, with `README is 11…` bytes (about 11 KB), `no dark <picture> source`, and the five `missing ## …` lines.

- [ ] **Step 3: Write the new `README.md`**

Replace the whole file with the text below. Keep it exactly; only fix a fact if the repo proves it wrong.

~~~~markdown
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/banner-dark.png">
  <img src=".github/assets/banner-light.png" alt="Sales Navigator saved search, Evaboot recurring export, any outreach tool, closed deals: a new batch of leads every week" width="1280">
</picture>

# The Infinite Leads System

Never run out of qualified leads. Sales Navigator finds them, Evaboot exports only the new ones every week, and your outreach tool contacts them.

[![Works with Claude Code · Codex · Cursor](https://img.shields.io/badge/works%20with-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Cursor-5719D9)](AGENTS.md)
[![MCP server](https://img.shields.io/badge/MCP-mcp.evaboot.com-5719D9)](https://evaboot.com/mcp)
[![License: MIT](https://img.shields.io/badge/license-MIT-5719D9)](LICENSE)
[![Use this template](https://img.shields.io/badge/template-use%20this%20template-5719D9)](https://github.com/evaboot-labs/infinite-leads-system/generate)

[![An AI Agent builds a Sales Navigator search and a weekly Evaboot export, then shows the check table](.github/assets/demo.gif)](.github/assets/demo.mp4)

<sub>The full run, at real speed: [demo.mp4](.github/assets/demo.mp4)</sub>

## Set it up in one prompt

Paste this into Claude Code, Codex or Cursor:

```text
Set up the Evaboot Infinite Leads System for me.
Clone https://github.com/evaboot-labs/infinite-leads-system, read AGENTS.md and follow the
evaboot-infinite-leads-system skill. Use the Evaboot MCP server at https://mcp.evaboot.com/mcp.
If I have no Evaboot account yet, walk me through creating one first. Ask me about my ideal
customer and my outreach tool, and confirm with me before you save any search, list or
recurring export.
```

<details>
<summary>Or install the skill</summary>

Claude Code:

```text
/plugin marketplace add evaboot-labs/infinite-leads-system
/plugin install infinite-leads-system@evaboot-labs-infinite-leads-system
```

Codex, Cursor and other agents:

```bash
npx skills add evaboot-labs/infinite-leads-system
```

</details>

## How it works

**1. Save a search.** One intent filter keeps it tracking new people.

<img src=".github/assets/screenshots/1-saved-search.png" alt="A Sales Navigator saved search with the Changed jobs filter" width="800">

**2. Export it weekly.** Each run returns only the leads added since the last one.

<img src=".github/assets/screenshots/2-recurring-export.png" alt="The Recurring tab of Sales Nav Exports in Evaboot" width="800">

**3. Send it to a campaign.** Every batch lands in your outreach tool, one campaign per signal.

<img src=".github/assets/screenshots/3-outreach-tool.png" alt="Evaboot integrations, with lemlist as the outreach tool" width="800">

## Four signals, four campaigns

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/signals-dark.png">
  <img src=".github/assets/signals-light.png" alt="Four lead signals, each with its opener: following your company, viewed your profile, changed jobs, posted on LinkedIn" width="1280">
</picture>

Each signal gets its own saved search, recurring export and campaign, with copy written for the reason you are reaching out now: [intent-filters.md](skills/evaboot-infinite-leads-system/references/intent-filters.md).

## What you need

- **An Evaboot account.** [Create one](https://dash.evaboot.com/accounts/signup/?last_click_origin=infinite-leads-repo), or paste the prompt and your agent walks you through sign-up.
- **LinkedIn Sales Navigator**, connected with the [Evaboot Chrome extension](https://dash.evaboot.com/install/).
- **Any outreach tool.** lemlist and Instantly connect in Evaboot under [Integrations](https://dash.evaboot.com/dash/integrations/); any other tool works through [Make](docs/make.md) or [n8n](docs/n8n.md).
- **An AI Agent that speaks MCP:** Claude Code, Codex, Cursor, or Claude and ChatGPT with a connector.
- **Cost:** Evaboot credits for the leads each run finds. The MCP server and this repo are free.

## Go further

| Page | For |
|---|---|
| [Connect your agent by hand](docs/connect-your-agent.md) | The MCP setup for each agent, `ICP.md` and the `check` command |
| [Make scenario](docs/make.md) | Filter, enrich or route leads in Make before the campaign |
| [n8n workflow](docs/n8n.md) | The same, in n8n |
| [Company signals](docs/company-signals.md) | Hiring, funding, leadership changes and headcount growth through account lists, plus every command |
| [Do it by hand](docs/manual-setup.md) | Ten minutes in the browser, no agent |

---

Agents: start at [AGENTS.md](AGENTS.md) · Built by [Evaboot](https://evaboot.com) · More workflows at [github.com/evaboot-labs](https://github.com/evaboot-labs) · [MIT license](LICENSE)
~~~~

- [ ] **Step 4: Run the Step 1 check again; expect PASS**

Expected: exit 0, no output. Then `wc -c < README.md` prints a number below 5120, and `claude plugin validate .` no longer warns that the README has no install line.

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "Rewrite the README: banner, demo, one prompt, screenshots, docs links"
```

---

### Task 7: Verify the branch end to end, write the PR description, strip the internal docs

**Blocked by:** Task 2, Task 6

**Files:**
- Delete: `docs/specs/2026-10-21-evaboot-labs-repo-standard-design.md`
- Delete: `docs/plans/2026-10-21-evaboot-labs-repo-standard.md`

Everything in this task that needs GitHub runs against the pushed work branch `2026-10-21-evaboot-labs-repo-standard`. Pushing the work branch needs no permission (project git autonomy); merging does.

- [ ] **Step 1: Review the docs**

Run `codex-review` mode=docs on `README.md`, `AGENTS.md`, `docs/*.md` and the edited `SKILL.md` lines, against the copy rules in Context. Fix critical and high findings, commit them, and rerun Task 6 Step 1 and Task 3 Step 4.

- [ ] **Step 2: Sizes (spec Verification 7)**

```bash
[ "$(wc -c < README.md)" -lt 5120 ] && [ "$(wc -l < AGENTS.md)" -lt 60 ] \
  && [ "$(wc -c < .github/assets/demo.gif)" -lt 5242880 ] && [ "$(wc -c < .github/assets/banner-light.png)" -lt 1048576 ] && echo SIZES-OK
```

Expected: `SIZES-OK`.

- [ ] **Step 3: Push the work branch**

```bash
git push -u origin 2026-10-21-evaboot-labs-repo-standard
```

- [ ] **Step 4: The README renders in both themes (spec Verification 5)**

With `browser-screen-control`, open `https://github.com/evaboot-labs/infinite-leads-system/blob/2026-10-21-evaboot-labs-repo-standard/README.md`. Screenshot the full page with GitHub's theme set to light, then to dark (Settings → Appearance, or the `prefers-color-scheme` emulation the skill offers). In each, every image must render: the banner, the demo GIF, the three screenshots, the signals figure and the four badges, with no broken-image icon or alt text in their place, and the dark screenshot must show `banner-dark.png` and `signals-dark.png`. Save both screenshots to `/tmp/ils-readme-light.png` and `/tmp/ils-readme-dark.png`.

- [ ] **Step 5: The plugin installs from the pushed branch (spec Verification 2 and 3)**

```bash
T=$(mktemp -d) && git clone -q --branch 2026-10-21-evaboot-labs-repo-standard https://github.com/evaboot-labs/infinite-leads-system "$T/repo" && cd "$T/repo" \
  && claude plugin validate .claude-plugin/marketplace.json && claude plugin validate . && cd -
```

Expected: both validations pass. Then, with `use-interactive-terminal`, start a fresh `claude` session in `$T/repo` with `CLAUDE_CONFIG_DIR` set to a new temp dir (log in if it asks; JB types any credential). Run `/plugin marketplace add ./`, then `/plugin install infinite-leads-system@evaboot-labs-infinite-leads-system`, then `/plugin`. Expected: both succeed and `/plugin` lists `infinite-leads-system` with the skill `evaboot-infinite-leads-system`. Copy the three outputs for the PR description.

- [ ] **Step 6: An agent sets up from the prompt alone (spec Verification 6)**

With `use-interactive-terminal`, in a new empty temp folder, start a fresh `claude` session (no plugin installed, JB's normal config). Paste the README's "Set it up in one prompt" text, with one line added at the end: `Use the branch 2026-10-21-evaboot-labs-repo-standard when you clone.` Answer its questions with the same ICP as the demo (VP of Sales, software, 51-200, Luxembourg, Changed jobs). Stop the session at its first confirmation question, before any call that saves a search, list, recurring export or destination: answer "no, stop here". Expected: the transcript shows it read `AGENTS.md` and `skills/evaboot-infinite-leads-system/SKILL.md`, and no write call ran. Save the transcript to `/tmp/ils-prompt-only.txt`. If the agent writes anything before asking, that is a failure: undo the write as in Task 5 Step 11 and fix AGENTS.md or the skill.

- [ ] **Step 7: Write the PR description**

Write `$(git rev-parse --git-dir)/pr-body.md` (inside `.git`, so it is never committed). It contains:
1. One paragraph: what changed and why (the repo standard, P1 of three; P2 and P3 follow after merge).
2. **The repo standard checklist**, every item ticked `- [x]` with a one-line proof, one item per line of the spec's "File layout", "README section order", "AGENTS.md" and "Copy rules" sections. Items that do not apply say so in the line and are still ticked (for example the repo has `.mcp.json`, so that item applies). Note the two additions: `docs/connect-your-agent.md` and `.github/assets/src/`.
3. **Verification results:** spec items 2, 3, 5, 6, 7 and 10, each with its command output or a pasted excerpt (the `/plugin` listing, the prompt-only transcript excerpt showing AGENTS.md and the skill being read and the stop at the first confirmation, the `CLEAN` line). Attach the two README screenshots and the saved-searches "after" screenshot by dragging them into the PR on github.com after it opens (with `browser-screen-control` + `bb_upload`).
4. **For JB:** spec item 4, verbatim: "Run `npx skills add . --list` in a clone of this branch (or `npx skills add https://github.com/evaboot-labs/infinite-leads-system/tree/2026-10-21-evaboot-labs-repo-standard --list`) and check it lists `evaboot-infinite-leads-system`." Plus: "After the merge, the social preview is set from `banner-light.png` (see the plan's Rollout)."

- [ ] **Step 8: Strip the internal spec and plan from the branch**

These two files exist only so `executing-plans` could run. They must not reach the public template.

```bash
git rm -q docs/specs/2026-10-21-evaboot-labs-repo-standard-design.md docs/plans/2026-10-21-evaboot-labs-repo-standard.md
git commit -m "Remove the internal spec and plan from the branch"
git ls-tree -r --name-only HEAD docs/ ; git push
```

Expected: `git ls-tree` lists exactly the five pages from Task 1 and nothing under `docs/specs/` or `docs/plans/`. The task ledger was built at the start of the run and does not need the plan file in the tree; the plan is still on the main checkout's local `main` and in `evaboot-website-v2/docs/plans/`.

- [ ] **Step 9: Hand over to test-worktree-and-merge**

Open the PR as a **draft**, with the body from Step 7: `gh pr create --draft --title "Bring the repo to the evaboot-labs standard" --body-file "$(git rev-parse --git-dir)/pr-body.md"`. If `test-worktree-and-merge` opens the PR itself, make sure it is a draft and run `gh pr edit <number> --body-file "$(git rev-parse --git-dir)/pr-body.md"`. Merging waits for JB.

---

## Acceptance

Spec Verification 11 and 12 belong to P2 (the skill) and are not graded here. Item 1 for this repo is the ticked checklist in the PR description, as the spec says. `ils-plugin-install` writes its throwaway Claude config under `$E2E_RUN_DIR`; outside the unattended driver, set `E2E_RUN_DIR` to a temp folder first. `ils-npx-skills` is the one item JB runs (agents do not install npm packages); the driver may run it when grading.

```json
{"items": [
  {"id": "ils-standard-checklist", "text": "The repo meets the standard: the merged PR description carries the repo standard checklist, every item ticked", "when": "merge",
   "check": {"type": "command", "run": "body=$(gh pr list --repo evaboot-labs/infinite-leads-system --state merged --head 2026-10-21-evaboot-labs-repo-standard --json body --jq '.[0].body') && echo \"$body\" | grep -q -- '- \\[x\\]' && ! echo \"$body\" | grep -q -- '- \\[ \\]'", "timeout": 60}},
  {"id": "ils-plugin-validate", "text": "The plugin manifest is valid", "when": "merge",
   "check": {"type": "command", "run": "claude plugin validate .claude-plugin/marketplace.json && claude plugin validate .", "timeout": 120}},
  {"id": "ils-plugin-install", "text": "The plugin install works in Claude Code and lists the skill", "when": "merge",
   "check": {"type": "command", "run": "C=\"$E2E_RUN_DIR/claude-config\" && mkdir -p \"$C\" && CLAUDE_CONFIG_DIR=\"$C\" claude plugin marketplace add ./ && CLAUDE_CONFIG_DIR=\"$C\" claude plugin install infinite-leads-system@evaboot-labs-infinite-leads-system && CLAUDE_CONFIG_DIR=\"$C\" claude plugin details infinite-leads-system@evaboot-labs-infinite-leads-system | grep -q evaboot-infinite-leads-system", "timeout": 300}},
  {"id": "ils-npx-skills", "text": "npx skills finds the skill", "when": "merge",
   "check": {"type": "command", "run": "npx --yes skills add evaboot-labs/infinite-leads-system --list | grep -q evaboot-infinite-leads-system", "timeout": 300}},
  {"id": "ils-readme-images", "text": "Every README image resolves to a file, and the banner and figure have dark versions", "when": "merge",
   "check": {"type": "command", "run": "python3 -c \"import os,re,sys;t=open('README.md').read();p=[a or b for a,b in re.findall(r'(?:src|srcset)=\\\"([^\\\"]+)\\\"|\\]\\(([^)#\\s]+)\\)',t)];bad=[x for x in p if not x.startswith(('http','mailto:')) and not os.path.exists(x)];print(bad);sys.exit(1 if bad or t.count('prefers-color-scheme: dark')<2 else 0)\"", "timeout": 60}},
  {"id": "ils-prompt-only-setup", "text": "An agent can set up from the prompt alone", "when": "merge",
   "check": {"type": "jev", "question": "Does this pull request description show a fresh agent session, given only the README prompt, that read AGENTS.md and the evaboot-infinite-leads-system skill and stopped at its first confirmation question before any write call?",
             "evidence": "gh pr list --repo evaboot-labs/infinite-leads-system --state merged --head 2026-10-21-evaboot-labs-repo-standard --json body --jq '.[0].body'",
             "why_not_command": "whether a transcript excerpt shows the agent reading the right files and stopping before writing is a judgment on prose, not an exit code", "timeout": 120}},
  {"id": "ils-sizes", "text": "Sizes are within limits", "when": "merge",
   "check": {"type": "command", "run": "[ \"$(wc -c < README.md)\" -lt 5120 ] && [ \"$(wc -l < AGENTS.md)\" -lt 60 ] && [ \"$(wc -c < .github/assets/demo.gif)\" -lt 5242880 ] && [ \"$(wc -c < .github/assets/banner-light.png)\" -lt 1048576 ]", "timeout": 30}},
  {"id": "ils-demo-cleaned", "text": "The demo left nothing running", "when": "merge",
   "check": {"type": "command", "run": "out=$(python3 infinite_leads.py check) && echo \"$out\" | grep -q 'API key      OK' && ! echo \"$out\" | grep -qi 'Infinite Leads demo'", "timeout": 120}},
  {"id": "ils-github-settings", "text": "The GitHub settings are set", "when": "deploy",
   "check": {"type": "command", "run": "gh api repos/evaboot-labs/infinite-leads-system --jq 'select(.description != null and .description != \"\" and .homepage != null and .homepage != \"\" and .topics[2] != null and .license.spdx_id == \"MIT\") | .name' | grep -qx infinite-leads-system", "timeout": 60}},
  {"id": "ils-social-preview", "text": "The social preview shows the banner", "when": "deploy",
   "check": {"type": "command", "run": "curl -s https://github.com/evaboot-labs/infinite-leads-system | grep -o 'og:image\" content=\"[^\"]*' | grep -q repository-images.githubusercontent.com", "timeout": 60}}
]}
```

## Rollout

Nothing deploys on evaboot.com. The "deploy" for this repo is two post-merge steps on GitHub.

1. **JB reviews the draft PR** on github.com (rendered README, light and dark), runs the `npx skills` line from the PR description, and merges. Nothing merges without JB's go-ahead.
2. **Capture the settings before changing anything** (for rollback):

```bash
gh api repos/evaboot-labs/infinite-leads-system --jq '{description,homepage,topics,is_template,license:.license.spdx_id}' > /tmp/ils-settings-before.json
```

3. **Settings** are already complete (Context). Confirm with the `ils-github-settings` command; change nothing if it passes.
4. **Social preview:** GitHub has no API for it. With `browser-screen-control`, open `https://github.com/evaboot-labs/infinite-leads-system/settings`, find **Social preview**, click **Edit → Upload an image…**, and upload `.github/assets/banner-light.png` from the merged `main` (use `bb_upload`; use `desktop-control` if the file picker is native). Then run the `ils-social-preview` command. GitHub caches the page, so if it still shows `opengraph.githubassets.com`, retry with `curl -s "https://github.com/evaboot-labs/infinite-leads-system?cb=$(date +%s)"`.
5. **Local `main` in the main checkout** still holds the unpushed commit that added the spec and plan (the branch stripped them, so the squash-merge does not absorb it). After the merge, in `~/.superset/projects/Infinite-Leads-System`:

```bash
git fetch origin
git log --oneline origin/main..main
```

   Expected: exactly one line, `docs: add spec and plan for the evaboot-labs repo standard`. If so, drop it without touching the working tree's other files: `git rebase --onto origin/main main~1 main`. If the log shows anything else, stop and investigate; do not reset.
6. **Then write P2:** run `/writing-plans` for the `evaboot-labs-repo` skill from the merged result, in `~/agent-setup`.

**Rollback:**
- Revert the PR: `gh pr view <number> --repo evaboot-labs/infinite-leads-system --json mergeCommit --jq .mergeCommit.oid`, then open a revert PR from the GitHub UI or `git revert <oid>` on a branch and open it as a draft.
- Social preview: GitHub settings → Social preview → **Remove**.
- Settings: `gh api -X PATCH repos/evaboot-labs/infinite-leads-system -f description="…" -f homepage="…"` with the values in `/tmp/ils-settings-before.json` (none are expected to change).
