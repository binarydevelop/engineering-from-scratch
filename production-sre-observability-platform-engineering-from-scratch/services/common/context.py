"""
W3C TraceContext and Correlation ID propagation utilities.
"""

import uuid
from typing import Dict, Optional
from fastapi import Request


CORRELATION_ID_HEADER = "x-correlation-id"
REQUEST_ID_HEADER = "x-request-id"
TRACEPARENT_HEADER = "traceparent"


def extract_or_generate_correlation_id(request: Request) -> str:
    """Extracts x-correlation-id from incoming HTTP headers or generates a new UUID4."""
    header_val = request.headers.get(CORRELATION_ID_HEADER) or request.headers.get(REQUEST_ID_HEADER)
    if header_val:
        return header_val.strip()
    return uuid.uuid4().hex


def get_forward_headers(correlation_id: str, traceparent: Optional[str] = None) -> Dict[str, str]:
    """Generates outbound HTTP headers to propagate correlation ID and W3C trace context."""
    headers = {
        CORRELATION_ID_HEADER: correlation_id,
        REQUEST_ID_HEADER: correlation_id,
    }
    if traceparent:
        headers[TRACEPARENT_HEADER] = traceparent
    return headers
