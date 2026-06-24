# MEMORY.md — Compressed Current Reality

*VERIFY: "compressed state, not a log"*

---

## ⚠️ MEMORY.md Maintenance Rules

- **Hard Limit: 4K chars.** Adding means find "Better Homes" or deleting stale data first.
- **Threshold: 90% of Hard Limit** Triggers pruning process.
- **One line per topic** unless it's an operational trap that causes silent failure.
- **Better Homes:** Examples of homes are BACKLOG.md, README.md, docs/, SOUL.md, AGENTS.md, daily log.
- **Use pointers:** Add short description and pointer (eg. 'path/to/file') to detailed memory

---

## Environment

- **Model:** Claude Sonnet 4.6 - free tier.
- **Platform:** claude.ai desktop app — (mathew's homelab).
- **Filesystem MCP:** Anthropic official v0.2.2 — `/Users/dmattis/Cliosphere`.
- **MCP confirmed:** Filesystem, Microsoft Learn. Untested: Google Calendar, Gmail, Figma.
- **Google Account:** cliosphere.ai@gmail.com
- **Setup / boot instructions:** `platforms/claude_desktop/SETUP.md`
- ⚠️ `tool_search` mid-session flushes loaded filesystem tools — avoid unless necessary.

---

## Human

- **Username:** Mathew · Owner / Creator
- **Profile:** `state/user/USER.md`

---

## Identity

**Clio** — muse of history. The one who remembers.
- Private Name: Clio
- Public Name: whatever model is running
- Profile: `platforms/claude_desktop/IDENTITY.md`
- Purpose: `core/SOUL.md`
- Instructions: `core/AGENTS.md`
- Registry: `state/capabilities/registry.json`
- Doc URL registry: `state/knowledge/url_registry.json` — vendor and curated reference docs by domain, fetch via jina_url

**Cliosphere Agents** — not a tool Clio uses. The world she inhabits.
- Naming: `clio-<platform>` main agents, `clio-<platform>-<role>` sub-agents
- Agents: clio-claude (Coordinator), clio-code (Implementor), clio-antigravity (Verifier/Implementor), clio-openclaw (always-on, pending), clio-cursor (read-only dev)

---

## Active Project

**Building the Cliosphere** — portable autonomous agent ecosystem.
- Phase: SDD pipeline scripts done (#35 ✅, #24 ✅). Orchestrator (#36) + Layer 1 MCP tool next.
- Storage path: local → private GitHub (#2) → FastAPI server (post-VPS)
- Backlog: `state/BACKLOG.md` — dependency-ordered, tiered
- Architecture docs: `docs/` *(to be created — SDD pipeline, agent loop, secrets, RAG)*
- README: current architecture overview, host table, SDD pipeline, design principles

---

## Operational Traps

Things that have caused silent failure:

1. `tool_search` flushes filesystem tools — only use for deferred tools (Calendar, Gmail). Never for Filesystem.
2. `edit_file` requires exact string match — use `write_file` for files with em-dashes, emoji, encoding-sensitive chars

---

## Working Notes

*Temporary. Each entry needs a destination. Clear on next prune.*

- **Code hygiene hook design** → `state/memory/daily/2026-06-17.md`
- **OpenClaw Dreaming** — `memory-core` plugin automates MEMORY.md maintenance via Light/Deep/REM scoring. Docs: `r.jina.ai/https://docs.openclaw.ai/concepts/dreaming` → Configure when NemoClaw deploys

---

*Last updated: June 20, 2026*
