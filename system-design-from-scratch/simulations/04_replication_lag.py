import time
from typing import Dict, Any, List

class ReplicationNode:
    def __init__(self, name: str):
        self.name = name
        self.storage: Dict[str, Any] = {}
        self.commit_log: List[Dict[str, Any]] = []

class ReplicationCluster:
    def __init__(self, replication_delay_sec: float = 0.05):
        self.primary = ReplicationNode("primary")
        self.replicas = [ReplicationNode("replica_1"), ReplicationNode("replica_2")]
        self.replication_delay = replication_delay_sec

    def write(self, key: str, val: Any) -> int:
        version = len(self.primary.commit_log) + 1
        record = {"version": version, "key": key, "val": val, "committed_at": time.time()}
        self.primary.storage[key] = val
        self.primary.commit_log.append(record)
        return version

    def sync_replicas(self, target_version: int):
        for rec in self.primary.commit_log:
            if rec["version"] <= target_version:
                for rep in self.replicas:
                    rep.storage[rec["key"]] = rec["val"]
                    if rec not in rep.commit_log:
                        rep.commit_log.append(rec)

    def read_replica(self, replica_idx: int, key: str) -> Any:
        return self.replicas[replica_idx].storage.get(key)
