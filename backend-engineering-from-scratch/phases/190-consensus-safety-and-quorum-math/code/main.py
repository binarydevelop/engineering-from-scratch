"""
Lesson 190: Consensus Safety and Quorum Math
Implements quorum intersection, majority calculation, and partition progress safety.
"""
from typing import Dict, Any, List, Set
import time

class PhaseComponent:
    def __init__(self, cluster_size: int = 5):
        self.name = "Consensus Safety and Quorum Math"
        self.cluster_size = cluster_size
        self.quorum_size = (cluster_size // 2) + 1
        self.state: Dict[str, Any] = {
            "phase": 190,
            "cluster_size": self.cluster_size,
            "quorum_size": self.quorum_size,
            "active_nodes": set(range(cluster_size))
        }
        self.metrics = {"operations_total": 0, "errors_total": 0}

    def can_commit(self, responding_nodes: Set[int]) -> bool:
        """Enforces that writes can only commit if accepted by a strict majority."""
        return len(responding_nodes) >= self.quorum_size

    def check_quorum_intersection(self, q1: Set[int], q2: Set[int]) -> bool:
        """Pigeonhole principle: Any two majority quorums must overlap by at least 1 node."""
        if len(q1) < self.quorum_size or len(q2) < self.quorum_size:
            return False
        return len(q1.intersection(q2)) >= 1

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("Simulated consensus error")

        responding = set(payload.get("responding_nodes", range(self.cluster_size)))
        is_safe = self.can_commit(responding)

        return {
            "status": "success" if is_safe else "partitioned_rejection",
            "phase": 190,
            "quorum_size": self.quorum_size,
            "votes_received": len(responding),
            "can_commit": is_safe,
            "data": payload
        }

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics, "state": self.state}
