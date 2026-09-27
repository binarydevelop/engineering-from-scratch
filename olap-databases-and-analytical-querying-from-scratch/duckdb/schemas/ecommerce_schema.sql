-- DuckDB eCommerce Star Schema DDL
CREATE TABLE dim_users (
    user_id BIGINT PRIMARY KEY,
    signup_date DATE,
    country VARCHAR(2),
    acquisition_channel VARCHAR(32),
    user_segment VARCHAR(16)
);

CREATE TABLE dim_products (
    product_id INTEGER PRIMARY KEY,
    category VARCHAR(32),
    brand VARCHAR(32),
    base_price DOUBLE,
    cost DOUBLE
);

CREATE TABLE fact_order_items (
    order_item_id BIGINT PRIMARY KEY,
    order_id BIGINT,
    created_at TIMESTAMP,
    user_id BIGINT REFERENCES dim_users(user_id),
    product_id INTEGER REFERENCES dim_products(product_id),
    category VARCHAR(32),
    price DOUBLE,
    quantity INTEGER,
    discount_amount DOUBLE,
    shipping_amount DOUBLE,
    tax_amount DOUBLE,
    net_revenue DOUBLE,
    payment_method VARCHAR(32),
    country VARCHAR(2),
    device VARCHAR(32)
);
