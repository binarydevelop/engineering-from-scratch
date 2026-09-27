#!/usr/bin/env python3
"""
Seed Data Generator for NoSQL Databases & Query Languages From Scratch
Generates rich, realistic, cross-paradigm datasets for:
1. E-Commerce (Customers, Products, Categories, Orders, Reviews, Inventory)
2. Social Network (Users, Posts, Follows, Likes, Comments, Messages)
3. SaaS Multi-Tenant (Organizations, Users, Projects, Audit Events, Subscriptions)
4. IoT & Telemetry (Devices, Sensor Readings, Maintenance Alerts)
5. Banking & Transactions (Accounts, Transfers, Fraud Flags, Cards)
6. Knowledge Graph (People, Companies, Skills, Projects, Affiliations)

Runs with pure Python standard library (zero external dependencies required).
Can export to JSON files or seed live databases when available.
"""

import os
import sys
import json
import random
import datetime
import argparse
from typing import Dict, List, Any

# Deterministic random seed for reproducible benchmark data
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")

CATEGORIES = [
    {"id": "CAT-01", "name": "Electronics", "slug": "electronics"},
    {"id": "CAT-02", "name": "Audio & Video", "slug": "audio-video"},
    {"id": "CAT-03", "name": "Computers & Office", "slug": "computers-office"},
    {"id": "CAT-04", "name": "Home & Kitchen", "slug": "home-kitchen"},
    {"id": "CAT-05", "name": "Wearable Tech", "slug": "wearables"}
]

PRODUCT_NAMES = [
    ("Pro Sound ANC Headphones", "CAT-02", 199.99, ["audio", "wireless", "noise-cancelling", "bluetooth"]),
    ("UltraSlim Mechanical Keyboard", "CAT-03", 129.50, ["keyboard", "gaming", "mechanical", "rgb"]),
    ("4K HDR Studio Monitor 32-inch", "CAT-03", 549.00, ["monitor", "4k", "hdr", "ips", "studio"]),
    ("Smart Fitness Tracker Band", "CAT-05", 79.99, ["fitness", "heart-rate", "waterproof", "gps"]),
    ("Mesh Wi-Fi 6 Router System", "CAT-01", 249.99, ["wifi", "networking", "gigabit", "mesh"]),
    ("True Wireless Earbuds Pro", "CAT-02", 149.00, ["audio", "earbuds", "wireless", "water-resistant"]),
    ("Ergonomic Vertical Mouse", "CAT-03", 49.95, ["mouse", "ergonomic", "wireless", "office"]),
    ("Smart Induction Coffee Maker", "CAT-04", 189.00, ["coffee", "smart-home", "app-enabled", "kitchen"]),
    ("Precision Touch Stylus Pen", "CAT-03", 69.00, ["stylus", "tablet", "drawing", "pressure-sensitive"]),
    ("USB-C Quad 100W GaN Charger", "CAT-01", 89.99, ["charger", "gan", "usb-c", "fast-charging"])
]

COUNTRIES = ["US", "DE", "IN", "GB", "JP", "CA", "FR", "AU"]
ORDER_STATUSES = ["CONFIRMED", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"]

def generate_ecommerce_dataset(count_customers=100, count_orders=500) -> Dict[str, List[Dict[str, Any]]]:
    customers = []
    for i in range(1, count_customers + 1):
        country = random.choice(COUNTRIES)
        customers.append({
            "customer_id": f"CUST-{i:04d}",
            "email": f"customer_{i}@example.com",
            "name": f"Customer {i}",
            "country": country,
            "tier": random.choice(["STANDARD", "PREMIUM", "VIP"]),
            "created_at": (datetime.datetime(2025, 1, 1) + datetime.timedelta(days=random.randint(0, 500))).isoformat() + "Z",
            "lifetime_spend": round(random.uniform(50.0, 5000.0), 2)
        })

    products = []
    for idx, (name, cat_id, base_price, tags) in enumerate(PRODUCT_NAMES, start=1):
        products.append({
            "product_id": f"PROD-{idx:04d}",
            "name": name,
            "category_id": cat_id,
            "price": base_price,
            "rating": round(random.uniform(3.5, 5.0), 1),
            "review_count": random.randint(10, 2500),
            "inventory_count": random.randint(0, 150),
            "tags": tags,
            "attributes": {
                "weight_g": random.randint(150, 2500),
                "in_stock": True,
                "warranty_months": random.choice([12, 24, 36])
            }
        })

    orders = []
    for i in range(1, count_orders + 1):
        cust = random.choice(customers)
        status = random.choice(ORDER_STATUSES)
        num_items = random.randint(1, 4)
        order_items = []
        total = 0.0
        for _ in range(num_items):
            prod = random.choice(products)
            qty = random.randint(1, 3)
            subtotal = round(prod["price"] * qty, 2)
            total += subtotal
            order_items.append({
                "product_id": prod["product_id"],
                "name": prod["name"],
                "unit_price": prod["price"],
                "quantity": qty,
                "subtotal": subtotal
            })
        order_time = (datetime.datetime(2025, 6, 1) + datetime.timedelta(hours=i*2, minutes=random.randint(0, 59))).isoformat() + "Z"
        orders.append({
            "_id": f"ORD-{i:05d}",
            "order_id": f"ORD-{i:05d}",
            "customer_id": cust["customer_id"],
            "customer_country": cust["country"],
            "status": status,
            "created_at": order_time,
            "total_amount": round(total, 2),
            "items": order_items,
            "shipping_address": {
                "city": f"City_{random.randint(1, 50)}",
                "country": cust["country"],
                "postal_code": f"{random.randint(10000, 99999)}"
            }
        })

    return {
        "categories": CATEGORIES,
        "customers": customers,
        "products": products,
        "orders": orders
    }

def generate_social_dataset(count_users=50, count_posts=200) -> Dict[str, List[Dict[str, Any]]]:
    users = []
    for i in range(1, count_users + 1):
        users.append({
            "user_id": f"USER-{i:04d}",
            "username": f"user_{i}",
            "display_name": f"User {i}",
            "followers_count": random.randint(5, 5000),
            "following_count": random.randint(5, 500),
            "interests": random.sample(["tech", "databases", "distributed-systems", "ai", "cloud", "gaming", "music"], k=3)
        })

    follows = []
    for u in users:
        target_users = random.sample([x for x in users if x["user_id"] != u["user_id"]], k=random.randint(3, 8))
        for t in target_users:
            follows.append({
                "follower_id": u["user_id"],
                "followed_id": t["user_id"],
                "since": "2025-03-15T10:00:00Z"
            })

    posts = []
    for i in range(1, count_posts + 1):
        author = random.choice(users)
        posts.append({
            "post_id": f"POST-{i:05d}",
            "author_id": author["user_id"],
            "author_username": author["username"],
            "content": f"Exploring NoSQL data models and query planning on day {i}! #nosql #databases",
            "created_at": (datetime.datetime(2026, 1, 1) + datetime.timedelta(hours=i*3)).isoformat() + "Z",
            "like_count": random.randint(0, 300),
            "reply_count": random.randint(0, 45),
            "tags": random.sample(["nosql", "distributed", "cql", "mongo", "graph", "perf"], k=2)
        })

    return {
        "users": users,
        "follows": follows,
        "posts": posts
    }

def generate_iot_dataset(count_devices=20, count_readings=400) -> Dict[str, List[Dict[str, Any]]]:
    devices = []
    for i in range(1, count_devices + 1):
        devices.append({
            "device_id": f"DEV-{i:03d}",
            "model": f"Sensor-X{random.choice(['100', '200', 'Pro'])}",
            "firmware_version": f"v{random.choice(['1.2.0', '1.3.4', '2.0.1'])}",
            "facility_id": f"FACILITY-{random.randint(1, 5)}",
            "status": random.choice(["ONLINE", "ONLINE", "ONLINE", "MAINTENANCE", "OFFLINE"])
        })

    readings = []
    base_time = datetime.datetime(2026, 9, 20, 0, 0, 0)
    for i in range(1, count_readings + 1):
        dev = random.choice(devices)
        readings.append({
            "device_id": dev["device_id"],
            "timestamp": (base_time + datetime.timedelta(minutes=i*5)).isoformat() + "Z",
            "temperature_c": round(random.uniform(18.0, 75.0), 2),
            "humidity_pct": round(random.uniform(30.0, 85.0), 1),
            "pressure_kpa": round(random.uniform(98.0, 105.0), 2),
            "battery_pct": max(5, 100 - (i // 5))
        })

    return {
        "devices": devices,
        "readings": readings
    }

def generate_knowledge_graph_dataset() -> Dict[str, List[Dict[str, Any]]]:
    people = [
        {"id": "P-01", "name": "Alice Chen", "role": "Principal Engineer"},
        {"id": "P-02", "name": "Bob Martin", "role": "Staff Data Engineer"},
        {"id": "P-03", "name": "Charlie Davis", "role": "Distinguished Architect"},
        {"id": "P-04", "name": "Dana Rao", "role": "Database Specialist"},
        {"id": "P-05", "name": "Evan Wright", "role": "Infrastructure Lead"}
    ]
    skills = [
        {"id": "S-01", "name": "Distributed Systems"},
        {"id": "S-02", "name": "Cassandra Architecture"},
        {"id": "S-03", "name": "MongoDB Aggregation"},
        {"id": "S-04", "name": "Graph Algorithms"},
        {"id": "S-05", "name": "Search & Inverted Indexes"}
    ]
    companies = [
        {"id": "C-01", "name": "DataScale Corp", "industry": "Cloud Infrastructure"},
        {"id": "C-02", "name": "HyperQuery AI", "industry": "Database Technologies"},
        {"id": "C-03", "name": "GlobalFin", "industry": "FinTech"}
    ]
    relationships = [
        {"source": "P-01", "target": "S-01", "type": "HAS_SKILL", "years": 10},
        {"source": "P-01", "target": "S-02", "type": "HAS_SKILL", "years": 8},
        {"source": "P-02", "target": "S-01", "type": "HAS_SKILL", "years": 6},
        {"source": "P-02", "target": "S-03", "type": "HAS_SKILL", "years": 5},
        {"source": "P-03", "target": "S-01", "type": "HAS_SKILL", "years": 15},
        {"source": "P-03", "target": "S-04", "type": "HAS_SKILL", "years": 12},
        {"source": "P-04", "target": "S-05", "type": "HAS_SKILL", "years": 7},
        {"source": "P-01", "target": "C-01", "type": "WORKS_AT", "title": "Principal Architect"},
        {"source": "P-02", "target": "C-01", "type": "WORKS_AT", "title": "Staff Engineer"},
        {"source": "P-03", "target": "C-02", "type": "WORKS_AT", "title": "CTO"},
        {"source": "P-01", "target": "P-02", "type": "COLLABORATED_WITH", "project": "Global Event Bus"},
        {"source": "P-02", "target": "P-03", "type": "COLLABORATED_WITH", "project": "LSM Storage Engine"}
    ]
    return {
        "people": people,
        "skills": skills,
        "companies": companies,
        "relationships": relationships
    }

def main():
    parser = argparse.ArgumentParser(description="Generate and export datasets for NoSQL Scratch Labs")
    parser.add_argument("--export-json", action="store_true", default=True, help="Export to datasets directory as JSON")
    args = parser.parse_args()

    os.makedirs(os.path.join(DATASETS_DIR, "ecommerce"), exist_ok=True)
    os.makedirs(os.path.join(DATASETS_DIR, "social"), exist_ok=True)
    os.makedirs(os.path.join(DATASETS_DIR, "iot"), exist_ok=True)
    os.makedirs(os.path.join(DATASETS_DIR, "saas"), exist_ok=True)
    os.makedirs(os.path.join(DATASETS_DIR, "banking"), exist_ok=True)
    os.makedirs(os.path.join(DATASETS_DIR, "knowledge-graph"), exist_ok=True)

    print("Generating E-Commerce dataset...")
    ecom = generate_ecommerce_dataset()
    for entity, data in ecom.items():
        with open(os.path.join(DATASETS_DIR, "ecommerce", f"{entity}.json"), "w") as f:
            json.dump(data, f, indent=2)

    print("Generating Social Network dataset...")
    social = generate_social_dataset()
    for entity, data in social.items():
        with open(os.path.join(DATASETS_DIR, "social", f"{entity}.json"), "w") as f:
            json.dump(data, f, indent=2)

    print("Generating IoT & Telemetry dataset...")
    iot = generate_iot_dataset()
    for entity, data in iot.items():
        with open(os.path.join(DATASETS_DIR, "iot", f"{entity}.json"), "w") as f:
            json.dump(data, f, indent=2)

    print("Generating Knowledge Graph dataset...")
    kg = generate_knowledge_graph_dataset()
    for entity, data in kg.items():
        with open(os.path.join(DATASETS_DIR, "knowledge-graph", f"{entity}.json"), "w") as f:
            json.dump(data, f, indent=2)

    print("Datasets successfully generated in:", DATASETS_DIR)

if __name__ == "__main__":
    main()
