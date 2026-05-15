#!/usr/bin/env bash
# platforms/openclaw/scripts/post-create.sh
# Lightweight — called by devcontainer.json on every container create.
# Fast checks only. Heavy installs go in setup-tools.sh.

set -e

CLIO_ROOT="/workspaces/Cliosphere"
WORKSPACE="$CLIO_ROOT/state"

echo "▶ Clio post-create checks..."

# ── Ensure state dirs exist (idempotent) ─────────────────────────────────────
mkdir -p "$WORKSPACE/memory"
mkdir -p "$CLIO_ROOT/state/capabilities"
mkdir -p "$CLIO_ROOT/state/user"
mkdir -p "$CLIO_ROOT/platforms/openclaw/memory"

# ── Symlink structure ─────────────────────────────────────────────────────────
# OPENCLAW_WORKSPACE_DIR=$WORKSPACE — OpenClaw reads flat filenames from here.
# All files are symlinks to canonical sources. One source of truth, no copies.
#
# Shared (core/) — platform-agnostic
link_if_exists() {
    local target="$1"
    local link="$2"
    if [ -f "$target" ]; then
        ln -sf "$target" "$link"
        echo "  linked: $(basename "$link") → ${target#$CLIO_ROOT/}"
    else
        echo "  ⚠ missing source: ${target#$CLIO_ROOT/}"
    fi
}

echo "  Symlinking workspace files..."

# core/ — shared, platform-agnostic
link_if_exists "$CLIO_ROOT/core/agent.md"      "$WORKSPACE/AGENTS.md"
link_if_exists "$CLIO_ROOT/core/soul.md"        "$WORKSPACE/SOUL.md"
link_if_exists "$CLIO_ROOT/core/bootstrap.md"   "$WORKSPACE/BOOTSTRAP.md"

# MEMORY.md lives at workspace root — OpenClaw recognizes this basename natively
# Source is state/memory/MEMORY.md; link at workspace root for bootstrap injection
link_if_exists "$WORKSPACE/memory/MEMORY.md" "$WORKSPACE/MEMORY.md"

# state/user/ — human profile
link_if_exists "$CLIO_ROOT/state/user/USER.md"  "$WORKSPACE/USER.md"

# platforms/openclaw/ — platform-specific (IDENTITY, SKILLS, TOOLS)
link_if_exists "$CLIO_ROOT/platforms/openclaw/IDENTITY.md" "$WORKSPACE/IDENTITY.md"
link_if_exists "$CLIO_ROOT/platforms/openclaw/SKILLS.md"   "$WORKSPACE/SKILLS.md"
link_if_exists "$CLIO_ROOT/platforms/openclaw/TOOLS.md"    "$WORKSPACE/TOOLS.md"

# HEARTBEAT.md — only when VPS deployed; skip silently if absent
if [ -f "$CLIO_ROOT/platforms/openclaw/HEARTBEAT.md" ]; then
    link_if_exists "$CLIO_ROOT/platforms/openclaw/HEARTBEAT.md" "$WORKSPACE/HEARTBEAT.md"
fi

# ── Verify Ollama ─────────────────────────────────────────────────────────────
if curl -fsS http://127.0.0.1:11434/api/tags > /dev/null 2>&1; then
    echo "  Ollama ✓"
else
    echo "  ⚠ Ollama unreachable — run: OLLAMA_HOST=0.0.0.0:11434 ollama serve"
fi

# ── Remind if full setup hasn't been run ─────────────────────────────────────
if ! which claude > /dev/null 2>&1; then
    echo "  ⚠ Claude Code not found — run setup-tools.sh for full provisioning"
fi

echo "▶ Post-create complete."
