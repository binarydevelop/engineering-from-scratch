# Analytical Query Exercise: EX-TIME-06

## Exercise Metadata
- **Exercise ID**: `EX-TIME-06`
- **Category**: `02-time-analytics`
- **Dataset**: `ecommerce`
- **Difficulty**: `Foundational`
- **SQL Dialect**: `DuckDB`

---

## 1. Requirement & Business Question
Temporal Resampling and Metrics by Day Drill #6

---

## 2. Relational Grains
- **Input Grain**: One row = one time-stamped transaction or telemetry ping
- **Expected Output Grain**: One row = one day time bucket with aggregated volume
- **Expected Row Count / Result Shape**: ~30 temporal buckets

---

## 3. Physical Execution Predictions
- **Expected Columns Scanned**: `created_at, net_revenue`
- **Expected Major Physical Operators**: `TableScan -> Filter -> HashAggregate`
- **Expected Partition Pruning**: Yes, timestamp range pruning
- **Performance Sensitivity**: Time ordering preserves cache locality

---

## 4. Query Assignment
Write the SQL query that fulfills the requirements while minimizing physical I/O and memory footprint.
*Do not view the solution in `solutions/sql-exercises/02-time-analytics/EX-TIME-06_solution.md` until you have predicted physical work and verified your execution plan.*
