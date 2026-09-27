"""
Broken implementation: Circular Dependency Deadlock
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Service A calls Service B, which synchronously calls Service A to verify permissions.")
        return {"status": "ok", "result": "fragile_success"}
