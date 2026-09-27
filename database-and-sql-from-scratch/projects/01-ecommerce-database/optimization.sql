-- Query Performance Lab & Index Optimization
SET search_path TO ecommerce, public;

-- Scenario: High-volume customer purchase history lookup
-- Query: Find all orders for customer 1 between two dates with total_amount > 50.

-- 1. Baseline Plan without composite index
DROP INDEX IF EXISTS idx_orders_customer_date_amount;

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, total_amount, order_date
FROM orders
WHERE customer_id = 1
  AND order_date >= '2026-01-01'
  AND total_amount > 50.00;

-- 2. Add Composite Index (Leading column = equality filter, followed by range filters)
CREATE INDEX idx_orders_customer_date_amount 
ON orders (customer_id, order_date, total_amount);

-- 3. Optimized Plan with Index-Only Scan or Index Scan
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, total_amount, order_date
FROM orders
WHERE customer_id = 1
  AND order_date >= '2026-01-01'
  AND total_amount > 50.00;
