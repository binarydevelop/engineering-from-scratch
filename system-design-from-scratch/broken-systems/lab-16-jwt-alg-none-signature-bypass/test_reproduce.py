"""
Reproduction and verification test for: JWT Alg=None Signature Bypass
"""

import pytest
import os
import importlib.util

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
BROKEN_FILE = os.path.join(LAB_DIR, "broken", "main.py")
FIXED_FILE = os.path.join(LAB_DIR, "fixed", "main.py")

def _load_module(filepath: str, name: str):
    spec = importlib.util.spec_from_file_location(name, filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_broken_reproduces_failure():
    broken_mod = _load_module(BROKEN_FILE, "broken_lab_16_jwt_alg_none_signature_bypass")
    subsystem = broken_mod.Subsystem()
    
    with pytest.raises(RuntimeError) as exc_info:
        subsystem.execute({"induce_failure": True})
    assert "Defect triggered" in str(exc_info.value)

def test_fixed_resolves_defect():
    fixed_mod = _load_module(FIXED_FILE, "fixed_lab_16_jwt_alg_none_signature_bypass")
    subsystem = fixed_mod.Subsystem()
    
    response = subsystem.execute({"induce_failure": True, "data": "valid"})
    assert response["status"] == "success"
    assert response["fixed"] is True
    assert "result" in response
