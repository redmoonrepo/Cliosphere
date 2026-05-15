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

### Files & Code
- bash_tool — shell commands in container
- create_file, str_replace, view — file operations
- present_files — share files for download

### Connectors (MCP)
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

## VPS (When Provisioned)

```
# Fill in when VPS is live:
# ssh-host: 
# workspace: ~/.openclaw/workspace
# identity-suite: ~/council/
```

---

*Last updated: April 3, 2026*
*Update when: new hardware, SSH hosts, or environment changes.*
