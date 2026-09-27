SELECT id, order_date, total_amount FROM ecommerce.orders WHERE (order_date, id) > ('2026-02-05 13:00:00+00'::TIMESTAMPTZ, 7) ORDER BY order_date ASC, id ASC LIMIT 3;
