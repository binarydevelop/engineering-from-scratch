SELECT customer_id, MIN(order_date) AS first_order, MAX(order_date) AS latest_order FROM ecommerce.orders GROUP BY customer_id ORDER BY customer_id ASC;
