#!/usr/bin/env python3
"""Pure, deterministic gates for reuse and contribution decisions."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def required_search(change_units: int) -> int:
    """Scale discovery with change size, while always requiring one candidate."""
    if change_units < 1:
        raise ValueError("change_units must be positive")
    return max(1, math.ceil(change_units / 8))


DISPOSITIONS = {
    "ADOPT",
    "ADAPT",
    "LEARN_FROM",
    "CONTRIBUTE_UPSTREAM",
    "BUILD_NEW",
    "REJECT",
}

SHAREABILITY_DISPOSITIONS = {
    "PRODUCT_ONLY",
    "REUSE_CANDIDATE",
    "INTERNAL_SHARED",
    "PUBLIC_CANDIDATE",
    "UPSTREAM_CANDIDATE",
    "KNOWLEDGE_ARTIFACT",
    "NOT_SHAREABLE",
}

COMPLETION_STATES = {
    "DONE",
    "BLOCKED_EXTERNAL",
    "BLOCKED_HUMAN",
    "BLOCKED_SECURITY",
    "WAITING_DEPENDENCY",
    "FAILED",
    "NOT_DONE",
    "CONTROL_PLANE_BLOCKED",
    "PORTFOLIO_DISCOVERY_INCOMPLETE",
    "PORTFOLIO_RECONCILIATION_BLOCKED",
    "EXTERNAL_SOURCE_UNAVAILABLE",
    "IDENTITY_UNRESOLVED",
}

EVALUATION_FIELDS = {
    "relevance",
    "quality",
    "maintenance",
    "license",
    "security",
    "privacy",
    "dependency_cost",
    "portability",
    "overlap",
    "adaptability",
    "provenance",
}

SUBSTANTIAL_PATHS = (
    ".agents/skills/",
    ".opencode/skills/",
    ".claude/skills/",
    ".factory/artifacts/packages/",
    "plugins/",
    "packages/",
    "safety_kernel/",
    "scripts/",
    ".github/workflows/",
)


def path_requires_gate(path: str) -> bool:
    """Return whether a changed path can introduce reusable or privileged machinery."""
    normalized = path.replace("\\", "/")
    if normalized.startswith("tests/") or normalized.startswith("docs/"):
        return False
    if normalized.endswith((".md", ".txt", ".json", ".yaml", ".yml")):
        return any(normalized.startswith(prefix) for prefix in SUBSTANTIAL_PATHS)
    return any(normalized.startswith(prefix) for prefix in SUBSTANTIAL_PATHS)


def validate_change_record(paths: list[str], record: dict[str, Any] | None) -> dict[str, Any]:
    """Require evidence only when changed paths can add substantial machinery."""
    gated_paths = sorted(path for path in paths if path_requires_gate(path))
    if not gated_paths:
        return {"decision": "BYPASS", "gated_paths": [], "errors": []}
    errors: list[str] = []
    if not record:
        errors.append("substantial paths require a reuse/contribution record")
    else:
        reuse = record.get("reuse", {})
        result = reuse_gate(
            int(record.get("change_units", 0)),
            int(reuse.get("searched", 0)),
            int(reuse.get("compatible", 0)),
            str(reuse.get("reason", "")),
        )
        if result["decision"] == "BLOCKED":
            errors.extend(result["errors"])
        discovery = reuse.get("discovery", {})
        if not str(discovery.get("capability", "")).strip():
            errors.append("substantial work requires capability discovery evidence")
        if discovery.get("decision") not in {"CONSUME_EXISTING", "BUILD_NEW", "EXTEND_EXISTING", "SPECIALIZE"}:
            errors.append("discovery decision must be recorded before implementation")
        if not isinstance(discovery.get("matches"), list):
            errors.append("discovery matches must be recorded")
        if discovery.get("matches") and discovery.get("decision") == "BUILD_NEW" and not str(discovery.get("specialization_reason", "")).strip():
            errors.append("existing capability found; BUILD_NEW requires specialization evidence")
        if record.get("contribution", {}).get("classification") not in {
            "product-specific", "internal-reusable", "public-reusable", "upstream-candidate", "upstream-contribution",
        }:
            errors.append("contribution classification is required")
        shareability = record.get("shareability", {})
        if shareability.get("disposition") not in SHAREABILITY_DISPOSITIONS:
            errors.append("shareability disposition is required for substantial work")
        elif not str(shareability.get("evidence", "")).strip():
            errors.append("shareability evidence is required for substantial work")
        if shareability.get("disposition") in {"PRODUCT_ONLY", "NOT_SHAREABLE"} and not str(shareability.get("reuse_analysis", "")).strip():
            errors.append("product-only/non-shareable work must include reuse analysis")
    return {"decision": "PASS" if not errors else "BLOCKED", "gated_paths": gated_paths, "errors": errors}


def validate_reuse_registry(registry: dict[str, Any]) -> list[str]:
    """Validate the canonical registry without treating records as executable input."""
    required = {
        "id", "title", "disposition", "origin", "created_by", "problem", "consumers", "consumer_evidence",
        "plausible_consumers", "second_consumer_demonstrated", "extraction_justified",
        "equivalent_public_capability", "upstream_assessment", "tests", "verification_evidence", "provenance",
        "license", "secrets_private_data", "differentiation_security", "lifecycle_state",
        "rationale",
    }
    errors: list[str] = []
    records = registry.get("artifacts")
    if not isinstance(records, list) or not records:
        return ["reuse registry must contain artifacts"]
    ids: set[str] = set()
    by_id = {record.get("id"): record for record in records if isinstance(record, dict)}
    for record in records:
        missing = sorted(required - record.keys()) if isinstance(record, dict) else ["record object"]
        if missing:
            errors.append(f"registry record missing: {', '.join(missing)}")
            continue
        artifact_id = record["id"]
        if artifact_id in ids:
            errors.append(f"duplicate registry id: {artifact_id}")
        ids.add(artifact_id)
        disposition = record["disposition"]
        if disposition not in SHAREABILITY_DISPOSITIONS:
            errors.append(f"{artifact_id}: invalid shareability disposition")
        if not str(record["rationale"]).strip() or not str(record["provenance"]).strip():
            errors.append(f"{artifact_id}: rationale and provenance are required")
        consumers = record["consumers"]
        if not isinstance(consumers, list):
            errors.append(f"{artifact_id}: consumers must be a list")
            consumers = []
        evidence = record["consumer_evidence"]
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{artifact_id}: consumer evidence is required")
        if disposition == "INTERNAL_SHARED" and len(consumers) < 2 and not record.get("strong_exception"):
            errors.append(f"{artifact_id}: INTERNAL_SHARED requires two consumers or a documented exception")
        if disposition == "INTERNAL_SHARED" and not record["second_consumer_demonstrated"] and not record.get("strong_exception"):
            errors.append(f"{artifact_id}: second consumer evidence is required")
        if disposition == "INTERNAL_SHARED" and not consumers:
            errors.append(f"{artifact_id}: shared components cannot have zero consumers")
        duplicate_of = record.get("duplicate_of")
        if duplicate_of and by_id.get(duplicate_of, {}).get("disposition") != "INTERNAL_SHARED":
            errors.append(f"{artifact_id}: duplicate_of must name an active INTERNAL_SHARED artifact")
        if disposition == "PUBLIC_CANDIDATE":
            safety = record["secrets_private_data"]
            if safety is not False or record["differentiation_security"] is not False:
                errors.append(f"{artifact_id}: public candidates must pass private/security safety checks")
            if not record.get("tests") or not record.get("license"):
                errors.append(f"{artifact_id}: public candidates require tests and license evidence")
            if record.get("publication_approved") is not False:
                errors.append(f"{artifact_id}: public candidates remain human-approval gated")
        if disposition == "UPSTREAM_CANDIDATE":
            if not record["equivalent_public_capability"]:
                errors.append(f"{artifact_id}: upstream candidates require an equivalent public capability")
            if not str(record.get("external_capability_evidence", "")).strip():
                errors.append(f"{artifact_id}: upstream candidates require external capability evidence")
        if disposition in {"PRODUCT_ONLY", "NOT_SHAREABLE"} and not str(record["rationale"]).strip():
            errors.append(f"{artifact_id}: product-only/non-shareable rationale is required")
    expected = registry.get("metrics", {})
    actual = {
        "assessed_substantial_artifacts": len(records),
        "unassessed_substantial_artifacts": sum(record.get("disposition") in {None, "UNASSESSED"} for record in records),
        "reuse_candidates": sum(record.get("disposition") == "REUSE_CANDIDATE" for record in records),
        "second_consumer_promotions": sum(record.get("second_consumer_demonstrated") is True for record in records),
        "internal_shared": sum(record.get("disposition") == "INTERNAL_SHARED" for record in records),
        "public_candidates": sum(record.get("disposition") == "PUBLIC_CANDIDATE" for record in records),
        "upstream_candidates": sum(record.get("disposition") == "UPSTREAM_CANDIDATE" for record in records),
        "knowledge_artifacts": sum(record.get("disposition") == "KNOWLEDGE_ARTIFACT" for record in records),
        "zero_consumer_shared": sum(record.get("disposition") == "INTERNAL_SHARED" and not record.get("consumers") for record in records),
    }
    for key, value in actual.items():
        if expected.get(key) != value:
            errors.append(f"metrics.{key}={expected.get(key)!r}, expected {value!r}")
    return errors


def validate_consumer_evidence(registry: dict[str, Any], root: Path) -> list[str]:
    """Reject stale or nonexistent repository evidence for declared consumers."""
    errors: list[str] = []
    for record in registry.get("artifacts", []):
        for relative in record.get("consumer_evidence", []):
            path = Path(str(relative))
            if path.is_absolute() or ".." in path.parts:
                errors.append(f"{record.get('id')}: consumer evidence path is unsafe: {relative}")
            elif not (root / path).exists():
                errors.append(f"{record.get('id')}: consumer evidence does not exist: {relative}")
    return errors


def discover_registry(registry: dict[str, Any], capability: str) -> list[dict[str, Any]]:
    """Return registry matches for a capability before any build decision."""
    needle = capability.casefold().strip()
    if not needle:
        return []
    terms = [term for term in needle.split() if term]
    return [
        record for record in registry.get("artifacts", [])
        if all(term in json.dumps(record, sort_keys=True).casefold() for term in terms)
    ]


def validate_work_start(task: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    """Make discovery an entry condition for substantial product work."""
    errors: list[str] = []
    capability = str(task.get("capability", "")).strip()
    matches = discover_registry(registry, capability)
    if int(task.get("change_units", 0)) < 1:
        errors.append("change_units must be positive")
    if not capability:
        errors.append("capability is required before implementation")
    if not matches and not str(task.get("build_new_reason", "")).strip():
        errors.append("no registry match requires an explicit BUILD_NEW reason")
    if matches and task.get("decision") == "BUILD_NEW" and not str(task.get("specialization_reason", "")).strip():
        errors.append("existing capability found; consume, extend, or justify specialization")
    return {
        "decision": "BLOCKED" if errors else ("CONSUME_EXISTING" if matches and task.get("decision") != "BUILD_NEW" else "BUILD_NEW"),
        "matches": [record["id"] for record in matches],
        "errors": errors,
    }


def completion_state(record: dict[str, Any]) -> dict[str, Any]:
    """Separate DONE from every unresolved or failed acceptance state."""
    explicit = str(record.get("blocker_state", "")).strip()
    if explicit in {
        "BLOCKED_EXTERNAL", "BLOCKED_HUMAN", "BLOCKED_SECURITY", "WAITING_DEPENDENCY", "FAILED",
        "PORTFOLIO_DISCOVERY_INCOMPLETE", "PORTFOLIO_RECONCILIATION_BLOCKED",
        "EXTERNAL_SOURCE_UNAVAILABLE", "IDENTITY_UNRESOLVED",
    }:
        if explicit == "WAITING_DEPENDENCY":
            exhaustion = record.get("idle_exhaustion")
            errors = []
            if not isinstance(exhaustion, dict):
                errors.append("WAITING_DEPENDENCY requires an idle exhaustion report")
            else:
                providers = exhaustion.get("provider_results", [])
                if not providers or any(item.get("status") != "PASS" for item in providers):
                    errors.append("idle exhaustion report must prove every provider passed")
                if exhaustion.get("eligible_count") != 0:
                    errors.append("idle exhaustion report must prove eligible_count is zero")
                if exhaustion.get("waiting_dependency_legal") is not True:
                    errors.append("idle exhaustion report does not authorize waiting")
            return {"state": explicit, "done": False, "errors": errors}
        return {"state": explicit, "done": False, "errors": []}
    if record.get("failed") is True:
        return {"state": "FAILED", "done": False, "errors": []}
    implementation = record.get("implementation") == "complete"
    issue_required = bool(record.get("issue", {}).get("required"))
    issue_reconciled = record.get("issue", {}).get("reconciled") is True
    blocker = str(record.get("control_plane_blocker", "")).strip()
    if not implementation:
        state = "NOT_DONE"
    elif issue_required and not issue_reconciled:
        state = "CONTROL_PLANE_BLOCKED"
    else:
        state = "DONE"
    errors = []
    if state == "CONTROL_PLANE_BLOCKED" and not blocker:
        errors.append("blocked control-plane completion requires an explicit blocker")
    return {"state": state, "done": state == "DONE", "errors": errors}


def evaluate_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    """Evaluate metadata only; candidate contents are never loaded or executed."""
    missing = sorted(EVALUATION_FIELDS - candidate.keys())
    reasons: list[str] = [f"missing evaluation field: {field}" for field in missing]
    license_state = str(candidate.get("license", "")).lower()
    security_state = str(candidate.get("security", "")).lower()
    if license_state in {"unknown", "unclear", "incompatible"}:
        reasons.append("license is unknown, unclear, or incompatible")
    if security_state in {"suspicious", "unsafe", "quarantine"}:
        reasons.append("security review requires quarantine")
    if not candidate.get("provenance"):
        reasons.append("provenance is missing")
    disposition = candidate.get("disposition")
    if disposition not in DISPOSITIONS:
        reasons.append("disposition must be an allowed ecosystem decision")
    if reasons:
        return {"decision": "REJECT", "reasons": reasons}
    return {"decision": disposition, "reasons": candidate.get("reasons", [])}


def validate_feedback_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a proposed feedback intake without applying external changes."""
    required = {"artifact", "source", "observed_at", "status", "requested_action"}
    missing = sorted(required - record.keys())
    errors = [f"missing feedback field: {field}" for field in missing]
    if record.get("status") not in {"unreviewed", "accepted", "rejected", "deferred"}:
        errors.append("feedback status is invalid")
    if record.get("requested_action") not in {"review", "adapt", "upstream", "reject", "defer"}:
        errors.append("feedback requested_action is invalid")
    if record.get("applied") is True:
        errors.append("feedback cannot authorize applying an external change")
    return {"decision": "BLOCKED" if errors else "REVIEW_REQUIRED", "errors": errors}


def reuse_gate(change_units: int, searched: int, compatible: int, reason: str = "") -> dict[str, Any]:
    minimum = required_search(change_units)
    errors: list[str] = []
    if searched < minimum:
        errors.append(f"searched {searched} candidate(s), need {minimum}")
    if compatible < 0 or compatible > searched:
        errors.append("compatible must be between zero and searched")
    if compatible == 0 and not reason.strip():
        errors.append("BUILD_NEW requires a concise reason")
    decision = "BLOCKED" if errors else ("REUSE" if compatible else "BUILD_NEW")
    return {"decision": decision, "required_search": minimum, "searched": searched, "compatible": compatible, "errors": errors}


def contribution_gate(
    *,
    product_specific: bool,
    portable: bool,
    dependency_free: bool,
    tests: bool,
    docs: bool,
    provenance: bool,
    license_checked: bool,
    upstream_useful: bool = False,
) -> dict[str, Any]:
    """Classify a contribution without granting publication authority."""
    checks = tests and docs and provenance and license_checked
    if product_specific:
        classification = "product-specific"
    elif upstream_useful:
        classification = "upstream-contribution"
    elif not portable:
        classification = "internal-reusable"
    elif checks and dependency_free:
        classification = "public-reusable"
    else:
        classification = "upstream-candidate"
    return {
        "classification": classification,
        "publication": "human-approval-required",
        "checks_pass": checks,
        "errors": [] if checks else ["tests, docs, provenance, and license checks are all required"],
    }


def _load(path: Path) -> dict[str, Any]:
    # JSON is treated as data only; this module never imports or executes it.
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    reuse = subparsers.add_parser("reuse")
    reuse.add_argument("change_units", type=int)
    reuse.add_argument("searched", type=int)
    reuse.add_argument("compatible", type=int)
    reuse.add_argument("--reason", default="")
    contribution = subparsers.add_parser("contribution")
    contribution.add_argument("record", type=Path)
    args = parser.parse_args()
    if args.command == "reuse":
        result = reuse_gate(args.change_units, args.searched, args.compatible, args.reason)
        exit_code = 0 if result["decision"] != "BLOCKED" else 1
    else:
        record = _load(args.record)
        result = contribution_gate(**record["checks"], product_specific=record["product_specific"], portable=record["portable"])
        exit_code = 0 if result["checks_pass"] else 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
