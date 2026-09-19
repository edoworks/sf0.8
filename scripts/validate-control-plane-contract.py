#!/usr/bin/env python3
"""Validate per-control-plane downstream preflight requirements."""

import argparse
import json
from pathlib import Path


def validate(record: dict) -> list[str]:
    errors: list[str] = []
    if record.get("schema_version") != 1:
        errors.append("control-plane requirements schema_version must be 1")
    requirements = record.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        return errors + ["control-plane requirements must contain entries"]
    ids: set[str] = set()
    for item in requirements:
        identifier = item.get("id")
        if identifier in ids:
            errors.append(f"duplicate control-plane requirement: {identifier}")
        ids.add(identifier)
        for field in ("id", "control_plane", "required_before", "human_authority", "proof"):
            if not str(item.get(field, "")).strip():
                errors.append(f"{identifier}: missing {field}")
        if item.get("status") == "PROVEN" and not item.get("proof_evidence"):
            errors.append(f"{identifier}: PROVEN requires proof_evidence")
        if item.get("status") not in {None, "PROVEN", "UNPROVEN", "BLOCKED"}:
            errors.append(f"{identifier}: invalid status")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    errors = validate(json.loads(args.record.read_text(encoding="utf-8")))
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("control-plane contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
