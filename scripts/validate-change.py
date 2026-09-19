#!/usr/bin/env python3
"""Enforce proportional ecosystem evidence for substantial changed paths."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from ecosystem_gates import validate_change_record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path)
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    record = None
    if args.record:
        record = json.loads(args.record.read_text(encoding="utf-8"))
    result = validate_change_record(args.paths, record)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["decision"] != "BLOCKED" else 1


if __name__ == "__main__":
    sys.exit(main())
