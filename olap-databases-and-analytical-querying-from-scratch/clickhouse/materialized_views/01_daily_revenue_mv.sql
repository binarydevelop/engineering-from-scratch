-- ClickHouse Incremental Materialized View & Target Table
CREATE TABLE IF NOT EXISTS olaplab.daily_revenue_summary
(
    event_date Date,
    country LowCardinality(FixedString(2)),
    category LowCardinality(String),
    total_orders SimpleAggregateFunction(sum, UInt64),
    gross_revenue SimpleAggregateFunction(sum, Float64)
)
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(event_date)
ORDER BY (country, category, event_date);

CREATE MATERIALIZED VIEW IF NOT EXISTS olaplab.mv_daily_revenue
TO olaplab.daily_revenue_summary AS
SELECT
    toDate(created_at) AS event_date,
    country,
    category,
    count() AS total_orders,
    sum(net_revenue) AS gross_revenue
FROM olaplab.fact_order_items
GROUP BY event_date, country, category;
