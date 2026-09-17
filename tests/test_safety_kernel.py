from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import unittest
from unittest.mock import patch
from tempfile import TemporaryDirectory

from safety_kernel import (
    AuditLog,
    Capability,
    Decision,
    DockerSandbox,
    Request,
    ResourceBudget,
    SafetyKernel,
    SandboxDenied,
)


def capability(**overrides):
    values = {
        "principal": "agent-a",
        "operation": "write_file",
        "resource": "/work/task/",
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=5),
        "max_cost": 2,
        "max_runtime_seconds": 10,
        "max_agents": 1,
    }
    values.update(overrides)
    return Capability(**values)


class SafetyKernelTests(unittest.TestCase):
    def setUp(self):
        self.audit = AuditLog()
        self.kernel = SafetyKernel(
            audit=self.audit,
            budget=ResourceBudget(max_cost=5, max_runtime_seconds=30, max_agents=2),
        )

    def request(self, **overrides):
        values = {
            "principal": "agent-a",
            "operation": "write_file",
            "resource": "/work/task/file.txt",
            "estimated_cost": 1,
            "estimated_runtime_seconds": 2,
            "requested_agents": 1,
        }
        values.update(overrides)
        return Request(**values)

    def test_denies_without_capability(self):
        self.assertEqual(self.kernel.authorize(self.request(), None), Decision.DENY)

    def test_allows_scoped_request_and_audits_it(self):
        self.assertEqual(self.kernel.authorize(self.request(), capability()), Decision.ALLOW)
        self.assertTrue(self.audit.verify())
        self.assertEqual(self.audit.records[0]["effect"], "not_executed_by_kernel")

    def test_tampered_audit_chain_is_detected(self):
        self.kernel.authorize(self.request(), capability())
        self.audit.records[0]["decision"] = Decision.ALLOW
        self.audit.records[0]["reason"] = "forged"
        self.assertFalse(self.audit.verify())

    def test_rejects_sibling_resource_prefix(self):
        request = self.request(resource="/work/task-escape/file.txt")
        self.assertEqual(self.kernel.authorize(request, capability()), Decision.DENY)

    def test_human_only_operation_never_allows(self):
        request = self.request(operation="publish", resource="release")
        self.assertEqual(self.kernel.authorize(request, capability(operation="publish", resource="release")), Decision.REQUIRE_HUMAN_AUTHORIZATION)

    def test_unknown_operation_is_denied(self):
        request = self.request(operation="erase_everything")
        self.assertEqual(self.kernel.authorize(request, capability(operation="erase_everything")), Decision.DENY)

    def test_colluding_principal_cannot_use_another_principals_capability(self):
        request = self.request(principal="agent-b")
        self.assertEqual(self.kernel.authorize(request, capability()), Decision.DENY)

    def test_colluding_agents_cannot_change_policy(self):
        request = self.request(principal="agent-b", operation="policy_change", resource="policy")
        self.assertEqual(self.kernel.authorize(request, capability(principal="agent-b", operation="policy_change", resource="policy")), Decision.REQUIRE_HUMAN_AUTHORIZATION)

    def test_rejects_expired_capability(self):
        expired = capability(expires_at=datetime.now(timezone.utc) - timedelta(seconds=1))
        self.assertEqual(self.kernel.authorize(self.request(), expired), Decision.DENY)

    def test_budget_is_hard_ceiling(self):
        self.assertEqual(self.kernel.authorize(self.request(estimated_cost=6), capability(max_cost=6)), Decision.DENY)

    def test_negative_estimates_are_denied(self):
        self.assertEqual(self.kernel.authorize(self.request(estimated_cost=-1), capability()), Decision.DENY)
        self.assertEqual(self.kernel.authorize(self.request(estimated_runtime_seconds=-1), capability()), Decision.DENY)
        self.assertEqual(self.kernel.authorize(self.request(requested_agents=-1), capability()), Decision.DENY)

    def test_non_finite_estimates_are_denied(self):
        self.assertEqual(self.kernel.authorize(self.request(estimated_cost=float("inf")), capability()), Decision.DENY)
        self.assertEqual(self.kernel.authorize(self.request(estimated_cost=float("nan")), capability()), Decision.DENY)

    def test_audit_failure_denies_without_consuming_budget(self):
        self.audit.available = False
        self.assertEqual(self.kernel.authorize(self.request(), capability()), Decision.DENY)
        self.assertEqual(self.kernel.budget.spent_cost, 0)

    def test_delegation_cannot_amplify_authority(self):
        parent = capability()
        child = parent.delegate(
            principal="agent-b",
            resource="/work/task/sub/",
            expires_at=parent.expires_at,
            max_cost=parent.max_cost,
            max_runtime_seconds=parent.max_runtime_seconds,
            max_agents=parent.max_agents,
        )
        self.assertIsNotNone(child)
        amplified = parent.delegate(
            principal="agent-b",
            resource="/work/task/sub/",
            expires_at=parent.expires_at + timedelta(seconds=1),
            max_cost=parent.max_cost + 1,
            max_runtime_seconds=parent.max_runtime_seconds,
            max_agents=parent.max_agents + 1,
        )
        self.assertIsNone(amplified)

    def test_effect_requires_live_authorization_and_cannot_replay(self):
        request = self.request()
        with self.assertRaises(PermissionError):
            self.kernel.record_effect(request, effect="container_completed", result="success")
        self.assertEqual(self.kernel.authorize(request, capability()), Decision.ALLOW)
        self.kernel.record_effect(request, effect="container_completed", result="success")
        with self.assertRaises(PermissionError):
            self.kernel.record_effect(request, effect="container_completed", result="success")


class DockerSandboxTests(unittest.TestCase):
    def setUp(self):
        self.workspace = TemporaryDirectory()
        self.sandbox = DockerSandbox(
            image="python:3.13@sha256:" + "a" * 64,
            workspace_root=Path(self.workspace.name),
        )
        self.audit = AuditLog()
        self.kernel = SafetyKernel(
            audit=self.audit,
            budget=ResourceBudget(max_cost=5, max_runtime_seconds=30, max_agents=2),
        )

    def tearDown(self):
        self.workspace.cleanup()

    def request(self):
        return Request(
            principal="agent-a",
            operation="run_command",
            resource=str(Path(self.workspace.name) / "work"),
            estimated_runtime_seconds=2,
            requested_agents=0,
        )

    def capability(self):
        return Capability(
            principal="agent-a",
            operation="run_command",
            resource=str(Path(self.workspace.name) / "work"),
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
            max_runtime_seconds=10,
            max_agents=0,
        )

    def test_profile_is_restricted(self):
        command = self.sandbox.command(workspace=Path(self.workspace.name), argv=["true"])
        self.assertIn("--network=none", command)
        self.assertIn("--read-only", command)
        self.assertIn("--cap-drop=ALL", command)
        self.assertIn("--security-opt=no-new-privileges:true", command)
        self.assertIn("--user=65532:65532", command)
        self.assertFalse(any("docker.sock" in item for item in command))

    def test_unpinned_image_is_denied(self):
        with self.assertRaises(SandboxDenied):
            DockerSandbox(image="python:latest", workspace_root=Path(self.workspace.name))

    def test_invalid_workspace_and_empty_argv_are_denied(self):
        with self.assertRaises(SandboxDenied):
            self.sandbox.command(workspace=Path("/tmp"), argv=["true"])
        with self.assertRaises(SandboxDenied):
            self.sandbox.command(workspace=Path(self.workspace.name), argv=[])

    def test_symlink_workspace_escape_is_denied(self):
        link = Path(self.workspace.name) / "escape"
        os.symlink("/tmp", link)
        with self.assertRaises(SandboxDenied):
            self.sandbox.command(workspace=link, argv=["true"])

    def test_agent_cannot_add_docker_flags(self):
        command = self.sandbox.command(workspace=Path(self.workspace.name), argv=["--privileged"])
        self.assertNotIn("--privileged", command[: command.index(self.sandbox.image)])

    @patch("safety_kernel.docker_sandbox.subprocess.Popen")
    def test_daemon_or_container_failure_is_denied(self, popen):
        popen.return_value.returncode = 1
        popen.return_value.communicate.return_value = ("", "daemon unavailable")
        with self.assertRaises(SandboxDenied):
            self.sandbox.run(
                kernel=self.kernel,
                request=self.request(),
                capability=self.capability(),
                workspace=Path(self.workspace.name),
                argv=["true"],
            )

    def test_direct_execution_without_kernel_is_impossible(self):
        with self.assertRaises(TypeError):
            self.sandbox.run(workspace=Path(self.workspace.name), argv=["true"])

    @patch("safety_kernel.docker_sandbox.subprocess.Popen")
    def test_authorized_execution_records_completed_effect(self, popen):
        popen.return_value.returncode = 0
        popen.return_value.communicate.return_value = ("sandbox-ok\n", "")
        result = self.sandbox.run(
            kernel=self.kernel,
            request=self.request(),
            capability=self.capability(),
            workspace=Path(self.workspace.name),
            argv=["true"],
        )
        self.assertEqual(result.stdout, "sandbox-ok\n")
        self.assertEqual(self.audit.records[-1]["effect"], "container_completed")

if __name__ == "__main__":
    unittest.main()
