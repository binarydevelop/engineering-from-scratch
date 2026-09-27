"""
Broken implementation: Multi-Tenant Data Leak
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: SQL query retrieves documents using WHERE id = ? omitting tenant_id filter.")
        return {"status": "ok", "result": "fragile_success"}
