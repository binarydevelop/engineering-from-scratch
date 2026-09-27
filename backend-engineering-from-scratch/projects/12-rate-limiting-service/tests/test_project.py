"""
Tests for Project: Rate Limiting Service
"""

import pytest
import os
import sys
import importlib.util

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(PROJ_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("proj_12_rate_limiting_service", APP_FILE)
proj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj)

globals().update({k: getattr(proj, k) for k in dir(proj) if not k.startswith("__")})

def test_token_bucket_rate_limiter():
    limiter = TokenBucketLimiter(capacity=2, refill_rate_per_sec=1.0)
    assert limiter.allow_request() is True
    assert limiter.allow_request() is True
    # Out of tokens
    assert limiter.allow_request() is False
