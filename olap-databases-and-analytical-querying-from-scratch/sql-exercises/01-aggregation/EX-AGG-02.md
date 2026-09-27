# Analytical Query Exercise: EX-AGG-02

## Exercise Metadata
- **Exercise ID**: `EX-AGG-02`
- **Category**: `01-aggregation`
- **Dataset**: `ecommerce`
- **Difficulty**: `Foundational`
- **SQL Dialect**: `ANSI SQL`

---

## 1. Requirement & Business Question
Category Average Price, Min and Max Order Value

---

## 2. Relational Grains
- **Input Grain**: One row = one order item purchased
- **Expected Output Grain**: One row = one product category with price distribution metrics
- **Expected Row Count / Result Shape**: ~5 rows, 4 columns: [category, avg_price, min_price, max_price]

---

## 3. Physical Execution Predictions
- **Expected Columns Scanned**: `category, price`
- **Expected Major Physical Operators**: `TableScan -> HashAggregate`
- **Expected Partition Pruning**: No
- **Performance Sensitivity**: Low cardinality (5 categories)

---

## 4. Query Assignment
Write the SQL query that fulfills the requirements while minimizing physical I/O and memory footprint.
*Do not view the solution in `solutions/sql-exercises/01-aggregation/EX-AGG-02_solution.md` until you have predicted physical work and verified your execution plan.*
