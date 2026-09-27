SELECT
    CASE
        WHEN price < 100 THEN '< 100'
        WHEN price <= 500 THEN '100-500'
        ELSE '> 500'
    END AS price_tier,
    COUNT(*) AS product_count
FROM ecommerce.products
GROUP BY 1
ORDER BY product_count DESC;
