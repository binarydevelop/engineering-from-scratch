# Analytical Query Exercise: EX-TIME-17

## Exercise Metadata
- **Exercise ID**: `EX-TIME-17`
- **Category**: `02-time-analytics`
- **Dataset**: `iot`
- **Difficulty**: `Intermediate`
- **SQL Dialect**: `DuckDB`

---

## 1. Requirement & Business Question
Temporal Resampling and Metrics by Month Drill #17

---

## 2. Relational Grains
- **Input Grain**: One row = one time-stamped transaction or telemetry ping
- **Expected Output Grain**: One row = one month time bucket with aggregated volume
- **Expected Row Count / Result Shape**: ~85 temporal buckets

---

## 3. Physical Execution Predictions
- **Expected Columns Scanned**: `timestamp, temperature_c`
- **Expected Major Physical Operators**: `TableScan -> Filter -> HashAggregate`
- **Expected Partition Pruning**: Yes, timestamp range pruning
- **Performance Sensitivity**: Time ordering preserves cache locality

---

## 4. Query Assignment
Write the SQL query that fulfills the requirements while minimizing physical I/O and memory footprint.
*Do not view the solution in `solutions/sql-exercises/02-time-analytics/EX-TIME-17_solution.md` until you have predicted physical work and verified your execution plan.*
