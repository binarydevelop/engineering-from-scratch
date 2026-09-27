import time
from typing import Callable, Any

class CircuitBreakerOpenError(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_time_sec: float = 0.5):
        self.threshold = failure_threshold
        self.recovery_time = recovery_time_sec
        self.failures = 0
        self.last_failure_time = 0.0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, fn: Callable, *args, **kwargs) -> Any:
        now = time.time()
        if self.state == "OPEN":
            if now - self.last_failure_time > self.recovery_time:
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpenError("Circuit is OPEN: Fast-failing")

        try:
            res = fn(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failures = 0
            return res
        except Exception as exc:
            self.failures += 1
            self.last_failure_time = now
            if self.failures >= self.threshold:
                self.state = "OPEN"
            raise exc
