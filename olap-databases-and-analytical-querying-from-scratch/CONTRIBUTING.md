# Contributing to OLAP Databases and Analytical Querying from Scratch

Thank you for contributing to this educational repository. Our mission is to teach the first principles of OLAP database engineering and analytical query fluency with mechanical rigor.

---

## Core Philosophy

Every lesson, exercise, and benchmark must adhere to our motto:

> **Understand it. Model it. Query it. Scan it. Aggregate it. Measure it. Break it. Optimize it. Scale it.**

We never teach a database command in isolation without first deriving the architectural problem it solves from first principles.

---

## 1. The Evidence Rule

1. **No Unverified Claims**: Never write "ClickHouse is 100x faster than PostgreSQL" or "DuckDB is the best analytical engine."
2. **Every Claim Must Include**:
   - Hardware specifications (CPU, RAM, Storage type)
   - Database versions (pinned in `VERSIONS.md`)
   - Dataset details (row count, columns, distributions, uncompressed/compressed sizes)
   - Cache state (Cold vs Warm)
   - Measured physical metrics (wall-clock latency, rows scanned, bytes read, memory allocated, CPU time)
3. **No "Benchmark Theater"**: Benchmarks designed to make one engine artificially fail or win without explaining workload mismatch will be rejected.

---

## 2. Adding or Modifying a Lesson

1. Every lesson must follow the strict 21-section structure defined in `LESSON_TEMPLATE.md`.
2. Every lesson must explicitly specify:
   - **Input Grain**: Exactly what one row in the source dataset represents.
   - **Output Grain**: Exactly what one row in the output represents.
   - **Prediction**: What physical work is expected before execution.
   - **Physical Plan**: Detailed plan analysis (`EXPLAIN ANALYZE`).
   - **Break It**: An intentional failure or performance anti-pattern.
   - **Optimize It**: The architectural cure with before/after metric comparisons.
   - **Evidence Artifact**: Fully filled evidence log.

---

## 3. Adding Analytical SQL Exercises

1. New exercises must follow `QUERY_TEMPLATE.md`.
2. Solutions must be placed in `solutions/sql-exercises/` or `solutions/drills/`, never inline in the exercise problem statement.
3. Every exercise must specify dialect suitability (ANSI, DuckDB, ClickHouse, PostgreSQL) and physical performance sensitivities.

---

## 4. Code Standards

- **Python**: PEP 8 compliant, type-annotated, compatible with Python 3.11+. Use the virtual environment in `.venv/`.
- **SQL**: Upper-case keywords (`SELECT`, `WHERE`, `GROUP BY`), lower-case column/table identifiers, indented CTEs and subqueries.
- **Docker**: All images must be pinned with exact version tags in `docker-compose.yml`.

---

## 5. Verification Commands

Before opening a Pull Request:
```bash
# Verify environment and dependencies
./scripts/check-environment.sh

# Run analytical test suite
.venv/bin/pytest tests/

# Validate data generation
.venv/bin/python scripts/generate-data.py --scale small
```
