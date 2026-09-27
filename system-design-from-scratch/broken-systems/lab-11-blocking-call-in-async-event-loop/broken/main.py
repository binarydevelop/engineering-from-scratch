"""
Broken implementation: Blocking Call in Async Event Loop
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Asynchronous route handler invokes synchronous time.sleep or disk I/O.")
        return {"status": "ok", "result": "fragile_success"}
