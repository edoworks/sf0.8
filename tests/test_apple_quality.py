import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("apple_quality", ROOT / "scripts" / "apple-quality.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class AppleQualityTests(unittest.TestCase):
    def test_complete_review_passes(self):
        record = json.loads((ROOT / ".factory/artifacts/ledger/apple-platform-review.json").read_text())
        self.assertEqual(MODULE.validate(record), [])

    def test_empty_intent_is_blocked(self):
        self.assertTrue(MODULE.validate_intent({}))

    def test_deployment_block_requires_fallback(self):
        errors = MODULE.validate_capabilities({"capabilities": [{
            "name": "Example", "source": "Apple", "maturity": "STABLE",
            "deployment_target": "iOS 26", "disposition": "BLOCKED_BY_DEPLOYMENT_TARGET",
            "reason": "not available",
        }]})
        self.assertIn("capabilities[0] needs fallback when deployment-target blocked", errors)

    def test_evidence_must_name_verification_boundary(self):
        errors = MODULE.validate_evidence({"rendered": True})
        self.assertIn("verification must distinguish simulator, device, or empirical evidence", errors)


if __name__ == "__main__":
    unittest.main()
