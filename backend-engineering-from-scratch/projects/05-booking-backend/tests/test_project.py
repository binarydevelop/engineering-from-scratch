"""
Tests for Project: Reservation Booking Engine
"""

import pytest
import os
import sys
import importlib.util

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(PROJ_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("proj_05_booking_backend", APP_FILE)
proj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj)

globals().update({k: getattr(proj, k) for k in dir(proj) if not k.startswith("__")})

def test_booking_hold_and_confirm():
    engine = BookingEngine(hold_ttl_seconds=1.0)
    assert engine.hold_slot("slot_10", "alice") is True
    # Bob cannot hold while Alice holds
    assert engine.hold_slot("slot_10", "bob") is False
    # Alice confirms
    assert engine.confirm_booking("slot_10", "alice") is True
