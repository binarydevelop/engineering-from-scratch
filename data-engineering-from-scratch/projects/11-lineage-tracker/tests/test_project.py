import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_11_lineage_tracker", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

# imported above: LineageTracker

def test_lineage():
    lt = LineageTracker()
    lt.register(["raw_orders", "raw_users"], "fact_orders")
    assert "raw_orders" in lt.trace_upstream("fact_orders")

