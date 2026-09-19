#!/usr/bin/env python3
"""Reconcile independently discovered products against factory knowledge."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def identity_keys(record: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    for field in ("bundle_id", "app_store_id", "product_id", "id"):
        value = record.get(field)
        if value:
            keys.add(f"{field}:{str(value).casefold()}")
    for field in ("bundle_ids",):
        for value in record.get(field, []):
            keys.add(f"bundle_id:{str(value).casefold()}")
    for field in ("source", "source_path", "local_path"):
        value = record.get(field)
        if value and value != "UNKNOWN":
            keys.add(f"path:{str(value).rstrip('/').casefold()}")
    for value in record.get("repositories", []):
        keys.add(f"repo:{str(value).casefold()}")
    repository = record.get("repository")
    if isinstance(repository, dict) and repository.get("repository_id"):
        keys.add(f"repo:{repository['repository_id'].casefold()}")
    elif isinstance(repository, str) and repository:
        keys.add(f"repo:{repository.casefold()}")
    return keys


def match(discovered: dict[str, Any], known: dict[str, Any]) -> bool:
    return bool(identity_keys(discovered) & identity_keys(known))


def reconcile(
    discovery: dict[str, Any],
    known_products: list[dict[str, Any]],
    verified_shipping: list[dict[str, Any]],
    *,
    historical_products: list[dict[str, Any]] | None = None,
    distribution_records: list[dict[str, Any]] | None = None,
    reusable_artifacts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    discovered = discovery.get("candidates", [])
    matched_known = [product for product in known_products if any(match(item, product) for item in discovered)]
    missing_shipping = [product for product in verified_shipping if not any(match(item, product) for item in discovered)]
    public = [item for item in discovered if item.get("distribution_states") or item.get("website_domains")]
    known_keys = {key for product in known_products for key in identity_keys(product)}
    orphans = []
    for item in discovered:
        if not identity_keys(item) & known_keys and item.get("confidence") == "HIGH":
            orphans.append({"type": "PUBLIC_PRODUCT_NOT_IN_FACTORY_PORTFOLIO", "candidate": item})
        if item.get("local_paths") and not item.get("repositories"):
            orphans.append({"type": "LOCAL_REPOSITORY_WITHOUT_PRODUCT_CLASSIFICATION", "candidate": item})
    for product in known_products:
        if not any(match(item, product) for item in discovered):
            orphans.append({"type": "FACTORY_PRODUCT_WITHOUT_IMPLEMENTATION", "candidate": product})
    for product in historical_products or []:
        if not any(match(item, product) for item in discovered):
            orphans.append({"type": "HISTORICAL_PRODUCT_NOT_RECONCILED", "candidate": product})
    for record in distribution_records or []:
        if not any(match(item, record) for item in discovered):
            orphans.append({"type": "DISTRIBUTION_RECORD_WITHOUT_PRODUCT", "candidate": record})
    for artifact in reusable_artifacts or []:
        if not artifact.get("consumers"):
            orphans.append({"type": "REUSABLE_ARTIFACT_WITHOUT_CONSUMERS", "candidate": artifact})
    recall = (len(verified_shipping) - len(missing_shipping)) / len(verified_shipping) if verified_shipping else 1.0
    blocking_types = {
        "PUBLIC_PRODUCT_NOT_IN_FACTORY_PORTFOLIO",
        "FACTORY_PRODUCT_WITHOUT_IMPLEMENTATION",
        "DISTRIBUTION_RECORD_WITHOUT_PRODUCT",
        "HISTORICAL_PRODUCT_NOT_RECONCILED",
        "UNKNOWN_IDENTITY_RELATIONSHIP",
    }
    blocking_orphans = [item for item in orphans if item["type"] in blocking_types]
    complete = recall == 1.0 and not blocking_orphans
    return {
        "schema_version": 2,
        "sets": {
            "A_public_products": public,
            "B_factory_known_products": known_products,
            "C_local_implementations": [item for item in discovered if item.get("local_paths")],
            "D_historical_products": historical_products or [],
            "E_distribution_records": distribution_records or [],
            "F_reusable_artifacts": reusable_artifacts or [],
        },
        "portfolio_recall": {
            "verified_known_products": len(verified_shipping),
            "verified_known_products_discovered": len(verified_shipping) - len(missing_shipping),
            "value": recall,
            "missing": missing_shipping,
        },
        "matched_factory_products": [product.get("id") or product.get("product_id") for product in matched_known],
        "orphans": orphans,
        "completion": {
            "state": "PORTFOLIO_RECONCILED" if complete else "PORTFOLIO_RECONCILIATION_BLOCKED",
            "done": complete,
            "requires": "100% verified shipping recall and no unexplained blocking identity or implementation orphans",
            "blocking_orphan_count": len(blocking_orphans),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("discovery", type=Path)
    parser.add_argument("fixture", type=Path, help="independent verified shipping fixture")
    parser.add_argument("--known", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    discovery = json.loads(args.discovery.read_text(encoding="utf-8"))
    fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
    known = json.loads(args.known.read_text(encoding="utf-8"))
    result = reconcile(discovery, known["products"], fixture["products"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["completion"], sort_keys=True))
    return 0 if result["completion"]["done"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
