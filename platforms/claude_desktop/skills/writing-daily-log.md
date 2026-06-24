---
name: writing-daily-log
description: Creates today's state/memory/daily/YYYY-MM-DD.md if it does not exist, then appends a structured session entry. Use at the start of any session, when Claude Desktop is rate-limited and another agent needs to maintain continuity, or when closing out a session.
---

# Writing Daily Log

Creates and maintains `state/memory/daily/YYYY-MM-DD.md` for session continuity.

## When to use

- Start of any session (if log doesn't exist yet)
- End of session (append what was done)
- Any agent on any platform maintaining continuity when Claude is unavailable

## Quick start

```bash
python platforms/claude_desktop/skills/scripts/write_daily_log.py \
  --action create
# Creates today's log if missing. No-op if it already exists.

python platforms/claude_desktop/skills/scripts/write_daily_log.py \
  --action append \
  --section "## Tasks Completed" \
  --content "- 20260608-027-test-invoke-agent: PASS"
```

## Log structure

```markdown
# Daily Log — YYYY-MM-DD

*Session: <platform> (<agent-id>) · Mathew*

---

## Session Summary
[One paragraph: what was worked on, what was decided]

## Tasks Completed
[List of task IDs with verdict]

## Decisions Made
[Architecture decisions, design choices, anything that affects future sessions]

## Files Changed
[List of files written or modified]

## Next Session Priorities
[Ordered list of what to pick up next]
```

## Platform coverage

This skill ships with `codex_session_start.py` for Codex CLI (SessionStart hook).
For other platforms without hooks, invoke manually at session start.

The goal: every session on every platform leaves a log entry. No session is silent.

## Do not overwrite

Never overwrite an existing log — always append. If the log exists, add a new dated section:

```markdown
---
*Continuation — [HH:MM] ET*

[new content]
```
