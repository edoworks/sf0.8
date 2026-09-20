#!/usr/bin/env python3
"""Validate the required evidence-to-implementation review handoff."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

REQUIRED = {"evidence", "challenge", "findings", "concrete_actions", "implementation_prompt"}


def validate_review(record: dict) -> list[str]:
    missing = sorted(REQUIRED - record.keys())
    errors = [f"missing review-contract field: {field}" for field in missing]
    for field in REQUIRED:
        if field in record and not str(record[field]).strip():
            errors.append(f"review-contract field is empty: {field}")
    prompt = str(record.get("implementation_prompt", ""))
    if prompt and not any(token in prompt.casefold() for token in ("implement", "fix", "change", "build")):
        errors.append("implementation_prompt must be action-oriented")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    errors = validate_review(json.loads(args.record.read_text(encoding="utf-8")))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("review contract validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
