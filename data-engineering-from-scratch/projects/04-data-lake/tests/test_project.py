import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_04_data_lake", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

# imported above: stage_lake_partition

def test_data_lake_partition(tmp_path):
    p = stage_lake_partition(tmp_path, "raw", "2026-09-01", "part-0.txt", "data")
    assert p.exists() and "date=2026-09-01" in str(p)

