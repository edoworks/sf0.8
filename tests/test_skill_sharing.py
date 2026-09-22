import json
import tempfile
import unittest
from pathlib import Path

from scripts.skill_sharing import recommendations, validate_inventory, validate_subject_anchoring


ROOT = Path(__file__).parents[1]


class SkillSharingTests(unittest.TestCase):
    def test_canonical_inventory_covers_declared_skill_roots(self):
        inventory = json.loads((ROOT / ".factory/artifacts/skill-sharing-inventory.json").read_text())
        self.assertEqual(validate_inventory(inventory, ROOT), [])
        self.assertEqual({item["id"] for item in recommendations(inventory)}, {"bounded-work", "curiosity-audit", "evidence-research", "focusreset", "prose-editing", "macos-screenshot", "neuroinclusive-ux", "product-art-direction"})

    def test_new_skill_cannot_be_silent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_root = root / ".agents/skills/newskill"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text("---\nname: newskill\n---\n", encoding="utf-8")
            inventory = {"roots": [{"id": "project", "path": ".agents/skills"}], "records": []}
            errors = validate_inventory(inventory, root)
            self.assertIn("missing inventory record: project/newskill", errors)

    def test_recommendation_does_not_approve_publication(self):
        inventory = {"roots": [], "records": [{"id": "x", "root": "x", "used": True, "recommendation": "SHAREABILITY_REVIEW", "evidence": ["x"], "publication_approved": True}]}
        self.assertIn("records[0]: publication must remain human-gated", validate_inventory(inventory, ROOT))

    def test_missing_optional_root_does_not_block_other_roots(self):
        inventory = {
            "roots": [
                {"id": "project", "path": ".agents/skills", "required": True},
                {"id": "optional", "path": ".missing-skills", "required": False},
            ],
            "records": [],
        }
        self.assertNotIn("required skill root is unavailable: project", validate_inventory(inventory, ROOT))

    def test_missing_required_root_blocks_validation(self):
        inventory = {"roots": [{"id": "required", "path": ".missing-skills", "required": True}], "records": []}
        self.assertIn("required skill root is unavailable: required", validate_inventory(inventory, ROOT))

    def test_advisory_skills_must_anchor_subject(self):
        inventory = json.loads((ROOT / ".factory/artifacts/skill-sharing-inventory.json").read_text())
        self.assertEqual(validate_subject_anchoring(inventory, ROOT), [])

    def test_advisory_skill_without_subject_lock_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_root = root / ".agents/skills/driftskill"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                "---\nname: driftskill\n---\n\n# Drift Skill\n\n## Output contract\n\nReturn findings.\n",
                encoding="utf-8",
            )
            inventory = {"roots": [{"id": "project", "path": ".agents/skills"}], "records": []}
            errors = validate_subject_anchoring(inventory, root)
            self.assertIn("project/driftskill: advisory skill must declare an immutable subject lock", errors)
            self.assertIn("project/driftskill: advisory skill must declare a closing subject-consistency check", errors)


if __name__ == "__main__":
    unittest.main()
