#!/usr/bin/env python3
"""Pure lifecycle transition and deletion-evidence rules."""

from __future__ import annotations

from typing import Any


def transition_allowed(contract: dict[str, Any], current: str, target: str) -> bool:
    return target in contract.get("transitions", {}).get(current, [])


def deletion_errors(contract: dict[str, Any], evidence: dict[str, Any]) -> list[str]:
    required = contract.get("deletion_requirements", [])
    errors = [field for field in required if evidence.get(field) is not True]
    if evidence.get("state") == "UNKNOWN":
        errors.append("UNKNOWN candidates cannot become deletion-eligible")
    if evidence.get("state") == "DELETION_CANDIDATE" and evidence.get("human_authorized_delete"):
        errors.append("DELETION_CANDIDATE cannot self-authorize deletion")
    if evidence.get("state") == "HUMAN_AUTHORIZED_DELETE" and evidence.get("human_authorization") is not True:
        errors.append("HUMAN_AUTHORIZED_DELETE requires explicit human authorization")
    return errors
