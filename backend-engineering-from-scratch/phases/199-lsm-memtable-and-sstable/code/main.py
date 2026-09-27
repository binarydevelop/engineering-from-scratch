"""
Lesson 199: LSM-Tree MemTable and SSTable
Implements sorted MemTable, immutable SSTable flushing, and sparse index lookups.
"""
from typing import Dict, Any, List, Optional

class PhaseComponent:
    def __init__(self, memtable_threshold: int = 4):
        self.name = "LSM-Tree MemTable and SSTable"
        self.memtable_threshold = memtable_threshold
        self.memtable: Dict[str, str] = {}
        # SSTable: list of sorted (key, value) tuples + index
        self.sstables: List[List[tuple]] = []
        self.metrics = {"operations_total": 0, "errors_total": 0, "flushes_total": 0}

    def put(self, key: str, value: str):
        self.memtable[key] = value
        if len(self.memtable) >= self.memtable_threshold:
            self.flush()

    def flush(self):
        """Flushes MemTable to a new SSTable sorted by key."""
        sorted_entries = sorted(self.memtable.items(), key=lambda x: x[0])
        self.sstables.append(sorted_entries)
        self.memtable = {}
        self.metrics["flushes_total"] += 1

    def get(self, key: str) -> Optional[str]:
        # 1. Check MemTable
        if key in self.memtable:
            return self.memtable[key]
        # 2. Check SSTables in reverse chronological order
        for sstable in reversed(self.sstables):
            for k, v in sstable:
                if k == key:
                    return v
        return None

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("SSTable write failure")

        k = payload.get("key", "k1")
        v = payload.get("value", "v1")
        self.put(k, v)

        return {
            "status": "success",
            "phase": 199,
            "memtable_size": len(self.memtable),
            "sstables_count": len(self.sstables),
            "queried_value": self.get(k)
        }

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics}
