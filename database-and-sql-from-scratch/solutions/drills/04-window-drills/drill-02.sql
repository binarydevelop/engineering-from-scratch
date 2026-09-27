SELECT
    id AS order_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER (
        ORDER BY order_date ASC, id ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_revenue
FROM ecommerce.orders
WHERE status = 'completed'
ORDER BY order_date ASC, order_id ASC;
