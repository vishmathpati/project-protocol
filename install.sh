#!/bin/bash
# project-protocol installer
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/vishmathpati/project-protocol/main/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/vishmathpati/project-protocol/main/install.sh | bash -s -- --cowork
#   INSTALL_FLAVOR=cowork curl -fsSL ... | bash
#
# Flavors:
#   FULL    (default) — Claude Code + Codex. Ships hooks, templates, .codex-plugin sidecars.
#   COWORK  (--cowork or INSTALL_FLAVOR=cowork) — Cowork-compatible stripped build.

set -e

REPO="vishmathpati/project-protocol"
PLUGIN_NAME="project-protocol"
TMP_DIR=$(mktemp -d)

# Flavor detection: --cowork flag wins over $INSTALL_FLAVOR; default is FULL.
FLAVOR="${INSTALL_FLAVOR:-full}"
for arg in "$@"; do
  case "$arg" in
    --cowork) FLAVOR="cowork" ;;
    --full)   FLAVOR="full" ;;
  esac
done

cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

echo "→ Installing ${PLUGIN_NAME} (${FLAVOR})..."

# Fetch latest release version from GitHub API
LATEST=$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" \
  | grep '"tag_name"' | sed -E 's/.*"tag_name": "v?([^"]+)".*/\1/')

if [ -z "$LATEST" ]; then
  echo "  ✗ Could not fetch latest release. Check your internet connection."
  exit 1
fi

echo "  Latest version: v${LATEST}"

# Resolve asset filename based on flavor
if [ "$FLAVOR" = "cowork" ]; then
  ASSET_NAME="${PLUGIN_NAME}-v${LATEST}-cowork.zip"
else
  ASSET_NAME="${PLUGIN_NAME}-v${LATEST}.zip"
fi

DOWNLOAD_URL="https://github.com/${REPO}/releases/download/v${LATEST}/${ASSET_NAME}"
PLUGIN_PATH="${TMP_DIR}/${ASSET_NAME}"

echo "  Downloading..."
curl -fsSL -o "$PLUGIN_PATH" "$DOWNLOAD_URL"

if [ "$FLAVOR" = "cowork" ]; then
  # Cowork has no CLI install path — save the zip and tell the user to drag it in.
  DEST="$HOME/Downloads/${ASSET_NAME}"
  cp "$PLUGIN_PATH" "$DEST"
  echo "  ✅ Cowork build downloaded (v${LATEST})"
  echo ""
  echo "  Drag this file into Cowork: $DEST"
elif command -v claude &> /dev/null; then
  claude plugin install "$PLUGIN_PATH"
  echo "  ✅ Installed into Claude Code (v${LATEST})"
  echo ""
  echo "  To use: open any project in Claude Code and say \"init project\""
else
  # Claude Code not found — save to Downloads as fallback
  DEST="$HOME/Downloads/${ASSET_NAME}"
  cp "$PLUGIN_PATH" "$DEST"
  echo "  ⚠️  Claude Code not found in PATH."
  echo "  Plugin saved to: $DEST"
  echo ""
  echo "  To install manually:"
  echo "    Claude Code: claude plugin install \"$DEST\""
  echo "    Codex:       add the repo as a marketplace — Codex has no zip-install path (see README Codex section)"
  echo "    Cowork:      re-run with the --cowork flag to get the Cowork-compatible build:"
  echo "                 curl -fsSL https://raw.githubusercontent.com/${REPO}/main/install.sh | bash -s -- --cowork"
fi
