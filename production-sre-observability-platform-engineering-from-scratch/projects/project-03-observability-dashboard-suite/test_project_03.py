import unittest
from dashboard_builder import DashboardBuilder

class TestProject03(unittest.TestCase):
    def test_red_dashboard_generation(self):
        dash = DashboardBuilder.build_red_dashboard("payment-service")
        self.assertEqual(len(dash["panels"]), 3)
        self.assertIn("payment-service", dash["panels"][0]["query"])

if __name__ == "__main__":
    unittest.main()
