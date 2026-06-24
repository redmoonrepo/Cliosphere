---
name: creating-tasks
description: Scaffolds a new SDD task directory at runtime/tasks/YYYYMMDD-<backlog_id>-<slug>/ from canonical templates. Use when creating a new spec for the SDD pipeline, when a backlog item is ready to be dispatched, or when Claude is rate-limited and another agent needs to unblock work. Runs create_task.py — does not require Claude to be online.
---

# Creating Tasks

Scaffolds a new spec directory from the canonical templates in `runtime/tasks/_templates/`.

## When to use

- A backlog item is ready to enter the SDD pipeline
- Claude Desktop is rate-limited and work must continue
- Any agent needs to create a dispatchable spec

## Quick start

```bash
python platforms/claude_desktop/skills/scripts/create_task.py \
  --id 027 \
  --slug test-invoke-agent \
  --agent clio-antigravity
```

This creates:
```
runtime/tasks/20260608-027-test-invoke-agent/
├── requirements.md   ← status: draft, placeholders substituted
├── design.md
├── tasks.md
└── (review.md written by implementing agent on completion)
```

## Naming convention

`YYYYMMDD-<backlog_id>-<slug>`

- `YYYYMMDD` — date task was created (today)
- `backlog_id` — zero-padded 3-digit backlog item number (e.g. `027`). Use `000` for ad-hoc tasks with no backlog entry.
- `slug` — lowercase, hyphens only, descriptive (e.g. `test-invoke-agent`, `github-push`)

## After scaffolding

1. Open `requirements.md` — fill every section. No placeholders, no TBDs.
2. Open `design.md` — fill approach and file ownership before any code is written.
3. Open `tasks.md` — fill phased task list.
4. Set status to `ready` in `requirements.md` when all three are complete.
5. Dispatch: `bash infra/scripts/agent_trigger.sh 20260608-027-test-invoke-agent`

## What the script does NOT do

- Does not fill in spec content — that is the coordinator's job
- Does not update `tasks.json` or `BACKLOG.md` — see [updating-backlog.md](updating-backlog.md)
- Does not dispatch the task — see [dispatching-agents.md](dispatching-agents.md)

## Error handling

| Exit code | Meaning |
|-----------|---------|
| 0 | Success — directory created |
| 1 | Task directory already exists (will not overwrite) |
| 2 | Templates directory not found |
| 3 | Missing required argument |
