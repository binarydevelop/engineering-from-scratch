# Project 01: Complete E-Commerce Database Engineering & Business Intelligence

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

---

## 1. Project Overview

This project implements an end-to-end, production-grade e-commerce database system. You will not only model the physical schema and enforce relational constraints, but also author 30 core business queries, execute ACID checkout transactions with concurrency safeguards, and optimize slow execution plans.

---

## 2. Relational Architecture

The database model consists of 9 normalized relations:
1. `customers`: User accounts with email uniqueness and status constraints.
2. `addresses`: Multiple shipping destinations per customer with default flags.
3. `categories`: Self-referencing hierarchical product taxonomy.
4. `products`: Catalog items with SKU uniqueness, price/cost constraints, and soft deletion.
5. `inventory`: Strict non-negative inventory balances with reorder thresholds.
6. `orders`: Purchase orders tracking state transitions (`pending` -> `paid` -> `completed` -> `refunded`).
7. `order_items`: Order line items with generated subtotals and foreign key constraints.
8. `payments`: Payment gateway transaction logs with idempotency references.
9. `refunds`: Financial reversal records linked to orders and original payments.

---

## 3. Included Deliverables

- `schema.sql`: Full DDL with primary keys, foreign keys, cascading deletes, check constraints, and generated columns.
- `transactions.sql`: Atomic checkout transaction flow demonstrating inventory reservation, payment authorization, and failure rollback.
- `optimization.sql`: Query optimization lab demonstrating before/after execution plans with B-tree indexing.
- `queries/30_business_queries.sql`: 30 production business queries answering catalog, sales, customer, and financial questions.

---

## 4. Running the Project

```bash
# Provision the database and load schema + seed
make seed-ecommerce

# Execute the 30 business queries
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab < projects/01-ecommerce-database/queries/30_business_queries.sql
```
