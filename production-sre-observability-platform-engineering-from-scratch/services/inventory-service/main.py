"""
Inventory Service: Relational state management, connection pooling, and DB query tracing.
"""

import os
import time
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

from services.common.context import extract_or_generate_correlation_id
from services.common.logger import (
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUEST_DURATION_SECONDS,
    ACTIVE_REQUESTS_GAUGE,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from prometheus_client import Gauge
from instrumentation.structured_logging import get_structured_logger, set_request_context, clear_request_context
from instrumentation.otel_sdk_setup import init_opentelemetry
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

SERVICE_NAME = "inventory-service"

logger = get_structured_logger(SERVICE_NAME)
tracer = init_opentelemetry(SERVICE_NAME)

app = FastAPI(title="Inventory Service", version="1.0.0")

# Database connection pool metrics
DB_POOL_ACTIVE_CONNECTIONS = Gauge(
    "db_pool_active_connections",
    "Current active database connections in use",
    ["database"]
)
DB_POOL_MAX_CONNECTIONS = Gauge(
    "db_pool_max_connections",
    "Maximum configured database connections",
    ["database"]
)
DB_POOL_MAX_CONNECTIONS.labels(database="production_store").set(50)

# In-memory inventory state with simulated SQL latency
INVENTORY_STORE = {
    "item_101": 5000,
    "item_102": 2500,
    "item_103": 100,
}


class ReserveItem(BaseModel):
    product_id: str
    quantity: int


class ReserveRequest(BaseModel):
    items: List[ReserveItem]


@app.middleware("http")
async def telemetry_middleware(request: Request, call_next):
    correlation_id = extract_or_generate_correlation_id(request)
    start_time = time.time()
    route_path = request.url.path
    method = request.method
    
    carrier = dict(request.headers)
    parent_context = TraceContextTextMapPropagator().extract(carrier=carrier)
    ACTIVE_REQUESTS_GAUGE.labels(service=SERVICE_NAME).inc()

    with tracer.start_as_current_span(
        f"{method} {route_path}",
        context=parent_context,
        attributes={
            "http.request.method": method,
            "url.path": route_path,
            "correlation.id": correlation_id,
        }
    ) as span:
        trace_id = format(span.get_span_context().trace_id, "032x")
        span_id = format(span.get_span_context().span_id, "016x")
        set_request_context(correlation_id=correlation_id, trace_id=trace_id, span_id=span_id)

        try:
            response = await call_next(request)
            status_code = response.status_code
            span.set_attribute("http.response.status_code", status_code)
        except Exception as exc:
            status_code = 500
            span.set_status(Status(StatusCode.ERROR, str(exc)))
            response = JSONResponse(status_code=500, content={"error": "Inventory Internal Failure"})
        finally:
            duration = time.time() - start_time
            ACTIVE_REQUESTS_GAUGE.labels(service=SERVICE_NAME).dec()
            HTTP_REQUESTS_TOTAL.labels(service=SERVICE_NAME, method=method, route=route_path, status=str(status_code)).inc()
            HTTP_REQUEST_DURATION_SECONDS.labels(service=SERVICE_NAME, method=method, route=route_path, status=str(status_code)).observe(duration)
            response.headers["x-correlation-id"] = correlation_id
            clear_request_context()

    return response


@app.get("/healthz")
def liveness():
    return {"status": "alive", "service": SERVICE_NAME}


@app.get("/ready")
def readiness():
    return {"status": "ready", "service": SERVICE_NAME}


@app.get("/metrics")
def metrics_endpoint():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/reserve")
async def reserve_stock(payload: ReserveRequest, request: Request):
    correlation_id = request.headers.get("x-correlation-id", "")
    
    # Simulate DB acquisition & query
    DB_POOL_ACTIVE_CONNECTIONS.labels(database="production_store").inc()
    with tracer.start_as_current_span(
        "postgresql.execute",
        attributes={
            "db.system": "postgresql",
            "db.namespace": "production_store",
            "db.query.text": "UPDATE inventory SET stock = stock - $1 WHERE product_id = $2 AND stock >= $1",
        }
    ):
        time.sleep(0.008)  # 8ms simulated database latency
        DB_POOL_ACTIVE_CONNECTIONS.labels(database="production_store").dec()

    for item in payload.items:
        current_stock = INVENTORY_STORE.get(item.product_id, 1000)
        if current_stock < item.quantity:
            logger.warn(f"Out of stock for product {item.product_id}: requested {item.quantity}, available {current_stock}")
            return JSONResponse(status_code=400, content={"error": f"Product {item.product_id} out of stock"})
        INVENTORY_STORE[item.product_id] = current_stock - item.quantity

    logger.info(f"Reserved stock for {len(payload.items)} items, correlation_id={correlation_id}")
    return {"status": "reserved", "items_reserved": len(payload.items)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
