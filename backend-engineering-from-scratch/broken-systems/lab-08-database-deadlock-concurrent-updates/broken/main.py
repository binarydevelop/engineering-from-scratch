"""
Broken implementation for: Database Deadlock on Inverted Lock Acquisition
Defect: Concurrent transfers between Account A and Account B trigger SQL 40P01 Deadlock Detected.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Concurrent transfers between Account A and Account B trigger SQL 40P01 Deadlock Detected.
            raise RuntimeError("Defect triggered: Concurrent transfers between Account A and Account B trigger SQL 40P01 Deadlock Detected.")
        return {"status": "ok", "result": payload}
