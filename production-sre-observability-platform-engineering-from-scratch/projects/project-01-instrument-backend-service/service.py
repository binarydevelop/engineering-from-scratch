"""
Project 01: Instrument a Backend Service from Scratch.
Implements RED metrics (Rate, Errors, Duration) and W3C trace correlation.
"""
import time
import uuid
from typing import Dict, Any

class TelemetryMiddleware:
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.latencies = []

    def handle_request(self, method: str, path: str, headers: Dict[str, str], handler_func) -> Dict[str, Any]:
        traceparent = headers.get("traceparent")
        if not traceparent:
            trace_id = uuid.uuid4().hex
            span_id = uuid.uuid4().hex[:16]
            traceparent = f"00-{trace_id}-{span_id}-01"

        start_time = time.time()
        self.request_count += 1
        status = 200
        error_msg = None

        try:
            response = handler_func()
            return {
                "status": status,
                "data": response,
                "traceparent": traceparent,
                "latency_ms": (time.time() - start_time) * 1000
            }
        except Exception as e:
            self.error_count += 1
            status = 500
            return {
                "status": status,
                "error": str(e),
                "traceparent": traceparent,
                "latency_ms": (time.time() - start_time) * 1000
            }
