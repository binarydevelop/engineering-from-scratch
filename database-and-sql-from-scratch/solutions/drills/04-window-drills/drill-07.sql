SELECT
    id AS order_id,
    total_amount,
    ROUND((total_amount / SUM(total_amount) OVER ()) * 100.0, 2) AS pct_of_total
FROM ecommerce.orders
WHERE status = 'completed'
ORDER BY total_amount DESC, order_id ASC;
