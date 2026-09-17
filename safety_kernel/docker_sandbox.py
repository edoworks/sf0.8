"""Fixed-profile Docker backend for low-consequence local experiments."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import re
import secrets
import signal
import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .kernel import Capability, Request, SafetyKernel


class SandboxDenied(RuntimeError):
    """The sandbox could not be established or was not safely configured."""


@dataclass(frozen=True)
class DockerLimits:
    cpus: str = "1"
    memory: str = "256m"
    pids: int = 64
    timeout_seconds: int = 30
    tmpfs_size: str = "64m"


class DockerSandbox:
    def __init__(
        self, *, image: str, workspace_root: Path, limits: DockerLimits = DockerLimits()
    ):
        if not re.fullmatch(r"[^@\s]+@sha256:[0-9a-f]{64}", image):
            raise SandboxDenied("image must be pinned by digest")
        if not workspace_root.is_absolute():
            raise SandboxDenied("workspace root must be absolute")
        if limits.pids < 1 or limits.timeout_seconds < 1:
            raise SandboxDenied("resource limits must be positive")
        self.image = image
        self.workspace_root = workspace_root.resolve()
        self.limits = limits

    def _workspace(self, workspace: Path) -> Path:
        candidate = workspace.resolve()
        try:
            candidate.relative_to(self.workspace_root)
        except ValueError as error:
            raise SandboxDenied("workspace is outside the approved root") from error
        if not candidate.is_dir() or "," in str(candidate):
            raise SandboxDenied("workspace must be an existing directory without commas")
        return candidate

    def command(self, *, workspace: Path, argv: list[str], name: str = "sandbox") -> list[str]:
        workspace = self._workspace(workspace)
        if not argv:
            raise SandboxDenied("argv must be non-empty")
        return [
            "docker",
            "run",
            "--rm",
            f"--name={name}",
            "--read-only",
            "--network=none",
            "--cap-drop=ALL",
            "--security-opt=no-new-privileges:true",
            "--user=65532:65532",
            f"--cpus={self.limits.cpus}",
            f"--memory={self.limits.memory}",
            f"--pids-limit={self.limits.pids}",
            f"--tmpfs=/tmp:rw,noexec,nosuid,size={self.limits.tmpfs_size}",
            f"--mount=type=bind,src={workspace},dst=/workspace,readonly",
            "--workdir=/workspace",
            self.image,
            *argv,
        ]

    def run(
        self,
        *,
        kernel: "SafetyKernel",
        request: "Request",
        capability: "Capability | None",
        workspace: Path,
        argv: list[str],
    ) -> subprocess.CompletedProcess[str]:
        """Authorize, execute, and record one Docker operation."""
        from .kernel import Decision

        if kernel.authorize(request, capability) != Decision.ALLOW:
            raise SandboxDenied("Docker execution was not authorized")

        name = f"safety-kernel-{secrets.token_hex(8)}"
        command = self.command(workspace=workspace, argv=argv, name=name)
        process: subprocess.Popen[str] | None = None
        try:
            process = subprocess.Popen(
                command,
                start_new_session=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, stderr = process.communicate(timeout=self.limits.timeout_seconds)
            result = subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
            if result.returncode != 0:
                raise SandboxDenied("Docker rejected or failed the sandbox")
            kernel.record_effect(request, effect="container_completed", result="success")
            return result
        except subprocess.TimeoutExpired as error:
            if process is not None and process.poll() is None:
                os.killpg(process.pid, signal.SIGKILL)
                process.communicate()
            subprocess.run(["docker", "rm", "-f", name], check=False, capture_output=True)
            raise SandboxDenied("Docker sandbox timed out and was terminated") from error
        except (FileNotFoundError, OSError) as error:
            raise SandboxDenied("Docker sandbox unavailable") from error
