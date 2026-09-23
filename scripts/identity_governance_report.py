#!/usr/bin/env python3
"""Build the deterministic, redacted identity-governance matrix."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def _domain_recommendation(record: dict[str, Any]) -> str:
    classification = record["classification"]
    if classification == "CORE":
        return "MAINTAIN_CORE"
    if classification == "DEFENSIVE":
        return "MAINTAIN_DEFENSIVE_NO_BRAND_ADOPTION"
    if classification == "DO_NOT_USE_AS_BRAND":
        return "DO_NOT_USE_AS_BRAND"
    if classification == "RETIRE_CANDIDATE":
        return "HUMAN_REVIEW_RETIREMENT"
    if classification == "REVIEW":
        return "HOLD_FOR_LEGAL_REVIEW"
    if classification in {"CANDIDATE", "EXPERIMENT"}:
        return "HOLD_NO_ADOPTION"
    return "MAINTAIN_PRODUCT" if record.get("adoption_allowed") else "HOLD_PENDING_IDENTITY_REVIEW"


def build_matrix(registry: dict[str, Any]) -> dict[str, Any]:
    legal = registry["legal_entity"]
    rows = [{
        "kind": "LEGAL_ENTITY",
        "id": legal["entity_id"],
        "display_name": legal["legal_name"],
        "role": "LEGAL_ENTITY_IP_OWNER_SELLER",
        "lifecycle": "active",
        "state": "EXTERNAL_VERIFICATION_REQUIRED",
        "trademark_state": "NOT_APPLICABLE",
        "domain": "foculoom.com",
        "release_blocker": "LIVE_EXTERNAL_RECORDS_UNVERIFIED",
        "required_action": "VERIFY_CA_SOS_AND_APP_STORE_SELLER",
        "recommendation": "VERIFY_CA_SOS_RECORD",
    }]
    for identity in sorted(registry["identities"], key=lambda item: item["entity_id"]):
        rows.append({
            "kind": identity["entity_type"].upper(),
            "id": identity["entity_id"],
            "display_name": identity["name"],
            "role": identity.get("role", "PRODUCT" if identity["entity_type"] == "product" else "BRAND"),
            "state": identity["identity_state"],
            "trademark_state": identity["trademark_state"],
            "lifecycle": identity["lifecycle"],
            "adoption_allowed": identity["adoption_allowed"],
            "domain": identity.get("canonical_domain"),
            "release_blocker": "NONE" if identity["adoption_allowed"] else "IDENTITY_OR_TRADEMARK_REVIEW_REQUIRED",
            "required_action": "PRESERVE_CURRENT_LIMITS" if identity["adoption_allowed"] else "COMPLETE_REVIEW_BEFORE_ADOPTION_OR_RELEASE",
            "recommendation": "MAINTAIN_WITH_CLAIM_LIMITS" if identity["adoption_allowed"] else "HOLD_PENDING_REVIEW",
        })
    for domain in sorted(registry["domains"], key=lambda item: item["domain"]):
        rows.append({
            "kind": "DOMAIN",
            "id": domain["entity_id"],
            "display_name": domain["domain"],
            "role": "DOMAIN",
            "lifecycle": "owned_inventory_unverified",
            "state": domain["classification"],
            "trademark_state": "NOT_A_CLEARANCE_SIGNAL",
            "adoption_allowed": domain["adoption_allowed"],
            "domain": domain["domain"],
            "release_blocker": "NONE" if domain["adoption_allowed"] else "DOMAIN_ADOPTION_NOT_ALLOWED",
            "required_action": _domain_recommendation(domain),
            "recommendation": _domain_recommendation(domain),
        })
    return {
        "schema_version": 1,
        "as_of": registry["as_of"],
        "source": ".factory/identity-registry.json",
        "legal_conclusion": "NONE",
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=ROOT / ".factory/identity-registry.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    matrix = build_matrix(json.loads(args.registry.read_text(encoding="utf-8")))
    rendered = json.dumps(matrix, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
