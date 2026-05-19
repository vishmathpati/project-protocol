#!/bin/bash
# Build script for project-protocol plugin
# Usage: ./build.sh
# Output:
#   dist/project-protocol-vX.Y.Z.zip         — FULL build (Claude Code + Codex)
#   dist/project-protocol-vX.Y.Z-cowork.zip  — STRIPPED build (Cowork only)
#
# Why two zips:
#   Cowork's validator rejects anything outside Anthropic's documented plugin
#   spec, so the Cowork zip ships a stripped shape (.claude-plugin + skills only,
#   no hooks, no templates, no codex sidecars). Claude Code and Codex tolerate
#   the stripped shape but lose value-adds: hooks, openai.yaml sidecars,
#   allowed-tools: frontmatter. The FULL zip keeps all of it for those tools.

set -e

PLUGIN_NAME="project-protocol"
VERSION=$(python3 -c "import sys,json; print(json.load(open('.claude-plugin/plugin.json'))['version'])")
OUTPUT_DIR="$(pwd)/dist"
OUTPUT_FULL="$OUTPUT_DIR/${PLUGIN_NAME}-v${VERSION}.zip"
OUTPUT_COWORK="$OUTPUT_DIR/${PLUGIN_NAME}-v${VERSION}-cowork.zip"

echo "→ Building ${PLUGIN_NAME} v${VERSION}..."

mkdir -p "$OUTPUT_DIR"

if [ -f "$OUTPUT_FULL" ] || [ -f "$OUTPUT_COWORK" ]; then
  echo "  ⚠️  One or both of these already exist:"
  echo "      $OUTPUT_FULL"
  echo "      $OUTPUT_COWORK"
  echo "      Delete them first or bump the version in .claude-plugin/plugin.json."
  exit 1
fi

# ──────────────────────────────────────────────────────────────────────────────
# Build 1 — FULL zip for Claude Code + Codex
# Includes:
#   .claude-plugin/plugin.json
#   .codex-plugin/plugin.json
#   hooks/
#   templates/
#   skills/<name>/SKILL.md           (allowed-tools: frontmatter intact)
#   skills/<name>/agents/openai.yaml (Codex sidecars)
#   skills/<name>/references/        (if present)
#   skills/<name>/examples/          (if present)
# ──────────────────────────────────────────────────────────────────────────────

STAGE_FULL=$(mktemp -d)

mkdir -p "$STAGE_FULL/.claude-plugin" "$STAGE_FULL/.codex-plugin" "$STAGE_FULL/skills"
cp .claude-plugin/plugin.json "$STAGE_FULL/.claude-plugin/"
cp .codex-plugin/plugin.json "$STAGE_FULL/.codex-plugin/"

if [ -d hooks ]; then
  cp -r hooks "$STAGE_FULL/"
fi

if [ -d templates ]; then
  cp -r templates "$STAGE_FULL/"
fi

# Copy skills as-is — preserve SKILL.md frontmatter, agents/openai.yaml,
# references/, examples/.
cp -r skills/* "$STAGE_FULL/skills/"

(cd "$STAGE_FULL" && zip -r "$OUTPUT_FULL" . -x "*.DS_Store" > /dev/null)
rm -rf "$STAGE_FULL"

echo "  ✅ Full build:   $OUTPUT_FULL"

# ──────────────────────────────────────────────────────────────────────────────
# Build 2 — COWORK zip (stripped to Anthropic's plugin spec)
# Includes:
#   .claude-plugin/plugin.json
#   skills/<name>/SKILL.md           (allowed-tools: stripped)
#   skills/<name>/references/        (if present)
#   skills/<name>/examples/          (if present)
# Excludes:
#   .codex-plugin/                   (not in spec)
#   hooks/                           (in spec, but none of Anthropic's Cowork
#                                     plugins ship hooks)
#   templates/                       (not a documented top-level dir)
#   skills/<name>/agents/            (Codex openai.yaml sidecars — not in spec)
# FUNDAMENTALS.md is relocated into skills/init-project/references/ so the
# init-project skill can still find it, and the staged SKILL.md is patched to
# point at the new path.
# ──────────────────────────────────────────────────────────────────────────────

STAGE_COWORK=$(mktemp -d)
trap "rm -rf '$STAGE_COWORK'" EXIT

mkdir -p "$STAGE_COWORK/.claude-plugin" "$STAGE_COWORK/skills"
cp .claude-plugin/plugin.json "$STAGE_COWORK/.claude-plugin/"

for skill_dir in skills/*/; do
  skill_name=$(basename "$skill_dir")
  mkdir -p "$STAGE_COWORK/skills/$skill_name"

  # SKILL.md with the allowed-tools: line stripped
  grep -v '^allowed-tools:' "$skill_dir/SKILL.md" > "$STAGE_COWORK/skills/$skill_name/SKILL.md"

  # Optional sub-folders Cowork accepts; skip agents/ (Codex-only)
  for sub in references examples; do
    if [ -d "$skill_dir$sub" ]; then
      cp -r "$skill_dir$sub" "$STAGE_COWORK/skills/$skill_name/"
    fi
  done
done

# Relocate FUNDAMENTALS.md into init-project/references and patch the path reference
if [ -f templates/FUNDAMENTALS.md ]; then
  mkdir -p "$STAGE_COWORK/skills/init-project/references"
  cp templates/FUNDAMENTALS.md "$STAGE_COWORK/skills/init-project/references/"
  if [ -f "$STAGE_COWORK/skills/init-project/SKILL.md" ]; then
    sed -i.bak 's|templates/FUNDAMENTALS.md|references/FUNDAMENTALS.md|g' \
      "$STAGE_COWORK/skills/init-project/SKILL.md"
    rm -f "$STAGE_COWORK/skills/init-project/SKILL.md.bak"
  fi
  # phase-4 reference also points at templates/FUNDAMENTALS.md
  if [ -f "$STAGE_COWORK/skills/init-project/references/phase-4-design-system.md" ]; then
    sed -i.bak 's|templates/FUNDAMENTALS.md|references/FUNDAMENTALS.md|g' \
      "$STAGE_COWORK/skills/init-project/references/phase-4-design-system.md"
    rm -f "$STAGE_COWORK/skills/init-project/references/phase-4-design-system.md.bak"
  fi
fi

# Relocate DESIGN.md template into init-project/references and patch the path reference
if [ -f templates/DESIGN.md ]; then
  mkdir -p "$STAGE_COWORK/skills/init-project/references"
  cp templates/DESIGN.md "$STAGE_COWORK/skills/init-project/references/"
  if [ -f "$STAGE_COWORK/skills/init-project/references/phase-4-design-system.md" ]; then
    sed -i.bak 's|templates/DESIGN.md|references/DESIGN.md|g' \
      "$STAGE_COWORK/skills/init-project/references/phase-4-design-system.md"
    rm -f "$STAGE_COWORK/skills/init-project/references/phase-4-design-system.md.bak"
  fi
fi

(cd "$STAGE_COWORK" && zip -r "$OUTPUT_COWORK" . -x "*.DS_Store" > /dev/null)

echo "  ✅ Cowork build: $OUTPUT_COWORK"

echo ""
echo "  Install:"
echo "    Cowork:      Drag $OUTPUT_COWORK into the Cowork chat"
echo "    Claude Code: claude plugin install \"$OUTPUT_FULL\""
echo "    Codex:       codex plugin install \"$OUTPUT_FULL\""
