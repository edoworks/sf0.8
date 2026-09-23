#!/usr/bin/env python3
"""Validate repository coverage without treating inaccessible scope as empty."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PREDECESSORS = {"foculoom/sf0.7", "foculoom/sf0.5"}


def portfolio_blocks(text: str) -> dict[str, str]:
    blocks = {}
    for block in re.split(r"(?=  - id: )", text):
        match = re.search(r"^  - id: (\S+)", block, re.MULTILINE)
        if match:
            blocks[match.group(1)] = block
    return blocks


def validate(
    inventory: dict,
    manifest: dict,
    portfolio: str,
    now: datetime | None = None,
) -> list[str]:
    errors: list[str] = []
    now = now or datetime.now(timezone.utc)
    public = inventory.get("public_inventory", {})
    private = inventory.get("private_inventory", {})
    repositories = public.get("repositories", [])
    ids = [repository.get("id") for repository in repositories]
    counts = public.get("counts", {})

    try:
        captured_at = datetime.fromisoformat(inventory["captured_at"].replace("Z", "+00:00"))
        max_age_hours = int(inventory["max_age_hours"])
        age_seconds = (now - captured_at).total_seconds()
        if captured_at > now:
            errors.append("repository inventory snapshot is future-dated")
        elif max_age_hours <= 0 or age_seconds > max_age_hours * 3600:
            errors.append("repository inventory snapshot is stale")
    except (KeyError, TypeError, ValueError):
        errors.append("repository inventory lacks a valid freshness boundary")

    if public.get("complete") is not True:
        errors.append("public inventory is not explicitly complete")
    if len(ids) != len(set(ids)):
        errors.append("public inventory contains duplicate repository ids")
    if len(ids) != sum(counts.values()):
        errors.append("public repository count does not match organization counts")
    if sum(repository_id.startswith("edoworks/") for repository_id in ids) != counts.get("edoworks"):
        errors.append("Edoworks public repository count drifted")
    if sum(repository_id.startswith("foculoom/") for repository_id in ids) != counts.get("foculoom"):
        errors.append("Foculoom public repository count drifted")

    if private.get("complete") is not False:
        errors.append("private inventory must remain incomplete until authenticated enumeration succeeds")
    if not private.get("blocker"):
        errors.append("incomplete private inventory lacks a blocker")

    try:
        blocks = portfolio_blocks(portfolio)
    except (IndexError, AttributeError):
        return errors + ["portfolio registry is missing a parseable repos section"]
    all_ids = ids + private.get("known_repositories", [])
    for repository_id in all_ids:
        block = blocks.get(repository_id, "")
        if not block:
            errors.append(f"inventoried repository is absent from portfolio: {repository_id}")
            continue
        for field in ("lifecycle", "disposition"):
            values = re.findall(rf"^    {field}:\s*(\S+)", block, re.MULTILINE)
            if len(values) != 1:
                errors.append(f"portfolio requires exactly one {field} for {repository_id}")

    for repository in repositories:
        repository_id = repository.get("id")
        block = blocks.get(repository_id, "")
        if not block:
            continue
        for field in ("lifecycle", "disposition"):
            values = re.findall(rf"^    {field}:\s*(\S+)", block, re.MULTILINE)
            if values != [repository.get(field)]:
                errors.append(f"portfolio {field} disagrees for {repository_id}")

    predecessor_keys = set(manifest.get("repositories", {})) & {
        "edoworks/sf0.7", "edoworks/sf0.5", "foculoom/sf0.7", "foculoom/sf0.5"
    }
    if predecessor_keys != REQUIRED_PREDECESSORS:
        errors.append("obligation manifest does not use canonical Foculoom predecessor owners")
    for repository_id in REQUIRED_PREDECESSORS:
        record = manifest.get("repositories", {}).get(repository_id, {})
        if record.get("open_issue_count") is not None:
            errors.append(f"blocked predecessor must not claim a numeric issue count: {repository_id}")
        if record.get("status") != "remote_inventory_blocked":
            errors.append(f"blocked predecessor status drifted: {repository_id}")
    if manifest.get("summary", {}).get("manifest_complete") is not False:
        errors.append("obligation manifest must remain incomplete while predecessors are blocked")
    if set(manifest.get("summary", {}).get("blocked_repos", [])) != REQUIRED_PREDECESSORS:
        errors.append("obligation manifest blocked repository list drifted")

    try:
        manifest_captured_at = datetime.fromisoformat(manifest["captured_at"].replace("Z", "+00:00"))
        manifest_max_age_hours = int(manifest["max_age_hours"])
        manifest_age_seconds = (now - manifest_captured_at).total_seconds()
        if manifest_captured_at > now:
            errors.append("obligation manifest snapshot is future-dated")
        elif manifest_max_age_hours <= 0 or manifest_age_seconds > manifest_max_age_hours * 3600:
            errors.append("obligation manifest snapshot is stale")
    except (KeyError, TypeError, ValueError):
        errors.append("obligation manifest lacks a valid freshness boundary")

    sf08 = manifest.get("repositories", {}).get("edoworks/sf0.8", {})
    issues = sf08.get("issues", [])
    classifications: dict[str, int] = {}
    for issue in issues:
        classification = issue.get("classification")
        classifications[classification] = classifications.get(classification, 0) + 1
    summary = manifest.get("summary", {})
    if summary.get("total_inventoried") != len(issues):
        errors.append("obligation summary total disagrees with sf0.8 issue records")
    summary_classifications = {
        "migrated", "completed", "superseded", "retained-evidence", "rejected", "duplicate"
    }
    for classification in summary_classifications | set(classifications):
        if summary.get(classification) != classifications.get(classification, 0):
            errors.append(f"obligation summary count drifted: {classification}")
    for repository_id, record in manifest.get("repositories", {}).items():
        if "issues" in record and record.get("inventory_record_count") != len(record["issues"]):
            errors.append(f"repository inventory record count drifted: {repository_id}")
        if repository_id in {"edoworks/sf0.8", "edoworks/product-a"} and record.get("open_issue_count") != len(record.get("issues", [])):
            errors.append(f"predecessor open issue count drifted: {repository_id}")
    return errors


def main() -> None:
    inventory = json.loads((ROOT / ".factory/repository-inventory.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / ".factory/obligation-disposition-manifest.json").read_text(encoding="utf-8"))
    portfolio = (ROOT / ".factory/portfolio.yaml").read_text(encoding="utf-8")
    errors = validate(inventory, manifest, portfolio)
    if errors:
        raise SystemExit("repository inventory validation failed:\n- " + "\n- ".join(errors))
    print("repository inventory validation passed: public complete, private UNKNOWN")


if __name__ == "__main__":
    main()
