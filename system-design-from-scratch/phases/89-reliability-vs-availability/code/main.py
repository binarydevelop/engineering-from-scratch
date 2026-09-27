"""
Phase 89: Reliability vs Availability
Core simulation model representing the architectural subsystem.
"""

import time
from typing import Dict, Any, Optional

class PhaseSystem:
    def __init__(self, name: str = "Reliability vs Availability"):
        self.name = name
        self.phase_num = 89
        self.metrics: Dict[str, Any] = {
            "requests_total": 0,
            "errors_total": 0,
            "latency_history_ms": []
        }
        self.chaos_active = False

    def process_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        start = time.perf_counter()
        self.metrics["requests_total"] += 1

        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")

        if self.chaos_active or payload.get("induce_failure", False):
            self.metrics["errors_total"] += 1
            raise RuntimeError(f"Chaos failure triggered in Phase 89: Reliability vs Availability")

        # Core domain processing
        duration_ms = (time.perf_counter() - start) * 1000.0
        self.metrics["latency_history_ms"].append(duration_ms)

        return {
            "status": "SUCCESS",
            "phase": self.phase_num,
            "system": self.name,
            "latency_ms": round(duration_ms, 3),
            "data": payload
        }

    def get_telemetry(self) -> Dict[str, Any]:
        latencies = self.metrics["latency_history_ms"]
        avg_lat = sum(latencies) / len(latencies) if latencies else 0.0
        return {
            "system": self.name,
            "phase": self.phase_num,
            "requests_total": self.metrics["requests_total"],
            "errors_total": self.metrics["errors_total"],
            "avg_latency_ms": round(avg_lat, 3)
        }
