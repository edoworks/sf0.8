#!/usr/bin/env python3
"""CLI entry point for the contribution classification gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ecosystem_gates import contribution_gate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path, help="JSON metadata record; contents are never executed")
    args = parser.parse_args()
    record = json.loads(args.record.read_text(encoding="utf-8"))
    result = contribution_gate(
        **record["checks"],
        product_specific=record["product_specific"],
        portable=record["portable"],
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
