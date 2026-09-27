"""
Broken implementation for: Deep Offset Pagination Query Timeout
Defect: Requesting `?page=5000&limit=20` takes 4.2 seconds; database scans 100,000 rows.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Requesting `?page=5000&limit=20` takes 4.2 seconds; database scans 100,000 rows.
            raise RuntimeError("Defect triggered: Requesting `?page=5000&limit=20` takes 4.2 seconds; database scans 100,000 rows.")
        return {"status": "ok", "result": payload}
