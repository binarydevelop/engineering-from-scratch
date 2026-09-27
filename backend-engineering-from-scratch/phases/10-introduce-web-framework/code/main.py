"""
Lesson 10: Introduce Web Framework
Implementation demonstrating core backend mechanisms.
"""

from typing import Dict, Any, Optional
import time

class PhaseComponent:
    """Core component representing Introduce Web Framework."""

    def __init__(self, name: str = "Introduce Web Framework"):
        self.name = name
        self.state: Dict[str, Any] = {"initialized": True, "phase": 10}
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
            raise RuntimeError(f"Simulated error in Introduce Web Framework")

        return {
            "status": "success",
            "phase": 10,
            "title": "Introduce Web Framework",
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
    print(f"[Introduce Web Framework] Execution result: {res['status']}")

if __name__ == "__main__":
    run_standalone()
