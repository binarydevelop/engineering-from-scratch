"""
Pytest verification test for Phase 46: Partitioning Data.
"""

import pytest
import os
import importlib.util

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_FILE = os.path.join(os.path.dirname(TEST_DIR), "code", "main.py")

spec = importlib.util.spec_from_file_location("phase_46_46_partitioning_data", CODE_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
globals().update({k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")})

def test_phase_initialization():
    sys = PhaseSystem()
    assert sys.phase_num == 46
    assert sys.metrics["requests_total"] == 0

def test_phase_happy_path():
    sys = PhaseSystem()
    res = sys.process_request({"key": "test_value"})
    assert res["status"] == "SUCCESS"
    assert res["phase"] == 46
    assert sys.metrics["requests_total"] == 1
    assert sys.metrics["errors_total"] == 0

def test_phase_invalid_payload():
    sys = PhaseSystem()
    with pytest.raises(ValueError):
        sys.process_request("not_a_dictionary")  # type: ignore
    assert sys.metrics["errors_total"] == 1

def test_phase_chaos_failure():
    sys = PhaseSystem()
    sys.chaos_active = True
    with pytest.raises(RuntimeError):
        sys.process_request({"key": "val"})
    assert sys.metrics["errors_total"] == 1
