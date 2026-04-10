#!/bin/bash
# Symlink Claude Code + Cowork skills dirs to the canonical RileyContext/skills.
# Run after a fresh install or when a new Cowork workspace appears.
set -e
CANON="$HOME/dev/RileyContext/skills"

link() {
  local target="$1"
  if [ -L "$target" ]; then
    [ "$(readlink "$target")" = "$CANON" ] && return 0
    rm "$target"
  elif [ -e "$target" ]; then
    local bak="${target}.bak.$(date +%s)"
    mv "$target" "$bak"
    echo "backed up existing $target -> $bak"
  fi
  mkdir -p "$(dirname "$target")"
  ln -s "$CANON" "$target"
  echo "linked $target"
}

# Claude Code
link "$HOME/.claude/skills"

# Cowork: link every workspace's skills-plugin dir
COWORK_ROOT="$HOME/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin"
if [ -d "$COWORK_ROOT" ]; then
  find "$COWORK_ROOT" -mindepth 3 -maxdepth 3 -type d -name skills 2>/dev/null | while read -r d; do
    link "$d"
  done
  # Also handle workspaces that don't yet have a skills subdir
  find "$COWORK_ROOT" -mindepth 2 -maxdepth 2 -type d 2>/dev/null | while read -r ws; do
    [ -e "$ws/skills" ] || link "$ws/skills"
  done
fi
