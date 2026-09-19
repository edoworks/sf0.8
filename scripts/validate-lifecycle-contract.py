#!/usr/bin/env python3
"""Validate the explicit repository lifecycle and destructive-action contract."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from lifecycle_contract import deletion_errors, transition_allowed

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / ".factory/lifecycle-contract.json"
PORTFOLIO = ROOT / ".factory/portfolio.yaml"
MANIFESTS = ROOT / ".factory/artifacts/portfolio-archaeology/preservation-manifests.json"
EXERCISE = ROOT / ".factory/artifacts/portfolio-archaeology/archive-candidate-exercise.json"


def portfolio_items(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for section in ("repos:", "surfaces:"):
        if section not in text:
            continue
        part = text.split(section, 1)[1]
        if section == "repos:":
            part = part.split("\nsurfaces:", 1)[0]
        elif "\ninventory_notes:" in part:
            part = part.split("\ninventory_notes:", 1)[0]
        for block in part.split("  - id: ")[1:]:
            lines = block.splitlines()
            item = {"id": lines[0].strip()} if lines else {}
            for line in lines[1:]:
                if line.startswith("    ") and ":" in line and not line.startswith("      "):
                    key, value = line.strip().split(":", 1)
                    item[key] = value.strip().strip('"')
            items.append(item)
    return items


def validate() -> list[str]:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    errors: list[str] = []
    states = set(contract.get("states", []))
    if len(states) != len(contract.get("states", [])):
        errors.append("lifecycle states must be unique")
    for state, targets in contract.get("transitions", {}).items():
        if state not in states or any(target not in states for target in targets):
            errors.append(f"transition references unknown lifecycle state: {state}")
    for item in portfolio_items(PORTFOLIO.read_text(encoding="utf-8")):
        lifecycle = item.get("lifecycle", "").upper()
        if lifecycle and lifecycle not in states and lifecycle not in {"DEPRECATED", "FROZEN_LEGACY", "PARKED", "CONDITIONAL", "INTERNAL", "RETIRED"}:
            errors.append(f"{item.get('id')}: lifecycle is not in the explicit contract: {lifecycle}")
        if "disposition" not in item:
            errors.append(f"{item.get('id')}: disposition is required")
        if "destructive_actions" not in item and item.get("id") in {"edoworks/sf0.8", "edoworks/product-a", "foculoom/vorynce"}:
            errors.append(f"{item.get('id')}: destructive actions are not explicit")
        if item.get("id") == "edoworks/product-a":
            if lifecycle != "SHELVED":
                errors.append("edoworks/product-a: canonical lifecycle must be SHELVED")
            if item.get("product_work") != "prohibited":
                errors.append("edoworks/product-a: product work must be prohibited while shelved")
            if item.get("read_only") != "true":
                errors.append("edoworks/product-a: shelved product must be read-only")
            if item.get("resume_requires_owner_instruction") != "true":
                errors.append("edoworks/product-a: resumption must require owner instruction")
            if item.get("archive_eligibility") != "":
                # The scalar parser cannot safely interpret nested YAML; the
                # canonical text guard below checks the required blocked fields.
                pass
    portfolio_text = PORTFOLIO.read_text(encoding="utf-8")
    if "active_private_product: null" not in portfolio_text:
        errors.append("portfolio: active_private_product must be null while Product A is shelved")
    if "state: blocked" not in portfolio_text or "External repository archive state" not in portfolio_text:
        errors.append("edoworks/product-a: archive eligibility must remain explicitly blocked with a reason")
    if MANIFESTS.exists():
        manifests = json.loads(MANIFESTS.read_text(encoding="utf-8")).get("manifests", [])
        for manifest in manifests:
            state = manifest.get("state")
            if state in {"DELETION_CANDIDATE", "HUMAN_AUTHORIZED_DELETE"}:
                errors.extend(f"{manifest.get('candidate')}: {error}" for error in deletion_errors(contract, manifest))
    if EXERCISE.exists():
        exercise = json.loads(EXERCISE.read_text(encoding="utf-8"))
        transitions = exercise.get("exercised_transitions", [])
        for transition in transitions:
            if not transition_allowed(contract, transition.get("from", ""), transition.get("to", "")):
                errors.append(f"{exercise.get('candidate')}: unsafe exercised transition")
        if exercise.get("deletion_authorized") or exercise.get("destructive_action_performed"):
            errors.append(f"{exercise.get('candidate')}: archive exercise cannot authorize or perform deletion")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(f"ERROR: {problem}" for problem in problems))
        sys.exit(1)
    print("lifecycle contract validation passed")
