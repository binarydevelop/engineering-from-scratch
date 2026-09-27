"""
Broken implementation for: Process OOM from Unbounded Global Cache
Defect: Application memory RSS grows linearly with requests until process is terminated by OS OOM killer.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Application memory RSS grows linearly with requests until process is terminated by OS OOM killer.
            raise RuntimeError("Defect triggered: Application memory RSS grows linearly with requests until process is terminated by OS OOM killer.")
        return {"status": "ok", "result": payload}
