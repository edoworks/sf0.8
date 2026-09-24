import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MetadataReconciliationTests(unittest.TestCase):
    def test_reusefirst_correction_supersedes_false_immutable_claim(self):
        original_path = (
            ROOT
            / ".factory/artifacts/evidence/reusefirst-public-surface-preflight-2026-09-20.json"
        )
        correction_path = (
            ROOT
            / ".factory/artifacts/evidence/reusefirst-public-surface-preflight-correction-2026-09-24.json"
        )
        original = json.loads(original_path.read_text())
        correction = json.loads(correction_path.read_text())
        registry = json.loads((ROOT / ".factory/evidence-supersessions.json").read_text())

        self.assertIn("immutable release", original["interpretation"])
        self.assertEqual(
            correction["supersedes"],
            ".factory/artifacts/evidence/reusefirst-public-surface-preflight-2026-09-20.json",
        )
        self.assertFalse(correction["release"]["immutable"])
        self.assertEqual(correction["release"]["asset_count"], 0)
        self.assertEqual(correction["release"]["asset_names"], [])
        self.assertEqual(correction["status"], "SUPERSEDES_WITH_BLOCKERS")
        self.assertEqual(
            registry["supersessions"],
            [
                {
                    "original": str(original_path.relative_to(ROOT)),
                    "correction": str(correction_path.relative_to(ROOT)),
                }
            ],
        )

    def test_prd_does_not_claim_current_releases_are_immutable(self):
        prd = (ROOT / "docs/PRD-edoworks-factory.md").read_text()

        self.assertNotIn("downloaded as an immutable release", prd)
        self.assertNotIn("Every factory correction is a new immutable version", prd)
        self.assertRegex(prd, r"generated source\s+archive for an exact release tag")
        self.assertIn("attached asset inventory", prd)

    def test_retired_rung_domain_has_active_replacement(self):
        portfolio = (ROOT / ".factory/portfolio.yaml").read_text()
        domain_block = portfolio.split("  - id: rung.edoworks.com", 1)[1].split(
            "  - id: edoworks/rung", 1
        )[0]

        self.assertIn("lifecycle: retired", domain_block)
        self.assertIn("disposition: keep_read_only", domain_block)
        self.assertIn("https://edoworks.com/rung/", domain_block)

    def test_metadata_target_preserves_explicit_license_policies(self):
        target = json.loads((ROOT / ".factory/repository-metadata-target.json").read_text())
        repositories = {item["repo"]: item for item in target["repositories"]}

        self.assertEqual(
            repositories["edoworks/artifacts"]["license_policy"],
            "mixed-per-artifact",
        )
        self.assertTrue(repositories["edoworks/artifacts"]["allow_missing_license"])
        self.assertEqual(
            repositories["edoworks/nownest"]["license_policy"],
            "owner-decision-pending",
        )
        self.assertTrue(repositories["edoworks/nownest"]["allow_missing_license"])


if __name__ == "__main__":
    unittest.main()
