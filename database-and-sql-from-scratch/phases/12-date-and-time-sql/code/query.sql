SELECT DATE_TRUNC('month', order_date)::DATE AS sales_month, SUM(total_amount) AS revenue FROM ecommerce.orders WHERE status = 'completed' GROUP BY 1 ORDER BY sales_month ASC;
