"""Deny-by-default authorization prototype.

This module decides whether an effect may be attempted. It does not execute
shell commands, make network calls, or provide host-level isolation.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
import hashlib
import json
import math
from typing import Any


HUMAN_ONLY = frozenset(
    {
        "secret_read",
        "policy_change",
        "publish",
        "deploy",
        "delete",
        "github_write",
    }
)
KNOWN_OPERATIONS = frozenset(
    {
        "read_file",
        "write_file",
        "run_command",
        "network_request",
        "spawn_agent",
        *HUMAN_ONLY,
    }
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _scope_contains(scope: str, resource: str) -> bool:
    if scope == resource:
        return True
    return scope.endswith("/") and resource.startswith(scope)


def _valid_nonnegative(value: float | int) -> bool:
    return value >= 0 and math.isfinite(value)


@dataclass(frozen=True)
class Capability:
    principal: str
    operation: str
    resource: str
    expires_at: datetime
    max_cost: float = 0.0
    max_runtime_seconds: int = 0
    max_agents: int = 0
    revoked: bool = False

    def delegate(
        self,
        *,
        principal: str,
        resource: str,
        expires_at: datetime,
        max_cost: float,
        max_runtime_seconds: int,
        max_agents: int,
    ) -> "Capability | None":
        if not _scope_contains(self.resource, resource):
            return None
        if expires_at > self.expires_at:
            return None
        if max_cost > self.max_cost:
            return None
        if max_runtime_seconds > self.max_runtime_seconds:
            return None
        if max_agents > self.max_agents:
            return None
        return replace(
            self,
            principal=principal,
            resource=resource,
            expires_at=expires_at,
            max_cost=max_cost,
            max_runtime_seconds=max_runtime_seconds,
            max_agents=max_agents,
        )


@dataclass(frozen=True)
class Request:
    principal: str
    operation: str
    resource: str
    estimated_cost: float = 0.0
    estimated_runtime_seconds: int = 0
    requested_agents: int = 0
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ResourceBudget:
    max_cost: float = 0.0
    max_runtime_seconds: int = 0
    max_agents: int = 0
    spent_cost: float = 0.0
    spent_runtime_seconds: int = 0
    used_agents: int = 0

    def permits(self, request: Request, capability: Capability) -> bool:
        return (
            request.estimated_cost <= capability.max_cost
            and request.estimated_runtime_seconds <= capability.max_runtime_seconds
            and request.requested_agents <= capability.max_agents
            and self.spent_cost + request.estimated_cost <= self.max_cost
            and self.spent_runtime_seconds + request.estimated_runtime_seconds
            <= self.max_runtime_seconds
            and self.used_agents + request.requested_agents <= self.max_agents
        )

    def consume(self, request: Request) -> "ResourceBudget":
        return replace(
            self,
            spent_cost=self.spent_cost + request.estimated_cost,
            spent_runtime_seconds=self.spent_runtime_seconds
            + request.estimated_runtime_seconds,
            used_agents=self.used_agents + request.requested_agents,
        )


class AuditLog:
    """Hash-chained evidence sink; privileged hosts can still rewrite it."""

    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []
        self.available = True

    def append(self, record: dict[str, Any]) -> None:
        if not self.available:
            raise OSError("audit sink unavailable")
        body = json.dumps(record, sort_keys=True, separators=(",", ":"))
        previous = self.records[-1]["hash"] if self.records else "GENESIS"
        record = dict(record, previous_hash=previous)
        record["hash"] = hashlib.sha256(
            (previous + body).encode("utf-8")
        ).hexdigest()
        self.records.append(record)

    def verify(self) -> bool:
        previous = "GENESIS"
        for record in self.records:
            candidate = dict(record)
            actual = candidate.pop("hash")
            candidate.pop("previous_hash")
            body = json.dumps(candidate, sort_keys=True, separators=(",", ":"))
            expected = hashlib.sha256((previous + body).encode("utf-8")).hexdigest()
            if actual != expected or record["previous_hash"] != previous:
                return False
            previous = actual
        return True


class Decision:
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_HUMAN_AUTHORIZATION = "REQUIRE_HUMAN_AUTHORIZATION"


class SafetyKernel:
    """Policy gateway. No method here performs the requested external effect."""

    def __init__(self, *, audit: AuditLog, budget: ResourceBudget) -> None:
        self._audit = audit
        self._budget = budget
        self._authorized_requests: set[str] = set()

    @property
    def budget(self) -> ResourceBudget:
        return self._budget

    def authorize(self, request: Request, capability: Capability | None) -> str:
        decision = Decision.DENY
        reason = "deny_by_default"
        now = _now()
        if not self._audit.available:
            return Decision.DENY
        if not request.principal or not request.operation or not request.resource:
            reason = "malformed_request"
        elif not all(
            (
                _valid_nonnegative(request.estimated_cost),
                _valid_nonnegative(request.estimated_runtime_seconds),
                _valid_nonnegative(request.requested_agents),
            )
        ):
            reason = "malformed_request"
        elif request.operation not in KNOWN_OPERATIONS:
            reason = "unknown_operation"
        elif request.operation in HUMAN_ONLY:
            decision = Decision.REQUIRE_HUMAN_AUTHORIZATION
            reason = "human_only_operation"
        elif capability is None:
            reason = "missing_capability"
        elif capability.revoked:
            reason = "revoked_capability"
        elif capability.principal != request.principal:
            reason = "principal_mismatch"
        elif capability.operation != request.operation:
            reason = "operation_mismatch"
        elif not _scope_contains(capability.resource, request.resource):
            reason = "resource_out_of_scope"
        elif now >= capability.expires_at:
            reason = "expired_capability"
        elif not self._budget.permits(request, capability):
            reason = "resource_ceiling_exceeded"
        else:
            decision = Decision.ALLOW
            reason = "capability_and_budget_valid"

        try:
            self._audit.append(
                {
                    "timestamp": now.isoformat(),
                    "principal": request.principal,
                    "operation": request.operation,
                    "resource": request.resource,
                    "arguments": request.arguments,
                    "capability": repr(capability),
                    "decision": decision,
                    "reason": reason,
                    "effect": "not_executed_by_kernel",
                    "resource_consumption": {
                        "cost": request.estimated_cost,
                        "runtime_seconds": request.estimated_runtime_seconds,
                        "agents": request.requested_agents,
                    },
                },
            )
        except OSError:
            return Decision.DENY
        if decision == Decision.ALLOW:
            self._budget = self._budget.consume(request)
            self._authorized_requests.add(self._request_key(request))
        return decision

    def record_effect(self, request: Request, *, effect: str, result: str) -> None:
        """Record the effect after a previously authorized mediated operation."""
        if not self._audit.available:
            raise OSError("audit sink unavailable")
        key = self._request_key(request)
        if key not in self._authorized_requests:
            raise PermissionError("effect has no live authorization")
        self._audit.append(
            {
                "timestamp": _now().isoformat(),
                "principal": request.principal,
                "operation": request.operation,
                "resource": request.resource,
                "arguments": request.arguments,
                "decision": Decision.ALLOW,
                "effect": effect,
                "result": result,
                "resource_consumption": {
                    "cost": request.estimated_cost,
                    "runtime_seconds": request.estimated_runtime_seconds,
                    "agents": request.requested_agents,
                },
            }
        )
        self._authorized_requests.remove(key)

    @staticmethod
    def _request_key(request: Request) -> str:
        body = json.dumps(
            {
                "principal": request.principal,
                "operation": request.operation,
                "resource": request.resource,
                "estimated_cost": request.estimated_cost,
                "estimated_runtime_seconds": request.estimated_runtime_seconds,
                "requested_agents": request.requested_agents,
                "arguments": request.arguments,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(body.encode("utf-8")).hexdigest()
