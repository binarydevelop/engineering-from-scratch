"""
Broken implementation for: Distributed Deadlock Between Two Microservices
Defect: Service A calls Service B, which synchronously calls Service A back; both thread pools exhaust.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Service A calls Service B, which synchronously calls Service A back; both thread pools exhaust.
            raise RuntimeError("Defect triggered: Service A calls Service B, which synchronously calls Service A back; both thread pools exhaust.")
        return {"status": "ok", "result": payload}
