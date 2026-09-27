SELECT
    oi.order_id,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price
FROM ecommerce.order_items oi
JOIN ecommerce.products p ON oi.product_id = p.id
WHERE oi.order_id = 1
ORDER BY p.name ASC;
