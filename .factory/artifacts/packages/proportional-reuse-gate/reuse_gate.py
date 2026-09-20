"""Dependency-free proportional reuse decision contract."""

from __future__ import annotations

import math


def required_search(change_units: int) -> int:
    if change_units < 1:
        raise ValueError("change_units must be positive")
    return max(1, math.ceil(change_units / 8))


def decide(change_units: int, searched: int, compatible: int, reason: str = "") -> str:
    minimum = required_search(change_units)
    if searched < minimum or compatible < 0 or compatible > searched:
        return "BLOCKED"
    if compatible == 0 and not reason.strip():
        return "BLOCKED"
    return "REUSE" if compatible else "BUILD_NEW"
