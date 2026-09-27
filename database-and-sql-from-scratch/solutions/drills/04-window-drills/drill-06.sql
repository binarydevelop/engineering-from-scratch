SELECT
    id AS order_id,
    order_date,
    total_amount,
    ROUND(AVG(total_amount) OVER (
        ORDER BY order_date ASC, id ASC
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg
FROM ecommerce.orders
WHERE status = 'completed'
ORDER BY order_date ASC, order_id ASC;
