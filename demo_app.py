"""
Mastercard API Demo Application with OpenTelemetry.

This FastAPI application demonstrates:
- Integration with Mastercard APIs
- Full OpenTelemetry instrumentation (traces, metrics, logs)
- Telemetry export to Elastic Serverless
- MCP-compatible endpoints for observability
"""
import logging
import time
from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from config import settings
from otel_config import setup_opentelemetry, instrument_fastapi, get_tracer, get_meter
from mastercard_client import MastercardClient

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize OpenTelemetry BEFORE creating FastAPI app
trace_provider, metric_provider, logger_provider = setup_opentelemetry()

# Get tracer and meter for custom instrumentation
tracer = get_tracer(__name__)
meter = get_meter(__name__)

# Create custom metrics
request_counter = meter.create_counter(
    name="mastercard.api.requests",
    description="Number of API requests",
    unit="1"
)

response_time_histogram = meter.create_histogram(
    name="mastercard.api.response_time",
    description="API response time",
    unit="ms"
)

fraud_check_counter = meter.create_counter(
    name="mastercard.fraud.checks",
    description="Number of fraud checks performed",
    unit="1"
)

# Initialize Mastercard client
mc_client = MastercardClient(mock_mode=settings.enable_mock_mode)


# Pydantic models
class FraudCheckRequest(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction identifier")
    amount: float = Field(..., gt=0, description="Transaction amount")
    merchant_id: Optional[str] = Field(None, description="Merchant identifier")
    currency: str = Field(default="USD", description="Currency code")


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str
    opentelemetry: dict


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown."""
    logger.info(f"🚀 Starting {settings.service_name} v{settings.service_version}")
    logger.info(f"📊 Mock mode: {settings.enable_mock_mode}")
    logger.info(f"🔭 OpenTelemetry → {settings.elastic_otlp_endpoint}")
    yield
    logger.info(f"🛑 Shutting down {settings.service_name}")


# Create FastAPI app
app = FastAPI(
    title="Mastercard API Demo",
    description="Demo application showcasing Mastercard APIs with OpenTelemetry observability",
    version=settings.service_version,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrument FastAPI with OpenTelemetry
instrument_fastapi(app)


@app.middleware("http")
async def add_metrics_middleware(request, call_next):
    """Middleware to add custom metrics to each request."""
    start_time = time.time()
    
    # Increment request counter
    request_counter.add(1, {
        "method": request.method,
        "path": request.url.path
    })
    
    response = await call_next(request)
    
    # Record response time
    duration_ms = (time.time() - start_time) * 1000
    response_time_histogram.record(duration_ms, {
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code
    })
    
    return response


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with service health information."""
    return HealthResponse(
        status="healthy",
        service=settings.service_name,
        version=settings.service_version,
        timestamp=datetime.utcnow().isoformat(),
        opentelemetry={
            "traces": "enabled",
            "metrics": "enabled",
            "logs": "enabled",
            "endpoint": settings.elastic_otlp_endpoint
        }
    )


@app.get("/health")
async def health():
    """Health check endpoint."""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/banking/accounts")
async def get_accounts(
    user_id: str = Query(..., description="User identifier")
):
    """
    Get banking accounts for a user using Mastercard Open Banking API.
    
    This endpoint demonstrates:
    - Mastercard Open Banking API integration
    - Automatic distributed tracing
    - Custom span attributes
    """
    with tracer.start_as_current_span("api.banking.accounts") as span:
        span.set_attribute("user.id", user_id)
        
        logger.info(f"Getting accounts for user: {user_id}")
        
        try:
            result = mc_client.get_banking_accounts(user_id)
            span.set_attribute("response.account_count", len(result.get("accounts", [])))
            
            return JSONResponse(content=result)
        except Exception as e:
            logger.error(f"Error fetching accounts: {str(e)}", exc_info=True)
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/merchant/locate")
async def locate_merchants(
    query: str = Query(..., description="Search query (e.g., 'coffee', 'restaurant')"),
    latitude: float = Query(37.7749, description="Latitude"),
    longitude: float = Query(-122.4194, description="Longitude"),
    radius: int = Query(5, ge=1, le=50, description="Search radius in miles")
):
    """
    Locate merchants using Mastercard Merchant Identifier API.
    
    This endpoint demonstrates:
    - Merchant location and identification
    - Geographic search capabilities
    - Real-time merchant data
    """
    with tracer.start_as_current_span("api.merchant.locate") as span:
        span.set_attribute("merchant.query", query)
        span.set_attribute("location.lat", latitude)
        span.set_attribute("location.lon", longitude)
        
        logger.info(f"Locating merchants: {query} near ({latitude}, {longitude})")
        
        try:
            result = mc_client.locate_merchants(query, latitude, longitude, radius)
            span.set_attribute("response.merchant_count", len(result.get("merchants", [])))
            
            return JSONResponse(content=result)
        except Exception as e:
            logger.error(f"Error locating merchants: {str(e)}", exc_info=True)
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/fraud/check")
async def check_fraud(request: FraudCheckRequest):
    """
    Check a transaction for fraud using Mastercard Decision Intelligence.
    
    This endpoint demonstrates:
    - Real-time fraud detection
    - Risk scoring and analysis
    - Transaction monitoring
    """
    with tracer.start_as_current_span("api.fraud.check") as span:
        span.set_attribute("transaction.id", request.transaction_id)
        span.set_attribute("transaction.amount", request.amount)
        span.set_attribute("transaction.currency", request.currency)
        
        # Increment fraud check counter
        fraud_check_counter.add(1, {"currency": request.currency})
        
        logger.info(f"Fraud check: {request.transaction_id}, amount: {request.amount}")
        
        try:
            result = mc_client.check_fraud(
                request.transaction_id,
                request.amount,
                request.merchant_id
            )
            
            span.set_attribute("fraud.risk_score", result["risk_score"])
            span.set_attribute("fraud.status", result["status"])
            
            # Log warning if flagged
            if result["status"] == "flagged":
                logger.warning(
                    f"🚨 Suspicious transaction detected: {request.transaction_id} "
                    f"(risk score: {result['risk_score']})"
                )
            
            return JSONResponse(content=result)
        except Exception as e:
            logger.error(f"Error checking fraud: {str(e)}", exc_info=True)
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/transactions/history")
async def get_transaction_history(
    account_id: str = Query(..., description="Account identifier"),
    days: int = Query(30, ge=1, le=365, description="Number of days to look back")
):
    """
    Get transaction history for an account.
    
    This endpoint demonstrates:
    - Transaction history retrieval
    - Historical data analysis
    - Time-based queries
    """
    with tracer.start_as_current_span("api.transactions.history") as span:
        span.set_attribute("account.id", account_id)
        span.set_attribute("history.days", days)
        
        logger.info(f"Getting transaction history: {account_id} ({days} days)")
        
        try:
            result = mc_client.get_transaction_history(account_id, days)
            span.set_attribute("response.transaction_count", len(result.get("transactions", [])))
            span.set_attribute("response.total_spent", result.get("total_spent", 0))
            
            return JSONResponse(content=result)
        except Exception as e:
            logger.error(f"Error fetching transactions: {str(e)}", exc_info=True)
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/demo/generate-traffic")
async def generate_traffic(
    requests: int = Query(10, ge=1, le=100, description="Number of requests to generate")
):
    """
    Generate demo traffic to populate observability dashboards.
    
    This endpoint makes multiple API calls to generate traces and metrics.
    """
    with tracer.start_as_current_span("api.demo.generate_traffic") as span:
        span.set_attribute("demo.request_count", requests)
        
        logger.info(f"Generating {requests} demo requests")
        
        results = {
            "generated": requests,
            "timestamp": datetime.utcnow().isoformat(),
            "operations": []
        }
        
        import random
        
        for i in range(requests):
            # Random operation
            operation = random.choice(["accounts", "merchants", "fraud", "transactions"])
            
            try:
                if operation == "accounts":
                    mc_client.get_banking_accounts(f"user_{random.randint(1, 100)}")
                elif operation == "merchants":
                    queries = ["coffee", "restaurant", "gas", "grocery", "pharmacy"]
                    mc_client.locate_merchants(random.choice(queries))
                elif operation == "fraud":
                    mc_client.check_fraud(
                        f"txn_{random.randint(1000, 9999)}",
                        round(random.uniform(10, 5000), 2)
                    )
                elif operation == "transactions":
                    mc_client.get_transaction_history(
                        f"acc_{random.randint(1000, 9999)}",
                        random.randint(7, 90)
                    )
                
                results["operations"].append({"index": i+1, "operation": operation, "status": "success"})
            except Exception as e:
                results["operations"].append({"index": i+1, "operation": operation, "status": "error", "error": str(e)})
        
        logger.info(f"Generated {requests} demo requests successfully")
        
        return JSONResponse(content=results)


if __name__ == "__main__":
    logger.info(f"Starting {settings.service_name} on port {settings.demo_port}")
    
    uvicorn.run(
        "demo_app:app",
        host="0.0.0.0",
        port=settings.demo_port,
        reload=False,
        log_level=settings.log_level.lower()
    )

