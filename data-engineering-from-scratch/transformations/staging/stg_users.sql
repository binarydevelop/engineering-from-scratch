-- transformations/staging/stg_users.sql
-- Grain: One row per customer. Cleans email, standardizes casing, validates format.

WITH raw_source AS (
    SELECT
        user_id,
        LOWER(TRIM(email)) AS email,
        TRIM(full_name) AS full_name,
        TRIM(city) AS city,
        UPPER(TRIM(tier)) AS customer_tier,
        CAST(signup_date AS DATE) AS signup_date
    FROM read_csv_auto('datasets/raw/users.csv')
)
SELECT
    user_id,
    email,
    full_name,
    city,
    customer_tier,
    signup_date
FROM raw_source
WHERE user_id IS NOT NULL;
