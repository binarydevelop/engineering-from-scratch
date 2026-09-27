"""
Notification Worker: Asynchronous background worker, queue backlog metrics, and async context.
"""

import asyncio
import os
import time
from fastapi import FastAPI, Response
from pydantic import BaseModel
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

from instrumentation.structured_logging import get_structured_logger
from instrumentation.otel_sdk_setup import init_opentelemetry
from opentelemetry import trace

SERVICE_NAME = "notification-worker"

logger = get_structured_logger(SERVICE_NAME)
tracer = init_opentelemetry(SERVICE_NAME)

app = FastAPI(title="Notification Worker", version="1.0.0")

# Queue & Worker Metrics
QUEUE_BACKLOG_GAUGE = Gauge(
    "queue_backlog_total",
    "Current number of pending notification jobs in queue",
    ["queue_name"]
)
JOBS_PROCESSED_TOTAL = Counter(
    "jobs_processed_total",
    "Total notification jobs processed",
    ["queue_name", "status"]
)
WORKER_PROCESSING_LAG_SECONDS = Gauge(
    "worker_processing_lag_seconds",
    "Age of the oldest unacknowledged item in the queue",
    ["queue_name"]
)

# Simulated in-memory queue
JOB_QUEUE = []


class EnqueueJobRequest(BaseModel):
    user_id: str
    email: str
    order_id: str
    amount: float


@app.get("/healthz")
def liveness():
    return {"status": "alive", "service": SERVICE_NAME}


@app.get("/ready")
def readiness():
    return {"status": "ready", "service": SERVICE_NAME}


@app.get("/metrics")
def metrics_endpoint():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/enqueue")
def enqueue_job(job: EnqueueJobRequest):
    JOB_QUEUE.append({
        "data": job.dict(),
        "enqueued_at": time.time()
    })
    QUEUE_BACKLOG_GAUGE.labels(queue_name="order_notifications").set(len(JOB_QUEUE))
    logger.info(f"Enqueued notification for order={job.order_id}, queue_depth={len(JOB_QUEUE)}")
    return {"status": "enqueued", "queue_depth": len(JOB_QUEUE)}


async def worker_loop():
    """Background consumer loop simulating async queue processing."""
    while True:
        if JOB_QUEUE:
            job = JOB_QUEUE.pop(0)
            QUEUE_BACKLOG_GAUGE.labels(queue_name="order_notifications").set(len(JOB_QUEUE))
            
            lag = time.time() - job["enqueued_at"]
            WORKER_PROCESSING_LAG_SECONDS.labels(queue_name="order_notifications").set(lag)

            with tracer.start_as_current_span(
                "process_notification_job",
                attributes={
                    "messaging.system": "redis_queue",
                    "messaging.destination": "order_notifications",
                    "order.id": job["data"]["order_id"],
                }
            ):
                await asyncio.sleep(0.05)  # 50ms processing
                JOBS_PROCESSED_TOTAL.labels(queue_name="order_notifications", status="success").inc()
                logger.info(f"Sent email confirmation for order {job['data']['order_id']} (Lag: {lag*1000:.1f}ms)")
        else:
            WORKER_PROCESSING_LAG_SECONDS.labels(queue_name="order_notifications").set(0.0)
            await asyncio.sleep(0.5)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(worker_loop())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
