#!/usr/bin/env python3
"""Validate and optionally apply one local primitive-learning record."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from primitive_discovery import (
    apply_learning,
    apply_learning_to_opportunities,
    validate_inventory,
    validate_learning_record,
)
from tool_opportunities import validate_ledger


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--inventory", type=Path, default=ROOT / ".factory/capability-primitive-inventory.json")
    parser.add_argument("--ledger", type=Path, default=ROOT / ".factory/tool-opportunity-ledger.json")
    parser.add_argument("--inventory-output", type=Path)
    parser.add_argument("--ledger-output", type=Path)
    args = parser.parse_args()
    result = json.loads(args.result.read_text(encoding="utf-8"))
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    errors = validate_learning_record(result)
    errors.extend(validate_inventory(inventory))
    errors.extend(validate_ledger(ledger))
    if not errors:
        try:
            updated_inventory = apply_learning(inventory, result)
            updated_ledger = apply_learning_to_opportunities(ledger, result)
        except ValueError as error:
            errors.append(str(error))
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    if bool(args.inventory_output) != bool(args.ledger_output):
        print("ERROR: inventory and ledger output paths must be supplied together")
        return 1
    if args.inventory_output and args.ledger_output:
        args.inventory_output.write_text(json.dumps(updated_inventory, indent=2) + "\n", encoding="utf-8")
        args.ledger_output.write_text(json.dumps(updated_ledger, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.inventory_output} and {args.ledger_output}")
    else:
        print(json.dumps({"inventory": updated_inventory, "ledger": updated_ledger}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
