SELECT
    id AS order_id,
    customer_id,
    order_date,
    total_amount
FROM ecommerce.orders
WHERE order_date >= '2026-02-01 00:00:00+00'
  AND order_date < '2026-03-01 00:00:00+00'
ORDER BY order_date ASC;
