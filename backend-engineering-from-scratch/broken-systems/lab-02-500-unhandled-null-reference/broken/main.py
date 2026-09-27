"""
Broken implementation for: HTTP 500 Unhandled Null Reference
Defect: Incoming JSON payload with missing optional nested field causes unhandled KeyError / AttributeError.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Incoming JSON payload with missing optional nested field causes unhandled KeyError / AttributeError.
            raise RuntimeError("Defect triggered: Incoming JSON payload with missing optional nested field causes unhandled KeyError / AttributeError.")
        return {"status": "ok", "result": payload}
