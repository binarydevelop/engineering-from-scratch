SELECT id, total_amount, CASE WHEN total_amount >= 1000 THEN 'High' WHEN total_amount >= 250 THEN 'Medium' ELSE 'Low' END AS spend_tier FROM ecommerce.orders ORDER BY id ASC;
