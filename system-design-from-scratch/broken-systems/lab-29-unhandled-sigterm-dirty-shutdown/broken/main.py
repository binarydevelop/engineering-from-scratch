"""
Broken implementation: Unhandled SIGTERM Dirty Shutdown
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Kubernetes sends SIGTERM; application terminates instantly killing in-flight requests.")
        return {"status": "ok", "result": "fragile_success"}
