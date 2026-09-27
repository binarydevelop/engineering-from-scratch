"""
Broken implementation: CORS Wildcard Credential Leak
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: API gateway configures Access-Control-Allow-Origin: * alongside credentials: true.")
        return {"status": "ok", "result": "fragile_success"}
