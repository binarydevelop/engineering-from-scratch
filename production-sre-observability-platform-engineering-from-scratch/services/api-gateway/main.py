"""
API Gateway: Edge routing, correlation ID generation, and RED metrics.
"""

import os
import time
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse

from services.common.context import extract_or_generate_correlation_id, get_forward_headers
from services.common.logger import (
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUEST_DURATION_SECONDS,
    ACTIVE_REQUESTS_GAUGE,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from instrumentation.structured_logging import get_structured_logger, set_request_context, clear_request_context
from instrumentation.otel_sdk_setup import init_opentelemetry
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

SERVICE_NAME = "api-gateway"
CHECKOUT_SERVICE_URL = os.getenv("CHECKOUT_SERVICE_URL", "http://checkout-service:8001")

logger = get_structured_logger(SERVICE_NAME)
tracer = init_opentelemetry(SERVICE_NAME)

app = FastAPI(title="API Gateway", version="1.0.0")


@app.middleware("http")
async def telemetry_middleware(request: Request, call_next):
    correlation_id = extract_or_generate_correlation_id(request)
    start_time = time.time()
    
    route_path = request.url.path
    method = request.method
    
    # Track in-flight concurrency
    ACTIVE_REQUESTS_GAUGE.labels(service=SERVICE_NAME).inc()

    # OpenTelemetry Span using stable semantic conventions
    with tracer.start_as_current_span(
        f"{method} {route_path}",
        attributes={
            "http.request.method": method,
            "url.path": route_path,
            "server.address": "0.0.0.0",
            "server.port": 8000,
            "correlation.id": correlation_id,
        }
    ) as span:
        trace_id = format(span.get_span_context().trace_id, "032x")
        span_id = format(span.get_span_context().span_id, "016x")
        
        # Attach context to structured logging thread
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
            logger.error(f"Unhandled gateway exception: {exc}", exc_info=True)
            response = JSONResponse(status_code=500, content={"error": "Internal Gateway Error", "correlation_id": correlation_id})
        finally:
            duration = time.time() - start_time
            ACTIVE_REQUESTS_GAUGE.labels(service=SERVICE_NAME).dec()
            
            # Record RED metrics
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

            response.headers["x-correlation-id"] = correlation_id
            response.headers["x-trace-id"] = trace_id
            
            logger.info(
                f"HTTP {method} {route_path} -> {status_code} ({duration*1000:.1f}ms)",
                extra={"extra_fields": {"duration_ms": duration * 1000, "status_code": status_code}}
            )
            clear_request_context()

    return response


@app.get("/healthz")
def liveness():
    """Liveness probe: verifies process is alive."""
    return {"status": "alive", "service": SERVICE_NAME}


@app.get("/ready")
def readiness():
    """Readiness probe: verifies ability to route traffic."""
    return {"status": "ready", "service": SERVICE_NAME}


@app.get("/metrics")
def metrics_endpoint():
    """Prometheus scrape endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/api/v1/checkout")
async def proxy_checkout(request: Request):
    """Proxies checkout request to checkout-service propagating W3C trace context."""
    correlation_id = request.headers.get("x-correlation-id", "")
    current_span = trace.get_current_span()
    trace_id = format(current_span.get_span_context().trace_id, "032x")
    span_id = format(current_span.get_span_context().span_id, "016x")
    traceparent = f"00-{trace_id}-{span_id}-01"

    body = await request.json()
    headers = get_forward_headers(correlation_id=correlation_id, traceparent=traceparent)

    target_url = f"{CHECKOUT_SERVICE_URL}/checkout"
    logger.info(f"Forwarding checkout to downstream {target_url}")

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.post(target_url, json=body, headers=headers)
            return JSONResponse(status_code=resp.status_code, content=resp.json())
        except httpx.TimeoutException:
            logger.error("Downstream checkout-service timed out after 10s")
            return JSONResponse(status_code=504, content={"error": "Gateway Timeout calling checkout-service"})
        except Exception as e:
            logger.error(f"Downstream checkout-service error: {e}")
            return JSONResponse(status_code=502, content={"error": "Bad Gateway calling checkout-service"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
