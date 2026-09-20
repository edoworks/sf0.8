#!/usr/bin/env python3
"""Validate changed-path ledgers across the complete GitHub event range."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Callable

from ecosystem_gates import validate_changed_records


ROOT = Path(__file__).resolve().parents[1]
SHA = re.compile(r"[0-9a-fA-F]{40}(?:[0-9a-fA-F]{24})?\Z")


def event_range(*, event_name: str, before: str, base: str, head: str) -> str:
    """Return a complete Git range or reject incomplete event metadata."""
    if event_name == "pull_request":
        start, separator = base, "..."
    elif event_name == "push":
        start, separator = before, ".."
    else:
        raise ValueError(f"unsupported GitHub event: {event_name or '<empty>'}")
    if not SHA.fullmatch(start) or not SHA.fullmatch(head):
        raise ValueError("event range requires full Git object IDs")
    if set(start) == {"0"}:
        raise ValueError("event range start cannot be the null object ID")
    return f"{start}{separator}{head}"


def changed_paths(
    revision_range: str,
    *,
    root: Path = ROOT,
    runner: Callable[..., subprocess.CompletedProcess[bytes]] = subprocess.run,
) -> list[str]:
    """Read exact changed paths without shell expansion or newline ambiguity."""
    result = runner(
        ["git", "diff", "--name-only", "-z", revision_range],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git diff failed: {detail or 'unknown error'}")
    return [item.decode("utf-8", errors="surrogateescape") for item in result.stdout.split(b"\0") if item]


def validate_event_change(
    *,
    event_name: str,
    before: str,
    base: str,
    head: str,
    root: Path = ROOT,
    runner: Callable[..., subprocess.CompletedProcess[bytes]] = subprocess.run,
) -> dict:
    revision_range = event_range(event_name=event_name, before=before, base=base, head=head)
    paths = changed_paths(revision_range, root=root, runner=runner)
    ledger_paths = [
        root / path
        for path in paths
        if path.startswith(".factory/artifacts/ledger/issue-") and path.endswith(".json")
    ]
    bindings = json.loads((root / ".factory/control-plane-bindings.json").read_text(encoding="utf-8"))
    bound_issues = {
        binding.get("number")
        for binding in bindings.get("by_capability", {}).values()
        if isinstance(binding, dict)
    }
    records = [
        record
        for path in ledger_paths
        if path.is_file()
        for record in [json.loads(path.read_text(encoding="utf-8"))]
        if record.get("issue") in bound_issues
    ]
    result = validate_changed_records(paths, records, bindings)
    result["event"] = event_name
    result["revision_range"] = revision_range
    result["changed_path_count"] = len(paths)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event-name", required=True)
    parser.add_argument("--before", default="")
    parser.add_argument("--base", default="")
    parser.add_argument("--head", required=True)
    args = parser.parse_args()
    try:
        result = validate_event_change(
            event_name=args.event_name,
            before=args.before,
            base=args.base,
            head=args.head,
        )
    except (ValueError, RuntimeError, OSError, json.JSONDecodeError) as error:
        result = {"decision": "BLOCKED", "errors": [str(error)]}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["decision"] != "BLOCKED" else 1


if __name__ == "__main__":
    sys.exit(main())
