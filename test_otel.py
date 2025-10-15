"""
Quick test script to verify OpenTelemetry configuration.
Run this to ensure telemetry is flowing to Elastic before running the full demo.
"""
import sys
import time
from config import settings
from otel_config import setup_opentelemetry, get_tracer, get_meter

print("🔧 Testing OpenTelemetry Configuration")
print("="*60)
print(f"Service Name: {settings.service_name}")
print(f"OTLP Endpoint: {settings.elastic_otlp_endpoint}")
print(f"Environment: {settings.environment}")
print("")

try:
    # Initialize OpenTelemetry
    print("1️⃣  Initializing OpenTelemetry...")
    trace_provider, metric_provider, logger_provider = setup_opentelemetry()
    print("   ✅ OpenTelemetry initialized successfully\n")
    
    # Get tracer and meter
    tracer = get_tracer("test")
    meter = get_meter("test")
    
    # Create a test trace
    print("2️⃣  Creating test trace...")
    with tracer.start_as_current_span("test.otel.configuration") as span:
        span.set_attribute("test.type", "configuration_check")
        span.set_attribute("test.timestamp", time.time())
        span.set_attribute("test.service", settings.service_name)
        
        # Nested span
        with tracer.start_as_current_span("test.nested_operation") as nested_span:
            nested_span.set_attribute("operation", "nested_test")
            time.sleep(0.1)
            nested_span.add_event("Nested operation completed")
        
        span.add_event("Test trace completed")
    
    print("   ✅ Test trace created\n")
    
    # Create test metrics
    print("3️⃣  Creating test metrics...")
    test_counter = meter.create_counter(
        name="test.otel.counter",
        description="Test counter metric",
        unit="1"
    )
    test_counter.add(1, {"test": "true", "component": "otel_test"})
    
    test_histogram = meter.create_histogram(
        name="test.otel.histogram",
        description="Test histogram metric",
        unit="ms"
    )
    test_histogram.record(123.45, {"test": "true", "metric_type": "histogram"})
    
    print("   ✅ Test metrics recorded\n")
    
    # Test logging
    print("4️⃣  Testing logging...")
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Test INFO log message")
    logger.warning("Test WARNING log message")
    print("   ✅ Test logs created\n")
    
    # Wait for export
    print("5️⃣  Waiting for telemetry export...")
    time.sleep(3)
    print("   ✅ Export complete\n")
    
    print("="*60)
    print("✅ OpenTelemetry test completed successfully!")
    print("")
    print("📊 Next steps:")
    print("   1. Wait 1-2 minutes for data to appear in Elastic")
    print("   2. Use MCP to query: 'Show me traces from mastercard-demo'")
    print("   3. Check Elastic APM UI for the test trace")
    print("   4. If you see data, you're ready to run the full demo!")
    print("")
    print("🔍 Trace details:")
    print(f"   Service: {settings.service_name}")
    print(f"   Span: test.otel.configuration")
    print(f"   Time: ~{time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
except Exception as e:
    print(f"\n❌ Error during OpenTelemetry test: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

