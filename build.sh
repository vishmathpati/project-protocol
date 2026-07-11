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

# Stage dirs for both builds. Hoisted here so a single EXIT trap covers any
# failure path (set -e mid-build, mid-zip, anywhere). Without this, an early
# exit during the full build would leak STAGE_FULL.
STAGE_FULL=$(mktemp -d)
STAGE_COWORK=$(mktemp -d)
trap "rm -rf '$STAGE_FULL' '$STAGE_COWORK'" EXIT

# ──────────────────────────────────────────────────────────────────────────────
# Build 1 — FULL zip for Claude Code + Codex
# Includes:
#   .claude-plugin/plugin.json
#   .codex-plugin/plugin.json
#   hooks/
#   templates/
#   aside-skill/                     (standalone skills the user uploads to Aside)
#   skills/<name>/SKILL.md           (allowed-tools: frontmatter intact)
#   skills/<name>/agents/openai.yaml (Codex sidecars)
#   skills/<name>/references/        (if present)
#   skills/<name>/examples/          (if present)
# ──────────────────────────────────────────────────────────────────────────────

mkdir -p "$STAGE_FULL/.claude-plugin" "$STAGE_FULL/.codex-plugin" "$STAGE_FULL/skills"
cp .claude-plugin/plugin.json "$STAGE_FULL/.claude-plugin/"
cp .codex-plugin/plugin.json "$STAGE_FULL/.codex-plugin/"

if [ -d hooks ]; then
  cp -r hooks "$STAGE_FULL/"
fi

if [ -d templates ]; then
  cp -r templates "$STAGE_FULL/"
fi

# Standalone Aside skills — shipped so `calibrate` can point users at the file to
# upload into the Aside browser. NOT loaded as a Claude/Codex skill (lives outside skills/).
if [ -d aside-skill ]; then
  cp -r aside-skill "$STAGE_FULL/"
fi

# Copy skills as-is — preserve SKILL.md frontmatter, agents/openai.yaml,
# references/, examples/.
cp -r skills/* "$STAGE_FULL/skills/"

(cd "$STAGE_FULL" && zip -r "$OUTPUT_FULL" . -x "*.DS_Store" > /dev/null)

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
# templates/ is relocated into the relevant skill's references/ folder so each
# skill can still find its template, and the staged SKILL.md / references/*.md
# are sed-patched to point at the new path. Relocations:
#   templates/FUNDAMENTALS.md → skills/init-project/references/
#   templates/DESIGN.md       → skills/init-project/references/
#   templates/TOOLING.md      → skills/init-project/references/
#   templates/STRUCTURE.md    → skills/build-component/references/
#   templates/CONTENT.md      → skills/marketing-brief/references/
# ──────────────────────────────────────────────────────────────────────────────

mkdir -p "$STAGE_COWORK/.claude-plugin" "$STAGE_COWORK/skills"
cp .claude-plugin/plugin.json "$STAGE_COWORK/.claude-plugin/"

# Rename the Cowork build to a distinct plugin identity so Claude Desktop
# treats it as a separate plugin from the FULL build (which keeps the original
# project-protocol name). Without this, both builds share the same logical
# plugin ID in the desktop app and enable/disable becomes coupled across
# Cowork and Claude Code. The Cowork zip becomes "project-protocol-cowork".
# Skill namespace also changes accordingly (project-protocol-cowork:save-session).
python3 -c "
import json
p = '$STAGE_COWORK/.claude-plugin/plugin.json'
d = json.load(open(p))
d['name'] = 'project-protocol-cowork'
d['description'] = 'Cowork build of project-protocol. ' + d['description']
json.dump(d, open(p, 'w'), indent=2)
print('  ↳ Renamed Cowork plugin to:', d['name'])
"

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
  # phase-0c-modernize also references templates/DESIGN.md
  if [ -f "$STAGE_COWORK/skills/init-project/references/phase-0c-modernize.md" ]; then
    sed -i.bak 's|templates/DESIGN.md|references/DESIGN.md|g' \
      "$STAGE_COWORK/skills/init-project/references/phase-0c-modernize.md"
    rm -f "$STAGE_COWORK/skills/init-project/references/phase-0c-modernize.md.bak"
  fi
fi

# Relocate TOOLING.md into init-project/references and patch the path references.
# Without this, Node projects via Cowork fail Phase 4 — the skill tries to cp
# from ${CLAUDE_PLUGIN_ROOT}/templates/TOOLING.md, which doesn't exist in the
# Cowork build because templates/ is stripped.
if [ -f templates/TOOLING.md ]; then
  mkdir -p "$STAGE_COWORK/skills/init-project/references"
  cp templates/TOOLING.md "$STAGE_COWORK/skills/init-project/references/"
  if [ -f "$STAGE_COWORK/skills/init-project/SKILL.md" ]; then
    sed -i.bak 's|templates/TOOLING.md|references/TOOLING.md|g' \
      "$STAGE_COWORK/skills/init-project/SKILL.md"
    rm -f "$STAGE_COWORK/skills/init-project/SKILL.md.bak"
  fi
  if [ -f "$STAGE_COWORK/skills/init-project/references/phase-4-design-system.md" ]; then
    sed -i.bak 's|templates/TOOLING.md|references/TOOLING.md|g' \
      "$STAGE_COWORK/skills/init-project/references/phase-4-design-system.md"
    rm -f "$STAGE_COWORK/skills/init-project/references/phase-4-design-system.md.bak"
  fi
  if [ -f "$STAGE_COWORK/skills/init-project/references/phase-0c-modernize.md" ]; then
    sed -i.bak 's|templates/TOOLING.md|references/TOOLING.md|g' \
      "$STAGE_COWORK/skills/init-project/references/phase-0c-modernize.md"
    rm -f "$STAGE_COWORK/skills/init-project/references/phase-0c-modernize.md.bak"
  fi
fi

# Relocate STRUCTURE.md into build-component/references. No current skill docs
# reference it via the `templates/` prefix (build-component generates STRUCTURE.md
# inline), but ship it alongside the skill so build-component can cp it if needed.
# Defensive sed in case future references appear.
if [ -f templates/STRUCTURE.md ]; then
  mkdir -p "$STAGE_COWORK/skills/build-component/references"
  cp templates/STRUCTURE.md "$STAGE_COWORK/skills/build-component/references/"
  if [ -f "$STAGE_COWORK/skills/build-component/SKILL.md" ]; then
    sed -i.bak 's|templates/STRUCTURE.md|references/STRUCTURE.md|g' \
      "$STAGE_COWORK/skills/build-component/SKILL.md"
    rm -f "$STAGE_COWORK/skills/build-component/SKILL.md.bak"
  fi
  if [ -d "$STAGE_COWORK/skills/build-component/references" ]; then
    find "$STAGE_COWORK/skills/build-component/references" -type f -name '*.md' \
      ! -name 'STRUCTURE.md' -exec sed -i.bak \
      's|templates/STRUCTURE.md|references/STRUCTURE.md|g' {} \;
    find "$STAGE_COWORK/skills/build-component/references" -type f -name '*.md.bak' -delete
  fi
fi

# Relocate CONTENT.md into marketing-brief/references. Same reasoning as
# STRUCTURE.md: nothing currently references it via the `templates/` prefix
# (marketing-brief writes CONTENT.md from inlined shape), but ship it next to
# the skill so the template scaffold is available. Defensive sed for the future.
if [ -f templates/CONTENT.md ]; then
  mkdir -p "$STAGE_COWORK/skills/marketing-brief/references"
  cp templates/CONTENT.md "$STAGE_COWORK/skills/marketing-brief/references/"
  if [ -f "$STAGE_COWORK/skills/marketing-brief/SKILL.md" ]; then
    sed -i.bak 's|templates/CONTENT.md|references/CONTENT.md|g' \
      "$STAGE_COWORK/skills/marketing-brief/SKILL.md"
    rm -f "$STAGE_COWORK/skills/marketing-brief/SKILL.md.bak"
  fi
  if [ -d "$STAGE_COWORK/skills/marketing-brief/references" ]; then
    find "$STAGE_COWORK/skills/marketing-brief/references" -type f -name '*.md' \
      ! -name 'CONTENT.md' -exec sed -i.bak \
      's|templates/CONTENT.md|references/CONTENT.md|g' {} \;
    find "$STAGE_COWORK/skills/marketing-brief/references" -type f -name '*.md.bak' -delete
  fi
fi

# Ship the standalone Aside skills in the Cowork build too — same deliverable the
# user uploads to Aside regardless of which tool drives the plugin.
if [ -d aside-skill ]; then
  cp -r aside-skill "$STAGE_COWORK/"
fi

(cd "$STAGE_COWORK" && zip -r "$OUTPUT_COWORK" . -x "*.DS_Store" > /dev/null)

echo "  ✅ Cowork build: $OUTPUT_COWORK"

echo ""
echo "  Install:"
echo "    Cowork:      Drag $OUTPUT_COWORK into the Cowork chat"
echo "    Claude Code: claude plugin install \"$OUTPUT_FULL\""
echo "    Codex:       codex plugin install \"$OUTPUT_FULL\""
