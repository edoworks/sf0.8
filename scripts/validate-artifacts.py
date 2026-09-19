#!/usr/bin/env python3
"""Validate Git-visible artifact records without executing artifact contents."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / ".factory" / "artifacts"
REQUIRED = {"id", "title", "version", "kind", "status", "source", "license", "provenance", "security", "verification", "publication", "maintenance"}
SECRET_RE = re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+:-]{12,}")
INTERNAL_PATH_RE = re.compile(r"/Users/[A-Za-z0-9._-]+/|/private/|/tmp/[A-Za-z0-9._-]+")


def errors_for(record: dict) -> list[str]:
    errors = sorted(REQUIRED - record.keys())
    if errors:
        return [f"missing fields: {', '.join(errors)}"]
    errors = []
    if record["status"] == "publication-ready" and not record["publication"].get("human_approval_required"):
        errors.append("publication-ready records must require human approval")
    if record["publication"].get("approved") is not False:
        errors.append("publication approval must remain false in the factory registry")
    if record["security"].get("execution") not in {"not-executed", "local-only"}:
        errors.append("external artifacts cannot be marked for execution")
    if not record["license"].get("compatibility_checked"):
        errors.append("license compatibility has not been checked")
    if not record["provenance"].get("derived_from"):
        errors.append("provenance must name source records")
    if record["status"] in {"validated", "publication-ready"} and not record["provenance"].get("human_reviewed"):
        errors.append("validated/publication-ready records require human review evidence")
    if record["license"].get("spdx") in {"UNKNOWN", "NOASSERTION", ""}:
        errors.append("adopted records cannot use an unknown license")
    if not record["source"].get("author"):
        errors.append("source author/organization is required")
    if not record["source"].get("evaluated_at"):
        errors.append("source evaluation date is required")
    if not record["provenance"].get("modifications"):
        errors.append("provenance must describe modifications")
    if not record["provenance"].get("attribution"):
        errors.append("provenance must describe attribution requirements")
    if not record["maintenance"].get("owner") or not record["maintenance"].get("next_review"):
        errors.append("maintenance owner and next review are required")
    for field, section in (("license.file", record["license"]), ("verification.docs", record["verification"]), ("verification.tests", record["verification"]), ("verification.provenance", record["verification"])):
        relative = section.get(field.split(".")[-1], "")
        if relative and (Path(relative).is_absolute() or ".." in Path(relative).parts):
            errors.append(f"{field} must be a safe repository-relative path")
    return errors


def validate(root: Path = ARTIFACTS) -> list[str]:
    errors: list[str] = []
    for path in sorted((root / "records").glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(record, dict):
                raise ValueError("record is not an object")
            errors.extend(f"{path}: {error}" for error in errors_for(record))
            serialized = json.dumps(record, sort_keys=True)
            if SECRET_RE.search(serialized):
                errors.append(f"{path}: possible secret pattern in public artifact record")
            if INTERNAL_PATH_RE.search(serialized):
                errors.append(f"{path}: internal path in public artifact record")
            for field in ("license.file", "verification.docs", "verification.provenance"):
                section_name, key = field.split(".")
                relative = record.get(section_name, {}).get(key, "")
                if relative and not (root / relative).is_file():
                    errors.append(f"{path}: missing evidence file: {relative}")
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(f"{path}: invalid JSON record: {error}")
    if not list((root / "records").glob("*.json")):
        errors.append("artifact registry has no records")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("artifact validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
