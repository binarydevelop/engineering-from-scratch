SELECT
    ROUND(AVG(customer_spend), 2) AS avg_customer_spend
FROM (
    SELECT customer_id, SUM(total_amount) AS customer_spend
    FROM ecommerce.orders
    WHERE status = 'completed'
    GROUP BY customer_id
) AS spend_summary;
