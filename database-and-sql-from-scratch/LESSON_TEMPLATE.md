# Lesson Template

Use this template when authoring or working through any lesson in `database-and-sql-from-scratch`. Every lesson is an empirical laboratory combining relational engineering intuition with rigorous SQL query mechanics.

---

```markdown
# Phase NN: [Lesson Title]

> **Motto:** [A punchy, 1-line truth anchor summarizing the core lesson insight]

**Type:** Querying | Engineering | Performance | Architecture  
**Primary Engine:** PostgreSQL 16.4 (Standard SQL vs Engine Specifics noted)  
**Dataset:** [ecommerce | social | saas | banking | analytics | scratch]  
**Prerequisites:** [Phase X, Phase Y]  
**Estimated Time:** ~[minutes] minutes  

---

## 1. The Motto

> [State the lesson motto in bold callout. Explain why this motto exists and what catastrophic failure it prevents.]

---

## 2. The Problem

[2-3 paragraphs. Introduce a concrete, high-stakes business or engineering problem.
Show what breaks, why intuition fails, or what query catastrophe occurs without this concept.]

---

## 3. Predict

Before running a single line of SQL or inspecting an engine data structure, record your prediction:

- **What should one output row represent (Grain)?**
- **How many rows do you predict will be returned?**
- **What physical access method will the engine choose? (Sequential Scan, Index Scan, Bitmap Heap Scan, Hash Join, Nested Loop)?**
- **What happens with NULLs or unmatched rows?**

---

## 4. First Principles & Relational Algebra

[Ground the concept in foundational mathematical or hardware realities:
- Codd's Relational Model & Relational Algebra (Selection $\sigma$, Projection $\pi$, Join $\bowtie$, Grouping $\gamma$)
- Hardware mechanics (8KB disk blocks, DRAM random access latency vs sequential I/O, CPU instruction cycles, memory sort buffers)]

---

## 5. Mental Model

[ASCII diagrams, relationship graphs, or row-transformation pipelines illustrating the concept before writing code.]

```text
Input Rows (N) ───────► [ Filter: WHERE ] ───────► Surviving Rows (M)
                                                          │
                                                          ▼
                                                  [ Bucket: GROUP BY ]
                                                          │
                                                          ▼
Output Rows (K) ◄────── [ Project: SELECT ] ◄───── [ Filter: HAVING ]
```

---

## 6. Model / Build It (Schema & Storage)

[Define or inspect the underlying DDL, data types, constraints, or internal layout.]

```sql
-- DDL or setup statements
```

---

## 7. Write SQL (Incremental Construction)

Follow the **14-Question SQL Query Framework**:
1. Identify output grain.
2. Select candidate tables.
3. Establish join pathways.
4. Construct query step-by-step.

```sql
-- Step 1: Base query
SELECT ...
FROM ...;

-- Step 2: Adding joins & filters
...

-- Step 3: Final formulation
...
```

---

## 8. Run It & Inspect Output

```sql
-- Production formulation
```

**Result Set:**
| column_a | column_b | column_c |
| :--- | :--- | :--- |
| ... | ... | ... |

*(Verify: Does the result match your prediction in Step 3?)*

---

## 9. Inspect It (The Engine's Plan)

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
[Your SQL Query];
```

**Key Execution Metrics:**
- **Node Type:** (e.g., `Seq Scan`, `Index Scan using idx_...`, `Hash Join`)
- **Estimated Rows vs Actual Rows:** (e.g., `rows=100 (actual rows=98)`)
- **Shared Hit / Read Blocks:** (e.g., `Buffers: shared hit=4 read=0`)
- **Execution Time:** (e.g., `0.142 ms`)

---

## 10. Measure It (Quantitative Baseline)

| Configuration | Planning Time | Execution Time | Buffer Hits | Buffer Reads | Peak Memory (work_mem) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Baseline (Unindexed) | 0.08 ms | 14.5 ms | 12 | 1420 | 0 KB |
| Optimized (Indexed)  | 0.12 ms | 0.18 ms | 4  | 0    | 0 KB |

---

## 11. Break It (Intentional Fault Injection)

[Deliberately break the query or schema to observe failure modes:
- Cartesian explosion (`JOIN` on wrong key or missing `ON`)
- `NOT IN` with a single `NULL` value
- Accidental predicate wrap: `WHERE LOWER(email) = 'x'` invalidating index
- Non-deterministic `ORDER BY` with pagination
- Concurrency deadlock under parallel transactions]

```sql
-- The Broken Query / Anti-Pattern
```

**What happened?**
*(Describe error message, incorrect row count, or planner fallback to Seq Scan)*

---

## 12. Debug It & Fix It

[Walk through diagnosing the failure from first principles, reading the query plan or error logs, and correcting the logic.]

---

## 13. Rewrite Another Way & Compare

Relational engines offer multiple ways to answer the same question. Compare your solution against an alternative (e.g., `JOIN` vs `EXISTS`, `Correlated Subquery` vs `Window Function`, `CASE Aggregation` vs `FILTER` clause).

| Aspect | Formulation A (e.g., Window Function) | Formulation B (e.g., Correlated Subquery) |
| :--- | :--- | :--- |
| **Readability** | High | Low |
| **Execution Cost** | Cost: 24.50 | Cost: 1890.20 |
| **Portability** | Standard SQL:2003+ | Standard SQL:92 |

---

## 14. Evidence Ledger

Document your empirical findings:

```text
Lesson: Phase NN — [Title]
Date: YYYY-MM-DD
PostgreSQL Version: 16.4
Requirement: [User business question]
Grain (1 Result Row): [What it represents]
Tables Used: [table1, table2]
Prediction: [Rows expected & scan type]
Actual Rows Returned: [Count]
Plan Nodes Observed: [Hash Join -> Seq Scan]
Intentional Breakage: [What was broken and how it behaved]
Optimization Impact: [Speedup or memory delta]
Key Takeaway: [Core insight in your own words]
```

---

## 15. Exercises

- **Level 1 (Direct):** [Fundamental application of the clause/engine property]
- **Level 2 (Combination):** [Combines current topic with prior phases]
- **Level 3 (Edge Case):** [Tests NULLs, empty sets, or duplicate keys]
- **Level 4 (Realistic):** [Messy real-world business schema requirement]
- **Level 5 (Performance-Aware):** [Optimize plan from Seq Scan to Index Scan / minimize buffer reads]
```
