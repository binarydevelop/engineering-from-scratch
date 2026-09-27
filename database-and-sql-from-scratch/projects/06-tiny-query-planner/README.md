# Project 06: Build a Tiny Relational Query Planner & Cost Estimator

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

---

## 1. Project Overview

This project implements the mathematical cost estimation engine that sits at the center of modern relational optimizers like PostgreSQL:
- **Cost Parameters:** `seq_page_cost`, `random_page_cost`, `cpu_tuple_cost`, and `cpu_operator_cost`.
- **Scan Decision:** Demonstrates why Sequential Scan beats Index Scan when selectivity exceeds 15-20% (proving that Sequential Scan is an intentional optimization, not a database failure).
- **Join Decision:** Chooses between Nested Loop Join (for small outer sets with indexed inner tables) and Hash Join (for large unsorted datasets).

---

## 2. Running Tests

```bash
python3 projects/06-tiny-query-planner/test_planner.py
```
