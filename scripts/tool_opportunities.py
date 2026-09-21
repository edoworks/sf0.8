#!/usr/bin/env python3
"""Validate and triage evidence-backed gold and shovel opportunity signals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = ROOT / ".factory" / "tool-opportunity-ledger.json"

CLASSIFICATIONS = {"GOLD", "SHOVEL", "INTERNAL_INFRASTRUCTURE", "NOISE"}
LIFECYCLES = {"REUSE", "WATCH", "VALIDATE", "PROTOTYPE", "STOP", "ARCHIVE"}
STAGES = {
    "SIGNAL",
    "REPETITION",
    "REUSE",
    "EXTERNAL_EVIDENCE",
    "ECONOMIC_EVIDENCE",
    "PRODUCT_HYPOTHESIS",
    "VALIDATION",
}
EVIDENCE_KINDS = {"FACT", "EVIDENCE", "INFERENCE", "ASSUMPTION", "HYPOTHESIS", "UNKNOWN"}
EXTERNAL_STATES = {"ABSENT", "UNKNOWN", "PRESENT", "CONFLICTING"}

REQUIRED_CANDIDATE_FIELDS = {
    "id",
    "title",
    "classification",
    "lifecycle",
    "stage",
    "signal_type",
    "problem",
    "origin",
    "observed_at",
    "frequency",
    "severity",
    "cost",
    "workaround",
    "internal_solution",
    "reusability",
    "external_evidence",
    "economic_evidence",
    "confidence",
    "provenance",
    "next_validation_action",
    "stop_condition",
}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _evidence_errors(value: Any, prefix: str) -> list[str]:
    if not isinstance(value, list) or not value:
        return [f"{prefix} must be a non-empty list"]
    errors: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{prefix}[{index}] must be an object")
            continue
        if item.get("kind") not in EVIDENCE_KINDS:
            errors.append(f"{prefix}[{index}].kind is invalid")
        if not _nonempty(item.get("claim")) or not _nonempty(item.get("source")):
            errors.append(f"{prefix}[{index}] requires claim and source")
    return errors


def validate_candidate(candidate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_CANDIDATE_FIELDS - candidate.keys())
    errors.extend(f"missing {field}" for field in missing)
    if missing:
        return errors
    if not _nonempty(candidate["id"]) or not _nonempty(candidate["title"]):
        errors.append("id and title must be non-empty")
    if candidate["classification"] not in CLASSIFICATIONS:
        errors.append("classification is invalid")
    if candidate["lifecycle"] not in LIFECYCLES:
        errors.append("lifecycle is invalid")
    if candidate["stage"] not in STAGES:
        errors.append("stage is invalid")
    if not _nonempty(candidate["signal_type"]):
        errors.append("signal_type must be non-empty")
    if not _nonempty(candidate["observed_at"]):
        errors.append("observed_at must be non-empty")
    frequency = candidate["frequency"]
    if not isinstance(frequency, dict) or not isinstance(frequency.get("count"), int) or frequency["count"] < 1:
        errors.append("frequency.count must be a positive integer")
    elif frequency["count"] >= 3 and candidate["stage"] == "SIGNAL":
        errors.append("repeated signals must advance beyond SIGNAL")
    if not isinstance(candidate["cost"], dict):
        errors.append("cost must be an object with explicit unknowns allowed")
    for field in ("problem", "origin", "workaround", "internal_solution", "reusability", "confidence", "next_validation_action", "stop_condition"):
        if not _nonempty(candidate[field]):
            errors.append(f"{field} must be non-empty")
    if not isinstance(candidate["provenance"], list) or not candidate["provenance"] or not all(_nonempty(item) for item in candidate["provenance"]):
        errors.append("provenance must be a non-empty list of paths")
    for field in ("severity", "external_evidence", "economic_evidence"):
        if not isinstance(candidate[field], dict):
            errors.append(f"{field} must be an object")
    if isinstance(candidate["external_evidence"], dict):
        state = candidate["external_evidence"].get("status")
        if state not in EXTERNAL_STATES:
            errors.append("external_evidence.status is invalid")
        if state == "PRESENT" and not candidate["external_evidence"].get("sources"):
            errors.append("present external evidence requires sources")
    if candidate["stage"] in {"EXTERNAL_EVIDENCE", "ECONOMIC_EVIDENCE", "PRODUCT_HYPOTHESIS", "VALIDATION"}:
        if candidate["external_evidence"].get("status") != "PRESENT":
            errors.append("advanced stages require PRESENT external evidence")
    if candidate["stage"] in {"ECONOMIC_EVIDENCE", "PRODUCT_HYPOTHESIS", "VALIDATION"}:
        if candidate["economic_evidence"].get("status") != "PRESENT":
            errors.append("economic stages require PRESENT economic evidence")
    if candidate["lifecycle"] == "PROTOTYPE" and candidate["stage"] not in {"PRODUCT_HYPOTHESIS", "VALIDATION"}:
        errors.append("PROTOTYPE requires a product hypothesis or validation stage")
    for field in ("known", "unknown"):
        if not isinstance(candidate.get(field, []), list):
            errors.append(f"{field} must be a list when present")
    errors.extend(_evidence_errors(candidate.get("evidence", []), "evidence"))
    return errors


def validate_ledger(ledger: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if ledger.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    candidates = ledger.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        return errors + ["candidates must be a non-empty list"]
    ids: set[str] = set()
    for candidate in candidates:
        if not isinstance(candidate, dict):
            errors.append("candidate must be an object")
            continue
        identity = candidate.get("id")
        if identity in ids:
            errors.append(f"duplicate candidate id: {identity}")
        ids.add(identity)
        errors.extend(f"{identity}: {error}" for error in validate_candidate(candidate))
    signals = ledger.get("signals", [])
    if not isinstance(signals, list):
        errors.append("signals must be a list")
    else:
        for index, signal in enumerate(signals):
            if not isinstance(signal, dict):
                errors.append(f"signals[{index}] must be an object")
                continue
            for field in ("id", "trigger", "source", "observed_at", "candidate_id"):
                if not _nonempty(signal.get(field)):
                    errors.append(f"signals[{index}] requires {field}")
            if signal.get("candidate_id") not in ids:
                errors.append(f"signals[{index}] references unknown candidate")
    return errors


def derived_stage(candidate: dict[str, Any]) -> str:
    """Return the strongest stage justified by recorded evidence."""
    frequency = candidate.get("frequency", {}).get("count", 0)
    if candidate.get("economic_evidence", {}).get("status") == "PRESENT":
        if candidate.get("external_evidence", {}).get("status") == "PRESENT":
            return "ECONOMIC_EVIDENCE"
    if candidate.get("external_evidence", {}).get("status") == "PRESENT":
        return "EXTERNAL_EVIDENCE"
    if candidate.get("reusability") not in {"NO", "UNKNOWN"} and candidate.get("internal_solution") not in {"NONE", "UNKNOWN"}:
        return "REUSE" if frequency >= 2 else "SIGNAL"
    return "REPETITION" if frequency >= 3 else "SIGNAL"


def scan(ledger: dict[str, Any]) -> dict[str, Any]:
    errors = validate_ledger(ledger)
    if errors:
        return {"status": "INVALID", "errors": errors}
    return {
        "status": "OK",
        "signals": [
            {
                "id": candidate["id"],
                "recorded_stage": candidate["stage"],
                "evidence_stage": derived_stage(candidate),
                "classification": candidate["classification"],
                "lifecycle": candidate["lifecycle"],
                "needs_review": derived_stage(candidate) != candidate["stage"],
            }
            for candidate in ledger["candidates"]
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "scan"))
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    args = parser.parse_args()
    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    if args.command == "scan":
        result = scan(ledger)
    else:
        errors = validate_ledger(ledger)
        result = {"status": "OK" if not errors else "INVALID", "errors": errors}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
