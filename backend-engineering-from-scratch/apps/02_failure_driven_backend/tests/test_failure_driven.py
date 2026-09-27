"""
Failure injection and resilience tests for Capstone 02: Failure-Driven Backend.
"""

import os
import sys
import time
import pytest

APP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from system import ResilientBackendSystem

def test_cache_failure_graceful_degradation():
    backend = ResilientBackendSystem()

    # Inject Redis/cache drop
    backend.chaos.drop_cache = True

    # System must degrade gracefully by falling back to primary DB
    code, data = backend.get_product("prod_1")
    assert code == 200
    assert data["name"] == "High Availability Server"
    assert backend.cache_manager.cache_faults == 1

def test_circuit_breaker_trip_and_fast_fail():
    backend = ResilientBackendSystem()

    # Drop database
    backend.chaos.drop_db = True

    # 1st failure
    code1, _ = backend.get_product("prod_1")
    assert code1 == 503

    # 2nd failure -> reaches threshold (2)
    code2, _ = backend.get_product("prod_1")
    assert code2 == 503
    assert backend.circuit_breaker.state == "OPEN"

    # 3rd request should fast-fail without touching DB
    code3, res3 = backend.get_product("prod_1")
    assert code3 == 503
    assert res3["code"] == "FAST_FAIL"

def test_circuit_breaker_recovery():
    backend = ResilientBackendSystem()
    backend.chaos.drop_db = True

    # Trip breaker
    backend.get_product("prod_1")
    backend.get_product("prod_1")
    assert backend.circuit_breaker.state == "OPEN"

    # Wait for recovery timeout (0.2s)
    time.sleep(0.25)

    # Heal database
    backend.chaos.drop_db = False

    # Next request tests half-open and restores CLOSED state
    code, data = backend.get_product("prod_1")
    assert code == 200
    assert backend.circuit_breaker.state == "CLOSED"

def test_database_timeout_deadline():
    backend = ResilientBackendSystem()
    backend.chaos.timeout_db = True

    code, res = backend.get_product("prod_1")
    assert code == 504
    assert res["code"] == "DB_TIMEOUT"
