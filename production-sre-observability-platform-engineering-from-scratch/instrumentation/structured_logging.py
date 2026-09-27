"""
Machine-Queryable Structured JSON Logging from First Principles.

Provides structured JSON logging with ISO-8601 timestamps, log levels,
automatic trace context attachment, correlation ID propagation, and PII redaction.
"""

import json
import logging
import re
import sys
import threading
from datetime import datetime, timezone
from typing import Any, Dict, Optional

# Regex patterns for basic PII redaction
REDACTION_PATTERNS = [
    (re.compile(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"), "[REDACTED_CREDIT_CARD]"),
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"), "[REDACTED_EMAIL]"),
    (re.compile(r'(?i)(password|secret|token|authorization)\s*[:=]\s*["\']([^"\']+)["\']'), r'\1: "[REDACTED]"')
]

_context_data = threading.local()


def set_request_context(correlation_id: str, trace_id: Optional[str] = None, span_id: Optional[str] = None) -> None:
    """Sets contextual IDs for the current request thread."""
    _context_data.correlation_id = correlation_id
    _context_data.trace_id = trace_id
    _context_data.span_id = span_id


def clear_request_context() -> None:
    _context_data.correlation_id = None
    _context_data.trace_id = None
    _context_data.span_id = None


def redact_sensitive_info(text: str) -> str:
    """Applies security regex transforms to scrub credentials and PII."""
    result = text
    for pattern, replacement in REDACTION_PATTERNS:
        result = pattern.sub(replacement, result)
    return result


class JSONFormatter(logging.Formatter):
    """Formats log records as single-line JSON objects."""
    def __init__(self, service_name: str, environment: str = "production"):
        super().__init__()
        self.service_name = service_name
        self.environment = environment

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now(timezone.utc).isoformat()
        
        message = record.getMessage()
        sanitized_message = redact_sensitive_info(message)

        payload: Dict[str, Any] = {
            "timestamp": timestamp,
            "level": record.levelname,
            "service": self.service_name,
            "environment": self.environment,
            "logger": record.name,
            "message": sanitized_message,
        }

        # Attach request context if available
        correlation_id = getattr(_context_data, "correlation_id", None)
        if correlation_id:
            payload["correlation_id"] = correlation_id
            
        trace_id = getattr(_context_data, "trace_id", None)
        if trace_id:
            payload["trace_id"] = trace_id

        span_id = getattr(_context_data, "span_id", None)
        if span_id:
            payload["span_id"] = span_id

        # Attach any extra fields passed in record.__dict__
        if hasattr(record, "extra_fields") and isinstance(record.extra_fields, dict):
            payload.update(record.extra_fields)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload)


def get_structured_logger(service_name: str, level: str = "INFO") -> logging.Logger:
    """Creates a configured structured logger emitting machine-queryable JSON."""
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.propagate = False

    # Avoid duplicate handlers if called multiple times
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter(service_name))
        logger.addHandler(handler)

    return logger
