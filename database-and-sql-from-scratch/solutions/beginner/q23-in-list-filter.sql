SELECT id, customer_id, status FROM ecommerce.orders WHERE status IN ('paid', 'shipped', 'completed') ORDER BY id ASC;
