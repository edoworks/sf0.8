import unittest
import pathlib
import importlib.util

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "check-apple-device.py"
SPEC = importlib.util.spec_from_file_location("check_apple_device", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
parse_devices = MODULE.parse_devices


class AppleDeviceCheckTests(unittest.TestCase):
    def test_parses_coredevice_available_and_unavailable_rows(self):
        output = """
Ethan                Ethan.coredevice.local              39C04F90-1CAA-5533-8FFD-BFB33A373880   available (paired)   iPhone 16 Pro Max (iPhone17,2)
Karen's iPad         Karens-iPad.coredevice.local         7FDD805A-15DD-5885-97BC-7E08AAD1C372   unavailable          iPad Air (4th generation) (iPad13,1)
"""
        devices = parse_devices(output)
        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0]["name"], "Ethan")
        self.assertEqual(devices[0]["state"], "available (paired)")
        self.assertEqual(devices[1]["state"], "unavailable")


if __name__ == "__main__":
    unittest.main()
