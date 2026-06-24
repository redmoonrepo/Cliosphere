# RAG.md — Knowledge Layer Configuration

*Status: Scaffolded. Not yet operational.*
*Last updated: 2026-05-23*

---

## Purpose

Semantic retrieval layer for Clio's knowledge corpus. Supplements the flat-file memory system by enabling query-based context retrieval instead of loading all files at boot.

Driver: as the daily log archive grows past a few dozen entries, loading everything into context becomes untenable. RAG replaces bulk loading with targeted retrieval.

---

## Directory Structure

```
state/knowledge/
├── chroma_db/     ← persistent Chroma vector store (gitignored)
├── sources/       ← raw documents fed into the index
└── RAG.md         ← this file
```

---

## Corpus (Planned Initial Index)

| Source | Path | Priority |
|--------|------|----------|
| Long-term memory | state/memory/MEMORY.md | High |
| Daily logs | state/memory/YYYY-MM-DD.md | High |
| Agent identity | core/AGENTS.md | High |
| Soul principles | core/SOUL.md | Medium |
| User profile | state/user/USER.md | Medium |
| RSS digests | state/knowledge/sources/ | Low (future) |

---

## Stack (Planned)

- **Embedding model:** `nomic-embed-text` via Ollama (local, free)
- **Vector store:** Chroma (persistent, local)
- **Orchestrator:** LlamaIndex or LangChain (Python)
- **LLM for retrieval:** Qwen3-14B or Qwen3.6-27B via MLX-LM (Mac) / Ollama (WSL2)

---

## Open Question

**Where does indexing run?**

- **Mac terminal (manual):** Python script run by Mathew on demand. Simple, no automation.
- **OpenClaw container (automated):** Hook-triggered indexing on session end. Requires OpenClaw on WSL2 to be operational.

Not yet resolved. Resolve before implementation begins.

---

## .gitignore Notes

`chroma_db/` should be gitignored — binary vector data, large, platform-specific.
`sources/` may contain sensitive documents — review before committing.
`RAG.md` — tracked in git.
