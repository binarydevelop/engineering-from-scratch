-- =============================================================================
-- Dimensional Analytical Warehouse Schema (Star Schema)
-- =============================================================================

-- 1. Date Dimension (Conformed Dimension)
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,           -- Format: YYYYMMDD (e.g., 20260901)
    full_date DATE NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    day_of_month INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    is_weekend BOOLEAN NOT NULL
);

-- 2. Customer Dimension (SCD Type 2 Capable)
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_surrogate_key INTEGER PRIMARY KEY, -- Synthetic warehouse key
    user_id VARCHAR(32) NOT NULL,              -- Natural source primary key
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    tier VARCHAR(50) NOT NULL,
    valid_from TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    valid_to TIMESTAMP WITHOUT TIME ZONE,
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);

-- 3. Product Dimension (Conformed Dimension)
CREATE TABLE IF NOT EXISTS dim_product (
    product_surrogate_key INTEGER PRIMARY KEY,
    product_id VARCHAR(32) NOT NULL,
    sku VARCHAR(64) NOT NULL,
    category VARCHAR(100) NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    unit_cost NUMERIC(10, 2) NOT NULL
);

-- 4. Orders Fact Table (Event Grain: One row per order)
CREATE TABLE IF NOT EXISTS fact_orders (
    order_id VARCHAR(32) PRIMARY KEY,
    customer_surrogate_key INTEGER NOT NULL REFERENCES dim_customer(customer_surrogate_key),
    order_date_key INTEGER NOT NULL REFERENCES dim_date(date_key),
    order_status VARCHAR(50) NOT NULL,
    subtotal_amount NUMERIC(12, 2) NOT NULL,
    tax_amount NUMERIC(12, 2) NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL
);

-- 5. Order Line Items Fact Table (Grain: One row per order line item)
CREATE TABLE IF NOT EXISTS fact_order_items (
    item_id VARCHAR(32) PRIMARY KEY,
    order_id VARCHAR(32) NOT NULL REFERENCES fact_orders(order_id),
    product_surrogate_key INTEGER NOT NULL REFERENCES dim_product(product_surrogate_key),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    line_total NUMERIC(12, 2) NOT NULL
);
