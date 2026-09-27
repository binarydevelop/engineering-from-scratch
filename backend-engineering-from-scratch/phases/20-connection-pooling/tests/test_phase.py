"""
Test suite for Lesson 20: Connection Pooling.
"""

import pytest
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_FILE = os.path.join(os.path.dirname(CURRENT_DIR), "code", "main.py")
mod_name = os.path.basename(os.path.dirname(CURRENT_DIR)).replace("-", "_")

import importlib.util
spec = importlib.util.spec_from_file_location(mod_name, CODE_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
globals().update({k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")})

def test_connection_pool_acquisition_and_reuse():
    # min_size=1 so the single connection is reused across sequential acquires
    pool = ConnectionPool(min_size=1, max_size=2)
    conn1 = pool.acquire()
    conn_id = conn1.conn_id
    conn1.execute("SELECT 1")
    
    # Return to pool
    pool.release(conn1)

    # Acquire again: should be the exact same connection object
    conn2 = pool.acquire()
    assert conn2.conn_id == conn_id
    assert conn2.queries_executed == 1
    pool.release(conn2)
    pool.close_all()

def test_connection_pool_exhaustion_timeout():
    pool = ConnectionPool(min_size=1, max_size=2, timeout=0.1)
    c1 = pool.acquire()
    c2 = pool.acquire()
    
    # Pool is now fully checked out (2 of 2)
    with pytest.raises(TimeoutError) as exc_info:
        pool.acquire()
    
    assert "Connection pool exhausted" in str(exc_info.value)
    
    pool.release(c1)
    pool.release(c2)
    pool.close_all()
