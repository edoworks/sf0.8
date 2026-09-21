#!/usr/bin/env bash
set -euo pipefail

# Restore opencode config from this repository to ~/.config/opencode
# Run from the sf0.8 repository root after cloning.

TARGET="${HOME}/.config/opencode"

if [ ! -d ".opencode-config" ]; then
  echo "ERROR: .opencode-config not found. Run from the sf0.8 repository root."
  exit 1
fi

echo "Restoring opencode config to ${TARGET}..."

mkdir -p "${TARGET}/commands" "${TARGET}/plugins" "${TARGET}/scripts"
mkdir -p "${TARGET}/skills/brb" "${TARGET}/skills/issue-tracking" "${TARGET}/skills/model-routing"
mkdir -p "${TARGET}/model-routing/incidents"

# Copy config files (preserve directory structure)
cp -R .opencode-config/* "${TARGET}/"

# Ensure node_modules exist for plugins
if [ ! -d "${TARGET}/node_modules" ]; then
  echo "Installing opencode config dependencies..."
  (cd "${TARGET}" && npm install)
fi

# Create factory-secrets directory placeholder (the actual ntfy_topic file
# must be manually restored or regenerated — it is not tracked here)
mkdir -p "${HOME}/factory-secrets"
if [ ! -f "${HOME}/factory-secrets/ntfy_topic" ]; then
  echo "WARNING: ${HOME}/factory-secrets/ntfy_topic is missing."
  echo "  Completion notifications will not work until it is restored."
  echo "  Create it with your ntfy topic name (mode 0400, owner-only)."
fi

echo "Done. Next steps:"
echo "  1. Restart opencode to load the restored config."
echo "  2. Run 'gh auth login' to restore GitHub credentials."
echo "  3. Run 'opencode debug config --pure' to verify config resolution."
echo "  4. Run 'python3 -m unittest tests/test_permission_policy.py' to verify permissions."
echo "  5. Read ~/.config/opencode/commands/continue-sf08.md for the restart sequence."