"""
Broken implementation for: Duplicate Financial Charges from Worker Retries
Defect: Network timeout between worker and queue causes message re-delivery; customer is billed twice.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Network timeout between worker and queue causes message re-delivery; customer is billed twice.
            raise RuntimeError("Defect triggered: Network timeout between worker and queue causes message re-delivery; customer is billed twice.")
        return {"status": "ok", "result": payload}
