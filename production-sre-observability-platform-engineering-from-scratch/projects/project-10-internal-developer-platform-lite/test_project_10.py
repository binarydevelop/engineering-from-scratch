import unittest
from idp_compiler import compile_service_yaml

class TestProject10(unittest.TestCase):
    def test_idp_compilation(self):
        res = compile_service_yaml({"name": "cart", "port": 8081, "replicas": 3})
        self.assertEqual(res["k8s_deployment"]["spec"]["replicas"], 3)
        self.assertEqual(res["k8s_service"]["spec"]["ports"][0]["port"], 8081)

if __name__ == "__main__":
    unittest.main()
