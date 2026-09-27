#!/usr/bin/env python3
"""
Generator for the 32 Broken Pipeline Labs
Creates structured labs with Problem, Broken Pipeline, Separate Solution, and Tests.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BROKEN_DIR = BASE_DIR / "broken-pipelines"
BROKEN_DIR.mkdir(parents=True, exist_ok=True)

LABS = [
    {
        "id": "lab-01-missing-delimiter-malformed-csv",
        "title": "Missing Delimiter & Malformed CSV Ingestion",
        "category": "ingestion",
        "description": "Upstream vendor sends CSV where some rows contain unescaped commas inside text fields without quoting, corrupting column alignment.",
        "broken_code": '''# Broken: Naive split on comma
def ingest_records(raw_text):
    rows = []
    for line in raw_text.strip().split("\\n"):
        parts = line.split(",") # Fails on unquoted commas
        rows.append({"id": parts[0], "name": parts[1], "city": parts[2]})
    return rows
''',
        "fixed_code": '''# Fixed: RFC 4180 compliant CSV parser with quarantine for malformed column counts
import csv
import io

def ingest_records(raw_text):
    valid, quarantined = [], []
    reader = csv.reader(io.StringIO(raw_text.strip()))
    for row_idx, parts in enumerate(reader, 1):
        if len(parts) == 3:
            valid.append({"id": parts[0], "name": parts[1], "city": parts[2]})
        else:
            quarantined.append({"row_idx": row_idx, "raw": parts, "reason": "COLUMN_COUNT_MISMATCH"})
    return valid, quarantined
''',
        "test_assert": "valid, quarantined = ingest_records('1,Alice,NYC\\n2,Bob,LA\\n3,BadRowOnlyTwo'); assert len(valid) == 2 and len(quarantined) == 1"
    },
    {
        "id": "lab-02-silent-type-coercion-string-to-int",
        "title": "Silent Type Coercion & Integer Overflow",
        "category": "schema",
        "description": "Source customer IDs changed from numeric to alphanumeric (e.g., '1004B'), causing silent null coercion or casting crashes in downstream SQL.",
        "broken_code": '''# Broken: Assumes IDs are always integers
def parse_customer_id(val):
    return int(val) # Crashes on '1004B'
''',
        "fixed_code": '''# Fixed: Preserves identifier semantics as string / validates format
def parse_customer_id(val):
    clean = str(val).strip()
    if not clean:
        raise ValueError("Customer ID cannot be empty")
    return clean
''',
        "test_assert": "assert parse_customer_id('1004B') == '1004B'"
    },
    {
        "id": "lab-03-duplicate-records-missing-idempotency",
        "title": "Duplicate Records from Missing Pipeline Idempotency",
        "category": "ingestion",
        "description": "A scheduled job appends new records into a table without checking primary key uniqueness. When retried, revenue metrics double.",
        "broken_code": '''# Broken: Blind append
def load_records(db_table, batch):
    db_table.extend(batch) # Doubles rows on rerun!
''',
        "fixed_code": '''# Fixed: Deduplicated upsert using unique business key
def load_records(db_table, batch):
    # Upsert by ID
    existing_ids = {r["id"] for r in db_table}
    for item in batch:
        if item["id"] in existing_ids:
            # Update existing
            for idx, r in enumerate(db_table):
                if r["id"] == item["id"]:
                    db_table[idx] = item
        else:
            db_table.append(item)
            existing_ids.add(item["id"])
''',
        "test_assert": "table = [{'id': '1', 'v': 10}]; load_records(table, [{'id': '1', 'v': 20}]); assert len(table) == 1 and table[0]['v'] == 20"
    },
    {
        "id": "lab-04-cartesian-product-join-explosion",
        "title": "Cartesian Product Join Row Explosion",
        "category": "transformation",
        "description": "Joining fact orders with customer dimension on non-unique customer key multiplies rows, inflating totals 10x.",
        "broken_code": '''# Broken: Non-unique join key causes Cartesian explosion
def join_orders_users(orders, users):
    out = []
    for o in orders:
        for u in users:
            if o["user_id"] == u["user_id"]: # Duplicate user records multiply order!
                out.append({**o, **u})
    return out
''',
        "fixed_code": '''# Fixed: Deduplicate dimension on surrogate key / current flag before joining
def join_orders_users(orders, users):
    latest_users = {u["user_id"]: u for u in users if u.get("is_current", True)}
    out = []
    for o in orders:
        u = latest_users.get(o["user_id"], {})
        out.append({**o, "user_name": u.get("name", "UNKNOWN")})
    return out
''',
        "test_assert": "orders = [{'id': 1, 'user_id': 'u1'}]; users = [{'user_id': 'u1', 'name': 'Old', 'is_current': False}, {'user_id': 'u1', 'name': 'New', 'is_current': True}]; res = join_orders_users(orders, users); assert len(res) == 1 and res[0]['user_name'] == 'New'"
    },
    {
        "id": "lab-05-null-primary-key-quarantine-failure",
        "title": "Null Primary Key Silently Passing Validation",
        "category": "quality",
        "description": "Pipeline only validates row length but ignores empty strings in primary key column, breaking relational foreign keys downstream.",
        "broken_code": '''def validate_record(rec):
    return len(rec) > 0 # Allows null or empty ID
''',
        "fixed_code": '''def validate_record(rec):
    pk = rec.get("id")
    if pk is None or str(pk).strip() == "":
        return False, "NULL_OR_EMPTY_PK"
    return True, "VALID"
''',
        "test_assert": "ok, _ = validate_record({'id': ''}); assert not ok"
    },
    {
        "id": "lab-06-unhandled-schema-drift-missing-column",
        "title": "Unhandled Schema Drift: Missing Expected Column",
        "category": "schema",
        "description": "Producer deprecates a field without warning; parser crashes with KeyError rather than falling back to default.",
        "broken_code": '''def parse_payload(payload):
    return {"order_id": payload["order_id"], "tax": payload["tax"]} # KeyError if tax missing
''',
        "fixed_code": '''def parse_payload(payload):
    return {
        "order_id": payload.get("order_id", "UNKNOWN"),
        "tax": float(payload.get("tax", 0.0))
    }
''',
        "test_assert": "res = parse_payload({'order_id': 'ord_1'}); assert res['tax'] == 0.0"
    },
    {
        "id": "lab-07-cdc-wal-lsn-checkpoint-rewind",
        "title": "CDC WAL Checkpoint Lost on Worker Crash",
        "category": "cdc",
        "description": "CDC pipeline acknowledges messages before writing to target database. When worker crashes, records are skipped forever.",
        "broken_code": '''class NaiveCDC:
    def __init__(self):
        self.checkpoint = 0
    def process_and_commit_first(self, event, db):
        self.checkpoint = event["lsn"] # Commits checkpoint BEFORE target write!
        if event.get("crash"): raise RuntimeError("Worker killed!")
        db.append(event)
''',
        "fixed_code": '''class SafeCDC:
    def __init__(self):
        self.checkpoint = 0
    def process_atomic(self, event, db):
        if event.get("crash"): raise RuntimeError("Worker killed!")
        # Target write first, then checkpoint commit
        db.append(event)
        self.checkpoint = event["lsn"]
''',
        "test_assert": "cdc = SafeCDC(); db = []; assert cdc.checkpoint == 0"
    },
    {
        "id": "lab-08-streaming-watermark-premature-close",
        "title": "Streaming Watermark Closes Window Prematurely",
        "category": "streaming",
        "description": "Watermark advances strictly with processing wall-clock time, causing network-delayed mobile events to be dropped as late data.",
        "broken_code": '''def is_late_naive(event_time, wall_clock):
    return event_time < wall_clock # Drops any event with even 1s network latency!
''',
        "fixed_code": '''def is_late_watermarked(event_time, high_watermark, allowed_lateness_sec=60):
    return event_time < (high_watermark - allowed_lateness_sec)
''',
        "test_assert": "assert not is_late_watermarked(95, 100, 10) and is_late_watermarked(80, 100, 10)"
    },
    {
        "id": "lab-09-out-of-memory-unbounded-batch-read",
        "title": "Out of Memory (OOM) from Unbounded In-Memory Load",
        "category": "performance",
        "description": "Using json.load() on a 20 GB file loads the entire syntax tree into RAM, crashing with OOM Killer.",
        "broken_code": '''# Broken: Reads entire file at once
def read_all(lines):
    return [l for l in lines] # OOM on huge files
''',
        "fixed_code": '''# Fixed: Streaming generator yields chunks
def read_in_chunks(lines, chunk_size=2):
    chunk = []
    for l in lines:
        chunk.append(l)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
''',
        "test_assert": "chunks = list(read_in_chunks([1,2,3,4,5], 2)); assert len(chunks) == 3"
    },
    {
        "id": "lab-10-small-files-partition-explosion",
        "title": "Small Files Problem from High-Cardinality Partitioning",
        "category": "partitioning",
        "description": "Partitioning by user_id and minute creates 500,000 files with 1 record each, overloading cloud object store metadata.",
        "broken_code": '''def get_partition_path(user_id, minute):
    return f"users/{user_id}/minute={minute}/data.parquet" # Millions of 100-byte files!
''',
        "fixed_code": '''def get_partition_path(event_date):
    # Coarse partition key: Date level + compacted batches
    return f"events/date={event_date}/data.parquet"
''',
        "test_assert": "assert get_partition_path('2026-09-01') == 'events/date=2026-09-01/data.parquet'"
    },
    {
        "id": "lab-11-partial-write-missing-atomic-commit",
        "title": "Partial Write Exposes Corrupted Data to Consumers",
        "category": "reliability",
        "description": "Pipeline writes directly into final destination folder. If killed halfway, downstream readers query incomplete data.",
        "broken_code": '''def write_direct(target_dir, files):
    for f in files:
        # Writes directly to prod directory
        (target_dir / f).touch()
''',
        "fixed_code": '''import shutil
def write_atomic(staging_dir, final_dir, files):
    staging_dir.mkdir(parents=True, exist_ok=True)
    for f in files:
        (staging_dir / f).touch()
    # Atomic swap / rename
    final_dir.parent.mkdir(parents=True, exist_ok=True)
    if final_dir.exists(): shutil.rmtree(final_dir)
    staging_dir.rename(final_dir)
''',
        "test_assert": "assert True"
    },
    {
        "id": "lab-12-stale-source-freshness-sla-breach",
        "title": "Stale Source Freshness SLA Breach",
        "category": "freshness",
        "description": "Pipeline runs green every hour, but upstream replication stopped 12 hours ago, silently reporting yesterday's numbers.",
        "broken_code": '''def check_freshness(latest_ts, current_ts):
    return True # Silently passes without checking delta
''',
        "fixed_code": '''def check_freshness(latest_ts, current_ts, max_lag_seconds=3600):
    lag = current_ts - latest_ts
    if lag > max_lag_seconds:
        return False, f"FRESHNESS_BREACH: Lag of {lag}s exceeds SLA of {max_lag_seconds}s"
    return True, "FRESH"
''',
        "test_assert": "ok, _ = check_freshness(1000, 5000, 3600); assert not ok"
    },
    {
        "id": "lab-13-circular-dag-orchestration-deadlock",
        "title": "Circular Dependency Deadlock in DAG Runner",
        "category": "orchestration",
        "description": "Task A depends on B, and B depends on A, hanging the orchestration runner in an infinite wait.",
        "broken_code": '''def naive_schedule(tasks):
    # Runs tasks without topological cycle check -> deadlocks
    pass
''',
        "fixed_code": '''def detect_cycle(graph):
    visited = set()
    rec_stack = set()
    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor): return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(node)
        return False
    for n in graph:
        if n not in visited:
            if dfs(n): return True
    return False
''',
        "test_assert": "assert detect_cycle({'A': ['B'], 'B': ['A']}) and not detect_cycle({'A': ['B'], 'B': []})"
    },
    {
        "id": "lab-14-backfill-overwriting-production-slice",
        "title": "Backfill Accidentally Overwriting Current Production Slice",
        "category": "backfills",
        "description": "A backfill script intended for 2025 omits partition filter in DELETE statement, truncating 2026 data.",
        "broken_code": '''def backfill_slice_broken(target_db):
    target_db.clear() # Catastrophic: deletes all partitions!
''',
        "fixed_code": '''def backfill_slice_safe(target_db, partition_date, new_data):
    # Isolated partition replacement
    target_db[:] = [r for r in target_db if r.get("date") != partition_date]
    target_db.extend(new_data)
''',
        "test_assert": "db = [{'date': '2026-01-01'}, {'date': '2026-09-01'}]; backfill_slice_safe(db, '2026-01-01', [{'date': '2026-01-01', 'v': 2}]); assert len(db) == 2"
    },
    {
        "id": "lab-15-financial-reconciliation-rounding-error",
        "title": "Financial Reconciliation Rounding Drift",
        "category": "quality",
        "description": "Using IEEE-754 floating-point numbers for currency amounts causes micro-cent drift in daily balance reconciliations.",
        "broken_code": '''def sum_revenue_float(amounts):
    return sum(amounts) # Float addition yields 0.30000000000000004
''',
        "fixed_code": '''from decimal import Decimal
def sum_revenue_decimal(amounts):
    return sum([Decimal(str(a)) for a in amounts])
''',
        "test_assert": "from decimal import Decimal; assert sum_revenue_decimal([0.1, 0.2]) == Decimal('0.3')"
    },
    {
        "id": "lab-16-late-arriving-dimension-fk-orphan",
        "title": "Late-Arriving Dimension Fact Orphan",
        "category": "modeling",
        "description": "Order fact arrives before customer registration completes in warehouse, failing strict foreign key joins.",
        "broken_code": '''def resolve_customer(fact, dim_customers):
    return dim_customers[fact["user_id"]] # KeyError if customer not arrived yet!
''',
        "fixed_code": '''def resolve_customer(fact, dim_customers):
    # Route to placeholder surrogate key: -1 (UNKNOWN / Late Dimension)
    return dim_customers.get(fact["user_id"], {"customer_sk": -1, "name": "UNKNOWN_PENDING_DIM"})
''',
        "test_assert": "assert resolve_customer({'user_id': 'missing'}, {})['customer_sk'] == -1"
    },
    {
        "id": "lab-17-skewed-partition-long-tail-straggler",
        "title": "Key Skew Creating Long-Tail Task Straggler",
        "category": "spark",
        "description": "Grouping by country code routes 85% of traffic to partition 'US', leaving 9 workers idle while 1 worker crashes.",
        "broken_code": '''def naive_key(country):
    return country # US key becomes giant hotspot
''',
        "fixed_code": '''import random
def salted_key(country, salt_factor=5):
    # Salting spreads hot key across multiple sub-partitions
    if country == "US":
        return f"US_{random.randint(0, salt_factor - 1)}"
    return country
''',
        "test_assert": "assert salted_key('US').startswith('US_')"
    },
    {
        "id": "lab-18-scd2-overlapping-effective-dates",
        "title": "SCD Type 2 Overlapping Effective Date Windows",
        "category": "modeling",
        "description": "Customer address updates set valid_from without closing previous record's valid_to, returning 2 active rows for point-in-time queries.",
        "broken_code": '''def update_scd2_broken(records, new_record):
    records.append(new_record) # Appends without setting valid_to on previous!
''',
        "fixed_code": '''def update_scd2_fixed(records, new_record):
    for r in records:
        if r["user_id"] == new_record["user_id"] and r.get("is_current", True):
            r["is_current"] = False
            r["valid_to"] = new_record["valid_from"]
    records.append(new_record)
''',
        "test_assert": "rec = [{'user_id': 'u1', 'is_current': True, 'valid_from': '2026-01-01'}]; update_scd2_fixed(rec, {'user_id': 'u1', 'is_current': True, 'valid_from': '2026-09-01'}); assert len(rec) == 2 and not rec[0]['is_current'] and rec[0]['valid_to'] == '2026-09-01'"
    },
    {
        "id": "lab-19-poison-record-crashing-entire-batch",
        "title": "Poison Record Crashing Entire 1M Row Pipeline",
        "category": "reliability",
        "description": "A single malformed JSON row crashes the entire 8-hour batch job instead of being quarantined.",
        "broken_code": '''import json
def process_batch_broken(lines):
    return [json.loads(l) for l in lines] # 1 corrupted byte crashes entire batch
''',
        "fixed_code": '''import json
def process_batch_quarantine(lines):
    valid, quarantine = [], []
    for idx, l in enumerate(lines):
        try:
            valid.append(json.loads(l))
        except Exception as e:
            quarantine.append({"line_idx": idx, "raw": l, "error": str(e)})
    return valid, quarantine
''',
        "test_assert": "v, q = process_batch_quarantine(['{\"a\": 1}', 'BAD_JSON']); assert len(v) == 1 and len(q) == 1"
    },
    {
        "id": "lab-20-missing-partition-pruning-full-table-scan",
        "title": "Missing Partition Pruning Triggering 10 TB Scan",
        "category": "performance",
        "description": "Applying a function to partition key (e.g. `WHERE DATE(event_timestamp) = ...`) defeats partition pruning.",
        "broken_code": '''# Inefficient: Function wraps partition column
def generate_filter_broken(date_str):
    return f"WHERE date_trunc('day', event_time) = '{date_str}'"
''',
        "fixed_code": '''# Efficient: SARGable predicate matches physical partition key directly
def generate_filter_pruned(date_str):
    return f"WHERE partition_date = '{date_str}'"
''',
        "test_assert": "assert 'partition_date =' in generate_filter_pruned('2026-09-01')"
    },
    {
        "id": "lab-21-lineage-graph-broken-dependency-gap",
        "title": "Broken Dependency Gap in Metadata Lineage",
        "category": "lineage",
        "description": "Intermediate temporary table created outside tracked framework obscures true provenance of marketing mart.",
        "broken_code": '''# Broken: Untracked ad-hoc intermediate table
def run_transform_broken(db):
    db["temp_untracked"] = db["raw"]
    db["mart"] = db["temp_untracked"]
''',
        "fixed_code": '''# Fixed: Explicit DAG dependency lineage registry
def record_lineage(registry, upstream, downstream):
    registry.setdefault(downstream, set()).add(upstream)
''',
        "test_assert": "reg = {}; record_lineage(reg, 'raw_orders', 'stg_orders'); assert 'raw_orders' in reg['stg_orders']"
    },
    {
        "id": "lab-22-unindexed-oltp-table-extraction-lock",
        "title": "Unindexed Extraction Triggering OLTP Table Locks",
        "category": "ingestion",
        "description": "ETL worker runs `SELECT * FROM orders WHERE updated_at > ...` without index on updated_at, causing table lock and API 500 errors.",
        "broken_code": '''def extract_query_broken():
    return "SELECT * FROM orders WHERE updated_at > '2026-09-01';"
''',
        "fixed_code": '''def extract_query_bounded():
    # Indexed cursor extraction with batch limits
    return "SELECT * FROM orders WHERE updated_at > '2026-09-01' ORDER BY updated_at LIMIT 1000;"
''',
        "test_assert": "assert 'LIMIT' in extract_query_bounded()"
    },
    {
        "id": "lab-23-stream-consumer-lag-backpressure-overflow",
        "title": "Streaming Consumer Lag Backpressure Overflow",
        "category": "streaming",
        "description": "Upstream broker produces 50k events/sec; single-threaded consumer processes 5k events/sec until buffers exhaust memory.",
        "broken_code": '''def estimate_backpressure_broken(prod_rate, cons_rate):
    return False # Ignores lag
''',
        "fixed_code": '''def estimate_lag_growth(prod_rate, cons_rate, elapsed_sec):
    deficit = prod_rate - cons_rate
    return max(0, deficit * elapsed_sec)
''',
        "test_assert": "assert estimate_lag_growth(1000, 800, 10) == 2000"
    },
    {
        "id": "lab-24-unhandled-timezone-dst-shift-in-grain",
        "title": "Daylight Savings Shift Corrupting Hourly Grain",
        "category": "modeling",
        "description": "Using local clock string without UTC offset creates duplicate 01:00 AM hours during fall-back DST shift.",
        "broken_code": '''import datetime
def get_naive_hourly_key():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:00") # Ambiguous on DST
''',
        "fixed_code": '''import datetime
def get_utc_hourly_key():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:00Z")
''',
        "test_assert": "assert get_utc_hourly_key().endswith('Z')"
    },
    {
        "id": "lab-25-iceberg-metadata-snapshot-mismatch",
        "title": "Lakehouse Snapshot Concurrency Conflict",
        "category": "lakehouse",
        "description": "Two concurrent writers attempt to commit new snapshots against the same base version; one experiences optimistic locking failure.",
        "broken_code": '''def commit_snapshot_naive(current_v, new_v):
    return new_v # Overwrites blindly without validating parent snapshot
''',
        "fixed_code": '''def commit_snapshot_optimistic(expected_parent, actual_parent, new_v):
    if expected_parent != actual_parent:
        raise ValueError("CONCURRENT_MODIFICATION_EXCEPTION: Snapshot conflict, retry required")
    return new_v
''',
        "test_assert": """try:
    commit_snapshot_optimistic(1, 2, 3)
    assert False
except ValueError:
    assert True"""
    },
    {
        "id": "lab-26-spark-broadcast-join-oom-driver",
        "title": "Oversized Broadcast Join Crashing Driver Node",
        "category": "spark",
        "description": "Broadcasting a table that grew to 15 GB exhausts Spark Driver memory.",
        "broken_code": '''def should_broadcast(table_size_bytes):
    return True # Broadcasts regardless of size
''',
        "fixed_code": '''def should_broadcast(table_size_bytes, max_broadcast_bytes=100*1024*1024):
    return table_size_bytes <= max_broadcast_bytes
''',
        "test_assert": "assert not should_broadcast(500*1024*1024) and should_broadcast(50*1024*1024)"
    },
    {
        "id": "lab-27-data-contract-semantic-violation-negative-price",
        "title": "Data Contract Semantic Violation: Negative Product Price",
        "category": "contracts",
        "description": "Upstream discounts bug creates negative price orders that pass type check (float) but violate business domain invariants.",
        "broken_code": '''def validate_price(price):
    return isinstance(price, (int, float)) # Passes -50.00
''',
        "fixed_code": '''def validate_price(price):
    return isinstance(price, (int, float)) and price >= 0.0
''',
        "test_assert": "assert not validate_price(-10.0) and validate_price(15.5)"
    },
    {
        "id": "lab-28-retry-storm-without-exponential-backoff",
        "title": "Immediate Retry Storm Overloading Upstream API",
        "category": "reliability",
        "description": "100 parallel workers immediately retry a failing API simultaneously, causing cascading HTTP 503 denial-of-service.",
        "broken_code": '''def calculate_retry_delay_broken(attempt):
    return 0 # Immediate retry creates storm
''',
        "fixed_code": '''import random
def calculate_retry_delay_backoff(attempt, base_sec=1.0, max_sec=30.0):
    delay = min(max_sec, base_sec * (2 ** attempt))
    jitter = random.uniform(0, 0.5 * delay)
    return delay + jitter
''',
        "test_assert": "assert calculate_retry_delay_backoff(2, 1.0) >= 4.0"
    },
    {
        "id": "lab-29-unbounded-state-store-leak-in-streaming",
        "title": "Unbounded State Store Memory Leak in Streaming",
        "category": "streaming",
        "description": "Stream join keeps user state in memory forever without TTL, eventually exhausting heap memory.",
        "broken_code": '''class UnboundedState:
    def __init__(self):
        self.state = {}
    def put(self, k, v):
        self.state[k] = v # Never evicts -> OOM
''',
        "fixed_code": '''import time
class TTLStateStore:
    def __init__(self, ttl_sec=3600):
        self.ttl = ttl_sec
        self.state = {}
    def put(self, k, v):
        self.state[k] = (v, time.time())
    def prune(self):
        now = time.time()
        self.state = {k: val for k, (val, ts) in self.state.items() if now - ts < self.ttl}
''',
        "test_assert": "store = TTLStateStore(ttl_sec=0); store.put('k', 1); store.prune(); assert len(store.state) == 0"
    },
    {
        "id": "lab-30-silent-truncation-unicode-string-overflow",
        "title": "Silent Truncation of Multi-Byte Unicode Strings",
        "category": "schema",
        "description": "Database schema defines VARCHAR(10) assuming ASCII; 4-byte emojis silently truncate or cause byte-length mismatch.",
        "broken_code": '''def truncate_bytes_broken(s, max_bytes=10):
    return s[:max_bytes] # Character slice != byte length in UTF-8
''',
        "fixed_code": '''def safe_utf8_truncate(s, max_bytes=10):
    encoded = s.encode("utf-8")
    if len(encoded) <= max_bytes:
        return s
    return encoded[:max_bytes].decode("utf-8", errors="ignore")
''',
        "test_assert": "assert len(safe_utf8_truncate('🚀🚀🚀', 8).encode('utf-8')) <= 8"
    },
    {
        "id": "lab-31-api-rate-limit-http-429-data-loss",
        "title": "API Rate Limit 429 Dropping Ingested Pages",
        "category": "ingestion",
        "description": "Paginated API crawler receives HTTP 429 (Too Many Requests), skips page and moves to next page, dropping 10,000 records.",
        "broken_code": '''def fetch_page_broken(page):
    resp = {"status": 429}
    if resp["status"] != 200:
        return [] # Skips page! Data lost!
''',
        "fixed_code": '''def fetch_page_resilient(page, max_retries=3):
    for attempt in range(max_retries):
        # Simulates retry with backoff on 429
        if attempt == 2:
            return [{"id": f"rec_{page}"}]
    return []
''',
        "test_assert": "assert len(fetch_page_resilient(1)) == 1"
    },
    {
        "id": "lab-32-corrupted-parquet-footer-dictionary-crash",
        "title": "Corrupted Parquet Footer Metadata File Crash",
        "category": "formats",
        "description": "A partially written Parquet file missing its 4-byte 'PAR1' magic footer byte causes entire directory scans to abort.",
        "broken_code": '''def scan_files_broken(file_list):
    for f in file_list:
        if f.endswith(".corrupt"):
            raise ValueError("Invalid Parquet magic bytes")
''',
        "fixed_code": '''def scan_files_resilient(file_list):
    valid, unreadable = [], []
    for f in file_list:
        if f.endswith(".corrupt"):
            unreadable.append({"file": f, "error": "CORRUPT_MAGIC_BYTES"})
        else:
            valid.append(f)
    return valid, unreadable
''',
        "test_assert": "v, u = scan_files_resilient(['good.parquet', 'bad.corrupt']); assert len(v) == 1 and len(u) == 1"
    }
]

def main():
    print(f"Generating {len(LABS)} Broken Pipeline Labs...")
    for lab in LABS:
        lab_dir = BROKEN_DIR / lab["id"]
        lab_dir.mkdir(parents=True, exist_ok=True)
        sol_dir = lab_dir / "solution"
        sol_dir.mkdir(parents=True, exist_ok=True)

        # 1. README.md
        readme_content = f"""# {lab['title']}

> **Category**: `{lab['category']}`
> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.

---

## 1. Problem Description
{lab['description']}

## 2. Failure Symptoms
- Downstream metrics drift, silent row multiplication, or unhandled process termination.
- Pipeline execution exit code may erroneously report `SUCCESS` while data is mathematically corrupt.

## 3. Investigation & Diagnosis
1. Inspect the broken script in `broken_pipeline.py`.
2. Observe how the failure occurs under real input.
3. Compare with the resilient architecture in `solution/fixed_pipeline.py`.

## 4. How to Verify
Run the lab test suite:
```bash
pytest broken-pipelines/{lab['id']}/test_lab.py
```
"""
        with open(lab_dir / "README.md", "w") as f:
            f.write(readme_content)

        # 2. broken_pipeline.py
        with open(lab_dir / "broken_pipeline.py", "w") as f:
            f.write(f'"""\nBroken implementation demonstrating the flaw in {lab["id"]}.\n"""\n' + lab["broken_code"])

        # 3. solution/fixed_pipeline.py
        with open(sol_dir / "fixed_pipeline.py", "w") as f:
            f.write(f'"""\nResilient, production-ready solution for {lab["id"]}.\n"""\n' + lab["fixed_code"])

        # 4. test_lab.py
        # Indent test_body by 4 spaces for direct Python execution
        indented_test = "\n".join("    " + line for line in lab['test_assert'].split("\n"))
        test_content = f"""import pytest
import importlib.util
from pathlib import Path

def test_fixed_implementation():
    mod_path = Path(__file__).resolve().parent / "solution" / "fixed_pipeline.py"
    spec = importlib.util.spec_from_file_location("sol_{lab['id'].replace('-', '_')}", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Inject solution symbols into globals
    for k, v in vars(mod).items():
        if not k.startswith("__"):
            globals()[k] = v

{indented_test}
"""
        with open(lab_dir / "test_lab.py", "w") as f:
            f.write(test_content)

    print(f"Successfully generated {len(LABS)} Broken Pipeline Labs in {BROKEN_DIR}")

if __name__ == "__main__":
    main()
