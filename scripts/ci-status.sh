#!/usr/bin/env bash
# ci-status.sh — blocking CI result gate (recurrence guard for stuck watches).
#
# INC lesson (2026-09-13): a session treated an aborted `gh run watch` as
# evidence of state. This script waits for a run to reach a terminal state,
# captures the result to a file, and exits non-zero on failure. No CI claim
# may be made without this file existing (per handoff rule).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO="${1:-edoworks/sf0.8}"
RUN_ID="${2:-}"           # empty = latest run on main
OUT_DIR="${3:-docs/ci}"
TIMEOUT_MIN="${TIMEOUT_MIN:-35}"

mkdir -p "$OUT_DIR"
OUT_FILE="$OUT_DIR/last-ci-result.txt"

resolve_run() {
  if [ -n "$RUN_ID" ]; then echo "$RUN_ID"; return; fi
  gh run list --repo "$REPO" --branch main --limit 1 --json databaseId --jq '.[0].databaseId'
}

RUN_ID="$(resolve_run)"
[ -n "$RUN_ID" ] || { echo "no runs found for $REPO" >&2; exit 2; }

initial_status=$(gh run view "$RUN_ID" --repo "$REPO" --json status -q .status 2>/dev/null || echo "unknown")
if [ "$REPO" = "edoworks/sf0.8" ] && [ "$initial_status" = "queued" ]; then
  "$SCRIPT_DIR/runner-readiness.sh" "${RUNNER_SERVICE_DIR:-$HOME/actions-runner-sf08}"
fi

deadline=$(( $(date +%s) + TIMEOUT_MIN * 60 ))
echo "watching $REPO run $RUN_ID (cap ${TIMEOUT_MIN}m)"

while :; do
  status=$(gh run view "$RUN_ID" --repo "$REPO" --json status -q .status 2>/dev/null || echo "unknown")
  conclusion=$(gh run view "$RUN_ID" --repo "$REPO" --json conclusion -q .conclusion 2>/dev/null || echo "null")
  {
    echo "repo=$REPO"
    echo "run=$RUN_ID"
    echo "checked_at=$(date -u +%FT%TZ)"
    echo "status=$status"
    echo "conclusion=$conclusion"
  } > "$OUT_FILE.tmp"

  if [ "$status" = "completed" ]; then
    failed_steps=$(gh run view "$RUN_ID" --repo "$REPO" --json jobs --jq '[.jobs[].steps[] | select(.conclusion=="failure") | .name] | join(", ")' 2>/dev/null || echo "")
    echo "failed_steps=$failed_steps" >> "$OUT_FILE.tmp"
    mv "$OUT_FILE.tmp" "$OUT_FILE"
    cat "$OUT_FILE"
    [ "$conclusion" = "success" ] && exit 0 || exit 1
  fi

  if [ "$(date +%s)" -ge "$deadline" ]; then
    echo "timeout_after=${TIMEOUT_MIN}m" >> "$OUT_FILE.tmp"
    mv "$OUT_FILE.tmp" "$OUT_FILE"
    echo "TIMEOUT waiting for $REPO run $RUN_ID" >&2
    cat "$OUT_FILE"
    exit 3
  fi
  sleep 30
done
