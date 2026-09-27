"""
Resilience primitives: Circuit Breaker, Fault-Tolerant Cache-Aside, and Retries.
"""

import time
from typing import Callable, Any, Dict, Optional
from chaos import CacheFailureError

class CircuitBreakerOpenError(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout_sec: float = 0.5):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func: Callable, *args, **kwargs) -> Any:
        now = time.time()

        if self.state == "OPEN":
            if now - self.last_failure_time > self.recovery_timeout_sec:
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpenError("Circuit is OPEN: fast failing call")

        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as exc:
            self.failure_count += 1
            self.last_failure_time = now
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            raise exc

class CacheAsideManager:
    def __init__(self, primary_db: Callable, cache_store: Dict[str, Any]):
        self.primary_db = primary_db
        self.cache_store = cache_store
        self.cache_misses = 0
        self.cache_faults = 0

    def get_with_fallback(self, key: str, chaos_check: Optional[Callable] = None) -> Any:
        # Step 1: Attempt cache retrieval
        try:
            if chaos_check:
                chaos_check()
            if key in self.cache_store:
                return self.cache_store[key]
            self.cache_misses += 1
        except CacheFailureError:
            # Degrade gracefully: log error and fall back to source of truth
            self.cache_faults += 1

        # Step 2: Fetch from primary database
        data = self.primary_db(key)

        # Step 3: Best-effort cache populate
        try:
            if data is not None and not (chaos_check and getattr(chaos_check, "__self__", None) and getattr(chaos_check.__self__, "drop_cache", False)):
                self.cache_store[key] = data
        except Exception:
            pass

        return data
