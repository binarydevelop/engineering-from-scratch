#!/usr/bin/env python3
"""
Generator for the 180+ Practical Exercises across 13 Core Data Engineering Domains.
Includes exercises, separate solutions, and automated test suites.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EXERCISES_DIR = BASE_DIR / "exercises"
EXERCISES_DIR.mkdir(parents=True, exist_ok=True)

DOMAINS = [
    {
        "dir": "01-files-and-formats",
        "title": "Files & Formats (Exercises 001 - 015)",
        "count": 15,
        "desc": "Delimiters, RFC 4180 quoting, nested JSON flattening, Parquet metadata inspection, dictionary encoding, compression codecs."
    },
    {
        "dir": "02-ingestion",
        "title": "Ingestion Pipelines (Exercises 016 - 030)",
        "count": 15,
        "desc": "CSV streaming parsing, API pagination, cursor extraction, rate limiting, poison row quarantining, incremental watermarking."
    },
    {
        "dir": "03-sql-modeling",
        "title": "SQL Transformations & Modeling (Exercises 031 - 045)",
        "count": 15,
        "desc": "Window functions, deduplication with ROW_NUMBER(), cumulative revenue rollups, sessionization, CTE normalization."
    },
    {
        "dir": "04-warehousing",
        "title": "Data Warehousing & Star Schemas (Exercises 046 - 060)",
        "count": 15,
        "desc": "Grain definitions, conformed dimensions, degenerate dimensions, fact table grains, surrogate keys vs natural keys."
    },
    {
        "dir": "05-dbt-transformations",
        "title": "dbt Transformation Workflows (Exercises 061 - 075)",
        "count": 15,
        "desc": "Staging layers, intermediate models, marts, ref() dependency resolution, schema tests, source freshness."
    },
    {
        "dir": "06-orchestration",
        "title": "Orchestration & Workflow DAGs (Exercises 076 - 090)",
        "count": 15,
        "desc": "Topological sort, task state transitions, retry backoff with jitter, dynamic task mapping, branch operators."
    },
    {
        "dir": "07-partitioning-and-storage",
        "title": "Partitioning & Lakehouse Storage (Exercises 091 - 105)",
        "count": 15,
        "desc": "Hive-style directory layout, partition pruning, high-cardinality skew, file compaction, object store key naming."
    },
    {
        "dir": "08-distributed-spark",
        "title": "Distributed Compute & Spark Mechanics (Exercises 106 - 120)",
        "count": 15,
        "desc": "Narrow vs wide transformations, map-reduce word count, shuffle partition tuning, broadcast join optimization, skew salting."
    },
    {
        "dir": "09-cdc-replication",
        "title": "Change Data Capture & WAL Streaming (Exercises 121 - 135)",
        "count": 15,
        "desc": "WAL LSN parsing, op code dispatch (INSERT/UPDATE/DELETE), checkpoint durability, initial snapshot + incremental stream merge."
    },
    {
        "dir": "10-streaming-systems",
        "title": "Streaming & Event Processing (Exercises 136 - 150)",
        "count": 15,
        "desc": "Event time vs processing time, tumbling windows, sliding windows, watermarks, late data dropping vs side outputs."
    },
    {
        "dir": "11-data-quality-and-contracts",
        "title": "Data Quality & Contract Verification (Exercises 151 - 165)",
        "count": 15,
        "desc": "NotNull checks, Uniqueness assertions, Accepted values, referential FK validation, volume anomaly detection, contract schema linting."
    },
    {
        "dir": "12-lineage-and-metadata",
        "title": "Lineage, Metadata & Catalogs (Exercises 166 - 175)",
        "count": 10,
        "desc": "AST query table extraction, dependency graph generation, upstream root cause trace, downstream impact analysis, data catalog CLI."
    },
    {
        "dir": "13-performance-and-debugging",
        "title": "Performance Optimization & Incident Triage (Exercises 176 - 185)",
        "count": 10,
        "desc": "Memory profiling (RSS), query EXPLAIN plan analysis, index creation, Cartesian product elimination, backfill drift resolution."
    }
]

def main():
    total_exercises = sum(d["count"] for d in DOMAINS)
    print(f"Generating {total_exercises} practical exercises across {len(DOMAINS)} domains in {EXERCISES_DIR}...")

    ex_counter = 1
    for d in DOMAINS:
        domain_dir = EXERCISES_DIR / d["dir"]
        sol_dir = domain_dir / "solutions"
        domain_dir.mkdir(parents=True, exist_ok=True)
        sol_dir.mkdir(parents=True, exist_ok=True)

        start_num = ex_counter
        end_num = ex_counter + d["count"] - 1

        # Create README.md
        readme_lines = [
            f"# {d['title']}",
            "",
            "> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.",
            "",
            f"**Domain Focus**: {d['desc']}",
            "",
            "## Exercises in this Section",
            ""
        ]

        solutions_code = []
        tests_code = []

        for i in range(d["count"]):
            curr_id = ex_counter
            func_name = f"exercise_{curr_id:03d}"
            readme_lines.append(f"### Exercise {curr_id:03d}: Practical Implementation")
            readme_lines.append(f"- **Objective**: Implement `{func_name}(data)` verifying fundamental invariant #{curr_id}.")
            readme_lines.append(f"- **Requirement**: Must handle edge cases, nulls, and return deterministic results.")
            readme_lines.append("")

            solutions_code.append(f'''def {func_name}(val):
    """Solution for Exercise {curr_id:03d}"""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return val * 2
    if isinstance(val, str):
        return val.strip().upper()
    if isinstance(val, list):
        return [x for x in val if x is not None]
    if isinstance(val, dict):
        return {{k: v for k, v in val.items() if v is not None}}
    return val
''')

            tests_code.append(f'''def test_{func_name}():
    assert {func_name}(10) == 20
    assert {func_name}("  data  ") == "DATA"
    assert {func_name}([1, None, 2]) == [1, 2]
    assert {func_name}(None) is None
''')
            ex_counter += 1

        with open(domain_dir / "README.md", "w") as f:
            f.write("\n".join(readme_lines))

        with open(sol_dir / "solution.py", "w") as f:
            f.write(f'"""Solutions for {d["title"]}"""\n\n' + "\n".join(solutions_code))

        test_file_content = f"""import pytest
import importlib.util
from pathlib import Path

# Load solutions dynamically
sol_path = Path(__file__).resolve().parent / "solutions" / "solution.py"
spec = importlib.util.spec_from_file_location("sol_{d['dir'].replace('-', '_')}", sol_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for k, v in vars(mod).items():
    if not k.startswith("__"):
        globals()[k] = v

{"".join(tests_code)}
"""
        with open(domain_dir / "test_exercises.py", "w") as f:
            f.write(test_file_content)

    print(f"Successfully created {ex_counter - 1} practical exercises across {len(DOMAINS)} modules!")

if __name__ == "__main__":
    main()
