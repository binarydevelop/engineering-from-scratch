import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_01_ecommerce_batch_pipeline", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

import pytest
from pathlib import Path
# imported above: run_pipeline

def test_ecommerce_batch(tmp_path):
    csv_file = tmp_path / "orders.csv"
    csv_file.write_text("order_id,user_id,total_amount,created_at\nord_1,u1,100.0,2026-09-01 10:00:00\n")
    db_file = tmp_path / "test.duckdb"
    res = run_pipeline(csv_file, db_file)
    assert res == 1

