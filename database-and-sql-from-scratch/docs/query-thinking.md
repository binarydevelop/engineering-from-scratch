# The SQL Query Thinking Framework

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

---

## Introduction: Why Most People Struggle with SQL

Novices approach SQL as a text-manipulation problem: they read an English question, guess a few keywords (`SELECT`, `JOIN`, `WHERE`), run the query, see incorrect rows, and randomly add `DISTINCT` or `GROUP BY` until the output "looks about right."

This is known as **cargo-cult SQL**. It produces queries that are subtly wrong, vulnerable to edge cases, and catastrophic to production database performance.

A senior relational engineer never guesses SQL syntax. Instead, they run an internal 14-question mental compiler that translates business intent into relational algebra, determines the exact mathematical shape of the result set, and then writes the declarative query.

---

## The 14-Question Query Thinking Framework

Whenever you are tasked with authoring an analytical query, reporting pipeline, or transactional lookup, work through these 14 questions in order:

```text
 1. What should one output row represent (Grain)?
 2. Which tables contain the required facts?
 3. How are those tables related?
 4. What rows should be filtered before grouping (WHERE)?
 5. Do I need grouping (bucketing)?
 6. Do I need aggregation (collapsing rows into summaries)?
 7. Do I need calculations across rows (window functions)?
 8. Do I need ranking (ties, dense vs sparse)?
 9. Do I need existence or non-existence checks (EXISTS / NOT EXISTS)?
10. What ordering is required (deterministic tie-breakers)?
11. Could joins duplicate rows (1:N or N:M cardinality explosions)?
12. What happens with NULL (three-valued logic, outer joins, aggregates)?
13. What edge cases exist (zero orders, missing dates, refund reversions)?
14. How will this query behave as data grows from 1,000 to 10,000,000 rows?
```

---

## Deep Dive: The 14 Questions

### 1. What should one output row represent (The Grain)?
The **Grain** is the atomic identity of a single row in the final result set.
- Is one row a *customer*?
- A *customer per calendar month*?
- An *order item*?
- A *product category*?

> **Rule:** If you cannot state the grain of your result set in one concise sentence, you are not ready to write `SELECT`.

### 2. Which tables contain the required facts?
Identify which entity tables hold the attributes you need for:
- Projection (columns to display)
- Filtering (conditions in `WHERE` or `HAVING`)
- Grouping (`GROUP BY` keys)
- Ordering (`ORDER BY` fields)

### 3. How are those tables related?
Trace the join paths through foreign keys:
- `orders.customer_id -> customers.id` (Many-to-One)
- `orders.id <- order_items.order_id` (One-to-Many)
- `order_items.product_id -> products.id` (Many-to-One)

### 4. What rows should be filtered before grouping (WHERE)?
Filter as early as possible. The `WHERE` clause eliminates rows *before* any costly grouping, hashing, or sorting takes place in the engine.
- Exclude cancelled orders: `WHERE status != 'cancelled'`
- Restrict date ranges: `WHERE created_at >= '2026-01-01'`

### 5. Do I need grouping?
Grouping changes the grain of your data. If your input tables are at the *order* grain, but your desired output grain is *customer*, you must group by `customer_id`.

### 6. Do I need aggregation?
Once you group, every column in your `SELECT` must either be in the `GROUP BY` clause or wrapped in an aggregate function (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`).
- *Pitfall:* `COUNT(column)` ignores `NULL`s, whereas `COUNT(*)` counts all physical rows.

### 7. Do I need calculations across rows (Window Functions)?
If you need to calculate running totals, moving averages, or compare a row to its predecessor (`LAG`) *without collapsing individual rows*, do NOT use `GROUP BY`. Use window functions with `OVER (...)`.

### 8. Do I need ranking?
When asked for "Top 3 per group":
- `ROW_NUMBER()`: Strictly sequential (1, 2, 3, 4) — arbitrates ties arbitrarily unless tied by secondary sort keys.
- `RANK()`: Leaves gaps on ties (1, 2, 2, 4).
- `DENSE_RANK()`: No gaps on ties (1, 2, 2, 3).

### 9. Do I need existence or non-existence checks?
If you need to answer "Which customers have never placed an order?" or "Which products have at least one return?":
- Prefer `EXISTS` and `NOT EXISTS` with correlated subqueries over `IN` / `NOT IN`.
- `NOT IN` returns zero rows if the subquery returns even a single `NULL`!

### 10. What ordering is required?
Relational tables are unordered mathematical bags of tuples. The engine makes **zero guarantees** about row order unless you supply an explicit `ORDER BY`.
- Always add a unique secondary tie-breaker (such as primary key `id`) for deterministic output.

### 11. Could joins duplicate rows (Cardinality Multiplication)?
If table `A` joins to table `B` on a 1-to-many relationship, and you join again to table `C` on another 1-to-many relationship, you create an $N \times M$ Cartesian explosion.
- Symptoms: `SUM(amount)` returns 4x the expected revenue.
- *Fix:* Aggregate before joining, or use CTEs to isolate row grains.

### 12. What happens with NULL?
In relational databases, `NULL` represents unknown or absent information, governed by **Three-Valued Logic** (`TRUE`, `FALSE`, `UNKNOWN`).
- `col = NULL` evaluates to `UNKNOWN`, never `TRUE`. Always use `col IS NULL`.
- `WHERE col != 'active'` will quietly drop all rows where `col IS NULL`.

### 13. What edge cases exist?
- What if an entity has 0 child records? (Use `LEFT JOIN` instead of `INNER JOIN`).
- What if a category has no sales this month? (Handle with `COALESCE(SUM(revenue), 0)`).
- What if dates have gaps? (Generate a date scaffold using `generate_series`).

### 14. How will this query behave as data grows?
Will this query force a sequential scan across 50,000,000 rows? Will an unindexed foreign key cause a Nested Loop join to stall CPU cores? Can an index provide index-only scan access?

---

## End-to-End Walkthrough: Applying the Framework

### Requirement:
> *"Find the top 3 customers by total completed revenue in each city over the last 90 days, including their city, customer name, total spent, and rank. Exclude refunded orders."*

#### Applying the 14 Questions:

1. **Output Grain:** One row represents *one customer within their city ranking*.
2. **Tables Required:** `customers` (id, name, city_id), `cities` (id, name), `orders` (id, customer_id, status, created_at, total_amount).
3. **Relationships:**
   - `cities.id <- customers.city_id` (1:N)
   - `customers.id <- orders.customer_id` (1:N)
4. **Filters (WHERE):**
   - `orders.status = 'completed'` (excludes refunded or pending)
   - `orders.created_at >= NOW() - INTERVAL '90 days'`
5. **Grouping:** Group at `(customers.id, customers.name, cities.name)` to calculate customer spending.
6. **Aggregation:** `SUM(orders.total_amount) AS total_spent`.
7. **Calculations Across Rows:** Need ranking within each city.
8. **Ranking:** Top 3 per city -> `DENSE_RANK() OVER (PARTITION BY city_name ORDER BY total_spent DESC) AS rnk`.
9. **Existence:** Handled via join filters.
10. **Ordering:** `ORDER BY city_name ASC, rnk ASC, customer_name ASC`.
11. **Join Duplication:** `customers` -> `orders` is 1:N. Aggregating by customer collapses orders correctly without inflating other tables.
12. **NULLs:** What if a customer has no orders? Requirement asks for top spenders; customers with no completed orders in 90 days have 0 revenue and should not appear. `INNER JOIN` is appropriate.
13. **Edge Cases:** Ties in total spent handled by `DENSE_RANK()`.
14. **Scale:** Index on `orders(customer_id, created_at, status)` enables fast index scans.

#### Incremental Query Construction:

```sql
WITH customer_spending AS (
    SELECT
        c.city_id,
        ci.name AS city_name,
        c.id AS customer_id,
        c.name AS customer_name,
        SUM(o.total_amount) AS total_spent
    FROM customers c
    JOIN cities ci
        ON c.city_id = ci.id
    JOIN orders o
        ON c.id = o.customer_id
    WHERE o.status = 'completed'
      AND o.created_at >= NOW() - INTERVAL '90 days'
    GROUP BY c.city_id, ci.name, c.id, c.name
),
ranked_customers AS (
    SELECT
        city_name,
        customer_name,
        total_spent,
        DENSE_RANK() OVER (
            PARTITION BY city_id 
            ORDER BY total_spent DESC
        ) AS spending_rank
    FROM customer_spending
)
SELECT
    city_name,
    customer_name,
    total_spent,
    spending_rank
FROM ranked_customers
WHERE spending_rank <= 3
ORDER BY city_name ASC, spending_rank ASC, customer_name ASC;
```

Notice how the final SQL flowed naturally and defensively from answering the 14 questions. You never had to guess or fiddle with syntax.
