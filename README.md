# claude-conversations

A personal archive of Claude Code sessions — each stored as an interactive HTML replay with a linked markdown summary.

## Prerequisites

- **Python 3.10+**
- **[Claude Code](https://claude.ai/code)** — provides the `claude` CLI used for summary generation
- **[claude-replay](https://skillsllm.com/skill/claude-replay)** — converts session files into self-contained HTML replays

### Install claude-replay

Follow the instructions on the [claude-replay skill page](https://skillsllm.com/skill/claude-replay). Once installed, verify it is available:

```bash
claude-replay --version
```

## Setup

Clone the repository:

```bash
git clone https://github.com/JeremieLitzler/claude-conversations.git
cd claude-conversations
```

No dependencies to install — the scripts use Python stdlib only.

## Usage

### 1. Generate the HTML replay

After completing a Claude Code session, run `claude-replay` to export it:

```bash
# By session ID (auto-discovered):
claude-replay <session-id> -o replay.html

# Or point directly at the session file:
claude-replay ~/.claude/projects/<project-hash>/<session-id>.jsonl -o replay.html
```

### 2. Archive the conversation

```bash
python scripts/add_conversation.py replay.html --title "Short descriptive title"
```

This will:
- Copy the HTML to `replays/YYYY-MM-DD-slug.html`
- Generate a markdown summary and write it to `summaries/YYYY-MM-DD-slug.md`
- The summary includes a link to the replay file

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--title` | filename stem | Title used as the summary heading and to derive the filename slug |
| `--date` | today | Override the date prefix (`YYYY-MM-DD`) |
| `--no-summary` | off | Copy the replay without generating a summary |

### Regenerate a summary

If the replay is already in `replays/` and you want to regenerate its summary:

```bash
python scripts/generate_summary.py replays/2026-06-03-my-session.html
```
