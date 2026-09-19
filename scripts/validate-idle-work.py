#!/usr/bin/env python3
"""Validate a bounded idle-work discovery or exhaustion report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from idle_work import validate_waiting_report


def validate_report(report: dict) -> list[str]:
    errors = []
    if report.get("schema_version") != 1:
        errors.append("idle-work report schema_version must be 1")
    for field in ("sources_searched", "provider_results", "candidates_found", "candidates_rejected_or_blocked", "eligible_candidates", "eligible_count", "exhaustive", "status"):
        if field not in report:
            errors.append(f"idle-work report missing {field}")
    if report.get("eligible_count") != len(report.get("eligible_candidates", [])):
        errors.append("eligible_count does not match eligible_candidates")
    if report.get("exhaustive") and any(item.get("status") != "PASS" for item in report.get("provider_results", [])):
        errors.append("exhaustive report contains a failed provider")
    for candidate in report.get("candidates_found", []):
        for field in ("value", "urgency", "reversibility", "risk", "cost", "required_authority", "dependencies", "scope", "evidence", "expected_validation", "category"):
            if field not in candidate:
                errors.append(f"candidate {candidate.get('id', '<unknown>')} missing {field}")
    errors.extend(validate_waiting_report(report))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    errors = validate_report(json.loads(args.report.read_text(encoding="utf-8")))
    if errors:
        print(json.dumps({"errors": errors}, indent=2))
        return 1
    print("idle-work report validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
