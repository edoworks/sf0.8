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
QUEUE_TIMEOUT_SECONDS="${QUEUE_TIMEOUT_SECONDS:-60}"
NO_PROGRESS_SECONDS="${NO_PROGRESS_SECONDS:-600}"
POLL_SECONDS="${POLL_SECONDS:-30}"
DATE_BIN="${DATE_BIN:-date}"
SLEEP_BIN="${SLEEP_BIN:-sleep}"
GH_BIN="${GH_BIN:-gh}"

mkdir -p "$OUT_DIR"
OUT_FILE="$OUT_DIR/last-ci-result.txt"

resolve_run() {
  if [ -n "$RUN_ID" ]; then echo "$RUN_ID"; return; fi
  "$GH_BIN" run list --repo "$REPO" --branch main --limit 1 --json databaseId --jq '.[0].databaseId'
}

RUN_ID="$(resolve_run)"
[ -n "$RUN_ID" ] || { echo "no runs found for $REPO" >&2; exit 2; }

snapshot() {
  run_snapshot=$("$GH_BIN" run view "$RUN_ID" --repo "$REPO" --json status,conclusion,attempt,jobs \
    --jq '[.status, (.conclusion // ""), ([.jobs[]? | .name as $job | .steps[]? | select(.status=="in_progress") | "\($job):\(.name)"] | sort | join(", ")), ([.jobs[]? | .name as $job | .steps[]? | "\($job):\(.name)=\(.status)"] | sort | join(",")), (.attempt | tostring)] | join("\u001f")') \
    || { printf 'unknown\037\037\037\0370\037\0370\n'; return; }
  attempt=${run_snapshot##*$'\037'}
  queued_pages=$("$GH_BIN" api "repos/$REPO/actions/runs/$RUN_ID/attempts/$attempt/jobs?per_page=100" \
    --paginate \
    --jq '[.jobs[]? | select(.status=="queued" and ((.steps // []) | length)==0)] as $queued | select(($queued | length) > 0) | [($queued | map(.name) | sort | join(", ")), ($queued | map(.created_at | fromdateiso8601) | min | tostring)] | join("\u001f")') \
    || queued_pages=""
  queued_jobs=""
  queued_at_epoch=0
  while IFS=$'\037' read -r page_jobs page_epoch; do
    [ -n "$page_jobs" ] || continue
    queued_jobs="${queued_jobs:+$queued_jobs, }$page_jobs"
    if [ "$queued_at_epoch" -eq 0 ] || [ "$page_epoch" -lt "$queued_at_epoch" ]; then
      queued_at_epoch=$page_epoch
    fi
  done <<< "$queued_pages"
  queued_snapshot="$queued_jobs"$'\037'"$queued_at_epoch"
  printf '%s\037%s\n' "$run_snapshot" "$queued_snapshot"
}

initial_snapshot=$(snapshot)
initial_status=${initial_snapshot%%$'\037'*}
if [ "$REPO" = "edoworks/sf0.8" ] && [ "$initial_status" = "queued" ]; then
  "$SCRIPT_DIR/runner-readiness.sh" "${RUNNER_SERVICE_DIR:-$HOME/actions-runner-sf08}"
fi

started_at=$($DATE_BIN +%s)
deadline=$((started_at + TIMEOUT_MIN * 60))
last_progress_at=$started_at
last_signature=""
echo "watching $REPO run $RUN_ID (cap ${TIMEOUT_MIN}m)"

while :; do
  current_snapshot=$(snapshot)
  IFS=$'\037' read -r status conclusion active_step progress_signature attempt queued_jobs queued_at_epoch <<< "$current_snapshot"
  now=$($DATE_BIN +%s)
  signature="$status|$progress_signature"
  if [ "$signature" != "$last_signature" ]; then
    echo "state=$status step=${active_step:-none} elapsed_seconds=$((now - started_at))"
    last_signature="$signature"
    last_progress_at=$now
  fi
  {
    echo "repo=$REPO"
    echo "run=$RUN_ID"
    echo "checked_at=$($DATE_BIN -u +%FT%TZ)"
    echo "status=$status"
    echo "conclusion=$conclusion"
    echo "active_step=$active_step"
    echo "elapsed_seconds=$((now - started_at))"
  } > "$OUT_FILE.tmp"

  if [ "$status" = "completed" ]; then
    failed_steps=$("$GH_BIN" run view "$RUN_ID" --repo "$REPO" --json jobs --jq '[.jobs[].steps[] | select(.conclusion=="failure") | .name] | join(", ")' 2>/dev/null || echo "")
    echo "failed_steps=$failed_steps" >> "$OUT_FILE.tmp"
    mv "$OUT_FILE.tmp" "$OUT_FILE"
    cat "$OUT_FILE"
    [ "$conclusion" = "success" ] && exit 0 || exit 1
  fi

  if [ -n "$queued_jobs" ] && [[ "$queued_at_epoch" =~ ^[0-9]+$ ]] && [ "$queued_at_epoch" -gt 0 ]; then
    queue_age=$((now - queued_at_epoch))
  elif [ "$status" = "queued" ]; then
    queue_age=$((now - started_at))
  else
    queue_age=0
  fi
  if { [ -n "$queued_jobs" ] || [ "$status" = "queued" ]; } && [ "$queue_age" -ge "$QUEUE_TIMEOUT_SECONDS" ]; then
    echo "queue_timeout_seconds=$QUEUE_TIMEOUT_SECONDS" >> "$OUT_FILE.tmp"
    echo "queue_age_seconds=$queue_age" >> "$OUT_FILE.tmp"
    echo "queued_jobs=$queued_jobs" >> "$OUT_FILE.tmp"
    mv "$OUT_FILE.tmp" "$OUT_FILE"
    echo "BLOCKED: queued without execution for ${QUEUE_TIMEOUT_SECONDS}s" >&2
    cat "$OUT_FILE"
    exit 4
  fi

  if [ "$status" = "in_progress" ] && [ $((now - last_progress_at)) -ge "$NO_PROGRESS_SECONDS" ]; then
    echo "no_progress_seconds=$NO_PROGRESS_SECONDS" >> "$OUT_FILE.tmp"
    mv "$OUT_FILE.tmp" "$OUT_FILE"
    echo "BLOCKED: step '${active_step:-unknown}' made no observable transition for ${NO_PROGRESS_SECONDS}s" >&2
    cat "$OUT_FILE"
    exit 5
  fi

  if [ "$now" -ge "$deadline" ]; then
    echo "timeout_after=${TIMEOUT_MIN}m" >> "$OUT_FILE.tmp"
    mv "$OUT_FILE.tmp" "$OUT_FILE"
    echo "TIMEOUT waiting for $REPO run $RUN_ID" >&2
    cat "$OUT_FILE"
    exit 3
  fi
  "$SLEEP_BIN" "$POLL_SECONDS"
done
