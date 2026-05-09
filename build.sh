#!/bin/bash
# Build script for project-protocol plugin
# Usage: ./build.sh
# Output: dist/project-protocol-vX.Y.Z.plugin

set -e

PLUGIN_NAME="project-protocol"
VERSION=$(python3 -c "import sys,json; print(json.load(open('.claude-plugin/plugin.json'))['version'])")
OUTPUT_DIR="$(pwd)/dist"
OUTPUT="$OUTPUT_DIR/${PLUGIN_NAME}-v${VERSION}.plugin"

echo "→ Building ${PLUGIN_NAME} v${VERSION}..."

mkdir -p "$OUTPUT_DIR"

# Bail if output already exists
if [ -f "$OUTPUT" ]; then
  echo "  ⚠️  $OUTPUT already exists — delete it first or bump the version in .claude-plugin/plugin.json"
  exit 1
fi

# Create temp staging dir
STAGE=$(mktemp -d)
trap "rm -rf $STAGE" EXIT

# Copy plugin structure into staging
mkdir -p "$STAGE/.claude-plugin" "$STAGE/hooks" "$STAGE/templates"

cp .claude-plugin/plugin.json "$STAGE/.claude-plugin/"
cp -r skills/ "$STAGE/skills/"
cp hooks/hooks.json "$STAGE/hooks/"
cp hooks/session-start-context.md "$STAGE/hooks/"
cp templates/FUNDAMENTALS.md "$STAGE/templates/"

# Zip it
cd "$STAGE"
zip -r "$OUTPUT" . -x "*.DS_Store" > /dev/null

echo "  ✅ Done: $OUTPUT"
echo ""
echo "  Install:"
echo "    Cowork:      Drag the .plugin file into the Cowork chat"
echo "    Claude Code: claude plugin install \"$OUTPUT\""
