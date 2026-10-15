#!/usr/bin/env bash
# Install pstack (poteto's agent skills) and cursor-team-kit for OpenCode v2.
#
# Usage:
#   ./install.sh
#
# Overrides:
#   PSTACK_SKILLS_DIR      default ~/.agents/skills
#   OPENCODE_AGENTS_DIR    default ~/.config/opencode/agents
#   OPENCODE_COMMANDS_DIR  default ~/.config/opencode/commands
#   UPSTREAM_REF           default the pinned port commit (set "main" to attempt newest upstream)
#   UPSTREAM_REPO          default https://github.com/cursor/plugins.git
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
UPSTREAM_REPO="${UPSTREAM_REPO:-https://github.com/cursor/plugins.git}"
UPSTREAM_REF="${UPSTREAM_REF:-99743e9c151c8537cbbf1f98bb38f34ef3368453}"
SKILLS_DIR="${PSTACK_SKILLS_DIR:-$HOME/.agents/skills}"
AGENTS_DIR="${OPENCODE_AGENTS_DIR:-$HOME/.config/opencode/agents}"
COMMANDS_DIR="${OPENCODE_COMMANDS_DIR:-$HOME/.config/opencode/commands}"

need() {
  command -v "$1" >/dev/null 2>&1 || { echo "error: $1 is required" >&2; exit 1; }
}
need git
need python3
need node

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

echo "==> fetching $UPSTREAM_REPO ($UPSTREAM_REF)"
git clone --depth 1 "$UPSTREAM_REPO" "$tmp/plugins" >/dev/null 2>&1
if ! git -C "$tmp/plugins" cat-file -e "$UPSTREAM_REF^{commit}" 2>/dev/null; then
  git -C "$tmp/plugins" fetch --depth 1 origin "$UPSTREAM_REF" >/dev/null 2>&1 || {
    echo "error: cannot fetch ref $UPSTREAM_REF from $UPSTREAM_REPO" >&2; exit 1; }
  git -C "$tmp/plugins" checkout --detach FETCH_HEAD >/dev/null 2>&1
fi

echo "==> installing skills into $SKILLS_DIR"
mkdir -p "$SKILLS_DIR"
for src in "$tmp/plugins/pstack/skills"/*/ "$tmp/plugins/cursor-team-kit/skills"/*/; do
  name="$(basename "$src")"
  rm -rf "$SKILLS_DIR/$name"
  cp -R "$src" "$SKILLS_DIR/$name"
done

echo "==> vendoring the pstack guide"
GUIDE="$SKILLS_DIR/poteto-help/references/guide"
mkdir -p "$GUIDE"
cp -R "$tmp/plugins/pstack/docs/guide/." "$GUIDE/"
if ! grep -q "OpenCode note" "$GUIDE/README.md"; then
  cat "$REPO_DIR/files/guide-note.md" "$GUIDE/README.md" > "$GUIDE/README.md.new"
  mv "$GUIDE/README.md.new" "$GUIDE/README.md"
fi

echo "==> applying the OpenCode rewrites"
cp -R "$REPO_DIR/files/skills/." "$SKILLS_DIR/"
python3 "$REPO_DIR/patches/patches_a.py" "$SKILLS_DIR"
python3 "$REPO_DIR/patches/patches_b.py" "$SKILLS_DIR"

echo "==> installing subagents into $AGENTS_DIR"
mkdir -p "$AGENTS_DIR"
cp "$REPO_DIR"/files/agents/*.md "$AGENTS_DIR/"

echo "==> generating slash commands into $COMMANDS_DIR"
node "$REPO_DIR/commands/generate-commands.mjs" --skills-dir "$SKILLS_DIR" --out "$COMMANDS_DIR"

echo ""
echo "done."
echo "next:"
echo "  1. start a new OpenCode session (or run: opencode2 service restart)"
echo "  2. run /setup-pstack to map models onto the poteto-agent and poteto-judge subagents"
echo "  3. start a task with /poteto-mode"
