#!/usr/bin/env python3
"""Resolve a registered repository to its canonical remote and lifecycle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / ".factory" / "portfolio.yaml"


def repo_blocks(text: str) -> list[str]:
    section = text.split("repos:\n", 1)[1].split("\nsurfaces:", 1)[0]
    return [block for block in section.split("  - id: ")[1:]]


def apple_product_blocks(text: str) -> list[str]:
    section = text.split("apple_products:\n", 1)[1]
    return [block for block in section.split("  - id: ")[1:]]


def flat_blocks(text: str, section_name: str) -> list[dict[str, str]]:
    marker = f"{section_name}:\n"
    if marker not in text:
        return []
    blocks: list[dict[str, str]] = []
    for block in text.split(marker, 1)[1].split("\n\n", 1)[0].split("  - id: ")[1:]:
        values: dict[str, str] = {}
        lines = block.splitlines()
        if not lines:
            continue
        values["id"] = lines[0].strip()
        for line in lines[1:]:
            if line.startswith("    ") and ":" in line and not line.startswith("      "):
                key, value = line.strip().split(":", 1)
                values[key] = value.strip().strip('"')
        blocks.append(values)
    return blocks


def enumerate_apple_products(portfolio: str | None = None) -> list[dict[str, str]]:
    text = portfolio if portfolio is not None else PORTFOLIO.read_text(encoding="utf-8")
    products = flat_blocks(text, "apple_products")
    required = ("id", "repository", "source_of_truth", "platform", "lifecycle", "release_state", "bundle_id")
    for product in products:
        missing = [key for key in required if not product.get(key)]
        if missing:
            raise ValueError(f"{product.get('id', '<unknown>')} missing canonical product fields: {', '.join(missing)}")
    if len({product["id"] for product in products}) != len(products):
        raise ValueError("canonical Apple product ids must be unique")
    return products


def enumerate_historical_products(portfolio: str | None = None) -> list[dict[str, str]]:
    text = portfolio if portfolio is not None else PORTFOLIO.read_text(encoding="utf-8")
    products = flat_blocks(text, "historical_products")
    required = ("id", "public_name", "source", "platform", "lifecycle", "release_state", "bundle_id", "origin")
    for product in products:
        missing = [key for key in required if not product.get(key)]
        if missing:
            raise ValueError(f"{product.get('id', '<unknown>')} missing historical product fields: {', '.join(missing)}")
    if len({product["id"] for product in products}) != len(products):
        raise ValueError("historical product ids must be unique")
    return products


def resolve(repo_id: str, portfolio: str | None = None) -> dict[str, str]:
    text = portfolio if portfolio is not None else PORTFOLIO.read_text(encoding="utf-8")
    for block in repo_blocks(text):
        lines = block.splitlines()
        if not lines or lines[0].strip() != repo_id:
            continue
        values: dict[str, str] = {"id": repo_id}
        for line in lines[1:]:
            if line.startswith("    ") and ":" in line and not line.startswith("      "):
                key, value = line.strip().split(":", 1)
                values[key] = value.strip().strip('"')
        required = ("source_of_truth", "default_branch", "lifecycle", "visibility")
        missing = [key for key in required if not values.get(key)]
        if missing:
            raise ValueError(f"{repo_id} missing canonical fields: {', '.join(missing)}")
        return values
    raise ValueError(f"repository is not registered: {repo_id}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_id", nargs="?")
    parser.add_argument("--list-apple", action="store_true")
    parser.add_argument("--list-historical", action="store_true")
    args = parser.parse_args()
    if args.list_apple:
        print(json.dumps(enumerate_apple_products(), indent=2, sort_keys=True))
        return 0
    if args.list_historical:
        print(json.dumps(enumerate_historical_products(), indent=2, sort_keys=True))
        return 0
    if not args.repo_id:
        parser.error("repo_id is required unless --list-apple is used")
    print(json.dumps(resolve(args.repo_id), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
