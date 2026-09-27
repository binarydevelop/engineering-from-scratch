SELECT id, total_amount, DATE_TRUNC('month', order_date)::DATE AS month_start FROM ecommerce.orders ORDER BY id ASC;
