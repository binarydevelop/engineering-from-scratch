"""
Broken implementation for: External Dependency Timeout Cascade
Defect: Third-party payment API hangs; upstream caller threads wait 60s, exhausting thread pools.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Third-party payment API hangs; upstream caller threads wait 60s, exhausting thread pools.
            raise RuntimeError("Defect triggered: Third-party payment API hangs; upstream caller threads wait 60s, exhausting thread pools.")
        return {"status": "ok", "result": payload}
