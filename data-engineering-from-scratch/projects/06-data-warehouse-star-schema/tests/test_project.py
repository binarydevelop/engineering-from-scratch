import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_06_data_warehouse_star_schema", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

import duckdb
# imported above: build_star_schema

def test_star_schema():
    con = duckdb.connect(":memory:")
    res = build_star_schema(con)
    assert res[0] == ("VIP", 150.0)

