SELECT DISTINCT ON (customer_id) customer_id, id AS order_id, total_amount FROM ecommerce.orders ORDER BY customer_id ASC, total_amount DESC, id ASC;
