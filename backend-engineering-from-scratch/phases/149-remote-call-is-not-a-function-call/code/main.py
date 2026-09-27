"""
Lesson 149: Remote Call Is Not a Function Call
Implementation demonstrating core backend mechanisms.
"""

from typing import Dict, Any, Optional
import time

class PhaseComponent:
    """Core component representing Remote Call Is Not a Function Call."""

    def __init__(self, name: str = "Remote Call Is Not a Function Call"):
        self.name = name
        self.state: Dict[str, Any] = {"initialized": True, "phase": 149}
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
            raise RuntimeError(f"Simulated error in Remote Call Is Not a Function Call")

        return {
            "status": "success",
            "phase": 149,
            "title": "Remote Call Is Not a Function Call",
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
    print(f"[Remote Call Is Not a Function Call] Execution result: {res['status']}")

if __name__ == "__main__":
    run_standalone()
