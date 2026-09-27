"""
Lesson 196: gRPC Client Stub and Deadline Propagation
Implements gRPC timeout header parsing and context cancellation.
"""
from typing import Dict, Any
import time

class PhaseComponent:
    def __init__(self):
        self.name = "gRPC Client Stub and Deadline Propagation"
        self.metrics = {"operations_total": 0, "errors_total": 0, "deadlines_exceeded": 0}

    @staticmethod
    def parse_grpc_timeout(timeout_str: str) -> float:
        """Parses gRPC timeout header format: {value}{unit} (e.g. '100m', '2S', '1M')."""
        unit = timeout_str[-1]
        val = float(timeout_str[:-1])
        if unit == 'H': return val * 3600.0
        elif unit == 'M': return val * 60.0
        elif unit == 'S': return val
        elif unit == 'm': return val / 1000.0
        elif unit == 'u': return val / 1000000.0
        elif unit == 'n': return val / 1000000000.0
        raise ValueError(f"Unknown gRPC timeout unit: {unit}")

    def execute_rpc(self, timeout_header: str, simulated_duration: float) -> Dict[str, Any]:
        timeout_sec = self.parse_grpc_timeout(timeout_header)
        if simulated_duration > timeout_sec:
            self.metrics["deadlines_exceeded"] += 1
            return {"status": "DEADLINE_EXCEEDED", "code": 4, "elapsed": simulated_duration, "limit": timeout_sec}
        return {"status": "OK", "code": 0, "elapsed": simulated_duration}

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("Simulated RPC connection failure")

        timeout_str = payload.get("grpc-timeout", "500m")
        duration = payload.get("duration_sec", 0.1)
        res = self.execute_rpc(timeout_str, duration)
        return {"status": "success", "phase": 196, "rpc_result": res}

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics}
