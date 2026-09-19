#!/usr/bin/env python3
"""Select bounded, independent ready work without starting blocked lanes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


def select_ready_lanes(document: dict[str, Any], limit: int | None = None) -> dict[str, Any]:
    active_resources = set(document.get("active_resources", []))
    selected: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for lane in sorted(document.get("lanes", []), key=lambda item: (item.get("priority", 999), item.get("work", ""))):
        if lane.get("state") != "READY":
            continue
        conflicts = set(lane.get("conflicts", []))
        resource = lane.get("resource")
        if conflicts & active_resources or resource in active_resources:
            skipped.append({"work": lane.get("work", ""), "reason": "resource_or_conflict"})
            continue
        selected.append(lane)
        active_resources.add(resource)
        if limit is not None and len(selected) >= limit:
            break
    ready_count = sum(lane.get("state") == "READY" for lane in document.get("lanes", []))
    portfolio = document.get("portfolio", {})
    discovery_confidence = portfolio.get("discovery_confidence", "UNKNOWN")
    unreconciled = int(portfolio.get("unreconciled_product_candidates", 0))
    return {
        "selected": [lane.get("work") for lane in selected],
        "skipped": skipped,
        "ready_work": ready_count,
        "known_ready_work_idle": max(0, ready_count - len(selected)) if selected else ready_count,
        # Kept as a compatibility alias, but it is explicitly known-work only.
        "idle_despite_ready_work": max(0, ready_count - len(selected)) if selected else ready_count,
        "portfolio_discovery_confidence": discovery_confidence,
        "unreconciled_product_candidates": unreconciled,
        "portfolio_complete": discovery_confidence == "COMPLETE" and unreconciled == 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("lanes", type=Path)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    result = select_ready_lanes(json.loads(args.lanes.read_text(encoding="utf-8")), args.limit)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["idle_despite_ready_work"] == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
