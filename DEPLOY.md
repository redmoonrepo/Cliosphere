# DEPLOY.md — Cliosphere Deployment Runbook

*Agent-executable. Humans handle HITL gates only.*

---

## Mac (Primary) — First Deploy

### Prerequisites (verify once)
```bash
docker --version          # 27.x+
ansible --version         # core 2.x+
gh --version              # for GitHub push
```

### Secrets (HITL — export before running deploy)
```bash
export VAULT_DEV_TOKEN=$(openssl rand -hex 16)
export LITELLM_MASTER_KEY=$(openssl rand -hex 32)
export GEMINI_API_KEY=<your-free-gemini-key>      # console.cloud.google.com
export ANTHROPIC_API_KEY=<your-key-if-you-have-one>  # optional
```

### Run
```bash
cd ~/Cliosphere
chmod +x infra/scripts/deploy.sh
./infra/scripts/deploy.sh
```

Deploy script phases:
1. **Prerequisites** — checks docker, ansible, git, gh
2. **GitHub** — creates private repo, commits, pushes
3. **Ansible** — renders `docker-compose.yml` + `.env` for mac-mathew
4. **Docker** — pulls images, builds, `compose up -d`, health checks
5. **Vault** — stores Anthropic + Gemini API keys
6. **LiteLLM** — issues virtual key for OpenClaw agent
7. **Claude Code** — adds gateway env vars to `.zshrc`

HITL gates fire automatically when a secret value is missing. Everything else runs unattended.

---

## Mac — Re-deploy (after config changes)

```bash
# Skip GitHub if no code changes to push
./infra/scripts/deploy.sh --skip-github

# Skip Vault if keys are already stored
./infra/scripts/deploy.sh --skip-vault

# Both
./infra/scripts/deploy.sh --skip-github --skip-vault
```

---

## Dell (WSL2) — After Mac Is Proven

Run from inside WSL2:
```bash
cd ~/Cliosphere     # or wherever repo is cloned
export VAULT_DEV_TOKEN=<same-or-new-token>
export LITELLM_MASTER_KEY=<same-or-new-key>
export GEMINI_API_KEY=<your-key>
./infra/scripts/deploy.sh --host wsl2-dell
```

WSL2 differences (handled automatically by Ansible group_vars):
- `network_mode: host` instead of bridge
- Ollama on `127.0.0.1:11434` instead of MLX-LM on `:1234`
- No Docker Desktop — Docker Engine runs natively in WSL2

---

## Verify Stack

```bash
docker compose ps                         # all services running?
docker compose logs -f clio-vault         # vault healthy?
docker compose logs -f clio-litellm       # litellm started?
docker compose logs -f clio-portkey       # guardrails loaded?
curl http://127.0.0.1:8000/healthz        # RAG service
curl http://127.0.0.1:4000/health         # LiteLLM
```

---

## Claude Code — Switch to Local Model

After deploy, Claude Code talks to LiteLLM instead of Anthropic directly:

```bash
# Already added to .zshrc by deploy.sh — verify:
echo $CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY   # should be 1
echo $ANTHROPIC_BASE_URL                           # should be http://127.0.0.1:4000

# Start Claude Code (MLX-LM must be running with Qwen3 loaded)
cd ~/Cliosphere
claude
```

### MLX-LM — start before Claude Code
```bash
# Pull and serve Qwen3 (first run downloads ~16GB)
pip install mlx-lm
mlx_lm.server --model mlx-community/Qwen2.5-Coder-7B-Instruct-4bit --port 1234
```

---

## Dependency Order Summary

```
GitHub repo (gh repo create)
    ↓
Docker + Ansible confirmed
    ↓
MLX-LM running + Qwen3 pulled          ← Mac only; Ollama on Dell
    ↓
Ansible renders docker-compose.yml + .env
    ↓
docker compose up -d
    ↓
Vault healthy → store API keys
    ↓
LiteLLM healthy → issue virtual key
    ↓
Portkey healthy → guardrails active
    ↓
Claude Code → ANTHROPIC_BASE_URL=http://127.0.0.1:4000
    ↓
claude (uses Gemini free via LiteLLM)
```

---

## Agent Assignment

| Phase | Agent |
|-------|-------|
| GitHub push | Gemini CLI / Claude Code |
| Ansible run | Gemini CLI / Claude Code |
| docker compose up | Gemini CLI / Claude Code |
| Vault key storage | HITL (you enter the key values) |
| LiteLLM virtual key | Gemini CLI / Claude Code |
| Claude Code config | Gemini CLI / Claude Code |
| MLX-LM setup | HITL (first run, model download) |

---

## Next: Dell Laptop

1. Clone repo from GitHub into WSL2
2. Install Docker Engine in WSL2 (not Docker Desktop)
3. Install Ansible in WSL2
4. Ensure Ollama is running: `OLLAMA_HOST=0.0.0.0:11434 ollama serve`
5. Run: `./infra/scripts/deploy.sh --host wsl2-dell`

*Last updated: May 28, 2026*
