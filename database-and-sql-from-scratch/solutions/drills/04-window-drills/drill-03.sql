SELECT
    category_id,
    name,
    price,
    DENSE_RANK() OVER (PARTITION BY category_id ORDER BY price DESC) AS price_rank
FROM ecommerce.products
ORDER BY category_id ASC, price_rank ASC, name ASC;
