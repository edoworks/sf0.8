#!/usr/bin/env python3
"""Govern capability inventory, primitive hypotheses, and learning evidence."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


STRATEGIC_CLASSES = {
    "INTERNAL_ADVANTAGE",
    "OPEN_DISTRIBUTION",
    "DEVELOPER_PRIMITIVE",
    "METERED_INFRASTRUCTURE",
    "PRODUCT_CANDIDATE",
    "INSUFFICIENT_EVIDENCE",
}
EVIDENCE_LEVELS = ("problem", "usage", "retention", "economic", "payment")
EVIDENCE_STATES = {"UNKNOWN", "ABSENT", "PRESENT"}
SENSITIVITY = {"LOW", "MEDIUM", "HIGH", "UNKNOWN"}
EXPERIMENTS = {
    "NONE",
    "INTERVIEW",
    "WORKFLOW_OBSERVATION",
    "LOCAL_CLI_TEST",
    "PRIVATE_PACKAGE",
    "PRIVATE_PLUGIN",
    "PRIVATE_API",
    "CONTROLLED_MCP",
    "MANUAL_SERVICE",
    "LANDING_PAGE",
    "WAITLIST",
    "PAID_PILOT",
    "PRECOMMITMENT",
    "PAYMENT_ATTEMPT",
}
EXTERNALIZATION_STATES = {"NOT_PROPOSED", "PROPOSED", "BLOCKED", "HUMAN_AUTHORIZED"}
REACH_SIGNAL_TYPES = {"DOWNLOAD", "VERIFIED_EXECUTION"}
AUDIENCE_TYPES = {"FOUNDER", "NON_FOUNDER", "AUTOMATED", "UNKNOWN"}

REQUIRED_RECORD_FIELDS = {
    "id",
    "capability_name",
    "source_repository_project",
    "source_records",
    "opportunity_ids",
    "original_internal_purpose",
    "current_consumers",
    "recurrence",
    "problem_solved",
    "inputs",
    "outputs",
    "dependencies",
    "maturity",
    "internal_operating_cost",
    "known_alternatives",
    "differentiation_hypothesis",
    "potential_external_users",
    "possible_external_workflows",
    "standalone_usefulness",
    "composability",
    "surface_feasibility",
    "telemetry_learning_potential",
    "strategic_sensitivity",
    "security_privacy_implications",
    "operational_burden",
    "evidence",
    "confidence",
    "unresolved_questions",
    "recommended_next_evidence_action",
    "strategic_classification",
    "externalization",
    "learning_records",
    "external_usage_evidence",
}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _list(value: Any) -> bool:
    return isinstance(value, list)


def _unknown_safe(value: Any) -> bool:
    return _text(value) or value == "UNKNOWN"


def _validate_evidence(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    evidence = record.get("evidence")
    if not isinstance(evidence, dict):
        return ["evidence must be an object"]
    for level in EVIDENCE_LEVELS:
        item = evidence.get(level)
        prefix = f"evidence.{level}"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        if item.get("status") not in EVIDENCE_STATES:
            errors.append(f"{prefix}.status is invalid")
        if item.get("status") == "PRESENT" and not _list(item.get("sources")):
            errors.append(f"{prefix}.sources are required for PRESENT evidence")
        if item.get("status") == "UNKNOWN" and item.get("sources"):
            errors.append(f"{prefix}.UNKNOWN cannot contain evidence sources")
    return errors


def validate_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_RECORD_FIELDS - record.keys())
    errors.extend(f"missing {field}" for field in missing)
    if missing:
        return errors
    if not _text(record["id"]) or not _text(record["capability_name"]):
        errors.append("id and capability_name must be non-empty")
    if not _list(record["source_records"]) or not record["source_records"]:
        errors.append("source_records must be a non-empty list")
    for field in (
        "current_consumers",
        "inputs",
        "outputs",
        "dependencies",
        "known_alternatives",
        "potential_external_users",
        "possible_external_workflows",
        "unresolved_questions",
        "learning_records",
        "opportunity_ids",
        "external_usage_evidence",
    ):
        if not _list(record[field]):
            errors.append(f"{field} must be a list")
    for field in (
        "original_internal_purpose",
        "problem_solved",
        "maturity",
        "internal_operating_cost",
        "differentiation_hypothesis",
        "standalone_usefulness",
        "composability",
        "telemetry_learning_potential",
        "security_privacy_implications",
        "operational_burden",
        "confidence",
        "recommended_next_evidence_action",
    ):
        if not _unknown_safe(record[field]):
            errors.append(f"{field} must be explicit or UNKNOWN")
    feasibility = record["surface_feasibility"]
    if not isinstance(feasibility, dict):
        errors.append("surface_feasibility must be an object")
    else:
        for surface in ("cli", "api", "sdk_library", "plugin_mcp_skill", "open_source", "hosted_service"):
            if not _unknown_safe(feasibility.get(surface)):
                errors.append(f"surface_feasibility.{surface} must be explicit or UNKNOWN")
    if record["strategic_sensitivity"] not in SENSITIVITY:
        errors.append("strategic_sensitivity is invalid")
    if record["strategic_classification"] not in STRATEGIC_CLASSES:
        errors.append("strategic_classification is invalid")
    errors.extend(_validate_evidence(record))

    gate = record["externalization"]
    if not isinstance(gate, dict):
        errors.append("externalization must be an object")
    else:
        if gate.get("status") not in EXTERNALIZATION_STATES:
            errors.append("externalization.status is invalid")
        experiment = gate.get("smallest_reversible_experiment")
        if experiment not in EXPERIMENTS:
            errors.append("externalization.smallest_reversible_experiment is invalid")
        for field in ("risk_review", "learning_objective", "authorization_required"):
            if not _text(gate.get(field)):
                errors.append(f"externalization.{field} is required")
        if gate.get("human_authorized") is True:
            errors.append("inventory cannot authorize externalization")
        if record["strategic_sensitivity"] in {"MEDIUM", "HIGH"} and gate.get("status") == "HUMAN_AUTHORIZED":
            errors.append("sensitive capabilities cannot be authorized by inventory")
        if gate.get("status") == "PROPOSED" and experiment == "NONE":
            errors.append("PROPOSED externalization requires a real experiment")
    return errors


def validate_inventory(inventory: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if inventory.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    reach_signals = inventory.get("reach_signals", [])
    if not isinstance(reach_signals, list):
        errors.append("reach_signals must be a list")
    else:
        signal_ids: set[str] = set()
        for signal in reach_signals:
            if not isinstance(signal, dict):
                errors.append("reach signal must be an object")
                continue
            signal_id = signal.get("signal_id")
            if signal_id in signal_ids:
                errors.append(f"duplicate reach signal: {signal_id}")
            signal_ids.add(signal_id)
            errors.extend(f"{signal_id}: {error}" for error in validate_reach_signal(signal))
    records = inventory.get("capabilities")
    if not isinstance(records, list) or not records:
        return errors + ["capabilities must be a non-empty list"]
    ids: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            errors.append("capability record must be an object")
            continue
        identity = record.get("id")
        if identity in ids:
            errors.append(f"duplicate capability id: {identity}")
        ids.add(identity)
        errors.extend(f"{identity}: {error}" for error in validate_record(record))
    return errors


def validate_reach_signal(signal: dict[str, Any]) -> list[str]:
    required = {
        "signal_id", "primitive_id", "signal_type", "observed_at", "artifact_revision",
        "source", "audience", "consent", "verified_execution", "workflow", "job_to_be_done",
    }
    errors = [f"missing {field}" for field in sorted(required - signal.keys())]
    if errors:
        return errors
    if signal["signal_type"] not in REACH_SIGNAL_TYPES:
        errors.append("signal_type is invalid")
    if signal["audience"] not in AUDIENCE_TYPES:
        errors.append("audience is invalid")
    for field in ("signal_id", "primitive_id", "observed_at", "artifact_revision", "source"):
        if not _text(signal[field]):
            errors.append(f"{field} must be non-empty")
    if not isinstance(signal["consent"], dict):
        errors.append("consent must be an object")
    consent_status = signal["consent"].get("status") if isinstance(signal["consent"], dict) else None
    if consent_status not in {"NOT_APPLICABLE", "OPT_IN", "UNKNOWN"}:
        errors.append("consent.status is invalid")
    if not isinstance(signal["verified_execution"], bool):
        errors.append("verified_execution must be boolean")
    if signal["signal_type"] == "DOWNLOAD":
        if signal["verified_execution"] is True:
            errors.append("downloads cannot claim verified execution")
        if signal["audience"] == "NON_FOUNDER" and consent_status == "OPT_IN":
            errors.append("download identity and consent cannot be used as execution evidence")
    if signal["signal_type"] == "VERIFIED_EXECUTION":
        if signal["verified_execution"] is not True:
            errors.append("verified execution signals require verified_execution=true")
        if signal["audience"] != "NON_FOUNDER":
            errors.append("verified execution requires a non-founder audience")
        if consent_status != "OPT_IN":
            errors.append("verified execution requires explicit opt-in consent")
        if not _text(signal["workflow"]) or not _text(signal["job_to_be_done"]):
            errors.append("verified execution requires workflow and job_to_be_done")
    return errors


def apply_reach_signal(inventory: dict[str, Any], signal: dict[str, Any]) -> dict[str, Any]:
    errors = validate_reach_signal(signal)
    errors.extend(validate_inventory(inventory))
    if errors:
        raise ValueError("; ".join(errors))
    updated = deepcopy(inventory)
    if any(item.get("signal_id") == signal["signal_id"] for item in updated.get("reach_signals", [])):
        raise ValueError(f"duplicate reach signal: {signal['signal_id']}")
    target = next((item for item in updated["capabilities"] if item.get("id") == signal["primitive_id"]), None)
    if target is None:
        raise ValueError(f"reach signal references unknown primitive: {signal['primitive_id']}")
    updated.setdefault("reach_signals", []).append(signal)
    if signal["signal_type"] == "VERIFIED_EXECUTION":
        target.setdefault("external_usage_evidence", []).append(signal["signal_id"])
        target["evidence"]["usage"] = {"status": "PRESENT", "sources": [*target["evidence"]["usage"].get("sources", []), signal["signal_id"]]}
    return updated


def classify(record: dict[str, Any]) -> str:
    """Return a conservative classification; no evidence means insufficient."""
    if record.get("strategic_sensitivity") == "HIGH":
        return "INTERNAL_ADVANTAGE"
    evidence = record.get("evidence", {})
    payment = evidence.get("payment", {}).get("status")
    usage = evidence.get("usage", {}).get("status")
    problem = evidence.get("problem", {}).get("status")
    if payment == "PRESENT" and usage == "PRESENT":
        return "METERED_INFRASTRUCTURE"
    if usage == "PRESENT" and problem == "PRESENT":
        return "DEVELOPER_PRIMITIVE"
    return "INSUFFICIENT_EVIDENCE"


def validate_learning_record(result: dict[str, Any]) -> list[str]:
    required = {
        "result_id", "primitive_id", "user", "workflow", "job_to_be_done", "frequency",
        "friction", "combinations", "problem_observed", "usage_observed", "repeated_use",
        "economic_value_observed", "value_created", "payment_signal", "consent", "synthetic",
    }
    errors = [f"missing {field}" for field in sorted(required - result.keys())]
    if result.get("synthetic") is True:
        errors.append("synthetic learning cannot update external evidence")
    for field in ("problem_observed", "usage_observed", "repeated_use", "economic_value_observed"):
        if not isinstance(result.get(field), bool):
            errors.append(f"{field} must be an explicit boolean")
    if not _text(result.get("user")) or not _text(result.get("workflow")) or not _text(result.get("job_to_be_done")):
        errors.append("user, workflow, and job_to_be_done are required")
    payment = result.get("payment_signal")
    if not isinstance(payment, dict):
        errors.append("payment_signal must be an object")
    elif payment.get("stage") not in {"NONE", "INTEREST", "CONTACT_EXCHANGE", "REQUEST_FOR_ACCESS", "RETURN_REQUEST", "REFERRAL", "DEPOSIT", "PREORDER", "PURCHASE", "REPEAT_PURCHASE"}:
        errors.append("payment_signal.stage is invalid")
    if not isinstance(result.get("consent"), dict):
        errors.append("consent must be an object")
    return errors


def apply_learning(inventory: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    """Append an admissible observation without promoting unrelated evidence."""
    errors = validate_learning_record(result)
    if errors:
        raise ValueError("; ".join(errors))
    updated = deepcopy(inventory)
    if any(result["result_id"] in item.get("learning_records", []) for item in updated["capabilities"]):
        raise ValueError(f"duplicate learning result: {result['result_id']}")
    target = next((item for item in updated["capabilities"] if item.get("id") == result["primitive_id"]), None)
    if target is None:
        raise ValueError("learning record references an unknown primitive")
    target.setdefault("learning_records", []).append(result["result_id"])
    source = result["result_id"]
    target["evidence"]["problem"] = {"status": "PRESENT" if result["problem_observed"] else "ABSENT", "sources": [source]}
    target["evidence"]["usage"] = {"status": "PRESENT" if result["usage_observed"] else "ABSENT", "sources": [source]}
    target["evidence"]["retention"] = {"status": "PRESENT" if result["repeated_use"] else "ABSENT", "sources": [source]}
    target["evidence"]["economic"] = {"status": "PRESENT" if result["economic_value_observed"] else "ABSENT", "sources": [source]}
    payment = result.get("payment_signal", {}).get("stage")
    target["evidence"]["payment"] = {
        "status": "PRESENT" if payment in {"DEPOSIT", "PREORDER", "PURCHASE", "REPEAT_PURCHASE"} else "ABSENT",
        "sources": [source],
    }
    return updated


def apply_learning_to_opportunities(ledger: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    """Update linked opportunity evidence only from explicit learning fields."""
    errors = validate_learning_record(result)
    if errors:
        raise ValueError("; ".join(errors))
    updated = deepcopy(ledger)
    targets = set(result.get("opportunity_ids", []))
    candidates = {item.get("id"): item for item in updated.get("candidates", [])}
    unknown = sorted(targets - candidates.keys())
    if unknown:
        raise ValueError(f"learning record references unknown opportunities: {', '.join(unknown)}")
    for candidate_id in targets:
        candidate = candidates[candidate_id]
        existing_sources = {item.get("source") for item in candidate.get("evidence", []) if isinstance(item, dict)}
        if result["problem_observed"] and candidate["external_evidence"].get("status") != "PRESENT":
            candidate["external_evidence"] = {
                "status": "PRESENT",
                "sources": sorted(set(candidate["external_evidence"].get("sources", [])) | {result["result_id"]}),
                "note": "External workflow observation recorded; this does not establish payment or product demand.",
            }
        if result["economic_value_observed"]:
            candidate["economic_evidence"] = {
                "status": "PRESENT",
                "sources": sorted(set(candidate["economic_evidence"].get("sources", [])) | {result["result_id"]}),
                "note": "Measured economic value recorded by an admissible learning result.",
            }
        if result["problem_observed"] and result["result_id"] not in existing_sources:
            candidate.setdefault("evidence", []).append({
                "kind": "EVIDENCE",
                "claim": "An admissible external workflow observation recorded the stated problem.",
                "source": result["result_id"],
            })
    return updated
