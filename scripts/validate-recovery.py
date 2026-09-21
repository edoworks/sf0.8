#!/usr/bin/env python3
"""Validate bounded recovery records without executing discovered solutions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from recovery import validate_solution_sources


def validate(registry: dict, sources: dict) -> list[str]:
    errors = []
    if registry.get("schema_version") != 1:
        errors.append("recovery registry schema_version must be 1")
    ids = set()
    for solution in registry.get("solutions", []):
        identifier = solution.get("id")
        if not identifier or identifier in ids:
            errors.append(f"duplicate or missing solution id: {identifier}")
        ids.add(identifier)
        errors.extend(validate_solution_sources(solution, sources))
        if solution.get("disposition") not in {"ADOPT", "ADAPT", "LEARN_FROM", "REJECT"}:
            errors.append(f"{identifier}: invalid disposition")
        if not solution.get("mechanism") or not solution.get("validation_evidence"):
            errors.append(f"{identifier}: mechanism and validation evidence are required")
        if not solution.get("authority_state"):
            errors.append(f"{identifier}: authority_state is required")
    if registry.get("policy", {}).get("max_attempts_per_objective", 0) < 1:
        errors.append("recovery attempt bound must be positive")
    for outcome in registry.get("outcomes", []):
        if outcome.get("next_state") not in {"HUMAN_AUTHORIZATION_REQUIRED", "BLOCKED_AFTER_SELF_UNBLOCKING", "OBJECTIVE_COMPLETE", "FAILED"}:
            errors.append(f"invalid recovery outcome state: {outcome.get('next_state')}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry", type=Path)
    parser.add_argument("sources", type=Path)
    args = parser.parse_args()
    errors = validate(json.loads(args.registry.read_text()), json.loads(args.sources.read_text()))
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("recovery registry validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
