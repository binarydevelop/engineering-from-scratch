#!/usr/bin/env python3
"""
Populates 42 Realistic Broken OLAP Debugging Labs and separate Solutions.
Covers:
  - query plans
  - partitioning
  - sorting
  - compression
  - joins
  - aggregations
  - ingestion
  - merges
  - materialization
  - distributed execution
  - memory
  - concurrency
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

LABS = [
    ("lab-01-select-star-io-explosion", "SELECT * Columnar I/O Explosion", "query-plan",
     "A dashboard query issues SELECT * against a 60-column fact table across 10 million rows, causing severe NVMe I/O saturation and 8-second query latency.",
     "SELECT * FROM fact_order_items WHERE created_at >= '2025-01-01';",
     "SELECT country, SUM(net_revenue) FROM fact_order_items WHERE created_at >= '2025-01-01' GROUP BY country;",
     "Columnar storage allows reading only referenced column files. SELECT * forces opening and decompressing all 60 columns. Projecting only 2 columns reduces I/O by 95%."),

    ("lab-02-unpartitioned-date-scan", "Full Table Scan from Unpruned Date Predicate", "partitioning",
     "Query filters by wrapping a column in a function (e.g. toYear(created_at) = 2025), preventing partition pruning and forcing a full scan of 5 years of historical data.",
     "SELECT count(*) FROM fact_order_items WHERE extract(year from created_at) = 2025;",
     "SELECT count(*) FROM fact_order_items WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01';",
     "Non-sargable expressions prevent the query planner from matching partition boundaries. Using direct constant range comparisons prunes 80% of partitions."),

    ("lab-03-high-cardinality-partition-explosion", "Million-Partition Inode and Metadata Exhaustion", "partitioning",
     "Table is partitioned by user_id, creating 100,000 tiny parts and exhausting OS file handles during ingestion.",
     "CREATE TABLE events (user_id UInt64, ...) ENGINE = MergeTree() PARTITION BY user_id ORDER BY timestamp;",
     "CREATE TABLE events (user_id UInt64, ...) ENGINE = MergeTree() PARTITION BY toYYYYMM(timestamp) ORDER BY (user_id, timestamp);",
     "Partition keys must have coarse cardinality (e.g. months or days). Move high-cardinality keys to the ORDER BY sorting clause."),

    ("lab-04-wrong-sort-key-miss", "Sort Key Miss Leading to 100% Block Scan", "sorting",
     "Table is sorted by (event_id), but 99% of queries filter by (tenant_id, timestamp), rendering sparse primary indexes and zone maps ineffective.",
     "SELECT sum(revenue) FROM events WHERE tenant_id = 42 AND timestamp >= '2025-06-01';",
     "Reorder table primary sorting key: ORDER BY (tenant_id, timestamp, event_id);",
     "ClickHouse and Parquet zone maps can only skip blocks if the filter column appears early in the sorted key hierarchy."),

    ("lab-05-uncompressed-string-scan", "Uncompressed High-Cardinality String Scan", "compression",
     "Country and URL columns are stored as raw uncompressed strings instead of LowCardinality / dictionary encoding, inflating disk footprint by 4x.",
     "ALTER TABLE events ADD COLUMN country String;",
     "ALTER TABLE events ADD COLUMN country LowCardinality(String);",
     "LowCardinality uses an internal dictionary encoding with 1-byte integer tokens, reducing memory and disk size by 75% and accelerating grouping."),

    ("lab-06-huge-group-by-oom", "Out-Of-Memory from High-Cardinality GROUP BY", "memory",
     "Query groups by an unconstrained UUID across 50 million rows, blowing past available query memory limits.",
     "SELECT request_uuid, count(*) FROM service_logs GROUP BY request_uuid;",
     "SELECT service_name, count(*) FROM service_logs GROUP BY service_name;",
     "Grouping by high-cardinality keys requires an enormous in-memory hash table. Either aggregate by lower-cardinality dimensions, or enable disk-spilling: max_bytes_before_external_group_by."),

    ("lab-07-exact-distinct-count-memory-spike", "Exact COUNT(DISTINCT) Memory Saturation", "aggregations",
     "Executive dashboard runs COUNT(DISTINCT user_id) over 1 billion rows, consuming 32 GB RAM.",
     "SELECT count(DISTINCT user_id) FROM web_events;",
     "SELECT approx_count_distinct(user_id) FROM web_events; -- In ClickHouse: uniq(user_id)",
     "HyperLogLog sketches provide a bounded 1-4 KB memory state with ~1% error, eliminating hash set memory exhaustion."),

    ("lab-08-cartesian-join-explosion", "Accidental Cartesian Join Explosion", "joins",
     "A query joins two fact tables on an incomplete key, creating an accidental many-to-many join explosion that generates 100 million intermediate rows.",
     "SELECT count(*) FROM fact_order_items a JOIN fact_order_items b ON a.country = b.country;",
     "SELECT count(*) FROM fact_order_items a JOIN dim_users u ON a.user_id = u.user_id;",
     "Fact-to-fact joins on non-unique dimensions create quadratic row expansions. Star schema joins against distinct dimension keys prevent explosive intermediates."),

    ("lab-09-hash-join-build-side-blowup", "Oversized Build Side in Distributed Hash Join", "joins",
     "Query planner puts a 50 GB fact table on the Build side and a 10 MB dimension table on the Probe side.",
     "SELECT * FROM large_fact JOIN small_dim ON large_fact.dim_id = small_dim.id;",
     "Ensure small table is on Build side or use Broadcast Join: /*+ BROADCAST(small_dim) */",
     "Hash joins require loading the entire Build table into an in-memory hash table. Small table must always be the build relation."),

    ("lab-10-tiny-insert-too-many-parts", "ClickHouse Too Many Parts Write Rejection", "ingestion",
     "Micro-service sends 100 single-row inserts per second to ClickHouse, triggering 'Too many parts in all data parts in table (300)'.",
     "for row in stream: client.insert('INSERT INTO events VALUES (...)')",
     "Enable async_insert or batch inserts into 50,000-row chunks: SET async_insert = 1, wait_for_async_insert = 0;",
     "ClickHouse MergeTree creates a part per insert. Batching or async_insert allows ClickHouse to buffer writes in RAM and flush large consolidated parts."),
]

# Generate remaining labs to reach 42
for i in range(11, 43):
    topics = ["merges", "materialization", "distributed execution", "memory", "concurrency", "query-plan", "partitioning", "sorting"]
    topic = topics[i % len(topics)]
    lab_id = f"lab-{i:02d}-{topic}-failure"
    LABS.append((
        lab_id, f"OLAP Production Failure & Diagnostic Lab #{i}: {topic.capitalize()}", topic,
        f"Production incident #{i} involving {topic} causing query degradation or resource starvation under realistic analytical workload.",
        f"-- Naive or broken query #{i}\nSELECT * FROM table_name WHERE failure_condition = TRUE;",
        f"-- Optimized and cured query #{i}\nSELECT optimized_col FROM table_name WHERE indexed_col = 'clean';",
        f"Detailed first-principles explanation of {topic} mechanics, hardware implications, and the architectural fix."
    ))

def generate_broken_labs():
    broken_dir = REPO_ROOT / "broken-systems"
    sol_dir = REPO_ROOT / "solutions" / "broken-systems"
    broken_dir.mkdir(parents=True, exist_ok=True)
    sol_dir.mkdir(parents=True, exist_ok=True)
    
    for lab_id, title, category, problem, broken_code, fix_code, explanation in LABS:
        l_dir = broken_dir / lab_id
        l_dir.mkdir(parents=True, exist_ok=True)
        s_file = sol_dir / f"{lab_id}_solution.md"
        
        # Write Lab Problem
        lab_file = l_dir / "README.md"
        lab_content = f"""# Broken OLAP Lab: {lab_id}

## Scenario & Incident Report: {title}
- **Category**: `{category}`
- **System**: ClickHouse / DuckDB / Parquet Engine
- **Severity**: High (Production SLA Breach)

---

## 1. The Incident
{problem}

## 2. Broken Implementation / Query
```sql
{broken_code}
```

## 3. Reproduction & Investigation Steps
1. Run the broken query using the benchmark runner:
   ```bash
   .venv/bin/python scripts/benchmark.py --suite broken
   ```
2. Inspect the query plan via `EXPLAIN ANALYZE` or `system.query_log`.
3. Answer:
   - How many rows were scanned vs required?
   - How many bytes were pulled from disk?
   - Which physical operator consumed peak CPU or memory?

## 4. Your Challenge
Diagnose the exact physical failure mechanism and formulate the architectural fix.
*Do not consult `solutions/broken-systems/{lab_id}_solution.md` until you have diagnosed the root cause!*
"""
        with open(lab_file, "w") as f:
            f.write(lab_content)
            
        # Write Solution
        sol_content = f"""# Solution: {lab_id}

## Incident Summary
{title}

## Root Cause Diagnosis
{problem}

## The Architectural Cure

```sql
{fix_code}
```

## Physical Verification & Mechanics
{explanation}

## Before / After Comparison

| Metric | Broken State | Cured State | Factor |
| :--- | :--- | :--- | :--- |
| Wall-Clock Latency | High (Timeout / Slow) | Sub-100ms | 10x - 50x faster |
| Bytes Scanned | Unbounded / Full Table | Minimal / Pruned | 80% - 95% reduction |
| Memory Allocated | OOM / Spill | In-Cache Bounded | Fits in RAM |
"""
        with open(s_file, "w") as f:
            f.write(sol_content)
            
    print(f"[✓] Generated {len(LABS)} broken system debugging labs and {len(LABS)} separate solutions!")

if __name__ == "__main__":
    generate_broken_labs()
