---
name: fetching-documentation
description: Retrieves and verifies external documentation using the council pattern — clio-antigravity searches and synthesizes via Google AI, clio-claude fetches ground truth via r.jina.ai and critiques the synthesis. Use during SDD planning phase when a spec requires grounding in external API docs, library references, or integration documentation. Produces verified docs with a confidence annotation, not just a URL.
---

# Fetching Documentation

Adversarial grounding for external documentation. Uses the council pattern: two models, one source of truth, discrepancies surface hallucinations.

## When to use

- Writing `requirements.md` and need to ground a contract, API, or integration in real docs
- A spec references an external library, service, or protocol
- clio-antigravity produced an implementation and you want to verify its API usage
- Any time "I think the API works like X" needs to become "I verified the API works like X"

**Rule:** If a spec references external code or APIs, documentation must be fetched and verified *before* status is set to `ready`. Do not dispatch on training memory.

---

## The Pattern

Three stages. All three must complete before the result is used in a spec.

### Stage 1 — Search (clio-antigravity)

Ask clio-antigravity via `agy -p` or interactively:

```
Find the official documentation for [library/API/concept].
Return:
1. The canonical documentation URL (not a search results page — the actual docs)
2. Your answer to: [specific question about the API/behavior needed for the spec]
```

This triggers a Google AI search. Gemini synthesizes the answer from search results and returns both the URL and its own understanding.

**Why clio-antigravity for this:** Google search underneath means it finds canonical sources, not cached training data. Especially useful for libraries that have changed since any model's training cutoff.

### Stage 2 — Fetch (clio-claude)

Take the URL returned in Stage 1. Prefix it with `r.jina.ai/`:

```
r.jina.ai/https://docs.example.com/api/endpoint
```

This returns the page as clean markdown — no nav chrome, no ads, no scripts. Paste or load into context directly.

**Why r.jina.ai over web_fetch:** web_fetch returns raw HTML with full page chrome, which bloats context significantly. r.jina.ai strips to content only. Use web_fetch as fallback if r.jina.ai is unavailable.

**Fallback:**
```bash
# If r.jina.ai is down or rate-limited
# web_fetch the URL directly — expect more noise in the result
```

### Stage 3 — Critique (clio-claude)

Compare Gemini's Stage 1 synthesis against the Stage 2 ground truth. Explicitly check:

- [ ] Are the method signatures / API contracts correct?
- [ ] Are the parameter names and types accurate?
- [ ] Are the error conditions described correctly?
- [ ] Does Gemini's answer omit anything material to the spec?
- [ ] Does Gemini's answer assert anything the docs don't support?

Flag every discrepancy. Discrepancies mean either:
- Gemini hallucinated (use the docs, discard Gemini's claim)
- The docs changed since Gemini's training (use the docs, note the version)
- The docs are ambiguous (escalate to HITL before spec is finalized)

---

## Output

After all three stages, produce a documentation block for inclusion in `requirements.md §2 Context`:

```markdown
### External documentation: [Library/API name]
- **Source:** [canonical URL]
- **Fetched:** [YYYY-MM-DD]
- **Verified:** Yes — ground truth checked against r.jina.ai fetch
- **Gemini discrepancies found:** [none | list what was wrong]
- **Relevant section:** [paste the specific section(s) needed for the spec]
- **Confidence:** [High / Medium / Low — with reason if not High]
```

This block lives in the spec permanently. It's the evidence trail that the spec was grounded, not assumed.

---

## Council pattern note

This skill is the first formal application of the council pattern to documentation research. The dynamic is intentional:

- clio-antigravity (Gemini) is strong at *finding* and *synthesizing* — Google search gives it breadth
- clio-claude is strong at *critiquing* and *verifying* — adversarial review of Gemini's synthesis surfaces errors

Neither model alone is sufficient. Gemini without verification = hallucination risk. Claude without search = training cutoff risk. Together = higher confidence than either achieves alone.

The output of this skill feeds directly into spec quality → review.md FR confidence scores → `prompt_performance.jsonl`. Specs grounded with verified docs should consistently score higher.

---

## Example invocation

**Scenario:** Writing a spec for `update_tasks_json.py` that reads/writes a JSON file atomically.

**Stage 1 prompt to clio-antigravity:**
```
Find the official Python documentation for atomic file writes using
the pathlib or tempfile modules. Return the canonical docs URL and
explain the correct pattern for writing a file atomically on both
macOS and Linux (write to temp, then os.replace).
```

**Stage 2:** Fetch `r.jina.ai/https://docs.python.org/3/library/os.html#os.replace`

**Stage 3:** Verify Gemini's claimed behavior of `os.replace()` against the actual docs. Check: is it truly atomic on macOS? (It is on POSIX — verify this is stated.)

---

## See also

- [dispatching-agents.md](dispatching-agents.md) — clio-antigravity is the agent for Stage 1
- [creating-tasks.md](creating-tasks.md) — specs using this skill should cite docs in §2 Context
- `core/AGENTS.md` — Council section for the broader council pattern
