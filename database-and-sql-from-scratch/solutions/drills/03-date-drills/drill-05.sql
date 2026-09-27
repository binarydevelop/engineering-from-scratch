SELECT
    d.day::DATE AS calendar_day,
    COUNT(o.id) AS order_count
FROM generate_series('2026-01-01'::DATE, '2026-01-05'::DATE, '1 day'::INTERVAL) AS d(day)
LEFT JOIN ecommerce.orders o
    ON d.day::DATE = o.order_date::DATE
    AND o.status = 'completed'
GROUP BY d.day
ORDER BY calendar_day ASC;
