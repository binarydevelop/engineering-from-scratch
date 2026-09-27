import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_16_slowly_changing_dimensions_scd2", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

# imported above: apply_scd2

def test_scd2():
    dim = [{"natural_key": "u1", "tier": "STANDARD", "is_current": True, "valid_from": "2026-01-01", "valid_to": None}]
    apply_scd2(dim, "u1", {"tier": "VIP"}, "2026-09-01")
    assert len(dim) == 2 and not dim[0]["is_current"] and dim[1]["tier"] == "VIP"

