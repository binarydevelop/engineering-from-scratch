# SQL Language Reference: Standard vs PostgreSQL

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

---

## 1. Logical SQL Processing Order

Although SQL is written in one order, the relational engine logically processes clauses in a fundamentally different order:

```text
WRITTEN ORDER                        LOGICAL PROCESSING ORDER
─────────────                        ────────────────────────
1. SELECT                            1. FROM & JOINs (identifies data source)
2. FROM & JOIN                       2. ON (evaluates join predicates)
3. WHERE                             3. WHERE (filters rows before aggregation)
4. GROUP BY                          4. GROUP BY (partitions rows into buckets)
5. HAVING                            5. HAVING (filters aggregated buckets)
6. WINDOW (OVER)                     6. SELECT & WINDOW (projects columns & computes windows)
7. DISTINCT                          7. DISTINCT (eliminates duplicate result rows)
8. UNION / INTERSECT / EXCEPT        8. SET OPERATIONS (combines result sets)
9. ORDER BY                          9. ORDER BY (sorts the final projected rows)
10. LIMIT / OFFSET                   10. LIMIT / OFFSET (slices final output rows)
```

> **Why this matters:**
> - You cannot use a column alias declared in `SELECT` inside `WHERE`, because `WHERE` executes *before* `SELECT`.
> - Window functions cannot be placed in `WHERE` or `HAVING`, because window functions execute *after* grouping.

---

## 2. Standard SQL Clauses & Grammar

### SELECT & Projection
```sql
SELECT
    column_1,
    column_2 * 1.10 AS adjusted_price,
    COALESCE(discount, 0) AS safe_discount,
    CASE
        WHEN status = 'active' THEN 'Live'
        ELSE 'Inactive'
    END AS status_label
FROM table_name;
```

### Filtering & Three-Valued Predicates
```sql
WHERE created_at >= '2026-01-01'
  AND (status = 'paid' OR amount > 1000)
  AND category_id IN (1, 2, 5)
  AND deleted_at IS NULL
  AND name LIKE 'A%';
```

### Joining Relations
```sql
-- Inner Join: matched pairs only
FROM orders o
JOIN customers c ON o.customer_id = c.id

-- Left Outer Join: preserves all left rows, NULLs unmatched right
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id

-- Full Outer Join: preserves all rows from both relations
FROM department d
FULL JOIN employee e ON d.id = e.department_id
```

### Aggregations & Grouping
```sql
SELECT
    department_id,
    COUNT(*) AS total_employees,
    COUNT(commission) AS employees_with_commission,
    SUM(salary) AS total_payroll,
    ROUND(AVG(salary), 2) AS average_salary
FROM employees
GROUP BY department_id
HAVING COUNT(*) > 5;
```

### Common Table Expressions (CTEs)
```sql
WITH regional_sales AS (
    SELECT region, SUM(amount) AS total_sales
    FROM orders
    GROUP BY region
),
top_regions AS (
    SELECT region
    FROM regional_sales
    WHERE total_sales > 100000
)
SELECT * FROM top_regions;
```

### Window Functions
```sql
SELECT
    department_id,
    employee_name,
    salary,
    -- Ranking
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS row_num,
    DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank,
    -- Running Total
    SUM(salary) OVER (
        PARTITION BY department_id 
        ORDER BY hire_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_salary,
    -- Lag/Lead
    LAG(salary, 1) OVER (PARTITION BY department_id ORDER BY hire_date) AS prev_salary
FROM employees;
```

---

## 3. PostgreSQL-Specific Features & Extensions

| Feature | PostgreSQL Syntax | Standard SQL / Alternative Equivalent |
| :--- | :--- | :--- |
| **Case-Insensitive Regex / Like** | `name ILIKE '%pro%'` | `LOWER(name) LIKE '%pro%'` |
| **Upsert (On Conflict)** | `INSERT INTO t VALUES (...) ON CONFLICT (id) DO UPDATE SET val = EXCLUDED.val` | `MERGE INTO ...` (Standard SQL:2003, supported in PG 15+) |
| **DML Returning** | `INSERT INTO orders (...) VALUES (...) RETURNING id, created_at;` | Multiple statements (`SELECT currval()` or secondary query) |
| **Distinct On** | `SELECT DISTINCT ON (customer_id) * FROM orders ORDER BY customer_id, order_date DESC;` | CTE with `ROW_NUMBER() OVER (...) WHERE row_num = 1` |
| **Array & Date Generation** | `SELECT * FROM generate_series('2026-01-01'::date, '2026-01-31'::date, '1 day');` | Recursive CTE with `UNION ALL` |
| **JSONB Operators** | `data->'address'->>'city'`, `data @> '{"role": "admin"}'` | `JSON_VALUE()`, `JSON_QUERY()` (SQL:2016) |
