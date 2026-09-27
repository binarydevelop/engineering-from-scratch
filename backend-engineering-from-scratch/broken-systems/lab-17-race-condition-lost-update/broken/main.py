"""
Broken implementation for: Lost Update Anomaly Under Concurrent Purchases
Defect: Two simultaneous purchases of the last item both succeed; stock is oversold to -1.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Two simultaneous purchases of the last item both succeed; stock is oversold to -1.
            raise RuntimeError("Defect triggered: Two simultaneous purchases of the last item both succeed; stock is oversold to -1.")
        return {"status": "ok", "result": payload}
