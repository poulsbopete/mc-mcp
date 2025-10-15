# MCP Workflows for Mastercard Demo Observability

This document provides example workflows for using the Elastic MCP Server with Cursor to monitor and analyze your Mastercard API demo.

## 🎯 Prerequisites

1. Elastic MCP Server configured in Cursor (check `mcp_config.json`)
2. Demo application running (`python demo_app.py`)
3. Some traffic generated to create telemetry data

## 📊 Common Workflows

### 1. View Recent API Traces

**Query in Cursor:**
```
Show me the latest traces from the mastercard-demo service in the last 15 minutes
```

**What you'll see:**
- Distributed traces showing the flow of requests
- Span details for each Mastercard API call
- Performance metrics (duration, status)
- Trace IDs for correlation

### 2. Analyze API Performance

**Query in Cursor:**
```
What's the average response time for API calls in the mastercard-demo service?
```

**Follow-up queries:**
```
Show me the slowest API endpoints in the last hour
Which Mastercard API calls are taking the longest?
```

### 3. Monitor Fraud Detection

**Query in Cursor:**
```
Show me all fraud check operations with high risk scores in the last hour
```

**What to look for:**
- Risk scores above 70
- Flagged transactions
- Risk factors identified

### 4. Debug Errors

**Query in Cursor:**
```
Show me any errors or exceptions in the mastercard-demo service
```

**Follow-up:**
```
Get the full trace for error with trace_id: <paste-trace-id>
Show me the logs around timestamp <paste-timestamp>
```

### 5. Track Specific Transactions

**Query in Cursor:**
```
Find traces containing transaction_id "txn_12345"
```

**What you'll discover:**
- Full request/response flow
- All services involved
- Any errors or warnings
- Performance bottlenecks

### 6. Service Health Overview

**Query in Cursor:**
```
Show me the health metrics for mastercard-demo service
```

**Metrics to analyze:**
- Request rate (requests per second)
- Error rate (percentage)
- Response time (p50, p95, p99)
- Active spans

### 7. API Usage Patterns

**Query in Cursor:**
```
Show me the most frequently called Mastercard API endpoints
```

**Analysis:**
```
Compare response times between open banking and fraud detection APIs
Which API operations have the highest error rates?
```

### 8. Correlate Logs and Traces

**Query in Cursor:**
```
Show me logs for trace_id <paste-trace-id>
```

**Benefits:**
- See exact log messages during a trace
- Debug issues with full context
- Understand decision flow

## 🚀 Advanced Workflows

### Performance Investigation

```
1. "Show me traces with duration > 500ms"
2. "What's causing the slowest requests in merchant location API?"
3. "Are there any database timeouts?"
```

### Security Monitoring

```
1. "Show me all fraud checks that were flagged"
2. "List transactions with risk_score > 80"
3. "Are there any unusual patterns in authentication?"
```

### Business Analytics

```
1. "How many merchant searches happened today?"
2. "What's the average transaction amount checked for fraud?"
3. "Which merchant categories are most popular?"
```

### Troubleshooting

```
1. "Show me the error rate trend for the last 6 hours"
2. "Find traces with status code 500"
3. "What errors occurred during transaction history calls?"
```

## 📝 Example MCP Commands

### List Available Indices

```
List all Elasticsearch indices for the mastercard demo
```

### Query Specific Index

```
Search the traces-apm* index for mastercard-demo service
```

### Aggregate Metrics

```
Calculate average response time for api.fraud.check operations
```

### ES|QL Queries

```
Run an ES|QL query to show top 10 slowest operations
```

## 🎨 Visualization Tips

After getting data via MCP, you can:

1. **Create Dashboards in Elastic**: Use trace IDs to deep-dive in Kibana
2. **Set Up Alerts**: Configure alerts based on your findings
3. **Export Data**: Save query results for reporting
4. **Compare Periods**: Query different time ranges to compare performance

## 🔧 Useful Filters

When querying via MCP, use these filters:

```json
{
  "service.name": "mastercard-demo",
  "transaction.type": "request",
  "span.name": "mastercard.*",
  "event.outcome": "failure"
}
```

## 📅 Time Range Examples

- `now-15m` - Last 15 minutes
- `now-1h` - Last hour  
- `now-24h` - Last 24 hours
- `now-7d` - Last 7 days
- `2024-01-01T00:00:00Z,2024-01-01T23:59:59Z` - Specific date range

## 🎯 Real-World Scenarios

### Scenario 1: Investigating Slow Performance

```
User: "The merchant search feels slow"

You (via MCP):
1. "Show me response times for merchant.locate operations in the last hour"
2. "What's the p95 response time for merchant searches?"
3. "Show me the slowest merchant search traces"
4. Analyze the trace to find bottlenecks
```

### Scenario 2: Fraud Alert Investigation

```
Alert: "High number of flagged transactions"

You (via MCP):
1. "How many fraud checks were flagged in the last hour?"
2. "Show me fraud checks with risk_score > 90"
3. "Get the full trace for transaction_id <id>"
4. Review risk factors and patterns
```

### Scenario 3: API Integration Issues

```
User: "Getting errors from Open Banking API"

You (via MCP):
1. "Show me errors in open_banking operations"
2. "What's the error rate for get_accounts calls?"
3. "Show me the error messages and stack traces"
4. Review the failing traces for patterns
```

## 🌟 Pro Tips

1. **Use Trace IDs**: Always capture trace_ids from responses for debugging
2. **Set Time Ranges**: Be specific about time ranges to get relevant data
3. **Filter Early**: Use filters to narrow down large result sets
4. **Combine Queries**: Start broad, then narrow based on findings
5. **Save Queries**: Document useful queries for your team

## 📚 Additional Resources

- [Elastic APM Documentation](https://www.elastic.co/guide/en/apm/guide/current/index.html)
- [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)

---

**Happy Debugging! 🔍✨**

