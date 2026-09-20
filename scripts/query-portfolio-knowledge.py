#!/usr/bin/env python3
"""Query the bounded portfolio archaeology knowledge records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / ".factory" / "artifacts" / "portfolio-archaeology" / "knowledge-records.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("term", nargs="?", help="case-insensitive product, lesson, or evidence term")
    args = parser.parse_args()
    payload = json.loads(RECORDS.read_text(encoding="utf-8"))
    records = payload["records"]
    if args.term:
        needle = args.term.lower()
        records = [
            record
            for record in records
            if needle in json.dumps(record, sort_keys=True).lower()
        ]
    print(json.dumps({"count": len(records), "records": records}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
