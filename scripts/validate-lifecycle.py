#!/usr/bin/env python3
"""Fail closed when factory successor and lifecycle records disagree."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / ".factory" / "portfolio.yaml"
FOCUS = ROOT / "docs" / "portfolio-focus.md"
CONTINUATIONS = (
    Path.home() / ".config" / "opencode" / "commands" / "continue-original.md",
    Path.home() / ".config" / "opencode" / "commands" / "continue-sf08.md",
)
SF07_STATUS = Path("/Users/hello/sf0.7/factory/status.json")
SF07_QUEUE = Path("/Users/hello/sf0.7/factory/queue.json")


def section(text: str, item_id: str, next_id: str | None = None) -> str:
    start = text.index(f"  - id: {item_id}")
    end = text.find(f"  - id: {next_id}", start) if next_id else len(text)
    return text[start : end if end >= 0 else len(text)]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"lifecycle validation failed: {message}")


def main() -> None:
    portfolio = PORTFOLIO.read_text(encoding="utf-8")
    require("active_factory: edoworks/sf0.8" in portfolio, "sf0.8 is not the active factory")
    require("active_private_product: edoworks/product-a" in portfolio, "active private product drifted")
    require("active_commercial_experiment: edoworks/rung" in portfolio, "commercial experiment drifted")

    sf07 = section(portfolio, "foculoom/sf0.7", "foculoom/sf0.5")
    require("lifecycle: deprecated" in sf07, "sf0.7 is not deprecated")
    require("read_only: true" in sf07, "sf0.7 is not read-only")
    require("resume_requires_owner_instruction: true" in sf07, "sf0.7 revival guard missing")

    sf05 = section(portfolio, "foculoom/sf0.5")
    require("lifecycle: frozen_legacy" in sf05, "sf0.5 is not frozen legacy")
    require("read_only: true" in sf05, "sf0.5 is not read-only")
    require("resume_requires_owner_instruction: true" in sf05, "sf0.5 revival guard missing")
    require(FOCUS.exists(), "portfolio focus document missing")

    for path in CONTINUATIONS:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        require("sf0.7 is the active factory" not in text, f"stale sf0.7 authority in {path}")
        require("sf0.7" not in text or "read-only" in text or "deprecated" in text, f"unqualified sf0.7 reference in {path}")
        require("sf0.5" not in text or "read-only" in text or "frozen" in text, f"unqualified sf0.5 reference in {path}")

    if SF07_STATUS.exists():
        status = json.loads(SF07_STATUS.read_text(encoding="utf-8"))
        require(status.get("state") == "deprecated_read_only", "sf0.7 status is not deprecated_read_only")
        require(status.get("active_increment") is None, "sf0.7 has an active increment")
    if SF07_QUEUE.exists():
        queue = json.loads(SF07_QUEUE.read_text(encoding="utf-8"))
        require(queue.get("read_only") is True, "sf0.7 queue is not read-only")
        require(queue.get("lifecycle") == "deprecated_read_only", "sf0.7 queue lifecycle drifted")
        require(all(item.get("status") != "active" for item in queue.get("increments", [])), "sf0.7 queue contains active work")

    print("lifecycle validation passed: sf0.8 is sole active factory")


if __name__ == "__main__":
    main()
