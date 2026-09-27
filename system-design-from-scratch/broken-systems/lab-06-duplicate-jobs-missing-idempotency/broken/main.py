"""
Broken implementation: Duplicate Jobs Due to Missing Idempotency
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Worker crashes after charging customer but before acknowledging queue message, causing duplicate charges on retry.")
        return {"status": "ok", "result": "fragile_success"}
