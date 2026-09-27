"""
Broken implementation for: Slow API Due to Missing Database Index
Defect: p99 latency increases from 5ms to 2500ms as table row count grows; CPU is idle waiting for disk I/O.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: p99 latency increases from 5ms to 2500ms as table row count grows; CPU is idle waiting for disk I/O.
            raise RuntimeError("Defect triggered: p99 latency increases from 5ms to 2500ms as table row count grows; CPU is idle waiting for disk I/O.")
        return {"status": "ok", "result": payload}
