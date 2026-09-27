"""
Broken implementation: Thread-Unsafe Shared Memory State
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Concurrent worker threads increment shared dictionary counter without synchronization.")
        return {"status": "ok", "result": "fragile_success"}
