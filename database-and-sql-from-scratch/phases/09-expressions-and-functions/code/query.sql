SELECT sku, ROUND(price * 1.0825, 2) AS price_with_tax FROM ecommerce.products ORDER BY id ASC;
