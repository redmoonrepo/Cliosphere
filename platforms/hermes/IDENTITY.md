# Hermes Platform — Identity & Status

*Status: UNDER EVALUATION — not yet deployed*
*Added: May 25, 2026*

---

## What Is Hermes?

Hermes is an agent from Nous Research — an open-weight model known for strong function calling, tool use, and structured output. In the NemoClaw ecosystem, NemoHermes is a variant that runs the Hermes agent inside a NemoClaw sandbox instead of the default OpenClaw agent.

`nemohermes` is an alias for `nemoclaw --agent=hermes`. The underlying infrastructure (OpenShell gateway, sandbox isolation, credential vault, network policy) is identical to a standard NemoClaw + OpenClaw deployment.

---

## Key Differences vs OpenClaw

| Aspect | OpenClaw | Hermes (NemoHermes) |
|--------|----------|---------------------|
| Agent type | Claude Code-style agentic assistant | Nous Research open-weight model |
| Interface | Browser dashboard (port 18789) | OpenAI-compatible API only (port 8642) |
| Config dir | `/sandbox/.openclaw` | `/sandbox/.hermes` |
| Status | Production | Experimental |
| Web search | NemoClaw-native config | Not supported in NemoClaw |
| Access method | `openclaw tui` or browser | API client or `hermes` CLI inside sandbox |
| Default model | Configurable | nvidia/nemotron-3-super-120b-a12b |

---

## Why This Is On The Radar

- Encountered organically in NemoClaw install docs — not searched for
- Hermes has a strong reputation for function calling fidelity and structured outputs
- OpenAI-compatible API at port 8642 → potential drop-in LiteLLM route
- Runs inside OpenShell — same security model as the rest of the stack, no new attack surface
- Could be a self-hosted alternative to paid API providers for structured tool-calling tasks

---

## Open Questions (Before Any Action)

1. **Is it an OpenClaw replacement or a complement?**
   OpenClaw is a platform (agentic coding assistant). Hermes is a model-level agent (structured tool use). They likely serve different roles. They can coexist as separate NemoClaw sandboxes.

2. **Can it run locally?**
   Default inference is NVIDIA Endpoints (cloud). Can the underlying Hermes model run via Ollama or vLLM on the WSL2 host? Unknown — needs testing.

3. **Council node candidate?**
   OpenAI-compatible API is exactly the interface LiteLLM routes to. If Hermes can run locally, it becomes a free council node. Worth evaluating.

4. **Production readiness?**
   Explicitly experimental. Not for production workflows. No timeline given.

---

## Install Reference (Experimental)

```bash
export NEMOCLAW_AGENT=hermes
curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash

# Or if NemoClaw is already installed:
nemohermes onboard

# Non-interactive:
export NEMOCLAW_AGENT=hermes
export NEMOCLAW_NON_INTERACTIVE=1
export NEMOCLAW_ACCEPT_THIRD_PARTY_SOFTWARE=1
export NEMOCLAW_SANDBOX_NAME=clio-hermes
export NVIDIA_API_KEY=<key>
curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash

# Health check:
curl -sf http://127.0.0.1:8642/health

# Connect:
nemohermes clio-hermes connect
hermes  # inside sandbox
```

Port forward (after reboot):
```bash
openshell forward start --background 8642 clio-hermes
```

---

## Next Steps

- [ ] Run `nemohermes onboard` in a named sandbox (`clio-hermes`)
- [ ] Test function-calling capability vs OpenClaw
- [ ] Test OpenAI-compatible API at port 8642 as a LiteLLM route
- [ ] Evaluate as council node — can it run on local inference?
- [ ] Revisit production readiness as NemoClaw matures

---

## Platform Files Status

| File | Status |
|------|--------|
| IDENTITY.md | ✅ (this file) |
| SKILLS.md | 🔲 pending evaluation |
| TOOLS.md | 🔲 pending evaluation |
