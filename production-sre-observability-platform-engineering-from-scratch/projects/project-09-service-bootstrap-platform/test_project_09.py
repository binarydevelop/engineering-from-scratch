import unittest
from bootstrapper import ServiceBootstrapper

class TestProject09(unittest.TestCase):
    def test_bootstrap_scaffold(self):
        files = ServiceBootstrapper.bootstrap("order-service")
        self.assertIn("Dockerfile", files)
        self.assertIn("deployment.yaml", files)
        self.assertIn("order-service", files["deployment.yaml"])

if __name__ == "__main__":
    unittest.main()
