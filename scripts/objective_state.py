#!/usr/bin/env python3
"""Evaluate objective-level completion separately from agent-run completion."""

from __future__ import annotations

from typing import Any


STAGES = (
    "IMPLEMENTATION",
    "LOCAL_VALIDATION",
    "BRANCH_PUSH",
    "PR",
    "REQUIRED_REVIEW",
    "MERGE",
    "DEPLOYMENT",
    "LIVE_HTTP_CHECK",
    "CANONICAL_ROUTING",
)

TERMINAL_STATES = {
    "OBJECTIVE_COMPLETE",
    "HUMAN_AUTHORIZATION_REQUIRED",
    "BLOCKED_AFTER_SELF_UNBLOCKING",
    "FAILED",
}


def evaluate(record: dict[str, Any]) -> dict[str, Any]:
    required = list(record.get("required_stages", []))
    if not required:
        required = list(STAGES) if record.get("external") else ["IMPLEMENTATION", "LOCAL_VALIDATION"]
    evidence = record.get("stage_evidence", {})
    missing = [stage for stage in required if evidence.get(stage, {}).get("status") != "VERIFIED"]
    declared = str(record.get("state", "")).strip()
    if declared in {"HUMAN_AUTHORIZATION_REQUIRED", "BLOCKED_AFTER_SELF_UNBLOCKING", "FAILED"}:
        return {"state": declared, "objective_complete": False, "missing_stages": missing, "errors": []}
    if missing:
        return {
            "state": "TASK_EXECUTION_COMPLETE" if record.get("task_execution_complete") else "NOT_DONE",
            "objective_complete": False,
            "missing_stages": missing,
            "errors": ["objective acceptance stages are incomplete"],
        }
    return {"state": "OBJECTIVE_COMPLETE", "objective_complete": True, "missing_stages": [], "errors": []}
