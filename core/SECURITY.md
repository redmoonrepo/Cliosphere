# SECURITY.md — Cliosphere Security Toolchain

*Gates that run automatically as part of the promotion pipeline.*
*Last updated: 2026-06-23*

---

## Promotion Pipeline Security Gates

Security scanning is not a separate step — it is Gate 2 of the promotion
pipeline. No artifact reaches a PR without passing all gates below.

See `docs/pipeline.md` for the full promotion sequence.

---

## Toolchain

| Tool | Category | Gate | What it catches |
|------|----------|------|----------------|
| `ruff` | Linter + formatter | Gate 1 (Hygiene) | Style violations, import order, dead code — fast |
| `bandit` | SAST (Python) | Gate 2 (Security) | Hardcoded secrets, insecure subprocess calls, weak crypto, shell injection |
| `gitleaks` | Secret detection | Gate 2 (Security) | API keys, tokens, credentials accidentally staged in diff |
| `semgrep` | SAST (pattern matching) | Gate 2 (Security) | Agentic-specific patterns: unsafe subprocess with unsanitized input, prompt injection vectors, insecure deserialization. Non-blocking initially — graduate to hard gate once ruleset is tuned. |
| `pip-audit` | Supply chain | Gate 2 (Security) | Actively malicious PyPI packages; catches what `safety` misses. Added after LiteLLM supply chain incident March 2026. |
| `safety` | Dependency CVEs | Gate 2 (Security) | Known CVEs in Python packages |
| `mcp-scan` | MCP security | Gate 2 (Security) | Tool poisoning, prompt injection in MCP tool descriptions, cross-origin escalation, rug-pull attacks |
| `pytest` | Test runner | Gate 3 (Integration) | Functional correctness in clean containerized environment |

---

## Agentic-Specific Concerns

Standard SAST tools were designed for human-written code. Agentic contexts
introduce additional failure modes that require explicit scanning:

**Semantic privilege escalation** — an agent receives a prompt that causes
it to invoke tools beyond the scope of its task. `semgrep` rules should
flag tool calls with unsanitized external input as their arguments.

**Prompt injection via external content** — web search results, file
contents, or MCP tool outputs fed back into agent context can carry
injected instructions. `mcp-scan` covers MCP surfaces; web content is
mitigated by sandboxing (`agy` sandbox, NemoClaw process isolation).

**Intent drift** — agent output that passes functional tests but does not
match `requirements.md`. This is caught by the reviewer agent reading both
`requirements.md` and the artifact, not by static analysis.

**Secret leakage into context** — Cliosphere's five-layer secrets
architecture (Keychain → ansible-vault → Vault → LiteLLM virtual keys →
Portkey) keeps secrets out of files. `gitleaks` is the backstop that
catches anything that slipped through.

---

## Install (mac-mathew)

```bash
pip install bandit semgrep pip-audit safety --break-system-packages
brew install gitleaks ruff
pip install mcp-scan --break-system-packages   # or: uvx mcp-scan
```

---

## Ansible Provisioning

Security tools are provisioned by the `workspace` Ansible role on all hosts.
See `cliosphere_infra/roles/workspace/` for the task list.

---

## References

- `docs/pipeline.md` — full gate sequence and state machine
- `cliosphere_infra/roles/workspace/` — Ansible provisioning
- NemoClaw Security Best Practices: `r.jina.ai/https://docs.nvidia.com/nemoclaw/security/best-practices`
