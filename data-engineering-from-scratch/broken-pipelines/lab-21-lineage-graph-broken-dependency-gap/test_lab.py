import pytest
import importlib.util
from pathlib import Path

def test_fixed_implementation():
    mod_path = Path(__file__).resolve().parent / "solution" / "fixed_pipeline.py"
    spec = importlib.util.spec_from_file_location("sol_lab_21_lineage_graph_broken_dependency_gap", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Inject solution symbols into globals
    for k, v in vars(mod).items():
        if not k.startswith("__"):
            globals()[k] = v

    reg = {}; record_lineage(reg, 'raw_orders', 'stg_orders'); assert 'raw_orders' in reg['stg_orders']
