import time
from typing import Dict, List, Any, Optional

class PartitionedQueueBroker:
    def __init__(self, num_partitions: int = 4, max_retries: int = 2):
        self.num_partitions = num_partitions
        self.max_retries = max_retries
        self.partitions: List[List[Dict[str, Any]]] = [[] for _ in range(num_partitions)]
        self.dlq: List[Dict[str, Any]] = []

    def publish(self, key: str, payload: Any):
        pid = hash(key) % self.num_partitions
        msg = {
            "key": key,
            "payload": payload,
            "attempts": 0,
            "visible_at": time.time()
        }
        self.partitions[pid].append(msg)

    def consume(self, partition_id: int, visibility_timeout_sec: float = 0.5) -> Optional[Dict[str, Any]]:
        now = time.time()
        part = self.partitions[partition_id]
        for msg in part:
            if now >= msg["visible_at"]:
                msg["attempts"] += 1
                if msg["attempts"] > self.max_retries:
                    part.remove(msg)
                    self.dlq.append(msg)
                    continue
                msg["visible_at"] = now + visibility_timeout_sec
                return msg
        return None
