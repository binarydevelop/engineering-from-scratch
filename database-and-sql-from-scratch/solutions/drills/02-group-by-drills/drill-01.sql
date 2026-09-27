SELECT
    category_id,
    COUNT(*) AS product_count
FROM ecommerce.products
GROUP BY category_id
ORDER BY product_count DESC, category_id ASC;
