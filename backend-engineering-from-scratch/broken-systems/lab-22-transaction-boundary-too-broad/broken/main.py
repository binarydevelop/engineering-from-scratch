"""
Broken implementation for: Connection Starvation from Mega-Transaction
Defect: Database connection pool exhausted under 10 concurrent requests; all queries blocked.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Database connection pool exhausted under 10 concurrent requests; all queries blocked.
            raise RuntimeError("Defect triggered: Database connection pool exhausted under 10 concurrent requests; all queries blocked.")
        return {"status": "ok", "result": payload}
