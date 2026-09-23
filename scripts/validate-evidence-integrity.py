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
)


def tracked_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, capture_output=True, check=False
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip() or "git ls-files failed")
    return [item for item in result.stdout.decode("utf-8").split("\0") if item]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(root: Path, state_path: Path, ledger_path: Path, continuation_path: Path) -> list[str]:
    state = load(state_path)
    requirements = load(root / ".factory/control-plane-requirements.json")
    queue = load(root / ".factory/human-action-queue.json")
    lifecycle = load(root / ".factory/lifecycle-contract.json")
    ledger = load(ledger_path)
    errors = validate_qualification_ledger(ledger)
    errors.extend(validate_continuation_state(state["continuation"], continuation_path.read_text(encoding="utf-8")))
    errors.extend(validate_reconciliation(
        state,
        requirements,
        queue,
        lifecycle,
        (root / ".factory/portfolio.yaml").read_text(encoding="utf-8"),
    ))
    errors.extend(validate_evidence_references(state.get("evidence_references", []), root, tracked_paths(root)))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=ROOT / ".factory/artifacts/evidence/integrity-state.json")
    parser.add_argument("--ledger", type=Path, default=ROOT / ".factory/qualification-ledger.json")
    parser.add_argument("--continuation", type=Path, default=Path.home() / ".config/opencode/commands/continue-sf08.md")
    args = parser.parse_args()
    try:
        errors = validate(ROOT, args.state, args.ledger, args.continuation)
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
