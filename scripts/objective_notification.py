#!/usr/bin/env python3
"""Map objective evidence to the sanitized completion-notification result."""

from __future__ import annotations

from typing import Any

try:
    from .objective_state import evaluate
except ImportError:
    from objective_state import evaluate


def notification_result(record: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    result = evaluate(record)
    return ("completed" if result["objective_complete"] else "blocked", result)
