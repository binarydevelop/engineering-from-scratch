import time
from collections import deque
from typing import Dict

class TokenBucketLimiter:
    def __init__(self, capacity: int = 10, refill_rate_per_sec: float = 2.0):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens: Dict[str, float] = {}
        self.last_updated: Dict[str, float] = {}

    def allow_request(self, client_id: str) -> bool:
        now = time.time()
        tokens = self.tokens.get(client_id, self.capacity)
        last_time = self.last_updated.get(client_id, now)

        elapsed = now - last_time
        tokens = min(self.capacity, tokens + elapsed * self.refill_rate)
        self.last_updated[client_id] = now

        if tokens >= 1.0:
            self.tokens[client_id] = tokens - 1.0
            return True
        self.tokens[client_id] = tokens
        return False

class SlidingWindowLogLimiter:
    def __init__(self, max_requests: int = 5, window_seconds: float = 1.0):
        self.max_requests = max_requests
        self.window = window_seconds
        self.logs: Dict[str, deque] = {}

    def allow_request(self, client_id: str) -> bool:
        now = time.time()
        if client_id not in self.logs:
            self.logs[client_id] = deque()

        q = self.logs[client_id]
        while q and q[0] <= now - self.window:
            q.popleft()

        if len(q) < self.max_requests:
            q.append(now)
            return True
        return False
