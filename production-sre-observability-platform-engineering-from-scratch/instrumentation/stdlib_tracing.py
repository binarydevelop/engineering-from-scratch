"""
Distributed Tracing from First Principles (Standard Library Only).

Builds Spans, Trace IDs, Span IDs, and W3C TraceContext header propagation
using only Python standard library primitives to understand tracing internals.
"""

import time
import uuid
import threading
from typing import Optional, Dict, Any, List

# Thread-local storage to track the active span context across function calls
_current_context = threading.local()


class SpanContext:
    """
    Immutable identifier for a span within a distributed trace.
    Adheres to W3C TraceContext specifications.
    """
    def __init__(self, trace_id: str, span_id: str, sampled: bool = True):
        self.trace_id = trace_id
        self.span_id = span_id
        self.sampled = sampled

    @classmethod
    def generate_new(cls, sampled: bool = True) -> "SpanContext":
        trace_id = uuid.uuid4().hex  # 16-byte (32 hex char) trace ID
        span_id = uuid.uuid4().hex[:16]  # 8-byte (16 hex char) span ID
        return cls(trace_id, span_id, sampled)

    def to_traceparent(self) -> str:
        """Serializes context to W3C 'traceparent' header format: 00-{trace_id}-{span_id}-{flags}"""
        flags = "01" if self.sampled else "00"
        return f"00-{self.trace_id}-{self.span_id}-{flags}"

    @classmethod
    def from_traceparent(cls, traceparent: str) -> Optional["SpanContext"]:
        """Parses a W3C 'traceparent' header string."""
        if not traceparent:
            return None
        parts = traceparent.split("-")
        if len(parts) != 4 or parts[0] != "00":
            return None
        trace_id, span_id, flags = parts[1], parts[2], parts[3]
        sampled = flags == "01"
        return cls(trace_id, span_id, sampled)


class Span:
    """
    Represents a single timed unit of work in a distributed system.
    """
    def __init__(
        self,
        name: str,
        context: SpanContext,
        parent_span_id: Optional[str] = None
    ):
        self.name = name
        self.context = context
        self.parent_span_id = parent_span_id
        self.start_time_ns: int = 0
        self.end_time_ns: int = 0
        self.status: str = "UNSET"  # OK, ERROR, UNSET
        self.attributes: Dict[str, Any] = {}
        self.events: List[Dict[str, Any]] = []

    def set_attribute(self, key: str, value: Any) -> "Span":
        self.attributes[key] = value
        return self

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        self.events.append({
            "name": name,
            "timestamp_ns": time.time_ns(),
            "attributes": attributes or {}
        })

    def set_status(self, status: str) -> None:
        self.status = status

    def start(self) -> "Span":
        self.start_time_ns = time.time_ns()
        return self

    def finish(self) -> None:
        self.end_time_ns = time.time_ns()

    @property
    def duration_ms(self) -> float:
        if self.end_time_ns == 0:
            return 0.0
        return (self.end_time_ns - self.start_time_ns) / 1_000_000.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "trace_id": self.context.trace_id,
            "span_id": self.context.span_id,
            "parent_span_id": self.parent_span_id,
            "duration_ms": self.duration_ms,
            "status": self.status,
            "attributes": self.attributes,
            "events": self.events,
            "start_time_ns": self.start_time_ns,
            "end_time_ns": self.end_time_ns,
        }

    def __enter__(self) -> "Span":
        self.start()
        _current_context.active_span = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.set_status("ERROR")
            self.set_attribute("error.type", exc_type.__name__)
            self.set_attribute("error.message", str(exc_val))
        else:
            if self.status == "UNSET":
                self.set_status("OK")
        self.finish()
        _current_context.active_span = None


class SimpleTracer:
    """
    Lightweight in-memory tracer for learning and local inspection.
    """
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.spans: List[Span] = []
        self._lock = threading.Lock()

    def start_span(
        self,
        name: str,
        parent_context: Optional[SpanContext] = None
    ) -> Span:
        if parent_context is not None:
            # Child span in existing trace
            new_span_id = uuid.uuid4().hex[:16]
            context = SpanContext(parent_context.trace_id, new_span_id, parent_context.sampled)
            span = Span(name, context, parent_span_id=parent_context.span_id)
        else:
            # Check thread-local active span
            active: Optional[Span] = getattr(_current_context, "active_span", None)
            if active is not None:
                new_span_id = uuid.uuid4().hex[:16]
                context = SpanContext(active.context.trace_id, new_span_id, active.context.sampled)
                span = Span(name, context, parent_span_id=active.context.span_id)
            else:
                # Root span
                context = SpanContext.generate_new()
                span = Span(name, context, parent_span_id=None)

        span.set_attribute("service.name", self.service_name)
        with self._lock:
            self.spans.append(span)
        return span

    def clear(self) -> None:
        with self._lock:
            self.spans.clear()


# Global singleton instance
tracer = SimpleTracer("first-principles-tracer")
