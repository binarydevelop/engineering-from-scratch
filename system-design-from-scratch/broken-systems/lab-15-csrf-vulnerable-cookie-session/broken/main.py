"""
Broken implementation: CSRF Vulnerable Cookie Session
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: State-changing POST requests rely on session cookies without anti-CSRF protection.")
        return {"status": "ok", "result": "fragile_success"}
