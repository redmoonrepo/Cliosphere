---
name: cliosphere-pipeline
description: Cliosphere SDD pipeline skills — create tasks, update backlog, dispatch agents, write daily logs, check pipeline status. Use when working with the task pipeline, backlog, or agent dispatch on any platform including when Claude Desktop is rate-limited.
---

# Cliosphere Pipeline Skills

These skills let any agent operate the SDD pipeline without Claude Desktop being online.

## Available skills

| Skill | When to use | Script |
|-------|-------------|--------|
| [creating-tasks.md](creating-tasks.md) | Scaffold a new spec directory | `scripts/create_task.py` |
| [updating-backlog.md](updating-backlog.md) | Mark done, cascade unblocked items | `scripts/update_tasks_json.py` |
| [dispatching-agents.md](dispatching-agents.md) | Fire agent_trigger.sh with pre-flight | `scripts/preflight_check.py` |
| [writing-daily-log.md](writing-daily-log.md) | Create/append session log | `scripts/write_daily_log.py` |
| [checking-task-status.md](checking-task-status.md) | Read pipeline state | `scripts/update_tasks_json.py --action status` |
| [fetching-documentation.md](fetching-documentation.md) | Verify external docs before dispatch | `agy -p` (Stage 1) + `r.jina.ai/` (Stage 2) |
| [resolution-loop/SKILL.md](resolution-loop/SKILL.md) | Before logging, parking, or acting on any problem, error, or blocker | `web_search` + council dispatch |

## Common sequences

**Start a new task from backlog:**
1. `creating-tasks.md` → scaffold directory
2. Fill spec files (coordinator work — requires judgment)
3. `dispatching-agents.md` → pre-flight + fire

**After a task completes:**
1. `updating-backlog.md` → mark complete, cascade
2. `checking-task-status.md` → see what's newly unblocked
3. `writing-daily-log.md` → record what happened

**Session start (any platform):**
1. `writing-daily-log.md` → create today's log
2. `checking-task-status.md` → orient on pipeline state

## Scripts location

All utility scripts: `platforms/claude_desktop/skills/scripts/`
Run from Cliosphere root: `cd ~/Cliosphere && python platforms/claude_desktop/skills/scripts/<script>.py`

**Pre-dispatch documentation check (when spec references external APIs):**
1. `fetching-documentation.md` → search, fetch, critique
2. Add verified docs block to `requirements.md §2 Context`
3. `dispatching-agents.md` → pre-flight + fire

## Note on script status

Scripts listed here are **specified but not yet implemented** as of June 8, 2026.
Implementation tracked in backlog #35 (create_task.py) and #36 (orchestrator + tasks.json).
The skill docs above define the interface — scripts will be written to match.
