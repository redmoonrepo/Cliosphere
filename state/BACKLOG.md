# BACKLOG.md — Cliosphere Task Backlog

*Source of truth for all pending work. Dependency-ordered by tier.*
*Format: ID · Name · Description · Depends on*
*Last updated: 2026-06-23*

---

## ✅ Done

- **#1** Manual cleanup — filesystem confirmed clean May 31, 2026
- **#6** Secrets management — architecture decided (SECURITY.md)
- **#9** NemoClaw → Ansible — nemoclaw role now exists
- **#11** HashiCorp Vault — added to docker-compose.j2
- **#12** LiteLLM virtual keys — config/litellm-config.yaml written
- **#13** Portkey — config/portkey-guardrails.json written
- **#18** Update IDENTITY.md model version — removed (Opus not accessible; Sonnet 4.6 is correct)
- **#21** API keys → macOS Keychain — both keys confirmed in Keychain and shell init
- **#22** Migrate Gemini CLI → Antigravity CLI — agy v1.0.7 installed, authenticated, Ansible role updated
- **#23** Configure platforms/antigravity_cli/ — AGENTS.md, IDENTITY.md, SKILLS.md, TOOLS.md, plugin.json written; gemini_cli/ files migrated
- **#24** agent_trigger.sh — written, patched, agy -p verified headless ✅
- **#32** VISION.md — created June 7, 2026
- **#35** Pipeline skills suite — all four scripts written ✅
- **#37** Layer 1 MCP tool (ask_agy) — PTY fix, first live A2A relay confirmed ✅ June 14, 2026
- **#36** tasks.json + orchestrator.py v1 — Phase 1 wire proven live ✅ June 23, 2026
  - `runtime/tasks/tasks.json` — state machine manifest, status values: draft → ready → dispatched → verifying → verified → promoting → pr_open → merged
  - `runtime/events/queue.jsonl` — event wire, appended per cycle, drained per cycle
  - `cliosphere_infra/scripts/orchestrator.py` — deterministic scheduler, two-phase cycle: emit TASK_READY → dispatch agent_trigger.sh via spec directory name
  - Full autonomous path confirmed: tasks.json → orchestrator → TASK_READY event → agent_trigger.sh → agy → review.md. 2m28s wall time. No human in loop.
  - Note: LangGraph assessment (#44) now unblocked.

---

## TIER 0 — Ready now

**#2** GitHub push — commit and push all Cliosphere changes to remote
- Remote repo already exists at redmoonrepo/Cliosphere (private)
- ~65+ uncommitted changes as of 2026-06-23 (a2a relay, orchestrator, pipeline docs, security toolchain, resolution loop update, url registry, Ansible role patch)
- Agent: clio-antigravity (agy) — Claude Code not yet available, agy handles git tasks
- Steps: `git status` (verify .gitignore coverage) → `git add -A` → semantic commit → `git push origin main`
- Stop condition: if git status shows anything from runtime/, infra/, state/memory/daily/, state/knowledge/sources/ — stop and report before committing
- Depends on: #24 ✅

**#38** A2A Layer 1 hardening & rollout
- Consolidates former #38, #39, #40, #27, #25, #17
1. **Auth preflight patch** — add preflight before every dispatch: `agy -p "ping" --print-timeout 15s`. On failure: attempt non-interactive re-auth. If browser required: fast-fail exit 42. Prevents silent 5-minute hangs from expired OAuth tokens.
2. **A2A trigger taxonomy** — document four trigger classes in `core/council/TRIGGERS.md`: failure (exit_code != 0, timeout, exception, test failure, dependency failure), confidence (below threshold, ambiguous requirements, multiple valid solutions), design (new architecture/protocol/schema/MCP/workflow, security decision), review (after code/design/spec complete, before marking done).
3. **agy boot intent classification gate** — agy fires full 12-step boot even for trivial `-p` prompts (47s for "hello"). Design classification gate: spec dispatch → task context only; interactive → full boot; trivial → answer immediately.
4. **Test invoke_agent with codebase_investigator** — ask clio-antigravity to invoke codebase_investigator sub-agent against Cliosphere/. Verify native orchestration, document output in daily log.
5. **Google Drive sync — first agentic pilot task** — clio-antigravity uploads Cliosphere/ state files to Google Drive via spec dispatch.
6. **Google Drive sync — Drive for Desktop + symlink + Drive MCP** — symlink `state/` → Google Drive/Cliosphere/state/ for multi-device state sync (Mirror mode required).
- Depends on: nothing

**#46** Agentic pipeline implementation layer — event bus, trigger engine, agent ownership
- `docs/pipeline.md` is governance only (B+/C- per ChatGPT + agy peer review, June 23 2026). Missing: who invokes each gate, who watches GitHub, who retries on failure.
- Architecture consensus (Claude + agy + ChatGPT): Loop → Event → Trigger → Workflow → Agent → Tool → Artifact
- Phase 2 build targets:
  - `runtime/events/` — event type definitions (TASK_READY proven; add TASK_VERIFIED, TASK_FAILED, PR_CREATED, PR_MERGED, DEPENDENCY_UNBLOCKED)
  - `cliosphere_infra/scripts/` — multiple consumers for queue.jsonl (github_agent, maintenance_agent)
  - `runtime/workflows/promotion.py` — replace future promote_task.sh smell; PromotionWorkflow with steps: run_hygiene(), run_security(), run_integration(), create_branch(), create_pr(), wait_for_hitl(), merge(), unblock_dependents()
  - `core/AGENTS.md` — assign ownership: Task Agent, Review Agent, Promotion Agent, Security Agent, Dependency Agent, GitHub Agent
  - Add governance-only note to `docs/pipeline.md`
- Orchestrator stays deterministic Python — no LLM in the scheduler
- Depends on: #36 ✅, #2

**#28** Cursor headless agent onboarding
- Verify cursor CLI in PATH, test headless flag (`cursor agent --instructions`)
- Write platforms/cursor/HEADLESS.md with dispatch pattern
- Add cursor as headless backend option in agent_trigger.sh
- Depends on: nothing

**#16** Claude Code configuration on mac-mathew
- CLAUDE.md spec-read instruction, agent_trigger.sh, gh CLI auth, git remote
- First spec must be hand-dispatched once (bootstrapping the bootstrapper)
- Depends on: nothing (priority — unblocks entire pipeline)

**#29** Revamp SOUL.md and AGENTS.md — reduce noise, increase signal
- SOUL.md ~6K bytes (target < 3K). AGENTS.md ~8.5K bytes (target < 3K).
- agy file size alerts firing every boot session — address soon.
- Goal: clear, concise, not curt. Bullet-forward.
- Depends on: nothing

**#33** STRATEGY.md — this year's priorities
- Repo root or core/. What we're building in 2026 and why. Outcome-framed epics.
- Depends on: #32 ✅

**#34** Codex CLI onboarding — wire Clio identity into Codex
- Platform files written June 8, 2026: IDENTITY.md, TOOLS.md, SKILLS.md, AGENTS.md, AGENTS.global.md, hooks.json, config.toml, codex_session_start.py
- Remaining: 8 installation steps. Quota-constrained — deprioritized until quota is less stingy.
- Depends on: nothing

**#41** Centralized log aggregation — platform visibility
- Design: each platform writes structured JSONL to `runtime/logs/<platform>/`
- fswatch or cron ships new entries to central aggregator
- Monitoring agent watches for error patterns, triggers A2A relay on match
- Depends on: #19

**#42** memory-wiki — OpenClaw knowledge vault
- Peter Steinberger's wiki concept. Obsidian-compatible.
- Depends on: #3

**#43** docs/ — architecture documentation directory *(partially done)*
- `docs/` directory created ✅ June 23, 2026
- `docs/pipeline.md` written ✅ (governance only — implementation layer is #46)
- Remaining: agent-loop.md, sdd-pipeline.md, secrets-architecture.md, diagrams/
- Depends on: nothing

**#44** LangChain/LangGraph assessment — backlog refinement session
- #36 is now done — this item is unblocked.
- Revisit: does LangGraph DAG-as-state-machine add value over plain Python orchestrator, now that we can see what orchestrator.py actually needs?
- Recommendation from all three agents (Claude + agy + ChatGPT): stay plain Python until the graph itself becomes dynamic. LangGraph is friction at current scale.
- Depends on: #36 ✅

---

## TIER 1 — Depends on Tier 0

**#4** LiteLLM on Mac — verify compose render for mac host_type + test endpoint
- Depends on: #2

**#26** Claude Code local model routing + second Gemini API key
- Claude Code `--model` flag routes to LiteLLM proxy → local Ollama/MLX-LM model
- Second Gemini API key: subagent role
- Depends on: #16, #4

---

## TIER 2 — Depends on Tier 1

**#3** NemoClaw deployment on wsl2-dell
- Full chain: Docker Desktop + Vault + Portkey + LiteLLM + Ollama + NemoClaw
- ⚠️ Define `clio-home` as a named Docker volume in docker-compose.j2 — required for OpenClaw auth persistence across container rebuilds
- ⚠️ Add `AZURE_MCP_COLLECT_TELEMETRY=false` to env.j2 and docker-compose.j2
- Depends on: #4

**#5** RAG first run
- docker compose up → POST /ingest → POST /query
- Depends on: #3, #16, #22 ✅

**#7** VPS deployment — Oracle Cloud ARM
- Depends on: #3, #5

---

## TIER 3 — Depends on Tier 2

**#8** CI/CD pipeline (full)
- infra/scripts/cicd.sh — local pipeline runner (lint → test → classify → merge/HITL)
- platforms/openclaw/CICD.md — OpenClaw hook config
- GitHub Actions = optional remote guard (VPS-era)
- Depends on: #2, #7, #36 ✅

**#19** Log aggregation — ETL: all agents → SQLite
- log_writer.py (per-agent JSONL) + log_etl.py (hourly ETL to SQLite)
- Depends on: #5, #8

**#31** Self-improving feedback loop
- Signal: review.md → prompt_performance.jsonl → template/prompt changes via SDD
- HITL gate until metric is trusted
- Depends on: #8, #19

**#14** Research intake flow
- Research docs → state/knowledge/sources/ → POST /ingest → RAG indexed
- Depends on: #5

**#45** Tether Clio to SOUL.md — structural trigger for principles at point of action
- Real hook: `message:received` — fires when inbound message arrives, before agent processes it.
- Note: `before_agent_reply` does not exist in OpenClaw — was a conceptual placeholder. Verified against OpenClaw source.
- Depends on: #3

---

## TIER 4 — Depends on Tier 3

**#20** Platform grouping refactor — IDE session required. After #2.

---

## Parked

**Hermes/NemoHermes** — function-calling fine-tune of Mistral. Revisit after NemoClaw stable.
