# Project 07: Production Database Application & Chaos Lab

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

---

## 1. Project Overview

This project bridges application software engineering and database engineering by constructing a production-like database access layer:
- **Connection Pooling:** Lifecycle management with min/max pool sizing.
- **Safe Query Layer:** Parameterized queries to eliminate SQL injection vulnerabilities.
- **Atomic Transactions:** Atomic multi-statement operations with rollback guarantees.
- **Migrations:** Sequential schema evolution (`001_initial_schema.sql`, `002_add_indexes.sql`).
- **Chaos Experiments:** Reproducing and diagnosing the 5 classic production failure modes (deadlocks, pool starvation, slow sequential scans, missing foreign key lock escalations, and hot row contention).

---

## 2. Running the Application & Chaos Lab

```bash
python3 projects/07-production-db-app/app.py
python3 projects/07-production-db-app/chaos_experiments.py
```
