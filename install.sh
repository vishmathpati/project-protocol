#!/bin/bash
# project-protocol installer
# Usage: curl -fsSL https://raw.githubusercontent.com/vishmathpati/project-protocol/main/install.sh | bash

set -e

REPO="vishmathpati/project-protocol"
PLUGIN_NAME="project-protocol"
TMP_DIR=$(mktemp -d)

cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

echo "→ Installing ${PLUGIN_NAME}..."

# Fetch latest release version from GitHub API
LATEST=$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" \
  | grep '"tag_name"' | sed -E 's/.*"tag_name": "v?([^"]+)".*/\1/')

if [ -z "$LATEST" ]; then
  echo "  ✗ Could not fetch latest release. Check your internet connection."
  exit 1
fi

echo "  Latest version: v${LATEST}"

# Download the plugin
DOWNLOAD_URL="https://github.com/${REPO}/releases/download/v${LATEST}/${PLUGIN_NAME}-v${LATEST}.zip"
PLUGIN_PATH="${TMP_DIR}/${PLUGIN_NAME}-v${LATEST}.zip"

echo "  Downloading..."
curl -fsSL -o "$PLUGIN_PATH" "$DOWNLOAD_URL"

# Install into Claude Code if available
if command -v claude &> /dev/null; then
  claude plugin install "$PLUGIN_PATH"
  echo "  ✅ Installed into Claude Code (v${LATEST})"
  echo ""
  echo "  To use: open any project in Claude Code and say \"init project\""
else
  # Claude Code not found — save to Downloads as fallback
  DEST="$HOME/Downloads/${PLUGIN_NAME}-v${LATEST}.zip"
  cp "$PLUGIN_PATH" "$DEST"
  echo "  ⚠️  Claude Code not found in PATH."
  echo "  Plugin saved to: $DEST"
  echo ""
  echo "  To install manually:"
  echo "    Claude Code: claude plugin install \"$DEST\""
  echo "    Cowork:      Drag the file into the Cowork chat window"
fi
