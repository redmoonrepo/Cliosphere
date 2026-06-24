#!/usr/bin/env python3
"""
create_task.py — Scaffold a new SDD task directory from canonical templates.

Usage:
    python create_task.py --id 027 --slug test-invoke-agent --agent clio-antigravity

Output:
    runtime/tasks/YYYYMMDD-<id>-<slug>/
        requirements.md
        design.md
        tasks.md

Exit codes:
    0 — success
    1 — task directory already exists
    2 — templates directory not found
    3 — missing required argument
"""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

CLIO_ROOT = Path(os.environ.get("CLIO_ROOT", Path(__file__).parents[4]))
TEMPLATES_DIR = CLIO_ROOT / "runtime" / "tasks" / "_templates"
TASKS_DIR = CLIO_ROOT / "runtime" / "tasks"

VALID_AGENTS = ["clio-antigravity", "clio-codex", "clio-code", "clio-claude"]

# Templates to copy (review.md is written by the implementing agent, not scaffolded)
SCAFFOLD_TEMPLATES = ["requirements.md", "design.md", "tasks.md"]

# ── Args ──────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(description="Scaffold a new SDD task directory.")
    parser.add_argument("--id", required=True,
                        help="Backlog item ID, zero-padded (e.g. 027). Use 000 for ad-hoc tasks.")
    parser.add_argument("--slug", required=True,
                        help="Task slug: lowercase, hyphens only (e.g. test-invoke-agent)")
    parser.add_argument("--agent", required=True, choices=VALID_AGENTS,
                        help=f"Implementing agent: {', '.join(VALID_AGENTS)}")
    parser.add_argument("--date", default=None,
                        help="Override date prefix YYYYMMDD (default: today)")
    return parser.parse_args()

# ── Validation ────────────────────────────────────────────────────────────────

def validate_slug(slug: str) -> None:
    if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$', slug):
        print(f"ERROR: slug must be lowercase letters, numbers, and hyphens only: {slug!r}", file=sys.stderr)
        sys.exit(3)

def validate_id(backlog_id: str) -> None:
    if not re.match(r'^\d{1,4}$', backlog_id):
        print(f"ERROR: --id must be a number (e.g. 027, 000): {backlog_id!r}", file=sys.stderr)
        sys.exit(3)

# ── Core ──────────────────────────────────────────────────────────────────────

def build_task_name(date_str: str, backlog_id: str, slug: str) -> str:
    padded_id = backlog_id.zfill(3)
    return f"{date_str}-{padded_id}-{slug}"

def substitute_placeholders(content: str, task_name: str, agent: str) -> str:
    """Replace all [task-name] and [agent] placeholders in template content."""
    content = content.replace("[task-name]", task_name)
    # Replace agent placeholder lines — keep whichever agent was chosen
    # Template has: `clio-code` | `clio-antigravity`
    # Replace the full line with just the chosen agent
    content = re.sub(
        r'`clio-code` \| `clio-antigravity`(\s*\n<!-- clio-code:.*\n<!-- clio-antigravity:.*-->)?',
        f'`{agent}`',
        content
    )
    return content

def scaffold_task(task_name: str, agent: str) -> Path:
    task_dir = TASKS_DIR / task_name

    # Check templates exist
    if not TEMPLATES_DIR.exists():
        print(f"ERROR: Templates directory not found: {TEMPLATES_DIR}", file=sys.stderr)
        sys.exit(2)

    # Check task doesn't already exist
    if task_dir.exists():
        print(f"ERROR: Task directory already exists: {task_dir}", file=sys.stderr)
        print("To avoid overwriting work, this script will not proceed.", file=sys.stderr)
        sys.exit(1)

    # Create task directory
    task_dir.mkdir(parents=True)

    # Copy and substitute each template
    for template_name in SCAFFOLD_TEMPLATES:
        template_path = TEMPLATES_DIR / template_name
        if not template_path.exists():
            print(f"WARNING: Template not found, skipping: {template_path}", file=sys.stderr)
            continue

        content = template_path.read_text(encoding="utf-8")
        content = substitute_placeholders(content, task_name, agent)

        dest = task_dir / template_name
        dest.write_text(content, encoding="utf-8")
        print(f"  ✓ {template_name}")

    return task_dir

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()

    validate_id(args.id)
    validate_slug(args.slug)

    date_str = args.date or date.today().strftime("%Y%m%d")
    task_name = build_task_name(date_str, args.id, args.slug)
    task_dir = TASKS_DIR / task_name

    print(f"Creating task: {task_name}")
    print(f"Agent: {args.agent}")
    print(f"Directory: {task_dir}")
    print()

    scaffold_task(task_name, args.agent)

    print()
    print(f"✓ Task scaffolded: {task_dir}")
    print()
    print("Next steps:")
    print(f"  1. Fill requirements.md — objective, context, FRs, contracts")
    print(f"  2. Fill design.md — approach, file ownership, architecture")
    print(f"  3. Fill tasks.md — phased atomic task list")
    print(f"  4. Set status to 'ready' in requirements.md")
    print(f"  5. Dispatch: bash infra/scripts/agent_trigger.sh {task_name}")

if __name__ == "__main__":
    main()
