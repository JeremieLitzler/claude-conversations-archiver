# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Store Claude Code session replays (HTML) and their markdown summaries. Each summary links to its corresponding replay.

## Repository Structure

```
replays/    HTML replay files  (YYYY-MM-DD-slug.html)
summaries/  Markdown summaries (YYYY-MM-DD-slug.md)
scripts/    add_conversation.py, generate_summary.py
```

Both `replays/` and `summaries/` contain a `.gitempty` marker that is automatically deleted when the first file is added to that folder.

## Workflow

### All-in-one (recommended)

```bash
python scripts/save_session.py
```

Auto-discovers the most recent session, asks `claude -p` to generate a title, produces the HTML replay via `npx claude-replay`, and writes both the replay and summary.

To target a specific session, run `/status` inside Claude Code to get the session ID:

```bash
python scripts/save_session.py <session-id>
```

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--title` | auto-generated | Override the Claude-generated title |
| `--date` | today | Override date prefix (`YYYY-MM-DD`) |
| `--file` | — | Path to a specific session JSONL file |
| `--no-summary` | off | Skip summary generation |

### Step by step

If you already have the HTML replay file:

```bash
python scripts/add_conversation.py replay.html --title "Short descriptive title"
```

To regenerate a summary for a replay already in `replays/`:

```bash
python scripts/generate_summary.py replays/2026-06-03-my-session.html
```

## Scripts

### `scripts/save_session.py`
All-in-one entry point. Locates the session JSONL in `~/.claude/projects/`, runs `npx claude-replay` to produce the HTML, then delegates to `add_conversation.archive()`.

### `scripts/add_conversation.py`
Takes an existing HTML replay, copies it to `replays/`, and calls `generate_summary.write_summary()`. Exposes `archive()` for use by `save_session.py`.

### `scripts/generate_summary.py`
Extracts conversation text from a claude-replay HTML file and calls `claude -p` (Claude Code CLI) to produce a markdown summary. Extraction strategy:
1. Looks for embedded session JSON in `<script>` tags (claude-replay embeds data this way)
2. Falls back to stripping all HTML tags via stdlib `html.parser`

## Requirements

- Python 3.10+
- `claude` CLI in PATH (available when using Claude Code)
- No external packages — stdlib only
