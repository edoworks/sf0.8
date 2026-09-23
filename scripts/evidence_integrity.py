#!/usr/bin/env python3
"""Pure validators for timeout, evidence, continuation, and gate integrity."""

from __future__ import annotations

from datetime import date, datetime, timezone
import math
from pathlib import Path
import re
from typing import Any, Iterable


VERIFICATION_OUTCOMES = {
    "PASSED",
    "FAILED",
    "COMMAND_TIMEOUT_PROGRESSING",
    "COMMAND_TIMEOUT_NO_PROGRESS",
    "TEST_HANG_CONFIRMED",
    "INFRASTRUCTURE_ERROR",
    "INCOMPLETE_NO_RESULT",
}
CONTROL_PLANE_STATUSES = {"PROVEN", "UNPROVEN", "BLOCKED"}
GATE_STATUSES = {"OPEN", "CLOSED", "BLOCKED"}


def _timestamp(value: Any, field: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be an ISO-8601 timestamp")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{field} must be an ISO-8601 timestamp")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{field} must include a timezone")
        return None
    return parsed.astimezone(timezone.utc)


def validate_timeout_receipt(receipt: dict[str, Any]) -> list[str]:
    """Classify a timeout only when its progress evidence supports the claim."""
    errors: list[str] = []
    for field in ("current_test", "result_bundle_path"):
        if not isinstance(receipt.get(field), str) or not receipt[field].strip():
            errors.append(f"{field} is required")
    outcome = receipt.get("outcome")
    if outcome not in VERIFICATION_OUTCOMES:
        errors.append("outcome is not a supported verification outcome")
    started = _timestamp(receipt.get("started_at"), "started_at", errors)
    last_progress = _timestamp(receipt.get("last_progress_at"), "last_progress_at", errors)
    ended = _timestamp(receipt.get("ended_at"), "ended_at", errors)
    threshold = receipt.get("inactivity_threshold_seconds")
    if not isinstance(threshold, (int, float)) or isinstance(threshold, bool) or threshold <= 0:
        errors.append("inactivity_threshold_seconds must be positive")
        threshold = 0
    completed = receipt.get("completed_count")
    if not isinstance(completed, int) or completed < 0:
        errors.append("completed_count must be a non-negative integer")
        completed = 0
    progress_events = receipt.get("progress_events", [])
    if not isinstance(progress_events, list):
        errors.append("progress_events must be a list")
        progress_events = []
    if started and last_progress and last_progress < started:
        errors.append("last_progress_at precedes started_at")
    if last_progress and ended and last_progress > ended:
        errors.append("last_progress_at follows ended_at")

    has_progress = bool(progress_events or completed > 0 or (started and last_progress and last_progress > started))
    if outcome == "COMMAND_TIMEOUT_PROGRESSING" and not has_progress:
        errors.append("progressing timeout requires progress events or a later progress timestamp")

    no_progress_duration = 0.0
    if last_progress and ended:
        no_progress_duration = (ended - last_progress).total_seconds()
    if outcome in {"COMMAND_TIMEOUT_NO_PROGRESS", "TEST_HANG_CONFIRMED"}:
        if has_progress:
            errors.append("no-progress timeout cannot contain test or output progress")
        if no_progress_duration < threshold:
            errors.append("no-progress timeout must exceed the inactivity threshold")

    if outcome == "TEST_HANG_CONFIRMED":
        samples = receipt.get("process_samples")
        if not isinstance(samples, list) or len(samples) < 2:
            errors.append("confirmed hang requires at least two process samples")
        else:
            parsed_samples = []
            active_tests = set()
            for index, sample in enumerate(samples):
                if not isinstance(sample, dict):
                    errors.append(f"process_samples[{index}] must be an object")
                    continue
                parsed = _timestamp(sample.get("at"), f"process_samples[{index}].at", errors)
                if parsed:
                    parsed_samples.append(parsed)
                active_tests.add(sample.get("active_test"))
                if sample.get("output_progress") or sample.get("result_bundle_progress"):
                    errors.append("confirmed hang samples must show no output or result-bundle progress")
            if len(active_tests) != 1 or None in active_tests:
                errors.append("confirmed hang samples must identify the same active test")
            if len(parsed_samples) >= 2 and (max(parsed_samples) - min(parsed_samples)).total_seconds() < threshold:
                errors.append("confirmed hang samples must span the inactivity threshold")

    if outcome == "PASSED" and receipt.get("exit_status") != 0:
        errors.append("PASSED receipt requires exit_status 0")
    return errors


def validate_evidence_references(
    references: Iterable[dict[str, Any]],
    root: Path,
    tracked_paths: Iterable[str],
) -> list[str]:
    """Reject missing, escaping, untracked, or revision-less gate evidence."""
    errors: list[str] = []
    tracked = {str(path).replace("\\", "/") for path in tracked_paths}
    for index, reference in enumerate(references):
        prefix = f"evidence_references[{index}]"
        if not isinstance(reference, dict):
            errors.append(f"{prefix} must be an object")
            continue
        relative = str(reference.get("path", ""))
        if not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
            errors.append(f"{prefix}: path must be a safe repository-relative path")
            continue
        normalized = relative.replace("\\", "/")
        if normalized not in tracked:
            errors.append(f"{prefix}: evidence is not tracked at the referenced revision: {relative}")
        if not (root / relative).is_file():
            errors.append(f"{prefix}: evidence file does not exist: {relative}")
        revision = str(reference.get("revision", "")).strip()
        if not revision:
            errors.append(f"{prefix}: evidence revision is required")
        elif revision != "HEAD" and not re.fullmatch(r"[0-9a-fA-F]{40}", revision):
            errors.append(f"{prefix}: evidence revision must be HEAD or a full commit id")
    return errors


def _business_days_between(start: date, end: date) -> int:
    cursor = start
    count = 0
    while cursor < end:
        cursor = date.fromordinal(cursor.toordinal() + 1)
        if cursor.weekday() < 5:
            count += 1
    return count


def validate_qualification_ledger(ledger: dict[str, Any], require_promotion: bool = False) -> list[str]:
    errors: list[str] = []
    if ledger.get("ledger_version") != "1.0.0":
        errors.append("qualification ledger must use version 1.0.0")
    try:
        started = date.fromisoformat(str(ledger.get("started", "")))
    except ValueError:
        started = None
        errors.append("qualification ledger started must be an ISO date")
    receipts = ledger.get("daily_receipts")
    if not isinstance(receipts, list):
        return errors + ["daily_receipts must be a list"]
    seen: set[date] = set()
    parsed_receipts: list[tuple[date, dict[str, Any]]] = []
    for index, receipt in enumerate(receipts):
        prefix = f"daily_receipts[{index}]"
        if not isinstance(receipt, dict):
            errors.append(f"{prefix} must be an object")
            continue
        try:
            receipt_date = date.fromisoformat(str(receipt.get("date", "")))
        except ValueError:
            errors.append(f"{prefix}.date must be an ISO date")
            continue
        if receipt_date in seen:
            errors.append(f"{prefix}: duplicate date")
        seen.add(receipt_date)
        if receipt.get("weekday") != receipt_date.strftime("%A"):
            errors.append(f"{prefix}.weekday does not match its ISO date")
        if started and receipt_date < started:
            errors.append(f"{prefix}.date precedes ledger start")
        for field in ("change_description", "operator_identity"):
            if not str(receipt.get(field, "")).strip():
                errors.append(f"{prefix}.{field} is required")
        if not isinstance(receipt.get("unattended_success"), bool):
            errors.append(f"{prefix}.unattended_success must be boolean")
        if not isinstance(receipt.get("manual_repair_required"), bool):
            errors.append(f"{prefix}.manual_repair_required must be boolean")
        if receipt.get("unattended_success") and receipt.get("manual_repair_required"):
            errors.append(f"{prefix}: unattended success cannot require manual repair")
        if not isinstance(receipt.get("denominator"), int) or receipt.get("denominator", 0) <= 0:
            errors.append(f"{prefix}.denominator must be a positive integer")
        rate = receipt.get("cumulative_success_rate")
        if not isinstance(rate, (int, float)) or isinstance(rate, bool) or not 0 <= rate <= 1:
            errors.append(f"{prefix}.cumulative_success_rate must be between 0 and 1")
        if not receipt.get("unattended_success") and not str(receipt.get("failure_classification", "")).strip():
            errors.append(f"{prefix}: failed receipt requires failure_classification")
        parsed_receipts.append((receipt_date, receipt))

    parsed_receipts.sort(key=lambda item: item[0])
    weekday_receipts = [item for item in parsed_receipts if item[0].weekday() < 5]
    for (previous_date, _), (current_date, _) in zip(weekday_receipts, weekday_receipts[1:]):
        if _business_days_between(previous_date, current_date) != 1:
            errors.append("weekday receipts must form a consecutive business-day sequence")

    denominator = sum(int(receipt.get("denominator", 0) or 0) for _, receipt in parsed_receipts)
    successes = sum(int(receipt.get("denominator", 0) or 0) for _, receipt in parsed_receipts if receipt.get("unattended_success") and not receipt.get("manual_repair_required"))
    expected_rate = successes / denominator if denominator else 0
    for index, (_, receipt) in enumerate(parsed_receipts):
        rate = receipt.get("cumulative_success_rate")
        if isinstance(rate, (int, float)) and not math.isclose(rate, expected_rate, rel_tol=0, abs_tol=0.000001) and index == len(parsed_receipts) - 1:
            errors.append("ledger cumulative_success_rate does not match receipt denominators")
    target = ledger.get("target", {})
    if not isinstance(target, dict):
        errors.append("target must be an object")
        target = {}
    qualifying_weekdays = [receipt_date for receipt_date, receipt in parsed_receipts if receipt_date.weekday() < 5 and receipt.get("unattended_success") and not receipt.get("manual_repair_required")]
    second_operator = len({receipt.get("operator_identity") for _, receipt in parsed_receipts}) >= 2
    promotion = require_promotion or ledger.get("status") in {"promotion_ready", "ready"}
    if promotion:
        if not started or not parsed_receipts or (parsed_receipts[-1][0] - started).days < 29:
            errors.append("promotion requires a 30-calendar-day observation window")
        if len(qualifying_weekdays) < int(target.get("weekday_changes", 10)):
            errors.append("promotion requires the target consecutive weekday changes")
        if expected_rate < float(target.get("unattended_success_rate", 0.95)):
            errors.append("promotion requires the target unattended success rate")
        if not second_operator:
            errors.append("promotion requires a second operator run")
        if not target.get("failure_taxonomy"):
            errors.append("promotion requires a complete failure taxonomy")
    return errors


def validate_continuation_state(state: dict[str, Any], text: str) -> list[str]:
    errors: list[str] = []
    required = {"status", "active_map_issue", "active_increment_issue", "source_of_truth"}
    errors.extend(f"continuation state missing {field}" for field in sorted(required - state.keys()))
    if state.get("status") not in {"IN_PROGRESS", "BLOCKED", "COMPLETE"}:
        errors.append("continuation state has an invalid status")
    markers = {
        "status": f"Canonical status: `{state.get('status')}`",
        "active_map_issue": f"Canonical active map issue: `#{state.get('active_map_issue')}`",
        "active_increment_issue": f"Canonical active increment issue: `#{state.get('active_increment_issue')}`",
    }
    for field, marker in markers.items():
        if marker not in text:
            label = field.replace("_", " ")
            errors.append(f"continuation text disagrees with canonical {label}")
    return errors


def validate_reconciliation(
    state: dict[str, Any],
    requirements: dict[str, Any],
    queue: dict[str, Any],
    lifecycle_contract: dict[str, Any],
    portfolio_text: str,
) -> list[str]:
    errors: list[str] = []
    if state.get("schema_version") != 1:
        errors.append("integrity state must use schema version 1")
    active_factory = state.get("active_factory")
    if f"active_factory: {active_factory}" not in portfolio_text:
        errors.append("active factory is not present in portfolio state")
    lifecycle_state = state.get("lifecycle", {}).get("state")
    if lifecycle_state not in set(lifecycle_contract.get("states", [])):
        errors.append("lifecycle receipt state is not in the lifecycle contract")
    if lifecycle_state != "ACTIVE":
        errors.append("integrity state must remain ACTIVE until cutover completes")
    requirement_ids = set()
    for item in requirements.get("requirements", []):
        identifier = item.get("id")
        requirement_ids.add(identifier)
        if item.get("status") not in CONTROL_PLANE_STATUSES | {None}:
            errors.append(f"control-plane requirement has invalid status: {identifier}")
    expected_statuses = state.get("control_plane_statuses", {})
    if not isinstance(expected_statuses, dict):
        errors.append("canonical control-plane statuses must be an object")
        expected_statuses = {}
    if set(expected_statuses) != requirement_ids:
        errors.append("canonical control-plane statuses do not match requirements")
    for identifier, status in expected_statuses.items():
        actual = next((item.get("status") for item in requirements.get("requirements", []) if item.get("id") == identifier), None)
        if actual != status:
            errors.append(f"control-plane status drift: {identifier}")
    action_ids = {item.get("id") for item in queue.get("actions", [])}
    for action_id in state.get("required_human_actions", []):
        if action_id not in action_ids:
            errors.append(f"required human action is absent from queue: {action_id}")
    gates = state.get("gates", {})
    if not isinstance(gates, dict):
        errors.append("gate status must be an object")
        gates = {}
    for issue, status in gates.items():
        if status not in GATE_STATUSES:
            errors.append(f"gate {issue} has invalid status")
    active_issue = str(state.get("continuation", {}).get("active_increment_issue", ""))
    if gates.get(active_issue) != "OPEN":
        errors.append("active increment gate must remain OPEN until its closeout is verified")
    return errors
