#!/usr/bin/env bash
# ledger.sh — factory telemetry ledger (disposable SQLite cache).
#
# Invariant: deleting factory.sqlite must never change product intent; this
# stores runs/costs only. Rebuildable from forge + run records.
set -euo pipefail
DB="${FACTORY_DB:-.factory/factory.sqlite}"
SCHEMA="$(dirname "$0")/../.factory/schema.sql"

init() { sqlite3 "$DB" < "$SCHEMA"; }

cmd="${1:-help}"; shift || true
case "$cmd" in
  init) init; echo "ledger ready: $DB" ;;
  start)
    # start <repo> <task_kind> <agent_route> [notes]
    repo="$1"; kind="$2"; route="$3"; notes="${4:-}"
    init >/dev/null
    id=$(uuidgen | tr 'A-Z' 'a-z')
    sqlite3 "$DB" "INSERT INTO runs(id,repo,task_kind,agent_route,started_at,notes) VALUES('$id','$repo','$kind','$route','$(date -u +%FT%TZ)','${notes//\'/\'\'}');"
    echo "$id"
    ;;
  finish)
    # finish <run_id> <outcome> <verification> [attempts]
    id="$1"; outcome="$2"; verification="${3:-}"; attempts="${4:-1}"
    sqlite3 "$DB" "UPDATE runs SET finished_at='$(date -u +%FT%TZ)', outcome='$outcome', verification='$verification', attempts=$attempts WHERE id='$id';"
    ;;
  cost)
    # cost <run_id> <usd> [tokens]
    id="$1"; usd="$2"; tokens="${3:-0}"
    sqlite3 "$DB" "INSERT INTO costs(run_id,usd,tokens,recorded_at) VALUES('$id',$usd,$tokens,'$(date -u +%FT%TZ)');"
    ;;
  report)
    sqlite3 -header -column "$DB" "
      SELECT repo, task_kind, agent_route, outcome, attempts, verification,
             substr(started_at,1,10) AS day FROM runs ORDER BY started_at DESC LIMIT 25;
      SELECT 'total_usd', round(coalesce(sum(usd),0),4) FROM costs;"
    ;;
  *) echo "usage: ledger.sh init|start|finish|cost|report" >&2; exit 2 ;;
esac
