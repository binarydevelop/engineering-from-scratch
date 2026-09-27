"""
Broken implementation for: Cross-Site Request Forgery on State Mutation
Defect: Rogue third-party website triggers unauthorized money transfer using victim's cached cookie.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Rogue third-party website triggers unauthorized money transfer using victim's cached cookie.
            raise RuntimeError("Defect triggered: Rogue third-party website triggers unauthorized money transfer using victim's cached cookie.")
        return {"status": "ok", "result": payload}
