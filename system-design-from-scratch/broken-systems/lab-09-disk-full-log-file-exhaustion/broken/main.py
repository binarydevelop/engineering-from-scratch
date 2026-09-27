"""
Broken implementation: Disk Full Log File Exhaustion
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Application logs verbose debug statements to a single file without rotation until disk is full.")
        return {"status": "ok", "result": "fragile_success"}
