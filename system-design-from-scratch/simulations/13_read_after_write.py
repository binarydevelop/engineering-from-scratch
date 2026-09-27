import time
from typing import Dict, Any

class ReadAfterWriteRouter:
    def __init__(self, sticky_window_sec: float = 2.0):
        self.window = sticky_window_sec
        self.recent_writes: Dict[str, float] = {}

    def record_write(self, user_id: str):
        self.recent_writes[user_id] = time.time()

    def route_read(self, user_id: str) -> str:
        last_write = self.recent_writes.get(user_id, 0.0)
        if time.time() - last_write < self.window:
            return "PRIMARY"  # Avoid replication lag
        return "REPLICA"
