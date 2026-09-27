"""
Chaos injection module for simulating real-world backend infrastructure faults.
"""

import time
from typing import Optional

class DatabaseDropError(Exception):
    """Simulates abrupt TCP connection drop to database."""
    pass

class DatabaseTimeoutError(Exception):
    """Simulates query execution exceeding deadline."""
    pass

class CacheFailureError(Exception):
    """Simulates Redis node partition or OOM crash."""
    pass

class WorkerCrashError(Exception):
    """Simulates async worker thread panic or uncaught exception."""
    pass

class ChaosInjector:
    def __init__(self):
        self.drop_db = False
        self.timeout_db = False
        self.drop_cache = False
        self.crash_worker = False
        self.injected_latency_sec = 0.0

    def maybe_fail_db(self):
        if self.injected_latency_sec > 0:
            time.sleep(self.injected_latency_sec)
        if self.timeout_db:
            raise DatabaseTimeoutError("Database operation timed out after deadline")
        if self.drop_db:
            raise DatabaseDropError("Connection reset by database server")

    def maybe_fail_cache(self):
        if self.drop_cache:
            raise CacheFailureError("Redis connection refused: cluster partition")

    def maybe_crash_worker(self):
        if self.crash_worker:
            raise WorkerCrashError("Worker encountered fatal unhandled exception")
