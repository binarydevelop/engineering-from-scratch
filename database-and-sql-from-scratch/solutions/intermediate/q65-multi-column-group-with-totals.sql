SELECT EXTRACT(YEAR FROM order_date)::INT AS order_year, status, COUNT(*) AS order_count, SUM(total_amount) AS total_sum FROM ecommerce.orders GROUP BY 1, 2 ORDER BY order_year ASC, status ASC;
