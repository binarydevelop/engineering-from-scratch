"""
Broken implementation: Unindexed Query Lock Escalation
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Concurrent queries on unindexed column trigger sequential table scans, escalating row locks to table locks.")
        return {"status": "ok", "result": "fragile_success"}
