SELECT
    p.id,
    p.sku,
    p.name
FROM ecommerce.products p
LEFT JOIN ecommerce.order_items oi ON p.id = oi.product_id
WHERE oi.id IS NULL
ORDER BY p.id ASC;
