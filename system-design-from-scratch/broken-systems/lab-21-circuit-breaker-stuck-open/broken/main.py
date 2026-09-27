"""
Broken implementation: Circuit Breaker Stuck Open
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Circuit breaker opens on failure but never checks if downstream has recovered.")
        return {"status": "ok", "result": "fragile_success"}
