# Analytical Query Exercise: EX-AGG-03

## Exercise Metadata
- **Exercise ID**: `EX-AGG-03`
- **Category**: `01-aggregation`
- **Dataset**: `clickstream`
- **Difficulty**: `Foundational`
- **SQL Dialect**: `ANSI SQL`

---

## 1. Requirement & Business Question
Event Count and Average Duration by Browser and Device OS

---

## 2. Relational Grains
- **Input Grain**: One row = one user web interaction event
- **Expected Output Grain**: One row = one (browser, device_os) combination with traffic measures
- **Expected Row Count / Result Shape**: ~12 rows, 4 columns: [browser, device_os, total_events, avg_duration_ms]

---

## 3. Physical Execution Predictions
- **Expected Columns Scanned**: `browser, device_os, duration_ms`
- **Expected Major Physical Operators**: `TableScan -> HashAggregate`
- **Expected Partition Pruning**: No
- **Performance Sensitivity**: Grouping cardinality is tiny (3 browsers * 4 OS = 12 buckets)

---

## 4. Query Assignment
Write the SQL query that fulfills the requirements while minimizing physical I/O and memory footprint.
*Do not view the solution in `solutions/sql-exercises/01-aggregation/EX-AGG-03_solution.md` until you have predicted physical work and verified your execution plan.*
