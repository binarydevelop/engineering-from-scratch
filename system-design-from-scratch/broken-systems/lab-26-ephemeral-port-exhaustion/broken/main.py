"""
Broken implementation: Ephemeral Port Exhaustion
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: HTTP client creates fresh TCP connection for every outbound request without pooling.")
        return {"status": "ok", "result": "fragile_success"}
