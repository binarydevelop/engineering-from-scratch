# Analytical Query Exercise: EX-APPR-07

## Exercise Metadata
- **Exercise ID**: `EX-APPR-07`
- **Category**: `07-approximate-analytics`
- **Dataset**: `clickstream`
- **Difficulty**: `Intermediate`
- **SQL Dialect**: `DuckDB`

---

## 1. Requirement & Business Question
Approximate Distinct Counting & Sketches Drill #7

---

## 2. Relational Grains
- **Input Grain**: One row = one user web interaction event
- **Expected Output Grain**: One row = one page URL with exact vs approximate user count
- **Expected Row Count / Result Shape**: ~5 URL rows

---

## 3. Physical Execution Predictions
- **Expected Columns Scanned**: `page_url, user_id`
- **Expected Major Physical Operators**: `TableScan -> ApproxCountDistinct (HyperLogLog)`
- **Expected Partition Pruning**: No
- **Performance Sensitivity**: approx_count_distinct utilizes fixed 1-4 KB memory state instead of multi-megabyte hash set

---

## 4. Query Assignment
Write the SQL query that fulfills the requirements while minimizing physical I/O and memory footprint.
*Do not view the solution in `solutions/sql-exercises/07-approximate-analytics/EX-APPR-07_solution.md` until you have predicted physical work and verified your execution plan.*
