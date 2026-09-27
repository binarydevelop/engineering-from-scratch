import pytest
import importlib.util
from pathlib import Path

def test_fixed_implementation():
    mod_path = Path(__file__).resolve().parent / "solution" / "fixed_pipeline.py"
    spec = importlib.util.spec_from_file_location("sol_lab_18_scd2_overlapping_effective_dates", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Inject solution symbols into globals
    for k, v in vars(mod).items():
        if not k.startswith("__"):
            globals()[k] = v

    rec = [{'user_id': 'u1', 'is_current': True, 'valid_from': '2026-01-01'}]; update_scd2_fixed(rec, {'user_id': 'u1', 'is_current': True, 'valid_from': '2026-09-01'}); assert len(rec) == 2 and not rec[0]['is_current'] and rec[0]['valid_to'] == '2026-09-01'
