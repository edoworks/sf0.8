#!/usr/bin/env python3
"""Discover Foculoom product candidates from independent local evidence.

This module deliberately does not read ``.factory/portfolio.yaml``.  The
portfolio registry is an evaluation target, not a discovery source.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT.parent
DEFAULT_FOCULOOM = HOME / "foculoom"
DEFAULT_HISTORY = HOME / "sf0.7" / "factory" / "app-portfolio.json"

BUNDLE_RE = re.compile(r"\b([A-Za-z0-9]+(?:\.[A-Za-z0-9_-]+){2,})\b")
REMOTE_RE = re.compile(r"github\.com[/:]([^/\s:]+/[^/\s]+?)(?:\.git)?$")


def slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return value or "unknown-product"


def run_git(path: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(path), *args], capture_output=True, text=True, check=False
    )
    return result.stdout.strip()


def git_evidence(path: Path) -> dict[str, Any]:
    if not ((path / ".git").exists() or (path / ".git").is_file()):
        return {"repository": False}
    remote = run_git(path, "remote", "get-url", "origin") or None
    match = REMOTE_RE.search(remote or "")
    return {
        "repository": True,
        "remote": remote,
        "repository_id": match.group(1) if match else None,
        "branch": run_git(path, "branch", "--show-current") or None,
    }


def historical_distribution_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = []
    for app in payload.get("apps", []):
        bundle_id = app.get("bundle_id")
        records.append(
            {
                "product_id": slug(str(bundle_id or app.get("name", "unknown"))).replace(
                    "com-foculoom-", ""
                ),
                "display_name": app.get("name"),
                "bundle_id": bundle_id,
                "source_path": app.get("source"),
                "distribution_state": app.get("asc_status"),
                "kind": "distribution_record",
                "entity_type": "app_store_application",
                "confidence": "HIGH",
                "provenance": [str(path)],
            }
        )
    return records


def manifest_evidence(path: Path) -> dict[str, Any]:
    evidence: dict[str, Any] = {}
    for candidate in (path / "project.yml", path / "project.pbxproj"):
        if not candidate.exists():
            continue
        text = candidate.read_text(encoding="utf-8", errors="ignore")
        bundles = sorted(
            {
                match
                for match in BUNDLE_RE.findall(text)
                if match.startswith("com.foculoom.") and not any(
                    suffix in match for suffix in (".tests", ".UITests", ".mac.tests")
                )
            }
        )
        versions = re.findall(r"(?:MARKETING_VERSION|CFBundleShortVersionString)\s*[:=]\s*[\"']?([^\"'\s]+)", text)
        builds = re.findall(r"(?:CURRENT_PROJECT_VERSION|CFBundleVersion)\s*[:=]\s*[\"']?([^\"'\s]+)", text)
        if bundles:
            evidence["bundle_ids"] = bundles
        if versions:
            evidence["versions"] = sorted(set(versions))
        if builds:
            evidence["builds"] = sorted(set(builds))
        evidence["manifest"] = str(candidate)
        break
    return evidence


def local_candidates(foculoom: Path) -> list[dict[str, Any]]:
    roots = ("products", "games", "web")
    candidates: list[dict[str, Any]] = []
    for root_name in roots:
        root = foculoom / root_name
        if not root.is_dir():
            continue
        for child in sorted(root.iterdir()):
            if child.name.startswith(".") or not child.is_dir():
                continue
            git = git_evidence(child)
            manifest = manifest_evidence(child)
            domain = child.name if root_name == "web" and "." in child.name else None
            if not git.get("repository") and not manifest and not domain:
                continue
            bundle_ids = manifest.get("bundle_ids", [])
            product_id = slug(bundle_ids[0].removeprefix("com.foculoom.")) if bundle_ids else slug(child.name.removesuffix(".com"))
            candidates.append(
                {
                    "product_id": product_id,
                    "display_name": child.name.removesuffix(".com"),
                    "local_path": str(child),
                    "scope": root_name,
                    "bundle_ids": bundle_ids,
                    "website_domain": domain,
                    "repository": git,
                    "manifest": manifest,
                    "kind": "local_candidate",
                    "entity_type": "product",
                    "confidence": "MEDIUM" if git.get("repository") or bundle_ids else "LOW",
                    "provenance": [str(child)],
                }
            )
    return candidates


def merge_candidates(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for record in records:
        durable = record.get("bundle_id") or (record.get("bundle_ids") or [None])[0]
        key = f"bundle:{durable}" if durable else f"product:{record['product_id']}"
        current = merged.setdefault(
            key,
            {
                "product_id": record["product_id"],
                "display_names": [],
                "bundle_ids": [],
                "repositories": [],
                "local_paths": [],
                "distribution_states": [],
                "website_domains": [],
                "confidence": "LOW",
                "provenance": [],
                "evidence_kinds": [],
            },
        )
        if record.get("display_name") and record["display_name"] not in current["display_names"]:
            current["display_names"].append(record["display_name"])
        for bundle_id in [record.get("bundle_id"), *(record.get("bundle_ids") or [])]:
            if bundle_id and bundle_id not in current["bundle_ids"]:
                current["bundle_ids"].append(bundle_id)
        repository_id = (record.get("repository") or {}).get("repository_id")
        if repository_id and repository_id not in current["repositories"]:
            current["repositories"].append(repository_id)
        if record.get("local_path") and record["local_path"] not in current["local_paths"]:
            current["local_paths"].append(record["local_path"])
        if record.get("distribution_state") and record["distribution_state"] not in current["distribution_states"]:
            current["distribution_states"].append(record["distribution_state"])
        if record.get("website_domain") and record["website_domain"] not in current["website_domains"]:
            current["website_domains"].append(record["website_domain"])
        if record.get("kind") not in current["evidence_kinds"]:
            current["evidence_kinds"].append(record["kind"])
        current["provenance"].extend(item for item in record.get("provenance", []) if item not in current["provenance"])
        if record.get("confidence") == "HIGH" or current["confidence"] == "LOW" and record.get("confidence") == "MEDIUM":
            current["confidence"] = record["confidence"]
    return sorted(merged.values(), key=lambda item: item["product_id"])


def discover(
    *, foculoom: Path = DEFAULT_FOCULOOM, history: Path = DEFAULT_HISTORY
) -> dict[str, Any]:
    distribution = historical_distribution_records(history)
    local = local_candidates(foculoom)
    inaccessible = []
    if not history.exists():
        inaccessible.append({"source": str(history), "reason": "not_available"})
    if not foculoom.exists():
        inaccessible.append({"source": str(foculoom), "reason": "not_available"})
    candidates = merge_candidates([*distribution, *local])
    return {
        "schema_version": 2,
        "company": {
            "entity_type": "company",
            "entity_id": "foculoom",
            "provenance": ["local Foculoom workspace root", str(foculoom)],
        },
        "discovery_input": "company identity plus independent local/distribution evidence; registry excluded",
        "sources": {
            "historical_distribution": str(history),
            "local_foculoom_roots": str(foculoom),
            "public_website": {"state": "LOCAL_MIRROR_SCANNED", "root": str(foculoom / "web")},
            "github_organization": {"state": "REMOTE_API_NOT_QUERIED", "reason": "no authenticated API evidence supplied"},
            "app_store_connect": {"state": "UNAVAILABLE_IN_THIS_RUN", "reason": "no live ASC session or export supplied"},
        },
        "inaccessible_sources": inaccessible,
        "candidates": candidates,
        "metrics": {
            "candidate_count": len(candidates),
            "high_confidence_count": sum(item["confidence"] == "HIGH" for item in candidates),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--foculoom", type=Path, default=DEFAULT_FOCULOOM)
    parser.add_argument("--history", type=Path, default=DEFAULT_HISTORY)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = discover(foculoom=args.foculoom, history=args.history)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
