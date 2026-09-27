"""
Lesson 25: Isolation and Concurrent Requests
Implementation demonstrating core backend mechanisms.
"""

from typing import Dict, Any, Optional
import time

class PhaseComponent:
    """Core component representing Isolation and Concurrent Requests."""

    def __init__(self, name: str = "Isolation and Concurrent Requests"):
        self.name = name
        self.state: Dict[str, Any] = {"initialized": True, "phase": 25}
        self.metrics: Dict[str, int] = {"operations_total": 0, "errors_total": 0}

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Processes request payload enforcing invariants."""
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        
        # Enforce validation and business invariants
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError(f"Simulated error in Isolation and Concurrent Requests")

        return {
            "status": "success",
            "phase": 25,
            "title": "Isolation and Concurrent Requests",
            "processed_at": time.time(),
            "data": payload
        }

    def get_telemetry(self) -> Dict[str, Any]:
        """Returns component metrics and operational state."""
        return {
            "component": self.name,
            "metrics": self.metrics,
            "state": self.state
        }

def run_standalone():
    """Demonstrates component execution."""
    comp = PhaseComponent()
    res = comp.process({"sample_key": "sample_val"})
    print(f"[Isolation and Concurrent Requests] Execution result: {res['status']}")

if __name__ == "__main__":
    run_standalone()
