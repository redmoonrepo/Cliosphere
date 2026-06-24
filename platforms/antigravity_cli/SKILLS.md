# SKILLS.md — clio-antigravity (Antigravity CLI)
# Skill profile for Clio on the Antigravity CLI platform.
# Source of truth: state/capabilities/registry.json
# Last updated: 2026-06-05 — updated at #23 migration

## Primary role in Cliosphere pipeline

**clio-antigravity = Verifier + Parallel Executor + SDD Implementor**

1. **Verifier:** Diffs Claude Code output against requirements.md → writes review.md
2. **Implementor:** Executes SDD tasks dispatched via agent_trigger.sh
3. **Hook executor:** Event-driven automation via Antigravity CLI plugin hooks
4. **Headless subagent:** Invoked by orchestrator.py for parallel task branches

## Skills

### SDD pipeline skills
- Read `runtime/tasks/<task>/requirements.md`, `design.md`, `tasks.md` before any action
- Execute tasks against spec — no deviation from design.md
- Write `runtime/tasks/<task>/review.md` — acceptance criteria checklist + pass/fail
- Update `tasks.md` — check off completed steps
- Update `runtime/tasks/tasks.json` — set status: done, unlock dependents

### Verification skills
- Diff implementation output against acceptance criteria in requirements.md
- Classify result: pass / fail / partial
- On fail: create `runtime/tasks/debug-<task>/` spec folder with failure analysis
- On pass: trigger orchestrator.py re-evaluation (update tasks.json)

### Shell / infrastructure skills
- Git: commit, push, PR creation via gh CLI
- Docker Compose: up, down, logs, exec
- Ansible: run playbooks against inventory hosts
- Python: run scripts, install packages
- macOS Keychain: read/write via `security` command
- curl: test HTTP endpoints

### Memory skills
- Read MEMORY.md and daily logs at session start
- Write daily log entries (`state/memory/YYYY-MM-DD.md`) at session end
- Never overwrite MEMORY.md without explicit instruction

### Research skills (via google_search + fetch)
- Search for current documentation, release notes, migration guides
- Fetch full page content for technical reference
- Surface findings as structured summaries for Clio (claude_desktop) to review

## Skills NOT available on this platform

- Image generation / SVG diagrams → use clio-claude (claude_desktop)
- Long-form architectural reasoning → use clio-claude (coordinator)
- MCP tool suite (Google Calendar, Gmail, Figma) → use clio-claude (claude_desktop)

## Skill load order for SDD tasks

```
1. Read boot files (AGENTS.md → SOUL.md → IDENTITY.md → MEMORY.md → USER.md)
2. Read task spec (requirements.md → design.md → tasks.md)
3. Use /plan to plan execution (Plan Mode — read-only safe)
4. Execute task step by step, checking off tasks.md as you go
5. Write review.md
6. Update tasks.json status
7. Write daily log entry
8. Exit (headless) or report (interactive)
```

*Last updated: 2026-06-05*
