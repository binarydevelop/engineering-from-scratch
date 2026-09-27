"""
Broken implementation for: Event Ordering Failure Due to Server Clock Skew
Defect: Event A occurred before Event B, but Event B has an earlier timestamp due to unsynchronized clocks.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Event A occurred before Event B, but Event B has an earlier timestamp due to unsynchronized clocks.
            raise RuntimeError("Defect triggered: Event A occurred before Event B, but Event B has an earlier timestamp due to unsynchronized clocks.")
        return {"status": "ok", "result": payload}
