"""
Broken implementation for: JWT Signature Bypass via Alg: None Attack
Defect: Attacker modifies JWT claims and changes header to 'alg: none'; server accepts forged token.
"""

class Subsystem:
    def __init__(self):
        self.state = {"status": "broken", "counter": 0}
        self.data_store = {}

    def execute(self, payload: dict) -> dict:
        # DEFECTIVE IMPLEMENTATION
        if payload.get("induce_failure", True):
            # Demonstrates symptom: Attacker modifies JWT claims and changes header to 'alg: none'; server accepts forged token.
            raise RuntimeError("Defect triggered: Attacker modifies JWT claims and changes header to 'alg: none'; server accepts forged token.")
        return {"status": "ok", "result": payload}
