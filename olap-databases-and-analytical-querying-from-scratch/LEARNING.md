# The Analytical Engineering Learning Guide

> **Motto**: Understand it. Model it. Query it. Scan it. Aggregate it. Measure it. Break it. Optimize it. Scale it.

Welcome to **OLAP Databases and Analytical Querying from Scratch**. This curriculum is designed to transform you into an engineer who understands both **how to write the analytical query** and **why the underlying storage and execution engine can process it efficiently**.

---

## 1. The Core Analytical Query Loop

Never write an analytical query, hit `Enter`, glance at the output table, and move on. Every exercise and lesson must execute this rigorous cognitive loop:

```text
                  1. ANALYTICAL QUESTION
                             │
                             ▼
                    2. DEFINE INPUT GRAIN
                (What does ONE row represent?)
                             │
                             ▼
                   3. PREDICT RESULT SHAPE
                 (Output grain & row count)
                             │
                             ▼
                  4. PREDICT PHYSICAL WORK
         (Which columns? Which blocks? Memory size?)
                             │
                             ▼
                    5. WRITE THE QUERY
                             │
                             ▼
                  6. RUN & INSPECT THE PLAN
                    (EXPLAIN ANALYZE / marks)
                             │
                             ▼
                   7. MEASURE PHYSICAL WORK
                (Bytes scanned vs tuples returned)
                             │
                             ▼
                    8. BREAK IT ON PURPOSE
              (Inject anti-pattern: SELECT *, unpruned)
                             │
                             ▼
                  9. OPTIMIZE STORAGE LAYOUT
             (Sort order, compression, projection)
                             │
                             ▼
                 10. MEASURE THE SPEEDUP
                             │
                             ▼
                 11. EXPLAIN FROM FIRST PRINCIPLES
```

---

## 2. The 15 Cardinal Invariants for the Learner

1. **Define the Grain First**: Never write `JOIN` or `GROUP BY` without knowing what exactly one row represents in the input, and what one row represents in the output.
2. **Predict the Result Shape**: Before running a query, state whether you expect 10 rows, 10,000 rows, or 10,000,000 rows.
3. **Predict Physical Work**: Before inspecting the plan, predict: *Which columns are touched? How many partitions are scanned? Does the aggregation hash table fit in L3 cache?*
4. **Inspect Query Plans Routinely**: Use `EXPLAIN` and `EXPLAIN ANALYZE` on DuckDB, ClickHouse, and PostgreSQL. Trace every operator.
5. **Measure Bytes, Not Just Latency**: Fast latency on a warm cache can deceive you. Physical bytes read from disk reveals true efficiency.
6. **Understand Compression**: Values of the same type sitting together compress 10× better. Sort keys dictate RLE and dictionary efficiency.
7. **Verify Partition Pruning**: If your table has 60 months of data and your query asks for last week, verify that 59 months of partitions were untouched.
8. **Verify Data Skipping**: Zone maps (min/max) and sparse marks skip blocks only if your query filters on the sort key hierarchy.
9. **Never Assume an Index Helps**: In columnar systems, sequential SIMD scans of compressed vectors are often 10× faster than random pointer chasing through dense secondary indexes.
10. **Understand Sorting & Order Keys**: In ClickHouse and Parquet, the sort key is your primary skipping weapon. Choose it based on filter frequency and selectivity.
11. **Test High Cardinality**: Aggregating on `country` (6 values) behaves completely differently than aggregating on `user_id` (10,000,000 values). Measure memory and spill.
12. **Measure Query Concurrency**: A database that runs 1 query in 10ms might collapse when 100 users hit it concurrently. Measure queue depths and admission control.
13. **Compare Raw vs Materialized Data**: Pre-aggregation via Materialized Views makes dashboards fast, but permanently sacrifices ad-hoc exploratory flexibility.
14. **Distinguish Ingestion Latency from Query Latency**: Streaming ingestion requires seconds freshness; analytical queries require sub-second scan speeds. Do not compromise query speed for unnecessary ingestion micro-updates.
15. **Repeatedly Ask: Is PostgreSQL or DuckDB Enough?**: If your dataset is 15 GB, do NOT deploy a distributed ClickHouse or Druid cluster. DuckDB or PostgreSQL with a BRIN index is simpler, cheaper, and faster to operate.

---

## 3. How to Complete a Phase

1. Open `phases/XX-[topic]/README.md`.
2. Read the **Problem**, **Input Grain**, and **Output Grain**.
3. Write your **Prediction** in your engineering notebook.
4. Run the code harness:
   ```bash
   .venv/bin/python phases/XX-[topic]/run.py
   ```
5. Inspect the execution plan via `EXPLAIN ANALYZE`.
6. Break the query by introducing the documented anti-pattern, then optimize it.
7. Fill out the **Evidence Artifact** and answer the **Questions for Mastery**.
