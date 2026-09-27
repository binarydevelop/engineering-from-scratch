# Phase 00: Environment And Sql Lab

> **Motto:** Your terminal is your microscope; understand every layer between your keystroke and the engine.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 00  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **Your terminal is your microscope; understand every layer between your keystroke and the engine.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

Without knowing how psql talks to PostgreSQL, you cannot distinguish client disconnects from server crashes or network latency from query execution.

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

psql client connects via TCP port 5432 to postmaster daemon, spawning a dedicated backend process per connection.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
Client (psql) -> TCP Socket (5432) -> Postmaster -> Backend Process -> Buffer Pool -> Disk Pages
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
SELECT version();
SELECT current_database();
SELECT current_user;
SELECT inet_server_addr(), inet_server_port();
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "SELECT version();"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
SELECT version();
SELECT current_database();
SELECT current_user;
SELECT inet_server_addr(), inet_server_port();;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
-- Connect with wrong user or port
-- psql -h localhost -p 9999 -U unknown_user
```

---

## 10. Debug It & Fix It

Verify port listening and pg_hba.conf host-based authentication rules.

---

## 11. Evidence Ledger

```text
Lesson: Phase 00 — Environment And Sql Lab
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: Your terminal is your microscope; understand every layer between your keystroke and the engine.
```

---

## 12. Exercises

Level 1: Inspect server version and uptime.
Level 5: Measure TCP socket connection establishment latency.
