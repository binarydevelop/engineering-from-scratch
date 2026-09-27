"""
Broken HTTP client that fails to propagate W3C TraceContext headers.
"""

from typing import Dict, Any, Optional
from instrumentation.stdlib_tracing import tracer, SpanContext


def make_outbound_call_broken(payload: Dict[str, Any]) -> Dict[str, str]:
    """
    BROKEN IMPLEMENTATION:
    Sends outbound call without forwarding the active span's W3C traceparent header.
    """
    with tracer.start_span("gateway.forward_request") as span:
        # BUG: Headers do not contain traceparent!
        outgoing_headers = {
            "Content-Type": "application/json",
            "x-service-sender": "api-gateway"
        }
        return outgoing_headers


def make_outbound_call_fixed(payload: Dict[str, Any]) -> Dict[str, str]:
    """
    FIXED IMPLEMENTATION:
    Extracts the active span's trace context and injects the W3C 'traceparent' header.
    """
    with tracer.start_span("gateway.forward_request") as span:
        traceparent = span.context.to_traceparent()
        outgoing_headers = {
            "Content-Type": "application/json",
            "x-service-sender": "api-gateway",
            "traceparent": traceparent
        }
        return outgoing_headers
