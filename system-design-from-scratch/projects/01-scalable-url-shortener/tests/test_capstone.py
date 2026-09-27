"""
Test suite for Capstone 01: Scalable URL Shortener.
"""

import pytest
import os
import importlib.util

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(TEST_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("cap_01_scalable_url_shortener", APP_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
globals().update({k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")})

def test_url_shortener_flow():
    svc = URLShortenerService()
    code = svc.shorten("https://example.com/long-page")
    assert len(code) > 0

    # Resolve from cache
    url = svc.resolve(code)
    assert url == "https://example.com/long-page"

    # Async worker processes click telemetry
    processed = svc.process_clicks_worker()
    assert processed == 1
    assert svc.db[code]["clicks"] == 1
