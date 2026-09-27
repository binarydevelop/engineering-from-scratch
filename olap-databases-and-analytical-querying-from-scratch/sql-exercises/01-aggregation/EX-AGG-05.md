# Analytical Query Exercise: EX-AGG-05

## Exercise Metadata
- **Exercise ID**: `EX-AGG-05`
- **Category**: `01-aggregation`
- **Dataset**: `finance`
- **Difficulty**: `Foundational`
- **SQL Dialect**: `ANSI SQL`

---

## 1. Requirement & Business Question
Transaction Volume, Fraud Rate, and Total Fees by Merchant Category

---

## 2. Relational Grains
- **Input Grain**: One row = one financial card/wire transaction
- **Expected Output Grain**: One row = one merchant category with risk metrics
- **Expected Row Count / Result Shape**: ~6 rows, 5 columns: [merchant_category, txn_count, total_amount, fraud_count, fraud_rate_pct]

---

## 3. Physical Execution Predictions
- **Expected Columns Scanned**: `merchant_category, amount, fee, is_fraud`
- **Expected Major Physical Operators**: `TableScan -> HashAggregate`
- **Expected Partition Pruning**: No
- **Performance Sensitivity**: Low cardinality hash table

---

## 4. Query Assignment
Write the SQL query that fulfills the requirements while minimizing physical I/O and memory footprint.
*Do not view the solution in `solutions/sql-exercises/01-aggregation/EX-AGG-05_solution.md` until you have predicted physical work and verified your execution plan.*
