"""
Test suite for Lesson 37: Token-Based Authentication.
"""

import pytest
import time
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_FILE = os.path.join(os.path.dirname(CURRENT_DIR), "code", "main.py")
mod_name = os.path.basename(os.path.dirname(CURRENT_DIR)).replace("-", "_")

import importlib.util
spec = importlib.util.spec_from_file_location(mod_name, CODE_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
globals().update({k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")})

# 32+ byte high-entropy keys conforming to RFC 7518 Sec 3.2
KEY_A = "a-very-long-secret-key-that-exceeds-thirty-two-bytes-minimum!"
KEY_B = "another-independent-secret-key-exceeding-thirty-two-bytes-!"

def test_token_issue_and_verify():
    service = TokenService(secret_key=KEY_A, token_ttl_seconds=60)
    token = service.issue_token(subject="user_123", claims={"role": "admin"})

    claims = service.verify_token(token)
    assert claims["sub"] == "user_123"
    assert claims["role"] == "admin"
    assert "exp" in claims

def test_token_tampered_signature_rejected():
    service = TokenService(secret_key=KEY_A)
    token = service.issue_token(subject="user_123")

    # Verify with different key
    wrong_service = TokenService(secret_key=KEY_B)
    with pytest.raises(PermissionError):
        wrong_service.verify_token(token)

def test_token_expiration():
    service = TokenService(secret_key=KEY_A, token_ttl_seconds=-1)
    token = service.issue_token(subject="user_123")

    with pytest.raises(PermissionError) as exc_info:
        service.verify_token(token)
    assert "expired" in str(exc_info.value).lower()
