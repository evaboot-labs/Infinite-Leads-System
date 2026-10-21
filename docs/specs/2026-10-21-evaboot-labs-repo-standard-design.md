# Evaboot Labs repo standard: visual READMEs, agent-ready layout, and a global skill

## Goal

Make every public `evaboot-labs` repository easy for two readers:

- **Humans** land on a visual, marketing-led README. They should understand in a few seconds what the repo does, see it work, and copy one prompt.
- **AI agents** (Claude Code, Codex, Cursor) find one short `AGENTS.md`, one skill per job, and a short install (two commands in Claude Code, one with `npx skills`). They never need to read the README.

The work runs in this order:

1. Bring `infinite-leads-system` to the standard by hand. JB checks it.
2. Turn the approved result into a global skill, `evaboot-labs-repo`.
3. Use the skill to bring the other four repos to the standard.

## Background

All of this was checked on 2026-10-21.

- `evaboot-labs` has five public repos: `infinite-leads-system`, `no-code-lead-generation`, `ai-sales-follow-up`, `openai-decisions-vs-jev`, `ai-driven-lead-scoring`.
- **None of the five READMEs contains an image.** The Infinite Leads README is 11 KB of text, and its only visual is an ASCII diagram.
- **Only `infinite-leads-system` has its GitHub settings filled in:** topics, a homepage, MIT license and template mode. The other four have no topics, no homepage and no LICENSE. `ai-driven-lead-scoring` also has no description.
- **Infinite Leads already follows the skill layout.** Its skill is in `skills/evaboot-infinite-leads-system/`, linked from `.claude/skills` and `.agents/skills`. It has `.mcp.json` and a short `AGENTS.md` (1.6 KB).
- **The other skills sit in the wrong folder.** `ai-sales-follow-up`, `openai-decisions-vs-jev` and `ai-driven-lead-scoring` keep their skill under `.claude/skills/<name>/`, which Codex does not read.
- **`no-code-lead-generation` has no AGENTS.md and no skill.**
- **No repo can be installed as a plugin**, because none has `.claude-plugin/marketplace.json`.

### What the research found

Sources: web, X and Reddit, 2026-10-21.

- **One root `AGENTS.md` serves every major agent.** Claude Code reads it from v2.1.277 when no `CLAUDE.md` is present. Keep it short and point to other files rather than copying them in.
- **Skills follow the agentskills.io spec:** `skills/<name>/SKILL.md` with `name` and `description` frontmatter, a body under 500 lines, and detail in `references/`.
- **The most-starred skill repos put a one-line install near the top:**
  - `/plugin marketplace add owner/repo` (Claude Code)
  - `npx skills add owner/repo` (Codex, Cursor and others)

  Examples: obra/superpowers, addyosmani/agent-skills, coreyhaines31/marketingskills.
- **The README is for humans:** what it does, who it is for, how to start. Visuals beat explanations of the technology.
- **Image rules:**
  - Use relative paths under `.github/assets/`.
  - Use `<picture>` for the light and dark versions.
  - The social preview is 1280×640 and under 1 MB.

## Decisions

- **The skill is personal and global** (JB, 2026-10-21). It lives in `~/agent-setup/skills/evaboot-labs-repo/`, so every project can use it, including evaboot-website and evaboot_seo. It is not copied into either project repo.
- **Screenshots are real captures from JB's Chrome, not blurred** (JB, 2026-10-21). They focus on Sales Navigator and Evaboot.
- **Outreach is always "any outreach tool", with lemlist as the example.** The copy never presents lemlist as the only option.
- **The banner is the Blueprint flow approved in the visual companion** (`.superpowers/brainstorm/80259-1792583240/content/hero-banner-v3.html`). It has:
  - a mono eyebrow `evaboot-labs · <repo>`
  - a one-line headline and a subline
  - four numbered nodes joined by dashed arrows, the last one filled in brand purple
  - a spec line at the bottom
- **The README order is the one approved in the visual companion** (`readme-layout.html`). It is listed in full under "README section order".
- **The demo GIF records a real run** with a narrow search. The recurring exports and saved searches it creates are deleted afterwards.
- **Approach O1:** do Infinite Leads by hand, write the skill from the approved result, then use the skill on the other four repos. Those four runs test the skill.

## The repo standard

### File layout

```
README.md                         humans (section order below), under 5 KB
AGENTS.md                         agents' entry point, under 60 lines, never repeats the README
skills/<skill-name>/SKILL.md      agentskills.io frontmatter; detail in skills/<skill-name>/references/
.claude/skills -> ../skills       symlink
.agents/skills -> ../skills       symlink
.claude-plugin/marketplace.json   marketplace named evaboot-labs-<repo>, one plugin entry named <repo>
.claude-plugin/plugin.json        the plugin: points at skills/ and, when the repo uses one, the MCP config
.mcp.json                         only in repos that call an MCP server
docs/*.md                         setup detail moved out of the README (Make, n8n, by hand, company signals, …)
.github/assets/banner-light.png   1280×640
.github/assets/banner-dark.png    1280×640
.github/assets/demo.gif           about 20 s, under 5 MB; the full-length MP4 sits beside it and is linked under the GIF
.github/assets/screenshots/*.png  1600 px wide, cropped to the relevant panel
LICENSE                           MIT
```

### README section order

A repo may skip a section that does not apply. No repo adds a new section.

1. **The banner** in `<picture>`: the dark version for `prefers-color-scheme: dark`, the light version as the fallback. Then the H1 title, a one-line pitch, and badges: works with Claude Code · Codex · Cursor; MCP server, when used; MIT; "use this template", when it is a template.
2. **The demo GIF**, linking to the full MP4.
3. **"Set it up in one prompt":**
   - the paste-this prompt, in a fenced code block
   - a `<details>` block with the Claude Code install, two commands: `/plugin marketplace add evaboot-labs/<repo>` then `/plugin install <repo>@evaboot-labs-<repo>`; and `npx skills add evaboot-labs/<repo>` for Codex, Cursor and others
4. **"How it works":** three screenshots, each with a numbered one-line caption.
5. **A drawn figure for the repo's main idea**, in the banner's style. For Infinite Leads this is "Four signals, four campaigns", one card per signal with its one-line opener.
6. **"What you need"**, with the cost in the same list.
7. **"Go further":** a table linking each `docs/*.md` page.
8. **A footer:** "Agents: start at AGENTS.md", "Built by Evaboot" with a link, a link to github.com/evaboot-labs, and the license.

### AGENTS.md

- Starts with one paragraph on what the repo does.
- Then a numbered procedure that sends the agent to the skill.
- Then the safety rules: confirm before writes, never handle third-party API keys, never commit `.env`.
- Points to other files rather than repeating them.

### GitHub settings

- Description, homepage (the matching evaboot.com page, or omitted when none exists), topics, MIT license.
- The social preview set to `banner-light.png`.
- Template mode where the user is meant to copy the repo and fill in their own config: `infinite-leads-system` and `no-code-lead-generation`.

### Copy rules

Each rule lives once, in the skill's `references/standard.md`:

- Repo names are lowercase.
- Product links go to `dash.evaboot.com` only, never `app.evaboot.com`.
- Say "AI Agent", never "AI Assistant".
- Outreach is "any outreach tool", with lemlist as the example.
- No claim of a free trial.

## Images

- **Banner:** the skill ships `assets/banner.html`, a parameterized version of the approved mockup. Its inputs are the eyebrow, headline, subline, four nodes (step label, title, caption) and the spec line, plus a `theme=light|dark` switch. `assets/render-banner.mjs` loads it in headless Chrome (`/Applications/Google Chrome.app`, `--headless=new`, 1280×640) and writes both PNGs. The light PNG must be under 1 MB. If it is not, the script re-encodes it with `ffmpeg` (already installed) and fails if it still is not.
- **Drawn figures** (such as the signal cards) use the same template system and the same renderer.
- **Screenshots** are captured with the `browser-screen-control` skill in JB's signed-in Chrome profile, cropped to the panel and resized to 1600 px wide with `sips`. They are not blurred.
- **Demo GIF:**
  - Recorded from a real agent session in the agent terminal (`use-interactive-terminal`) with `ffmpeg` screen capture.
  - Waits are sped up to keep it about 20 s, and it is converted with `ffmpeg` palettegen. The GIF must be under 5 MB, and the full MP4 is kept beside it.
  - For Infinite Leads: one narrow search (a few leads), one recurring export, then the `check` table.
  - When the recording ends, successful or not, delete the recurring export and the saved search the run created, before the PR opens. No credits are spent past the recording.

## The skill: `evaboot-labs-repo`

**Location:** `~/agent-setup/skills/evaboot-labs-repo/`, exposed at `~/.agents/skills/` by `bin/install.py --apply`. A line is added to `~/agent-setup/skills/SKILL_INDEX.md`.

**Trigger:** creating a new evaboot-labs repo (for example the companion repo of a blog article), or auditing or upgrading an existing one.

```
SKILL.md                    the procedure, under 300 lines
references/standard.md      the file layout, README order, AGENTS.md shape, GitHub settings, copy rules
references/assets.md        banner rendering, screenshot capture, demo recording, size limits
assets/banner.html          the parameterized Blueprint banner and figure template
assets/render-banner.mjs    headless Chrome renderer
assets/README.template.md
assets/AGENTS.template.md
assets/marketplace.template.json
assets/plugin.template.json
scripts/audit.sh            checks a repo against the standard; exit 0 = pass
```

**Procedure:**

1. **Audit** with `scripts/audit.sh <repo-dir>`.
2. **Plan** which README sections and docs pages apply.
3. **Build** the files.
4. **Produce** the images.
5. **Validate** (see Verification).
6. **Open a draft PR.** Merging stays with JB.
7. **After the merge,** set the GitHub settings and the social preview.

**`audit.sh` checks:**

- the required files are present
- `.claude/skills` and `.agents/skills` are symlinks to `../skills`
- every `SKILL.md` has `name` matching its folder, and a `description`
- the README is under 5 KB, and AGENTS.md is under 60 lines
- every relative image and link in the README resolves to a file
- the README links no `app.evaboot.com`
- with `--remote`: topics, homepage and license are set on GitHub

## Per-repo notes

- **`infinite-leads-system`** (done by hand):
  - The README's Make, n8n, by-hand, company-signals and commands sections move to `docs/make.md`, `docs/n8n.md`, `docs/manual-setup.md` and `docs/company-signals.md`.
  - The commands table goes into `docs/company-signals.md`, since `refresh` is the only command beyond `check` and `lead-url`.
  - Change the skill's "Through Make" and "Through n8n" references from README.md sections to the new docs pages.
  - Add `.claude-plugin/`. The plugin bundles the skill and the Evaboot MCP config.
- **`no-code-lead-generation`:** new AGENTS.md, plus a skill that sets up the n8n or Make template. Add LICENSE, topics and template mode.
- **`ai-driven-lead-scoring`:** move `.claude/skills/score-leads/` to `skills/score-leads/` and add the two symlinks. Add a description, LICENSE and topics.
- **`ai-sales-follow-up`:** move `.claude/skills/follow-up/` to `skills/follow-up/` and add the two symlinks. Add LICENSE and topics.
- **`openai-decisions-vs-jev`:** move `.claude/skills/compare-models/` to `skills/compare-models/` and add the two symlinks. Add LICENSE and topics.
  - Its demo GIF shows the benchmark running, with its `results.csv` summary.
  - "How it works" shows the results chart in place of product screenshots.

## File Inventory

- `evaboot-labs/infinite-leads-system/README.md` — rewritten to the section order; setup detail moves out. Linked from `AGENTS.md:5` and from the skill.
- `evaboot-labs/infinite-leads-system/AGENTS.md` — step 5 points to `docs/make.md` and `docs/n8n.md` instead of README sections.
- `evaboot-labs/infinite-leads-system/skills/evaboot-infinite-leads-system/SKILL.md` — "Through Make" and "Through n8n" references change from README.md to `docs/*.md`.
- `evaboot-labs/infinite-leads-system/.mcp.json` — unchanged; referenced by the new `.claude-plugin/plugin.json`.
- `evaboot-labs/no-code-lead-generation/README.md` — rewritten. New: `AGENTS.md`, `skills/`, `LICENSE`.
- `evaboot-labs/ai-driven-lead-scoring/README.md`, `AGENTS.md`, `.claude/skills/score-leads/SKILL.md` — README rewritten; the skill moves to `skills/score-leads/`; AGENTS.md path updated.
- `evaboot-labs/ai-sales-follow-up/README.md`, `AGENTS.md`, `.claude/skills/follow-up/SKILL.md` — same treatment.
- `evaboot-labs/openai-decisions-vs-jev/README.md`, `AGENTS.md`, `.claude/skills/compare-models/SKILL.md` — same treatment.
- `~/agent-setup/skills/SKILL_INDEX.md` — one line for `evaboot-labs-repo`.
- New: `~/agent-setup/skills/evaboot-labs-repo/` (every file listed under "The skill").

The local checkout of Infinite Leads is `~/.superset/projects/Infinite-Leads-System` (remote `evaboot-labs/infinite-leads-system`, on `main`, clean on 2026-10-21). The other four have no local checkout; the work clones them.

## Verification

Per repo, before its PR leaves draft:

1. [merge] **The repo meets the standard.** Check: for the four skill-driven repos, `~/.agents/skills/evaboot-labs-repo/scripts/audit.sh <repo-dir>` exits 0. For `infinite-leads-system`, which is built before the skill exists, the PR description carries the "The repo standard" checklist ticked item by item; `audit.sh` runs on it later under check 11.
2. [merge] **The plugin manifest is valid.** Check: `claude plugin validate .` in the repo exits 0.
3. [merge] **The plugin install works in Claude Code.** Check: in a fresh Claude Code session in a clone of the PR branch, `/plugin marketplace add ./` then `/plugin install <repo>@evaboot-labs-<repo>` succeed, and `/plugin` lists the skill.
4. [merge] **`npx skills` finds the skill on the PR branch.** Check: JB runs `npx skills add . --list` from a clone checked out on the PR branch (agents do not install npm packages), and the output lists the skill name. If the CLI rejects a local path, JB runs it against the branch URL `https://github.com/evaboot-labs/<repo>/tree/<pr-branch>` instead.
5. [merge] **Every README image renders, in both themes.** Check: screenshot the PR branch's README on github.com in light and dark mode with `browser-screen-control`. Jev — "Does every image in this screenshot render (no broken-image icon or alt text shown in place of an image)?"
6. [merge] **An agent can set up from the prompt alone.** Check: a fresh agent session in a fresh clone, given only the README's paste-this prompt, reaches its first confirmation question (before any write call). The transcript shows it read `AGENTS.md` and the skill.
7. [merge] **Sizes are within limits.** Check: `wc -c README.md` < 5120; `wc -l AGENTS.md` < 60; `.github/assets/demo.gif` < 5 MB; `banner-light.png` < 1 MB.
8. [deploy] **The GitHub settings are set.** Check: `gh api repos/evaboot-labs/<repo> --jq '[.description,.homepage,(.topics|length),.license.spdx_id]'` shows a description, a homepage where one exists, at least three topics, and `MIT`.
9. [deploy] **The social preview shows the banner.** Check: `curl -s https://github.com/evaboot-labs/<repo> | grep -o 'og:image" content="[^"]*'` returns a `repository-images.githubusercontent.com` URL (a custom preview), not `opengraph.githubassets.com`.
10. [merge] **The demo left nothing running.** Infinite Leads only, checked before the PR opens. Check: `python3 infinite_leads.py check` lists no recurring export created for the recording, and a `browser-screen-control` screenshot of Sales Navigator's saved searches shows no search created for it.

For the skill:

11. [merge] **The skill reproduces the standard.** Check: after the four skill-driven runs, `audit.sh` passes on all five repos, and any patch the runs needed is committed in `~/agent-setup` before the next repo starts.
12. [merge] **The skill is visible to every client.** Check: `ls ~/.agents/skills/evaboot-labs-repo/SKILL.md` succeeds after `bin/install.py --apply`, and `SKILL_INDEX.md` lists the skill.

## Rollout

- **Nothing deploys on evaboot.com.** All changes are in the five `evaboot-labs` repos and `jbjzq/agent-setup`. This spec lives in evaboot-website because the work started here.
- **Order:**
  1. `infinite-leads-system` draft PR. JB reviews the rendered README and merges.
  2. Set its GitHub settings and social preview. The demo's recurring export and saved search were already removed when the recording ended.
  3. Commit the skill to `jbjzq/agent-setup` and run `bin/install.py --apply`.
  4. One draft PR per repo, in this order: `no-code-lead-generation`, `ai-driven-lead-scoring`, `ai-sales-follow-up`, `openai-decisions-vs-jev`. JB merges each, then the settings are applied.
- **Env vars and secrets:** none new. The demo run uses JB's existing `EVABOOT_API_KEY`.
- **Post-deploy:** steps 8–10 of Verification, per repo.
- **Rollback:**
  - Revert the repo's PR.
  - Restore settings with `gh api -X PATCH repos/evaboot-labs/<repo>` from the values captured before the change.
  - Remove the skill folder and run `bin/install.py --apply`.
