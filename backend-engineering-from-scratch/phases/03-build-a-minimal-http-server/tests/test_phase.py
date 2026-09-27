"""
Test suite for Lesson 03: Build a Minimal HTTP Server.
Uses an HTTP client to verify raw HTTP responses.
"""

import httpx
import pytest
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

def test_minimal_http_server_get():
    server = MinimalHTTPServer()
    port = server.start()
    try:
        url = f"http://127.0.0.1:{port}/hello"
        resp = httpx.get(url, timeout=2.0)
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "text/plain"
        assert resp.text == "hello from first principles"
    finally:
        server.stop()

def test_minimal_http_server_json():
    server = MinimalHTTPServer()
    port = server.start()
    try:
        url = f"http://127.0.0.1:{port}/json"
        resp = httpx.get(url, timeout=2.0)
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "application/json"
        data = resp.json()
        assert data["status"] == "ok"
    finally:
        server.stop()

def test_minimal_http_server_not_found():
    server = MinimalHTTPServer()
    port = server.start()
    try:
        url = f"http://127.0.0.1:{port}/nonexistent"
        resp = httpx.get(url, timeout=2.0)
        assert resp.status_code == 404
    finally:
        server.stop()
