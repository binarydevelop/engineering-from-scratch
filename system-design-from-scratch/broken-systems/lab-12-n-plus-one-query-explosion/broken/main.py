"""
Broken implementation: N+1 Query Explosion
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Endpoint fetches 100 users, then executes a separate query in a loop for each user's orders.")
        return {"status": "ok", "result": "fragile_success"}
