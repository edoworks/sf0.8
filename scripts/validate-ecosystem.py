#!/usr/bin/env python3
"""Run the local artifact and contribution integrity checks."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import re

ROOT = Path(__file__).resolve().parents[1]


def validate_package_manifests() -> list[str]:
    errors: list[str] = []
    pattern = re.compile(r"^\d+\.\d+\.\d+$")
    for path in sorted((ROOT / ".factory/artifacts/packages").glob("*/MANIFEST.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        for field in ("artifact", "version", "source_revision", "distribution", "release_state", "publication_approved"):
            if field not in record:
                errors.append(f"{path}: missing package manifest field: {field}")
        if not pattern.match(str(record.get("version", ""))):
            errors.append(f"{path}: version must be semantic versioning")
        if record.get("release_state") not in {"CANDIDATE_UNRELEASED", "RELEASED"}:
            errors.append(f"{path}: invalid release_state")
        if record.get("release_state") == "RELEASED" and "working-tree" in str(record.get("source_revision")):
            errors.append(f"{path}: released package cannot use working-tree provenance")
        if record.get("publication_approved") is not False:
            errors.append(f"{path}: publication approval must remain false")
    return errors


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    validator = load("validate_artifacts", "validate-artifacts.py")
    errors = validator.validate()
    errors.extend(validate_package_manifests())
    gates = load("ecosystem_gates", "ecosystem_gates.py")
    registry = json.loads((ROOT / ".factory" / "artifacts" / "reuse-registry.json").read_text(encoding="utf-8"))
    errors.extend(gates.validate_reuse_registry(registry))
    errors.extend(gates.validate_consumer_evidence(registry, ROOT))
    for record in registry.get("artifacts", []):
        for relative in record.get("verification_evidence", []):
            if not (ROOT / relative).is_file():
                errors.append(f"{record.get('id')}: verification evidence does not exist: {relative}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("ecosystem validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
