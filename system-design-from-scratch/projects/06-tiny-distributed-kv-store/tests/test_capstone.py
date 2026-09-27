"""
Test suite for Capstone 06: Tiny Distributed KV Store.
"""

import pytest
import os
import importlib.util

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(TEST_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("cap_06_tiny_distributed_kv_store", APP_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
globals().update({k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")})

def test_quorum_write_and_read():
    cluster = TinyKVCluster()
    # Write with W=2 quorum
    assert cluster.write_quorum("config:timeout", 500, w=2) is True
    # Read with R=2 quorum
    val = cluster.read_quorum("config:timeout", r=2)
    assert val == 500

    # Node failure: 1 node dies
    cluster.nodes[2].alive = False
    # Write still succeeds because 2 nodes remain alive (W=2)
    assert cluster.write_quorum("config:retries", 3, w=2) is True
    assert cluster.read_quorum("config:retries", r=2) == 3
