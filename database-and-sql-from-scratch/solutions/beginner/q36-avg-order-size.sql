SELECT ROUND(AVG(total_amount), 2) AS avg_order_val FROM ecommerce.orders WHERE status = 'completed';
