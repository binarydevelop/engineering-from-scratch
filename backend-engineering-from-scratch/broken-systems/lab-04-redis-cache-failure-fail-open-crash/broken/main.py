"""
Broken implementation for: Application Crash on Redis Cache Outage
Defect: When Redis crashes, entire API throws unhandled ConnectionRefusedError returning 500 for all reads.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: When Redis crashes, entire API throws unhandled ConnectionRefusedError returning 500 for all reads.
            raise RuntimeError("Defect triggered: When Redis crashes, entire API throws unhandled ConnectionRefusedError returning 500 for all reads.")
        return {"status": "ok", "result": payload}
