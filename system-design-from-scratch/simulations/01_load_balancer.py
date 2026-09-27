import random
from typing import List, Dict, Optional

class LoadBalancer:
    def __init__(self, algorithm: str = "round_robin"):
        self.algorithm = algorithm
        self.backends: List[Dict[str, any]] = []
        self._rr_index = 0

    def add_backend(self, host: str, weight: int = 1):
        self.backends.append({"host": host, "weight": weight, "active_conns": 0, "healthy": True})

    def mark_health(self, host: str, healthy: bool):
        for b in self.backends:
            if b["host"] == host:
                b["healthy"] = healthy

    def route(self) -> Optional[str]:
        healthy = [b for b in self.backends if b["healthy"]]
        if not healthy:
            return None

        if self.algorithm == "round_robin":
            choice = healthy[self._rr_index % len(healthy)]
            self._rr_index += 1
            return choice["host"]
        elif self.algorithm == "least_connections":
            choice = min(healthy, key=lambda b: b["active_conns"])
            return choice["host"]
        elif self.algorithm == "random":
            return random.choice(healthy)["host"]
        return healthy[0]["host"]

    def acquire_conn(self, host: str):
        for b in self.backends:
            if b["host"] == host:
                b["active_conns"] += 1

    def release_conn(self, host: str):
        for b in self.backends:
            if b["host"] == host and b["active_conns"] > 0:
                b["active_conns"] -= 1
