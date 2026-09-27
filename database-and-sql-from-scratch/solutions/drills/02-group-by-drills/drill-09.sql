SELECT
    o.status,
    p.payment_method,
    COUNT(DISTINCT o.id) AS order_count,
    SUM(p.amount) AS total_paid
FROM ecommerce.orders o
JOIN ecommerce.payments p ON o.id = p.order_id
GROUP BY o.status, p.payment_method
ORDER BY o.status ASC, p.payment_method ASC;
