SELECT
    customer_id,
    SUM(total_amount) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_amount
FROM ecommerce.orders
WHERE status = 'completed'
GROUP BY customer_id
ORDER BY total_revenue DESC;
