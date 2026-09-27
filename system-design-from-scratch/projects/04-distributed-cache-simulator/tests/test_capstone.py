"""
Test suite for Capstone 04: Distributed Cache Simulator.
"""

import pytest
import os
import importlib.util

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(TEST_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("cap_04_distributed_cache_simulator", APP_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
globals().update({k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")})

def test_distributed_cache_cluster():
    cluster = DistributedCacheCluster()
    cluster.add_node("cache_A")
    cluster.add_node("cache_B")

    cluster.put("user:101", {"name": "Alice"})
    val = cluster.get("user:101")
    assert val == {"name": "Alice"}
