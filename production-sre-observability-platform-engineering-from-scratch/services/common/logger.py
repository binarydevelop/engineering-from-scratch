"""
Unified logger and telemetry helper for production services.
"""

import os
from instrumentation.structured_logging import get_structured_logger
from instrumentation.otel_sdk_setup import init_opentelemetry
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Standard RED Metrics across microservices (using prometheus_client)
# Rate, Errors, Duration
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests processed by endpoint and status",
    ["service", "method", "route", "status"]
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency distributions in seconds",
    ["service", "method", "route", "status"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
)

ACTIVE_REQUESTS_GAUGE = Gauge(
    "http_active_requests",
    "In-flight active requests currently being processed",
    ["service"]
)

# SLI / SLO metric counters
SLO_GOOD_EVENTS_TOTAL = Counter(
    "slo_good_events_total",
    "Count of requests that satisfied the Service Level Indicator",
    ["service", "slo_name"]
)

SLO_TOTAL_EVENTS_TOTAL = Counter(
    "slo_total_events_total",
    "Count of total valid requests eligible for the SLO calculation",
    ["service", "slo_name"]
)
