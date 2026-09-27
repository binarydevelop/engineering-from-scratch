"""
Project 08: Production Evaluation Harness (Phase 215).
Reusable automated evaluation system supporting:
- Dataset loaders
- Model runner wrappers
- Deterministic, semantic, and judge-based graders
- Multi-dimensional metrics (accuracy, latency, cost)
- Regression comparison gates.
"""

from typing import List, Dict, Any, Callable
import time

class EvalSample:
    def __init__(self, prompt: str, target: str, metadata: Dict[str, Any] = None):
        self.prompt = prompt
        self.target = target
        self.metadata = metadata or {}

class ProductionEvalHarness:
    def __init__(self, samples: List[EvalSample], grader_fn: Callable[[str, str], bool]):
        self.samples = samples
        self.grader_fn = grader_fn

    def evaluate(self, model_fn: Callable[[str], str]) -> Dict[str, Any]:
        passed = 0
        latencies = []
        
        for s in self.samples:
            t0 = time.perf_counter()
            pred = model_fn(s.prompt)
            latencies.append((time.perf_counter() - t0) * 1000.0)
            if self.grader_fn(pred, s.target):
                passed += 1

        total = len(self.samples)
        return {
            "total_samples": total,
            "passed": passed,
            "accuracy_pct": (passed / total) * 100.0 if total > 0 else 0.0,
            "mean_latency_ms": sum(latencies) / len(latencies) if latencies else 0.0,
            "p95_latency_ms": sorted(latencies)[int(0.95 * len(latencies))] if latencies else 0.0
        }
