"""
Broken implementation for: Retry Storm Crashing Recovering Database
Defect: When database recovers from brief hiccup, 500 clients retry simultaneously, immediately crashing it again.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: When database recovers from brief hiccup, 500 clients retry simultaneously, immediately crashing it again.
            raise RuntimeError("Defect triggered: When database recovers from brief hiccup, 500 clients retry simultaneously, immediately crashing it again.")
        return {"status": "ok", "result": payload}
