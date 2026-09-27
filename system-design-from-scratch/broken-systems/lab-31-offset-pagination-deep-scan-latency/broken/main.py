"""
Broken implementation: Offset Pagination Deep Scan Latency
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Client requests SELECT * FROM logs ORDER BY id LIMIT 20 OFFSET 1000000.")
        return {"status": "ok", "result": "fragile_success"}
