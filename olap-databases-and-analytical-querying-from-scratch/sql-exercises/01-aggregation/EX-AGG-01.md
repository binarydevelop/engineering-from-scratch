# Analytical Query Exercise: EX-AGG-01

## Exercise Metadata
- **Exercise ID**: `EX-AGG-01`
- **Category**: `01-aggregation`
- **Dataset**: `ecommerce`
- **Difficulty**: `Foundational`
- **SQL Dialect**: `ANSI SQL`

---

## 1. Requirement & Business Question
Total Revenue and Orders by Country

---

## 2. Relational Grains
- **Input Grain**: One row = one order item purchased
- **Expected Output Grain**: One row = one country with aggregated volume and revenue
- **Expected Row Count / Result Shape**: ~6 rows, 3 columns: [country, total_orders, total_revenue]

---

## 3. Physical Execution Predictions
- **Expected Columns Scanned**: `country, order_id, net_revenue`
- **Expected Major Physical Operators**: `TableScan -> HashAggregate -> TopNSort`
- **Expected Partition Pruning**: No (full country scan required)
- **Performance Sensitivity**: Low cardinality (6 countries); hash table fits in CPU L1 cache

---

## 4. Query Assignment
Write the SQL query that fulfills the requirements while minimizing physical I/O and memory footprint.
*Do not view the solution in `solutions/sql-exercises/01-aggregation/EX-AGG-01_solution.md` until you have predicted physical work and verified your execution plan.*
