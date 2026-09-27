"""
Broken implementation: Transaction Boundary Too Broad
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Database transaction remains open while application makes 5-second 3rd party HTTP call.")
        return {"status": "ok", "result": "fragile_success"}
