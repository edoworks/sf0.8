import unittest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from reuse_gate import decide, required_search


class PackageContractTests(unittest.TestCase):
    def test_search_scales_and_new_build_requires_reason(self):
        self.assertEqual(required_search(1), 1)
        self.assertEqual(required_search(17), 3)
        self.assertEqual(decide(9, 2, 0), "BLOCKED")
        self.assertEqual(decide(9, 2, 0, "No compatible artifact"), "BUILD_NEW")


if __name__ == "__main__":
    unittest.main()
