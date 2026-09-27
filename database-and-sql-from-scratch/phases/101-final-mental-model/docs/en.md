# Phase 101: The Final Mental Model — Unifying Querying and Engineering

> **Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

---

## 1. The Capstone Synthesis

You have reached the culmination of `database-and-sql-from-scratch`. At this stage, you no longer see SQL as disconnected clauses or syntax templates, and you no longer view the database engine as a mysterious black box.

To prove your mastery, we trace a single production requirement along **both dimensions simultaneously**:
1. **The SQL Language Track (Declarative Query Reasoning)**
2. **The Database Engine Track (Physical Execution Mechanics)**

---

## 2. Dimension A: The SQL Language Track

### Requirement:
> *"Find the top five customers by paid revenue during the last 30 days."*

### The Relational Reasoning Chain:

```text
1. Define the Grain
   What should one output row represent?
   One customer entity with aggregated spending.
          │
          ▼
2. Identify Required Entities
   Which tables hold the facts?
   customers (customer attributes) + orders (transaction facts).
          │
          ▼
3. Determine Relationship & Cardinality
   customers (1) ───◄ orders (N)
   Join key: customers.id = orders.customer_id
          │
          ▼
4. Filter Before Grouping (Relational Selection σ)
   Keep only: orders.status = 'paid'
   Keep only: orders.order_date >= NOW() - INTERVAL '30 days'
          │
          ▼
5. Determine Grouping Grain
   Group by: customers.id, customers.email, customers.first_name, customers.last_name
          │
          ▼
6. Compute Aggregates
   SUM(orders.total_amount) AS paid_revenue
          │
          ▼
7. Order Output
   ORDER BY paid_revenue DESC, customers.id ASC (deterministic tie-breaker)
          │
          ▼
8. Slice Result
   LIMIT 5 (or FETCH FIRST 5 ROWS ONLY)
```

### The Declarative SQL:

```sql
SELECT
    c.id AS customer_id,
    c.email,
    c.first_name || ' ' || c.last_name AS customer_name,
    SUM(o.total_amount) AS paid_revenue
FROM ecommerce.customers c
JOIN ecommerce.orders o
    ON c.id = o.customer_id
WHERE o.status = 'completed'
  AND o.order_date >= NOW() - INTERVAL '30 days'
GROUP BY c.id, c.email, c.first_name, c.last_name
ORDER BY paid_revenue DESC, c.id ASC
LIMIT 5;
```

---

## 3. Dimension B: The Database Engine Track

Now trace what physically happens inside PostgreSQL 16 when this exact SQL text is submitted:

```text
               Raw SQL Text String
                        │
                        ▼
               [ 1. Query Parser ]
       Constructs Abstract Syntax Tree (AST);
       verifies grammar and token validity.
                        │
                        ▼
           [ 2. Semantic Analysis ]
       Resolves identifiers against catalog pg_class & pg_attribute;
       verifies types (e.g. total_amount is numeric).
                        │
                        ▼
             [ 3. Query Rewriter ]
       Applies view expansions, rules, and constant folding
       (e.g., evaluates NOW() - INTERVAL '30 days' once).
                        │
                        ▼
            [ 4. Query Optimizer / Planner ]
       Estimates selectivity and row counts via pg_statistic:
       - Evaluates Index Scan vs Seq Scan on orders(order_date, status)
       - Evaluates Hash Join vs Nested Loop Join with customers
       - Calculates estimated startup and total costs.
                        │
                        ▼
             [ 5. Plan Tree Selection ]
       Top-N Sort (Heapsort in work_mem)
         └── HashAggregate (Buckets on c.id)
               └── Hash Join (customers.id = orders.customer_id)
                     ├── Index Scan / Bitmap Scan on orders
                     └── Seq Scan on customers
                        │
                        ▼
               [ 6. Plan Executor ]
       - Demands rows from Buffer Pool (shared_buffers).
       - Pages read from memory cache (shared hit) or disk (read).
       - MVCC snapshot verifies xmin/xmax visibility of each tuple.
       - Discards tuples failing WHERE filter.
       - Populates in-memory hash aggregation table.
       - Pushes aggregated rows into bounded priority queue (Heapsort).
                        │
                        ▼
               [ 7. Result Materialization ]
       Emits exactly 5 tuples across TCP socket to client.
```

---

## 4. The Final Standard

You have achieved true relational competence when you can think fluently across both tracks:

```text
Requirement
     │
     ▼
Data Model
     │
     ▼
Relationships & Cardinality
     │
     ▼
Query Shape
     │
     ▼
Expected Cardinality
     │
     ▼
Indexes
     │
     ▼
Execution Plan
     │
     ▼
Concurrency Requirements
     │
     ▼
Production Performance
```

When you are given data and a question, you can query it. When the query becomes slow, you can diagnose it. When the schema becomes complicated, you can model it. And when a relational database appears inside a system architecture, you understand what it is doing and why.
