#!/usr/bin/env sh
# Link every skill in this repository into a Claude Code skills directory.
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

for skill in "$ROOT"/*/SKILL.md; do
  dir=$(dirname "$skill")
  name=$(basename "$dir")
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
