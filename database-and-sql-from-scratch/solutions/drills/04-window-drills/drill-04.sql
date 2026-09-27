SELECT
    id AS order_id,
    order_date,
    total_amount,
    LAG(total_amount, 1) OVER (ORDER BY order_date ASC) AS prev_order_amount
FROM ecommerce.orders
WHERE customer_id = 1
ORDER BY order_date ASC;
