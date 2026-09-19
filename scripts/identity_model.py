"""Small durable identity model shared by portfolio discovery and reconciliation."""

from __future__ import annotations

from typing import Any


ENTITY_KINDS = {
    "company",
    "product",
    "repository",
    "local_folder",
    "bundle_identifier",
    "app_store_application",
    "app_store_release",
    "website_domain",
    "package_component",
    "historical_product",
    "experiment",
    "reusable_artifact",
}

DURABLE_FIELDS = {"entity_id", "bundle_id", "app_store_id", "repository_id", "domain", "path"}


def validate_entity(entity: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if entity.get("entity_type") not in ENTITY_KINDS:
        errors.append("entity_type must be a supported identity kind")
    if not str(entity.get("entity_id", "")).strip():
        errors.append("entity_id is required")
    if not any(entity.get(field) for field in DURABLE_FIELDS):
        errors.append("at least one durable identifier is required")
    if not isinstance(entity.get("provenance"), list) or not entity["provenance"]:
        errors.append("provenance is required")
    return errors


def relation(left: str, relation_type: str, right: str, provenance: list[str]) -> dict[str, Any]:
    return {
        "from": left,
        "type": relation_type,
        "to": right,
        "provenance": provenance,
    }
