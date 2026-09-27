import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_05_lakehouse_table_format", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

# imported above: LakehouseTable

def test_lakehouse_snapshot():
    t = LakehouseTable()
    s1 = t.commit(["f1.parquet"], {"id": "int"})
    s2 = t.commit(["f1.parquet", "f2.parquet"], {"id": "int", "name": "str"})
    assert len(t.time_travel(s1)["files"]) == 1
    assert len(t.time_travel(s2)["files"]) == 2

