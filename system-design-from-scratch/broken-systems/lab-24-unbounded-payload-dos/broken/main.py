"""
Broken implementation: Unbounded Payload Denial of Service
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: API reads request body with f.read() into memory without Content-Length limit.")
        return {"status": "ok", "result": "fragile_success"}
