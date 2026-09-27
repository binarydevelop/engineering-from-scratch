import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_02_clickstream_pipeline", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

# imported above: compute_funnel

def test_clickstream_funnel():
    events = [
        {"user_id": "u1", "action": "page_view"},
        {"user_id": "u1", "action": "add_to_cart"},
        {"user_id": "u1", "action": "purchase"},
        {"user_id": "u2", "action": "page_view"}
    ]
    counts = compute_funnel(events)
    assert counts["page_view"] == 2 and counts["purchase"] == 1

