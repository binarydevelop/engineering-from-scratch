"""
Broken implementation: DNS Failure Timeout Cascade
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: DNS provider encounters transient failure; backend attempts fresh lookup per request with no cache.")
        return {"status": "ok", "result": "fragile_success"}
