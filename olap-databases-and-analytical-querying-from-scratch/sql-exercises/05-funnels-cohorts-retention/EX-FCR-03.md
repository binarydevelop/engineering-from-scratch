# Analytical Query Exercise: EX-FCR-03

## Exercise Metadata
- **Exercise ID**: `EX-FCR-03`
- **Category**: `05-funnels-cohorts-retention`
- **Dataset**: `clickstream`
- **Difficulty**: `Advanced`
- **SQL Dialect**: `DuckDB`

---

## 1. Requirement & Business Question
Multi-Stage Conversion Funnel and User Cohort Retention Drill #3

---

## 2. Relational Grains
- **Input Grain**: One row = one user web interaction event
- **Expected Output Grain**: One row = one conversion step or weekly retention cohort
- **Expected Row Count / Result Shape**: ~5 funnel steps or ~12 weekly cohort rows

---

## 3. Physical Execution Predictions
- **Expected Columns Scanned**: `user_id, event_type, event_time`
- **Expected Major Physical Operators**: `TableScan -> HashAggregate -> ConditionalAggregation`
- **Expected Partition Pruning**: Pruning by session/event date
- **Performance Sensitivity**: Self-joins vs conditional aggregation; conditional aggregation avoids quadratic shuffle

---

## 4. Query Assignment
Write the SQL query that fulfills the requirements while minimizing physical I/O and memory footprint.
*Do not view the solution in `solutions/sql-exercises/05-funnels-cohorts-retention/EX-FCR-03_solution.md` until you have predicted physical work and verified your execution plan.*
