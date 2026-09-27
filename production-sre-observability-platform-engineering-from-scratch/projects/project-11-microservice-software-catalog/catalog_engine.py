"""
Project 11: Service Catalog & Dependency Registry.
"""
from typing import Dict, Any, List

class SoftwareCatalog:
    def __init__(self):
        self.services: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, owner: str, tier: str, dependencies: List[str]):
        self.services[name] = {
            "name": name,
            "owner": owner,
            "tier": tier,
            "dependencies": dependencies
        }

    def get_service(self, name: str) -> Dict[str, Any]:
        return self.services.get(name, {})

    def find_dependents(self, target_service: str) -> List[str]:
        return [name for name, data in self.services.items() if target_service in data.get("dependencies", [])]
