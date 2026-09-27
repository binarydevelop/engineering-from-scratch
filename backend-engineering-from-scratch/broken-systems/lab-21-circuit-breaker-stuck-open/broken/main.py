"""
Broken implementation for: Circuit Breaker Permanently Stuck in Open State
Defect: Downstream service recovers, but circuit breaker continues failing fast and never probes.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Downstream service recovers, but circuit breaker continues failing fast and never probes.
            raise RuntimeError("Defect triggered: Downstream service recovers, but circuit breaker continues failing fast and never probes.")
        return {"status": "ok", "result": payload}
