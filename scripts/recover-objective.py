#!/usr/bin/env python3
"""Search and classify bounded recovery candidates without executing them."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from recovery import classify_blocker, recovery_decision, search_solutions

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--objective", default="")
    parser.add_argument("--error", default="")
    parser.add_argument("--operation", default="")
    parser.add_argument("--attempts", type=int, default=0)
    parser.add_argument("--attempted", action="append", default=[])
    args = parser.parse_args()
    registry = json.loads((ROOT / ".factory/recovery/solutions.json").read_text(encoding="utf-8"))
    sources = json.loads((ROOT / ".factory/recovery/sources.json").read_text(encoding="utf-8"))
    candidates = search_solutions(args.query, registry, sources, objective_id=args.objective, attempted=args.attempted)
    blocker = {"class": classify_blocker(error=args.error, operation=args.operation), "error": args.error, "operation": args.operation}
    result = recovery_decision(blocker=blocker, candidates=candidates, attempts=args.attempts, max_attempts=registry["policy"]["max_attempts_per_objective"])
    result["blocker"] = blocker
    result["candidates"] = candidates
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
