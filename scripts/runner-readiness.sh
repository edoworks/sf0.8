#!/usr/bin/env bash
set -euo pipefail

RUNNER_ROOT="${1:-${RUNNER_SERVICE_DIR:-$HOME/actions-runner-sf08}}"
PGREP_BIN="${PGREP_BIN:-pgrep}"

if [ ! -x "$RUNNER_ROOT/svc.sh" ]; then
  echo "BLOCKED: runner service command is missing at $RUNNER_ROOT/svc.sh" >&2
  exit 2
fi

STATUS="$(cd "$RUNNER_ROOT" && ./svc.sh status)"
if ! grep -q "Started:" <<<"$STATUS"; then
  echo "BLOCKED: runner service is not started at $RUNNER_ROOT" >&2
  exit 3
fi

if ! "$PGREP_BIN" -f "$RUNNER_ROOT/bin/Runner.Listener" >/dev/null; then
  echo "BLOCKED: runner service has no active listener at $RUNNER_ROOT" >&2
  exit 4
fi

echo "READY: runner service and listener are active at $RUNNER_ROOT"
