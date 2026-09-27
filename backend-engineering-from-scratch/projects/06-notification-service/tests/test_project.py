"""
Tests for Project: Notification Microservice
"""

import pytest
import os
import sys
import importlib.util

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(PROJ_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("proj_06_notification_service", APP_FILE)
proj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj)

globals().update({k: getattr(proj, k) for k in dir(proj) if not k.startswith("__")})

def test_notification_failover():
    svc = NotificationService()
    res1 = svc.send("user@test.com", "Welcome!")
    assert res1["provider"] == "PrimaryProvider_SES"

    svc.primary_online = False
    res2 = svc.send("user@test.com", "Backup notice")
    assert res2["provider"] == "BackupProvider_SendGrid"
