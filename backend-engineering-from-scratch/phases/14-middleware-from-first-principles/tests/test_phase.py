"""
Test suite for Lesson 14: Middleware From First Principles.
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

def test_middleware_execution_order():
    trace = []

    def mw_outer(req, next_handler):
        trace.append("outer_before")
        resp = next_handler(req)
        trace.append("outer_after")
        resp["outer"] = True
        return resp

    def mw_inner(req, next_handler):
        trace.append("inner_before")
        resp = next_handler(req)
        trace.append("inner_after")
        resp["inner"] = True
        return resp

    def core_handler(req):
        trace.append("core_handler")
        return {"status": 200, "user": req.get("user")}

    pipeline = MiddlewarePipeline(core_handler)
    pipeline.use(mw_outer)
    pipeline.use(mw_inner)

    response = pipeline.execute({"user": "alice"})

    assert trace == [
        "outer_before",
        "inner_before",
        "core_handler",
        "inner_after",
        "outer_after"
    ]
    assert response["status"] == 200
    assert response["outer"] is True
    assert response["inner"] is True

def test_middleware_short_circuit():
    trace = []

    def auth_mw(req, next_handler):
        if not req.get("token"):
            trace.append("auth_rejected")
            return {"status": 401, "error": "Unauthorized"}
        return next_handler(req)

    def core_handler(req):
        trace.append("core_handler")
        return {"status": 200}

    pipeline = MiddlewarePipeline(core_handler)
    pipeline.use(auth_mw)

    resp = pipeline.execute({})
    assert resp["status"] == 401
    assert trace == ["auth_rejected"]
