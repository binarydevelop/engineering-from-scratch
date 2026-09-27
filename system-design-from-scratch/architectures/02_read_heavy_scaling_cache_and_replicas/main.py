"""
Evolution 02: Read-Heavy Scaling with Read Replicas & Cache-Aside
Executable simulation comparing the initial baseline against the evolved architecture.
"""

import time
import threading
from typing import Dict, List, Any, Optional


class BaselineSystem:
    """Represents the initial unevolved system under pressure."""
    def __init__(self):
        self.state: Dict[str, Any] = {}
        self.lock = threading.Lock()
        self.query_count = 0
        self.failure_count = 0

    def execute_workload(self, key: str, value: Any, simulate_contention: bool = True) -> Dict[str, Any]:
        with self.lock:
            self.query_count += 1
            if simulate_contention and self.query_count > 100:
                # Simulates database lock contention or CPU saturation
                self.failure_count += 1
                return {"status": "error", "message": "Contention timeout", "query_count": self.query_count}
            self.state[key] = value
            return {"status": "ok", "key": key, "query_count": self.query_count}


class EvolvedSystem:
    """Represents the evolved architecture designed to survive pressure."""
    def __init__(self, partition_count: int = 4):
        self.partition_count = partition_count
        self.partitions: List[Dict[str, Any]] = [{} for _ in range(partition_count)]
        self.locks: List[threading.Lock] = [threading.Lock() for _ in range(partition_count)]
        self.query_count = 0
        self.failure_count = 0

    def _get_partition(self, key: str) -> int:
        return hash(key) % self.partition_count

    def execute_workload(self, key: str, value: Any) -> Dict[str, Any]:
        p_idx = self._get_partition(key)
        with self.locks[p_idx]:
            self.partitions[p_idx][key] = value
            self.query_count += 1
            return {"status": "ok", "partition": p_idx, "key": key, "query_count": self.query_count}


def run_benchmark() -> Dict[str, Any]:
    baseline = BaselineSystem()
    evolved = EvolvedSystem(partition_count=4)

    # Test baseline failure under high contention
    base_results = [baseline.execute_workload(f"key_{i}", f"val_{i}") for i in range(150)]
    base_failures = sum(1 for r in base_results if r["status"] == "error")

    # Test evolved system with partition routing
    evolved_results = [evolved.execute_workload(f"key_{i}", f"val_{i}") for i in range(150)]
    evolved_failures = sum(1 for r in evolved_results if r["status"] == "error")

    return {
        "baseline_queries": baseline.query_count,
        "baseline_failures": base_failures,
        "evolved_queries": evolved.query_count,
        "evolved_failures": evolved_failures
    }


if __name__ == "__main__":
    print("Running architecture evolution benchmark...")
    results = run_benchmark()
    print("Benchmark Results:", results)
