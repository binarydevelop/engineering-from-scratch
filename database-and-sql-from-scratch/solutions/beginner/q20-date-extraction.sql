SELECT id, EXTRACT(YEAR FROM order_date)::INT AS order_year, EXTRACT(MONTH FROM order_date)::INT AS order_month FROM ecommerce.orders ORDER BY id ASC;
