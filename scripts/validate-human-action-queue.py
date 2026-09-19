#!/usr/bin/env python3
"""Validate the executable human action queue."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from human_actions import validate_queue


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    errors = validate_queue(json.loads(args.record.read_text(encoding="utf-8")))
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("human action queue validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
