#!/usr/bin/env python3
"""Scan public surfaces for identity-governance contradictions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from public_identity import scan


ROOT = Path(__file__).resolve().parents[1]


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="+", type=Path)
    parser.add_argument("--registry", type=Path, default=ROOT / ".factory/identity-registry.json")
    parser.add_argument("--private-pattern-file", type=Path)
    parser.add_argument("--observations", type=Path)
    parser.add_argument("--overrides", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--subject-identity")
    parser.add_argument("--mode", choices=("audit", "release"), default="audit")
    args = parser.parse_args()
    if args.mode == "release" and not args.subject_identity:
        print(json.dumps({"schema_version": 1, "mode": args.mode, "status": "ERROR", "error": "release scans require --subject-identity"}, sort_keys=True))
        return 2
    try:
        patterns = args.private_pattern_file.read_text(encoding="utf-8").splitlines() if args.private_pattern_file else []
        report = scan(
            args.roots,
            _json(args.registry),
            private_patterns=patterns,
            observations=_json(args.observations) if args.observations else None,
            overrides=_json(args.overrides).get("overrides", []) if args.overrides else None,
            mode=args.mode,
            subject_identity=args.subject_identity,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError):
        print(json.dumps({"schema_version": 1, "mode": args.mode, "status": "ERROR", "error": "scanner input is invalid"}, sort_keys=True))
        return 2
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if report["override_errors"]:
        return 2
    if args.mode == "release" and report["status"] != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
