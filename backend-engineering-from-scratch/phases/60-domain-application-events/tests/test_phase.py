"""
Tests for Lesson 60: Domain/Application Events.
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

def test_component_initialization():
    """Verifies component initializes with valid state."""
    comp = PhaseComponent()
    assert comp.name == "Domain/Application Events"
    assert comp.state["phase"] == 60
    assert comp.state["initialized"] is True

def test_component_happy_path():
    """Verifies successful payload processing."""
    comp = PhaseComponent()
    payload = {"key": "value", "id": 123}
    res = comp.process(payload)
    assert res["status"] == "success"
    assert res["phase"] == 60
    assert res["data"] == payload
    assert comp.metrics["operations_total"] == 1
    assert comp.metrics["errors_total"] == 0

def test_component_error_handling():
    """Verifies failure handling and error metric tracking."""
    comp = PhaseComponent()
    with pytest.raises(ValueError):
        comp.process("invalid_type")  # type: ignore
    
    assert comp.metrics["errors_total"] == 1

def test_component_simulated_fault():
    """Verifies fault injection error handling."""
    comp = PhaseComponent()
    with pytest.raises(RuntimeError):
        comp.process({"trigger_error": True})
    
    assert comp.metrics["errors_total"] == 1
