SELECT * FROM ecommerce.products WHERE category_id = 2 OR category_id = 3 AND price < 500.00; -- Operator precedence bug!
