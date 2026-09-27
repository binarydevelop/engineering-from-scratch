SELECT product_id, stock_quantity, reorder_level, ROUND(reorder_level::NUMERIC / NULLIF(stock_quantity, 0), 2) AS ratio FROM ecommerce.inventory ORDER BY product_id ASC;
