"""
OpenTelemetry SDK Initialization & Stable Semantic Conventions (v1.26.0+).

Configures TracerProvider, MeterProvider, Batch Processors, OTLP Exporters,
and W3C TraceContext propagation adhering strictly to modern OpenTelemetry specifications.
"""

import os
import socket
import uuid
from typing import Optional, Dict

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.propagate import set_global_textmap

# Try importing OTLP exporters if installed, otherwise fallback to console for local offline labs
try:
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter as OTLPGrpcSpanExporter
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter as OTLPGrpcMetricExporter
    HAS_OTLP = True
except ImportError:
    HAS_OTLP = False


def create_production_resource(service_name: str, service_version: str = "1.0.0", environment: str = "production") -> Resource:
    """
    Constructs an OpenTelemetry Resource using stable semantic conventions.
    Identifies the service, environment, host, and unique instance.
    """
    host_name = socket.gethostname()
    instance_id = f"{service_name}-{host_name}-{uuid.uuid4().hex[:8]}"

    attributes: Dict[str, str] = {
        "service.name": service_name,
        "service.version": service_version,
        "service.instance.id": instance_id,
        "deployment.environment": environment,
        "host.name": host_name,
        "telemetry.sdk.language": "python",
    }
    return Resource.create(attributes)


def init_opentelemetry(
    service_name: str,
    otlp_endpoint: Optional[str] = None,
    service_version: str = "1.0.0",
    environment: str = "production"
) -> trace.Tracer:
    """
    Initializes the global OpenTelemetry TracerProvider and MeterProvider.
    Enforces W3C TraceContext propagation globally.
    """
    # 1. Set global W3C context propagator
    set_global_textmap(TraceContextTextMapPropagator())

    # 2. Build resource identity
    resource = create_production_resource(service_name, service_version, environment)

    # 3. Configure TracerProvider and Exporters
    tracer_provider = TracerProvider(resource=resource)
    
    endpoint = otlp_endpoint or os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    insecure = os.getenv("OTEL_EXPORTER_OTLP_INSECURE", "true").lower() == "true"

    if HAS_OTLP and endpoint:
        try:
            span_exporter = OTLPGrpcSpanExporter(endpoint=endpoint, insecure=insecure)
            tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
        except Exception:
            # Fallback to in-memory/console exporter if collector is offline
            tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    else:
        tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(tracer_provider)

    # 4. Configure MeterProvider and Exporters
    if HAS_OTLP and endpoint:
        try:
            metric_exporter = OTLPGrpcMetricExporter(endpoint=endpoint, insecure=insecure)
            reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=15000)
            meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
            metrics.set_meter_provider(meter_provider)
        except Exception:
            metrics.set_meter_provider(MeterProvider(resource=resource))
    else:
        metrics.set_meter_provider(MeterProvider(resource=resource))

    return trace.get_tracer(service_name, service_version)
