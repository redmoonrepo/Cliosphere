# TOOLS.md — clio-antigravity (Antigravity CLI)
# Tools available to Clio in the Antigravity CLI runtime.
# Source of truth: state/capabilities/registry.json
# Last updated: 2026-06-05 — written at #23 migration

---

## Native filesystem & search tools

| Tool | Invocation | Notes |
|------|-----------|-------|
| read_file | native | Read files or targeted line ranges |
| write_file | native | Create new files or overwrite existing |
| replace | native | Surgical context-aware text replacement |
| list_directory | native | List files and subdirectories at a path |
| glob | native | Find files matching patterns (e.g. **/*.py) |
| grep_search | native | Regex search across files |

## Execution & control tools

| Tool | Invocation | Notes |
|------|-----------|-------|
| run_shell_command | native:shell | Bash commands — git, docker, ansible, python, curl, etc. |
| list_background_processes | native | Manage long-running tasks |
| read_background_output | native | Read output from background processes |
| plan mode | /plan | Read-only safe planning before acting. Use before destructive ops. |
| ask_user | native | Request clarification or decisions |

## External research tools

| Tool | Invocation | Notes |
|------|-----------|-------|
| google_web_search | tool:google_search | Search internet for docs, troubleshooting, current info |
| web_fetch | tool:fetch | Extract content from specific URLs including GitHub |

## Delegation & skills tools

| Tool | Invocation | Notes |
|------|-----------|-------|
| invoke_agent | tool:invoke_agent | Delegate to sub-agents: codebase_investigator, generalist, cli_help |
| skills | /skills | Browse and invoke registered skill slash commands |

## Shell-accessible tools (via run_shell_command)

| Tool | Invocation | Notes |
|------|-----------|-------|
| Git | shell:git | Source control — requires git configured |
| GitHub CLI | shell:gh | Repos, PRs, issues — requires gh auth |
| Docker Compose | shell:docker compose | Requires Docker Desktop running |
| Ansible | shell:ansible-playbook | Runs from infra/ |
| Python | shell:python3 | System Python on mac-mathew |
| curl / wget | shell:curl | HTTP — API calls, endpoint testing |
| security | shell:security | macOS Keychain read/write |

## Antigravity CLI session tools

| Tool | Invocation | Notes |
|------|-----------|-------|
| Headless mode | -p / --prompt flag | Inject spec and run non-interactively. Key for agent_trigger.sh. |
| Sandbox | enableTerminalSandbox in settings.json | macOS: sandbox-exec. Linux: nsjail. Default: false. |
| Conversation management | /resume, /rewind, /rename | Session navigation and history rollback |
| Agents panel | /agents | View, manage, approve subagent actions. ctrl+j to jump to pending approval. |
| Tasks panel | /tasks | Monitor background tasks and logs |
| Hooks inspector | /hooks | View all loaded and active hooks |
| MCP manager | /mcp | Configure and inspect MCP server connections |
| Model selector | /model | Change reasoning model (persists across sessions) |
| Permissions | /permissions | Set autonomy level: request-review / always-proceed / strict |
| Logout | /logout | Clear Google session and keyring credentials |

## Plugin system

| Item | Path | Notes |
|------|------|-------|
| Clio plugin root | `~/.gemini/antigravity-cli/plugins/clio/` | hooks.json, skills/, rules/, mcp_config.json |
| Global skills | `~/.gemini/antigravity-cli/skills/` | Auto-load as slash commands in all workspaces |
| Workspace skills | `.agents/skills/` | Git-local slash commands for this project |
| Global MCP config | `~/.gemini/antigravity-cli/mcp_config.json` | Global MCP server definitions |
| Workspace MCP config | `.agents/mcp_config.json` | Project-local MCP servers |
| Settings | `~/.gemini/antigravity-cli/settings.json` | Sandbox, permissions, keybindings |
| Plugin import | `agy plugin import gemini` | One-time migration from legacy Gemini CLI extensions |
| Plugin management | `agy plugin list/install/disable/enable/uninstall` | Plugin lifecycle |

## MCP servers

| Server | Status | Notes |
|--------|--------|-------|
| Filesystem MCP | not yet configured | Add to `~/.gemini/antigravity-cli/mcp_config.json` |
| Google Drive MCP | not yet configured | Available via existing Google OAuth |

## Cliosphere-specific endpoints (when stack is running)

| Service | URL | Auth |
|---------|-----|------|
| RAG query | http://localhost:8000/query | none (local) |
| RAG ingest | http://localhost:8000/ingest | none (local) |
| LiteLLM | http://localhost:4000 | LITELLM_MASTER_KEY |
| Portkey | http://localhost:8787 | none (local) |
| Vault | http://localhost:8200 | VAULT_DEV_TOKEN |
| OpenClaw gateway | http://localhost:18789 | OPENCLAW_GATEWAY_TOKEN |

## Tools NOT available on this platform

- Image generation / SVG visualization → use clio-claude (claude_desktop)
- claude_desktop MCP tools (Google Calendar, Gmail, Figma, Filesystem MCP)
- Claude Code sandbox (different runtime)

## ~/.agents/ conflict note

Microsoft Azure Copilot Skills occupy `~/.agents/skills/` on mac-mathew (23 skills + telemetry hook).
Antigravity CLI workspace skills also land in `.agents/skills/` (project root, not home).
These are different paths — no collision for workspace use. Monitor if global `~/.agents/` overlap emerges.
