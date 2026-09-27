import unittest
from golden_path import GoldenPath

class TestProject12(unittest.TestCase):
    def test_golden_path_execution(self):
        res = GoldenPath.execute_golden_path("payment-gateway", "billing-team")
        self.assertEqual(res["status"], "READY_FOR_DEPLOYMENT")
        self.assertTrue(res["telemetry_verified"])

if __name__ == "__main__":
    unittest.main()
