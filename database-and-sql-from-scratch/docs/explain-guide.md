# The Definitive Guide to EXPLAIN and EXPLAIN ANALYZE

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

---

## 1. Why EXPLAIN Matters

In software engineering, you would never profile an application without measuring CPU cycles, stack traces, and heap allocations. Yet many developers deploy SQL queries completely blind to how the database engine executes them.

`EXPLAIN` opens the hood of the database engine. It reveals:
1. Which access methods were chosen (sequential scan, index scan, bitmap scan).
2. Which join algorithms were selected (hash join, merge join, nested loop).
3. How many rows the planner *estimated* vs how many rows were *actually* returned.
4. How many 8KB pages were read from memory (`shared hit`) vs read from physical disk (`read`).
5. Whether sorts and hash aggregations stayed in fast RAM (`work_mem`) or spilled to slow disk.

---

## 2. Command Syntax: EXPLAIN vs EXPLAIN ANALYZE

```sql
-- 1. Planner Estimate Only (Zero execution, safe for heavy writes)
EXPLAIN (COSTS, VERBOSE)
SELECT * FROM orders WHERE total_amount > 500;

-- 2. Full Execution with Timing and Buffer Statistics (Gold Standard)
EXPLAIN (ANALYZE, BUFFERS, TIMING, COSTS, VERBOSE)
SELECT * FROM orders WHERE total_amount > 500;
```

> [!WARNING]
> `EXPLAIN ANALYZE` **actually executes** the query! If you run `EXPLAIN ANALYZE DELETE FROM orders;`, those rows will be deleted. Always wrap experimental modifications in a transaction and roll back:
> ```sql
> BEGIN;
> EXPLAIN ANALYZE DELETE FROM orders WHERE status = 'expired';
> ROLLBACK;
> ```

---

## 3. Anatomy of an EXPLAIN Output

Consider this example plan:

```text
Hash Join  (cost=12.50..45.80 rows=25 width=72) (actual time=0.124..0.345 rows=28 loops=1)
  Hash Cond: (o.customer_id = c.id)
  Buffers: shared hit=8 read=2
  ->  Seq Scan on orders o  (cost=0.00..28.50 rows=150 width=40) (actual time=0.012..0.150 rows=150 loops=1)
        Filter: (status = 'completed')
        Rows Removed by Filter: 50
        Buffers: shared hit=4 read=2
  ->  Hash  (cost=10.00..10.00 rows=200 width=36) (actual time=0.080..0.080 rows=200 loops=1)
        Buckets: 1024  Batches: 1  Memory Usage: 18kB
        Buffers: shared hit=4
        ->  Seq Scan on customers c  (cost=0.00..10.00 rows=200 width=36) (actual time=0.008..0.050 rows=200 loops=1)
              Buffers: shared hit=4
Planning Time: 0.180 ms
Execution Time: 0.410 ms
```

### Breaking Down the Metrics:

1. **`cost=12.50..45.80`:**
   - `12.50`: **Startup Cost** — The cost before the node can output its first row (e.g., building the hash table).
   - `45.80`: **Total Cost** — The estimated cost to return all rows. Measured in arbitrary cost units where 1.0 = cost of reading one 8KB page sequentially (`seq_page_cost`).
2. **`rows=25`:** Estimated number of output rows calculated from statistical histograms (`pg_statistic`).
3. **`actual time=0.124..0.345`:** Real wall-clock time in milliseconds (first row returned at 0.124ms, complete at 0.345ms).
4. **`actual rows=28 loops=1`:** Exactly 28 rows were emitted across 1 loop iteration.
   - *Total rows processed = `actual rows * loops`*.
5. **`Buffers: shared hit=8 read=2`:**
   - `shared hit=8`: 8 pages (64KB) found in PostgreSQL buffer pool RAM.
   - `read=2`: 2 pages (16KB) had to be read from OS cache or physical disk.

---

## 4. The Core Access Methods (Scans)

| Scan Type | How it Works | When it is Optimal |
| :--- | :--- | :--- |
| **Seq Scan** | Reads every page in the heap from beginning to end. | High selectivity (query returns > 15-20% of the table) or tiny tables (< 50 pages). |
| **Index Scan** | Traverses B-tree to leaf, then fetches each matching heap tuple by `ctid`. | High selectivity (< 5% of rows). Can be random I/O heavy if heap pages are scattered. |
| **Index Only Scan** | Traverses B-tree and retrieves all required columns directly from index leaf nodes without touching the heap. | Requires index to cover all projected columns and visibility map shows all tuples visible. |
| **Bitmap Scan** | `Bitmap Index Scan` builds a bitmask of matching pages in memory; `Bitmap Heap Scan` reads pages in sequential physical order. | Moderate selectivity (5-15% of table) or combining multiple indexes via `BitmapAnd` / `BitmapOr`. |

---

## 5. The Three Physical Join Algorithms

```text
1. Nested Loop Join
   For every outer row, scan the inner table.
   Optimal when: Outer set is very small (< 100 rows) and inner table has an index on join key.

2. Hash Join
   Hash the smaller relation into memory; stream the larger relation through the hash table.
   Optimal when: Joining large unsorted datasets on equality (=). Requires enough work_mem.

3. Merge Join
   Both relations must be sorted on join keys. Walk both streams simultaneously like a zipper.
   Optimal when: Both tables are already sorted by indexes or required output ordering matches.
```

---

## 6. The Cardinality Estimation Trap

The single most common cause of catastrophic query performance is **cardinality misestimation**:
- If the planner estimates `rows=1`, it chooses a `Nested Loop`.
- If in reality the table returns `10,000,000 rows`, that Nested Loop will execute 10,000,000 index scans, locking CPU for minutes!
- **Diagnostic:** Always check the ratio of `actual rows` to estimated `rows`. If they diverge by more than an order of magnitude (10x), run `ANALYZE table_name;` or create extended statistics (`CREATE STATISTICS`).
