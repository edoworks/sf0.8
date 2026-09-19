#!/usr/bin/env python3
"""Small, domain-neutral gates for crossing from reasoning to human evidence."""

from __future__ import annotations

from typing import Any

MACHINE_CLASSES = {"PUBLIC_RESEARCH", "COMPETITOR_EVIDENCE", "REVIEWS", "TECHNICAL_FEASIBILITY", "PUBLIC_PRICING", "EXISTING_ALTERNATIVE"}
EXTERNAL_CLASSES = {"OBSERVED_BEHAVIOR", "INTERVIEW", "WORKFLOW_OBSERVATION", "LEARNING_OUTCOME", "REPEATED_USAGE_REQUEST", "DEPOSIT", "PREORDER", "PURCHASE", "REPEAT_PURCHASE"}
PAYMENT_LADDER = ("NONE", "INTEREST", "CONTACT_EXCHANGE", "REQUEST_FOR_ACCESS", "RETURN_REQUEST", "REFERRAL", "DEPOSIT", "PREORDER", "PURCHASE", "REPEAT_PURCHASE")


def validate_frontier(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    frontier = record.get("evidence_frontier", {})
    if frontier.get("reached") is not True:
        errors.append("evidence frontier must be reached before autonomous research stops")
    if not set(frontier.get("machine_obtainable", [])) >= MACHINE_CLASSES:
        errors.append("machine-obtainable evidence classes are incomplete")
    if not frontier.get("external_human_required"):
        errors.append("frontier must name external human evidence requirements")
    for hypothesis in record.get("hypotheses", []):
        if hypothesis.get("state") in {"HYPOTHESIS", "VALIDATION-READY"} and not hypothesis.get("experiment"):
            errors.append(f"{hypothesis.get('id')}: active hypothesis requires a human experiment")
    return errors


def validate_result(result: dict[str, Any]) -> list[str]:
    required = {"hypothesis_id", "experiment_id", "participant_source", "observations", "behavior_change", "learning_evidence", "payment_signal"}
    errors = [f"missing result field: {key}" for key in sorted(required - result.keys())]
    if result.get("participant_source") != "EXTERNAL_HUMAN":
        errors.append("results must come from external human participants")
    if result.get("synthetic") is True or result.get("generated_by_model") is True:
        errors.append("synthetic or model-generated observations cannot satisfy evidence gates")
    if not isinstance(result.get("observations"), list) or not result.get("observations"):
        errors.append("raw observations are required")
    payment = result.get("payment_signal", {})
    if payment.get("stage") not in PAYMENT_LADDER:
        errors.append("payment signal must preserve the observed monetization ladder stage")
    if not isinstance(result.get("consent", {}), dict):
        errors.append("consent record is required")
    return errors


def apply_result(record: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    errors = validate_result(result)
    if errors:
        raise ValueError("; ".join(errors))
    updated = dict(record)
    updated["results"] = [*record.get("results", []), result]
    for hypothesis in updated.get("hypotheses", []):
        if hypothesis.get("id") == result["hypothesis_id"]:
            hypothesis["results"] = [*hypothesis.get("results", []), result["experiment_id"]]
            hypothesis["last_outcome"] = result.get("outcome", "UNRESOLVED")
    learning = dict(updated.get("factory_learning", {}))
    learning.setdefault("external_observations", []).append(result["result_id"])
    learning.setdefault("behavior_change_evidence", []).append(result["behavior_change"])
    learning.setdefault("learning_effect_evidence", []).append(result["learning_evidence"])
    learning.setdefault("willingness_to_pay_evidence", []).append(result["payment_signal"])
    learning.setdefault("failed_assumptions", []).extend(result.get("falsified_assumptions", []))
    updated["factory_learning"] = learning
    return updated
