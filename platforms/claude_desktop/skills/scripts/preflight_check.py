#!/usr/bin/env python3
"""
preflight_check.py — Validate a task spec before dispatch to agent_trigger.sh.

Usage:
    python preflight_check.py --task-id 20260610-027-test-invoke-agent

Checks:
    - Task directory exists
    - requirements.md exists and status is 'ready' (not 'draft')
    - tasks.md exists
    - No [task-name] placeholders remain in either file
    - Agent binary is in PATH (agy for clio-antigravity, codex for clio-codex)
    - jq is installed (required by agent_trigger.sh)

Exit codes:
    0 — all checks pass, safe to dispatch
    1 — one or more checks failed (details printed to stdout)
    3 — missing required argument
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

CLIO_ROOT = Path(os.environ.get("CLIO_ROOT", Path(__file__).parents[4]))
TASKS_DIR = CLIO_ROOT / "runtime" / "tasks"

AGENT_BINARIES = {
    "clio-antigravity": "agy",
    "clio-codex": "codex",
    "clio-code": "claude",
    "clio-claude": None,  # coordinator — not dispatched headlessly
}

# ── Args ──────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Pre-flight validation before agent dispatch."
    )
    parser.add_argument("--task-id", required=True,
                        help="Full task ID (e.g. 20260610-027-test-invoke-agent)")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress output, only exit code matters")
    return parser.parse_args()

# ── Checks ────────────────────────────────────────────────────────────────────

def check(label: str, passed: bool, detail: str = "", quiet: bool = False) -> bool:
    icon = "✓" if passed else "✗"
    if not quiet:
        line = f"  {icon} {label}"
        if not passed and detail:
            line += f"\n      → {detail}"
        print(line)
    return passed

def run_checks(task_id: str, quiet: bool = False) -> bool:
    task_dir = TASKS_DIR / task_id
    req_path = task_dir / "requirements.md"
    tasks_path = task_dir / "tasks.md"
    all_pass = True

    if not quiet:
        print(f"Pre-flight: {task_id}\n")

    # 1. Task directory exists
    ok = task_dir.exists() and task_dir.is_dir()
    all_pass &= check("Task directory exists", ok,
                      f"Expected: {task_dir}", quiet)
    if not ok:
        # No point continuing — nothing to read
        if not quiet:
            print(f"\n✗ BLOCKED — fix the above before dispatching.")
        return False

    # 2. requirements.md exists
    ok = req_path.exists()
    all_pass &= check("requirements.md exists", ok,
                      f"Expected: {req_path}", quiet)

    # 3. tasks.md exists
    ok = tasks_path.exists()
    all_pass &= check("tasks.md exists", ok,
                      f"Expected: {tasks_path}", quiet)

    # 4. Status is 'ready' in requirements.md
    if req_path.exists():
        content = req_path.read_text(encoding="utf-8")
        status_match = re.search(r"^## Status\s*\n`([^`]+)`", content, re.MULTILINE)
        status = status_match.group(1) if status_match else "unknown"
        ok = (status == "ready")
        all_pass &= check(f"Status is 'ready' (found: '{status}')", ok,
                          "Set ## Status to `ready` in requirements.md", quiet)

        # 5. No [task-name] placeholders in requirements.md
        placeholders = re.findall(r'\[task-name\]', content)
        ok = len(placeholders) == 0
        all_pass &= check("No [task-name] placeholders in requirements.md", ok,
                          f"Found {len(placeholders)} placeholder(s) — replace with actual task ID",
                          quiet)

        # 6. Extract agent for binary check
        agent_match = re.search(r"^## Agent\s*\n`([^`]+)`", content, re.MULTILINE)
        agent = agent_match.group(1) if agent_match else None
    else:
        agent = None

    # 7. No [task-name] placeholders in tasks.md
    if tasks_path.exists():
        tasks_content = tasks_path.read_text(encoding="utf-8")
        placeholders = re.findall(r'\[task-name\]', tasks_content)
        ok = len(placeholders) == 0
        all_pass &= check("No [task-name] placeholders in tasks.md", ok,
                          f"Found {len(placeholders)} placeholder(s) — replace with actual task ID",
                          quiet)

    # 8. Agent binary in PATH
    if agent and agent in AGENT_BINARIES:
        binary = AGENT_BINARIES[agent]
        if binary is None:
            check(f"Agent binary ({agent})", True,
                  "Coordinator — no binary check needed", quiet)
        else:
            ok = shutil.which(binary) is not None
            all_pass &= check(f"Agent binary '{binary}' in PATH ({agent})", ok,
                              f"Install or add to PATH: {binary}", quiet)
    elif agent:
        all_pass &= check(f"Agent '{agent}' recognized", False,
                          f"Unknown agent. Valid: {', '.join(AGENT_BINARIES.keys())}", quiet)

    # 9. jq installed (required by agent_trigger.sh)
    ok = shutil.which("jq") is not None
    all_pass &= check("jq installed", ok,
                      "Install with: brew install jq", quiet)

    # Summary
    if not quiet:
        print()
        if all_pass:
            print(f"✓ READY — safe to dispatch:")
            print(f"  bash infra/scripts/agent_trigger.sh {task_id}")
        else:
            print(f"✗ BLOCKED — fix the above before dispatching.")

    return all_pass

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    if not args.task_id:
        print("ERROR: --task-id is required", file=sys.stderr)
        sys.exit(3)

    passed = run_checks(args.task_id, quiet=args.quiet)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
