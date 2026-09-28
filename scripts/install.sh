#!/usr/bin/env sh
# Link the active skills of this repository into a Claude Code skills directory.
#
#   sh scripts/install.sh                  -> ~/.claude/skills   (all projects)
#   sh scripts/install.sh ./.claude/skills -> one project only
#
# Links, not copies: `git pull` in this repo updates every installed skill.
# An existing folder with the same name is left alone and reported.
set -eu

ROOT=$(cd "$(dirname "$0")/.." && pwd)
TARGET=${1:-"$HOME/.claude/skills"}
mkdir -p "$TARGET"

# Only the active set from .claude-plugin/plugin.json; a hub's spokes load through that hub.
# Entries are ./<hub> or ./<realm>/<skill>; the link is named for the skill folder alone.
ACTIVE=$(grep -o '"\./[a-z0-9/-]*"' "$ROOT/.claude-plugin/plugin.json" | tr -d '"' | sed 's#^\./##')

for rel in $ACTIVE; do
  name=$(basename "$rel")
  dir="$ROOT/$rel"
  dest="$TARGET/$name"
  if [ -L "$dest" ]; then
    rm "$dest"
  elif [ -e "$dest" ]; then
    echo "skip  $name (already exists and is not a link)"
    continue
  fi
  ln -s "$dir" "$dest"
  echo "link  $name"
done
