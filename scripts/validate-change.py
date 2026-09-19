#!/usr/bin/env python3
"""Enforce proportional ecosystem evidence for substantial changed paths."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from ecosystem_gates import validate_change_record, validate_changed_records


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path)
    parser.add_argument("--changed-ledgers", action="store_true")
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    if args.changed_ledgers:
        ledger_paths = [ROOT / path for path in args.paths if path.startswith(".factory/artifacts/ledger/issue-") and path.endswith(".json")]
        records = [json.loads(path.read_text(encoding="utf-8")) for path in ledger_paths if path.is_file()]
        bindings = json.loads((ROOT / ".factory/control-plane-bindings.json").read_text(encoding="utf-8"))
        result = validate_changed_records(args.paths, records, bindings)
    else:
        record = json.loads(args.record.read_text(encoding="utf-8")) if args.record else None
        result = validate_change_record(args.paths, record)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["decision"] != "BLOCKED" else 1


if __name__ == "__main__":
    sys.exit(main())
