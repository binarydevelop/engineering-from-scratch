"""
Broken implementation for: Dual-Write Inconsistency Between SQL and Broker
Defect: Order exists in database, but customer never received confirmation because broker was down.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Order exists in database, but customer never received confirmation because broker was down.
            raise RuntimeError("Defect triggered: Order exists in database, but customer never received confirmation because broker was down.")
        return {"status": "ok", "result": payload}
