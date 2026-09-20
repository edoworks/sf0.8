#!/usr/bin/env python3
"""Fail-closed preflight for material work and mandatory GitHub tracking."""

from __future__ import annotations

import subprocess
from urllib.parse import urlparse
from typing import Any, Callable


OWNER = "hellofoculoom"


def _valid_issue_binding(issue: dict[str, Any], repo: str, expected: dict[str, Any] | None) -> bool:
    """Validate the factory binding before attempting any GitHub write."""
    if issue.get("repo") != repo or issue.get("canonical") is not True:
        return False
    if expected and (issue.get("number") != expected.get("number") or issue.get("url") != expected.get("url")):
        return False
    parsed = urlparse(str(issue.get("url", "")))
    return (
        parsed.scheme == "https"
        and parsed.netloc == "github.com"
        and parsed.path == f"/{repo}/issues/{issue.get('number')}"
    )


def is_material_work(task: dict[str, Any]) -> bool:
    """Classify work before any reuse or implementation decision is accepted."""
    return bool(task.get("material", task.get("change_units", 0) > 0))


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def capability_preflight(
    task: dict[str, Any],
    *,
    repo: str,
    issue: dict[str, Any] | None,
    expected_issue: dict[str, Any] | None = None,
    runner: Callable[[list[str]], subprocess.CompletedProcess[str]] = _run,
) -> dict[str, Any]:
    """Prove identity, write capability, and issue binding in that order.

    The write probe is an idempotent comment on the canonical issue. Creation or
    reuse must already have produced the issue binding supplied to this gate.
    """
    if not is_material_work(task):
        return {"decision": "NOT_REQUIRED", "stage": "classification", "errors": []}

    errors: list[str] = []
    if not repo.strip():
        errors.append("material work requires a repository binding")
        return {"decision": "BLOCKED", "stage": "request", "errors": errors}

    if not issue or not isinstance(issue.get("number"), int) or issue["number"] < 1 or issue.get("created_or_reused") is not True:
        errors.append("canonical issue must be created or reused before material work")
        return {"decision": "BLOCKED", "stage": "issue_requirement", "errors": errors}

    if not _valid_issue_binding(issue, repo, expected_issue):
        errors.append("issue binding is not the trusted canonical issue for this work")
        return {"decision": "BLOCKED", "stage": "binding", "errors": errors}

    identity = runner(["gh", "api", "user", "--jq", ".login"])
    if identity.returncode != 0 or identity.stdout.strip() != OWNER:
        errors.append("GitHub owner identity was not proven")
        return {"decision": "BLOCKED", "stage": "identity", "errors": errors}

    issue_number = str(issue["number"])
    write_probe = str(issue.get("write_probe", "")).strip()
    if not write_probe:
        errors.append("write capability proof requires an idempotent issue probe")
        return {"decision": "BLOCKED", "stage": "write_capability", "errors": errors}
    probe = runner(["gh", "issue", "comment", "--repo", repo, issue_number, "--body", write_probe])
    if probe.returncode != 0:
        errors.append("mandatory GitHub issue write capability was not proven")
        return {"decision": "BLOCKED", "stage": "write_capability", "errors": errors}

    return {
        "decision": "PASS",
        "stage": "bound",
        "errors": [],
        "binding": {"repo": repo, "issue_number": issue["number"], "url": issue["url"]},
    }
