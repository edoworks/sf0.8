#!/usr/bin/env python3
"""Run the repository-wide evidence-integrity consistency guard."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from evidence_integrity import (
    validate_continuation_state,
    validate_evidence_references,
    validate_qualification_ledger,
    validate_reconciliation,
    validate_remote_snapshot,
    validate_timeout_receipt,
)


def tracked_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, capture_output=True, check=False
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip() or "git ls-files failed")
    return [item for item in result.stdout.decode("utf-8").split("\0") if item]


def evidence_at_revision(root: Path, references: list[dict]) -> list[str]:
    errors: list[str] = []
    for index, reference in enumerate(references):
        revision = str(reference.get("revision", ""))
        path = str(reference.get("path", ""))
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{revision}:{path}"],
            cwd=root,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            errors.append(f"evidence_references[{index}]: evidence is absent at revision {revision}: {path}")
    return errors


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_supersessions(root: Path) -> list[str]:
    errors: list[str] = []
    registry_path = root / ".factory/evidence-supersessions.json"
    registry = load(registry_path)
    if set(registry) != {"schema_version", "supersessions"}:
        errors.append("evidence supersession registry fields drifted")
    if registry.get("schema_version") != 1:
        errors.append("evidence supersession registry schema is invalid")
    records = registry.get("supersessions")
    if not isinstance(records, list):
        return errors + ["evidence supersessions must be a list"]

    originals: set[str] = set()
    corrections: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict) or set(record) != {"original", "correction"}:
            errors.append(f"evidence supersessions[{index}] fields drifted")
            continue
        original = str(record["original"])
        correction = str(record["correction"])
        if original in originals or correction in corrections:
            errors.append("evidence supersession paths must be unique")
        originals.add(original)
        corrections.add(correction)
        original_path = root / original
        correction_path = root / correction
        if not original_path.is_file():
            errors.append(f"superseded evidence is missing: {original}")
        if not correction_path.is_file():
            errors.append(f"superseding evidence is missing: {correction}")
            continue
        correction_record = load(correction_path)
        if correction_record.get("supersedes") != original:
            errors.append(f"superseding evidence does not point to original: {correction}")
        if not str(correction_record.get("status", "")).startswith("SUPERSEDES_"):
            errors.append(f"superseding evidence status is invalid: {correction}")

    discovered = set()
    for path in sorted((root / ".factory/artifacts/evidence").rglob("*.json")):
        try:
            record = load(path)
        except json.JSONDecodeError:
            continue
        if "supersedes" in record:
            discovered.add(str(path.relative_to(root)))
    if discovered != corrections:
        errors.append("evidence supersession registry does not match correction records")
    return errors


def validate(
    root: Path,
    state_path: Path,
    ledger_path: Path,
    continuation_path: Path,
    canonical_continuation_path: Path,
    remote_snapshot_path: Path,
) -> list[str]:
    state = load(state_path)
    requirements = load(root / ".factory/control-plane-requirements.json")
    queue = load(root / ".factory/human-action-queue.json")
    lifecycle = load(root / ".factory/lifecycle-contract.json")
    ledger = load(ledger_path)
    canonical_continuation = load(canonical_continuation_path)
    snapshot = load(remote_snapshot_path)
    errors = validate_qualification_ledger(ledger)
    expected_continuation = str(canonical_continuation_path.relative_to(root))
    if state.get("continuation_path") != expected_continuation:
        errors.append("integrity state does not reference the canonical continuation record")
    errors.extend(validate_continuation_state(canonical_continuation, continuation_path.read_text(encoding="utf-8")))
    reconciled_state = dict(state)
    reconciled_state["continuation"] = canonical_continuation
    errors.extend(validate_reconciliation(
        reconciled_state,
        requirements,
        queue,
        lifecycle,
        (root / ".factory/portfolio.yaml").read_text(encoding="utf-8"),
    ))
    references = state.get("evidence_references", [])
    errors.extend(validate_evidence_references(references, root, tracked_paths(root)))
    errors.extend(evidence_at_revision(root, references))
    errors.extend(validate_remote_snapshot(snapshot, state.get("gates", {})))
    errors.extend(validate_supersessions(root))
    for path in sorted((root / ".factory/artifacts/evidence/verification-receipts").glob("*.json")):
        errors.extend(f"{path.relative_to(root)}: {error}" for error in validate_timeout_receipt(load(path)))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=ROOT / ".factory/artifacts/evidence/integrity-state.json")
    parser.add_argument("--ledger", type=Path, default=ROOT / ".factory/qualification-ledger.json")
    parser.add_argument("--continuation", type=Path, default=ROOT / ".opencode-config/commands/continue-sf08.md")
    parser.add_argument("--canonical-continuation", type=Path, default=ROOT / ".factory/continuation-state.json")
    parser.add_argument("--remote-snapshot", type=Path, default=ROOT / ".factory/remote-state-snapshot.json")
    args = parser.parse_args()
    try:
        errors = validate(
            ROOT,
            args.state,
            args.ledger,
            args.continuation,
            args.canonical_continuation,
            args.remote_snapshot,
        )
    except (OSError, RuntimeError, KeyError, json.JSONDecodeError) as error:
        errors = [str(error)]
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("evidence integrity validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
