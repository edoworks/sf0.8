#!/usr/bin/env python3
"""Search the canonical registry before a new implementation is started."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ecosystem_gates import discover_registry

ROOT = Path(__file__).resolve().parents[1]

EXTERNAL_SOURCES = {
    "skill": [
        {"source": "GitHub agent skills", "discovery": "gh skill search <capability>", "intake": "gh skill preview OWNER/REPO SKILL"},
        {"source": "Awesome Copilot", "discovery": "https://awesome-copilot.github.com/llms.txt", "intake": "inspect the exact source tree"},
        {"source": "skills.sh", "discovery": "https://skills.sh", "intake": "inspect the underlying source repository"},
    ],
    "mcp": [
        {"source": "Official MCP Registry", "discovery": "https://registry.modelcontextprotocol.io", "intake": "inspect server.json and the underlying package/source"},
        {"source": "GitHub MCP Registry", "discovery": "https://github.com/mcp", "intake": "inspect permissions, endpoints, package, and source"},
    ],
    "library": [
        {"source": "Platform documentation", "discovery": "search the first-party platform API", "intake": "prefer native capability when it meets the need"},
        {"source": "Package registry", "discovery": "search the language ecosystem registry", "intake": "inspect source, immutable version, dependencies, license, and advisories"},
    ],
    "github-integration": [
        {"source": "GitHub Marketplace", "discovery": "https://github.com/marketplace", "intake": "inspect app permissions, data flows, vendor terms, and source where available"},
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("capability")
    parser.add_argument("--artifact-type", choices=sorted(EXTERNAL_SOURCES))
    args = parser.parse_args()
    needle = args.capability.lower()
    registry = json.loads((ROOT / ".factory" / "artifacts" / "reuse-registry.json").read_text())
    matches = discover_registry(registry, needle)
    print(json.dumps({"search_order": registry["search_order"], "matches": matches, "external_sources": EXTERNAL_SOURCES.get(args.artifact_type, [])}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
