"""
Broken implementation for: Credential Stuffing on Unthrottled Login
Defect: Attacker submits 5,000 password guesses per minute against `/login` without restriction.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Attacker submits 5,000 password guesses per minute against `/login` without restriction.
            raise RuntimeError("Defect triggered: Attacker submits 5,000 password guesses per minute against `/login` without restriction.")
        return {"status": "ok", "result": payload}
