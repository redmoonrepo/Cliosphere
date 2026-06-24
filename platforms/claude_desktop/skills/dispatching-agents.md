---
name: dispatching-agents
description: Sends a ready SDD task to the appropriate agent via agent_trigger.sh. Use when a spec directory exists with status ready and you want to dispatch it to clio-antigravity, clio-codex, or clio-code. Validates pre-flight conditions before firing.
---

# Dispatching Agents

Validates and fires `infra/scripts/agent_trigger.sh` for a ready task.

## When to use

- A spec is complete (requirements.md + tasks.md filled, status = `ready`)
- You want to dispatch headlessly without Claude Desktop

## Quick dispatch

```bash
bash infra/scripts/agent_trigger.sh 20260608-027-test-invoke-agent
```

## Pre-flight checklist (run before dispatching)

```bash
python platforms/claude_desktop/skills/scripts/preflight_check.py \
  --task-id 20260608-027-test-invoke-agent
```

Checks:
- [ ] Task directory exists at `runtime/tasks/<task-id>/`
- [ ] `requirements.md` exists and status is `ready` (not `draft`)
- [ ] `tasks.md` exists
- [ ] No `[task-name]` placeholders remain in either file
- [ ] `jq` is installed
- [ ] `agy` is in PATH (for clio-antigravity tasks)
- [ ] `codex` is in PATH (for clio-codex tasks)

Exit 0 = safe to dispatch. Any failure prints the specific blocker.

## Agent routing

| Agent | Command | Use for |
|-------|---------|---------|
| `clio-antigravity` | `agy -p` | Verification, analysis, Drive ops, cross-check |
| `clio-codex` | `codex exec` | Implementation, code tasks, file writes |
| `clio-code` | `claude` (Claude Code) | Complex implementation, repo-wide tasks |

The agent is set in `requirements.md` → `## Agent` field. `agent_trigger.sh` reads it automatically.

## After dispatch

- `tasks.json` status → `dispatched` (agent_trigger.sh stamps this)
- Watch for `runtime/tasks/<task-id>/review.md` to appear
- On completion: run `update_tasks_json.py --action complete` to cascade

## Verify agy headless flag

Before first dispatch to clio-antigravity:
```bash
agy --help | grep -i "\-p\|headless\|prompt"
```
Confirm the flag syntax. If `-p` is not listed, update `agent_trigger.sh` accordingly.

## See also

- [creating-tasks.md](creating-tasks.md) — scaffold spec directory first
- [updating-backlog.md](updating-backlog.md) — mark complete and cascade after
