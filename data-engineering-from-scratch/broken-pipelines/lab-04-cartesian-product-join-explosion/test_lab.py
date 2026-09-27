import pytest
import importlib.util
from pathlib import Path

def test_fixed_implementation():
    mod_path = Path(__file__).resolve().parent / "solution" / "fixed_pipeline.py"
    spec = importlib.util.spec_from_file_location("sol_lab_04_cartesian_product_join_explosion", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Inject solution symbols into globals
    for k, v in vars(mod).items():
        if not k.startswith("__"):
            globals()[k] = v

    orders = [{'id': 1, 'user_id': 'u1'}]; users = [{'user_id': 'u1', 'name': 'Old', 'is_current': False}, {'user_id': 'u1', 'name': 'New', 'is_current': True}]; res = join_orders_users(orders, users); assert len(res) == 1 and res[0]['user_name'] == 'New'
