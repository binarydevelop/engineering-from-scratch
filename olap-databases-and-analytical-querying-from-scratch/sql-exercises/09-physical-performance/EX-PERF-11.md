# Analytical Query Exercise: EX-PERF-11

## Exercise Metadata
- **Exercise ID**: `EX-PERF-11`
- **Category**: `09-physical-performance`
- **Dataset**: `ecommerce`
- **Difficulty**: `Advanced Mastery`
- **SQL Dialect**: `DuckDB`

---

## 1. Requirement & Business Question
Physical Execution & Plan Optimization Challenge #11

---

## 2. Relational Grains
- **Input Grain**: One row = one line item record
- **Expected Output Grain**: Aggregated summary answering business question without scanning unneeded columns
- **Expected Row Count / Result Shape**: ~10 rows

---

## 3. Physical Execution Predictions
- **Expected Columns Scanned**: `country, category, net_revenue`
- **Expected Major Physical Operators**: `TableScan (with Projection Pushdown) -> HashAggregate`
- **Expected Partition Pruning**: Partition pruning verified via EXPLAIN
- **Performance Sensitivity**: Avoids SELECT *, applies filter pushdown, minimizes hash table memory

---

## 4. Query Assignment
Write the SQL query that fulfills the requirements while minimizing physical I/O and memory footprint.
*Do not view the solution in `solutions/sql-exercises/09-physical-performance/EX-PERF-11_solution.md` until you have predicted physical work and verified your execution plan.*
