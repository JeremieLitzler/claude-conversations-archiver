#!/usr/bin/env python3
"""Generate a markdown summary from a claude-replay HTML file.

Usage:
    python scripts/generate_summary.py <replay_html>

The replay HTML should already be in replays/. The summary is written to
summaries/<same_stem>.md with a relative link back to the replay.
Requires the `claude` CLI in PATH (provided by Claude Code).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SUMMARIES_DIR = REPO_ROOT / "summaries"

SUMMARY_PROMPT = (
    "Summarize this Claude Code session in markdown. "
    "Include: a one-sentence overview, key topics/tasks as bullet points, "
    "and any notable outputs or decisions. Under 300 words. No top-level heading."
)


class _TextExtractor(HTMLParser):
    """Strip HTML tags, skipping <script> and <style> blocks."""

    _SKIP = {"script", "style"}

    def __init__(self) -> None:
        super().__init__()
        self._depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: object) -> None:
        if tag in self._SKIP:
            self._depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIP:
            self._depth = max(0, self._depth - 1)

    def handle_data(self, data: str) -> None:
        if self._depth == 0:
            stripped = data.strip()
            if stripped:
                self.parts.append(stripped)

    def get_text(self) -> str:
        return "\n".join(self.parts)


def _try_extract_json(html: str) -> list[dict] | None:
    """Try to pull embedded session JSON from a claude-replay HTML file."""
    patterns = [
        r'(?:const|var|let)\s+sessionData\s*=\s*(\[[\s\S]*?\]);',
        r'window\.__SESSION__\s*=\s*(\[[\s\S]*?\]);',
        r'window\.__DATA__\s*=\s*(\{[\s\S]*?\});',
    ]
    for pat in patterns:
        m = re.search(pat, html)
        if m:
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError:
                pass
    return None


def _format_turns(session: list[dict]) -> str:
    lines = []
    for entry in session:
        role = (entry.get("role") or entry.get("type") or "").upper()
        content = entry.get("content") or entry.get("message") or ""
        if isinstance(content, list):
            content = " ".join(
                b.get("text", "") for b in content
                if isinstance(b, dict) and b.get("type") == "text"
            )
        if role and str(content).strip():
            lines.append(f"[{role}]\n{str(content).strip()}")
    return "\n\n".join(lines)


def extract_conversation(html_path: Path) -> str:
    html = html_path.read_text(encoding="utf-8")

    session = _try_extract_json(html)
    if isinstance(session, list):
        text = _format_turns(session)
        if text.strip():
            return text

    extractor = _TextExtractor()
    extractor.feed(html)
    return extractor.get_text()


def _call_claude(conversation_text: str) -> str:
    full_prompt = f"{SUMMARY_PROMPT}\n\n---\n\n{conversation_text[:12000]}"
    result = subprocess.run(
        ["claude", "-p", full_prompt],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude CLI failed: {result.stderr.strip()}")
    return result.stdout.strip()


def write_summary(replay_path: Path, title: str | None = None) -> Path:
    stem = replay_path.stem
    display_title = title or stem
    summary_path = SUMMARIES_DIR / f"{stem}.md"

    conversation_text = extract_conversation(replay_path)
    summary_body = _call_claude(conversation_text)

    marker = SUMMARIES_DIR / ".gitempty"
    if marker.exists():
        marker.unlink()

    content = (
        f"# {display_title}\n\n"
        f"[View replay](../replays/{replay_path.name})\n\n"
        f"{summary_body}\n"
    )
    summary_path.write_text(content, encoding="utf-8")
    return summary_path


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: python {Path(__file__).name} <replay_html>", file=sys.stderr)
        sys.exit(1)

    replay_path = Path(sys.argv[1]).resolve()
    if not replay_path.exists():
        print(f"Error: not found: {replay_path}", file=sys.stderr)
        sys.exit(1)

    summary_path = write_summary(replay_path)
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
