#!/usr/bin/env python3
"""
Scalable Multi-Domain Synthetic Analytical Dataset Generator.
Generates realistic event data across 6 core OLAP domains:
  1. ecommerce
  2. clickstream
  3. observability
  4. ads
  5. finance
  6. iot

Supports formats:
  - Parquet (columnar, compressed)
  - CSV (for format comparisons and scan benchmarks)
  - DuckDB tables (in outputs/olap_lab.duckdb)
"""

import os
import sys
import argparse
import time
from pathlib import Path
import duckdb

SCALE_CONFIG = {
    "small": {
        "ecommerce": 50_000,
        "clickstream": 100_000,
        "observability": 100_000,
        "ads": 50_000,
        "finance": 50_000,
        "iot": 100_000,
    },
    "medium": {
        "ecommerce": 500_000,
        "clickstream": 1_000_000,
        "observability": 1_000_000,
        "ads": 500_000,
        "finance": 500_000,
        "iot": 1_000_000,
    },
    "large": {
        "ecommerce": 5_000_000,
        "clickstream": 10_000_000,
        "observability": 10_000_000,
        "ads": 5_000_000,
        "finance": 5_000_000,
        "iot": 10_000_000,
    },
}

def ensure_dirs(base_dir: Path):
    for domain in ["ecommerce", "clickstream", "observability", "ads", "finance", "iot"]:
        (base_dir / "datasets" / domain).mkdir(parents=True, exist_ok=True)
    (base_dir / "outputs").mkdir(parents=True, exist_ok=True)

def generate_ecommerce(con: duckdb.DuckDBPyConnection, base_dir: Path, n_rows: int):
    print(f"[*] Generating eCommerce dataset ({n_rows:,} rows)...")
    t0 = time.time()
    
    # 1. Dim Users (10% of order count)
    n_users = max(1000, n_rows // 10)
    con.execute(f"""
        CREATE OR REPLACE TABLE dim_users AS
        SELECT
            (100000 + i)::BIGINT AS user_id,
            (DATE '2024-01-01' + (i % 730)::INT) AS signup_date,
            CASE (i % 6)
                WHEN 0 THEN 'US'
                WHEN 1 THEN 'DE'
                WHEN 2 THEN 'UK'
                WHEN 3 THEN 'JP'
                WHEN 4 THEN 'FR'
                ELSE 'IN'
            END AS country,
            CASE (i % 4)
                WHEN 0 THEN 'organic'
                WHEN 1 THEN 'cpc_ad'
                WHEN 2 THEN 'email'
                ELSE 'referral'
            END AS acquisition_channel,
            CASE (i % 3)
                WHEN 0 THEN 'vip'
                WHEN 1 THEN 'frequent'
                ELSE 'standard'
            END AS user_segment
        FROM generate_series(1, {n_users}) t(i);
    """)
    
    # 2. Dim Products (500 products)
    n_products = 500
    con.execute(f"""
        CREATE OR REPLACE TABLE dim_products AS
        SELECT
            (5000 + i)::INT AS product_id,
            CASE (i % 5)
                WHEN 0 THEN 'Electronics'
                WHEN 1 THEN 'Apparel'
                WHEN 2 THEN 'Home & Kitchen'
                WHEN 3 THEN 'Books'
                ELSE 'Sports'
            END AS category,
            'Brand_' || (1 + (i % 20)) AS brand,
            ROUND(10.0 + (i % 990) * 1.5, 2) AS base_price,
            ROUND(5.0 + (i % 450) * 1.1, 2) AS cost
        FROM generate_series(1, {n_products}) t(i);
    """)

    # 3. Fact Order Items
    con.execute(f"""
        CREATE OR REPLACE TABLE fact_order_items AS
        SELECT
            (10000000 + i)::BIGINT AS order_item_id,
            (1000000 + (i / 3)::BIGINT) AS order_id,
            TIMESTAMP '2025-01-01 00:00:00' + ((i % (365 * 86400))::BIGINT * INTERVAL '1 second') AS created_at,
            (100000 + (hash(i * 17) % {n_users}))::BIGINT AS user_id,
            (5000 + (hash(i * 31) % {n_products}))::INT AS product_id,
            CASE (i % 5)
                WHEN 0 THEN 'Electronics'
                WHEN 1 THEN 'Apparel'
                WHEN 2 THEN 'Home & Kitchen'
                WHEN 3 THEN 'Books'
                ELSE 'Sports'
            END AS category,
            ROUND(15.0 + (hash(i * 47) % 500) * 1.25, 2) AS price,
            (1 + (i % 5))::INT AS quantity,
            ROUND((i % 4) * 2.5, 2) AS discount_amount,
            ROUND((i % 3) * 4.99, 2) AS shipping_amount,
            ROUND(((15.0 + (hash(i * 47) % 500) * 1.25) * (1 + (i % 5))) * 0.08, 2) AS tax_amount,
            ROUND(((15.0 + (hash(i * 47) % 500) * 1.25) * (1 + (i % 5))) - ((i % 4) * 2.5), 2) AS net_revenue,
            CASE (i % 4)
                WHEN 0 THEN 'credit_card'
                WHEN 1 THEN 'paypal'
                WHEN 2 THEN 'apple_pay'
                ELSE 'bank_transfer'
            END AS payment_method,
            CASE (i % 6)
                WHEN 0 THEN 'US'
                WHEN 1 THEN 'DE'
                WHEN 2 THEN 'UK'
                WHEN 3 THEN 'JP'
                WHEN 4 THEN 'FR'
                ELSE 'IN'
            END AS country,
            CASE (i % 3)
                WHEN 0 THEN 'mobile_ios'
                WHEN 1 THEN 'mobile_android'
                ELSE 'desktop'
            END AS device
        FROM generate_series(1, {n_rows}) t(i);
    """)

    # Export to Parquet and CSV
    ecom_dir = base_dir / "datasets" / "ecommerce"
    con.execute(f"COPY dim_users TO '{ecom_dir}/dim_users.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);")
    con.execute(f"COPY dim_products TO '{ecom_dir}/dim_products.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);")
    con.execute(f"COPY fact_order_items TO '{ecom_dir}/fact_order_items.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);")
    con.execute(f"COPY (SELECT * FROM fact_order_items LIMIT 25000) TO '{ecom_dir}/fact_order_items_sample.csv' (HEADER, DELIMITER ',');")
    print(f"  [✓] eCommerce dataset written in {time.time() - t0:.2f}s")

def generate_clickstream(con: duckdb.DuckDBPyConnection, base_dir: Path, n_rows: int):
    print(f"[*] Generating Clickstream dataset ({n_rows:,} rows)...")
    t0 = time.time()
    n_users = max(5000, n_rows // 20)
    
    con.execute(f"""
        CREATE OR REPLACE TABLE web_events AS
        SELECT
            uuid() AS event_id,
            TIMESTAMP '2025-03-01 00:00:00' + ((i % (30 * 86400))::BIGINT * INTERVAL '1 second') AS event_time,
            (100000 + (hash(i * 13) % {n_users}))::BIGINT AS user_id,
            (500000 + (hash(i * 19) % ({n_users} * 4)))::BIGINT AS session_id,
            CASE (i % 5)
                WHEN 0 THEN '/home'
                WHEN 1 THEN '/product/detail'
                WHEN 2 THEN '/cart'
                WHEN 3 THEN '/checkout'
                ELSE '/confirmation'
            END AS page_url,
            CASE (i % 5)
                WHEN 0 THEN 'view'
                WHEN 1 THEN 'view'
                WHEN 2 THEN 'add_to_cart'
                WHEN 3 THEN 'checkout_start'
                ELSE 'purchase'
            END AS event_type,
            CASE (i % 4)
                WHEN 0 THEN 'https://google.com'
                WHEN 1 THEN 'https://twitter.com'
                WHEN 2 THEN 'https://youtube.com'
                ELSE 'direct'
            END AS referrer,
            CASE (i % 4)
                WHEN 0 THEN 'iOS'
                WHEN 1 THEN 'Android'
                WHEN 2 THEN 'macOS'
                ELSE 'Windows'
            END AS device_os,
            CASE (i % 3)
                WHEN 0 THEN 'Chrome'
                WHEN 1 THEN 'Safari'
                ELSE 'Firefox'
            END AS browser,
            (50 + (hash(i * 23) % 4500))::INT AS duration_ms
        FROM generate_series(1, {n_rows}) t(i);
    """)

    click_dir = base_dir / "datasets" / "clickstream"
    con.execute(f"COPY web_events TO '{click_dir}/web_events.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);")
    con.execute(f"COPY (SELECT * FROM web_events LIMIT 25000) TO '{click_dir}/web_events_sample.csv' (HEADER, DELIMITER ',');")
    print(f"  [✓] Clickstream dataset written in {time.time() - t0:.2f}s")

def generate_observability(con: duckdb.DuckDBPyConnection, base_dir: Path, n_rows: int):
    print(f"[*] Generating Observability dataset ({n_rows:,} rows)...")
    t0 = time.time()
    
    con.execute(f"""
        CREATE OR REPLACE TABLE service_logs AS
        SELECT
            TIMESTAMP '2025-06-01 00:00:00' + ((i % (7 * 86400))::BIGINT * INTERVAL '1 second') AS timestamp,
            CASE (i % 5)
                WHEN 0 THEN 'auth-service'
                WHEN 1 THEN 'payment-service'
                WHEN 2 THEN 'order-service'
                WHEN 3 THEN 'inventory-service'
                ELSE 'gateway'
            END AS service_name,
            'host-node-' || ((i % 50) + 1) AS host_id,
            CASE (i % 4)
                WHEN 0 THEN 'us-east-1'
                WHEN 1 THEN 'us-west-2'
                WHEN 2 THEN 'eu-central-1'
                ELSE 'ap-southeast-1'
            END AS region,
            CASE (i % 6)
                WHEN 0 THEN '/api/v1/auth/login'
                WHEN 1 THEN '/api/v1/payments/charge'
                WHEN 2 THEN '/api/v1/orders/create'
                WHEN 3 THEN '/api/v1/orders/list'
                WHEN 4 THEN '/api/v1/inventory/check'
                ELSE '/healthz'
            END AS endpoint,
            CASE
                WHEN (i % 100) = 0 THEN 500
                WHEN (i % 50) = 0 THEN 503
                WHEN (i % 25) = 0 THEN 404
                WHEN (i % 20) = 0 THEN 401
                ELSE 200
            END AS http_status,
            CASE
                WHEN (i % 100) = 0 THEN (800 + (hash(i * 7) % 4000))::DOUBLE
                ELSE (5.0 + (hash(i * 11) % 180) * 1.5)::DOUBLE
            END AS latency_ms,
            CASE
                WHEN (i % 100) = 0 THEN 'INTERNAL_SERVER_ERROR'
                WHEN (i % 50) = 0 THEN 'SERVICE_UNAVAILABLE'
                WHEN (i % 25) = 0 THEN 'NOT_FOUND'
                WHEN (i % 20) = 0 THEN 'UNAUTHORIZED'
                ELSE NULL
            END AS error_code,
            uuid() AS trace_id,
            uuid() AS span_id,
            ROUND(256.0 + (i % 1024) * 0.75, 1) AS memory_rss_mb,
            ROUND(5.0 + (hash(i * 29) % 85) * 1.0, 1) AS cpu_usage_pct
        FROM generate_series(1, {n_rows}) t(i);
    """)

    obs_dir = base_dir / "datasets" / "observability"
    con.execute(f"COPY service_logs TO '{obs_dir}/service_logs.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);")
    con.execute(f"COPY (SELECT * FROM service_logs LIMIT 25000) TO '{obs_dir}/service_logs_sample.csv' (HEADER, DELIMITER ',');")
    print(f"  [✓] Observability dataset written in {time.time() - t0:.2f}s")

def generate_ads(con: duckdb.DuckDBPyConnection, base_dir: Path, n_rows: int):
    print(f"[*] Generating Ad Tech dataset ({n_rows:,} rows)...")
    t0 = time.time()
    
    con.execute(f"""
        CREATE OR REPLACE TABLE ad_impressions AS
        SELECT
            uuid() AS impression_id,
            TIMESTAMP '2025-05-01 00:00:00' + ((i % (14 * 86400))::BIGINT * INTERVAL '1 second') AS timestamp,
            (100 + (i % 40))::INT AS campaign_id,
            (10 + (i % 15))::INT AS advertiser_id,
            (500 + (i % 100))::INT AS placement_id,
            'publisher-' || ((i % 50) + 1) || '.com' AS publisher_domain,
            CASE (i % 5)
                WHEN 0 THEN 'US'
                WHEN 1 THEN 'GB'
                WHEN 2 THEN 'CA'
                WHEN 3 THEN 'DE'
                ELSE 'AU'
            END AS country,
            ROUND(0.5 + (hash(i * 13) % 450) * 0.05, 3) AS bid_cpm,
            ROUND((0.5 + (hash(i * 13) % 450) * 0.05) / 1000.0, 6) AS cost_usd,
            ((i % 20) = 0)::BOOLEAN AS is_clicked,
            ((i % 100) = 0)::BOOLEAN AS is_converted,
            CASE WHEN (i % 100) = 0 THEN ROUND(15.0 + (hash(i * 37) % 150) * 1.2, 2) ELSE 0.0 END AS attributed_revenue
        FROM generate_series(1, {n_rows}) t(i);
    """)

    ads_dir = base_dir / "datasets" / "ads"
    con.execute(f"COPY ad_impressions TO '{ads_dir}/ad_impressions.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);")
    con.execute(f"COPY (SELECT * FROM ad_impressions LIMIT 25000) TO '{ads_dir}/ad_impressions_sample.csv' (HEADER, DELIMITER ',');")
    print(f"  [✓] Ad Tech dataset written in {time.time() - t0:.2f}s")

def generate_finance(con: duckdb.DuckDBPyConnection, base_dir: Path, n_rows: int):
    print(f"[*] Generating Finance dataset ({n_rows:,} rows)...")
    t0 = time.time()
    
    con.execute(f"""
        CREATE OR REPLACE TABLE financial_transactions AS
        SELECT
            (50000000 + i)::BIGINT AS transaction_id,
            TIMESTAMP '2025-04-01 00:00:00' + ((i % (30 * 86400))::BIGINT * INTERVAL '1 second') AS timestamp,
            (200000 + (hash(i * 7) % 50000))::BIGINT AS account_id,
            (8000 + (hash(i * 11) % 2500))::INT AS merchant_id,
            CASE (i % 6)
                WHEN 0 THEN 'Grocery'
                WHEN 1 THEN 'Airlines'
                WHEN 2 THEN 'Restaurants'
                WHEN 3 THEN 'Electronics'
                WHEN 4 THEN 'Fuel'
                ELSE 'Digital Goods'
            END AS merchant_category,
            CASE (i % 4)
                WHEN 0 THEN 'POS_SWIPE'
                WHEN 1 THEN 'ONLINE_CARD'
                WHEN 2 THEN 'WIRE_TRANSFER'
                ELSE 'ATM_WITHDRAWAL'
            END AS transaction_type,
            'USD' AS currency,
            ROUND(5.0 + (hash(i * 23) % 2000) * 0.85, 2) AS amount,
            ROUND((5.0 + (hash(i * 23) % 2000) * 0.85) * 0.025, 2) AS fee,
            ((i % 250) = 0)::BOOLEAN AS is_fraud,
            ROUND((hash(i * 41) % 1000) / 1000.0, 3) AS risk_score
        FROM generate_series(1, {n_rows}) t(i);
    """)

    fin_dir = base_dir / "datasets" / "finance"
    con.execute(f"COPY financial_transactions TO '{fin_dir}/transactions.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);")
    con.execute(f"COPY (SELECT * FROM financial_transactions LIMIT 25000) TO '{fin_dir}/transactions_sample.csv' (HEADER, DELIMITER ',');")
    print(f"  [✓] Finance dataset written in {time.time() - t0:.2f}s")

def generate_iot(con: duckdb.DuckDBPyConnection, base_dir: Path, n_rows: int):
    print(f"[*] Generating IoT dataset ({n_rows:,} rows)...")
    t0 = time.time()
    
    con.execute(f"""
        CREATE OR REPLACE TABLE sensor_readings AS
        SELECT
            TIMESTAMP '2025-02-01 00:00:00' + ((i % (14 * 86400))::BIGINT * INTERVAL '1 second') AS timestamp,
            'sensor-dev-' || ((i % 1000) + 1) AS device_id,
            'v2.4.' || (i % 4) AS firmware_version,
            'facility-' || ((i % 10) + 1) AS facility_id,
            CASE (i % 3)
                WHEN 0 THEN 'environmental'
                WHEN 1 THEN 'vibration'
                ELSE 'power'
            END AS sensor_type,
            ROUND(18.0 + (sin(i::DOUBLE / 5000.0) * 15.0) + ((i % 10) * 0.2), 2) AS temperature_c,
            ROUND(45.0 + (cos(i::DOUBLE / 3000.0) * 25.0), 2) AS humidity_pct,
            ROUND(101.3 + ((i % 20) * 0.05), 2) AS pressure_kpa,
            (100 - (i % 70))::INT AS battery_pct,
            ((i % 300) = 0)::BOOLEAN AS is_alert
        FROM generate_series(1, {n_rows}) t(i);
    """)

    iot_dir = base_dir / "datasets" / "iot"
    con.execute(f"COPY sensor_readings TO '{iot_dir}/sensor_readings.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);")
    con.execute(f"COPY (SELECT * FROM sensor_readings LIMIT 25000) TO '{iot_dir}/sensor_readings_sample.csv' (HEADER, DELIMITER ',');")
    print(f"  [✓] IoT dataset written in {time.time() - t0:.2f}s")

def main():
    parser = argparse.ArgumentParser(description="OLAP Synthetic Analytical Dataset Generator")
    parser.add_argument("--scale", choices=["small", "medium", "large"], default="small",
                        help="Data scale: small (~450K rows total), medium (~4.5M rows total), large (~45M rows total)")
    parser.add_argument("--persist-duckdb", action="store_true", default=True,
                        help="Persist tables into outputs/olap_lab.duckdb")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    ensure_dirs(repo_root)

    print(f"\n=======================================================")
    print(f"  Generating Analytical Datasets [Scale: {args.scale.upper()}]")
    print(f"  Target Root: {repo_root}")
    print(f"=======================================================\n")

    db_path = str(repo_root / "outputs" / "olap_lab.duckdb")
    con = duckdb.connect(db_path)
    con.execute("PRAGMA threads=4;")
    con.execute("PRAGMA memory_limit='4GB';")

    scale = SCALE_CONFIG[args.scale]

    t_start = time.time()
    generate_ecommerce(con, repo_root, scale["ecommerce"])
    generate_clickstream(con, repo_root, scale["clickstream"])
    generate_observability(con, repo_root, scale["observability"])
    generate_ads(con, repo_root, scale["ads"])
    generate_finance(con, repo_root, scale["finance"])
    generate_iot(con, repo_root, scale["iot"])

    con.close()
    total_sec = time.time() - t_start
    print(f"\n[✓] All 6 domain datasets successfully generated and persisted in {total_sec:.2f}s!")
    print(f"    - Parquet files: datasets/<domain>/*.parquet")
    print(f"    - Sample CSVs:   datasets/<domain>/*_sample.csv")
    print(f"    - DuckDB database: outputs/olap_lab.duckdb\n")

if __name__ == "__main__":
    main()
