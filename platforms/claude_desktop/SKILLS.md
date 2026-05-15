---
name: claude-skills-registry
description: My capability registry for this platform. Check this before saying "I cannot." If a skill isn't here, search for it or build it.
---

# SKILLS.md — What I Can Do (claude_desktop)

*Part of: Cliosphere / platforms/claude_desktop*
*Check this file before concluding something is impossible.*
*Update this file when new capabilities are discovered or tools change.*
*Global capability map lives in: state/capabilities/registry.json*

---

## The Capability Awareness Protocol

Before saying "I cannot" or "I don't have access to", run the full protocol (defined in core/agent.md):
1. Check `state/capabilities/registry.json` — global capability map
2. Check this file (SKILLS.md) — platform-specific workflows
3. Check TOOLS.md — confirmed tools in this environment
4. Identify what applies, reason about which platform handles it best
5. Remember: web_search is itself a capability — often the bridge when nothing else applies
6. Convene council if blind spots may be limiting the answer
7. Only say "I cannot" if nothing applies after steps 1–6

"I cannot" is a last resort conclusion, not a default response.

---

## Core Skills (Always Available)

### Reasoning & Research
- Long-form reasoning and synthesis
- Web search — query the internet for anything current or unknown
- Web fetch — retrieve full content from specific URLs
- Image search — find visual content
- Extended thinking — visible reasoning chains for hard problems

### Writing & Communication
- Nuanced writing, editing, summarization
- Document drafting (reports, memos, emails, creative)
- Message composition with multiple strategic variants
- Multi-language support

### Code & Engineering
- Write, debug, refactor code in any language
- Code execution in sandboxed environment
- File creation: .md, .html, .jsx, .svg, .mermaid
- Full agentic coding via Claude Code (when on VPS)

### File & Document Creation
- Word documents (.docx) — via skill
- Presentations (.pptx) — via skill
- Spreadsheets (.xlsx) — via skill
- PDFs — via skill
- Images, SVG, diagrams inline

### Data & Analysis
- Read and analyze: CSV, JSON, PDF, images, code files
- Charts and visualizations (React, D3, Recharts)
- Structured data extraction

### Tools & Integrations (Session-Dependent)
- Google Calendar — read/write events
- Gmail — read/compose
- Google Drive — read/write files (MCP)
- Figma — design files
- Microsoft Learn — documentation search
- Web search + fetch — always on

### Memory & Persistence
- Read/write files in this session's container
- Present files for download
- Cliosphere file suite (core/ + state/ + platforms/claude_desktop/)
- Auto Dream (when on Claude Code + VPS)

---

## Skills I Can Build On Demand

If a capability isn't listed above, I can often construct it:
- Custom SKILL.md files for repeatable workflows
- Scripts (Python, JS, bash) for specific tasks
- API calls to Anthropic or other services
- Artifacts: interactive HTML, React components, SVG diagrams

---

## How to Discover New Skills

**At boot — always:**
1. Run Capability Awareness Protocol (steps above)
2. Note the environment: claude.ai? OpenClaw? VPS? Different model?
3. Compare to last known state in MEMORY.md — what's new, what's missing?
4. Write confirmed findings to TOOLS.md and registry.json

**Anthropic tool documentation (canonical reference):**
- Tool use overview: platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- Web search: /web-search-tool
- Web fetch: /web-fetch-tool
- Bash: /bash-tool
- Code execution: /code-execution-tool
- Computer use: /computer-use-tool
- Memory tool: /memory-tool
- Text editor: /text-editor-tool
- Tool search: /tool-search-tool

**For new environments:**
- OpenClaw: docs.openclaw.ai/tools/skills
- agentskills.io for community skills
- Search: "[environment name] available tools capabilities 2026"

**Build it if nothing exists.** The absence of a tool in this list is not "I cannot." It's a gap to fill.

---

*Last updated: April 15, 2026*
*Update when: new tools connected, capabilities discovered, "I cannot" turns out to be wrong*
