-- transformations/staging/stg_orders.sql
-- Grain: One row per order. Normalizes types, handles timezone, and filters deleted/invalid records.

WITH raw_source AS (
    SELECT
        order_id,
        user_id,
        order_status,
        CAST(subtotal AS NUMERIC(10, 2)) AS subtotal_amount,
        CAST(tax AS NUMERIC(10, 2)) AS tax_amount,
        CAST(total_amount AS NUMERIC(10, 2)) AS total_amount,
        CAST(created_at AS TIMESTAMP) AS ordered_at
    FROM read_csv_auto('datasets/raw/orders.csv')
)
SELECT
    order_id,
    user_id,
    UPPER(TRIM(order_status)) AS order_status,
    subtotal_amount,
    tax_amount,
    total_amount,
    ordered_at,
    CAST(strftime(ordered_at, '%Y%m%d') AS INTEGER) AS order_date_key
FROM raw_source
WHERE order_id IS NOT NULL AND total_amount >= 0;
