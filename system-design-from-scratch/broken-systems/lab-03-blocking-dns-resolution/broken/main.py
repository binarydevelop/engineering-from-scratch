"""
Broken implementation: Blocking DNS Resolution
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Synchronous socket DNS resolution blocks the asynchronous worker loop.")
        return {"status": "ok", "result": "fragile_success"}
