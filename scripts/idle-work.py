#!/usr/bin/env python3
"""Discover, dispatch, and optionally execute one bounded idle-work item."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from idle_work import ROOT, discover_idle_work, select_work, validate_waiting_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget", type=float, default=5.0)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    report = discover_idle_work(ROOT, args.budget)
    selected = select_work(report)
    report["selected"] = selected
    if args.execute and selected and selected.get("action"):
        completed = subprocess.run(selected["action"], cwd=ROOT, capture_output=True, text=True, check=False)
        report["execution"] = {
            "candidate": selected["id"],
            "command": selected["action"],
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
        report["execution"]["status"] = "PASSED" if completed.returncode == 0 else "FAILED"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    errors = validate_waiting_report(report)
    if errors:
        print(json.dumps({"errors": errors}, indent=2), file=sys.stderr)
        return 1
    if report["status"] == "READY_WORK_FOUND":
        if report.get("execution", {}).get("status") == "FAILED":
            return 1
        return 0
    if report["status"] == "WAITING_DEPENDENCY":
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main())
