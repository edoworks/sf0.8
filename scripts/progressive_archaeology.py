#!/usr/bin/env python3
"""Cheap, bounded candidate triage for portfolio archaeology."""

from __future__ import annotations

import re
from typing import Any


CLASSIFICATIONS = {
    "TRIVIAL/GENERATED",
    "DUPLICATE",
    "HISTORICAL IMPLEMENTATION",
    "MEANINGFUL EXPERIMENT",
    "RELEASED PRODUCT",
    "REJECTED SUBMISSION",
    "REUSABLE-CAPABILITY CANDIDATE",
    "UNKNOWN",
}

DEFAULT_MAX_DEEP_CANDIDATES = 4
GENERATED_RE = re.compile(r"(?:derived|generated|build|deriveddata|xcresult|preview|fixture)", re.I)


def dedupe_key(candidate: dict[str, Any]) -> str:
    bundle_ids = candidate.get("bundle_ids") or []
    repositories = (candidate.get("repository") or {}).get("repository_id")
    if bundle_ids:
        return f"bundle:{bundle_ids[0]}"
    if repositories:
        return f"repo:{repositories}"
    return f"path:{candidate.get('local_path') or candidate.get('path') or candidate.get('product_id') or candidate.get('identity')}"


def classify(candidate: dict[str, Any]) -> str:
    text = " ".join(
        str(candidate.get(field, ""))
        for field in ("identity", "product_id", "display_name", "path", "local_path", "scope", "kind")
    )
    states = " ".join(str(item) for item in candidate.get("distribution_states", []))
    if candidate.get("duplicate_of"):
        return "DUPLICATE"
    if GENERATED_RE.search(text):
        return "TRIVIAL/GENERATED"
    if any(token in states.casefold() for token in ("rejected", "developer rejected", "removed")):
        return "REJECTED SUBMISSION"
    if any(token in states.casefold() for token in ("ready for sale", "testflight", "released", "approved")):
        return "RELEASED PRODUCT"
    if candidate.get("reusable_capability") is True:
        return "REUSABLE-CAPABILITY CANDIDATE"
    if candidate.get("experiment") is True or "experiment" in text.casefold() or "prototype" in text.casefold():
        return "MEANINGFUL EXPERIMENT"
    if candidate.get("historical") is True or candidate.get("scope") in {"historical", "foculoom/.archived"}:
        return "HISTORICAL IMPLEMENTATION"
    return "UNKNOWN"


def expected_knowledge_value(classification: str) -> int:
    return {
        "REJECTED SUBMISSION": 5,
        "RELEASED PRODUCT": 5,
        "REUSABLE-CAPABILITY CANDIDATE": 4,
        "MEANINGFUL EXPERIMENT": 4,
        "HISTORICAL IMPLEMENTATION": 3,
        "DUPLICATE": 1,
        "TRIVIAL/GENERATED": 0,
        "UNKNOWN": 0,
    }[classification]


def triage(candidates: list[dict[str, Any]], max_deep_candidates: int = DEFAULT_MAX_DEEP_CANDIDATES) -> dict[str, Any]:
    if max_deep_candidates < 0:
        raise ValueError("max_deep_candidates must not be negative")
    rows: list[dict[str, Any]] = []
    seen: dict[str, str] = {}
    for candidate in candidates:
        key = dedupe_key(candidate)
        classification = classify(candidate)
        duplicate_of = seen.get(key)
        if duplicate_of:
            classification = "DUPLICATE"
        else:
            seen[key] = str(candidate.get("product_id") or candidate.get("identity") or key)
        value = expected_knowledge_value(classification)
        rows.append(
            {
                "candidate": candidate.get("product_id") or candidate.get("identity"),
                "dedupe_key": key,
                "classification": classification,
                "analysis_stage": "METADATA_ONLY",
                "estimated_cost_units": 1,
                "expected_knowledge_value": value,
                "knowledge_value_per_cost": value,
                "duplicate_of": duplicate_of,
                "deep_analysis_eligible": value >= 3 and classification != "UNKNOWN",
                "deletion_eligible": False,
            }
        )
    eligible = [row for row in rows if row["deep_analysis_eligible"]]
    eligible.sort(key=lambda row: (-row["knowledge_value_per_cost"], str(row["candidate"])))
    selected = {id(row) for row in eligible[:max_deep_candidates]}
    for row in rows:
        row["deep_analysis_selected"] = id(row) in selected
    return {
        "schema_version": 1,
        "policy": {
            "stage_1": "METADATA_ONLY",
            "max_deep_candidates": max_deep_candidates,
            "unknown_fails_closed": True,
            "deletion_during_triage": False,
        },
        "candidate_count": len(rows),
        "selected_deep_count": sum(row["deep_analysis_selected"] for row in rows),
        "rows": rows,
    }
