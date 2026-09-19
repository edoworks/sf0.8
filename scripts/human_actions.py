#!/usr/bin/env python3
"""Validate and order executable human actions without a synthetic score."""

from __future__ import annotations

from typing import Any


REQUIRED_FIELDS = {
    "id",
    "action",
    "why_human_required",
    "blocked_work",
    "priority",
    "estimated_human_minutes",
    "required_input_or_decision",
    "evidence_to_collect",
    "resume_condition",
    "can_expire",
    "related",
    "blocking_impact",
    "information_gain",
    "reversibility",
    "urgency",
}
DIMENSION_VALUES = {
    "blocking_impact": {"HIGH", "MEDIUM", "LOW"},
    "information_gain": {"HIGH", "MEDIUM", "LOW"},
    "reversibility": {"HIGH", "MEDIUM", "LOW"},
    "urgency": {"HIGH", "MEDIUM", "LOW"},
}


def validate_action(action: dict[str, Any]) -> list[str]:
    errors = [f"missing {field}" for field in sorted(REQUIRED_FIELDS - action.keys())]
    for field, values in DIMENSION_VALUES.items():
        if action.get(field) not in values:
            errors.append(f"{field} must be one of {sorted(values)}")
    if not isinstance(action.get("estimated_human_minutes"), int) or action.get("estimated_human_minutes", 0) <= 0:
        errors.append("estimated_human_minutes must be a positive integer")
    if not isinstance(action.get("evidence_to_collect"), list) or not action.get("evidence_to_collect"):
        errors.append("evidence_to_collect must be a non-empty list")
    if not isinstance(action.get("related"), dict):
        errors.append("related must be an object")
    if action.get("can_expire") is True and not str(action.get("expiry_condition", "")).strip():
        errors.append("expiring actions require expiry_condition")
    return errors


def validate_queue(queue: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if queue.get("schema_version") != 1:
        errors.append("human action queue schema_version must be 1")
    actions = queue.get("actions")
    if not isinstance(actions, list) or not actions:
        return errors + ["human action queue must contain actions"]
    ids: set[str] = set()
    for action in actions:
        if action.get("id") in ids:
            errors.append(f"duplicate action id: {action.get('id')}")
        ids.add(action.get("id"))
        errors.extend(f"{action.get('id')}: {error}" for error in validate_action(action))
    return errors


def attention_order(action: dict[str, Any]) -> tuple[int, int, int, int, int, str]:
    """Return separate dimension ranks; this is ordering, not a readiness score."""
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    return (
        rank[action["blocking_impact"]],
        rank[action["information_gain"]],
        action["estimated_human_minutes"],
        rank[action["reversibility"]],
        rank[action["urgency"]],
        action["id"],
    )


def ordered_actions(queue: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(queue.get("actions", []), key=attention_order)
