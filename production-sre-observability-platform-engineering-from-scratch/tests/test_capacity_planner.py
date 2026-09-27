import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "projects", "project-07-capacity-planner")))
from planner import plan_capacity


class TestCapacityPlanner(unittest.TestCase):
    def test_littles_law_and_sizing(self):
        # 1,000 RPS, 50ms latency -> L = 50 in-flight requests
        res = plan_capacity(
            peak_rps=1000,
            avg_latency_ms=50,
            cpu_ms_per_request=10.0,
            memory_mb_per_replica=512,
            db_queries_per_request=2,
            desired_headroom_percent=50.0, # 50% headroom means operating at 50% capacity
            core_cpu_capacity_cores=2.0
        )
        self.assertEqual(res["concurrency_needed"], 50.0)
        self.assertEqual(res["raw_cpu_cores"], 10.0)
        self.assertEqual(res["total_cpu_cores_with_headroom"], 20.0)
        self.assertEqual(res["replicas_needed"], 10)
        self.assertEqual(res["total_db_qps"], 2000)


if __name__ == "__main__":
    unittest.main()
