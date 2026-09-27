# Data Lineage and Provenance

> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.

Data lineage is the directed provenance graph tracking the origin, movements, transformations, and consumption of data across an organization.

---

## 1. Why Lineage Matters

When an executive asks: *"Why did the Monthly Recurring Revenue (MRR) metric drop by 15% this morning?"*, without lineage, the data engineering team enters hours of panic:
- Which pipeline updated the mart?
- What raw tables fed into that model?
- Did a backend engineer deploy an application update that modified the upstream `payments` table?
- Which dashboards and machine learning models are impacted right now?

Lineage answers two fundamental operational questions:
1. **Upstream Root Cause Analysis**: Where did this number come from, and what changed upstream to cause this anomaly?
2. **Downstream Impact Analysis**: If we drop or modify column `tax_cents` in table `orders`, what dashboards, downstream pipelines, and ML feature stores will break?

---

## 2. Levels of Lineage

```text
       ┌────────────────────────────────────────────────────────┐
       │ 1. SYSTEM LEVEL: PostgreSQL -> Kafka -> S3 -> DuckDB   │
       ├────────────────────────────────────────────────────────┤
       │ 2. DATASET LEVEL: raw_orders -> stg_orders -> fact_ord │
       ├────────────────────────────────────────────────────────┤
       │ 3. COLUMN LEVEL: raw_orders.amount -> fact_orders.rev  │
       └────────────────────────────────────────────────────────┘
```

1. **System / Infrastructure Lineage**: Maps data across physical nodes and network boundaries (e.g., PostgreSQL CDC -> Kafka topic `orders` -> S3 bronze bucket -> Snowflake).
2. **Dataset / Table Lineage**: Maps dataset dependencies inside transformations (e.g., `stg_orders` and `stg_users` join to produce `fact_orders`).
3. **Column-Level Lineage**: The highest level of precision. Tracks how individual output columns are derived from source columns through mathematical operations, CASE statements, and aggregations.

---

## 3. Extracting Lineage: Approaches

- **Static SQL AST Parsing**: Analyzing SQL `SELECT` queries with an AST parser (such as `sqlparse` or Python AST) to extract input tables, joined aliases, and projection columns.
- **Transformation Framework Metadata**: Tools like `dbt` compile lineage automatically from `ref()` and `source()` macro calls.
- **Runtime Query Engine Logs**: Distributed query engines (Spark, Trino) emit query plans with input and output dataset catalogs (e.g., OpenLineage protocol).
