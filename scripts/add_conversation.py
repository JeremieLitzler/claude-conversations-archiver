#!/usr/bin/env python3
"""Add a Claude Code conversation to the repository.

Usage:
    python scripts/add_conversation.py <source_html> [--title "Title"] [--date YYYY-MM-DD]

Steps:
  1. Generate the HTML replay first:
         npx claude-replay <session-id> -o replay.html
  2. Run this script to file it and generate a summary:
         python scripts/add_conversation.py replay.html --title "My conversation"

  The HTML is copied to replays/YYYY-MM-DD-slug.html and a markdown summary
  is written to summaries/YYYY-MM-DD-slug.md with a link to the replay.

Options:
    --title      Human-readable title (defaults to the source filename stem)
    --date       Date in YYYY-MM-DD format (defaults to today)
    --no-summary Skip summary generation
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import generate_summary  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
REPLAYS_DIR = REPO_ROOT / "replays"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


def archive(source: Path, title: str | None = None, date_str: str | None = None, no_summary: bool = False) -> None:
    """Copy a replay HTML into replays/ and optionally generate its summary."""
    title = title or source.stem
    date_str = date_str or str(date.today())
    dest_name = f"{date_str}-{slugify(title)}.html"
    dest_path = REPLAYS_DIR / dest_name

    marker = REPLAYS_DIR / ".gitempty"
    if marker.exists():
        marker.unlink()

    shutil.copy2(source, dest_path)
    print(f"Replay:  replays/{dest_name}")

    if not no_summary:
        summary_path = generate_summary.write_summary(dest_path, title)
        print(f"Summary: summaries/{summary_path.name}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("source", help="Path to the source HTML replay file")
    parser.add_argument("--title", default=None, help="Conversation title")
    parser.add_argument("--date", default=str(date.today()), help="YYYY-MM-DD (default: today)")
    parser.add_argument("--no-summary", action="store_true", help="Skip summary generation")
    args = parser.parse_args()

    source = Path(args.source)
    if not source.exists():
        print(f"Error: not found: {source}", file=sys.stderr)
        sys.exit(1)

    archive(source, args.title, args.date, args.no_summary)


if __name__ == "__main__":
    main()
