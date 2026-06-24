# Verification Sources

Reference guide for the INVESTIGATE step of the resolution loop.
Use multiple independent sources. Cross-reference before concluding.

---

## Source Hierarchy

In rough order of authority for technical claims:

| Source | When to use | How |
|--------|-------------|-----|
| Official docs | Any API, CLI, config claim | `web_search` → fetch with `r.jina.ai/` |
| Release notes / changelog | Version-specific behavior | `web_search "<tool> changelog <version>"` |
| RFC / white paper | Protocol or standard claims | `web_search` + fetch |
| Live test / POC | Behavioral claims | Run the command, reproduce the error |
| Log files | Runtime failures | Read actual log, not memory of it |
| Agent council | Independent reasoning | `ask_agy`, `ask_codex` in parallel |
| Human | Intent, priority, context | Ask User directly |
| Memory / training | Last resort only | Flag as unverified if used alone |

---

## Cross-referencing Rules

- **Two sources minimum** for any non-trivial claim
- **Independent sources only** — two sources citing the same upstream don't count
- **Conflicts are signal** — don't discard the disagreeing source, investigate why
- **Live test beats docs** when behavior differs from documentation
- **Agent council beats memory** — ask_agy/ask_gemini fire fresh reasoning

---

## Common Investigation Patterns

**CLI flag or behavior claim:**
```
1. web_search "<tool> <flag> official docs"
2. Run: <tool> --help | grep <flag>
3. Live test with minimal POC
```

**"This is already handled somewhere" claim:**
```
1. Read the actual file (don't trust memory)
2. Search the file for the relevant string
3. Confirm with: Filesystem:read_text_file → grep
```

**Error message diagnosis:**
```
1. Read the actual log file
2. web_search the exact error string
3. Ask council: ask_agy / ask_codex with error + context
4. Cross-reference against official docs
5. POC the suspected fix before committing
```

**"I cannot do X" conclusion:**
```
1. web_search "how to X <platform/tool>"
2. Check SKILLS.md — is there a skill for this?
3. Ask council — ask_agy / ask_gemini
4. Only conclude "cannot" after all three return no ladder
```

---

## Cliosphere-Specific Sources

| Topic | Source |
|-------|--------|
| Agent behavior | `core/AGENTS.md`, `core/SOUL.md` |
| Platform capabilities | `platforms/<platform>/TOOLS.md`, `SKILLS.md` |
| Security decisions | `SECURITY.md` |
| Architecture | `README.md`, `docs/` (when written) |
| Backlog / priorities | `state/BACKLOG.md` |
| Recent decisions | `state/memory/daily/YYYY-MM-DD.md` |
| Operational traps | `state/memory/MEMORY.md` |
| Registry | `state/capabilities/registry.json` |
