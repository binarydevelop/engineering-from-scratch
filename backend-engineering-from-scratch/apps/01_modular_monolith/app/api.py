"""
Unified Modular Monolith Application Gateway & Controller.
Coordinates HTTP request boundaries, middleware tracking, and domain services.
"""

import time
import uuid
from typing import Dict, Any, Tuple
from database import Database
from observability import REDMetrics, StructuredLogger
from services import UserService, CatalogService, OrderService, OutboxWorker

class MonolithApp:
    def __init__(self, db_path: str = ":memory:"):
        self.db = Database(db_path)
        self.metrics = REDMetrics()
        self.users = UserService(self.db)
        self.catalog = CatalogService(self.db)
        self.orders = OrderService(self.db)
        self.outbox_worker = OutboxWorker(self.db)

    def handle_request(self, endpoint: str, payload: Dict[str, Any], correlation_id: str = "") -> Tuple[int, Dict[str, Any]]:
        corr_id = correlation_id or str(uuid.uuid4())
        start_time = time.time()
        status_code = 200
        response = {}

        try:
            if endpoint == "POST /users":
                res = self.users.register_user(payload["email"], payload.get("password_hash", "default_hash"))
                status_code, response = 201, res
            elif endpoint == "POST /catalog":
                res = self.catalog.add_product(payload["name"], payload["price_cents"], payload["stock"])
                status_code, response = 201, res
            elif endpoint == "POST /orders":
                res = self.orders.place_order(payload["user_id"], payload["product_id"], payload["quantity"])
                status_code, response = 201, res
            elif endpoint == "GET /metrics":
                status_code, response = 200, self.metrics.summary()
            else:
                status_code, response = 404, {"error": "Endpoint not found"}
        except KeyError as ke:
            status_code, response = 404, {"error": str(ke)}
        except ValueError as ve:
            status_code, response = 400, {"error": str(ve)}
        except Exception as exc:
            status_code, response = 500, {"error": "Internal server error", "detail": str(exc)}
        finally:
            duration = time.time() - start_time
            self.metrics.record_request(duration, status_code)
            StructuredLogger.log(
                "INFO" if status_code < 400 else "ERROR",
                f"{endpoint} completed with {status_code}",
                correlation_id=corr_id,
                duration_sec=duration
            )

        return status_code, response
