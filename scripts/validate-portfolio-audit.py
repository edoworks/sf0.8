#!/usr/bin/env python3
"""Validate archaeology, preservation, Apple-history, and lane artifacts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / ".factory" / "artifacts" / "portfolio-archaeology"
POLICY = ARTIFACTS / "progressive-policy.json"


def load(name: str) -> dict:
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


def main() -> int:
    inventory = load("inventory.json")
    manifests = load("preservation-manifests.json")["manifests"]
    knowledge = load("knowledge-records.json")["records"]
    report = load("audit-report.json")
    apple = load("apple-history.json")
    lanes = load("parallel-lanes.json")
    fixture = load("fixtures/vorynce-rejection.json")
    reuse_mining = load("reuse-mining.json")
    priority = load("prioritized-reuse-batch.json")
    portfolio_reconciliation = load("portfolio-reconciliation.json")
    exercise = load("archive-candidate-exercise.json")
    policy = json.loads(POLICY.read_text(encoding="utf-8"))

    reconciliation = inventory["reconciliation"]
    expected_manifests = (
        len(inventory["local_candidates"])
        + len(inventory["factory_roots"])
        + len(inventory["historical_apple_apps"])
    )
    assert len(manifests) == expected_manifests
    assert len(knowledge) == report["knowledge"]["queryable_records"]
    assert reconciliation["historical_apple_count"] == 11
    assert reconciliation["canonical_apple_count"] == 2
    assert len(reconciliation["historical_apple_missing_from_canonical"]) == 10
    assert len(inventory["canonical"]["historical_product_ids"]) == 10
    assert all(manifest["deletion_authorized"] is False for manifest in manifests)
    assert report["deletion_performed"] is False
    assert apple["submission_performed"] is False
    assert apple["current_reviewer_comparison"]["regression_fixture_candidate"]["fixture_status"] == "IMPLEMENTED_AND_TESTED"
    assert fixture["historical_evidence_only"] is True
    assert len(reuse_mining["findings"]) >= 4
    assert reuse_mining["remaining_investigation"]["count"] == report["knowledge"]["preservation_manifests"]
    assert report["knowledge"]["unassessed_substantial_artifacts"] == 0
    assert priority["batch"][0]["candidate"] == "vorynce-rebuild"
    assert priority["remaining_count"] == report["knowledge"]["preservation_manifests"]
    assert priority["deletion_authorized"] is False
    assert lanes["uncontrolled_swarm"] is False
    assert lanes["safe_concurrency"]["idle_despite_ready_work"] == 0
    assert {item["id"] for item in portfolio_reconciliation["entries"]} >= {
        "edoworks/sf0.8", "edoworks/product-a", "edoworks/rung", "edoworks/edoworks.github.io",
        "edoworks/factory-constitution", "edoworks/asc-client", "edoworks/trycycle",
    }
    assert exercise["deletion_authorized"] is False
    assert exercise["destructive_action_performed"] is False
    assert exercise["exercised_transitions"][0]["result"] == "BLOCKED_INCOMPLETE_EVIDENCE"
    assert policy["stage_1"] == "METADATA_ONLY"
    assert policy["max_deep_candidates"] > 0
    assert policy["unknown_fails_closed"] is True
    assert policy["deletion_during_triage"] is False
    governance = report["governance"]
    assert governance["untracked_material_work"] == 0
    assert governance["unprioritized_material_work"] == 0
    assert governance["closed_without_evidence"] == 0
    assert governance["deletion_without_knowledge_extraction"] == 0
    assert governance["unauthorized_destructive_actions"] == 0
    print("portfolio audit validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
