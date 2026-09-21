#!/usr/bin/env python3
"""Validate one download or verified external-use signal."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from primitive_discovery import apply_reach_signal


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("signal", type=Path)
    parser.add_argument("--inventory", type=Path, default=ROOT / ".factory/capability-primitive-inventory.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    signal = json.loads(args.signal.read_text(encoding="utf-8"))
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    try:
        updated = apply_reach_signal(inventory, signal)
    except ValueError as error:
        print(f"ERROR: {error}")
        return 1
    if args.output:
        args.output.write_text(json.dumps(updated, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(json.dumps({"status": "VALID", "signal": signal["signal_id"], "inventory": updated}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
