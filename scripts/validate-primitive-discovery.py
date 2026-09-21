#!/usr/bin/env python3
"""Validate the governed capability primitive inventory."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from primitive_discovery import validate_inventory


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", nargs="?", type=Path, default=ROOT / ".factory/capability-primitive-inventory.json")
    args = parser.parse_args()
    errors = validate_inventory(json.loads(args.record.read_text(encoding="utf-8")))
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("primitive discovery inventory validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
