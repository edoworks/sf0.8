#!/usr/bin/env python3
"""Metadata-only recovery discovery and bounded blocker classification."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
import re
from typing import Any


BLOCKER_CLASSES = {
    "missing_knowledge",
    "missing_capability",
    "configuration_problem",
    "dependency_problem",
    "authentication_problem",
    "authorization_problem",
    "governance_restriction",
    "external_service_problem",
    "transient_infrastructure_problem",
    "safety_restriction",
    "incompatible_local_solution",
    "human_only_decision",
}

TOKEN_ALIASES = {
    "pr": "pull_request",
    "prs": "pull_request",
    "pull": "pull_request",
    "request": "pull_request",
    "github": "github",
    "gh": "github",
    "review": "review",
    "reviews": "review",
    "permission": "authorization",
    "permissions": "authorization",
    "policy": "governance",
    "protected": "governance",
    "branch": "branch",
    "branches": "branch",
    "direct": "push",
    "pushing": "push",
    "pushed": "push",
    "create": "creation",
    "creating": "creation",
}


def normalize_terms(value: str | Iterable[str]) -> set[str]:
    values = value.split() if isinstance(value, str) else value
    terms: set[str] = set()
    for value in values:
        for token in re.findall(r"[a-z0-9]+", str(value).casefold()):
            terms.add(TOKEN_ALIASES.get(token, token))
    return terms


def classify_blocker(*, error: str, operation: str = "") -> str:
    text = f"{operation} {error}".casefold()
    if any(term in text for term in ("secret", "human authorization", "owner approval")):
        return "human_only_decision"
    if any(term in text for term in ("permission denied", "not permitted", "policy", "hook", "protected branch")):
        return "governance_restriction"
    if any(term in text for term in ("unauthorized", "forbidden", "access denied")):
        return "authorization_problem"
    if any(term in text for term in ("authentication", "login", "token", "credential")):
        return "authentication_problem"
    if any(term in text for term in ("timeout", "temporarily", "connection", "http 5")):
        return "transient_infrastructure_problem"
    if any(term in text for term in ("not found", "missing", "unavailable")):
        return "missing_capability"
    return "configuration_problem"


def _record_terms(record: dict[str, Any]) -> set[str]:
    fields = [
        record.get("problem_class", ""),
        record.get("mechanism", ""),
        *record.get("symptoms", []),
        *record.get("aliases", []),
    ]
    return normalize_terms(fields)


def _source_allowed(path: str, sources: dict[str, Any]) -> bool:
    candidate = Path(path)
    if not candidate.is_absolute():
        return False
    for source in sources.get("sources", []):
        root = Path(str(source.get("root", ""))).resolve()
        try:
            relative = candidate.resolve().relative_to(root).as_posix()
        except ValueError:
            continue
        if any(Path(relative).match(str(pattern).rstrip("/")) or relative.startswith(str(pattern).rstrip("/") ) for pattern in source.get("allowed_paths", [])):
            return not any(Path(relative).match(pattern) for pattern in sources.get("excluded_patterns", []))
    return False


def validate_solution_sources(solution: dict[str, Any], sources: dict[str, Any]) -> list[str]:
    errors = []
    for field in ("implementation_location", "validation_evidence"):
        values = solution.get(field, []) if field == "validation_evidence" else [solution.get(field, "")]
        for value in values:
            if not _source_allowed(str(value), sources):
                errors.append(f"{solution.get('id')}: source is outside the allowlist: {value}")
    return errors


def search_solutions(
    query: str,
    registry: dict[str, Any],
    sources: dict[str, Any],
    *,
    objective_id: str = "",
    attempted: Iterable[str] = (),
) -> list[dict[str, Any]]:
    terms = normalize_terms(query)
    attempted_ids = set(attempted)
    ranked = []
    for solution in registry.get("solutions", []):
        errors = validate_solution_sources(solution, sources)
        if errors:
            continue
        record_terms = _record_terms(solution)
        matched = terms & record_terms
        if not matched:
            continue
        compatibility = solution.get("compatibility", {}).get(objective_id, "unknown")
        score = len(matched) * 10
        if solution.get("disposition") in {"ADOPT", "ADAPT"}:
            score += 20
        if compatibility == "directly_compatible":
            score += 30
        elif compatibility == "compatible_mechanism_authority_unavailable":
            score += 15
        if solution.get("authority_state") == "AVAILABLE":
            score += 10
        if solution.get("id") in attempted_ids:
            score -= 100
        ranked.append({
            "id": solution.get("id"),
            "score": score,
            "matched_terms": sorted(matched),
            "compatibility": compatibility,
            "authority_state": solution.get("authority_state"),
            "human_authorization_required": solution.get("human_authorization_required", True),
            "mechanism": solution.get("mechanism"),
            "source_project": solution.get("source_project"),
        })
    return sorted(ranked, key=lambda item: (-item["score"], item["id"]))


def recovery_decision(
    *,
    blocker: dict[str, Any],
    candidates: list[dict[str, Any]],
    attempts: int,
    max_attempts: int = 3,
) -> dict[str, Any]:
    if attempts >= max_attempts:
        return {"state": "BLOCKED_AFTER_SELF_UNBLOCKING", "candidates": candidates, "reason": "attempt bound exhausted"}
    if not candidates:
        return {"state": "BLOCKED_AFTER_SELF_UNBLOCKING", "candidates": [], "reason": "no compatible proven solution found"}
    candidate = candidates[0]
    if candidate["authority_state"] != "AVAILABLE" or candidate["human_authorization_required"]:
        return {"state": "HUMAN_AUTHORIZATION_REQUIRED", "candidate": candidate, "blocker": blocker}
    return {"state": "ATTEMPT_BOUNDED_REMEDIATION", "candidate": candidate, "blocker": blocker}
