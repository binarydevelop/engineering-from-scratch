"""
Test suite for Lesson 09: Routing From Scratch.
"""

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

def test_static_routing():
    router = Router()
    router.add("GET", "/users", lambda p: ["alice", "bob"])
    
    status, result, params = router.dispatch("GET", "/users")
    assert status == 200
    assert result == ["alice", "bob"]
    assert params == {}

def test_dynamic_parameter_routing():
    router = Router()
    router.add("GET", "/users/{id}", lambda p: {"user_id": p["id"]})
    router.add("GET", "/users/{id}/orders/{order_id}", lambda p: {"uid": p["id"], "oid": p["order_id"]})

    status, result, params = router.dispatch("GET", "/users/42")
    assert status == 200
    assert result == {"user_id": "42"}
    assert params == {"id": "42"}

    status, result, params = router.dispatch("GET", "/users/42/orders/999")
    assert status == 200
    assert result == {"uid": "42", "oid": "999"}

def test_method_not_allowed_405():
    router = Router()
    router.add("GET", "/users", lambda p: [])
    
    status, result, _ = router.dispatch("POST", "/users")
    assert status == 405
    assert result["error"] == "Method Not Allowed"

def test_not_found_404():
    router = Router()
    router.add("GET", "/users", lambda p: [])
    
    status, result, _ = router.dispatch("GET", "/unknown")
    assert status == 404
    assert result["error"] == "Not Found"
