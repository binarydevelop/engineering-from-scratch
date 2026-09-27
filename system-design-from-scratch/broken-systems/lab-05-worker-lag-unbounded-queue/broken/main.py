"""
Broken implementation: Worker Lag on Unbounded Queue
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Producers write at 10,000 msg/s while consumers process 1,000 msg/s with no queue bounds.")
        return {"status": "ok", "result": "fragile_success"}
