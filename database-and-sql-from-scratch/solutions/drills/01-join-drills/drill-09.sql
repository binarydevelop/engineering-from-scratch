SELECT
    c.id AS customer_id,
    c.email,
    tot.total_spent
FROM ecommerce.customers c
JOIN (
    SELECT customer_id, SUM(total_amount) AS total_spent
    FROM ecommerce.orders
    WHERE status = 'completed'
    GROUP BY customer_id
    HAVING SUM(total_amount) > 500
) tot ON c.id = tot.customer_id
ORDER BY tot.total_spent DESC;
