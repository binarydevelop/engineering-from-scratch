SELECT
    DATE_TRUNC('month', order_date)::DATE AS order_month,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_revenue
FROM ecommerce.orders
WHERE status = 'completed'
GROUP BY 1
ORDER BY order_month ASC;
