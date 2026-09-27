"""
Broken implementation for: Stale Data Returned Due to Missing Cache Eviction
Defect: Database contains updated product price, but API GET endpoint returns old price indefinitely.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Database contains updated product price, but API GET endpoint returns old price indefinitely.
            raise RuntimeError("Defect triggered: Database contains updated product price, but API GET endpoint returns old price indefinitely.")
        return {"status": "ok", "result": payload}
