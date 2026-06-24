---
name: resolution-loop
description: >
  Use before logging a problem, adding a trap, creating a backlog item,
  concluding "I cannot", or taking action on any error, blocker, unexpected
  behavior, or unverified claim. Triggers on: "I should note this", "let me
  add that", "this is a trap", "I can't do this", "let me park this", any
  failure, timeout, or ambiguous requirement. Guides structured resolution —
  Triage, Comprehend, Hold, Investigate, Synthesize, Resolve, Completeness —
  before writing anything down. Prevents premature logging, anxiety-driven
  list-building, parroting instead of reasoning, and acting without
  verification. Anchors to SOUL.md principles at point of action.
compatibility: claude_desktop, antigravity_cli, codex_cli
---

# Resolution Loop

A structured reasoning process to apply before acting on any problem,
claim, blocker, or decision. The goal is genuine resolution — not logging,
not parking, not parroting. Structural solutions over documentation.

> *"Explore before concluding 'I cannot.' That conclusion requires evidence."*
> — `core/SOUL.md`

---

## 0. TRIAGE — Choose your loop depth before starting

Not every question warrants a full six-stage loop. Applying full depth to
low-stakes questions wastes context and message budget. Classify first.

| Depth | When to use | Stages |
|-------|-------------|--------|
| **Light** | Known domain, low stakes, no live state involved | COMPREHEND → RESOLVE |
| **Standard** | Multiple valid approaches, moderate stakes, some verification needed | COMPREHEND → HOLD → SYNTHESIZE → RESOLVE → COMPLETENESS |
| **Deep** | Architectural decisions, unknown current state, post-cutoff info needed, peer review warranted | Full loop: all 7 stages |

**Default to Light.** Escalate to Standard if assumptions surface. Escalate to
Deep if investigation would change the answer.

**Force Deep when:**
- The question involves live system state (configs, venvs, running processes)
- The answer may have changed since training cutoff
- An architectural decision will be hard to reverse
- A peer council (`ask_agy`) opinion is warranted

---

## 1. COMPREHEND
Before investigating anything — understand the real intent.

- What is the actual objective, not just the surface request?
- What's implied, inferred, or carrying the most weight?
- What would genuine resolution look like?
- What would "not done" look like?

**Anti-pattern:** parroting the words back without reasoning to the intent.
**Test:** can I state the objective in my own words without using the human's phrasing?

---

## 2. HOLD
Before acting — audit what is known vs assumed.

- What do I actually know with evidence?
- What am I assuming without verification?
- What would change if the assumption is wrong?

**Anti-pattern:** acting on the first plausible explanation.
**Test:** have I separated fact from inference?

---

## 3. INVESTIGATE
Gather before concluding. Use multiple independent sources.

- `web_search` — official docs, white papers, RFCs, release notes
- Read the actual artifact — file, config, log, not memory of it
- Parallel council — `ask_agy` for independent architectural opinion
- Live test — run the command, reproduce the error, POC the fix
- Cross-reference — where do sources agree? Where do they conflict?

See [verification-sources.md](references/verification-sources.md) for source guidance.

**Anti-pattern:** concluding from memory or a single source.
**Test:** have I checked at least two independent sources?

---

## 4. SYNTHESIZE
Reason across what was gathered.

- Where do sources agree? That's signal.
- Where do they conflict? That's where the real answer lives.
- What does the evidence actually support vs what was assumed?

**Anti-pattern:** cherry-picking the source that confirms the first hypothesis.
**Test:** have I accounted for conflicting evidence?

---

## 5. RESOLVE
Fix structurally where possible. In priority order:

1. **Configure it away** — setting, config file, env var
2. **Encode it in the artifact** — file header comment, schema note, template field
3. **Wire it as infrastructure** — preflight script, hook, backlog note at point of use
4. **Document it minimally** — one line, pointer to fix location, only if no structural home exists

**Anti-pattern:** logging the problem instead of solving it. MEMORY.md is the last resort.
**Test:** is there a structural home for this fix that isn't a list?

---

## 6. COMPLETENESS
Before declaring done — verify genuine resolution.

- Did I satisfy the actual intent, not just the surface request?
- Did resolving this surface anything else that now needs attention?
- Am I confident it's resolved, or just done for now?
- If something new surfaced — loop back to COMPREHEND for that too.

**Anti-pattern:** closing the thread while opening another silently.
**Test:** if Mathew asked "is this actually done?" could I say yes with evidence?

---

## When to invoke

| Signal | Action |
|--------|--------|
| "I should note/log/add this" | Stop. Run loop from COMPREHEND. |
| Error, timeout, unexpected output | Stop. Run loop from HOLD. |
| "I can't do X" | Stop. Run loop from INVESTIGATE. |
| About to add a backlog item | Run RESOLVE first — is there a structural fix? |
| About to add an operational trap | Run INVESTIGATE — does it already have a better home? |
| Ambiguous requirement | Run COMPREHEND — what is the actual intent? |
| Task feels done | Run COMPLETENESS before closing. |

---

## Grounding

This loop operationalizes three principles from `core/SOUL.md`:

- **The prior question** → TRIAGE + COMPREHEND + HOLD
- **Explore before "I cannot"** → INVESTIGATE
- **Logical deduction governs action** → SYNTHESIZE + RESOLVE + COMPLETENESS

When in doubt, read `core/SOUL.md` Core Truths before acting.
