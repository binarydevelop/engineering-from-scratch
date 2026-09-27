"""
Health probe checker for liveness and readiness probes.
"""

from typing import Dict, Any, Callable

class ProbeManager:
    def __init__(self):
        self.dependencies: Dict[str, Callable[[], bool]] = {}

    def register_dependency(self, name: str, check_fn: Callable[[], bool]):
        self.dependencies[name] = check_fn

    def check_liveness(self) -> Dict[str, Any]:
        # Process is running and event loop is responsive
        return {"status": "ALIVE"}

    def check_readiness(self) -> Dict[str, Any]:
        # Checks if all external dependencies are responsive
        status = "READY"
        failed = []
        for name, check in self.dependencies.items():
            try:
                ok = check()
                if not ok:
                    status = "NOT_READY"
                    failed.append(name)
            except Exception:
                status = "NOT_READY"
                failed.append(name)

        return {
            "status": status,
            "dependencies_checked": len(self.dependencies),
            "unhealthy": failed
        }
