SELECT
    EXTRACT(YEAR FROM order_date)::INT AS order_year,
    COUNT(*) AS total_orders
FROM ecommerce.orders
GROUP BY 1
ORDER BY order_year ASC;
