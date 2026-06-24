# TOOLS.md — clio-codex (Codex CLI)
# Tools available to Clio in the OpenAI Codex CLI runtime.
# Source of truth: state/capabilities/registry.json
# Last updated: 2026-06-08

---

## Native filesystem & code tools

| Tool | Invocation | Notes |
|------|-----------|-------|
| read_file | native | Read files or line ranges |
| write_file / apply_patch | native (Edit/Write) | Create or overwrite files; patch-based edits |
| Bash shell | native:shell | Full shell access within approval/sandbox policy |
| Web search | native | Cached by default; `web_search = "live"` for real-time |
| Image input | `-i file.png` or paste | PNG/JPEG; combine with text prompts |
| Image generation | `$imagegen` in prompt | Uses gpt-image-2; burns 3-5x limit vs text |

## Execution & control

| Tool | Invocation | Notes |
|------|-----------|-------|
| Interactive TUI | `codex` | Full-screen terminal UI |
| Headless exec | `codex exec "<prompt>"` | Non-interactive; stdout = final message |
| JSONL stream | `codex exec --json` | Full event stream for pipeline use |
| Structured output | `codex exec --output-schema schema.json` | JSON schema-constrained final response |
| Session resume | `codex exec resume --last` or `--last "<next>"` | Chains multi-step pipelines |
| Remote TUI | `codex app-server --listen ws://...` + `codex --remote ws://...` | Run server on one machine, TUI on another |
| Cloud tasks | `codex cloud exec --env ENV_ID "<prompt>"` | Launch cloud-hosted Codex task |
| Approval mode | `/permissions` | auto / read-only / full-access |
| Sandbox mode | `--sandbox workspace-write` / `danger-full-access` | Control filesystem + network scope |

## Multi-agent & subagents

| Tool | Invocation | Notes |
|------|-----------|-------|
| Subagents | native + `/agents` | Parallel task delegation; explicit invocation required |
| MCP client | `~/.codex/config.toml` → `[mcp_servers]` | STDIO or streaming HTTP servers |
| MCP server mode | `codex mcp-server` | Expose Codex as MCP tool to other agents |
| MCP management | `codex mcp` CLI | Add, list, remove MCP servers |

## Code review

| Tool | Invocation | Notes |
|------|-----------|-------|
| /review | slash command | Branch diff, uncommitted changes, specific commit; each run = own transcript turn |
| /fork | slash command | Fork conversation from a prior point |
| /side | slash command | Side-by-side diff view |

## Session & config tools

| Tool | Invocation | Notes |
|------|-----------|-------|
| Status | `/status` | Model, account, context %, monthly limit |
| Model selector | `/model` | Switch model mid-session |
| Permissions | `/permissions` | Approval mode switcher |
| Theme | `/theme` | TUI syntax highlighting; saves to config.toml |
| History search | Ctrl+R | Search prompt history |
| Shell passthrough | `!<cmd>` in composer | Run local shell commands inline |
| Completion scripts | `codex completion zsh/bash/fish` | Shell tab completion |
| Features | `codex features list/enable/disable` | Toggle experimental features |

## Hooks (see hooks.json)

| Event | Matcher | Use |
|-------|---------|-----|
| SessionStart | startup\|resume | Auto-create daily log if missing |
| PreToolUse | Bash | Policy check before shell commands |
| PostToolUse | Bash\|Edit\|Write | Post-action logging, validation |
| UserPromptSubmit | — | Prompt scanning (API keys, etc.) |
| Stop | — | Continue loop, log flush |

## Config locations

| File | Purpose |
|------|---------|
| `~/.codex/config.toml` | Global config: model, approval, sandbox, web_search, features, hooks inline |
| `~/.codex/AGENTS.md` | Global persistent instructions (Clio identity chain) |
| `~/.codex/hooks.json` | Global lifecycle hooks |
| `~/.codex/auth.json` | Auth tokens — never commit |
| `~/.codex/sessions/` | Local session transcripts |
| `.codex/config.toml` | Project-local config overrides (trusted projects only) |
| `.codex/hooks.json` | Project-local hooks |
| `AGENTS.md` (repo root) | Project instructions — loaded automatically when `codex` launched from Cliosphere/ |

## Shell-accessible tools (via Bash)

| Tool | Notes |
|------|-------|
| Git | Source control |
| GitHub CLI (`gh`) | PRs, issues, CI logs |
| Docker Compose | Requires Docker running |
| Ansible | Infra provisioning |
| Python 3 | Scripts, orchestrator.py |
| curl | HTTP endpoint testing |
| security | macOS Keychain |

## Tools NOT available on this platform

- Google Workspace MCP (Calendar, Gmail, Drive) → use clio-claude (claude_desktop)
- Long-form architectural reasoning → use clio-claude (coordinator)
- Gemini-specific research/verification → use clio-antigravity
