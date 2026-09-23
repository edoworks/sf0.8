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
    "legal_entity",
    "brand",
    "trademark_application",
    "contact_point",
    "address_policy",
}

DURABLE_FIELDS = {
    "entity_id", "bundle_id", "app_store_id", "repository_id", "domain",
    "serial_number", "state_entity_number", "path",
}

IDENTITY_STATES = {"ESTABLISHED", "ADOPTED", "PROVISIONAL", "CLEARANCE_REQUIRED", "HISTORICAL", "RETIRED"}
TRADEMARK_STATES = {
    "INTERNAL", "PROVISIONAL", "CLEARANCE_REQUIRED", "CLEARED", "FILED",
    "REGISTERED", "LEGAL_REVIEW_REQUIRED", "ABANDONED", "RETIRED",
}
DOMAIN_CLASSIFICATIONS = {
    "CORE", "DEFENSIVE", "PRODUCT", "DO_NOT_USE_AS_BRAND", "REVIEW",
    "RETIRE_CANDIDATE", "CANDIDATE", "EXPERIMENT",
}
ADDRESS_CATEGORIES = {
    "PUBLIC_CONTACT", "PUBLIC_MAILING_ADDRESS", "REGISTERED_AGENT",
    "LEGAL_ENTITY_ADDRESS", "PRIVATE_DOMICILE",
}


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


def validate_governed_identity(entity: dict[str, Any]) -> list[str]:
    """Validate the shared state vocabulary used by the identity registry."""
    errors = validate_entity(entity)
    if "identity_state" in entity and entity["identity_state"] not in IDENTITY_STATES:
        errors.append("identity_state must be supported")
    if "trademark_state" in entity and entity["trademark_state"] not in TRADEMARK_STATES:
        errors.append("trademark_state must be supported")
    if "classification" in entity and entity["classification"] not in DOMAIN_CLASSIFICATIONS:
        errors.append("domain classification must be supported")
    if "category" in entity and entity["category"] not in ADDRESS_CATEGORIES:
        errors.append("address category must be supported")
    return errors


def relation(left: str, relation_type: str, right: str, provenance: list[str]) -> dict[str, Any]:
    return {
        "from": left,
        "type": relation_type,
        "to": right,
        "provenance": provenance,
    }
