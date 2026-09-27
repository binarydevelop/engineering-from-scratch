# Learning Data Engineering From Scratch

> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.

---

## 1. The Core Philosophy

Data Engineering is **NOT** a collection of pipeline tools. It is not "Airflow + Spark + dbt".

> **Data Engineering is the discipline of moving, transforming, validating, organizing, and operating data so that downstream systems can depend on it.**

When a business requirement arrives ("We need to track customer lifetime value" or "We need real-time fraud alerts"), the novice immediately jumps to tooling: *"Should we use Spark or Flink? Airflow or Dagster? Snowflake or BigQuery?"*

The experienced data engineer starts with fundamentals:
1. **Source of Truth**: Where does the raw data originate? Is it an OLTP database log, an API webhook, or clickstream events?
2. **Grain**: What does exactly one record represent? An entire order, an item inside an order, or a status transition?
3. **Volume & Velocity**: How many bytes and records per hour? Does the consumer truly need sub-second updates, or does a daily batch meet the business requirement at 1/50th of the cost and complexity?
4. **Failure Modes**: What happens when network timeouts occur midway? If a job runs twice, do duplicate rows appear? If a schema column changes type, does the pipeline silently corrupt financial metrics?
5. **Replayability**: If downstream business logic changes or a bug is discovered, can the entire historical state be reconstructed deterministically from immutable raw files?

---

## 2. The 15 Non-Negotiable Rules of Data Engineering

1. **Inspect Raw Data First**: Never write ingestion logic without viewing raw hex/bytes, examining delimiters, checking line breaks, and inspecting malformed rows.
2. **Define the Grain**: State explicitly what a single row represents in every dataset. Changing grain without noticing is the #1 cause of doubled metrics and flawed executive decisions.
3. **Predict Row Counts and File Sizes**: Before pressing run, calculate the expected row count and output byte volume. If you expect 10,000 rows and get 10,005, your pipeline is broken.
4. **Keep Raw Input Immutable**: Never overwrite or discard raw incoming data. Raw storage is your insurance policy; if your transformations have a bug, raw data allows you to recompute history.
5. **Make Pipelines Idempotent**: A pipeline must produce the exact same final state whether executed once, twice, or ten times with the same input. If running twice creates duplicates, the design is incomplete.
6. **Design for Reruns**: Failures are normal. Disks fill, nodes reboot, APIs rate limit. Every pipeline must be safely rerun without manual surgical database cleanups.
7. **Validate Every Output**: Pipeline success exit code `0` means only that Python did not crash. It does **NOT** mean data is correct. Always validate nullability, uniqueness, and value bounds.
8. **Reason About Schema Evolution**: Producers will change data without warning. Distinguish backward, forward, and breaking changes before schema changes reach production.
9. **Inspect Query & Compute Plans**: Do not blindly execute queries or transformations. Inspect `EXPLAIN ANALYZE` in SQL or execution DAGs in Spark to spot unindexed scans, Cartesian products, and shuffles.
10. **Break Pipelines Deliberately**: You do not understand a pipeline until you have intentionally injected duplicate keys, null values, malformed timestamps, and sudden node kills, and observed how it fails.
11. **Perform Backfills**: Never write code that only functions "from this moment forward." You will always be asked to reprocess the last 90 days or 3 years of history.
12. **Measure File and Partition Layout**: Small files kill distributed systems. Thousands of 10 KB files create catalog bottlenecks and slow queries. Compact files and choose partition keys deliberately.
13. **Never Use Spark if SQL or Local Processing Is Enough**: A single multicore machine running DuckDB or Polars can process 100 GB in seconds. Distributed compute introduces network shuffles, serialization overhead, cluster management, and massive costs.
14. **Never Stream When Batch Meets Requirements**: Streaming adds watermarks, late-data windows, state stores, and operational on-call complexity. If the business only looks at numbers every morning, an hourly or daily batch is superior.
15. **Never Accept Success Status as Proof of Correctness**: A pipeline that runs in 2 seconds and reports `SUCCESS` when 0 rows were ingested is an outage masquerading as success.

---

## 3. The Core Learning Loop

Every phase in this curriculum follows the rigorous 12-step cycle:

```text
       ┌───────────────┐
       │     SOURCE    │ Inspect raw bytes, headers, and schemas
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │    PREDICT    │ Hypothesize row count, data types, and sizes
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │     INGEST    │ Extract and stage data cleanly
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │    INSPECT    │ Examine intermediate files, partitions, and logs
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │   TRANSFORM   │ Model data: raw -> staging -> intermediate -> mart
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │    VALIDATE   │ Run automated checks: unique, not-null, range, grain
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │    MEASURE    │ Quantify rows/sec, MB scanned, execution plans
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │     BREAK     │ Inject poisons, duplicates, network drops, latency
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │    RECOVER    │ Quarantine poison rows, isolate failures, resume
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │     REPLAY    │ Backfill history, verify idempotent state
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │    EXPLAIN    │ Articulate trade-offs, architecture, and evidence
       └───────────────┘
```

---

## 4. How to Work Through This Repository

1. **Follow the Order**: The 201 phases are carefully sequenced. Do not skip to Airflow or Spark until you have built manual DAG runners, dependency orchestrators, and map-reduce shuffles from scratch.
2. **Type and Run the Code**: Do not merely read markdown files. Run the scripts, inspect the intermediate DuckDB tables, and run the automated tests.
3. **Break Things**: Complete the deliberate failure injections in each lesson. If a lesson asks you to corrupt a file, corrupt it and witness the stack trace and the quarantine behavior.
4. **Log Your Evidence**: Keep track of row counts, run durations, and test outputs in the provided `outputs/evidence-template.md` for each phase.
