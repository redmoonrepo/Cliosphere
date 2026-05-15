#!/usr/bin/env bash
# platforms/openclaw/scripts/wsl2-setup.sh
# WSL2 Ubuntu host setup — run ONCE on the WSL2 side (not inside Docker).
# Sets up: CUDA verification, Ollama, model pulls, systemd service config.
# Designed to migrate cleanly to Ansible when multi-host deployment begins.
#
# Usage: bash wsl2-setup.sh
# Re-running is safe — all steps are idempotent.

set -e

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║   Clio - WSL2 Host Setup                     ║"
echo "║   Ollama + CUDA + Local Model Stack          ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# ── 0. Confirm we're in WSL2 ─────────────────────────────────────────────────
if ! grep -qi microsoft /proc/version 2>/dev/null; then
    echo "⚠  This script is intended for WSL2 Ubuntu."
    echo "   /proc/version does not indicate a Microsoft kernel."
    read -rp "   Continue anyway? [y/N] " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || exit 1
fi

# ── 1. System update ─────────────────────────────────────────────────────────
echo "▶ [1/7] Updating system packages..."
sudo apt-get update -qq && sudo apt-get upgrade -y -qq
sudo apt-get install -y -qq \
    curl \
    git \
    jq \
    build-essential \
    ca-certificates

# ── 2. CUDA / GPU verification ───────────────────────────────────────────────
echo ""
echo "▶ [2/7] Verifying CUDA / GPU access..."

if command -v nvidia-smi &>/dev/null; then
    echo "  nvidia-smi found:"
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader \
        | sed 's/^/    /'
    CUDA_OK=true
else
    echo "  ⚠ nvidia-smi not found."
    echo "    GPU passthrough requires:"
    echo "    1. NVIDIA driver 470+ on Windows host"
    echo "    2. WSL2 kernel 5.10.43+ (check: uname -r)"
    echo "    3. cuda-toolkit NOT installed in WSL2 (Windows driver provides this)"
    echo "    See: https://docs.nvidia.com/cuda/wsl-user-guide/"
    CUDA_OK=false
fi

if [ "$CUDA_OK" = false ]; then
    read -rp "  Continue without confirmed GPU? Ollama will use CPU. [y/N] " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || exit 1
fi

# ── 3. Install Ollama ────────────────────────────────────────────────────────
echo ""
echo "▶ [3/7] Installing Ollama..."

if command -v ollama &>/dev/null; then
    CURRENT=$(ollama --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+' || echo "unknown")
    echo "  Ollama already installed (version: $CURRENT)"
    echo "  Checking for updates..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "  Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

echo "  Ollama: $(ollama --version 2>/dev/null || echo 'installed')"

# ── 4. Configure Ollama for Docker access ────────────────────────────────────
echo ""
echo "▶ [4/7] Configuring Ollama host binding..."
# Ollama must listen on 0.0.0.0 so the Docker container can reach it
# via 127.0.0.1 (host networking) or host.docker.internal

OLLAMA_ENV_FILE="/etc/systemd/system/ollama.service.d/override.conf"

if [ ! -f "$OLLAMA_ENV_FILE" ]; then
    sudo mkdir -p "$(dirname "$OLLAMA_ENV_FILE")"
    sudo tee "$OLLAMA_ENV_FILE" > /dev/null <<'EOF'
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"

# ── TurboQuant (enable when Ollama PR #15505 merges — expected Q3 2026) ──
# Uncomment the lines below to activate KV cache compression.
# Provides ~4.9x VRAM savings on long contexts with near-zero quality loss.
# Requires: OLLAMA_NEW_ENGINE=1 and OLLAMA_FLASH_ATTENTION=1
#
# Environment="OLLAMA_NEW_ENGINE=1"
# Environment="OLLAMA_FLASH_ATTENTION=1"
# Environment="OLLAMA_KV_CACHE_TYPE=tq3k"
#
# tq3k = 3-bit K cache only, V at full precision (safer first step)
# tq3  = 3-bit K+V cache (requires flash attention, maximum savings)
# tq4  = 4-bit K+V cache (more conservative, still ~3.8x savings)
# See: https://github.com/ollama/ollama/pull/15505
EOF
    echo "  Created $OLLAMA_ENV_FILE"
else
    echo "  Ollama override already exists — skipping (edit manually if needed)"
fi

# Reload systemd and restart Ollama
sudo systemctl daemon-reload
sudo systemctl enable ollama 2>/dev/null || true
sudo systemctl restart ollama
sleep 3  # Give Ollama a moment to start

# Verify Ollama is listening
if curl -fsS http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "  Ollama serving on 0.0.0.0:11434 ✓"
else
    echo "  ⚠ Ollama not responding — check: journalctl -u ollama -n 20"
fi

# ── 5. Pull models ───────────────────────────────────────────────────────────
echo ""
echo "▶ [5/7] Pulling local models..."
echo "  Note: Use Q4_K_M quantization to leave VRAM headroom for KV cache."
echo "  RTX 2000 Ada (8GB VRAM) targets:"

# Primary: coding tasks
echo ""
echo "  Pulling qwen2.5-coder:7b (primary — coding, OpenClaw default)..."
ollama pull qwen2.5-coder:7b

# Secondary: reasoning tasks
echo ""
echo "  Pulling deepseek-r1:7b (secondary — complex reasoning, logic)..."
ollama pull deepseek-r1:7b

# Verify
echo ""
echo "  Models available:"
ollama list | sed 's/^/    /'

# ── 6. Create Ollama Modelfile for Clio ─────────────────────────────────────
echo ""
echo "▶ [6/7] Creating Clio Modelfile (optimized context for 8GB VRAM)..."

MODELFILE_DIR="$HOME/.ollama/modelfiles"
mkdir -p "$MODELFILE_DIR"

cat > "$MODELFILE_DIR/clio-coder.Modelfile" <<'EOF'
# Clio - Coding Model
# Base: qwen2.5-coder:7b with VRAM-optimized context settings
# RTX 2000 Ada (8GB): Q4_K_M ~5GB weights, ~3GB left for KV cache
# At Q4_K_M + num_ctx 16384: fits comfortably without swap

FROM qwen2.5-coder:7b

PARAMETER num_ctx 16384       # 16K context — safe for 8GB VRAM
PARAMETER num_gpu 999         # All layers on GPU
PARAMETER num_thread 8        # CPU threads for non-GPU work

# When TurboQuant lands in Ollama (Q3 2026), num_ctx can be raised to
# 65536+ without additional VRAM cost. Update this file then.

SYSTEM """
You are Clio, a portable autonomous agent running on a local model.
You are the coding and task-execution instance of Clio.
Read your files before acting. Explore before saying you cannot.
"""
EOF

# Build the custom model
echo "  Building clio-coder model..."
ollama create clio-coder -f "$MODELFILE_DIR/clio-coder.Modelfile"
echo "  clio-coder ✓"

# ── 7. Final verification ────────────────────────────────────────────────────
echo ""
echo "▶ [7/7] Final verification..."

echo "  Ollama status:"
systemctl is-active ollama | sed 's/^/    /'

echo "  Listening on:"
ss -tlnp | grep 11434 | sed 's/^/    /' || echo "    (not found — check ollama service)"

echo "  Models:"
ollama list | sed 's/^/    /'

if [ "$CUDA_OK" = true ]; then
    echo "  GPU memory:"
    nvidia-smi --query-gpu=memory.used,memory.free,memory.total \
        --format=csv,noheader | sed 's/^/    /'
fi

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║   WSL2 setup complete.                       ║"
echo "║                                              ║"
echo "║   Next: run docker compose build             ║"
echo "║   from platforms/openclaw/                   ║"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "  TurboQuant note:"
echo "  When Ollama PR #15505 merges (est. Q3 2026):"
echo "  Edit $OLLAMA_ENV_FILE"
echo "  Uncomment the TurboQuant env vars and restart:"
echo "  sudo systemctl restart ollama"
echo ""
