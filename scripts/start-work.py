#!/usr/bin/env python3
"""Cold-session product-work entrypoint: discover before implementation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from ecosystem_gates import validate_work_start
from control_plane import capability_preflight

ROOT = Path(__file__).resolve().parents[1]


def canonical_issue_for(task: dict) -> dict | None:
    bindings = json.loads((ROOT / ".factory/control-plane-bindings.json").read_text(encoding="utf-8"))
    return bindings.get("by_capability", {}).get(str(task.get("capability", "")))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("task", type=Path)
    args = parser.parse_args()
    task = json.loads(args.task.read_text(encoding="utf-8"))
    control_plane = capability_preflight(
        task,
        repo=str(task.get("repo", "")),
        issue=task.get("issue"),
        expected_issue=canonical_issue_for(task),
    )
    if control_plane["decision"] == "BLOCKED":
        print(json.dumps({"decision": "BLOCKED", "control_plane": control_plane}, indent=2, sort_keys=True))
        return 1
    registry = json.loads((ROOT / ".factory/artifacts/reuse-registry.json").read_text(encoding="utf-8"))
    result = validate_work_start(task, registry)
    result["control_plane"] = control_plane
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["decision"] != "BLOCKED" else 1


if __name__ == "__main__":
    sys.exit(main())
