# pipeline.md — SDD Promotion Pipeline

*How a completed SDD task goes from review.md PASS to merged on main.*
*Last updated: 2026-06-23*

---

## Overview

The SDD pipeline ends at `review.md PASS`. The promotion pipeline starts
there and carries the artifact to `main` through four gates, each enforced
by a dedicated agent or script — never by the worker that produced the artifact.

**Core principle:** the worker agent and the reviewer agent must be
structurally separate. An agent cannot be both producer and judge.

---

## Task Lifecycle States

Tracked in `runtime/tasks/tasks.json`:

```
draft → ready → dispatched → verifying → verified → promoting → pr_open → merged
                                                         │
                                                    (gate fail)
                                                         │
                                             debug spec generated → ready
```

The orchestrator (`infra/scripts/orchestrator.py`) manages state transitions.
The promotion runner (`infra/scripts/promote_task.sh`) owns the `verified →
merged` path.

---

## Promotion Sequence

```
review.md PASS (reviewer agent ≠ worker agent)
       │
       ▼
  Gate 1: Hygiene
  - ruff (lint + format)
  - MEMORY.md size check (< 4KB)
  - .gitignore coverage check (no runtime/, infra/, daily/ leaking)
       │ PASS
       ▼
  Gate 2: Security
  - gitleaks (secret detection on diff)
  - bandit (Python SAST)
  - pip-audit (supply chain)
  - mcp-scan (MCP tool descriptions)
  - semgrep (agentic patterns — non-blocking initially)
       │ PASS
       ▼
  Gate 3: Integration
  - docker compose up (clean container matching target environment)
  - pytest (functional correctness)
       │ PASS
       ▼
  Git: create branch clio/task-<id>-<slug>
  Git: stage only task-scoped changes
  Git: semantic commit message from task manifest
  GitHub: gh pr create --body-file review.md --base main
       │
       ▼
  Gate 4: HITL
  - Mathew reviews PR diff and CI output
  - gh pr merge --squash (keeps main history clean)
       │ APPROVED
       ▼
  tasks.json status → merged
  orchestrator promotes unblocked dependents → ready
```

---

## Gate Failure Behavior

If Gate 1, 2, or 3 fails:

1. Promotion runner captures stdout/stderr from the failing tool.
2. Orchestrator creates a debug task at `runtime/tasks/debug-<task_id>/`:
   - `requirements.md` — contains the error output and failing gate
   - `tasks.md` — debugging steps for the implementor agent
3. Original task status → `ready` (re-enters the queue).
4. Debug task dispatched to implementor agent.
5. Once debug task reaches `verified`, the original promotion re-runs.

This is the auto-fix loop — gate failures route back into SDD automatically,
no human intervention required.

---

## Reviewer Agent Options

The reviewer must be a different model or platform than the worker.

| Reviewer | Status | Notes |
|----------|--------|-------|
| clio-antigravity (agy) | ✅ Active | Primary reviewer. Dispatched via `ask_agy` MCP tool or agy subagents (`/agents` panel). |
| clio-codex (Codex CLI) | ⚠️ Quota-constrained | Available but stingy monthly quota — reserve for high-stakes review. Codex `/review` reads diffs natively. |
| clio-claude (self) | ❌ Avoid | Worker and reviewer must be separate. Only if no other agent reachable. |

agy subagents run in parallel background threads without blocking the primary
session — use `/agents` to monitor, `Ctrl+J` to teleport to a pending approval.

---

## Commit Message Format

```
type(task-id): brief description

- Implements requirements from requirements.md
- Closes task-<id>
```

Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `infra`

---

## Branch Naming

```
clio/task-<id>-<slug>
```

Example: `clio/task-038-a2a-trigger-taxonomy`

Agent-generated branches are visually distinct from human branches on GitHub.

---

## Related Files

- `runtime/tasks/tasks.json` — DAG manifest and task state
- `infra/scripts/orchestrator.py` — state machine and dependency promotion
- `infra/scripts/promote_task.sh` — promotion runner (to be built, backlog #8)
- `core/SECURITY.md` — security gate toolchain
- `state/BACKLOG.md` — upstream work queue
