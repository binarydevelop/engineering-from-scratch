from typing import List, Callable, Dict, Any

class SagaStep:
    def __init__(self, name: str, execute_fn: Callable, compensate_fn: Callable):
        self.name = name
        self.execute = execute_fn
        self.compensate = compensate_fn

class SagaOrchestrator:
    def __init__(self, steps: List[SagaStep]):
        self.steps = steps
        self.executed_steps: List[SagaStep] = []

    def run(self) -> Dict[str, Any]:
        for step in self.steps:
            try:
                step.execute()
                self.executed_steps.append(step)
            except Exception as exc:
                # Rollback compensations in reverse
                for executed in reversed(self.executed_steps):
                    executed.compensate()
                return {"status": "FAILED_COMPENSATED", "failed_at": step.name, "error": str(exc)}
        return {"status": "SUCCESS"}
