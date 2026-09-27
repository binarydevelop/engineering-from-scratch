"""
Test suite for Capstone 03: Real-Time Chat Platform.
"""

import pytest
import os
import importlib.util

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(TEST_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("cap_03_real_time_chat", APP_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
globals().update({k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")})

def test_chat_room_and_presence():
    chat = RealTimeChatPlatform()
    chat.join_room("general", "alice")
    chat.join_room("general", "bob")

    msg = chat.send_message("general", "alice", "Hello Bob!")
    assert msg["sender"] == "alice"
    assert len(chat.history["general"]) == 1
    assert chat.is_user_online("alice") is True
