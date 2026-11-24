# ai-token-usage (fork of ccusage)

This is a fork of [ccusage/ccusage](https://github.com/ccusage/ccusage) (MIT, by ryoppippi and contributors). The tool itself is unchanged. All credit for it goes to its authors; see `LICENSE`.

What this fork adds: an Agent Skill, `skills/token-usage/`, so Claude Code, Codex and OpenCode can answer "how many tokens did each task use?" by running ccusage.

ccusage already reads Claude Code, Codex (`ccusage codex ...`) and OpenCode (`ccusage opencode ...`) logs. The skill only tells the agent which command to run and adds a small script that names Claude Code sessions.

## Install the skill

| Agent | Copy `skills/token-usage/` to |
|---|---|
| Claude Code | `~/.claude/skills/token-usage` |
| Codex | `~/.agents/skills/token-usage` |
| OpenCode | `~/.config/opencode/skills/token-usage` |

Status: tested with Claude Code on Windows. Not yet run inside Codex or OpenCode (neither is installed on the author's PC), so those two folders and commands come from ccusage's own docs.

## Staying up to date

```bash
git fetch upstream && git merge upstream/main
```
