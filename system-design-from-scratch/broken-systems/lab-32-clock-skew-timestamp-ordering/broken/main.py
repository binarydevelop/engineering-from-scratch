"""
Broken implementation: Clock Skew Timestamp Ordering
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Two nodes use wall-clock datetime.now() for Last-Write-Wins conflict resolution.")
        return {"status": "ok", "result": "fragile_success"}
