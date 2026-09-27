"""
Lesson 191: Raft Leader Election and Heartbeats
Implements role state transitions, RequestVote RPC logic, and heartbeat handling.
"""
from typing import Dict, Any, Optional, Set
import time
import random

class PhaseComponent:
    def __init__(self, node_id: int = 1, cluster_size: int = 3):
        self.name = "Raft Leader Election and Heartbeats"
        self.node_id = node_id
        self.cluster_size = cluster_size
        self.quorum_size = (cluster_size // 2) + 1
        self.current_term = 0
        self.voted_for: Optional[int] = None
        self.role = "FOLLOWER"  # FOLLOWER, CANDIDATE, LEADER
        self.votes_received: Set[int] = set()
        self.metrics = {"operations_total": 0, "errors_total": 0, "elections_started": 0}

    def start_election(self) -> Dict[str, Any]:
        """Transitions to Candidate and increments term."""
        self.role = "CANDIDATE"
        self.current_term += 1
        self.voted_for = self.node_id
        self.votes_received = {self.node_id}
        self.metrics["elections_started"] += 1
        return {"term": self.current_term, "candidate_id": self.node_id}

    def handle_request_vote(self, term: int, candidate_id: int) -> bool:
        """Grants vote if candidate term is newer and node has not voted in this term."""
        if term > self.current_term:
            self.current_term = term
            self.role = "FOLLOWER"
            self.voted_for = None

        if term == self.current_term and (self.voted_for is None or self.voted_for == candidate_id):
            self.voted_for = candidate_id
            return True
        return False

    def receive_vote(self, voter_id: int) -> str:
        """Records vote; transitions to LEADER if majority attained."""
        if self.role == "CANDIDATE":
            self.votes_received.add(voter_id)
            if len(self.votes_received) >= self.quorum_size:
                self.role = "LEADER"
        return self.role

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("Simulated election failure")

        action = payload.get("action", "heartbeat")
        if action == "start_election":
            self.start_election()
        elif action == "vote":
            voter = payload.get("voter_id", 2)
            self.receive_vote(voter)

        return {
            "status": "success",
            "phase": 191,
            "node_id": self.node_id,
            "role": self.role,
            "current_term": self.current_term,
            "votes": len(self.votes_received)
        }

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics, "role": self.role}
