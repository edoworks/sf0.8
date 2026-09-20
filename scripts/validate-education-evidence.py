#!/usr/bin/env python3
"""Validate education discovery as falsifiable hypotheses, not product proof."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evidence_frontier import validate_frontier


STATES = {"DISCOVERED", "HYPOTHESIS", "EVIDENCE-WEAK", "VALIDATION-READY", "VALIDATED", "FALSIFIED", "PARKED", "KILLED"}
REQUIRED_SUBSTITUTION = {
    "job", "pain", "trigger", "current_workaround", "cost_of_workaround",
    "why_current_workaround_fails", "proposed_substitute", "switching_cost", "payment_evidence",
}


def validate(record: dict) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_frontier(record))
    catalog = record.get("state_catalog", {})
    if set(catalog.get("states", [])) != STATES:
        errors.append("state catalog must contain every explicit opportunity state")
    if catalog.get("transition_evidence_required") != ["from", "to", "reason", "evidence_reference"]:
        errors.append("state transitions must preserve reason and evidence reference")
    if record.get("evidence_discipline", {}).get("direct_customer_evidence") != "ABSENT":
        errors.append("direct customer evidence must remain ABSENT until observed")
    hypotheses = record.get("hypotheses", [])
    if len(hypotheses) != 5:
        errors.append("exactly five named education hypotheses are required")
    for item in hypotheses:
        if item.get("state") not in STATES:
            errors.append(f"{item.get('id')}: invalid opportunity state")
        if not str(item.get("state_reason", "")).strip():
            errors.append(f"{item.get('id')}: state reason is required")
        missing = REQUIRED_SUBSTITUTION - set(item.get("substitution", {}))
        errors.extend(f"{item.get('id')}: missing substitution field {field}" for field in sorted(missing))
        if item.get("state") == "VALIDATED":
            errors.append(f"{item.get('id')}: cannot be VALIDATED without external evidence in this artifact")
    contract = record.get("experiment_contract", {})
    if contract.get("experiment_artifact_is_not_product") is not True:
        errors.append("experiment artifacts must remain distinct from products")
    if contract.get("learning_gate") != ["BEFORE", "EXPERIENCE", "IMMEDIATE_AFTER", "NOVEL_TRANSFER_TASK", "48_HOUR_RETEST"]:
        errors.append("learning gate must include transfer and delayed retest")
    if contract.get("no_subscription_default") is not True:
        errors.append("subscription cannot be the default monetization assumption")
    if not contract.get("behavior_change_evidence"):
        errors.append("behavior-change evidence categories are required")
    kits = record.get("experiment_kits", {})
    for artifact in [*kits.get("shared", []), *kits.get("specific", [])]:
        if not (Path(__file__).resolve().parents[1] / ".factory/experiments/education" / artifact).exists():
            errors.append(f"experiment kit artifact is missing: {artifact}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    errors = validate(json.loads(args.record.read_text(encoding="utf-8")))
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
