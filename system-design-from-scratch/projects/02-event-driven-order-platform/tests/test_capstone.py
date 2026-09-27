"""
Test suite for Capstone 02: Event-Driven Order Platform.
"""

import pytest
import os
import importlib.util

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(TEST_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("cap_02_event_driven_order_platform", APP_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
globals().update({k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")})

def test_order_and_outbox_transaction():
    platform = OrderPlatform()
    order = platform.place_order("item_1", 2)
    assert order["status"] == "CONFIRMED"

    # Outbox worker dispatches event
    dispatched = platform.outbox_worker()
    assert dispatched == 1
    assert len(platform.dispatched_events) == 1

    # Invariant: inventory decremented
    cur = platform.conn.cursor()
    cur.execute("SELECT stock FROM inventory WHERE item_id = 'item_1'")
    assert cur.fetchone()["stock"] == 8
