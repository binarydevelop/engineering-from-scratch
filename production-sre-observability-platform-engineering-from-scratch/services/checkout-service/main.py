"""
Checkout Service: Core business orchestrator and SLI/SLO measurement point.
"""

import os
import time
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List

from services.common.context import extract_or_generate_correlation_id, get_forward_headers
from services.common.logger import (
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUEST_DURATION_SECONDS,
    ACTIVE_REQUESTS_GAUGE,
    SLO_GOOD_EVENTS_TOTAL,
    SLO_TOTAL_EVENTS_TOTAL,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from instrumentation.structured_logging import get_structured_logger, set_request_context, clear_request_context
from instrumentation.otel_sdk_setup import init_opentelemetry
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

SERVICE_NAME = "checkout-service"
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL", "http://inventory-service:8002")
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL", "http://payment-service:8003")

logger = get_structured_logger(SERVICE_NAME)
tracer = init_opentelemetry(SERVICE_NAME)

app = FastAPI(title="Checkout Service", version="1.0.0")


class CheckoutItem(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)


class CheckoutRequest(BaseModel):
    user_id: str
    items: List[CheckoutItem]
    payment_token: str
    total_amount: float


@app.middleware("http")
async def telemetry_middleware(request: Request, call_next):
    correlation_id = extract_or_generate_correlation_id(request)
    start_time = time.time()
    
    route_path = request.url.path
    method = request.method
    
    # Extract upstream parent trace context from HTTP headers
    carrier = dict(request.headers)
    parent_context = TraceContextTextMapPropagator().extract(carrier=carrier)
    
    ACTIVE_REQUESTS_GAUGE.labels(service=SERVICE_NAME).inc()

    with tracer.start_as_current_span(
        f"{method} {route_path}",
        context=parent_context,
        attributes={
            "http.request.method": method,
            "url.path": route_path,
            "server.address": "0.0.0.0",
            "server.port": 8001,
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
            if status_code >= 500:
                span.set_status(Status(StatusCode.ERROR, f"HTTP {status_code}"))
        except Exception as exc:
            status_code = 500
            span.set_status(Status(StatusCode.ERROR, str(exc)))
            span.record_exception(exc)
            logger.error(f"Unhandled checkout exception: {exc}", exc_info=True)
            response = JSONResponse(status_code=500, content={"error": "Internal Checkout Failure"})
        finally:
            duration = time.time() - start_time
            ACTIVE_REQUESTS_GAUGE.labels(service=SERVICE_NAME).dec()
            
            HTTP_REQUESTS_TOTAL.labels(
                service=SERVICE_NAME,
                method=method,
                route=route_path,
                status=str(status_code)
            ).inc()
            
            HTTP_REQUEST_DURATION_SECONDS.labels(
                service=SERVICE_NAME,
                method=method,
                route=route_path,
                status=str(status_code)
            ).observe(duration)

            # SLI Measurement for the checkout user journey
            if route_path == "/checkout" and method == "POST":
                SLO_TOTAL_EVENTS_TOTAL.labels(service=SERVICE_NAME, slo_name="checkout_availability_and_latency").inc()
                # Good Event: status < 500 AND duration <= 0.500s (500ms)
                if status_code < 500 and duration <= 0.500:
                    SLO_GOOD_EVENTS_TOTAL.labels(service=SERVICE_NAME, slo_name="checkout_availability_and_latency").inc()

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


@app.post("/checkout")
async def process_checkout(payload: CheckoutRequest, request: Request):
    correlation_id = request.headers.get("x-correlation-id", "")
    current_span = trace.get_current_span()
    trace_id = format(current_span.get_span_context().trace_id, "032x")
    span_id = format(current_span.get_span_context().span_id, "016x")
    traceparent = f"00-{trace_id}-{span_id}-01"

    headers = get_forward_headers(correlation_id=correlation_id, traceparent=traceparent)

    logger.info(
        f"Processing checkout for user={payload.user_id}, total=${payload.total_amount:.2f}",
        extra={"extra_fields": {"user_id": payload.user_id, "amount": payload.total_amount}}
    )

    async with httpx.AsyncClient(timeout=5.0) as client:
        # Step 1: Reserve inventory
        with tracer.start_as_current_span("inventory.reserve_stock") as inv_span:
            inv_span.set_attribute("item.count", len(payload.items))
            try:
                inv_resp = await client.post(
                    f"{INVENTORY_SERVICE_URL}/reserve",
                    json={"items": [item.dict() for item in payload.items]},
                    headers=headers
                )
                if inv_resp.status_code != 200:
                    logger.warn(f"Inventory reservation failed: {inv_resp.text}")
                    return JSONResponse(status_code=400, content={"error": "Inventory unavailable"})
            except Exception as e:
                inv_span.set_status(Status(StatusCode.ERROR, str(e)))
                logger.error(f"Failed to communicate with inventory-service: {e}")
                return JSONResponse(status_code=503, content={"error": "Inventory dependency unavailable"})

        # Step 2: Process payment
        with tracer.start_as_current_span("payment.process_charge") as pay_span:
            pay_span.set_attribute("payment.amount", payload.total_amount)
            try:
                pay_resp = await client.post(
                    f"{PAYMENT_SERVICE_URL}/charge",
                    json={
                        "user_id": payload.user_id,
                        "amount": payload.total_amount,
                        "payment_token": payload.payment_token
                    },
                    headers=headers
                )
                if pay_resp.status_code != 200:
                    logger.error(f"Payment charge rejected: {pay_resp.text}")
                    return JSONResponse(status_code=pay_resp.status_code, content=pay_resp.json())
            except httpx.TimeoutException:
                pay_span.set_status(Status(StatusCode.ERROR, "Payment timed out"))
                logger.error("Payment dependency timed out")
                return JSONResponse(status_code=504, content={"error": "Payment processing timed out"})
            except Exception as e:
                pay_span.set_status(Status(StatusCode.ERROR, str(e)))
                logger.error(f"Payment service communication error: {e}")
                return JSONResponse(status_code=503, content={"error": "Payment service unavailable"})

    logger.info(f"Checkout completed successfully for user={payload.user_id}")
    return {
        "status": "success",
        "order_id": f"ord_{int(time.time()*1000)}",
        "amount_charged": payload.total_amount,
        "correlation_id": correlation_id
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
