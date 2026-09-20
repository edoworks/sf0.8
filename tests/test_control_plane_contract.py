import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]

SPEC = importlib.util.spec_from_file_location(
    "validate_control_plane_contract", ROOT / "scripts" / "validate-control-plane-contract.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ControlPlaneContractTests(unittest.TestCase):
    def test_each_mandatory_control_plane_has_downstream_proof_definition(self):
        record = json.loads((ROOT / ".factory/control-plane-requirements.json").read_text())
        self.assertEqual(MODULE.validate(record), [])
        self.assertGreaterEqual(len(record["requirements"]), 5)

    def test_unproven_control_plane_cannot_claim_proven(self):
        record = {"schema_version": 1, "requirements": [{
            "id": "x", "control_plane": "x", "required_before": "work",
            "human_authority": "human", "proof": "receipt", "status": "PROVEN"
        }]}
        self.assertTrue(any("proof_evidence" in error for error in MODULE.validate(record)))


if __name__ == "__main__":
    unittest.main()
