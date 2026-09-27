WITH ranked AS (
    SELECT
        category_id,
        name,
        price,
        ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC, id ASC) AS rn
    FROM ecommerce.products
)
SELECT
    category_id,
    name,
    price,
    rn AS rank
FROM ranked
WHERE rn <= 2
ORDER BY category_id ASC, price DESC, name ASC;
