import copy
from datetime import datetime, timedelta, timezone
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_repository_inventory", ROOT / "scripts/validate-repository-inventory.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class RepositoryInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads((ROOT / ".factory/repository-inventory.json").read_text())
        cls.manifest = json.loads((ROOT / ".factory/obligation-disposition-manifest.json").read_text())
        cls.portfolio = (ROOT / ".factory/portfolio.yaml").read_text()

    def test_canonical_inventory_is_consistent(self):
        self.assertEqual([], MODULE.validate(self.inventory, self.manifest, self.portfolio))

    def test_wrong_predecessor_owner_is_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["repositories"]["edoworks/sf0.7"] = manifest["repositories"].pop("foculoom/sf0.7")
        errors = MODULE.validate(self.inventory, manifest, self.portfolio)
        self.assertTrue(any("canonical Foculoom" in error for error in errors))

    def test_inaccessible_private_scope_cannot_be_complete(self):
        inventory = copy.deepcopy(self.inventory)
        inventory["private_inventory"]["complete"] = True
        errors = MODULE.validate(inventory, self.manifest, self.portfolio)
        self.assertTrue(any("private inventory" in error for error in errors))

    def test_public_count_drift_is_rejected(self):
        inventory = copy.deepcopy(self.inventory)
        inventory["public_inventory"]["repositories"].pop()
        errors = MODULE.validate(inventory, self.manifest, self.portfolio)
        self.assertTrue(any("count" in error for error in errors))

    def test_blocked_predecessor_cannot_claim_zero_issues(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["repositories"]["foculoom/sf0.5"]["open_issue_count"] = 0
        errors = MODULE.validate(self.inventory, manifest, self.portfolio)
        self.assertTrue(any("numeric issue count" in error for error in errors))

    def test_stale_snapshot_is_rejected(self):
        captured = datetime.fromisoformat(self.inventory["captured_at"].replace("Z", "+00:00"))
        errors = MODULE.validate(
            self.inventory,
            self.manifest,
            self.portfolio,
            now=captured + timedelta(hours=self.inventory["max_age_hours"] + 1),
        )
        self.assertTrue(any("stale" in error for error in errors))

    def test_future_snapshot_is_rejected(self):
        inventory = copy.deepcopy(self.inventory)
        now = datetime.now(timezone.utc)
        inventory["captured_at"] = (now + timedelta(hours=1)).isoformat()
        errors = MODULE.validate(inventory, self.manifest, self.portfolio, now=now)
        self.assertTrue(any("future-dated" in error for error in errors))

    def test_obligation_summary_drift_is_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["summary"]["migrated"] -= 1
        errors = MODULE.validate(self.inventory, manifest, self.portfolio)
        self.assertTrue(any("summary count" in error for error in errors))

    def test_zero_count_summary_drift_is_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["summary"]["rejected"] = 1
        errors = MODULE.validate(self.inventory, manifest, self.portfolio)
        self.assertTrue(any("summary count" in error for error in errors))

    def test_record_count_is_distinct_from_open_issue_count(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["repositories"]["edoworks/factory"]["open_issue_count"] = 12
        self.assertEqual([], MODULE.validate(self.inventory, manifest, self.portfolio))
        manifest["repositories"]["edoworks/factory"]["inventory_record_count"] = 12
        errors = MODULE.validate(self.inventory, manifest, self.portfolio)
        self.assertTrue(any("inventory record count" in error for error in errors))

    def test_predecessor_open_count_matches_open_records(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["repositories"]["edoworks/sf0.8"]["open_issue_count"] = 22
        errors = MODULE.validate(self.inventory, manifest, self.portfolio)
        self.assertTrue(any("predecessor open issue count" in error for error in errors))

    def test_private_repository_requires_lifecycle_and_disposition(self):
        portfolio = self.portfolio.replace("    lifecycle: dormant\n    disposition: simplify", "    disposition: simplify", 1)
        errors = MODULE.validate(self.inventory, self.manifest, portfolio)
        self.assertTrue(any("exactly one lifecycle" in error for error in errors))

    def test_conflicting_public_lifecycle_is_rejected(self):
        portfolio = self.portfolio.replace(
            "  - id: edoworks/nownest\n    type:",
            "  - id: edoworks/nownest\n    lifecycle: archived\n    type:",
            1,
        )
        errors = MODULE.validate(self.inventory, self.manifest, portfolio)
        self.assertTrue(any("exactly one lifecycle" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
