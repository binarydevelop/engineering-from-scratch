import pytest
import importlib.util
from pathlib import Path

def test_phase_190_execution():
    code_path = Path(__file__).resolve().parent.parent / "code" / "main.py"
    spec = importlib.util.spec_from_file_location("phase_190_mod", code_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    res = mod.execute_phase()
    assert res["status"] == "SUCCESS"
    assert res["records_processed"] == 10
    assert res["aggregated_total"] == 550
