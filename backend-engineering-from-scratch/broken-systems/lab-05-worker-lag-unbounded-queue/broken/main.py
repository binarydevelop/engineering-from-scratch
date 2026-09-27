"""
Broken implementation for: Worker Queue Lag and Unbounded Growth
Defect: Queue depth grows continuously; worker memory usage swells until process is OOM-killed.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Queue depth grows continuously; worker memory usage swells until process is OOM-killed.
            raise RuntimeError("Defect triggered: Queue depth grows continuously; worker memory usage swells until process is OOM-killed.")
        return {"status": "ok", "result": payload}
