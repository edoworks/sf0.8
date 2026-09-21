#!/usr/bin/env python3
"""Check physical Apple-device availability through CoreDevice, not xctrace."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys


DEVICE_LINE = re.compile(
    r"^(?P<name>.+?)\s+(?P<hostname>\S+)\s+(?P<identifier>[0-9A-F-]+)\s+"
    r"(?P<state>available \(paired\)|unavailable)\s+(?P<model>.+)$"
)


def parse_devices(output: str) -> list[dict[str, str]]:
    devices = []
    for line in output.splitlines():
        match = DEVICE_LINE.match(line.strip())
        if match:
            devices.append(match.groupdict())
    return devices


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", help="device name or UDID to require")
    args = parser.parse_args()

    result = subprocess.run(
        ["xcrun", "devicectl", "list", "devices"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        print(result.stderr.strip() or "devicectl failed", file=sys.stderr)
        return 2

    devices = parse_devices(result.stdout)
    if args.device:
        devices = [
            device
            for device in devices
            if args.device in (device["name"], device["identifier"])
        ]

    print(json.dumps(devices, indent=2, sort_keys=True))
    if not devices:
        return 1
    return 0 if any(device["state"] == "available (paired)" for device in devices) else 1


if __name__ == "__main__":
    raise SystemExit(main())
