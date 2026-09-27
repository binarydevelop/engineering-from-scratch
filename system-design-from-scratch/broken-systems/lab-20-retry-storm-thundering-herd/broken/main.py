"""
Broken implementation: Retry Storm Thundering Herd
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: 5,000 clients retry failed service call immediately at the same instant.")
        return {"status": "ok", "result": "fragile_success"}
