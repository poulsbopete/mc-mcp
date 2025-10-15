# Mastercard API Demo with OpenTelemetry & Elastic Observability

This demo showcases Mastercard APIs integrated with OpenTelemetry for full observability (metrics, traces, logs) flowing to Elastic Serverless, with MCP (Model Context Protocol) workflows for intelligent monitoring.

## 🏗️ Architecture

```
┌─────────────────────┐
│  Mastercard APIs    │
│  - Open Banking     │
│  - Merchant ID      │
│  - Fraud Detection  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Demo Application  │
│   (Python/FastAPI)  │
│  + OpenTelemetry    │
└──────────┬──────────┘
           │
           ├─► Traces
           ├─► Metrics
           └─► Logs
           │
           ▼
┌─────────────────────┐
│ Elastic Serverless  │
│  - APM              │
│  - Logs Explorer    │
│  - Metrics          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   MCP Workflows     │
│  - Query traces     │
│  - Analyze metrics  │
│  - Debug issues     │
└─────────────────────┘
```

## 🚀 Features

- **Mastercard API Integration**: Real-world API calls with authentication
- **OpenTelemetry**: Full instrumentation for distributed tracing
- **Elastic APM**: Automatic performance monitoring
- **MCP Workflows**: Intelligent observability queries via Cursor
- **Demo Scenarios**: Multiple use cases (banking, fraud, merchants)

## 📋 Prerequisites

- Python 3.10+
- Mastercard Developer Account & API Keys
- Elastic Serverless Cluster (configured in .env)
- Cursor with MCP support

## 🔧 Quick Start

1. **Install Dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp env.example .env
   # Edit .env with your Elastic credentials
   # Mock mode is enabled by default for Mastercard APIs
   ```

3. **Run the Demo Application**
   ```bash
   source venv/bin/activate
   python3 demo_app.py
   ```

4. **Generate Test Traffic**
   ```bash
   # In a new terminal, with venv activated
   source venv/bin/activate
   python3 load_test.py --requests 50
   ```
   This creates traces, metrics, and logs in Elastic!

5. **Query with MCP in Cursor**
   ```
   Show me the latest traces from mastercard-demo service
   List all Elasticsearch indices
   What's the average response time for API calls?
   ```

6. **Access the API Documentation**
   ```
   http://localhost:8000/docs
   ```

## 🔑 Environment Variables

- `MASTERCARD_API_KEY`: Your Mastercard API key
- `MASTERCARD_CONSUMER_KEY`: OAuth consumer key
- `MASTERCARD_PRIVATE_KEY_PATH`: Path to your .p12 file
- `ELASTIC_OTLP_ENDPOINT`: Elastic OTLP endpoint
- `ELASTIC_OTEL_API_KEY`: Elastic API key for telemetry
- `ELASTICSEARCH_URL`: Elasticsearch cluster URL
- `ELASTICSEARCH_API_KEY`: API key for querying observability data

## 🎯 Demo Endpoints

### 1. Open Banking Flow
```bash
curl http://localhost:8000/api/banking/accounts
```

### 2. Merchant Lookup
```bash
curl http://localhost:8000/api/merchant/locate?query=coffee
```

### 3. Fraud Detection
```bash
curl -X POST http://localhost:8000/api/fraud/check \
  -H "Content-Type: application/json" \
  -d '{"transaction_id": "txn_123", "amount": 1000}'
```

## 🔍 MCP Workflows

### View Recent Traces
Use Cursor MCP to query:
```
Show me the latest traces from the Mastercard demo
```

### Analyze Performance
```
What's the average response time for merchant API calls?
```

### Debug Errors
```
Show me any errors in the last hour for the fraud detection service
```

## 📊 Observability Features

- **Distributed Tracing**: See full request flow across services
- **Custom Metrics**: Track API calls, response times, error rates
- **Structured Logs**: Correlated with traces via trace_id
- **Service Map**: Visualize dependencies in Elastic APM
- **Real-time Alerts**: Set up alerts based on metrics

## 🏃 Running Examples

```bash
# Run basic demo
python demo_app.py

# Run with specific scenario
python scenarios/banking_demo.py

# Load test with telemetry
python load_test.py --requests 100
```

## 📖 Documentation

- [Quick Start Guide](QUICKSTART.md) - Get up and running in 5 minutes
- [MCP Workflows](MCP_WORKFLOWS.md) - Example observability queries
- [Combined MCP Workflow](MCP_COMBINED_WORKFLOW.md) - **NEW!** Use both Mastercard + Elasticsearch MCP together
- [Mastercard API Documentation](https://developer.mastercard.com/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [Elastic APM](https://www.elastic.co/guide/en/apm/get-started/current/overview.html)
- [MCP Protocol](https://modelcontextprotocol.io/)

## 🤝 Contributing

This is a demo project. Feel free to extend with more Mastercard APIs or observability features!

## 📝 License

MIT License - See LICENSE file for details

