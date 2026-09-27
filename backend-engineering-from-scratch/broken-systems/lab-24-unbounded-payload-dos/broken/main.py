"""
Broken implementation for: Denial of Service from Oversized JSON Body
Defect: Attacker sends 100MB JSON payload; server memory spikes and process is OOM-killed.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Attacker sends 100MB JSON payload; server memory spikes and process is OOM-killed.
            raise RuntimeError("Defect triggered: Attacker sends 100MB JSON payload; server memory spikes and process is OOM-killed.")
        return {"status": "ok", "result": payload}
