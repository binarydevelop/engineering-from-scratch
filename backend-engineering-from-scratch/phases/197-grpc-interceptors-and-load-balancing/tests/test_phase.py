"""
Tests for Lesson 197: gRPC Interceptors and Load Balancing.
"""
import pytest
import os
import sys
import importlib.util

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_FILE = os.path.join(os.path.dirname(CURRENT_DIR), "code", "main.py")
mod_name = os.path.basename(os.path.dirname(CURRENT_DIR)).replace("-", "_")

spec = importlib.util.spec_from_file_location(mod_name, CODE_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
globals().update({k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")})

def test_component_initialization():
    comp = PhaseComponent()
    assert comp.name == "gRPC Interceptors and Load Balancing"
    telemetry = comp.get_telemetry()
    assert telemetry["component"] == "gRPC Interceptors and Load Balancing"

def test_component_happy_path():
    comp = PhaseComponent()
    res = comp.process({"sample": "data"})
    assert res["status"] == "success"
    assert res["phase"] == 197

def test_component_error_handling():
    comp = PhaseComponent()
    with pytest.raises(ValueError):
        comp.process("invalid_type")  # type: ignore

def test_component_simulated_fault():
    comp = PhaseComponent()
    with pytest.raises(RuntimeError):
        comp.process({"trigger_error": True})
