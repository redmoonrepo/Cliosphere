# SETUP.md — Claude Desktop Platform Setup

*How to configure Claude Desktop to run Clio correctly.*
*Follow this when setting up a new Claude Desktop install or recovering from a reset.*

---

## Prerequisites

- Claude Desktop installed (claude.ai/download)
- Cliosphere repo cloned to `$CLIO_ROOT` (default: `~/Cliosphere`)

---

## Step 1 — Install the Filesystem Extension

This gives Clio direct read/write access to the Cliosphere directory without file uploads.

1. Open Claude Desktop
2. Settings > Extensions > Browse Extensions
3. Select **Connectors** tab
4. Find **Filesystem** (developed by Anthropic, v0.2.2)
5. Click **Install**
6. When prompted, allow access to `/Users/<HOME_DIR>/Cliosphere`

Verify: the wrench/hammer icon appears in the chat input box.

Tools this unlocks: `read_file`, `read_multiple_files`, `write_file`, `edit_file`, `create_directory`, `list_directory`, `directory_tree`, `move_file`, `search_files`, `get_file_info`, `list_allowed_directories`

---

## Step 2 — Add "Instructions for Claude"

This triggers Clio's boot sequence automatically on every new conversation.

1. Run the Ansible `claude_desktop` role — this renders the boot instruction to:
   `$CLIO_ROOT/platforms/claude_desktop/boot_instruction.txt`
2. `cat $CLIO_ROOT/platforms/claude_desktop/boot_instruction.txt` and copy the output
3. Settings > General > **Instructions for Claude** — paste

> The template lives at `cliosphere_infra/templates/claude_desktop_boot_instruction.txt.j2`.
> Paths are injected at render time from `{{ clio_root }}` — no hardcoded paths in the repo.

---

## Step 3 — Verify Boot

Start a new conversation. Clio should:
- Read all 7 files silently
- List state/memory/ and read the most recent dated log
- Output a boot checklist with "Who Am I: Clio" as the first row
- End with something to the effect of: "Who am I speaking with, and what are we working on?"
- NOT introduce as Clio in prose
- NOT assume the user's name

If boot doesn't trigger, check that Instructions for Claude saved correctly.

---

## Known Limitations

- No hook system in Claude Desktop (unlike Claude Code's SessionStart hook)
- Boot depends on the "Instructions for Claude" system prompt firing — which it does reliably
- Tool access mode defaults to "Load tools when needed" — filesystem tools load on first use
- tool_search calls mid-session can flush loaded filesystem tools — avoid unless necessary
- Claude Desktop does not run on WSL2; use native macOS or Windows host

---

## What's Next

- [ ] GitHub private repo push (gh repo create Cliosphere --private --source=. --push)
- [ ] OpenClaw platform files: IDENTITY.md, SKILLS.md, TOOLS.md, HEARTBEAT.md
- [ ] Test council poc: Claude Desktop + Gemini CLI sharing same filesystem MCP server
- [ ] VPS provisioning (Oracle Cloud Always Free)

---

*Last updated: 2026-06-18*
