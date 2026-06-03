Run the following command from the repository root to archive the current Claude Code session:

```bash
python scripts/save_session.py
```

This will:
1. Auto-discover the most recent session in ~/.claude/projects/
2. Generate a title using `claude -p`
3. Produce an HTML replay via `npx claude-replay`
4. Save the replay to replays/ and the summary to summaries/

Pass `--title "My title"` to override the auto-generated title, or `--no-summary` to skip summary generation.
