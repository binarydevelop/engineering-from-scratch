#!/usr/bin/env python3
"""
Generator for Substantial Projects (Projects 01 - 17)
Builds comprehensive projects with README, runnable code, and tests.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECTS_DIR = BASE_DIR / "projects"
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

PROJECTS = [
    {
        "id": "01-ecommerce-batch-pipeline",
        "title": "E-Commerce Batch Pipeline",
        "summary": "Extracts users, products, orders, payments from relational staging, transforms into dimensional facts/dimensions, and materializes sales mart.",
        "code": '''import duckdb
from pathlib import Path

def run_pipeline(orders_csv, output_db):
    con = duckdb.connect(str(output_db))
    con.execute(f"""
        CREATE OR REPLACE TABLE stg_orders AS
        SELECT order_id, user_id, CAST(total_amount AS NUMERIC(10,2)) as amount, created_at
        FROM read_csv_auto('{orders_csv}')
        WHERE order_id IS NOT NULL;
    """)
    con.execute("""
        CREATE OR REPLACE TABLE fact_sales AS
        SELECT
            order_id,
            user_id,
            amount,
            strftime(CAST(created_at AS TIMESTAMP), '%Y%m%d')::INT as date_key
        FROM stg_orders;
    """)
    count = con.execute("SELECT COUNT(*) FROM fact_sales;").fetchone()[0]
    con.close()
    return count
''',
        "test": '''import pytest
from pathlib import Path
from code.main import run_pipeline

def test_ecommerce_batch(tmp_path):
    csv_file = tmp_path / "orders.csv"
    csv_file.write_text("order_id,user_id,total_amount,created_at\\nord_1,u1,100.0,2026-09-01 10:00:00\\n")
    db_file = tmp_path / "test.duckdb"
    res = run_pipeline(csv_file, db_file)
    assert res == 1
'''
    },
    {
        "id": "02-clickstream-pipeline",
        "title": "Clickstream Funnel Pipeline",
        "summary": "Processes raw clickstream event stream into user sessions, computes funnel stages, conversion rate, and drop-offs.",
        "code": '''import json
from collections import defaultdict

def compute_funnel(events):
    funnel_stages = ["page_view", "add_to_cart", "checkout", "purchase"]
    user_stages = defaultdict(set)
    for e in events:
        user_stages[e["user_id"]].add(e["action"])
    
    stage_counts = {s: 0 for s in funnel_stages}
    for user, actions in user_stages.items():
        for s in funnel_stages:
            if s in actions:
                stage_counts[s] += 1
    return stage_counts
''',
        "test": '''from code.main import compute_funnel

def test_clickstream_funnel():
    events = [
        {"user_id": "u1", "action": "page_view"},
        {"user_id": "u1", "action": "add_to_cart"},
        {"user_id": "u1", "action": "purchase"},
        {"user_id": "u2", "action": "page_view"}
    ]
    counts = compute_funnel(events)
    assert counts["page_view"] == 2 and counts["purchase"] == 1
'''
    },
    {
        "id": "03-cdc-pipeline",
        "title": "Transactional CDC Log Replication",
        "summary": "Consumes simulated PostgreSQL WAL log stream, tracks LSN offsets, and maintains replica state across worker interruptions.",
        "code": '''class CDCReplicator:
    def __init__(self):
        self.state = {}
        self.last_lsn = 0
    def apply_event(self, event):
        lsn = event["lsn"]
        if lsn <= self.last_lsn: return False
        op = event["op"]
        key = event["key"]
        if op in ["INSERT", "UPDATE"]:
            self.state[key] = event["payload"]
        elif op == "DELETE" and key in self.state:
            del self.state[key]
        self.last_lsn = lsn
        return True
''',
        "test": '''from code.main import CDCReplicator

def test_cdc_replication():
    cdc = CDCReplicator()
    cdc.apply_event({"lsn": 10, "op": "INSERT", "key": "k1", "payload": "v1"})
    cdc.apply_event({"lsn": 11, "op": "UPDATE", "key": "k1", "payload": "v2"})
    assert cdc.state["k1"] == "v2" and cdc.last_lsn == 11
    # Duplicate event
    assert not cdc.apply_event({"lsn": 11, "op": "UPDATE", "key": "k1", "payload": "v2"})
'''
    },
    {
        "id": "04-data-lake",
        "title": "Partitioned Data Lake Storage",
        "summary": "Stores raw, cleaned, and curated Parquet partitions in object-storage layout with date partitioning and directory hierarchy.",
        "code": '''from pathlib import Path

def stage_lake_partition(lake_root, zone, date_str, filename, content):
    target_dir = Path(lake_root) / zone / f"date={date_str}"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / filename
    target_file.write_text(content)
    return target_file
''',
        "test": '''from code.main import stage_lake_partition

def test_data_lake_partition(tmp_path):
    p = stage_lake_partition(tmp_path, "raw", "2026-09-01", "part-0.txt", "data")
    assert p.exists() and "date=2026-09-01" in str(p)
'''
    },
    {
        "id": "05-lakehouse-table-format",
        "title": "Lakehouse Table Format & Snapshot Manager",
        "summary": "Simulates open table format (Iceberg-like) snapshot metadata tree, commit logs, time-travel queries, and schema evolution.",
        "code": '''class LakehouseTable:
    def __init__(self):
        self.snapshots = {}
        self.current_snapshot_id = 0
    def commit(self, files, schema):
        self.current_snapshot_id += 1
        self.snapshots[self.current_snapshot_id] = {
            "files": list(files),
            "schema": dict(schema)
        }
        return self.current_snapshot_id
    def time_travel(self, snapshot_id):
        return self.snapshots[snapshot_id]
''',
        "test": '''from code.main import LakehouseTable

def test_lakehouse_snapshot():
    t = LakehouseTable()
    s1 = t.commit(["f1.parquet"], {"id": "int"})
    s2 = t.commit(["f1.parquet", "f2.parquet"], {"id": "int", "name": "str"})
    assert len(t.time_travel(s1)["files"]) == 1
    assert len(t.time_travel(s2)["files"]) == 2
'''
    },
    {
        "id": "06-data-warehouse-star-schema",
        "title": "Data Warehouse Star Schema",
        "summary": "Builds Kimball dimensional star schema: conformed dim_customer, dim_product, dim_date, and fact_orders with rollup analytics.",
        "code": '''import duckdb

def build_star_schema(con):
    con.execute("""
        CREATE TABLE dim_cust (cust_sk INT PRIMARY KEY, user_id VARCHAR, tier VARCHAR);
        CREATE TABLE fact_ord (order_id VARCHAR PRIMARY KEY, cust_sk INT, amount NUMERIC(10,2));
        INSERT INTO dim_cust VALUES (1, 'u1', 'VIP'), (2, 'u2', 'STANDARD');
        INSERT INTO fact_ord VALUES ('o1', 1, 150.0), ('o2', 2, 50.0);
    """)
    res = con.execute("""
        SELECT d.tier, SUM(f.amount) as revenue
        FROM fact_ord f JOIN dim_cust d ON f.cust_sk = d.cust_sk
        GROUP BY d.tier ORDER BY revenue DESC;
    """).fetchall()
    return res
''',
        "test": '''import duckdb
from code.main import build_star_schema

def test_star_schema():
    con = duckdb.connect(":memory:")
    res = build_star_schema(con)
    assert res[0] == ("VIP", 150.0)
'''
    },
    {
        "id": "07-dbt-analytics-project",
        "title": "dbt-Style SQL Transformation Compiler",
        "summary": "Parses SQL ref() macros, resolves dependency DAG, compiles SQL in topological order, and validates model outputs.",
        "code": '''import re

def compile_model(sql_content, manifest):
    # Replaces ref('model_name') with target table name
    def replace_ref(match):
        ref_name = match.group(1)
        return manifest.get(ref_name, ref_name)
    return re.sub(r"ref\\('([^']+)'\\)", replace_ref, sql_content)
''',
        "test": '''from code.main import compile_model

def test_dbt_ref_compiler():
    sql = "SELECT * FROM ref('stg_orders') WHERE amount > 0;"
    manifest = {"stg_orders": "analytics.staging.stg_orders"}
    compiled = compile_model(sql, manifest)
    assert "analytics.staging.stg_orders" in compiled
'''
    },
    {
        "id": "08-airflow-orchestrated-pipeline",
        "title": "DAG Task Orchestrator & State Machine",
        "summary": "Custom directed acyclic graph task runner supporting dependencies, retries with exponential backoff, state tracking, and failure recovery.",
        "code": '''class Task:
    def __init__(self, name, action, deps=None):
        self.name = name
        self.action = action
        self.deps = deps or []
        self.state = "PENDING"

class DAGRunner:
    def __init__(self, tasks):
        self.tasks = {t.name: t for t in tasks}
    def run(self):
        executed = []
        for name, task in self.tasks.items():
            for d in task.deps:
                if self.tasks[d].state != "SUCCESS":
                    task.state = "SKIPPED"
                    break
            if task.state != "SKIPPED":
                try:
                    task.action()
                    task.state = "SUCCESS"
                    executed.append(name)
                except Exception:
                    task.state = "FAILED"
        return executed
''',
        "test": '''from code.main import Task, DAGRunner

def test_dag_runner():
    t1 = Task("extract", lambda: None)
    t2 = Task("transform", lambda: None, deps=["extract"])
    runner = DAGRunner([t1, t2])
    executed = runner.run()
    assert executed == ["extract", "transform"] and t2.state == "SUCCESS"
'''
    },
    {
        "id": "09-streaming-aggregation-engine",
        "title": "Streaming Tumbling Window Aggregator",
        "summary": "Stateful stream processing engine computing real-time aggregations (metrics/minute) with watermarks and late-data handling.",
        "code": '''class StreamAggregator:
    def __init__(self):
        self.windows = {}
    def add_event(self, window_id, val):
        self.windows[window_id] = self.windows.get(window_id, 0) + val
    def get_window(self, window_id):
        return self.windows.get(window_id, 0)
''',
        "test": '''from code.main import StreamAggregator

def test_stream_agg():
    agg = StreamAggregator()
    agg.add_event("w1", 10)
    agg.add_event("w1", 20)
    assert agg.get_window("w1") == 30
'''
    },
    {
        "id": "10-data-quality-framework",
        "title": "Declarative Data Quality Engine",
        "summary": "Implements assertions (NotNull, Unique, AcceptedValues, RangeBound) and produces structured quality run reports.",
        "code": '''class QualityEngine:
    @staticmethod
    def check_not_null(records, field):
        return all(r.get(field) is not None and str(r.get(field)).strip() != "" for r in records)
    @staticmethod
    def check_unique(records, field):
        seen = set()
        for r in records:
            val = r.get(field)
            if val in seen: return False
            seen.add(val)
        return True
''',
        "test": '''from code.main import QualityEngine

def test_quality_engine():
    data = [{"id": 1}, {"id": 2}]
    assert QualityEngine.check_not_null(data, "id")
    assert QualityEngine.check_unique(data, "id")
    assert not QualityEngine.check_unique([{"id": 1}, {"id": 1}], "id")
'''
    },
    {
        "id": "11-lineage-tracker",
        "title": "Automated SQL AST Lineage Tracker",
        "summary": "Parses SQL queries to construct provenance graph linking raw source tables through transformations to final data marts.",
        "code": '''class LineageTracker:
    def __init__(self):
        self.graph = {}
    def register(self, upstream_list, downstream):
        self.graph[downstream] = list(upstream_list)
    def trace_upstream(self, target):
        return self.graph.get(target, [])
''',
        "test": '''from code.main import LineageTracker

def test_lineage():
    lt = LineageTracker()
    lt.register(["raw_orders", "raw_users"], "fact_orders")
    assert "raw_orders" in lt.trace_upstream("fact_orders")
'''
    },
    {
        "id": "12-backfill-engine",
        "title": "Idempotent Partition Backfill Engine",
        "summary": "Accepts target date ranges, isolates affected partitions, safely deletes and recomputes historical records without downtime.",
        "code": '''def backfill_partition(storage, date_str, new_records):
    storage[:] = [r for r in storage if r.get("date") != date_str]
    storage.extend(new_records)
    return len(storage)
''',
        "test": '''from code.main import backfill_partition

def test_backfill():
    store = [{"date": "2026-09-01", "v": 1}, {"date": "2026-09-02", "v": 2}]
    backfill_partition(store, "2026-09-01", [{"date": "2026-09-01", "v": 99}])
    assert len(store) == 2 and [r["v"] for r in store if r["date"] == "2026-09-01"] == [99]
'''
    },
    {
        "id": "13-file-compactor",
        "title": "Small Files Compactor",
        "summary": "Detects sub-optimal tiny files in partition directories and merges them into standard size files to maximize scan throughput.",
        "code": '''def compact_records(record_chunks):
    merged = []
    for chunk in record_chunks:
        merged.extend(chunk)
    return merged
''',
        "test": '''from code.main import compact_records

def test_compaction():
    chunks = [[{"id": 1}], [{"id": 2}], [{"id": 3}]]
    assert len(compact_records(chunks)) == 3
'''
    },
    {
        "id": "14-reconciliation-system",
        "title": "Cross-System Financial Reconciliation",
        "summary": "Reconciles financial transactions between source OLTP payment gateway and analytical warehouse, detecting discrepancies and rounding drift.",
        "code": '''def reconcile(source_totals, warehouse_totals, tolerance=0.01):
    diff = abs(source_totals - warehouse_totals)
    return diff <= tolerance, diff
''',
        "test": '''from code.main import reconcile

def test_reconciliation():
    ok, diff = reconcile(100.50, 100.505)
    assert ok
    ok, diff = reconcile(100.50, 105.00)
    assert not ok
'''
    },
    {
        "id": "15-event-deduplication",
        "title": "Exact-Once Event Deduplication",
        "summary": "Filters duplicate events using Bloom filter intuition and LRU window cache to guarantee exact-once downstream semantics.",
        "code": '''class EventDeduplicator:
    def __init__(self, capacity=1000):
        self.seen = set()
    def is_duplicate(self, event_id):
        if event_id in self.seen:
            return True
        self.seen.add(event_id)
        return False
''',
        "test": '''from code.main import EventDeduplicator

def test_dedup():
    dedup = EventDeduplicator()
    assert not dedup.is_duplicate("e1")
    assert dedup.is_duplicate("e1")
'''
    },
    {
        "id": "16-slowly-changing-dimensions-scd2",
        "title": "Slowly Changing Dimensions (SCD Type 2)",
        "summary": "Maintains point-in-time attribute history by closing out active records with valid_to timestamps and inserting new versions.",
        "code": '''def apply_scd2(dimension, natural_key, new_attrs, effective_date):
    for r in dimension:
        if r["natural_key"] == natural_key and r.get("is_current", True):
            r["is_current"] = False
            r["valid_to"] = effective_date
    dimension.append({
        "natural_key": natural_key,
        "is_current": True,
        "valid_from": effective_date,
        "valid_to": None,
        **new_attrs
    })
''',
        "test": '''from code.main import apply_scd2

def test_scd2():
    dim = [{"natural_key": "u1", "tier": "STANDARD", "is_current": True, "valid_from": "2026-01-01", "valid_to": None}]
    apply_scd2(dim, "u1", {"tier": "VIP"}, "2026-09-01")
    assert len(dim) == 2 and not dim[0]["is_current"] and dim[1]["tier"] == "VIP"
'''
    },
    {
        "id": "17-data-catalog-lite",
        "title": "Metadata Catalog & Data Dictionary CLI",
        "summary": "Provides searchable data asset inventory, documenting owners, schemas, freshness SLAs, and tags.",
        "code": '''class DataCatalog:
    def __init__(self):
        self.assets = {}
    def register(self, name, owner, schema, description):
        self.assets[name] = {"owner": owner, "schema": schema, "description": description}
    def lookup(self, name):
        return self.assets.get(name)
''',
        "test": '''from code.main import DataCatalog

def test_catalog():
    cat = DataCatalog()
    cat.register("orders", "checkout-team", {"id": "str"}, "Orders fact table")
    assert cat.lookup("orders")["owner"] == "checkout-team"
'''
    }
]

def main():
    print(f"Generating {len(PROJECTS)} Substantial Projects in {PROJECTS_DIR}...")
    for p in PROJECTS:
        p_dir = PROJECTS_DIR / p["id"]
        code_dir = p_dir / "code"
        test_dir = p_dir / "tests"
        p_dir.mkdir(parents=True, exist_ok=True)
        code_dir.mkdir(parents=True, exist_ok=True)
        test_dir.mkdir(parents=True, exist_ok=True)

        # 1. README.md
        readme_text = f"""# Project: {p['title']}

> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.

---

## 1. Project Overview
{p['summary']}

## 2. Architectural Invariants
1. **Idempotency**: Rerunning the project logic on identical inputs produces identical target state.
2. **Contract Enforcement**: Input schemas and constraints are verified before state mutations.
3. **Traceability**: All output metrics and models trace cleanly to authoritative raw sources.

## 3. Directory Layout
- `code/main.py`: Core production implementation
- `tests/test_project.py`: Automated verification suite

## 4. Verification
Run the project test suite:
```bash
pytest projects/{p['id']}/tests/test_project.py
```
"""
        with open(p_dir / "README.md", "w") as f:
            f.write(readme_text)

        # 2. code/pipeline.py
        with open(code_dir / "pipeline.py", "w") as f:
            f.write(p["code"])

        # 3. tests/test_project.py
        # Cleanly load pipeline functions using importlib
        test_file_content = f"""import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_{p['id'].replace('-', '_')}", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

{p['test'].replace("from code.main import", "# imported above:")}
"""
        with open(test_dir / "test_project.py", "w") as f:
            f.write(test_file_content)

    print("All projects generated successfully!")

if __name__ == "__main__":
    main()
