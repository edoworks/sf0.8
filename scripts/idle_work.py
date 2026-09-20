"""Discover and classify bounded work across the factory.

This module deliberately separates discovery from authority. A blocked product
is still a discovered candidate, while an independent read-only task remains
eligible. WAITING_DEPENDENCY is only legal after every provider has returned a
successful, machine-readable result and the eligible set is empty.
"""

from __future__ import annotations

import json
import importlib
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]


def _candidate(
    candidate_id: str,
    title: str,
    category: str,
    source: str,
    *,
    priority: int = 50,
    value: str = "MEDIUM",
    urgency: str = "LOW",
    reversibility: str = "HIGH",
    risk: str = "LOW",
    cost: float = 0.0,
    required_authority: str = "NONE",
    dependencies: list[str] | None = None,
    scope: str = "bounded read-only review",
    evidence: list[str] | None = None,
    expected_validation: list[str] | None = None,
    state: str = "READY",
    action: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "id": candidate_id,
        "title": title,
        "category": category,
        "source": source,
        "priority": priority,
        "value": value,
        "urgency": urgency,
        "reversibility": reversibility,
        "risk": risk,
        "cost": cost,
        "required_authority": required_authority,
        "dependencies": dependencies or [],
        "scope": scope,
        "evidence": evidence or [],
        "expected_validation": expected_validation or [],
        "state": state,
        "action": action,
    }


def discover_lanes(context: dict[str, Any]) -> list[dict[str, Any]]:
    document = context["lanes"]
    result = []
    for lane in document.get("lanes", []):
        state = lane.get("state", "UNKNOWN")
        work = str(lane.get("work", "")).strip()
        if not work:
            continue
        blocked = state != "READY"
        result.append(_candidate(
            f"lane:{lane.get('issue', work)}",
            work,
            "portfolio" if "portfolio" in work or "historical" in work else "product",
            "parallel-lanes.json",
            priority=int(lane.get("priority", 50)),
            value="HIGH" if "knowledge" in work or "archaeology" in work else "MEDIUM",
            urgency="MEDIUM" if state == "READY" else "LOW",
            required_authority="HUMAN" if "HUMAN" in state or "APPLE" in state else "NONE",
            dependencies=list(lane.get("conflicts", [])) if blocked else [],
            scope="bounded lane work; no deletion, publication, or product resumption",
            evidence=[".factory/artifacts/portfolio-archaeology/parallel-lanes.json"],
            expected_validation=["lane-specific evidence record", "bounded lane validator"],
            state="BLOCKED" if blocked else "READY",
        ))
    return result


def discover_portfolio(context: dict[str, Any]) -> list[dict[str, Any]]:
    return [_candidate(
        "portfolio:product-a-resume",
        "Resume Product A implementation",
        "product",
        ".factory/portfolio.yaml",
        priority=5,
        value="HIGH",
        required_authority="HUMAN",
        dependencies=["owner revival instruction"],
        scope="explicitly excluded from autonomous work",
        evidence=[".factory/portfolio.yaml", "docs/decisions/2026-09-17-product-a-shelved.md"],
        expected_validation=["owner decision"],
        state="BLOCKED",
    )]


def discover_reuse(context: dict[str, Any]) -> list[dict[str, Any]]:
    registry = context["reuse"]
    result = []
    for artifact in registry.get("artifacts", []):
        if artifact.get("disposition") != "REUSE_CANDIDATE":
            continue
        artifact_id = str(artifact.get("id", "unknown"))
        result.append(_candidate(
            f"reuse:{artifact_id}",
            f"Evaluate reusable capability: {artifact.get('title', artifact_id)}",
            "reuse",
            ".factory/artifacts/reuse-registry.json",
            priority=20,
            value="HIGH",
            urgency="MEDIUM",
            risk="MEDIUM" if artifact.get("license", "").startswith("Unknown") else "LOW",
            required_authority="NONE",
            dependencies=["source review"] if "Unknown" in str(artifact.get("license")) else [],
            scope="read-only candidate evaluation; extraction and publication are excluded",
            evidence=[".factory/artifacts/reuse-registry.json", str(artifact.get("provenance", ""))],
            expected_validation=["reuse decision record", "registry validation"],
            state="BLOCKED" if "Unknown" in str(artifact.get("license")) else "READY",
        ))
    return result


def discover_hygiene(context: dict[str, Any]) -> list[dict[str, Any]]:
    hygiene = context["hygiene"]
    result = []
    for index, item in enumerate(hygiene.get("classifications", [])):
        if item.get("action") != "REPORT_ONLY":
            continue
        result.append(_candidate(
            f"hygiene:{index}",
            f"Classify {item.get('category', 'resource')} without deletion",
            "hygiene",
            ".factory/artifacts/portfolio-archaeology/resource-hygiene.json",
            priority=30,
            value="MEDIUM",
            scope="metadata-only report; no cleanup or deletion",
            evidence=[".factory/artifacts/portfolio-archaeology/resource-hygiene.json"],
            expected_validation=["resource classification evidence"],
        ))
    return result


def discover_knowledge(context: dict[str, Any]) -> list[dict[str, Any]]:
    audit = context["audit"]
    if audit.get("knowledge", {}).get("preservation_manifests", 0) <= 0:
        return []
    return [_candidate(
        "knowledge:preservation-batch",
        "Review the next preserved historical knowledge batch",
        "knowledge",
        ".factory/artifacts/portfolio-archaeology/audit-report.json",
        priority=15,
        value="HIGH",
        scope="metadata-only review; no archive or deletion",
        evidence=[".factory/artifacts/portfolio-archaeology/preservation-manifests.json", ".factory/artifacts/portfolio-archaeology/knowledge-records.json"],
        expected_validation=["preservation provenance record", "portfolio audit validator"],
    )]


def discover_rejections(context: dict[str, Any]) -> list[dict[str, Any]]:
    history = context["audit"].get("apple_history", {})
    if history.get("comparison_blocked_records", 0) <= 0:
        return []
    return [_candidate(
        "rejections:historical-comparison",
        "Compare historical App Review evidence",
        "rejection-analysis",
        ".factory/artifacts/portfolio-archaeology/audit-report.json",
        priority=40,
        value="MEDIUM",
        required_authority="EXTERNAL",
        dependencies=["exact historical metadata/screenshots"],
        scope="blocked until historical evidence is available",
        evidence=[".factory/artifacts/portfolio-archaeology/apple-history.json"],
        expected_validation=["review regression record"],
        state="BLOCKED",
    )]


def discover_verification(context: dict[str, Any]) -> list[dict[str, Any]]:
    return [_candidate(
        "verification:portfolio-audit",
        "Re-run portfolio audit and preserve current evidence",
        "validation",
        ".factory/artifacts/portfolio-archaeology/audit-report.json",
        priority=1,
        value="HIGH",
        urgency="MEDIUM",
        scope="local validator only; no external writes",
        evidence=[".factory/artifacts/portfolio-archaeology/audit-report.json"],
        expected_validation=["scripts/validate-portfolio-audit.py"],
        action=["python3", "scripts/validate-portfolio-audit.py"],
    )]


def discover_ci(context: dict[str, Any]) -> list[dict[str, Any]]:
    return [_candidate(
        "ci:status-evidence",
        "Refresh local CI status evidence",
        "reliability",
        "scripts/ci-status.sh",
        priority=2,
        value="HIGH",
        scope="read-only CI status inspection; no external mutation",
        evidence=["docs/ci/last-ci-result.txt"],
        expected_validation=["scripts/ci-status.sh"],
        action=["./scripts/ci-status.sh"],
    )]


def _load_context(root: Path = ROOT) -> dict[str, Any]:
    def load(relative: str) -> dict[str, Any]:
        return json.loads((root / relative).read_text(encoding="utf-8"))

    return {
        "audit": load(".factory/artifacts/portfolio-archaeology/audit-report.json"),
        "lanes": load(".factory/artifacts/portfolio-archaeology/parallel-lanes.json"),
        "reuse": load(".factory/artifacts/reuse-registry.json"),
        "hygiene": load(".factory/artifacts/portfolio-archaeology/resource-hygiene.json"),
    }


def _classify(candidate: dict[str, Any], budget: float) -> tuple[bool, str | None]:
    required = ("value", "urgency", "reversibility", "risk", "cost", "required_authority", "dependencies", "scope", "evidence", "expected_validation", "category")
    missing = [field for field in required if field not in candidate]
    if missing:
        return False, f"missing classification fields: {', '.join(missing)}"
    if candidate["state"] != "READY":
        return False, "candidate is blocked or not ready"
    if candidate["required_authority"] != "NONE":
        return False, f"requires {candidate['required_authority']} authority"
    if candidate["dependencies"]:
        return False, "dependency is unresolved"
    if candidate["risk"] not in {"LOW", "MEDIUM"}:
        return False, "risk is not bounded"
    if candidate["reversibility"] not in {"HIGH", "MEDIUM"}:
        return False, "work is not reversible"
    if float(candidate["cost"]) > budget:
        return False, "autonomous cost budget would be exceeded"
    if not candidate["scope"] or not candidate["evidence"] or not candidate["expected_validation"]:
        return False, "scope, evidence, and validation must be explicit"
    return True, None


def discover_idle_work(root: Path = ROOT, budget: float = 5.0, providers: dict[str, Callable[[dict[str, Any]], list[dict[str, Any]]]] | None = None) -> dict[str, Any]:
    context = _load_context(root)
    configured = json.loads((root / ".factory/idle-work-sources.json").read_text(encoding="utf-8"))
    provider_map = providers or {}
    all_candidates: list[dict[str, Any]] = []
    provider_results = []
    for descriptor in configured.get("providers", []):
        provider_id = descriptor["id"]
        provider = provider_map.get(provider_id)
        if provider is None:
            try:
                module_name = descriptor["module"]
                try:
                    module = importlib.import_module(f"scripts.{module_name}")
                except ModuleNotFoundError:
                    module = importlib.import_module(module_name)
                provider = getattr(module, descriptor["function"])
            except (KeyError, ImportError, AttributeError) as error:
                provider_results.append({"source": provider_id, "status": "ERROR", "error": str(error), "candidate_ids": []})
                continue
        if provider is None:
            provider_results.append({"source": provider_id, "status": "ERROR", "error": "provider is not registered", "candidate_ids": []})
            continue
        try:
            candidates = provider(context)
        except Exception as error:  # provider failure must prevent exhaustion claims
            provider_results.append({"source": provider_id, "status": "ERROR", "error": str(error), "candidate_ids": []})
            continue
        all_candidates.extend(candidates)
        provider_results.append({"source": provider_id, "status": "PASS", "candidate_ids": [item["id"] for item in candidates]})

    eligible = []
    rejected = []
    for candidate in all_candidates:
        allowed, reason = _classify(candidate, budget)
        if allowed:
            eligible.append(candidate)
        else:
            rejected.append({"candidate": candidate["id"], "reason": reason})
    eligible.sort(key=lambda item: (item["priority"], -{"HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(item["value"], 0), item["id"]))
    exhaustive = all(item["status"] == "PASS" for item in provider_results)
    report = {
        "schema_version": 1,
        "sources_searched": [item["source"] for item in provider_results],
        "provider_results": provider_results,
        "candidates_found": all_candidates,
        "candidates_rejected_or_blocked": rejected,
        "eligible_candidates": eligible,
        "eligible_count": len(eligible),
        "exhaustive": exhaustive,
        "waiting_dependency_legal": exhaustive and not eligible,
        "status": "READY_WORK_FOUND" if eligible else ("WAITING_DEPENDENCY" if exhaustive else "DISCOVERY_FAILED"),
        "budget": {"max_cost": budget, "remaining_eligible_cost": round(sum(float(item["cost"]) for item in eligible), 4)},
    }
    return report


def select_work(report: dict[str, Any]) -> dict[str, Any] | None:
    eligible = report.get("eligible_candidates", [])
    return eligible[0] if eligible else None


def validate_waiting_report(report: dict[str, Any]) -> list[str]:
    errors = []
    if report.get("status") == "WAITING_DEPENDENCY":
        if not report.get("exhaustive"):
            errors.append("WAITING_DEPENDENCY requires successful results from every provider")
        if report.get("eligible_count") != 0:
            errors.append("WAITING_DEPENDENCY is illegal while eligible candidates exist")
        if report.get("waiting_dependency_legal") is not True:
            errors.append("WAITING_DEPENDENCY lacks legal exhaustion evidence")
    if report.get("status") == "DISCOVERY_FAILED":
        errors.append("discovery provider failure cannot be represented as idleness")
    return errors
