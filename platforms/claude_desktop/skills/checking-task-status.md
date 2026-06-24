---
name: checking-task-status
description: Reads runtime/tasks/tasks.json and reports current pipeline state — what is ready, dispatched, blocked, complete, and what is newly unblocked. Use when orienting at session start, when deciding what to work on next, or when Mathew asks what the pipeline looks like. Read-only, safe for any agent.
---

# Checking Task Status

Read-only pipeline status report from `runtime/tasks/tasks.json`.

## When to use

- Session start orientation: "what should I work on?"
- After a task completes: "what's newly unblocked?"
- Mathew asks for a pipeline overview

## Quick status

```bash
python platforms/claude_desktop/skills/scripts/update_tasks_json.py --action status
```

Sample output:
```
=== Pipeline Status — 2026-06-08 ===

READY (can dispatch now):
  20260608-027-test-invoke-agent  [clio-antigravity]  #27

DISPATCHED (in progress):
  (none)

BLOCKED (waiting on dependencies):
  20260608-002-github-push  → waiting on: #16, #24

COMPLETE:
  (none yet)

Newly unblocked by recent completions:
  (none)
```

## If tasks.json doesn't exist yet

It won't exist until `update_tasks_json.py --action add` is run for the first time, or `orchestrator.py` initializes it. Until then, refer to `state/BACKLOG.md` directly.

## Relationship to BACKLOG.md

`BACKLOG.md` = human planning layer (prose, intent, context)
`tasks.json` = machine execution layer (status, dependencies, agent assignments)

They are not duplicates — they serve different consumers.
