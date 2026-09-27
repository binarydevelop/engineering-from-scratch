# Analytical Query Exercise: EX-AGG-24

## Exercise Metadata
- **Exercise ID**: `EX-AGG-24`
- **Category**: `01-aggregation`
- **Dataset**: `ecommerce`
- **Difficulty**: `Intermediate`
- **SQL Dialect**: `ANSI SQL`

---

## 1. Requirement & Business Question
Multi-Measure Aggregation and Group Filter Drill #24

---

## 2. Relational Grains
- **Input Grain**: One row = one granular event record
- **Expected Output Grain**: One row = one aggregated grouping tier 24
- **Expected Row Count / Result Shape**: ~48 rows, 4 columns: [group_key, count, sum_measure, avg_measure]

---

## 3. Physical Execution Predictions
- **Expected Columns Scanned**: `created_at, category, net_revenue`
- **Expected Major Physical Operators**: `TableScan -> Filter -> HashAggregate`
- **Expected Partition Pruning**: Yes, where date filtering is applied
- **Performance Sensitivity**: Moderate cardinality

---

## 4. Query Assignment
Write the SQL query that fulfills the requirements while minimizing physical I/O and memory footprint.
*Do not view the solution in `solutions/sql-exercises/01-aggregation/EX-AGG-24_solution.md` until you have predicted physical work and verified your execution plan.*
