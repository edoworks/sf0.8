#!/usr/bin/env python3
"""Inspect an Xcode archive without changing Apple or project state."""

from __future__ import annotations

import argparse
import hashlib
import json
import plistlib
import subprocess
from pathlib import Path
from typing import Any


def plist(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return plistlib.load(handle)


def command(*args: str) -> str:
    return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT).strip()


def inspect_archive(path: Path) -> dict[str, Any]:
    app = path / "Products/Applications"
    apps = sorted(app.glob("*.app"))
    if len(apps) != 1:
        raise ValueError(f"expected exactly one application, found {len(apps)}")
    bundle = apps[0]
    info = plist(bundle / "Info.plist")
    archive = plist(path / "Info.plist")
    entitlements = command("codesign", "-d", "--entitlements", ":-", str(bundle))
    executable = bundle / info["CFBundleExecutable"]
    return {
        "archive": str(path),
        "archive_sha256": hashlib.sha256((path / "Info.plist").read_bytes()).hexdigest(),
        "application": str(bundle),
        "bundle_identifier": info.get("CFBundleIdentifier"),
        "display_name": info.get("CFBundleDisplayName"),
        "marketing_version": info.get("CFBundleShortVersionString"),
        "build_version": info.get("CFBundleVersion"),
        "platform": info.get("DTPlatformName"),
        "deployment_target": info.get("MinimumOSVersion"),
        "sdk": info.get("DTSDKName"),
        "xcode": info.get("DTXcode"),
        "xcode_build": info.get("DTXcodeBuild"),
        "architectures": command("lipo", "-archs", str(executable)).split(),
        "device_families": info.get("UIDeviceFamily", []),
        "signing": command("codesign", "-d", "--verbose=4", str(bundle)),
        "entitlements": entitlements,
        "development_artifact": "<key>get-task-allow</key><true/>" in entitlements,
        "privacy_manifest": (bundle / "PrivacyInfo.xcprivacy").is_file(),
        "permission_purpose_strings": {
            key: value for key, value in info.items() if key.endswith("UsageDescription")
        },
        "archive_metadata": {
            "creation_date": archive.get("CreationDate"),
            "scheme": archive.get("SchemeName"),
            "team": archive.get("ApplicationProperties", {}).get("Team"),
            "archive_identity": archive.get("ApplicationProperties", {}).get("SigningIdentity"),
        },
        "unexpected_development_files": sorted(
            str(item.relative_to(bundle))
            for item in bundle.rglob("*")
            if item.is_file() and (".debug" in item.name or item.suffix in {".dSYM", ".xcresult"})
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = inspect_archive(args.archive)
    text = json.dumps(result, indent=2, sort_keys=True, default=str) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if not result["development_artifact"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
