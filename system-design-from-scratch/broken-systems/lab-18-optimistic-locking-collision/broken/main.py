"""
Broken implementation: Optimistic Locking Collision Storm
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: High-concurrency updates on hot row cause version conflicts, triggering infinite unjittered retries.")
        return {"status": "ok", "result": "fragile_success"}
