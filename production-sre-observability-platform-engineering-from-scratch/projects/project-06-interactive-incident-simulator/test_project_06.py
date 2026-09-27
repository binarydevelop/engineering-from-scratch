import unittest
from simulator import IncidentSimulator

class TestProject06(unittest.TestCase):
    def test_simulator_injection(self):
        sim = IncidentSimulator()
        sim.inject_failure("latency_spike", "database", 30)
        tl = sim.generate_timeline()
        self.assertEqual(len(tl), 1)
        self.assertEqual(tl[0]["failure_type"], "latency_spike")

if __name__ == "__main__":
    unittest.main()
