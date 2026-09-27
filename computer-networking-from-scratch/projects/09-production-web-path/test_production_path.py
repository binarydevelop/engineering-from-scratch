#!/usr/bin/env python3
"""
projects/09-production-web-path/test_production_path.py
Automated test suite verifying the end-to-end multi-tier web path and failure modes.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from production_topology import ProductionWebPath


class TestProductionWebPath(unittest.TestCase):
    def setUp(self):
        self.path = ProductionWebPath()

    def test_happy_path_trace(self):
        code, body, trace = self.path.execute_request_trace("http://api.company.internal/items/item:1")
        self.assertEqual(code, 200)
        self.assertIn("Widget A", body)
        self.assertEqual(len(trace), 4)
        self.assertEqual(trace[0].layer, "L7-DNS")
        self.assertEqual(trace[1].layer, "L4-TCP")
        self.assertEqual(trace[2].layer, "L7-LB")
        self.assertEqual(trace[3].layer, "L7-APP")

    def test_dns_failure_nxdomain(self):
        code, body, trace = self.path.execute_request_trace("http://unknown.invalid/items/item:1")
        self.assertEqual(code, 0)
        self.assertIn("NXDOMAIN", body)
        self.assertEqual(trace[0].status, "FAILED")

    def test_worker_crash_failover(self):
        # Kill App A
        self.path.app_a.is_alive = False
        code, body, trace = self.path.execute_request_trace("http://api.company.internal/items/item:1")
        self.assertEqual(code, 200)
        self.assertIn("app-worker-2", body)  # Routed to surviving worker B

    def test_db_timeout_returns_504(self):
        self.path.db.is_healthy = False
        code, body, trace = self.path.execute_request_trace("http://api.company.internal/items/item:1")
        self.assertEqual(code, 504)
        self.assertEqual(body, "Gateway Timeout")


if __name__ == "__main__":
    unittest.main()
