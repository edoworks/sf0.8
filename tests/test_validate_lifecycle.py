import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_lifecycle", ROOT / "scripts" / "validate-lifecycle.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class LifecycleValidationTests(unittest.TestCase):
    def setUp(self):
        self.portfolio = (ROOT / ".factory" / "portfolio.yaml").read_text()

    def test_current_portfolio_fixture_passes_registry_checks(self):
        self.assertEqual(MODULE.portfolio_errors(self.portfolio), [])

    def test_duplicate_active_factory_is_blocked(self):
        fixture = self.portfolio.replace(
            "lifecycle: deprecated\n    disposition: keep_read_only",
            "lifecycle: active\n    disposition: keep_read_only",
            1,
        )
        errors = MODULE.portfolio_errors(fixture)
        self.assertIn("expected exactly one active factory, found 2", errors)

    def test_missing_disposition_is_blocked(self):
        fixture = self.portfolio.replace("    disposition: keep\n", "", 1)
        errors = MODULE.portfolio_errors(fixture)
        self.assertTrue(any("lacks a disposition" in error for error in errors))

    def test_deployed_surface_without_release_evidence_is_blocked(self):
        fixture = self.portfolio.replace(
            "    lifecycle: active\n    disposition: keep\n    source_of_truth:",
            "    lifecycle: deployed\n    disposition: keep\n    source_of_truth:",
            1,
        )
        errors = MODULE.portfolio_errors(fixture)
        self.assertTrue(any("lacks release evidence" in error for error in errors))

    def test_active_product_must_exist_as_active_repo(self):
        fixture = self.portfolio.replace(
            "active_private_product: edoworks/product-a",
            "active_private_product: edoworks/other-product",
        )
        errors = MODULE.portfolio_errors(fixture)
        self.assertTrue(any("active private product" in error for error in errors))

    def test_stale_continuation_is_blocked(self):
        errors = MODULE.continuation_errors(
            [("fixture.md", "sf0.7 is the active factory")]
        )
        self.assertIn("stale sf0.7 authority in fixture.md", errors)

    def test_active_legacy_status_and_queue_are_blocked(self):
        status_errors = MODULE.legacy_state_errors(
            {"state": "deprecated_read_only", "active_increment": "old-task"}, None
        )
        queue_errors = MODULE.legacy_state_errors(
            None,
            {
                "read_only": True,
                "lifecycle": "deprecated_read_only",
                "increments": [{"status": "active"}],
            },
        )
        self.assertIn("sf0.7 has an active increment", status_errors)
        self.assertIn("sf0.7 queue contains active work", queue_errors)


if __name__ == "__main__":
    unittest.main()
