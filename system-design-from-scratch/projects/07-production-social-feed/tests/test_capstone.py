"""
Test suite for Capstone 07: Production-Like Social Feed.
"""

import pytest
import os
import importlib.util

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(TEST_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("cap_07_production_social_feed", APP_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
globals().update({k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")})

def test_social_feed_hybrid_fanout():
    feed_app = SocialFeedPlatform(celebrity_threshold=3)

    # Bob is a celebrity with 4 followers
    for i in range(4):
        feed_app.follow(f"user_{i}", "bob")

    # Alice is a regular user with 1 follower
    feed_app.follow("user_0", "alice")

    feed_app.post("alice", "alice_post_1")
    feed_app.post("bob", "bob_post_1")

    # user_0 follows both Alice and Bob -> feed contains both
    u0_feed = feed_app.get_feed("user_0")
    assert "alice_post_1" in u0_feed
    assert "bob_post_1" in u0_feed
