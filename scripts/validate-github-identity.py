#!/usr/bin/env python3
"""Fail-closed validation for the edoworks GitHub identity boundary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / ".factory/github-identity-policy.json"


def allowed_login(login: Any, policy: dict[str, Any]) -> bool:
    if not isinstance(login, str) or not login.strip():
        return False
    value = login.strip()
    suffix = policy.get("allowed_username_suffix")
    if not isinstance(suffix, str) or not suffix:
        return False
    if policy.get("matching") == "case_insensitive":
        value, suffix = value.casefold(), suffix.casefold()
    return value.endswith(suffix)


def snapshot_errors(snapshot: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    organizations = [policy.get("organization")]
    additional = policy.get("additional_organizations", [])
    if isinstance(additional, list):
        organizations.extend(additional)
    if snapshot.get("organization") not in organizations:
        errors.append("snapshot organization does not match policy")
    for field in ("members", "collaborators", "reviewers", "bypass_actors"):
        values = snapshot.get(field, [])
        if not isinstance(values, list):
            errors.append(f"{field} must be a list")
            continue
        for login in values:
            if not allowed_login(login, policy):
                errors.append(f"unauthorized login in {field}: {login!r}")
    expected_bypass = policy.get("exclusive_bypass_actors")
    actual_bypass = snapshot.get("bypass_actors")
    if isinstance(expected_bypass, list) and isinstance(actual_bypass, list):
        expected = {str(login).casefold() for login in expected_bypass}
        actual = {str(login).casefold() for login in actual_bypass}
        if actual != expected:
            errors.append(
                "bypass_actors must exactly match exclusive_bypass_actors"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--actor")
    parser.add_argument("--snapshot", type=Path)
    args = parser.parse_args()
    if bool(args.actor) == bool(args.snapshot):
        parser.error("provide exactly one of --actor or --snapshot")

    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    errors = []
    if args.actor and not allowed_login(args.actor, policy):
        errors.append(f"unauthorized actor: {args.actor!r}")
    if args.snapshot:
        try:
            snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"cannot read snapshot: {exc}")
        else:
            errors.extend(snapshot_errors(snapshot, policy))
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("GitHub identity policy validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
