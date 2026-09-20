#!/usr/bin/env python3
"""Build a bounded, read-only Foculoom portfolio archaeology report."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT.parent
FOCULOOM = HOME / "foculoom"
OUTPUT = ROOT / ".factory" / "artifacts" / "portfolio-archaeology"
PORTFOLIO = ROOT / ".factory" / "portfolio.yaml"
SF07_APPS = HOME / "sf0.7" / "factory" / "app-portfolio.json"


def independent_discovery() -> dict[str, object]:
    spec = importlib.util.spec_from_file_location("discover_portfolio", ROOT / "scripts" / "discover-portfolio.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("portfolio discovery module unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.discover(foculoom=FOCULOOM, history=SF07_APPS)


def git_metadata(path: Path) -> dict[str, str | bool | None]:
    if not (path / ".git").exists() and not (path / ".git").is_file():
        return {"repository": False, "branch": None, "dirty": None, "remote": None}
    def run(*args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(path), *args],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip()
    return {
        "repository": True,
        "branch": run("branch", "--show-current") or None,
        "dirty": bool(run("status", "--porcelain")),
        "remote": run("remote", "get-url", "origin") or None,
    }


def canonical_ids() -> tuple[list[str], list[str], list[str]]:
    text = PORTFOLIO.read_text(encoding="utf-8")
    repo_ids = re.findall(r"^  - id: ([^\n]+)$", text, re.MULTILINE)
    apple_section = text.split("apple_products:\n", 1)[1].split("\nhistorical_products:", 1)[0]
    apple_ids = re.findall(r"^  - id: ([^\n]+)$", apple_section, re.MULTILINE)
    historical_section = text.split("historical_products:\n", 1)[1] if "historical_products:\n" in text else ""
    historical_ids = re.findall(r"^  - id: ([^\n]+)$", historical_section, re.MULTILINE)
    return repo_ids, apple_ids, historical_ids


def historical_apps() -> list[dict[str, object]]:
    if not SF07_APPS.exists():
        return []
    payload = json.loads(SF07_APPS.read_text(encoding="utf-8"))
    return [
        {
            "identity": app.get("name"),
            "source": app.get("source"),
            "bundle_id": app.get("bundle_id"),
            "asc_status": app.get("asc_status"),
            "decision": app.get("decision"),
            "stack": app.get("stack"),
            "tests": app.get("tests"),
            "reasoning": app.get("reasoning"),
            "pending": app.get("pending"),
            "origin": "sf0.7/factory/app-portfolio.json",
            "certainty": "KNOWN",
        }
        for app in payload.get("apps", [])
    ]


def candidates() -> list[dict[str, object]]:
    roots = [
        ("foculoom/products", FOCULOOM / "products"),
        ("foculoom/games", FOCULOOM / "games"),
        ("foculoom/web", FOCULOOM / "web"),
        ("foculoom/demos", FOCULOOM / "demos"),
        ("foculoom/tools", FOCULOOM / "tools"),
        ("foculoom/.archived", FOCULOOM / ".archived"),
    ]
    found: list[dict[str, object]] = []
    for label, root in roots:
        if not root.is_dir():
            continue
        for child in sorted(root.iterdir()):
            if child.name.startswith("."):
                continue
            found.append(
                {
                    "identity": child.name,
                    "path": str(child),
                    "scope": label,
                    "kind": "directory_candidate",
                    "certainty": "INFERRED",
                    "source_control": git_metadata(child),
                }
            )
    return found


def factory_roots() -> list[dict[str, object]]:
    result = []
    for number in range(1, 9):
        path = HOME / f"sf0.{number}"
        if path.exists():
            result.append(
                {
                    "identity": f"sf0.{number}",
                    "path": str(path),
                    "kind": "factory",
                    "certainty": "KNOWN",
                    "source_control": git_metadata(path),
                }
            )
    return result


def apple_history(apps: list[dict[str, object]]) -> dict[str, object]:
    statuses = [str(app.get("asc_status", "")) for app in apps]
    rejected = [app for app in apps if "rejected" in str(app.get("asc_status", "")).lower()]
    removed = [app for app in apps if "removed" in str(app.get("asc_status", "")).lower()]
    prepared = [app for app in apps if "prepare" in str(app.get("asc_status", "")).lower()]
    return {
        "source": str(SF07_APPS),
        "historical_app_count": len(apps),
        "rejected_count": len(rejected),
        "removed_from_store_count": len(removed),
        "prepare_for_submission_count": len(prepared),
        "testflight_evidence": [
            str(HOME / "sf0.7" / "evidence" / "inc-017" / "verification.txt"),
            str(HOME / "sf0.7" / "evidence" / "inc-017" / "docketloom-verification.txt"),
        ],
        "review_feedback_evidence": [
            str(HOME / "sf0.7" / "evidence" / "inc-010" / "verification.txt"),
        ],
        "statuses_observed": sorted(set(statuses)),
    }


def build() -> dict[str, object]:
    repo_ids, apple_ids, historical_ids = canonical_ids()
    apps = historical_apps()
    known_historical_names = {str(app["identity"]).lower() for app in apps}
    candidate_rows = candidates()
    discovery = independent_discovery()
    missing_from_apple = [
        app["identity"] for app in apps if str(app["identity"]).lower() not in {item.lower() for item in apple_ids}
    ]
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": {
            "included": ["sf0.8", "sf0.1-sf0.7", "foculoom products/games/web/demos/tools/.archived"],
            "excluded": ["arbitrary personal data", "unrelated home directories", "credential stores"],
        },
        "canonical": {"repository_ids": repo_ids, "apple_product_ids": apple_ids, "historical_product_ids": historical_ids},
        "historical_apple_apps": apps,
        "factory_roots": factory_roots(),
        "local_candidates": candidate_rows,
        "independent_discovery": discovery,
        "reconciliation": {
            "historical_apple_missing_from_canonical": missing_from_apple,
            "canonical_apple_count": len(apple_ids),
            "historical_apple_count": len(apps),
            "local_candidate_count": len(candidate_rows),
            "historical_identity_names_normalized": sorted(known_historical_names),
            "competing_sources_requiring_review": [
                {"identity": "Vorynce", "sources": ["sf0.7/factory/app-portfolio.json", "foculoom/products/vorynce-rebuild", "sf0.8/.factory/portfolio.yaml"]},
                {"identity": "Cat Whispers/Product A", "sources": ["sf0.7/apps/catwhispers", "sf0.5/catcomm", "edoworks/product-a", "sf0.8/.factory/portfolio.yaml"]},
                {"identity": "Jumpyloo/Docketloom", "sources": ["sf0.7/factory/queue.json", "sf0.7/factory/legacy-quarantine.json", "sf0.7/evidence/inc-013"]},
            ],
            "discovery_completeness": {
                "confidence": "INDEPENDENT_EVIDENCE_RECORDED",
                "registry_is_not_discovery_input": True,
                "high_confidence_candidates": discovery["metrics"]["high_confidence_count"],
                "unexplained_candidates": [
                    candidate["product_id"]
                    for candidate in discovery["candidates"]
                    if candidate["confidence"] == "HIGH"
                    and candidate["product_id"] not in {item.casefold() for item in apple_ids + historical_ids}
                ],
            },
        },
        "apple_history": apple_history(apps),
        "deletion_policy": {
            "source_repositories_deleted": 0,
            "unique_artifacts_deleted": 0,
            "human_authorization_required": True,
        },
    }


def knowledge_records(report: dict[str, object]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for app in report["historical_apple_apps"]:
        records.append(
            {
                "record_id": f"apple-history:{str(app['identity']).lower().replace(' ', '-')}",
                "kind": "historical_product",
                "product": app["identity"],
                "source": app["origin"],
                "durable_knowledge": ["Apple lifecycle state", "bundle identity", "originating source", "historical decision"],
                "query_terms": [str(app["identity"]), str(app.get("bundle_id") or ""), "Apple", "App Review"],
                "preservation_status": "EXTRACTED_TO_ARCHAEOLOGY_REPORT",
            }
        )
    records.extend(
        [
            {
                "record_id": "lesson:apple-review-rejection-extraction",
                "kind": "lesson",
                "product": "Vorynce",
                "source": "/Users/hello/sf0.7/evidence/inc-010/verification.txt",
                "durable_knowledge": ["rejection reason required resolution-center or review-message evidence", "submit dry-run gate was previously missing"],
                "query_terms": ["Vorynce", "rejection", "App Review", "dry run"],
                "preservation_status": "EXTRACTED_TO_APPLE_HISTORY_EVIDENCE",
            },
            {
                "record_id": "lesson:sf07-queue-title-drift",
                "kind": "lesson",
                "product": "Docketloom/Jumpyloo",
                "source": "/Users/hello/sf0.7/factory/legacy-quarantine.json",
                "durable_knowledge": ["queue title and evidence payload diverged", "historical identifiers require evidence cross-check"],
                "query_terms": ["Docketloom", "Jumpyloo", "queue drift", "identity"],
                "preservation_status": "EXTRACTED_TO_RECONCILIATION_REPORT",
            },
            {
                "record_id": "lesson:sf05-knowledge-snapshot-integrity",
                "kind": "factory_capability",
                "product": "sf0.5",
                "source": "/Users/hello/sf0.5/factory/knowledge-sources.json",
                "durable_knowledge": ["content-addressed knowledge snapshots", "source registry with scope and trust tier"],
                "query_terms": ["knowledge", "snapshot", "sha256", "source registry"],
                "preservation_status": "REFERENCE_ONLY_NOT_COPIED",
            },
        ]
    )
    return records


def preservation_manifests(report: dict[str, object]) -> list[dict[str, object]]:
    candidates = list(report["local_candidates"])
    candidates.extend(report["factory_roots"])
    candidates.extend(
        {
            "identity": app["identity"],
            "path": app["source"],
            "kind": "historical_apple_product",
            "certainty": app["certainty"],
        }
        for app in report["historical_apple_apps"]
    )
    manifests = []
    for candidate in candidates:
        path = str(candidate.get("path") or "")
        source_exists = bool(path and path != "UNKNOWN" and Path(path).exists())
        is_historical = candidate.get("kind") == "historical_apple_product"
        source_control = candidate.get("source_control") or (git_metadata(Path(path)) if source_exists else {})
        app = next(
            (item for item in report["historical_apple_apps"] if item["identity"] == candidate["identity"]),
            None,
        )
        durable_items = [
            item
            for item in [
                ("Apple lifecycle state", app.get("asc_status") if app else None),
                ("bundle identity", app.get("bundle_id") if app else None),
                ("architecture", app.get("stack") if app else None),
                ("test strategy", app.get("tests") if app else None),
                ("historical decision", app.get("decision") if app else None),
            ]
            if item[1]
        ]
        manifests.append(
            {
                "candidate": candidate["identity"],
                "path": path,
                "state": "KNOWLEDGE_EXTRACTION_REQUIRED",
                "unique_knowledge": durable_items or "UNKNOWN_PENDING_SOURCE_REVIEW",
                "durable_preservation": "portfolio-archaeology/inventory.json plus source path",
                "knowledge_status": "PARTIAL_EXTRACTED" if is_historical and durable_items else "UNEXTRACTED",
                "uniquely_valuable_code": "SOURCE_PATH_RETAINED" if source_exists else "UNKNOWN",
                "uniquely_valuable_assets": "REVIEW_REQUIRED",
                "history_loss_if_deleted": "UNKNOWN",
                "apple_evidence_loss": "HISTORICAL_RECORD_PRESENT" if is_historical else "UNKNOWN",
                "fresh_agent_recoverable": bool(is_historical and durable_items),
                "recoverable_from_version_control_or_remote": "LOCAL_SOURCE_PRESENT" if source_exists else "UNKNOWN",
                "uncommitted": source_control.get("dirty", "UNKNOWN"),
                "unpushed": "UNKNOWN",
                "unbacked_up": "UNKNOWN",
                "deletion_authorized": False,
            }
        )
    return manifests


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUTPUT / "inventory.json"))
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    report = build()
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output.parent.joinpath("independent-discovery.json").write_text(
        json.dumps(report["independent_discovery"], indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    output.parent.joinpath("knowledge-records.json").write_text(
        json.dumps({"schema_version": 1, "records": knowledge_records(report)}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    output.parent.joinpath("preservation-manifests.json").write_text(
        json.dumps({"schema_version": 1, "manifests": preservation_manifests(report)}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
