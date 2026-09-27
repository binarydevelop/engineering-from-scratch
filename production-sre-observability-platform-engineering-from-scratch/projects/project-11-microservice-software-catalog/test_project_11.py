import unittest
from catalog_engine import SoftwareCatalog

class TestProject11(unittest.TestCase):
    def test_catalog_and_dependency_lookup(self):
        cat = SoftwareCatalog()
        cat.register("auth", "security-team", "tier-0", [])
        cat.register("checkout", "commerce-team", "tier-1", ["auth"])
        cat.register("gateway", "platform-team", "tier-0", ["checkout"])

        self.assertEqual(cat.find_dependents("auth"), ["checkout"])
        self.assertEqual(cat.find_dependents("checkout"), ["gateway"])

if __name__ == "__main__":
    unittest.main()
