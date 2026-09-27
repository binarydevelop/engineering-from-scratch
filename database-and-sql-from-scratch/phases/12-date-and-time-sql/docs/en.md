# Phase 12: Date And Time Sql

> **Motto:** Time without timezone awareness is ambiguous; timestamps without intervals are useless.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 11  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **Time without timezone awareness is ambiguous; timestamps without intervals are useless.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

Storing timestamps in UTC without understanding timezone offsets causes reporting discrepancies across calendar days.

When engineers operate on blind assumptions, queries return incorrect grain, Cartesian duplicates slip into reports, and database CPU saturates under unexpected sequential scans.

---

## 3. Predict

Before executing any queries in this phase:
- What should one output row represent (Grain)?
- How many rows do you predict will be returned?
- Will the planner choose an Index Scan, Bitmap Heap Scan, or Sequential Scan?
- How will the query handle edge cases and NULL values?

---

## 4. First Principles & Relational Algebra

Epoch timestamps (seconds since 1970-01-01 UTC) vs calendar date representations with leap seconds and daylight savings.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
Timestamp with Time Zone ──► Stored as UTC Epoch ──► Formatted to Client Session Timezone
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
SELECT DATE_TRUNC('month', order_date)::DATE AS sales_month, SUM(total_amount) AS revenue FROM ecommerce.orders WHERE status = 'completed' GROUP BY 1 ORDER BY sales_month ASC;
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "SELECT DATE_TRUNC('month', order_date)::DATE AS sales_month, SUM(total_amount) AS revenue FROM ecommerce.orders WHERE status = 'completed' GROUP BY 1 ORDER BY sales_month ASC;"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
SELECT DATE_TRUNC('month', order_date)::DATE AS sales_month, SUM(total_amount) AS revenue FROM ecommerce.orders WHERE status = 'completed' GROUP BY 1 ORDER BY sales_month ASC;;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
SELECT * FROM ecommerce.orders WHERE order_date = '2026-02-01'; -- Fails to match rows with non-zero time!
```

---

## 10. Debug It & Fix It

Use half-open ranges: [start, end) for robust timestamp filtering.

---

## 11. Evidence Ledger

```text
Lesson: Phase 12 — Date And Time Sql
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: Time without timezone awareness is ambiguous; timestamps without intervals are useless.
```

---

## 12. Exercises

Level 1: Extract year.
Level 5: Generate date scaffolds using generate_series to catch missing days.
