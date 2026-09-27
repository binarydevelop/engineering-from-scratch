"""
Broken implementation: JWT Alg=None Signature Bypass
"""

class Subsystem:
    def __init__(self):
        self.state = "UNHEALTHY_BASELINE"
        self.defect_active = True

    def execute(self, params: dict) -> dict:
        if params.get("induce_failure", False) or self.defect_active:
            raise RuntimeError("Defect triggered: Token verification parser accepts alg: none in header without signature check.")
        return {"status": "ok", "result": "fragile_success"}
