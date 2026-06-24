# SKILLS.md — clio-codex (Codex CLI)
# Skill profile for Clio on the OpenAI Codex CLI platform.
# Source of truth: state/capabilities/registry.json
# Last updated: 2026-06-08

---

## Primary role in Cliosphere pipeline

**clio-codex = Implementor / Code Reviewer / Cross-Validator**

1. **Implementor:** Executes SDD tasks dispatched via `codex exec` (analog to `agy -p`)
2. **Code Reviewer:** `/review` against branch/commit — pre-PR quality gate
3. **Cross-validator:** Council member providing GPT-5.5 perspective on architectural decisions
4. **Headless subagent:** `codex exec "<prompt>"` invoked by agent_trigger.sh or orchestrator.py

---

## Skills

### SDD pipeline skills
- Read `runtime/tasks/<task>/requirements.md`, `design.md`, `tasks.md` before any action
- Execute tasks against spec — no deviation from design.md
- Write `runtime/tasks/<task>/review.md` — acceptance criteria checklist + pass/fail
- Update `tasks.md` — check off completed steps
- Update `runtime/tasks/tasks.json` — set status: done, unlock dependents

### Code review skills
- `/review` against base branch — pre-PR risk assessment
- `/review` uncommitted changes — pre-commit quality gate
- `/review` specific commit — post-merge audit
- Custom review instructions: "Focus on security regressions", "Check for spec deviations"
- Each review run = independent transcript turn; comparable across iterations

### Headless dispatch skills
- `codex exec "<prompt>"` — fire and collect final stdout
- `codex exec --json` — JSONL stream for structured pipeline consumption
- `codex exec --output-schema schema.json -o result.json` — schema-constrained structured output
- `codex exec resume --last "<next step>"` — multi-stage pipeline chaining
- Stdin piping: `cat requirements.md | codex exec "implement this spec"`

### Multi-agent skills
- Explicit subagent delegation for parallel task branches
- `codex app-server` for remote TUI access from wsl2-dell or VPS
- MCP client: connect to Cliosphere services (RAG, LiteLLM) when stack is running

### Memory skills
- Read MEMORY.md and daily logs at session start (via AGENTS.md → core/AGENTS.md)
- SessionStart hook creates daily log automatically if missing
- Write daily log entries at session end
- Never overwrite MEMORY.md without explicit instruction

### Research skills
- Web search: built-in (cached default; `--search` for live)
- Prompt: provide URL or question; Codex handles retrieval internally

### Shell / infrastructure skills (same as clio-antigravity)
- Git, gh CLI, Docker Compose, Ansible, Python 3, curl, macOS Keychain

---

## Skill load order for SDD tasks (headless)

```
1. Boot files loaded via AGENTS.md chain (~/.codex/AGENTS.md → core/AGENTS.md)
2. Prompt injected by agent_trigger.sh: spec context + task instruction
3. Read task spec (requirements.md → design.md → tasks.md)
4. Execute task step by step, checking off tasks.md
5. Write review.md
6. Update tasks.json status
7. Exit (codex exec completes; stdout captured by caller)
```

## Skills NOT available on this platform

- Google Workspace MCP (Calendar, Gmail, Drive) → use clio-claude (claude_desktop)
- Gemini-native tools (invoke_agent, subagents with Gemini models) → use clio-antigravity
- Long-form architectural coordination → use clio-claude (coordinator)

*Last updated: 2026-06-08*
