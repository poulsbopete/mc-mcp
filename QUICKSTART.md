# 🚀 Quick Start Guide

Get the Mastercard API demo running with full observability in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- An Elastic Serverless account (configured)
- Cursor with MCP support (Elastic MCP Server configured)

## Step 1: Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## Step 2: Configure Environment

Your `.env` file has already been created with:
- ✅ Elastic OTLP endpoint
- ✅ Elastic API keys
- ✅ Default configuration

If you have real Mastercard API credentials, update these values in `.env`:
```env
MASTERCARD_API_KEY=your_actual_key
MASTERCARD_CONSUMER_KEY=your_consumer_key
MASTERCARD_PRIVATE_KEY_PATH=./certs/your-key.p12
```

For demo purposes, mock mode is enabled by default.

## Step 3: Start the Demo

### Option A: Using the run script (recommended)
```bash
./run_demo.sh
```

### Option B: Direct Python
```bash
python demo_app.py
```

The application will start on `http://localhost:8000`

## Step 4: Generate Some Traffic

### Option A: Use the demo endpoint
```bash
curl "http://localhost:8000/api/demo/generate-traffic?requests=20"
```

### Option B: Run the load tester
```bash
python load_test.py --requests 50
```

### Option C: Run scenario demos
```bash
# Banking scenario
python scenarios/banking_demo.py

# Merchant discovery
python scenarios/merchant_demo.py

# Fraud detection
python scenarios/fraud_demo.py
```

## Step 5: Explore with MCP in Cursor

Now you can use natural language queries in Cursor to explore your observability data!

### Example Queries:

**View Recent Activity:**
```
Show me the latest traces from mastercard-demo in the last 15 minutes
```

**Performance Analysis:**
```
What's the average response time for API calls?
```

**Find Errors:**
```
Show me any errors in the last hour
```

**Fraud Detection:**
```
Show me all fraud checks with high risk scores
```

See [MCP_WORKFLOWS.md](MCP_WORKFLOWS.md) for more examples!

## Step 6: Access the API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation where you can:
- Test all endpoints
- See request/response schemas
- Generate traces in real-time

## What You Get

✅ **Full Observability Stack:**
- Distributed tracing (OpenTelemetry)
- Custom metrics (request counts, response times, fraud checks)
- Structured logging (correlated with traces)

✅ **Elastic Integration:**
- All telemetry flows to Elastic Serverless
- Automatic APM integration
- Service maps and dashboards

✅ **MCP Workflows:**
- Query traces with natural language
- Analyze performance patterns
- Debug issues quickly

## Architecture Overview

```
┌─────────────────────────┐
│   Your Requests         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   FastAPI Application   │
│   + OpenTelemetry       │
│   (demo_app.py)         │
└───────────┬─────────────┘
            │
            ├─► Mastercard APIs (mocked)
            │   ├─ Open Banking
            │   ├─ Merchant Locate
            │   └─ Fraud Detection
            │
            ▼
┌─────────────────────────┐
│   OpenTelemetry         │
│   Collector (OTLP)      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Elastic Serverless    │
│   ├─ APM                │
│   ├─ Traces             │
│   ├─ Metrics            │
│   └─ Logs               │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   MCP Server            │
│   (Elasticsearch)       │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Cursor IDE            │
│   (Natural Language)    │
└─────────────────────────┘
```

## Troubleshooting

### Application won't start
- Check that port 8000 is available
- Verify Python 3.10+ is installed
- Make sure all dependencies are installed

### No traces in Elastic
- Verify ELASTIC_OTLP_ENDPOINT in .env
- Check ELASTIC_OTEL_API_KEY is correct
- Wait 1-2 minutes for data to appear
- Generate more traffic

### MCP queries not working
- Ensure Elastic MCP Server is configured in Cursor
- Check ELASTICSEARCH_API_KEY in .env
- Verify ELASTICSEARCH_URL is correct

## Next Steps

1. **Explore the API**: Visit `/docs` and try different endpoints
2. **Run Scenarios**: Execute the demo scenarios to see realistic workflows
3. **Query with MCP**: Use Cursor to explore your observability data
4. **Customize**: Add your own Mastercard API integrations
5. **Monitor**: Set up alerts and dashboards in Elastic

## Useful Commands

```bash
# Start the application
./run_demo.sh

# Generate 100 requests
python load_test.py --requests 100 --concurrent 20

# Run all scenarios
python scenarios/banking_demo.py
python scenarios/merchant_demo.py
python scenarios/fraud_demo.py

# View logs
tail -f logs/app.log  # if you configured file logging
```

## Support & Resources

- [Full Documentation](README.md)
- [MCP Workflows Guide](MCP_WORKFLOWS.md)
- [Elastic APM Docs](https://www.elastic.co/guide/en/apm)
- [Mastercard Developer Portal](https://developer.mastercard.com/)

---

**Happy Coding! 🎉**

