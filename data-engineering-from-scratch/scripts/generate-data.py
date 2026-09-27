#!/usr/bin/env python3
"""
Synthetic Data Generator for Data Engineering From Scratch
Generates structured, semi-structured, CDC, financial, and corrupted datasets.
"""
import os
import csv
import json
import random
import datetime
from pathlib import Path

# Fix seed for reproducibility
random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "datasets"
RAW_DIR = DATA_DIR / "raw"
CORRUPTED_DIR = DATA_DIR / "corrupted"
PARTITIONED_DIR = DATA_DIR / "partitioned"

RAW_DIR.mkdir(parents=True, exist_ok=True)
CORRUPTED_DIR.mkdir(parents=True, exist_ok=True)
PARTITIONED_DIR.mkdir(parents=True, exist_ok=True)

def generate_users(count=100):
    users = []
    cities = ["New York", "San Francisco", "Austin", "London", "Berlin", "Tokyo", "Toronto"]
    tiers = ["STANDARD", "PREMIUM", "VIP"]
    base_date = datetime.date(2025, 1, 1)

    for i in range(1, count + 1):
        created_date = base_date + datetime.timedelta(days=random.randint(0, 365))
        users.append({
            "user_id": f"usr_{i:04d}",
            "email": f"user{i}@example.com",
            "full_name": f"User {i}",
            "city": random.choice(cities),
            "tier": random.choice(tiers),
            "signup_date": created_date.isoformat()
        })
    return users

def generate_products(count=50):
    categories = ["Electronics", "Books", "Home & Kitchen", "Apparel", "Sports"]
    products = []
    for i in range(1, count + 1):
        price = round(random.uniform(9.99, 499.99), 2)
        products.append({
            "product_id": f"prd_{i:03d}",
            "sku": f"SKU-{1000 + i}",
            "category": random.choice(categories),
            "price": price,
            "cost": round(price * random.uniform(0.4, 0.7), 2),
            "stock_quantity": random.randint(10, 500)
        })
    return products

def generate_orders_and_items(users, products, order_count=300):
    orders = []
    order_items = []
    payments = []
    statuses = ["COMPLETED", "COMPLETED", "COMPLETED", "PROCESSING", "CANCELLED", "REFUNDED"]
    payment_methods = ["CREDIT_CARD", "PAYPAL", "APPLE_PAY", "BANK_TRANSFER"]
    base_time = datetime.datetime(2026, 9, 1, 8, 0, 0)

    item_id_counter = 1
    payment_id_counter = 1

    for i in range(1, order_count + 1):
        user = random.choice(users)
        order_time = base_time + datetime.timedelta(minutes=random.randint(10, 20000))
        num_items = random.randint(1, 4)
        order_id = f"ord_{i:05d}"
        status = random.choice(statuses)

        subtotal = 0.0
        for _ in range(num_items):
            product = random.choice(products)
            qty = random.randint(1, 3)
            line_total = round(product["price"] * qty, 2)
            subtotal += line_total
            order_items.append({
                "item_id": f"itm_{item_id_counter:06d}",
                "order_id": order_id,
                "product_id": product["product_id"],
                "quantity": qty,
                "unit_price": product["price"],
                "line_total": line_total
            })
            item_id_counter += 1

        subtotal = round(subtotal, 2)
        tax = round(subtotal * 0.08, 2)
        total = round(subtotal + tax, 2)

        orders.append({
            "order_id": order_id,
            "user_id": user["user_id"],
            "order_status": status,
            "subtotal": subtotal,
            "tax": tax,
            "total_amount": total,
            "created_at": order_time.strftime("%Y-%m-%d %H:%M:%S")
        })

        if status in ["COMPLETED", "PROCESSING"]:
            payments.append({
                "payment_id": f"pay_{payment_id_counter:05d}",
                "order_id": order_id,
                "amount": total,
                "payment_method": random.choice(payment_methods),
                "payment_status": "SUCCESS",
                "processed_at": (order_time + datetime.timedelta(seconds=random.randint(5, 60))).strftime("%Y-%m-%d %H:%M:%S")
            })
            payment_id_counter += 1

    return orders, order_items, payments

def generate_clickstream(count=500):
    events = []
    actions = ["page_view", "product_detail", "add_to_cart", "cart_view", "checkout_step", "purchase"]
    devices = ["mobile_ios", "mobile_android", "desktop_chrome", "desktop_safari"]
    base_time = datetime.datetime(2026, 9, 15, 10, 0, 0)

    for i in range(1, count + 1):
        event_time = base_time + datetime.timedelta(seconds=i * random.randint(2, 15))
        session_id = f"ses_{random.randint(100, 250):04d}"
        user_id = f"usr_{random.randint(1, 100):04d}" if random.random() > 0.3 else None
        event = {
            "event_id": f"evt_{i:06d}",
            "session_id": session_id,
            "user_id": user_id,
            "action": random.choice(actions),
            "device": random.choice(devices),
            "url_path": "/products" if random.random() > 0.5 else "/checkout",
            "event_timestamp": event_time.isoformat() + "Z"
        }
        events.append(event)
    return events

def generate_cdc_stream():
    """Generates simulated Postgres WAL logical replication events"""
    cdc_records = [
        {"lsn": 1001, "timestamp": "2026-09-01T10:00:00Z", "table": "orders", "op": "INSERT", "before": None, "after": {"order_id": "ord_90001", "user_id": "usr_0010", "status": "PENDING", "amount": 120.50}},
        {"lsn": 1002, "timestamp": "2026-09-01T10:02:15Z", "table": "orders", "op": "UPDATE", "before": {"order_id": "ord_90001", "user_id": "usr_0010", "status": "PENDING", "amount": 120.50}, "after": {"order_id": "ord_90001", "user_id": "usr_0010", "status": "COMPLETED", "amount": 120.50}},
        {"lsn": 1003, "timestamp": "2026-09-01T10:05:00Z", "table": "orders", "op": "INSERT", "before": None, "after": {"order_id": "ord_90002", "user_id": "usr_0045", "status": "PENDING", "amount": 55.00}},
        {"lsn": 1004, "timestamp": "2026-09-01T10:10:30Z", "table": "orders", "op": "DELETE", "before": {"order_id": "ord_90002", "user_id": "usr_0045", "status": "PENDING", "amount": 55.00}, "after": None}
    ]
    return cdc_records

def generate_corrupted_data():
    """Generates corrupted records for quality checks and broken pipeline scenarios"""
    corrupted_orders = [
        {"order_id": "ord_99001", "user_id": "usr_0001", "order_status": "COMPLETED", "total_amount": 150.00, "created_at": "2026-09-01 12:00:00"},
        # Duplicate order_id
        {"order_id": "ord_99001", "user_id": "usr_0001", "order_status": "COMPLETED", "total_amount": 150.00, "created_at": "2026-09-01 12:00:00"},
        # Negative amount (semantic invalidity)
        {"order_id": "ord_99002", "user_id": "usr_0002", "order_status": "COMPLETED", "total_amount": -45.00, "created_at": "2026-09-01 12:05:00"},
        # Null primary key
        {"order_id": "", "user_id": "usr_0003", "order_status": "COMPLETED", "total_amount": 80.00, "created_at": "2026-09-01 12:10:00"},
        # Non-numeric string in numeric amount
        {"order_id": "ord_99003", "user_id": "usr_0004", "order_status": "COMPLETED", "total_amount": "INVALID_PRICE", "created_at": "2026-09-01 12:15:00"},
        # Malformed date format
        {"order_id": "ord_99004", "user_id": "usr_0005", "order_status": "COMPLETED", "total_amount": 95.00, "created_at": "01/09/26 12:20PM"}
    ]
    return corrupted_orders

def write_csv(filepath, rows, fieldnames):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def write_jsonl(filepath, rows):
    with open(filepath, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")

def main():
    print("Generating synthetic datasets...")
    users = generate_users(100)
    products = generate_products(50)
    orders, order_items, payments = generate_orders_and_items(users, products, 300)
    clickstream = generate_clickstream(500)
    cdc_records = generate_cdc_stream()
    corrupted_orders = generate_corrupted_data()

    # Write Raw CSVs
    write_csv(RAW_DIR / "users.csv", users, ["user_id", "email", "full_name", "city", "tier", "signup_date"])
    write_csv(RAW_DIR / "products.csv", products, ["product_id", "sku", "category", "price", "cost", "stock_quantity"])
    write_csv(RAW_DIR / "orders.csv", orders, ["order_id", "user_id", "order_status", "subtotal", "tax", "total_amount", "created_at"])
    write_csv(RAW_DIR / "order_items.csv", order_items, ["item_id", "order_id", "product_id", "quantity", "unit_price", "line_total"])
    write_csv(RAW_DIR / "payments.csv", payments, ["payment_id", "order_id", "amount", "payment_method", "payment_status", "processed_at"])

    # Write JSONL
    write_jsonl(RAW_DIR / "clickstream.jsonl", clickstream)
    write_jsonl(RAW_DIR / "cdc_wal_stream.jsonl", cdc_records)

    # Write Corrupted
    write_csv(CORRUPTED_DIR / "corrupted_orders.csv", corrupted_orders, ["order_id", "user_id", "order_status", "total_amount", "created_at"])

    # Generate Parquet partitioned datasets if pyarrow is present
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq

        for dt in ["2026-09-01", "2026-09-02"]:
            p_dir = PARTITIONED_DIR / "events" / f"date={dt}"
            p_dir.mkdir(parents=True, exist_ok=True)
            batch = [
                {"event_id": f"p_evt_{i}", "user_id": f"usr_{i%10}", "action": "click", "partition_date": dt}
                for i in range(100)
            ]
            table = pa.Table.from_pylist(batch)
            pq.write_table(table, p_dir / "data.parquet")
        print("Generated partitioned Parquet files successfully.")
    except ImportError:
        print("Note: PyArrow not installed yet, skipping parquet partition generation.")

    print(f"Data generation complete!")
    print(f"  Raw files in: {RAW_DIR}")
    print(f"  Corrupted files in: {CORRUPTED_DIR}")
    print(f"  Partitioned files in: {PARTITIONED_DIR}")

if __name__ == "__main__":
    main()
