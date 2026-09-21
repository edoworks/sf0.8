#!/usr/bin/env python3
"""Notify only from an objective receipt, never from agent-run completion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from objective_notification import notification_result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    result, evaluation = notification_result(json.loads(args.record.read_text(encoding="utf-8")))
    print(json.dumps({"notification_result": result, "objective": evaluation}, indent=2, sort_keys=True))
    completed = subprocess.run(
        ["node", "/Users/hello/.config/opencode/scripts/notify-completion.mjs", "--result", result],
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
