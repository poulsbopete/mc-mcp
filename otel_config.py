"""OpenTelemetry configuration for comprehensive observability."""
import logging
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

from config import settings


def setup_opentelemetry():
    """
    Configure OpenTelemetry with traces, metrics, and logs.
    All telemetry is exported to Elastic Serverless via OTLP.
    """
    
    # Define resource attributes
    resource = Resource.create({
        SERVICE_NAME: settings.service_name,
        SERVICE_VERSION: settings.service_version,
        "deployment.environment": settings.environment,
        "service.namespace": "mastercard",
        "telemetry.sdk.name": "opentelemetry",
        "telemetry.sdk.language": "python",
    })
    
    # Configure headers with authorization
    headers = {
        "Authorization": f"Bearer {settings.elastic_otel_api_key}"
    }
    
    # === TRACES ===
    trace_exporter = OTLPSpanExporter(
        endpoint=f"{settings.elastic_otlp_endpoint}/v1/traces",
        headers=headers,
    )
    
    trace_provider = TracerProvider(resource=resource)
    trace_processor = BatchSpanProcessor(trace_exporter)
    trace_provider.add_span_processor(trace_processor)
    trace.set_tracer_provider(trace_provider)
    
    # === METRICS ===
    metric_exporter = OTLPMetricExporter(
        endpoint=f"{settings.elastic_otlp_endpoint}/v1/metrics",
        headers=headers,
    )
    
    metric_reader = PeriodicExportingMetricReader(
        metric_exporter,
        export_interval_millis=60000,  # Export every 60 seconds
    )
    
    metric_provider = MeterProvider(
        resource=resource,
        metric_readers=[metric_reader]
    )
    metrics.set_meter_provider(metric_provider)
    
    # === LOGS ===
    log_exporter = OTLPLogExporter(
        endpoint=f"{settings.elastic_otlp_endpoint}/v1/logs",
        headers=headers,
    )
    
    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    set_logger_provider(logger_provider)
    
    # Attach OTLP handler to root logger
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)
    
    # === AUTO-INSTRUMENTATION ===
    # These will be called after FastAPI app is created
    RequestsInstrumentor().instrument()
    LoggingInstrumentor().instrument(set_logging_format=True)
    
    print(f"✅ OpenTelemetry configured for {settings.service_name}")
    print(f"📊 Traces, Metrics, and Logs → {settings.elastic_otlp_endpoint}")
    
    return trace_provider, metric_provider, logger_provider


def get_tracer(name: str):
    """Get a tracer for creating custom spans."""
    return trace.get_tracer(name, settings.service_version)


def get_meter(name: str):
    """Get a meter for creating custom metrics."""
    return metrics.get_meter(name, settings.service_version)


def instrument_fastapi(app):
    """Instrument FastAPI application with OpenTelemetry."""
    FastAPIInstrumentor.instrument_app(app)
    print(f"✅ FastAPI instrumented with OpenTelemetry")

