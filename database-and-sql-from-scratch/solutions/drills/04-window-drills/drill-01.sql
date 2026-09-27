WITH ranked_orders AS (
    SELECT
        customer_id,
        id AS order_id,
        order_date,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, id DESC) AS rn
    FROM ecommerce.orders
)
SELECT
    customer_id,
    order_id,
    order_date
FROM ranked_orders
WHERE rn = 1
ORDER BY customer_id ASC;
