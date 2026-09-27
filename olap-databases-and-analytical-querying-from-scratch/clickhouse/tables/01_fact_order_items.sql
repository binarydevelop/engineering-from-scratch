-- ClickHouse MergeTree Fact Table
CREATE DATABASE IF NOT EXISTS olaplab;

CREATE TABLE IF NOT EXISTS olaplab.fact_order_items
(
    order_item_id UInt64,
    order_id UInt64,
    created_at DateTime CODEC(DoubleDelta, LZ4),
    user_id UInt64 CODEC(T64, LZ4),
    product_id UInt32,
    category LowCardinality(String),
    price Float64,
    quantity UInt8,
    discount_amount Float32,
    shipping_amount Float32,
    tax_amount Float32,
    net_revenue Float64 CODEC(Gorilla, LZ4),
    payment_method LowCardinality(String),
    country LowCardinality(FixedString(2)),
    device LowCardinality(String)
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(created_at)
ORDER BY (country, category, created_at, user_id)
SETTINGS index_granularity = 8192;
