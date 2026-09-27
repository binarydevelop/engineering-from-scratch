"""
Broken implementation for: Dropped Requests During Rolling Container Deploy
Defect: Kubernetes rolling update causes 502 Bad Gateway errors for in-flight requests.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Kubernetes rolling update causes 502 Bad Gateway errors for in-flight requests.
            raise RuntimeError("Defect triggered: Kubernetes rolling update causes 502 Bad Gateway errors for in-flight requests.")
        return {"status": "ok", "result": payload}
