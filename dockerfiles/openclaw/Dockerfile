# dockerfiles/openclaw/Dockerfile
# Cliosphere - OpenClaw Platform Image
# Extends official OpenClaw image with Clio's tooling baked in.
# Build: docker compose build
# Base image uses node:24-bookworm-slim + tini (per OpenClaw docs)

FROM ghcr.io/openclaw/openclaw:latest

# Switch to root for installs
USER root

# ── System dependencies ──────────────────────────────────────────────────────
RUN apt-get update -qq && apt-get install -y -qq \
    curl \
    git \
    jq \
    python3 \
    python3-pip \
    build-essential \
    apt-transport-https \
    ca-certificates \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# ── GitHub CLI ───────────────────────────────────────────────────────────────
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
    | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
    | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update -qq \
    && apt-get install -y gh \
    && rm -rf /var/lib/apt/lists/*

# ── Node global tools ────────────────────────────────────────────────────────
RUN npm install -g \
    @anthropic-ai/claude-code \
    @google/gemini-cli \
    playwright

# ── Playwright Chromium ──────────────────────────────────────────────────────
RUN npx playwright install --with-deps chromium

# ── Drop back to node user (OpenClaw default) ────────────────────────────────
USER node

RUN node --version && npm --version

ENV OPENCLAW_WORKSPACE_DIR=/workspaces/Cliosphere/state
ENV OPENCLAW_DISABLE_BONJOUR=1
