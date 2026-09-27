"""
Broken implementation for: Silent Overwrite from Missing Version Check
Defect: User A and User B edit document simultaneously; User B silently overwrites User A's changes.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: User A and User B edit document simultaneously; User B silently overwrites User A's changes.
            raise RuntimeError("Defect triggered: User A and User B edit document simultaneously; User B silently overwrites User A's changes.")
        return {"status": "ok", "result": payload}
