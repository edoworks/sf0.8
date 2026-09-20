#!/usr/bin/env python3
"""Validate shareability dispositions and their evidence."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from ecosystem_gates import validate_reuse_registry

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    path = ROOT / ".factory" / "artifacts" / "reuse-registry.json"
    errors = validate_reuse_registry(json.loads(path.read_text(encoding="utf-8")))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("reuse registry validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
