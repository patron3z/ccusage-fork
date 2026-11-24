---
name: token-usage
description: Show how many tokens and how much estimated cost each task (session), day or month used, for Claude Code, Codex, OpenCode and other coding agents, using ccusage. Use when the user asks about token usage, cost per task, or which conversation used the most.
---

# Token usage per task (ccusage)

[ccusage](https://github.com/ccusage/ccusage) reads the log files the agent already keeps on this computer. Nothing is uploaded. Costs are estimates at API prices, not what a subscription plan charges.

## Run

Install once (Node.js required), or use `npx ccusage` with no install:

```bash
npm install -g ccusage
ccusage telemetry disable   # optional: turn off the small anonymous usage ping
```

| Agent | Command | Where it reads (default) |
|---|---|---|
| Claude Code | `ccusage session` | `~/.claude/projects` |
| Codex | `ccusage codex session` | `${CODEX_HOME:-~/.codex}` |
| OpenCode | `ccusage opencode session` | `${OPENCODE_DATA_DIR:-${XDG_DATA_HOME:-~/.local/share}/opencode}` |
| All detected agents | `ccusage session` | all of the above |

Swap `session` for `daily`, `weekly`, `monthly` or `blocks` (5-hour windows). Add `--json` for machine-readable output.

Run `ccusage codex --help` or `ccusage opencode --help` to confirm what the installed version supports. If a report is empty, the agent has no logs in the default folder: set `CODEX_HOME` or `OPENCODE_DATA_DIR` to the real one.

## Name the tasks (Claude Code only)

`ccusage session` shows session ids. To turn them into titles and first messages:

```bash
python skills/token-usage/scripts/session_titles.py --top 10
```

It runs `ccusage session --json` and matches each id to the transcript in `~/.claude/projects`. It only reads local files.

## Report

Give the user: total tokens and estimated cost, the top sessions with their titles, and a plain note that most tokens in long conversations are cache reads of the growing context. Do not call the cost a bill.
