"""
Broken implementation for: Service Outage Caused by Unrotated Log Files
Defect: Database writes fail with `IOError: [Errno 28] No space left on device`.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Database writes fail with `IOError: [Errno 28] No space left on device`.
            raise RuntimeError("Defect triggered: Database writes fail with `IOError: [Errno 28] No space left on device`.")
        return {"status": "ok", "result": payload}
