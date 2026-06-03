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

### 1. Generate the HTML replay

After completing a Claude Code session, use the [claude-replay](https://skillsllm.com/skill/claude-replay) skill:

```bash
claude-replay <session-id> -o replay.html
# or point directly at the session file:
claude-replay ~/.claude/projects/<project-hash>/<session-id>.jsonl -o replay.html
```

### 2. File it and generate the summary

```bash
python scripts/add_conversation.py replay.html --title "Short descriptive title"
```

This copies the HTML to `replays/`, calls `generate_summary.py` internally, and writes a markdown summary to `summaries/`. Both files share the same `YYYY-MM-DD-slug` stem derived from `--title` and today's date.

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--title` | filename stem | Human-readable title used for slug and summary heading |
| `--date` | today | Override date in `YYYY-MM-DD` format |
| `--no-summary` | off | Skip summary generation |

### 3. Generate a summary independently

If the replay is already in `replays/`:

```bash
python scripts/generate_summary.py replays/2026-06-03-my-session.html
```

## Scripts

### `scripts/add_conversation.py`
Main entry point. Copies the HTML replay into `replays/`, then delegates to `generate_summary.write_summary()`.

### `scripts/generate_summary.py`
Extracts conversation text from a claude-replay HTML file and calls `claude -p` (Claude Code CLI) to produce a markdown summary. Extraction strategy:
1. Looks for embedded session JSON in `<script>` tags (claude-replay embeds data this way)
2. Falls back to stripping all HTML tags via stdlib `html.parser`

## Requirements

- Python 3.10+
- `claude` CLI in PATH (available when using Claude Code)
- No external packages — stdlib only
