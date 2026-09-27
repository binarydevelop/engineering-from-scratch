"""
Lesson 20: Connection Pooling from First Principles.
Implements a bounded pool of reusable database connections with timeout and starvation handling.
"""

import queue
import time
import uuid
from typing import Optional

class MockDBConnection:
    """Represents an established, persistent database connection."""

    def __init__(self, conn_id: str):
        self.conn_id = conn_id
        self.is_closed = False
        self.queries_executed = 0

    def execute(self, query: str) -> str:
        if self.is_closed:
            raise RuntimeError("Cannot execute query on closed connection")
        self.queries_executed += 1
        return f"result_for_{query}"

    def close(self):
        self.is_closed = True

class ConnectionPool:
    """A bounded pool of reusable database connections."""

    def __init__(self, min_size: int = 2, max_size: int = 5, timeout: float = 1.0):
        self.max_size = max_size
        self.timeout = timeout
        self._pool: queue.Queue[MockDBConnection] = queue.Queue(maxsize=max_size)
        self.allocated_count = 0

        # Pre-seed min_size connections
        for _ in range(min_size):
            conn = self._create_connection()
            self._pool.put(conn)

    def _create_connection(self) -> MockDBConnection:
        self.allocated_count += 1
        return MockDBConnection(conn_id=str(uuid.uuid4())[:8])

    def acquire(self) -> MockDBConnection:
        """Acquires a connection from the pool, blocking up to timeout seconds."""
        try:
            # First check if an existing connection is idle in the queue
            return self._pool.get_nowait()
        except queue.Empty:
            # If not, can we allocate a new connection up to max_size?
            if self.allocated_count < self.max_size:
                return self._create_connection()
            # Pool is at capacity: wait up to timeout
            try:
                return self._pool.get(block=True, timeout=self.timeout)
            except queue.Empty:
                raise TimeoutError(f"Connection pool exhausted (max={self.max_size}, timeout={self.timeout}s)")

    def release(self, conn: MockDBConnection):
        """Returns a healthy connection back to the pool."""
        if conn.is_closed:
            self.allocated_count -= 1
            return
        try:
            self._pool.put_nowait(conn)
        except queue.Full:
            conn.close()
            self.allocated_count -= 1

    def close_all(self):
        """Closes all connections in the pool."""
        while not self._pool.empty():
            conn = self._pool.get_nowait()
            conn.close()
        self.allocated_count = 0
