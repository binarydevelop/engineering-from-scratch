SELECT
    category_id,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM ecommerce.products
GROUP BY category_id
ORDER BY category_id ASC;
