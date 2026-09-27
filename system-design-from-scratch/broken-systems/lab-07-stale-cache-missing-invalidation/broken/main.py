"""
Broken implementation: Stale Cache Missing Invalidation
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Database record is updated directly, but corresponding cache key is never invalidated.")
        return {"status": "ok", "result": "fragile_success"}
