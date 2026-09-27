import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_14_reconciliation_system", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

# imported above: reconcile

def test_reconciliation():
    ok, diff = reconcile(100.50, 100.505)
    assert ok
    ok, diff = reconcile(100.50, 105.00)
    assert not ok

