#!/usr/bin/env python3
"""Shared evidence-strength vocabulary; stronger claims require stronger evidence."""

from __future__ import annotations

EVIDENCE_LEVELS = (
    "UNVERIFIED",
    "SCHEMA_VALID",
    "UNIT_TESTED",
    "INTEGRATION_TESTED",
    "SIMULATED",
    "SANDBOX_VERIFIED",
    "DEVICE_VERIFIED",
    "REAL_WORLD_VERIFIED",
    "HUMAN_AUTHORITY",
)


def evidence_levels(product: dict) -> dict[str, str]:
    evidence = product.get("evidence", {})
    return {
        "registry": "SCHEMA_VALID",
        "local_implementation": "UNIT_TESTED" if evidence.get("tests") else "UNVERIFIED",
        "simulator": "SIMULATED" if evidence.get("simulator") else "UNVERIFIED",
        "sandbox_or_pipeline": "SANDBOX_VERIFIED" if evidence.get("processed_build") else "UNVERIFIED",
        "device": "DEVICE_VERIFIED" if evidence.get("device") else "UNVERIFIED",
        "real_world": "REAL_WORLD_VERIFIED" if evidence.get("external_testflight") else "UNVERIFIED",
        "release_authority": "HUMAN_AUTHORITY" if product.get("human_authorized") else "UNVERIFIED",
    }


def validate_levels(levels: dict[str, str]) -> list[str]:
    return [f"{key}: invalid evidence level {value}" for key, value in levels.items() if value not in EVIDENCE_LEVELS]
