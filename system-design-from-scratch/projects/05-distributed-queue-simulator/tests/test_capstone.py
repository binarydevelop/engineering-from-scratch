"""
Test suite for Capstone 05: Distributed Queue Simulator.
"""

import pytest
import os
import importlib.util

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(TEST_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("cap_05_distributed_queue_simulator", APP_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
globals().update({k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")})

def test_partitioned_queue_and_dlq():
    broker = PartitionedQueueBroker(num_partitions=2, max_retries=1)
    broker.publish("order_99", {"amount": 200})

    # Find which partition has the message
    msg = broker.consume(0, visibility_timeout_sec=0.05) or broker.consume(1, visibility_timeout_sec=0.05)
    assert msg is not None
    assert msg["key"] == "order_99"

    # Sleep and re-consume exceeding max retries -> goes to DLQ
    time.sleep(0.06)
    _ = broker.consume(0) or broker.consume(1)
    assert len(broker.dlq) == 1
