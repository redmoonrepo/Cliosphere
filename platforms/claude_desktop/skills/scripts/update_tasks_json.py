#!/usr/bin/env python3
"""
update_tasks_json.py — Read/write runtime/tasks/tasks.json. Cascade on complete.

Usage:
    python update_tasks_json.py --action status
    python update_tasks_json.py --action add --task-id 20260610-027-test-invoke-agent
    python update_tasks_json.py --action add --task-id 20260610-002-github-push \
        --depends-on "20260610-016-claude-code-setup,20260610-024-agent-trigger" \
        --unblocks ""
    python update_tasks_json.py --action complete --task-id 20260610-027-test-invoke-agent
    python update_tasks_json.py --action set-status --task-id <id> --status dispatched

Actions:
    status       — print pipeline state (ready, dispatched, blocked, complete)
    add          — register a task in tasks.json. Dependencies passed explicitly as args.
    complete     — mark task done, cascade to unblocked downstream items
    set-status   — set arbitrary status (draft/ready/dispatched/failed/blocked)

Dependency args (--action add):
    --depends-on  comma-separated list of task IDs this task waits on (default: none)
    --unblocks    comma-separated list of task IDs this task unblocks (default: none)
    Dependencies are coordinator knowledge — pass them here, not in the spec file.

Exit codes:
    0 — success
    1 — task not found in tasks.json
    2 — spec directory or requirements.md not found
    3 — missing required argument
    4 — invalid status value
"""

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

CLIO_ROOT = Path(os.environ.get("CLIO_ROOT", Path(__file__).parents[4]))
TASKS_DIR = CLIO_ROOT / "runtime" / "tasks"
TASKS_JSON = TASKS_DIR / "tasks.json"

VALID_STATUSES = {"draft", "ready", "dispatched", "complete", "failed", "blocked"}

# ── Args ──────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(description="Manage runtime/tasks/tasks.json DAG.")
    parser.add_argument("--action", required=True,
                        choices=["status", "add", "complete", "set-status"],
                        help="Action to perform")
    parser.add_argument("--task-id", default=None,
                        help="Full task ID (e.g. 20260610-027-test-invoke-agent)")
    parser.add_argument("--depends-on", default="",
                        help="Comma-separated task IDs this task waits on (add only)")
    parser.add_argument("--unblocks", default="",
                        help="Comma-separated task IDs this task unblocks (add only)")
    parser.add_argument("--status", default=None,
                        help="Status value for set-status action")
    return parser.parse_args()


def parse_id_list(raw: str) -> list:
    """Parse a comma-separated string of task IDs into a list. Empty string → []."""
    if not raw or not raw.strip():
        return []
    return [s.strip() for s in raw.split(",") if s.strip()]

# ── tasks.json helpers ────────────────────────────────────────────────────────

def load_tasks() -> list:
    """Load tasks.json, returning empty list if file doesn't exist yet."""
    if not TASKS_JSON.exists():
        return []
    return json.loads(TASKS_JSON.read_text(encoding="utf-8"))


def save_tasks(tasks: list) -> None:
    TASKS_JSON.parent.mkdir(parents=True, exist_ok=True)
    TASKS_JSON.write_text(
        json.dumps(tasks, indent=2) + "\n",
        encoding="utf-8"
    )


def find_task(tasks: list, task_id: str) -> dict | None:
    return next((t for t in tasks if t["id"] == task_id), None)

# ── Spec parsing ──────────────────────────────────────────────────────────────

def parse_requirements(task_id: str) -> dict:
    """
    Read requirements.md to extract agent, backlog_ref, and slug.
    Dependencies are NOT parsed from the file — they are passed as CLI args.
    """
    spec_dir = TASKS_DIR / task_id
    req_path = spec_dir / "requirements.md"

    if not spec_dir.exists():
        print(f"ERROR: Spec directory not found: {spec_dir}", file=sys.stderr)
        sys.exit(2)
    if not req_path.exists():
        print(f"ERROR: requirements.md not found in {spec_dir}", file=sys.stderr)
        sys.exit(2)

    content = req_path.read_text(encoding="utf-8")

    # Extract agent from ## Agent section
    agent_match = re.search(r"^## Agent\s*\n`([^`]+)`", content, re.MULTILINE)
    agent = agent_match.group(1) if agent_match else "unknown"

    # Derive backlog_ref and slug from task ID segments
    # Format: YYYYMMDD-NNN-slug → parts[1] = NNN, parts[2:] = slug
    parts = task_id.split("-")
    backlog_ref = f"#{int(parts[1])}" if len(parts) >= 3 and parts[1].isdigit() else ""
    slug = "-".join(parts[2:]) if len(parts) >= 3 else task_id

    return {
        "id": task_id,
        "backlog_ref": backlog_ref,
        "slug": slug,
        "agent": agent,
        "spec_dir": f"runtime/tasks/{task_id}",
    }

# ── Actions ───────────────────────────────────────────────────────────────────

def action_status(tasks: list) -> None:
    if not tasks:
        print("tasks.json is empty or does not exist.")
        print(f"Expected at: {TASKS_JSON}")
        return

    buckets = {s: [] for s in ["ready", "dispatched", "draft", "blocked", "complete", "failed"]}
    for t in tasks:
        status = t.get("status", "draft")
        buckets.setdefault(status, []).append(t)

    print(f"=== Pipeline Status — {date.today()} ===\n")

    for label, entries in [
        ("READY (can dispatch now)", buckets["ready"]),
        ("DISPATCHED (in progress)", buckets["dispatched"]),
        ("DRAFT (spec incomplete)", buckets["draft"]),
        ("BLOCKED (waiting on deps)", buckets["blocked"]),
        ("FAILED", buckets["failed"]),
        ("COMPLETE", buckets["complete"]),
    ]:
        if entries:
            print(f"{label}:")
            for t in entries:
                deps = f"  → waiting on: {', '.join(t.get('depends_on', []))}" \
                    if t.get("status") == "blocked" and t.get("depends_on") else ""
                print(f"  {t['id']}  [{t.get('agent', '?')}]  {t.get('backlog_ref', '')}{deps}")
        else:
            print(f"{label}:\n  (none)")
        print()


def action_add(tasks: list, task_id: str,
               depends_on: list, unblocks: list) -> None:
    if find_task(tasks, task_id):
        print(f"Task already exists in tasks.json: {task_id}")
        print("Use --action set-status to update it.")
        return

    entry = parse_requirements(task_id)
    entry["depends_on"] = depends_on
    entry["unblocks"] = unblocks

    # Determine initial status: ready if no unmet dependencies, else blocked
    existing_complete = {t["id"] for t in tasks if t.get("status") == "complete"}
    unmet = [d for d in depends_on if d not in existing_complete]
    entry["status"] = "blocked" if unmet else "ready"
    entry["created"] = date.today().isoformat()

    tasks.append(entry)
    save_tasks(tasks)

    print(f"✓ Added: {task_id}")
    print(f"  Status:     {entry['status']}")
    print(f"  Agent:      {entry['agent']}")
    print(f"  depends_on: {depends_on or '(none)'}")
    print(f"  unblocks:   {unblocks or '(none)'}")
    if unmet:
        print(f"  Blocked by: {', '.join(unmet)}")


def action_complete(tasks: list, task_id: str) -> None:
    task = find_task(tasks, task_id)
    if not task:
        print(f"ERROR: Task not found in tasks.json: {task_id}", file=sys.stderr)
        print("Run --action add first.", file=sys.stderr)
        sys.exit(1)

    task["status"] = "complete"
    task["completed"] = date.today().isoformat()

    # Cascade: find every blocked task that lists this one in depends_on
    newly_unblocked = []
    complete_ids = {t["id"] for t in tasks if t.get("status") == "complete"}

    for t in tasks:
        if t.get("status") != "blocked":
            continue
        deps = t.get("depends_on", [])
        if task_id not in deps:
            continue
        if all(d in complete_ids for d in deps):
            t["status"] = "ready"
            newly_unblocked.append(t["id"])

    save_tasks(tasks)

    print(f"✓ Marked complete: {task_id}")
    if newly_unblocked:
        print(f"\nNewly unblocked ({len(newly_unblocked)}):")
        for uid in newly_unblocked:
            t = find_task(tasks, uid)
            print(f"  {uid}  [{t.get('agent', '?')}]  {t.get('backlog_ref', '')}")
        print("\nThese tasks are now READY. Scaffold specs with create_task.py if needed.")
    else:
        print("No tasks newly unblocked.")


def action_set_status(tasks: list, task_id: str, status: str) -> None:
    if status not in VALID_STATUSES:
        print(f"ERROR: Invalid status {status!r}. Valid: {', '.join(sorted(VALID_STATUSES))}",
              file=sys.stderr)
        sys.exit(4)

    task = find_task(tasks, task_id)
    if not task:
        print(f"ERROR: Task not found in tasks.json: {task_id}", file=sys.stderr)
        sys.exit(1)

    old_status = task.get("status", "unknown")
    task["status"] = status
    save_tasks(tasks)
    print(f"✓ {task_id}: {old_status} → {status}")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    tasks = load_tasks()

    if args.action == "status":
        action_status(tasks)

    elif args.action == "add":
        if not args.task_id:
            print("ERROR: --task-id required for --action add", file=sys.stderr)
            sys.exit(3)
        action_add(
            tasks,
            args.task_id,
            depends_on=parse_id_list(args.depends_on),
            unblocks=parse_id_list(args.unblocks),
        )

    elif args.action == "complete":
        if not args.task_id:
            print("ERROR: --task-id required for --action complete", file=sys.stderr)
            sys.exit(3)
        action_complete(tasks, args.task_id)

    elif args.action == "set-status":
        if not args.task_id or not args.status:
            print("ERROR: --task-id and --status required for --action set-status",
                  file=sys.stderr)
            sys.exit(3)
        action_set_status(tasks, args.task_id, args.status)


if __name__ == "__main__":
    main()
