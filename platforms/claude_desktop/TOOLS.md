---
title: "TOOLS.md"
summary: "Environment-specific tool configuration — my setup specifics"
read_when:
  - When using environment-specific resources
  - When connecting to named devices, hosts, or services
---

# TOOLS.md — My Tool Setup

*Skills define how tools work. This file is for specifics unique to my setup.*
*Keep this clean. No capabilities lists (that's SKILLS.md). No human notes (that's USER.md).*

---

## Current Tools (claude.ai session)

### Web
- web_search — general search
- web_fetch — fetch specific URLs (auth-gated pages return nav only)

### Filesystem Extension (Desktop MCP — Anthropic official, v0.2.2)
Installed via Settings > Extensions > Connectors > Filesystem.
Provides direct read/write access to '/Users/<HOME_DIR>/Cliosphere' and '/Users/<HOME_DIR>/Library/Application Support/Claude'.
No uploads needed — files are always current on disk.

Tools confirmed:
- read_file — read a single file
- read_multiple_files — batch read
- write_file — create or overwrite a file
- edit_file — make line-based edits
- create_directory — create directories (nested ok)
- list_directory — list files/dirs at a path
- directory_tree — recursive tree view as JSON
- move_file — move or rename files
- search_files — recursive search by pattern
- get_file_info — metadata (size, modified, permissions)
- list_allowed_directories — returns allowed root paths (always check first)

Allowed paths:
- `/Users/<HOME_DIR>/Cliosphere`
- `/Users/<HOME_DIR>/Library/Application Support/Claude`

⚠️ Known quirk: tool_search calls mid-session can flush loaded filesystem tools. Avoid tool_search unless necessary. Tools reload on next use but may require restart if fully dropped.

### Files & Code (Claude.ai container)
- bash_tool — shell commands in container
- create_file, str_replace, view — file operations in Claude's container
- present_files — share files for download

### Connectors (MCP — remote)
- Google Calendar — read/write (not yet tested)
- Gmail — read/compose (not yet tested)
- Microsoft Learn — documentation search
- Figma — design files

### UI & Data
- ask_user_input_v0 — interactive buttons
- weather_fetch — weather by coordinates
- places_search, places_map_display_v0 — location search/maps
- image_search — web images
- message_compose_v1 — draft messages
- visualize:read_me, visualize:show_widget — charts/diagrams
- memory_user_edits — cross-session memory (Claude.ai only)

---

## Setup Notes

### Filesystem Extension installation
- Settings > Extensions > Browse Extensions > Connectors > Filesystem > Install
- Developed by Anthropic, MIT license
- Underlying package: @modelcontextprotocol/server-filesystem

---

## VPS (When Provisioned)

```
# Fill in when VPS is live:
# ssh-host: 
# workspace: ~/.openclaw/workspace
# identity-suite: ~/council/
```

---

*Last updated: May 15, 2026*
*Update when: new hardware, SSH hosts, extensions added, or environment changes.*
