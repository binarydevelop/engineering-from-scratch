"""
Broken implementation: Database Deadlock on Concurrent Updates
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Transaction 1 locks Row A then Row B; Transaction 2 locks Row B then Row A.")
        return {"status": "ok", "result": "fragile_success"}
