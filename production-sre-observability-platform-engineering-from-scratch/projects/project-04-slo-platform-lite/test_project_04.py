import unittest
from slo_engine import SLOEngine

class TestProject04(unittest.TestCase):
    def test_slo_burn_rate_and_page_decision(self):
        engine = SLOEngine(target_slo=0.999) # Budget = 0.001
        # Current error rate 2% = 0.02 -> burn rate = 20
        burn = engine.calculate_burn_rate(0.02)
        self.assertAlmostEqual(burn, 20.0, places=5)
        eval_result = engine.evaluate_alert(burn_rate_1h=20.0, burn_rate_6h=8.0)
        self.assertTrue(eval_result["should_page"])

if __name__ == "__main__":
    unittest.main()
