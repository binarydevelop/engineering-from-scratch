"""
Broken implementation: Dual-Write Inconsistency
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Service writes order to database, then publishes event to Kafka; Kafka network call fails.")
        return {"status": "ok", "result": "fragile_success"}
