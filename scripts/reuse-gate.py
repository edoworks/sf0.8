#!/usr/bin/env python3
"""CLI entry point for the proportional reuse gate."""

from __future__ import annotations

import argparse
import json

from ecosystem_gates import reuse_gate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("change_units", type=int)
    parser.add_argument("searched", type=int)
    parser.add_argument("compatible", type=int)
    parser.add_argument("--reason", default="")
    args = parser.parse_args()
    result = reuse_gate(args.change_units, args.searched, args.compatible, args.reason)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["decision"] != "BLOCKED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
