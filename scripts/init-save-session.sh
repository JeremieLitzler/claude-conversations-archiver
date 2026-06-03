#!/usr/bin/env bash
# Run from the root of your private repo to install the /save-session command.
# Usage: bash <submodule>/scripts/init-save-session.sh [submodule-name]
#
# The submodule name is auto-detected from the invocation path, so passing it
# explicitly is only needed when running with a non-standard invocation.
#
# Example:
#   bash archiver/scripts/init-save-session.sh

set -euo pipefail

SUBMODULE="${1:-$(dirname "$(dirname "$0")")}"

COMMAND_DIR=".claude/commands"
COMMAND_FILE="$COMMAND_DIR/save-session.md"

mkdir -p "$COMMAND_DIR"

cat > "$COMMAND_FILE" <<EOF
Run the following command from the repository root to archive the current Claude Code session:

\`\`\`bash
python $SUBMODULE/scripts/save_session.py
\`\`\`

This will:
1. Auto-discover the most recent session in ~/.claude/projects/
2. Generate a title using \`claude -p\`
3. Produce an HTML replay via \`npx claude-replay\`
4. Save the replay to replays/ and the summary to summaries/

Pass \`--title "My title"\` to override the auto-generated title, or \`--no-summary\` to skip summary generation.
EOF

echo "Created $COMMAND_FILE (submodule: $SUBMODULE)"
echo "Restart Claude Code and use /save-session to archive sessions."
