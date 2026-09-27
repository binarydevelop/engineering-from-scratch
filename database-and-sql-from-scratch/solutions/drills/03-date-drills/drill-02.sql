SELECT
    EXTRACT(DOW FROM order_date) AS day_of_week,
    COUNT(*) AS order_count
FROM ecommerce.orders
GROUP BY 1
ORDER BY day_of_week ASC;
