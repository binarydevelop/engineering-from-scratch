# Analytical Query Exercise: EX-WIN-09

## Exercise Metadata
- **Exercise ID**: `EX-WIN-09`
- **Category**: `03-window-functions`
- **Dataset**: `clickstream`
- **Difficulty**: `Intermediate`
- **SQL Dialect**: `ANSI SQL`

---

## 1. Requirement & Business Question
Analytical Window Function Drill #9: Running Totals and Trailing Lags

---

## 2. Relational Grains
- **Input Grain**: One row = one sequential customer interaction
- **Expected Output Grain**: One row = one event with analytical window metrics (cumulative sum, rank, lag)
- **Expected Row Count / Result Shape**: Same as input event stream

---

## 3. Physical Execution Predictions
- **Expected Columns Scanned**: `user_id, event_time, duration_ms`
- **Expected Major Physical Operators**: `TableScan -> Sort -> WindowOperator`
- **Expected Partition Pruning**: Optional partition pruning on date range
- **Performance Sensitivity**: Window operator requires partition sort in memory; large windows spill to disk

---

## 4. Query Assignment
Write the SQL query that fulfills the requirements while minimizing physical I/O and memory footprint.
*Do not view the solution in `solutions/sql-exercises/03-window-functions/EX-WIN-09_solution.md` until you have predicted physical work and verified your execution plan.*
