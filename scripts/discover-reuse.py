#!/usr/bin/env python3
"""Search the canonical registry before a new implementation is started."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ecosystem_gates import discover_registry

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("capability")
    args = parser.parse_args()
    needle = args.capability.lower()
    registry = json.loads((ROOT / ".factory" / "artifacts" / "reuse-registry.json").read_text())
    matches = discover_registry(registry, needle)
    print(json.dumps({"search_order": registry["search_order"], "matches": matches}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
