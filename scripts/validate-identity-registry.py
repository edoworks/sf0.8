#!/usr/bin/env python3
"""Validate canonical identity governance and portfolio lifecycle agreement."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any

from identity_model import (
    ADDRESS_CATEGORIES,
    DOMAIN_CLASSIFICATIONS,
    IDENTITY_STATES,
    TRADEMARK_STATES,
    validate_governed_identity,
)


ROOT = Path(__file__).resolve().parents[1]
UNRESOLVED_TRADEMARK_STATES = {"PROVISIONAL", "CLEARANCE_REQUIRED", "LEGAL_REVIEW_REQUIRED"}
NON_ADOPTABLE_DOMAIN_CLASSES = {
    "DEFENSIVE", "DO_NOT_USE_AS_BRAND", "REVIEW", "RETIRE_CANDIDATE", "CANDIDATE", "EXPERIMENT",
}
SUPPORTED_OWNER_NAMES = {"Foculoom LLC", "Movotosa Ojiru"}
PRIVATE_VALUE_KEYS = {"address", "street", "street_address", "city", "postal_code", "zip", "region", "state"}
PRIVATE_METADATA_KEYS = {
    "entity_type", "entity_id", "category", "storage", "public", "repository_allowed", "provenance",
}


def portfolio_lifecycles(text: str) -> dict[tuple[str, str], str]:
    """Extract only the section, durable id, and lifecycle from simple portfolio YAML."""
    records: dict[tuple[str, str], str] = {}
    section = ""
    item_id: str | None = None
    for line in text.splitlines():
        section_match = re.match(r"^([a-z_]+):$", line)
        if section_match:
            section = section_match.group(1)
            item_id = None
            continue
        id_match = re.match(r"^  - id:\s*(\S+)", line)
        if id_match:
            item_id = id_match.group(1)
            continue
        lifecycle_match = re.match(r"^    lifecycle:\s*(\S+)", line)
        if item_id and lifecycle_match:
            records[(section, item_id)] = lifecycle_match.group(1)
    return records


def _duplicates(values: list[str]) -> set[str]:
    return {value for value in values if values.count(value) > 1}


def validate(registry: dict[str, Any], portfolio_text: str) -> list[str]:
    errors: list[str] = []
    if registry.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    for field in ("authority", "legal_entity", "contacts", "address_policies", "identities", "trademarks", "domains"):
        if field not in registry:
            errors.append(f"missing required registry field: {field}")

    legal_entity = registry.get("legal_entity", {})
    if legal_entity.get("legal_name") != "Foculoom LLC":
        errors.append("canonical legal owner must be Foculoom LLC")
    if legal_entity.get("state_entity_number") != "20260100384":
        errors.append("California entity number disagrees with owner-provided fact")
    if legal_entity.get("formed_on") != "2026-02-26":
        errors.append("formation date disagrees with owner-provided fact")
    if legal_entity.get("registered_agent_name") != "Northwest Registered Agent, Inc.":
        errors.append("registered agent disagrees with owner-provided fact")
    contacts = {item.get("email") for item in registry.get("contacts", [])}
    expected_contacts = {"hello@foculoom.com", "support@foculoom.com", "billing@foculoom.com"}
    if contacts != expected_contacts:
        errors.append("canonical role-based contacts are incomplete or unsupported")

    groups = [registry.get(name, []) for name in ("contacts", "address_policies", "identities", "trademarks", "domains")]
    records = [legal_entity] + [record for group in groups for record in group]
    entity_ids = [record.get("entity_id", "") for record in records]
    for duplicate in sorted(_duplicates(entity_ids)):
        errors.append(f"duplicate durable entity identity: {duplicate}")
    for record in records:
        errors.extend(f"{record.get('entity_id', '<unknown>')}: {error}" for error in validate_governed_identity(record))

    private_records = [item for item in registry.get("address_policies", []) if item.get("category") == "PRIVATE_DOMICILE"]
    if len(private_records) != 1:
        errors.append("exactly one PRIVATE_DOMICILE metadata policy is required")
    for record in private_records:
        exposed = PRIVATE_VALUE_KEYS & set(record)
        if exposed or set(record) - PRIVATE_METADATA_KEYS:
            errors.append("PRIVATE_DOMICILE must contain metadata only, not address fields")
        if record.get("repository_allowed") is not False or record.get("public") is not False or record.get("storage") != "EXTERNAL_SECURE_RECORD":
            errors.append("PRIVATE_DOMICILE must prohibit repository values and reference external secure storage")
    categories = {record.get("category") for record in registry.get("address_policies", [])}
    if categories != ADDRESS_CATEGORIES or len(registry.get("address_policies", [])) != len(ADDRESS_CATEGORIES):
        errors.append("address policies must cover every canonical category exactly once")

    lifecycles = portfolio_lifecycles(portfolio_text)
    for identity in registry.get("identities", []):
        if identity.get("identity_state") not in IDENTITY_STATES:
            errors.append(f"unsupported identity state: {identity.get('entity_id')}")
        if identity.get("trademark_state") not in TRADEMARK_STATES:
            errors.append(f"unsupported trademark state: {identity.get('entity_id')}")
        if identity.get("owner_entity_id") != legal_entity.get("entity_id"):
            errors.append(f"unsupported identity owner: {identity.get('entity_id')}")
        if identity.get("trademark_state") in UNRESOLVED_TRADEMARK_STATES and identity.get("adoption_allowed") is not False:
            errors.append(f"unresolved clearance must block adoption: {identity.get('entity_id')}")
        reference = identity.get("portfolio_ref")
        if reference:
            key = (reference.get("section", ""), reference.get("id", ""))
            if key not in lifecycles:
                errors.append(f"portfolio reference does not resolve: {identity.get('entity_id')}")
            elif lifecycles[key] != identity.get("lifecycle"):
                errors.append(f"portfolio lifecycle contradiction: {identity.get('entity_id')}")

    serials = [record.get("serial_number", "") for record in registry.get("trademarks", [])]
    for duplicate in sorted(_duplicates(serials)):
        errors.append(f"duplicate trademark serial: {duplicate}")
    for mark in registry.get("trademarks", []):
        if mark.get("state") not in TRADEMARK_STATES:
            errors.append(f"unsupported trademark application state: {mark.get('entity_id')}")
        if mark.get("owner_name") not in SUPPORTED_OWNER_NAMES:
            errors.append(f"unsupported trademark owner: {mark.get('entity_id')}")
        if mark.get("registration_claimed") is not False:
            if mark.get("state") != "REGISTERED" or not mark.get("registration_number"):
                errors.append(f"unverified registration claim: {mark.get('entity_id')}")
        if mark.get("state") == "REGISTERED" and not mark.get("registration_number"):
            errors.append(f"REGISTERED mark lacks registration evidence: {mark.get('entity_id')}")

    domains = [record.get("domain", "") for record in registry.get("domains", [])]
    for duplicate in sorted(_duplicates(domains)):
        errors.append(f"duplicate domain identity: {duplicate}")
    for domain in registry.get("domains", []):
        classification = domain.get("classification")
        if classification not in DOMAIN_CLASSIFICATIONS:
            errors.append(f"unsupported domain classification: {domain.get('entity_id')}")
        if classification in NON_ADOPTABLE_DOMAIN_CLASSES and domain.get("adoption_allowed") is not False:
            errors.append(f"unresolved or restricted domain must block adoption: {domain.get('domain')}")
        if domain.get("entity_id") != f"domain:{domain.get('domain')}":
            errors.append(f"domain durable identity disagrees: {domain.get('domain')}")
    return errors


def main() -> None:
    registry = json.loads((ROOT / ".factory/identity-registry.json").read_text(encoding="utf-8"))
    portfolio = (ROOT / ".factory/portfolio.yaml").read_text(encoding="utf-8")
    errors = validate(registry, portfolio)
    if errors:
        raise SystemExit("identity registry validation failed:\n- " + "\n- ".join(errors))
    print("identity registry validation passed")


if __name__ == "__main__":
    main()
