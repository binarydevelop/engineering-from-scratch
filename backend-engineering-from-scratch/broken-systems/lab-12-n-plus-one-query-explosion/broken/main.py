"""
Broken implementation for: N+1 Query Explosion on Relationship Endpoint
Defect: Fetching 50 users triggers 51 separate SQL queries, degrading endpoint latency to 300ms.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Fetching 50 users triggers 51 separate SQL queries, degrading endpoint latency to 300ms.
            raise RuntimeError("Defect triggered: Fetching 50 users triggers 51 separate SQL queries, degrading endpoint latency to 300ms.")
        return {"status": "ok", "result": payload}
