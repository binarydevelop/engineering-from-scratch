import pytest
import importlib.util
from pathlib import Path

def test_fixed_implementation():
    mod_path = Path(__file__).resolve().parent / "solution" / "fixed_pipeline.py"
    spec = importlib.util.spec_from_file_location("sol_lab_19_poison_record_crashing_entire_batch", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Inject solution symbols into globals
    for k, v in vars(mod).items():
        if not k.startswith("__"):
            globals()[k] = v

    v, q = process_batch_quarantine(['{"a": 1}', 'BAD_JSON']); assert len(v) == 1 and len(q) == 1
