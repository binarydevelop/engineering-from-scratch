"""
Broken implementation: Race Condition Lost Update
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Two concurrent requests read balance $100, calculate $100 - $30 = $70, and write back.")
        return {"status": "ok", "result": "fragile_success"}
