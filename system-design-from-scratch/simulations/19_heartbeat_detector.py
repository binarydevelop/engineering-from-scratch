import time
from typing import Dict

class HeartbeatDetector:
    def __init__(self, timeout_sec: float = 1.0):
        self.timeout = timeout_sec
        self.last_heartbeats: Dict[str, float] = {}

    def heartbeat(self, node_id: str):
        self.last_heartbeats[node_id] = time.time()

    def is_alive(self, node_id: str) -> bool:
        last = self.last_heartbeats.get(node_id)
        if last is None:
            return False
        return (time.time() - last) <= self.timeout
