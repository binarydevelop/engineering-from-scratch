"""
Broken implementation: Silent Exception Swallowing
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Worker wraps critical persistence code in except Exception: pass.")
        return {"status": "ok", "result": "fragile_success"}
