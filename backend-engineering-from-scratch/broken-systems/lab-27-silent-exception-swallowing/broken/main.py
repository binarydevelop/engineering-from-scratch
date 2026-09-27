"""
Broken implementation for: Silent Data Corruption from Swallowed Exception
Defect: Inventory balance is wrong, but zero errors appear in logs or monitoring dashboards.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Inventory balance is wrong, but zero errors appear in logs or monitoring dashboards.
            raise RuntimeError("Defect triggered: Inventory balance is wrong, but zero errors appear in logs or monitoring dashboards.")
        return {"status": "ok", "result": payload}
