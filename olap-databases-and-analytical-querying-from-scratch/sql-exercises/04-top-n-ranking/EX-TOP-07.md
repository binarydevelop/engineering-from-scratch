# Analytical Query Exercise: EX-TOP-07

## Exercise Metadata
- **Exercise ID**: `EX-TOP-07`
- **Category**: `04-top-n-ranking`
- **Dataset**: `ecommerce`
- **Difficulty**: `Intermediate`
- **SQL Dialect**: `ANSI SQL`

---

## 1. Requirement & Business Question
Top-N Products by Revenue within Each Region Drill #7

---

## 2. Relational Grains
- **Input Grain**: One row = one order item record
- **Expected Output Grain**: Top 3 entities per country partition
- **Expected Row Count / Result Shape**: ~18 ranked rows

---

## 3. Physical Execution Predictions
- **Expected Columns Scanned**: `country, product_id, net_revenue`
- **Expected Major Physical Operators**: `TableScan -> HashAggregate -> WindowSort -> Filter`
- **Expected Partition Pruning**: No
- **Performance Sensitivity**: Window partitioning and Top-N heap filter pushdown

---

## 4. Query Assignment
Write the SQL query that fulfills the requirements while minimizing physical I/O and memory footprint.
*Do not view the solution in `solutions/sql-exercises/04-top-n-ranking/EX-TOP-07_solution.md` until you have predicted physical work and verified your execution plan.*
