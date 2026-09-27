SELECT sku, name, (price - cost) AS profit, ROUND(((price - cost) / cost) * 100, 2) AS markup_pct FROM ecommerce.products ORDER BY profit DESC, sku ASC;
