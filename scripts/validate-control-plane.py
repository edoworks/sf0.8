#!/usr/bin/env python3
"""Validate the durable implementation/control-plane reconciliation record."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from ecosystem_gates import completion_state

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    path = ROOT / ".factory/artifacts/evidence/control-plane/issue-49-reconciliation.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    result = completion_state(record)
    errors = list(result["errors"])
    if record.get("state") != result["state"]:
        errors.append("durable control-plane state disagrees with completion evaluator")
    if record.get("done") is not result["done"]:
        errors.append("durable done flag disagrees with completion evaluator")
    if not record.get("idempotency_key") or not record.get("resume_action"):
        errors.append("blocked control-plane records require idempotency and resume evidence")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("control-plane reconciliation validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
