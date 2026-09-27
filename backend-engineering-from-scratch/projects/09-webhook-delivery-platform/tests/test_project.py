"""
Tests for Project: Webhook Delivery Platform
"""

import pytest
import os
import sys
import importlib.util

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(PROJ_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("proj_09_webhook_delivery_platform", APP_FILE)
proj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj)

globals().update({k: getattr(proj, k) for k in dir(proj) if not k.startswith("__")})

def test_webhook_delivery_signing():
    platform = WebhookPlatform(secret="secure_secret")
    body = '{"order_id": 42}'
    res = platform.deliver("https://client.com/webhook", body)
    assert res["status"] == "DELIVERED"
    assert len(res["signature"]) == 64
