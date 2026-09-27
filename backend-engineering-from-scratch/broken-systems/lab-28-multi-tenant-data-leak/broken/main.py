"""
Broken implementation for: Cross-Tenant Data Leak from Missing Scoping
Defect: User in Tenant A accesses `/invoices/100` and views private invoice belonging to Tenant B.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: User in Tenant A accesses `/invoices/100` and views private invoice belonging to Tenant B.
            raise RuntimeError("Defect triggered: User in Tenant A accesses `/invoices/100` and views private invoice belonging to Tenant B.")
        return {"status": "ok", "result": payload}
