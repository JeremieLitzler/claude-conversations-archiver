# claude-conversations

A personal archive of Claude Code sessions — each stored as an interactive HTML replay with a linked markdown summary.

## Prerequisites

- **Python 3.10+**
- **[Claude Code](https://claude.ai/code)** — provides the `claude` CLI used for summary generation
- **Node.js with npx** — used to run [claude-replay](https://skillsllm.com/skill/claude-replay) without a global install

## Setup

Clone the repository:

```bash
git clone https://github.com/JeremieLitzler/claude-conversations.git
cd claude-conversations
```

No dependencies to install — the scripts use Python stdlib only.

## Usage

### All-in-one (recommended)

```bash
python scripts/save_session.py
```

Auto-discovers the most recent Claude Code session, asks Claude to generate a title from the conversation, produces the HTML replay, and archives everything. To target a specific session, run `/status` inside Claude Code to get the session ID:

```bash
python scripts/save_session.py <session-id>
```

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--title` | auto-generated | Override the Claude-generated title |
| `--date` | today | Override the date prefix (`YYYY-MM-DD`) |
| `--file` | — | Path to a specific session JSONL file |
| `--no-summary` | off | Skip summary generation |

### Step by step

If you already have the HTML replay file:

```bash
python scripts/add_conversation.py replay.html --title "My session title"
```

To regenerate a summary for a replay already in `replays/`:

```bash
python scripts/generate_summary.py replays/2026-06-03-my-session.html
```
