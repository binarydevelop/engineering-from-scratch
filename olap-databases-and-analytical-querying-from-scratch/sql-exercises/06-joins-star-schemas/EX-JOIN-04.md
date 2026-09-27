# Analytical Query Exercise: EX-JOIN-04

## Exercise Metadata
- **Exercise ID**: `EX-JOIN-04`
- **Category**: `06-joins-star-schemas`
- **Dataset**: `ecommerce`
- **Difficulty**: `Intermediate`
- **SQL Dialect**: `ANSI SQL`

---

## 1. Requirement & Business Question
Star Schema Multi-Way Dimension Join Drill #4

---

## 2. Relational Grains
- **Input Grain**: One row = one order line item
- **Expected Output Grain**: One row = one customer segment + product brand pair
- **Expected Row Count / Result Shape**: ~60 aggregated rows

---

## 3. Physical Execution Predictions
- **Expected Columns Scanned**: `user_id, product_id, net_revenue, user_segment, brand`
- **Expected Major Physical Operators**: `TableScan -> HashJoin(dim_users) -> HashJoin(dim_products) -> HashAggregate`
- **Expected Partition Pruning**: Yes, fact table temporal pruning
- **Performance Sensitivity**: Broadcast join on small dimension tables avoids network redistribution

---

## 4. Query Assignment
Write the SQL query that fulfills the requirements while minimizing physical I/O and memory footprint.
*Do not view the solution in `solutions/sql-exercises/06-joins-star-schemas/EX-JOIN-04_solution.md` until you have predicted physical work and verified your execution plan.*
