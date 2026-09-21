#!/usr/bin/env python3
"""Dogfood the pinned public ReuseFirst contract for factory/product workflows."""

from __future__ import annotations

import ast
import json
import sys
from urllib.request import urlopen


REVISION = "30e588b4dc0d869da9b58a01d91c22d6f4931361"
SOURCE_URL = (
    "https://raw.githubusercontent.com/edoworks/artifacts/"
    f"{REVISION}/artifacts/reusefirst/reuse_gate.py"
)


def load_public_contract() -> dict[str, object]:
    with urlopen(SOURCE_URL, timeout=20) as response:
        source = response.read().decode("utf-8")
    tree = ast.parse(source)
    imports = {
        alias.name
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    if imports != {"math"} or functions != {"required_search", "decide"}:
        raise RuntimeError("public contract shape changed; review before execution")
    namespace: dict[str, object] = {}
    exec(compile(tree, SOURCE_URL, "exec"), namespace)
    return namespace


def main() -> int:
    products = sys.argv[1:] or ["factory", "product-a", "vorynce", "intent-compiler-modeled"]
    namespace = load_public_contract()
    required_search = namespace["required_search"]
    decide = namespace["decide"]
    cases = []
    for product in products:
        cases.append(
            {
                "consumer": product,
                "change_units": 8,
                "searched": 1,
                "compatible": 1,
                "decision": decide(8, 1, 1),
                "required_search": required_search(8),
            }
        )
    result = {
        "artifact": "reusefirst",
        "revision": REVISION,
        "source_url": SOURCE_URL,
        "contract": "public reuse_gate.py",
        "status": "VERIFIED",
        "consumers": cases,
        "negative_case": {"decision": decide(8, 0, 0), "expected": "BLOCKED"},
    }
    if any(case["decision"] != "REUSE" for case in cases) or result["negative_case"]["decision"] != "BLOCKED":
        result["status"] = "FAILED"
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
