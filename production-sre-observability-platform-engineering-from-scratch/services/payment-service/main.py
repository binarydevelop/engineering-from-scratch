"""
Payment Service: Downstream dependency with controllable chaos and circuit breaking.
"""

import asyncio
import os
import random
import time
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from services.common.context import extract_or_generate_correlation_id
from services.common.logger import (
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUEST_DURATION_SECONDS,
    ACTIVE_REQUESTS_GAUGE,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from services.common.circuit_breaker import CircuitBreaker, CircuitBreakerOpenException
from instrumentation.structured_logging import get_structured_logger, set_request_context, clear_request_context
from instrumentation.otel_sdk_setup import init_opentelemetry
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

SERVICE_NAME = "payment-service"

logger = get_structured_logger(SERVICE_NAME)
tracer = init_opentelemetry(SERVICE_NAME)

app = FastAPI(title="Payment Service", version="1.0.0")

# Circuit breaker for external card network
stripe_circuit_breaker = CircuitBreaker("stripe-gateway", failure_threshold=5, recovery_timeout_sec=10.0)

# Runtime chaos injection state
CHAOS_STATE = {
    "artificial_delay_ms": 0,
    "artificial_error_rate": 0.0,
}


class ChargeRequest(BaseModel):
    user_id: str
    amount: float
    payment_token: str


class ChaosConfigRequest(BaseModel):
    delay_ms: int = 0
    error_rate: float = 0.0


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
            if status_code >= 500:
                span.set_status(Status(StatusCode.ERROR, f"HTTP {status_code}"))
        except Exception as exc:
            status_code = 500
            span.set_status(Status(StatusCode.ERROR, str(exc)))
            response = JSONResponse(status_code=500, content={"error": "Payment Service Failure"})
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


@app.post("/chaos/config")
def set_chaos(cfg: ChaosConfigRequest):
    """Admin endpoint to inject controlled delay or error rate."""
    CHAOS_STATE["artificial_delay_ms"] = cfg.delay_ms
    CHAOS_STATE["artificial_error_rate"] = cfg.error_rate
    logger.warn(f"Chaos updated: delay={cfg.delay_ms}ms, error_rate={cfg.error_rate}")
    return {"status": "updated", "chaos_state": CHAOS_STATE}


@app.post("/chaos/reset")
def reset_chaos():
    """Admin endpoint to restore healthy state."""
    CHAOS_STATE["artificial_delay_ms"] = 0
    CHAOS_STATE["artificial_error_rate"] = 0.0
    stripe_circuit_breaker.record_success()
    logger.info("Chaos reset to healthy baseline.")
    return {"status": "reset", "chaos_state": CHAOS_STATE}


@app.post("/charge")
async def process_charge(payload: ChargeRequest, request: Request):
    correlation_id = request.headers.get("x-correlation-id", "")
    
    # 1. Check artificial latency injection
    if CHAOS_STATE["artificial_delay_ms"] > 0:
        delay_sec = CHAOS_STATE["artificial_delay_ms"] / 1000.0
        logger.warn(f"Injecting {CHAOS_STATE['artificial_delay_ms']}ms artificial delay")
        await asyncio.sleep(delay_sec)

    # 2. Check artificial error rate injection
    if CHAOS_STATE["artificial_error_rate"] > 0:
        if random.random() < CHAOS_STATE["artificial_error_rate"]:
            logger.error("Injected artificial HTTP 500 failure")
            stripe_circuit_breaker.record_failure()
            return JSONResponse(status_code=500, content={"error": "Injected Payment Processing Failure"})

    # 3. Execute downstream charge wrapped with circuit breaker
    def _execute_charge():
        with tracer.start_as_current_span(
            "stripe.external_charge",
            attributes={
                "peer.service": "stripe_api",
                "payment.amount": payload.amount,
                "payment.currency": "USD"
            }
        ):
            time.sleep(0.025)  # 25ms baseline external latency
            return {"transaction_id": f"txn_{int(time.time()*1000)}"}

    try:
        charge_result = stripe_circuit_breaker.call(_execute_charge)
    except CircuitBreakerOpenException:
        logger.error("Circuit breaker is OPEN for payment gateway; failing fast.")
        return JSONResponse(status_code=503, content={"error": "Payment Gateway Temporarily Unavailable (Circuit Breaker Tripped)"})
    except Exception as e:
        logger.error(f"Downstream charge error: {e}")
        return JSONResponse(status_code=500, content={"error": "Payment Gateway Transaction Error"})

    logger.info(f"Payment charged ${payload.amount:.2f} for user={payload.user_id}, correlation_id={correlation_id}")
    return {
        "status": "charged",
        "amount": payload.amount,
        "transaction_id": charge_result["transaction_id"],
        "circuit_breaker_state": stripe_circuit_breaker.state.value
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
