# Analytical Query Exercise: EX-CH-07

## Exercise Metadata
- **Exercise ID**: `EX-CH-07`
- **Category**: `08-clickhouse-sql`
- **Dataset**: `observability`
- **Difficulty**: `Intermediate`
- **SQL Dialect**: `ClickHouse SQL`

---

## 1. Requirement & Business Question
ClickHouse Vectorized & Specialized OLAP Functions Drill #7

---

## 2. Relational Grains
- **Input Grain**: One row = one service telemetry log
- **Expected Output Grain**: One row = one service with quantiles and high-speed aggregation
- **Expected Row Count / Result Shape**: ~5 service rows

---

## 3. Physical Execution Predictions
- **Expected Columns Scanned**: `service_name, latency_ms, timestamp`
- **Expected Major Physical Operators**: `MergeTreeScan -> VectorizedAggregate`
- **Expected Partition Pruning**: Pruning by partition toYYYYMM(timestamp)
- **Performance Sensitivity**: Uses ClickHouse specialized quantiles (quantileExact, quantileTiming, uniq)

---

## 4. Query Assignment
Write the SQL query that fulfills the requirements while minimizing physical I/O and memory footprint.
*Do not view the solution in `solutions/sql-exercises/08-clickhouse-sql/EX-CH-07_solution.md` until you have predicted physical work and verified your execution plan.*
