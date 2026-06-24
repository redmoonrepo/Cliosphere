---
name: updating-backlog
description: Reads and writes state/BACKLOG.md and runtime/tasks/tasks.json in sync. Use when marking a backlog item done, promoting an item to ready, checking what is newly unblocked after a task completes, or adding a new backlog entry. Runs update_tasks_json.py for machine-readable DAG updates.
---

# Updating Backlog

Keeps `state/BACKLOG.md` (human-readable) and `runtime/tasks/tasks.json` (machine-readable DAG) in sync.

## When to use

- Marking a backlog item done after a task completes
- Adding a new backlog item
- Checking what is newly unblocked after a completion
- Promoting an item from `draft` → `ready`

## Human layer: BACKLOG.md

Edit `state/BACKLOG.md` directly for:
- Adding new items (assign next sequential ID)
- Moving items to ✅ Done
- Updating descriptions, dependencies, notes

Always update the `Last updated:` date at the top.

## Machine layer: tasks.json

**Add a task** (dependencies are coordinator knowledge — pass them explicitly):
```bash
# No dependencies
python platforms/claude_desktop/skills/scripts/update_tasks_json.py \
  --action add \
  --task-id 20260610-027-test-invoke-agent

# With dependencies
python platforms/claude_desktop/skills/scripts/update_tasks_json.py \
  --action add \
  --task-id 20260610-002-github-push \
  --depends-on "20260610-016-claude-code-setup,20260610-024-agent-trigger" \
  --unblocks ""
```

**Mark complete** (cascades to unblocked downstream items automatically):
```bash
python platforms/claude_desktop/skills/scripts/update_tasks_json.py \
  --action complete \
  --task-id 20260610-027-test-invoke-agent
```

**Check status:**
```bash
python platforms/claude_desktop/skills/scripts/update_tasks_json.py --action status
```

**Override status manually:**
```bash
python platforms/claude_desktop/skills/scripts/update_tasks_json.py \
  --action set-status \
  --task-id 20260610-027-test-invoke-agent \
  --status dispatched
```

## Dependency cascade (the agentic Jira)

When a task is marked `complete`, `update_tasks_json.py`:
1. Marks the task complete with today's date
2. Scans all `blocked` tasks for any that listed this task in `depends_on`
3. For each: checks whether ALL its `depends_on` entries are now complete
4. If satisfied → promotes status `blocked` → `ready`
5. Prints "Newly unblocked: [list]"

The orchestrator cron (once built, #36) picks up newly `ready` items automatically.

## tasks.json entry format

```json
{
  "id": "20260610-027-test-invoke-agent",
  "backlog_ref": "#27",
  "slug": "test-invoke-agent",
  "status": "ready",
  "agent": "clio-antigravity",
  "created": "2026-06-10",
  "depends_on": [],
  "unblocks": ["20260610-002-github-push"],
  "spec_dir": "runtime/tasks/20260610-027-test-invoke-agent"
}
```

Status values: `draft` → `ready` → `dispatched` → `complete` | `failed` | `blocked`

## See also

- [creating-tasks.md](creating-tasks.md) — scaffold a new spec directory
- [dispatching-agents.md](dispatching-agents.md) — send a ready task to an agent
