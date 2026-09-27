# Contributing to Database and SQL from Scratch

Thank you for your interest in improving `database-and-sql-from-scratch`! We welcome contributions that maintain our high standards of empirical rigor, pedagogical clarity, and dual-track relational engineering.

---

## 1. Core Principles for Contributions

1. **No Superficial Syntax Dumps:** Every lesson must follow [`LESSON_TEMPLATE.md`](LESSON_TEMPLATE.md) and include a clear problem, mental model, prediction step, plan inspection, intentional breakage, and evidence ledger.
2. **PostgreSQL 16.4 Pinned Standards:** All SQL must execute against PostgreSQL 16.4. Standard SQL features must be clearly differentiated from Postgres-specific extensions and implementation details (see [`VERSIONS.md`](VERSIONS.md)).
3. **Deterministic Results:** Any new exercises, seeds, or drills must yield deterministic output rows with explicit `ORDER BY` clauses where row order matters.
4. **Separation of Exercises and Solutions:** Problem descriptions, schemas, and expected outputs belong in `exercises/` or `drills/`. Reference answers belong strictly in `solutions/`.

---

## 2. Repository Structure & Naming Conventions

- **Phases:** `phases/NN-topic-name/` containing `docs/en.md`, `code/`, `experiments/`, and `outputs/`.
- **Exercises:**
  - `exercises/beginner/q01-title.md`
  - `exercises/intermediate/q50-title.md`
  - `exercises/advanced/q100-title.md`
  - `exercises/challenge/q140-title.md`
- **Solutions:** Exact matching paths under `solutions/` (e.g., `solutions/beginner/q01-title.sql`).
- **Drills:** `drills/01-join-drills/drill-01.md` with solutions in `solutions/drills/01-join-drills/drill-01.sql`.

---

## 3. SQL Style Guide

We adhere to the readable SQL format detailed in Phase 92:
- Keywords in `UPPERCASE` (`SELECT`, `FROM`, `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`).
- Identifiers in `snake_case` (`user_id`, `created_at`, `order_items`).
- Explicit column aliasing using `AS`.
- Meaningful table aliases (e.g., `users u JOIN orders o ON ...` rather than `t1`, `t2`).
- 4-space indentation for clauses and expressions.
- Every join condition on its own line:
  ```sql
  SELECT
      u.id AS user_id,
      u.email,
      COUNT(o.id) AS total_orders
  FROM users u
  LEFT JOIN orders o
      ON u.id = o.user_id
      AND o.status = 'completed'
  WHERE u.created_at >= '2026-01-01'
  GROUP BY u.id, u.email
  ORDER BY total_orders DESC, u.id ASC;
  ```

---

## 4. Verification Workflow

Before submitting a PR:
1. Run environment verification: `make env`
2. Validate datasets & migrations: `make reset && make seed`
3. Verify all drills: `make drills`
4. Run project test suites: `make test`
