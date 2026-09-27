SELECT
    id AS order_id,
    order_date AS utc_time,
    order_date AT TIME ZONE 'America/New_York' AS ny_time,
    total_amount
FROM ecommerce.orders
WHERE id = 1;
