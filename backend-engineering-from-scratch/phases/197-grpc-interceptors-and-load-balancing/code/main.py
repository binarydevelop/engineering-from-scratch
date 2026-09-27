"""
Lesson 197: gRPC Interceptors and Load Balancing
Implements client interceptor chain and client-side Round-Robin load balancing.
"""
from typing import Dict, Any, List, Callable

class PhaseComponent:
    def __init__(self, endpoints: List[str] = None):
        self.name = "gRPC Interceptors and Load Balancing"
        self.endpoints = endpoints or ["10.0.0.1:50051", "10.0.0.2:50051", "10.0.0.3:50051"]
        self.current_idx = 0
        self.interceptors: List[Callable] = []
        self.metrics = {"operations_total": 0, "errors_total": 0}

    def add_interceptor(self, fn: Callable):
        self.interceptors.append(fn)

    def pick_endpoint(self) -> str:
        """Round-robin endpoint selector."""
        ep = self.endpoints[self.current_idx]
        self.current_idx = (self.current_idx + 1) % len(self.endpoints)
        return ep

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("All endpoints unavailable")

        # Run interceptors
        for interceptor in self.interceptors:
            interceptor(payload)

        chosen_endpoint = self.pick_endpoint()
        return {
            "status": "success",
            "phase": 197,
            "endpoint": chosen_endpoint,
            "interceptors_count": len(self.interceptors)
        }

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics, "endpoints": self.endpoints}
