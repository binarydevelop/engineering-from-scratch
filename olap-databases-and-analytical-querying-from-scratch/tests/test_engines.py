import pytest
import os
import sys
import importlib.util
from pathlib import Path
import duckdb

REPO_ROOT = Path(__file__).resolve().parent.parent

def load_module_from_path(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod

tiny_col_mod = load_module_from_path(
    "tiny_col_store",
    REPO_ROOT / "projects" / "project-09-tiny-column-store" / "engine.py"
)
TinyColumnStore = tiny_col_mod.TinyColumnStore

tiny_vec_mod = load_module_from_path(
    "tiny_vec_engine",
    REPO_ROOT / "projects" / "project-10-tiny-vectorized-engine" / "engine.py"
)
PhysicalVectorScan = tiny_vec_mod.PhysicalVectorScan
PhysicalVectorFilter = tiny_vec_mod.PhysicalVectorFilter
PhysicalVectorHashAggregate = tiny_vec_mod.PhysicalVectorHashAggregate

def test_tiny_column_store(tmp_path):
    store = TinyColumnStore(tmp_path / "test_store")
    data = {
        "created_at": [100, 200, 300, 400, 500, 600, 700, 800],
        "country": ["US", "DE", "US", "DE", "FR", "FR", "IN", "IN"],
        "revenue": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0]
    }
    store.write_table(data)
    
    # Query with zone map pruning
    res, scanned, skipped = store.query(
        select_cols=["country", "revenue"],
        where_col="created_at",
        where_op=">=",
        where_val=300,
        group_by_col="country",
        agg_col="revenue"
    )
    
    assert "US" in res
    assert res["US"][0] == 1 # 1 row >= 300 (which is 300)
    assert res["US"][1] == 30.0

def test_tiny_vectorized_engine():
    data = {
        "country": ["US", "DE", "US", "DE", "FR"],
        "latency": [10, 50, 20, 80, 15],
        "revenue": [100.0, 200.0, 300.0, 400.0, 500.0]
    }
    scan = PhysicalVectorScan(data)
    filt = PhysicalVectorFilter(scan, predicate_col="latency", op="<=", target_val=30)
    agg = PhysicalVectorHashAggregate(filt, group_col="country", agg_col="revenue")
    
    res = agg.execute()
    assert "US" in res
    assert res["US"][0] == 2
    assert res["US"][1] == 400.0
    assert "FR" in res
    assert res["FR"][0] == 1
    assert res["FR"][1] == 500.0
    assert "DE" not in res

def test_duckdb_lab_queries():
    db_file = REPO_ROOT / "outputs" / "olap_lab.duckdb"
    assert db_file.exists(), "olap_lab.duckdb not found. Run make data-small."
    con = duckdb.connect(str(db_file), read_only=True)
    
    # 1. Test Aggregation
    res_agg = con.execute("SELECT country, SUM(net_revenue) FROM fact_order_items GROUP BY country").fetchall()
    assert len(res_agg) == 6
    
    # 2. Test Window Function
    res_win = con.execute("""
        SELECT user_id, created_at, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at)
        FROM fact_order_items
        LIMIT 10
    """).fetchall()
    assert len(res_win) == 10
    
    # 3. Test Approx Quantile
    res_quant = con.execute("SELECT approx_quantile(latency_ms, 0.95) FROM service_logs").fetchone()
    assert res_quant[0] is not None
    assert res_quant[0] > 0
    
    con.close()
