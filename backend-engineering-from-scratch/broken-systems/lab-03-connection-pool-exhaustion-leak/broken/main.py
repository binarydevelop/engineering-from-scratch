"""
Broken implementation for: Database Connection Pool Exhaustion Leak
Defect: All database connections become saturated; application hangs and times out after 10 requests.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: All database connections become saturated; application hangs and times out after 10 requests.
            raise RuntimeError("Defect triggered: All database connections become saturated; application hangs and times out after 10 requests.")
        return {"status": "ok", "result": payload}
