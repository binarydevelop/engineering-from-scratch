SELECT
    id AS order_id,
    customer_id,
    order_date
FROM ecommerce.orders
WHERE order_date >= '2026-01-01'
  AND order_date < '2026-01-01'::DATE + INTERVAL '45 days'
ORDER BY order_date ASC;
