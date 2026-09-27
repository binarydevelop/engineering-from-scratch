"""
Tests for Project: Authentication Microservice
"""

import pytest
import os
import sys
import importlib.util

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(PROJ_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("proj_13_authentication_service", APP_FILE)
proj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj)

globals().update({k: getattr(proj, k) for k in dir(proj) if not k.startswith("__")})

def test_auth_login_and_refresh_rotation():
    svc = AuthService()
    svc.register("alice@test.com", "hashed_pwd")
    tokens = svc.login("alice@test.com")
    
    new_tokens = svc.rotate_refresh(tokens["refresh_token"])
    assert new_tokens["refresh_token"] != tokens["refresh_token"]

    import pytest
    with pytest.raises(PermissionError):
        svc.rotate_refresh(tokens["refresh_token"])  # Reuse detected
