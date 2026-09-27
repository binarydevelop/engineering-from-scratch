"""
Production Circuit Breaker State Machine.

Prevents cascade failures and retry storms by tripping open when downstream
services fail repeatedly, failing fast until a cooldown period elapses.
"""

import time
import threading
from enum import Enum
from typing import Callable, Any, Optional


class CircuitState(str, Enum):
    CLOSED = "CLOSED"        # Normal health, passing requests
    OPEN = "OPEN"            # Tripped, rejecting requests fast
    HALF_OPEN = "HALF_OPEN"  # Testing single probe request to check recovery


class CircuitBreakerOpenException(Exception):
    """Raised when an operation is rejected by an open circuit breaker."""
    pass


class CircuitBreaker:
    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_sec: float = 15.0
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: float = 0.0
        self._lock = threading.Lock()

    def can_execute(self) -> bool:
        with self._lock:
            now = time.time()
            if self.state == CircuitState.OPEN:
                if now - self.last_failure_time >= self.recovery_timeout_sec:
                    self.state = CircuitState.HALF_OPEN
                    return True
                return False
            return True

    def record_success(self) -> None:
        with self._lock:
            self.failure_count = 0
            self.state = CircuitState.CLOSED

    def record_failure(self) -> None:
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN

    def call(self, func: Callable, *args, **kwargs) -> Any:
        if not self.can_execute():
            raise CircuitBreakerOpenException(f"Circuit breaker '{self.name}' is OPEN. Failing fast.")
        
        try:
            result = func(*args, **kwargs)
            self.record_success()
            return result
        except Exception as e:
            self.record_failure()
            raise e
