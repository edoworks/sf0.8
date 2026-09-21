#!/usr/bin/env python3
"""Inventory discoverable skills without approving installation or publication."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


RECOMMENDATIONS = {"SHAREABILITY_REVIEW", "DEFER", "NOT_SHAREABLE"}


def discover_skills(inventory: dict[str, Any], root: Path) -> set[tuple[str, str]]:
    """Return every skill directory containing SKILL.md under declared roots."""
    discovered: set[tuple[str, str]] = set()
    for declared in inventory.get("roots", []):
        source_root = Path(str(declared["path"]))
        if not source_root.is_absolute():
            source_root = root / source_root
        if not source_root.is_dir():
            continue
        for skill_file in source_root.glob("*/SKILL.md"):
            discovered.add((str(declared["id"]), skill_file.parent.name))
    return discovered


def available_root_ids(inventory: dict[str, Any], root: Path) -> set[str]:
    available: set[str] = set()
    for declared in inventory.get("roots", []):
        source_root = Path(str(declared["path"]))
        if not source_root.is_absolute():
            source_root = root / source_root
        if source_root.is_dir():
            available.add(str(declared["id"]))
    return available


def validate_inventory(inventory: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    roots = {str(item.get("id")): item for item in inventory.get("roots", [])}
    if len(roots) != len(inventory.get("roots", [])):
        errors.append("skill roots must have unique ids")
    for root_id, declared in roots.items():
        source_root = Path(str(declared.get("path", "")))
        if not source_root.is_absolute():
            source_root = root / source_root
        if not source_root.is_dir() and declared.get("required", True) is True:
            errors.append(f"required skill root is unavailable: {root_id}")
    records = inventory.get("records", [])
    identities: set[tuple[str, str]] = set()
    for index, record in enumerate(records):
        prefix = f"records[{index}]"
        identity = (str(record.get("root", "")), str(record.get("id", "")))
        if identity in identities:
            errors.append(f"{prefix}: duplicate skill identity")
        identities.add(identity)
        if identity[0] not in roots or not identity[1]:
            errors.append(f"{prefix}: unknown root or empty skill id")
        if record.get("recommendation") not in RECOMMENDATIONS:
            errors.append(f"{prefix}: invalid recommendation")
        if not isinstance(record.get("evidence"), list) or not record["evidence"]:
            errors.append(f"{prefix}: evidence is required")
        if record.get("publication_approved") is not False:
            errors.append(f"{prefix}: publication must remain human-gated")
        if record.get("used") is True and record.get("recommendation") == "DEFER" and not str(record.get("reason", "")).strip():
            errors.append(f"{prefix}: deferred used skills require a reason")

    discovered = discover_skills(inventory, root)
    missing = sorted(discovered - identities)
    available = available_root_ids(inventory, root)
    extra = sorted(identity for identity in identities - discovered if identity[0] in available)
    errors.extend(f"missing inventory record: {source}/{name}" for source, name in missing)
    errors.extend(f"inventory record has no skill file: {source}/{name}" for source, name in extra)
    return errors


def recommendations(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    """Return only used skills recommended for human shareability review."""
    return [record for record in inventory.get("records", []) if record.get("used") is True and record.get("recommendation") == "SHAREABILITY_REVIEW"]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, default=Path(".factory/artifacts/skill-sharing-inventory.json"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    payload = json.loads(args.inventory.read_text(encoding="utf-8"))
    errors = validate_inventory(payload, args.root)
    print(json.dumps({"decision": "PASS" if not errors else "BLOCKED", "errors": errors, "recommendations": recommendations(payload)}, indent=2, sort_keys=True))
    raise SystemExit(1 if errors else 0)
