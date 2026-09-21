#!/usr/bin/env python3
"""Validate host-side audio replay evidence without overstating device proof."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys


REQUIRED_REPORT = {
    "schema_version",
    "runner",
    "environment",
    "device_claim",
    "fixtures",
}
REQUIRED_FIXTURE = {
    "id",
    "path",
    "sha256",
    "observations",
    "decision",
    "status",
    "sample_rate",
    "frame_count",
}
ALLOWED_STATUS = {"PASS", "FAIL"}
ALLOWED_DECISION = {"TARGET", "NON_TARGET", "ABSTAIN"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_finite_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate_report(document: dict, root: Path) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_REPORT - document.keys()
    errors.extend(f"report: missing {field}" for field in sorted(missing))
    if document.get("schema_version") != 1:
        errors.append("report: schema_version must be 1")
    if document.get("device_claim") != "HOST_REPLAY_ONLY":
        errors.append("report: device_claim must be HOST_REPLAY_ONLY")
    if not isinstance(document.get("runner"), dict):
        errors.append("report: runner must be an object")
    if not isinstance(document.get("environment"), dict):
        errors.append("report: environment must be an object")
    fixtures = document.get("fixtures")
    if not isinstance(fixtures, list) or not fixtures:
        errors.append("report: fixtures must be a non-empty list")
        return errors

    ids: set[str] = set()
    for index, fixture in enumerate(fixtures):
        prefix = f"fixtures[{index}]"
        if not isinstance(fixture, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        errors.extend(f"{prefix}: missing {field}" for field in sorted(REQUIRED_FIXTURE - fixture.keys()))
        fixture_id = fixture.get("id")
        if not isinstance(fixture_id, str) or not fixture_id:
            errors.append(f"{prefix}: id must be a non-empty string")
        elif fixture_id in ids:
            errors.append(f"{prefix}: duplicate id {fixture_id}")
        elif isinstance(fixture_id, str):
            ids.add(fixture_id)
        if fixture.get("status") not in ALLOWED_STATUS:
            errors.append(f"{prefix}: status must be PASS or FAIL")
        elif fixture.get("status") == "FAIL":
            errors.append(f"{prefix}: fixture expectation failed")
        if fixture.get("decision") not in ALLOWED_DECISION:
            errors.append(f"{prefix}: decision must be TARGET, NON_TARGET, or ABSTAIN")
        observations = fixture.get("observations")
        if not isinstance(observations, list):
            errors.append(f"{prefix}: observations must be a list")
        else:
            for observation_index, observation in enumerate(observations):
                observation_prefix = f"{prefix}.observations[{observation_index}]"
                if not isinstance(observation, dict):
                    errors.append(f"{observation_prefix}: must be an object")
                    continue
                if not isinstance(observation.get("label"), str) or not observation["label"]:
                    errors.append(f"{observation_prefix}: label must be a non-empty string")
                confidence = observation.get("confidence")
                if not is_finite_number(confidence) or not 0 <= confidence <= 1:
                    errors.append(f"{observation_prefix}: confidence must be a number from 0 to 1")
        sample_rate = fixture.get("sample_rate")
        if not is_finite_number(sample_rate) or sample_rate <= 0:
            errors.append(f"{prefix}: sample_rate must be a positive number")
        frame_count = fixture.get("frame_count")
        if not isinstance(frame_count, int) or isinstance(frame_count, bool) or frame_count < 0:
            errors.append(f"{prefix}: frame_count must be a non-negative integer")
        path_value = fixture.get("path")
        if not isinstance(path_value, str):
            errors.append(f"{prefix}: path must be a string")
            continue
        path = (root / path_value).resolve()
        try:
            path.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{prefix}: path escapes the report root")
            continue
        if not path.is_file():
            errors.append(f"{prefix}: fixture does not exist: {path_value}")
            continue
        expected_hash = fixture.get("sha256")
        if not isinstance(expected_hash, str) or len(expected_hash) != 64:
            errors.append(f"{prefix}: sha256 must be a 64-character hex digest")
        elif any(character not in "0123456789abcdef" for character in expected_hash.lower()):
            errors.append(f"{prefix}: sha256 must be hexadecimal")
        elif sha256_file(path) != expected_hash.lower():
            errors.append(f"{prefix}: sha256 does not match fixture bytes")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args()
    report_path = args.report.resolve()
    root = (args.root or report_path.parent).resolve()
    try:
        document = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: cannot read report: {error}")
        return 1
    errors = validate_report(document, root)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(json.dumps({"status": "passed", "fixtures": len(document["fixtures"])}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
