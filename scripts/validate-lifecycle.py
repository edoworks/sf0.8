#!/usr/bin/env python3
"""Fail closed when factory successor and lifecycle records disagree."""

from __future__ import annotations

import json
from pathlib import Path
import re


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


def portfolio_errors(portfolio: str) -> list[str]:
    """Validate invariants that can be checked from the portable registry alone."""
    try:
        repo_text = portfolio.split("repos:\n", 1)[1].split("\nsurfaces:", 1)[0]
        surface_text = portfolio.split("surfaces:\n", 1)[1].split("\ninventory_notes:", 1)[0]
    except IndexError:
        return ["portfolio registry is missing repos or surfaces"]

    repo_blocks = [block for block in re.split(r"(?=  - id: )", repo_text) if block.strip()]
    surface_blocks = [block for block in re.split(r"(?=  - id: )", surface_text) if block.strip()]
    factory_blocks = [block for block in repo_blocks if "purpose:" in block and "factory" in block.split("purpose:", 1)[1].split("\n", 1)[0]]

    errors = []
    active_factories = [block for block in factory_blocks if "lifecycle: active" in block]
    if len(active_factories) != 1:
        errors.append(f"expected exactly one active factory, found {len(active_factories)}")
    if not any("id: edoworks/sf0.8" in block and "lifecycle: active" in block for block in active_factories):
        errors.append("sf0.8 is not the sole active factory")
    active_product = next(
        (line.split(":", 1)[1].strip() for line in portfolio.splitlines() if line.startswith("active_private_product:")),
        None,
    )
    if active_product in {"null", "~", "''", '""'}:
        active_product = None
    if active_product and not any(
        f"id: {active_product}" in block and "lifecycle: active" in block for block in repo_blocks
    ):
        errors.append(f"active private product is not active in the repo registry: {active_product}")
    if active_product:
        active_block = next(
            (block for block in repo_blocks if f"id: {active_product}" in block), ""
        )
        if "revival_issue:" not in active_block:
            errors.append(f"active private product lacks a revival issue: {active_product}")
    for block in repo_blocks + surface_blocks:
        if "disposition:" not in block:
            item = block.split("id:", 1)[1].split("\n", 1)[0].strip() if "id:" in block else "unknown"
            errors.append(f"inventoried item lacks a disposition: {item}")
    for block in surface_blocks:
        if "lifecycle: deployed" in block and "release_evidence:" not in block:
            item = block.split("id:", 1)[1].split("\n", 1)[0].strip() if "id:" in block else "unknown"
            errors.append(f"deployed public surface lacks release evidence: {item}")
    return errors


def continuation_errors(texts: list[str]) -> list[str]:
    errors = []
    for path, text in texts:
        lowered = text.lower()
        if "sf0.7 is the active factory" in lowered:
            errors.append(f"stale sf0.7 authority in {path}")
        if "sf0.7" in lowered and "read-only" not in lowered and "deprecated" not in lowered:
            errors.append(f"unqualified sf0.7 reference in {path}")
        if "sf0.5" in lowered and "read-only" not in lowered and "frozen" not in lowered:
            errors.append(f"unqualified sf0.5 reference in {path}")
    return errors


def legacy_state_errors(status: dict | None, queue: dict | None) -> list[str]:
    errors = []
    if status is not None:
        if status.get("state") != "deprecated_read_only":
            errors.append("sf0.7 status is not deprecated_read_only")
        if status.get("active_increment") is not None:
            errors.append("sf0.7 has an active increment")
    if queue is not None:
        if queue.get("read_only") is not True:
            errors.append("sf0.7 queue is not read-only")
        if queue.get("lifecycle") != "deprecated_read_only":
            errors.append("sf0.7 queue lifecycle drifted")
        if any(item.get("status") == "active" for item in queue.get("increments", [])):
            errors.append("sf0.7 queue contains active work")
    return errors


def main() -> None:
    portfolio = PORTFOLIO.read_text(encoding="utf-8")
    for error in portfolio_errors(portfolio):
        require(False, error)
    require("active_factory: edoworks/sf0.8" in portfolio, "sf0.8 is not the active factory")
    active_product = next(
        (line.split(":", 1)[1].strip() for line in portfolio.splitlines()
         if line.startswith("active_private_product:")),
        "null",
    )
    if active_product not in {"null", "~", "''", '""'}:
        require(
            "revival_issue:" in section(portfolio, active_product),
            "active private product lacks a revival issue",
        )
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

    continuation_texts = [(path, path.read_text(encoding="utf-8")) for path in CONTINUATIONS if path.exists()]
    for error in continuation_errors(continuation_texts):
        require(False, error)

    status = None
    if SF07_STATUS.exists():
        status = json.loads(SF07_STATUS.read_text(encoding="utf-8"))
    queue = None
    if SF07_QUEUE.exists():
        queue = json.loads(SF07_QUEUE.read_text(encoding="utf-8"))
    for error in legacy_state_errors(status, queue):
        require(False, error)

    print("lifecycle validation passed: sf0.8 is sole active factory")


if __name__ == "__main__":
    main()
