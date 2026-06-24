#!/usr/bin/env python3
"""
write_daily_log.py — Create or append to today's daily memory log.

Usage:
    python write_daily_log.py --action create
    python write_daily_log.py --action append --section "## Tasks Completed" --content "- 20260610-027: PASS"
    python write_daily_log.py --action append --section "## Files Changed" --content "- platforms/foo.py — new"

Actions:
    create  — creates today's YYYY-MM-DD.md if it doesn't exist. No-op if it does.
    append  — appends content under a named section. Creates file first if needed.

Exit codes:
    0 — success
    3 — missing required argument
"""

import argparse
import os
import sys
from datetime import date, datetime
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

CLIO_ROOT = Path(os.environ.get("CLIO_ROOT", Path(__file__).parents[4]))
DAILY_DIR = CLIO_ROOT / "state" / "memory" / "daily"

# ── Args ──────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(description="Create or append to today's daily log.")
    parser.add_argument("--action", required=True, choices=["create", "append"],
                        help="create: scaffold today's log. append: add content to a section.")
    parser.add_argument("--section", default=None,
                        help="Section header to append under (e.g. '## Tasks Completed')")
    parser.add_argument("--content", default=None,
                        help="Content to append under the section")
    parser.add_argument("--platform", default="unknown",
                        help="Platform ID for session header (e.g. claude_desktop, codex_cli)")
    parser.add_argument("--agent", default="clio",
                        help="Agent ID for session header (e.g. clio-claude, clio-codex)")
    parser.add_argument("--date", default=None,
                        help="Override date YYYY-MM-DD (default: today)")
    return parser.parse_args()

# ── Helpers ───────────────────────────────────────────────────────────────────

def log_path(date_str: str) -> Path:
    return DAILY_DIR / f"{date_str}.md"

def scaffold_log(date_str: str, platform: str, agent: str) -> str:
    return f"""# Daily Log — {date_str}

*Session: {platform} ({agent}) · Mathew*

---

## Session Summary

*(to be updated)*

---

## Tasks Completed

*(none yet)*

---

## Decisions Made

*(none yet)*

---

## Files Changed

*(none yet)*

---

## Next Session Priorities

*(to be updated at session close)*
"""

def ensure_log_exists(date_str: str, platform: str, agent: str) -> Path:
    """Create the log file if it doesn't exist. Return the path."""
    path = log_path(date_str)
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(scaffold_log(date_str, platform, agent), encoding="utf-8")
        print(f"✓ Created: {path}")
    return path

# ── Actions ───────────────────────────────────────────────────────────────────

def action_create(date_str: str, platform: str, agent: str) -> None:
    path = log_path(date_str)
    if path.exists():
        print(f"Log already exists (no-op): {path}")
        return
    ensure_log_exists(date_str, platform, agent)


def action_append(date_str: str, platform: str, agent: str,
                  section: str, content: str) -> None:
    if not section:
        print("ERROR: --section is required for --action append", file=sys.stderr)
        sys.exit(3)
    if not content:
        print("ERROR: --content is required for --action append", file=sys.stderr)
        sys.exit(3)

    path = ensure_log_exists(date_str, platform, agent)
    existing = path.read_text(encoding="utf-8")

    timestamp = datetime.now().strftime("%H:%M")

    # If section already exists in the file, append content after it
    if section in existing:
        # Find the section and insert content after the first blank line following it
        lines = existing.splitlines(keepends=True)
        insert_at = None
        in_section = False
        for i, line in enumerate(lines):
            if line.strip() == section.strip():
                in_section = True
                continue
            if in_section:
                # Find the end of this section (next ## heading or EOF)
                if line.startswith("## ") or line.startswith("---"):
                    insert_at = i
                    break
        if insert_at is not None:
            lines.insert(insert_at, f"{content}\n")
        else:
            # Section found but no following heading — append at end of file
            lines.append(f"{content}\n")
        path.write_text("".join(lines), encoding="utf-8")
    else:
        # Section doesn't exist — add a new continuation block at the end
        addition = f"\n---\n*Continuation — {timestamp} ET*\n\n{section}\n\n{content}\n"
        with path.open("a", encoding="utf-8") as f:
            f.write(addition)

    print(f"✓ Appended to {section} in {path.name}")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    date_str = args.date or date.today().isoformat()

    if args.action == "create":
        action_create(date_str, args.platform, args.agent)

    elif args.action == "append":
        action_append(date_str, args.platform, args.agent,
                      args.section, args.content)


if __name__ == "__main__":
    main()
