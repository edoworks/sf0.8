#!/usr/bin/env python3
"""Ingest one externally observed experiment result into factory memory."""

import argparse
import json
from pathlib import Path

from evidence_frontier import apply_result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("result", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    record = json.loads(args.record.read_text(encoding="utf-8"))
    result = json.loads(args.result.read_text(encoding="utf-8"))
    args.output.write_text(json.dumps(apply_result(record, result), indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
