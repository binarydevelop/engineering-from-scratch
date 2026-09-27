"""
Lesson 192: Raft Log Replication and Commit Index
Implements replicated log entries, AppendEntries consistency checks, and commit index advancement.
"""
from typing import Dict, Any, List, Optional

class PhaseComponent:
    def __init__(self, node_id: int = 1):
        self.name = "Raft Log Replication and Commit Index"
        self.node_id = node_id
        # Log entry: {"index": int, "term": int, "command": Any}
        self.log: List[Dict[str, Any]] = [{"index": 0, "term": 0, "command": "ROOT"}]
        self.commit_index = 0
        self.current_term = 1
        self.metrics = {"operations_total": 0, "errors_total": 0}

    def append_entries(self, term: int, prev_log_idx: int, prev_log_term: int, entries: List[Dict[str, Any]], leader_commit: int) -> bool:
        """Validates log matching invariant and appends new entries."""
        if term < self.current_term:
            return False

        # Invariant: prev_log_idx must exist and have matching prev_log_term
        if prev_log_idx >= len(self.log):
            return False
        if self.log[prev_log_idx]["term"] != prev_log_term:
            # Drop conflicting entries
            self.log = self.log[:prev_log_idx]
            return False

        # Append any new entries not already present
        for entry in entries:
            idx = entry["index"]
            if idx < len(self.log):
                self.log[idx] = entry
            else:
                self.log.append(entry)

        # Advance commit index
        if leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, len(self.log) - 1)
        return True

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("Simulated replication fault")

        entries = payload.get("entries", [{"index": len(self.log), "term": self.current_term, "command": "set x=1"}])
        success = self.append_entries(
            term=payload.get("term", self.current_term),
            prev_log_idx=payload.get("prev_log_idx", len(self.log) - 1),
            prev_log_term=payload.get("prev_log_term", self.log[-1]["term"]),
            entries=entries,
            leader_commit=payload.get("leader_commit", len(self.log))
        )
        return {
            "status": "success" if success else "rejected",
            "phase": 192,
            "commit_index": self.commit_index,
            "log_length": len(self.log)
        }

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics, "commit_index": self.commit_index}
