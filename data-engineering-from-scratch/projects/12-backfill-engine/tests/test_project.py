import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_12_backfill_engine", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

# imported above: backfill_partition

def test_backfill():
    store = [{"date": "2026-09-01", "v": 1}, {"date": "2026-09-02", "v": 2}]
    backfill_partition(store, "2026-09-01", [{"date": "2026-09-01", "v": 99}])
    assert len(store) == 2 and [r["v"] for r in store if r["date"] == "2026-09-01"] == [99]

