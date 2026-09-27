import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_07_dbt_analytics_project", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

# imported above: compile_model

def test_dbt_ref_compiler():
    sql = "SELECT * FROM ref('stg_orders') WHERE amount > 0;"
    manifest = {"stg_orders": "analytics.staging.stg_orders"}
    compiled = compile_model(sql, manifest)
    assert "analytics.staging.stg_orders" in compiled

