from collections import deque
from typing import Any

class BackpressureBuffer:
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.buffer = deque()

    def push(self, item: Any) -> bool:
        if len(self.buffer) >= self.capacity:
            return False  # Signal upstream to back off
        self.buffer.append(item)
        return True

    def pop(self) -> Any:
        return self.buffer.popleft() if self.buffer else None
