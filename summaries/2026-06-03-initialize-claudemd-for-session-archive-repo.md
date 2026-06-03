# Initialize CLAUDE.md for session archive repo

[View replay](../replays/2026-06-03-initialize-claudemd-for-session-archive-repo.html)

**Session focused on initializing the `claude-conversations` repository structure and tooling for archiving Claude Code session replays.**

- Created the repository layout: `replays/`, `summaries/`, and `scripts/` directories with `.gitempty` placeholder files
- Wrote `scripts/add_conversation.py` to copy an HTML replay into `replays/` and trigger summary generation
- Wrote `scripts/generate_summary.py` to extract conversation text from a `claude-replay` HTML file and call `claude -p` to produce a markdown summary; extraction tries embedded JSON first, falls back to HTML stripping
- Wrote `scripts/save_session.py` as the all-in-one entry point: auto-discovers the most recent session JSONL in `~/.claude/projects/`, calls `npx claude-replay` to produce the HTML, then delegates to `add_conversation.archive()`
- Updated `CLAUDE.md` with full workflow documentation, script descriptions, and a table of CLI flags
- Updated `README.md` to reflect the finalized project purpose and usage
- Fixed `save_session.py` to invoke `claude-replay` via `npx` rather than a direct binary call, resolving a PATH issue on Windows
- Committed the initial structure in two commits: "Initialize repository structure and archiving scripts" and "Use npx to invoke claude-replay"

**Notable decisions:**
- No external Python dependencies â€” stdlib only (`html.parser`, `subprocess`, `pathlib`, etc.)
- Summary generation delegates to `claude -p` so the summary quality benefits from the full Claude model rather than a local heuristic
- `save_session.py` supports `--title`, `--date`, `--file`, and `--no-summary` flags for flexibility without breaking the simple default flow
