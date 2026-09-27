SELECT id, total_amount, ROUND(CUME_DIST() OVER (ORDER BY total_amount ASC)::NUMERIC, 4) AS cume_dist_val FROM ecommerce.orders WHERE status = 'completed' ORDER BY total_amount ASC, id ASC;
