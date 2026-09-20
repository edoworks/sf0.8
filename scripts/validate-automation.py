#!/usr/bin/env python3
"""Validate automation-first release criteria and evidence bundles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CLASSIFICATIONS = {"AUTOMATED", "SIMULATOR", "SANDBOX", "DEVICE", "EMPIRICAL", "HUMAN-AUTHORITY", "NOT-APPLICABLE"}
BUNDLE_STATUSES = {"VERIFIED", "PARTIALLY VERIFIED", "UNVERIFIED", "NOT APPLICABLE"}
AUTOMATED_CLASSES = {"AUTOMATED", "SIMULATOR", "SANDBOX"}
ESCAPE_CLASSES = {"DEVICE", "EMPIRICAL", "HUMAN-AUTHORITY"}


def validate_criteria(document: dict) -> list[str]:
    errors: list[str] = []
    if document.get("schema_version") != 2 or not isinstance(document.get("criteria"), list):
        return ["criteria document must use schema version 1 and contain criteria"]
    ids: set[str] = set()
    for index, criterion in enumerate(document["criteria"]):
        prefix = f"criteria[{index}]"
        missing = {"id", "source", "requirement", "classification", "production_blocker", "claim", "evidence"} - criterion.keys()
        errors.extend(f"{prefix}: missing {field}" for field in sorted(missing))
        if "id" in criterion and criterion["id"] in ids:
            errors.append(f"{prefix}: duplicate id {criterion['id']}")
        ids.add(criterion.get("id", ""))
        classification = criterion.get("classification")
        if classification not in CLASSIFICATIONS:
            errors.append(f"{prefix}: invalid classification")
        if classification in ESCAPE_CLASSES:
            escape = criterion.get("escape", {})
            required = {"why_automation_is_insufficient", "physical_or_empirical_property", "satisfying_evidence"}
            errors.extend(f"{prefix}: escape requires {field}" for field in sorted(required - escape.keys()))
        if classification in AUTOMATED_CLASSES and "escape" in criterion:
            errors.append(f"{prefix}: automated criterion must not carry an escape")
        if "manual review required" in json.dumps(criterion, sort_keys=True).lower():
            errors.append(f"{prefix}: generic manual-review language is not an escape justification")
    return errors


def validate_customer_zero(document: dict, manifests: list[dict]) -> list[str]:
    errors: list[str] = []
    if document.get("schema_version") != 1 or not isinstance(document.get("products"), list):
        return ["customer-zero document must use schema version 1 and contain products"]
    by_product = {manifest.get("product"): manifest for manifest in manifests}
    for index, product in enumerate(document["products"]):
        prefix = f"products[{index}]"
        required = {"id", "primary_customer_zero", "evidence", "desired_outcome", "would_build", "critical_journeys"}
        errors.extend(f"{prefix}: missing {field}" for field in sorted(required - product.keys()))
        manifest = by_product.get(product.get("id"))
        if not manifest:
            errors.append(f"{prefix}: no automation manifest for {product.get('id')}")
            continue
        journeys = manifest.get("customer_zero_journeys", [])
        journey_ids = {journey.get("id") for journey in journeys}
        for journey_id in product.get("critical_journeys", []):
            if journey_id not in journey_ids:
                errors.append(f"{prefix}: critical journey is not declared by the product manifest: {journey_id}")
        criteria_ids = {criterion.get("id") for criterion in manifest.get("criteria", [])}
        for journey in journeys:
            missing = set(journey.get("release_criteria", [])) - criteria_ids
            errors.extend(f"{prefix}: journey {journey.get('id')} references missing criterion {criterion_id}" for criterion_id in sorted(missing))
            if not journey.get("outcome"):
                errors.append(f"{prefix}: journey {journey.get('id')} has no human outcome")
    return errors


def load_sources(document: dict) -> tuple[list[str], list[dict]]:
    """Resolve canonical product manifests without copying their criteria."""
    errors: list[str] = []
    manifests: list[dict] = []
    if document.get("schema_version") != 2 or not isinstance(document.get("sources"), list):
        return ["source index must use schema version 2 and contain sources"], []
    for index, source in enumerate(document["sources"]):
        path = Path(source.get("path", ""))
        if not path.is_file():
            errors.append(f"sources[{index}]: canonical manifest is missing: {path}")
            continue
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"sources[{index}]: cannot read canonical manifest: {error}")
            continue
        errors.extend(f"{source.get('product', index)}: {error}" for error in validate_criteria(manifest))
        manifests.append(manifest)
    return errors, manifests


def summarize(manifests: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {classification: 0 for classification in sorted(CLASSIFICATIONS)}
    for manifest in manifests:
        for criterion in manifest.get("criteria", []):
            counts[criterion["classification"]] += 1
    counts["UNJUSTIFIED_MANUAL"] = 0
    return counts


def validate_bundle(document: dict, criteria: dict | None = None) -> list[str]:
    errors: list[str] = []
    categories = document.get("categories")
    if document.get("schema_version") != 1 or not isinstance(categories, dict):
        return ["evidence bundle must use schema version 1 and contain categories"]
    for category, result in categories.items():
        if result.get("status") not in BUNDLE_STATUSES:
            errors.append(f"{category}: invalid bundle status")
        if not isinstance(result.get("evidence"), list):
            errors.append(f"{category}: evidence must be a list")
        if result.get("status") in {"VERIFIED", "PARTIALLY VERIFIED"} and not result.get("evidence"):
            errors.append(f"{category}: verified status requires evidence")
    if criteria and document.get("criteria_file") != ".factory/automation/release-criteria.json":
        errors.append("bundle must identify the canonical criteria file")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--criteria", type=Path, default=ROOT / ".factory/automation/release-criteria.json")
    parser.add_argument("--bundle", type=Path, default=ROOT / ".factory/automation/evidence-bundle.json")
    args = parser.parse_args()
    criteria = json.loads(args.criteria.read_text(encoding="utf-8"))
    bundle = json.loads(args.bundle.read_text(encoding="utf-8"))
    source_errors, manifests = load_sources(criteria)
    customer_zero_path = ROOT / criteria.get("customer_zero_source", ".factory/customer-zero.json")
    customer_zero = json.loads(customer_zero_path.read_text(encoding="utf-8"))
    errors = source_errors + validate_bundle(bundle, criteria) + validate_customer_zero(customer_zero, manifests)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(json.dumps({"status": "passed", "summary": summarize(manifests)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
