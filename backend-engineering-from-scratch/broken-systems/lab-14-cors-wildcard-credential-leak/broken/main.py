"""
Broken implementation for: Insecure Wildcard CORS Configuration
Defect: Browser blocks request or allows unauthorized origins to read sensitive authenticated data.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Browser blocks request or allows unauthorized origins to read sensitive authenticated data.
            raise RuntimeError("Defect triggered: Browser blocks request or allows unauthorized origins to read sensitive authenticated data.")
        return {"status": "ok", "result": payload}
