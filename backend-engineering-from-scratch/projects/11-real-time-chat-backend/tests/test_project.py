"""
Tests for Project: Real-Time Chat Backend
"""

import pytest
import os
import sys
import importlib.util

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(PROJ_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("proj_11_real_time_chat_backend", APP_FILE)
proj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj)

globals().update({k: getattr(proj, k) for k in dir(proj) if not k.startswith("__")})

def test_chat_room_broadcast():
    mgr = ChatRoomManager()
    mgr.join("general", "alice")
    mgr.join("general", "bob")
    
    recipients = mgr.broadcast("general", "alice", "Hello everyone!")
    assert recipients == 2
    assert len(mgr.history["general"]) == 1
