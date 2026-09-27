"""
Tests for Project: URL Shortener Service
"""

import pytest
import os
import sys
import importlib.util

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(os.path.dirname(PROJ_DIR), "app", "main.py")

spec = importlib.util.spec_from_file_location("proj_01_url_shortener", APP_FILE)
proj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proj)

globals().update({k: getattr(proj, k) for k in dir(proj) if not k.startswith("__")})

def test_shorten_and_resolve():
    shortener = URLShortener()
    code = shortener.shorten("https://google.com")
    assert len(code) > 0
    resolved = shortener.resolve(code)
    assert resolved == "https://google.com"
    assert shortener.db[code]["clicks"] == 1
