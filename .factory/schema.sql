-- Factory telemetry ledger: disposable cache of runs and costs.
-- Disposability invariant (design review): deleting factory.sqlite must never
-- change what the product is supposed to do. PRDs/policies/handoffs live in Git.
-- Schema version 1. Rebuildable from forge + run records at any time.

CREATE TABLE IF NOT EXISTS runs (
  id            TEXT PRIMARY KEY,          -- uuid
  repo          TEXT NOT NULL,             -- edoworks/product-a | edoworks/sf0.8
  task_kind     TEXT NOT NULL,             -- feature | fix | factory | research
  agent_route   TEXT NOT NULL,             -- primary | fallback
  started_at    TEXT NOT NULL,             -- iso8601
  finished_at   TEXT,
  outcome       TEXT,                      -- success | failed | escalated | bypassed
  attempts      INTEGER DEFAULT 1,
  verification  TEXT,                      -- test_succeeded | verify_failed | human_confirmed
  notes         TEXT
);

CREATE TABLE IF NOT EXISTS costs (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id        TEXT NOT NULL REFERENCES runs(id),
  usd           REAL NOT NULL DEFAULT 0,
  tokens        INTEGER,
  recorded_at   TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_runs_repo_started ON runs(repo, started_at);
CREATE INDEX IF NOT EXISTS idx_costs_run ON costs(run_id);
