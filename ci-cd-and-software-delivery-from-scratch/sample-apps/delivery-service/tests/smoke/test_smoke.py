#!/usr/bin/env python3
"""
Post-Deployment Smoke Tests (Phase 95)
Verifies that a newly deployed application instance responds to liveness and readiness
probes, exposes expected version metadata, and accepts sample traffic.
"""

import json
import os
import sys
import threading
import time
import unittest
import urllib.request
import urllib.error

# Import server components for local in-process testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app import DeliveryServiceHandler, init_database
from http.server import HTTPServer


class TestSmokeDeployment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Allow testing against external live URL or spawn local test server
        cls.target_url = os.environ.get("TARGET_URL")
        cls.server = None

        if not cls.target_url:
            init_database()
            cls.server = HTTPServer(("127.0.0.1", 0), DeliveryServiceHandler)
            cls.port = cls.server.server_port
            cls.target_url = f"http://127.0.0.1:{cls.port}"
            cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
            cls.server_thread.start()
            time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        if cls.server:
            cls.server.shutdown()
            cls.server.server_close()

    def test_liveness_probe(self):
        url = f"{self.target_url}/health/liveness"
        with urllib.request.urlopen(url, timeout=3) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertEqual(data.get("status"), "alive")

    def test_readiness_probe(self):
        url = f"{self.target_url}/health/readiness"
        with urllib.request.urlopen(url, timeout=3) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertEqual(data.get("status"), "ready")
            self.assertEqual(data.get("database"), "connected")

    def test_version_metadata(self):
        url = f"{self.target_url}/version"
        with urllib.request.urlopen(url, timeout=3) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertIn("version", data)
            self.assertIn("commit_sha", data)
            self.assertIn("artifact_digest", data)

    def test_order_creation_smoke(self):
        url = f"{self.target_url}/api/orders"
        payload = json.dumps({"customer_email": "smoke-test@example.com", "amount_cents": 1999}).encode()
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            self.assertEqual(resp.status, 201)
            data = json.loads(resp.read().decode())
            self.assertEqual(data.get("order", {}).get("status"), "pending")


if __name__ == "__main__":
    unittest.main()
