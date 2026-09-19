#!/usr/bin/env python3
"""Report completion without hiding unresolved authoritative control-plane work."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from ecosystem_gates import completion_state


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    result = completion_state(json.loads(args.record.read_text(encoding="utf-8")))
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["state"] == "DONE":
        return 0
    return 2 if result["state"] == "CONTROL_PLANE_BLOCKED" else 1


if __name__ == "__main__":
    sys.exit(main())
