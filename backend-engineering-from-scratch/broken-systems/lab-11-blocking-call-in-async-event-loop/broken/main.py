"""
Broken implementation for: Event Loop Freeze from Synchronous Sleep
Defect: Single client calling slow endpoint freezes requests for all other concurrent users.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Single client calling slow endpoint freezes requests for all other concurrent users.
            raise RuntimeError("Defect triggered: Single client calling slow endpoint freezes requests for all other concurrent users.")
        return {"status": "ok", "result": payload}
