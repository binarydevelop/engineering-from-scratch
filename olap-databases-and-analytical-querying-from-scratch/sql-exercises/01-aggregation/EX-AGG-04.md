# Analytical Query Exercise: EX-AGG-04

## Exercise Metadata
- **Exercise ID**: `EX-AGG-04`
- **Category**: `01-aggregation`
- **Dataset**: `observability`
- **Difficulty**: `Foundational`
- **SQL Dialect**: `ANSI SQL`

---

## 1. Requirement & Business Question
Error Rate and Total Requests per Microservice Endpoint

---

## 2. Relational Grains
- **Input Grain**: One row = one HTTP service access log event
- **Expected Output Grain**: One row = one (service_name, endpoint) with volume and error metrics
- **Expected Row Count / Result Shape**: ~30 rows, 5 columns: [service_name, endpoint, total_requests, errors, error_rate_pct]

---

## 3. Physical Execution Predictions
- **Expected Columns Scanned**: `service_name, endpoint, http_status`
- **Expected Major Physical Operators**: `TableScan -> HashAggregate`
- **Expected Partition Pruning**: No
- **Performance Sensitivity**: Filter and conditional count evaluation per row

---

## 4. Query Assignment
Write the SQL query that fulfills the requirements while minimizing physical I/O and memory footprint.
*Do not view the solution in `solutions/sql-exercises/01-aggregation/EX-AGG-04_solution.md` until you have predicted physical work and verified your execution plan.*
