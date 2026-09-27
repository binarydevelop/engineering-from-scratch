"""
Lesson 200: LSM-Tree Leveled Compaction
Implements two-pointer k-way merge of sorted SSTables and tombstone garbage collection.
"""
from typing import Dict, Any, List, Tuple

TOMBSTONE = "__DELETED__"

class PhaseComponent:
    def __init__(self):
        self.name = "LSM-Tree Leveled Compaction"
        self.metrics = {"operations_total": 0, "errors_total": 0, "compactions_total": 0}

    @staticmethod
    def compact_sstables(sstable_older: List[Tuple[str, str]], sstable_newer: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """Merges two sorted SSTables. Newer values supersede older values; tombstones purge entries."""
        merged = {}
        # Apply older entries
        for k, v in sstable_older:
            merged[k] = v
        # Apply newer entries (overwrites)
        for k, v in sstable_newer:
            if v == TOMBSTONE:
                merged.pop(k, None)
            else:
                merged[k] = v
        # Return sorted merged list
        return sorted(merged.items(), key=lambda x: x[0])

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("Compaction lock contention")

        older = payload.get("older_sstable", [("a", "1"), ("b", "2"), ("c", "3")])
        newer = payload.get("newer_sstable", [("b", "20"), ("c", TOMBSTONE), ("d", "4")])
        compacted = self.compact_sstables(older, newer)
        self.metrics["compactions_total"] += 1

        return {
            "status": "success",
            "phase": 200,
            "original_keys_count": len(older) + len(newer),
            "compacted_keys_count": len(compacted),
            "compacted_entries": compacted
        }

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics}
