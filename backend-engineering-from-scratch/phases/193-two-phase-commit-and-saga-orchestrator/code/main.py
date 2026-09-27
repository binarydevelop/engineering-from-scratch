"""
Lesson 193: Two-Phase Commit and Saga Orchestrator
Implements 2PC coordinator and Saga compensation workflow.
"""
from typing import Dict, Any, List

class PhaseComponent:
    def __init__(self):
        self.name = "Two-Phase Commit and Saga Orchestrator"
        self.metrics = {"operations_total": 0, "errors_total": 0, "compensations_total": 0}

    def run_2pc(self, participants: List[str], should_fail: bool = False) -> Dict[str, Any]:
        """Phase 1: Prepare. Phase 2: Commit or Abort."""
        votes = {}
        for p in participants:
            votes[p] = "VOTE_ABORT" if should_fail and p == participants[-1] else "VOTE_COMMIT"

        all_commit = all(v == "VOTE_COMMIT" for v in votes.values())
        decision = "GLOBAL_COMMIT" if all_commit else "GLOBAL_ABORT"
        return {"protocol": "2PC", "decision": decision, "votes": votes}

    def run_saga(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Executes forward steps; if any step fails, executes reverse compensations."""
        executed = []
        for step in steps:
            if step.get("fail"):
                self.metrics["compensations_total"] += len(executed)
                # Compensate executed steps in reverse order
                compensated = [s["compensation"] for s in reversed(executed)]
                return {"protocol": "SAGA", "status": "COMPENSATED", "compensated_steps": compensated}
            executed.append(step)
        return {"protocol": "SAGA", "status": "COMPLETED", "steps_count": len(executed)}

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("Simulated transaction crash")

        proto = payload.get("protocol", "2pc")
        if proto == "saga":
            steps = payload.get("steps", [{"action": "reserve_stock", "compensation": "release_stock"}])
            res = self.run_saga(steps)
        else:
            parts = payload.get("participants", ["billing", "inventory"])
            res = self.run_2pc(parts, payload.get("fail_participant", False))

        return {"status": "success", "phase": 193, "result": res}

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics}
