import unittest
from slo_labs.error_budget_calculator import calculate_error_budget


class TestSLOMath(unittest.TestCase):
    def test_compliant_error_budget(self):
        # 1,000,000 requests, 500 failures on 99.9% target
        res = calculate_error_budget(
            total_requests=1000000,
            failed_requests=500,
            slo_target=0.999,
            window_days=30
        )
        self.assertEqual(res["slo_status"], "COMPLIANT")
        self.assertEqual(res["allowed_failures"], 1000)
        self.assertEqual(res["actual_failures"], 500)
        self.assertEqual(res["consumed_budget_percent"], 50.0)
        self.assertEqual(res["remaining_budget_percent"], 50.0)
        self.assertEqual(res["burn_rate"], 0.5)

    def test_exhausted_error_budget(self):
        # 1,000,000 requests, 1,500 failures on 99.9% target
        res = calculate_error_budget(
            total_requests=1000000,
            failed_requests=1500,
            slo_target=0.999,
            window_days=30
        )
        self.assertEqual(res["slo_status"], "BREACHED")
        self.assertEqual(res["consumed_budget_percent"], 150.0)
        self.assertEqual(res["remaining_budget_percent"], 0.0)
        self.assertEqual(res["burn_rate"], 1.5)


if __name__ == "__main__":
    unittest.main()
