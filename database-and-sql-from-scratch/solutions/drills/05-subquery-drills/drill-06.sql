WITH order_totals AS (
    SELECT customer_id, SUM(total_amount) AS total_spent
    FROM ecommerce.orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
ranked AS (
    SELECT
        customer_id,
        total_spent,
        DENSE_RANK() OVER (ORDER BY total_spent DESC) AS rnk
    FROM order_totals
)
SELECT
    customer_id,
    total_spent,
    rnk AS rank
FROM ranked
WHERE rnk <= 3
ORDER BY rank ASC;
