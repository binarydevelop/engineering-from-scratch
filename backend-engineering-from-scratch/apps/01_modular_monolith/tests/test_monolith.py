"""
Unit and integration tests for Capstone 01: Modular Monolith.
"""

import os
import sys
import pytest

APP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from api import MonolithApp

@pytest.fixture
def app():
    return MonolithApp(db_path=":memory:")

def test_user_and_catalog_flow(app):
    code, u_res = app.handle_request("POST /users", {"email": "alice@example.com"})
    assert code == 201
    assert "usr_" in u_res["id"]

    code, c_res = app.handle_request("POST /catalog", {"name": "Mechanical Keyboard", "price_cents": 12000, "stock": 5})
    assert code == 201
    assert c_res["stock"] == 5

def test_atomic_order_placement_and_outbox(app):
    # Setup user and product
    _, user = app.handle_request("POST /users", {"email": "buyer@example.com"})
    _, prod = app.handle_request("POST /catalog", {"name": "Laptop Stand", "price_cents": 4500, "stock": 2})

    # 1. Place valid order
    code, order = app.handle_request("POST /orders", {
        "user_id": user["id"],
        "product_id": prod["id"],
        "quantity": 1
    })
    assert code == 201
    assert order["status"] == "CONFIRMED"

    # Check remaining stock
    updated_prod = app.catalog.get_product(prod["id"])
    assert updated_prod["stock"] == 1

    # 2. Verify Transactional Outbox
    dispatched = app.outbox_worker.process_pending(limit=10)
    assert dispatched == 1
    assert len(app.outbox_worker.dispatched_events) == 1
    event = app.outbox_worker.dispatched_events[0]
    assert event["event_type"] == "OrderCreated"
    assert event["payload"]["order_id"] == order["order_id"]

def test_insufficient_stock_rollback(app):
    _, user = app.handle_request("POST /users", {"email": "buyer2@example.com"})
    _, prod = app.handle_request("POST /catalog", {"name": "Monitor", "price_cents": 30000, "stock": 1})

    # Attempt to order 5 units when only 1 exists
    code, res = app.handle_request("POST /orders", {
        "user_id": user["id"],
        "product_id": prod["id"],
        "quantity": 5
    })
    assert code == 400
    assert "Insufficient stock" in res["error"]

    # Stock should remain untouched
    updated_prod = app.catalog.get_product(prod["id"])
    assert updated_prod["stock"] == 1

    # No outbox event should be pending
    dispatched = app.outbox_worker.process_pending()
    assert dispatched == 0

def test_red_metrics_tracking(app):
    app.handle_request("POST /users", {"email": "test@test.com"})
    app.handle_request("POST /invalid-path", {})

    code, metrics = app.handle_request("GET /metrics", {})
    assert code == 200
    assert metrics["rate_total_requests"] >= 2
    assert metrics["errors_total"] >= 1
    assert metrics["error_rate"] > 0
    assert "duration_p50_sec" in metrics
