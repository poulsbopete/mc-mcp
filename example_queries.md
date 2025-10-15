# Example MCP Queries for Mastercard Demo

This file contains ready-to-use queries you can ask in Cursor to explore your Mastercard demo observability data.

## 🔍 Basic Exploration

### See Recent Activity
```
Show me the latest 20 traces from mastercard-demo in the last 15 minutes
```

### Check Service Health
```
What's the current health status of the mastercard-demo service?
```

### List Available Indices
```
List all Elasticsearch indices related to mastercard-demo
```

## 📊 Performance Analysis

### Response Time Analysis
```
What's the average response time for mastercard-demo API calls in the last hour?
```

### Slowest Operations
```
Show me the slowest operations in mastercard-demo in the last hour, ordered by duration
```

### Percentile Analysis
```
Calculate p50, p95, and p99 response times for mastercard API calls
```

### Operation Breakdown
```
Show me the average duration for each operation type (banking, merchant, fraud) in the last 2 hours
```

## 🚨 Error Detection

### Find All Errors
```
Show me all errors and exceptions in mastercard-demo from the last hour
```

### Error Rate
```
What's the error rate for mastercard-demo in the last 24 hours?
```

### Specific Error Investigation
```
Show me traces with status code 500 in the last 6 hours
```

### Exception Details
```
Show me all traces where exceptions were recorded
```

## 💳 Fraud Detection Analysis

### High Risk Transactions
```
Show me all fraud checks with risk_score > 70 in the last hour
```

### Flagged Transactions
```
Find all transactions where fraud.status = "flagged"
```

### Fraud Check Volume
```
How many fraud checks were performed in the last 24 hours?
```

### Risk Distribution
```
Show me the distribution of fraud risk scores for today
```

## 🏦 Banking Operations

### Account Queries
```
Show me all open banking API calls from the last hour
```

### Transaction History Requests
```
How many transaction history requests were made today?
```

### Account Access Patterns
```
Show me the most frequently accessed accounts in the last 24 hours
```

## 🏪 Merchant Operations

### Merchant Searches
```
Show me all merchant location searches from the last 2 hours
```

### Popular Search Terms
```
What are the most common merchant search queries today?
```

### Geographic Distribution
```
Show me merchant searches grouped by location
```

### Search Performance
```
What's the average response time for merchant locate operations?
```

## 📈 Metrics and Aggregations

### Request Volume
```
How many total API requests did mastercard-demo handle today?
```

### Requests Per Endpoint
```
Show me request counts grouped by API endpoint for the last hour
```

### Peak Traffic Times
```
When was the peak traffic time for mastercard-demo today?
```

### Success Rate
```
What's the success rate (non-error responses) for mastercard-demo in the last 24 hours?
```

## 🔗 Trace Correlation

### Find Specific Trace
```
Show me the full trace for trace_id: <paste-your-trace-id>
```

### Find Transaction Traces
```
Find all traces containing transaction_id: "txn_123456"
```

### User Activity
```
Show me all traces for user_id: "user_42" in the last hour
```

### Account Activity
```
Find all operations related to account_id: "acc_1234"
```

## 📝 Log Analysis

### Recent Logs
```
Show me the latest 50 log entries from mastercard-demo
```

### Warning Logs
```
Show me all WARNING and ERROR level logs from the last hour
```

### Logs for Trace
```
Show me all logs associated with trace_id: <paste-trace-id>
```

### Fraud Alerts
```
Show me all logs containing "suspicious" or "flagged" in the last 24 hours
```

## 🎯 Advanced Queries

### Multi-Service Traces
```
Show me traces that span multiple services (if you have multiple services)
```

### Long-Running Operations
```
Find operations that took longer than 1 second in the last hour
```

### Failed Operations
```
Show me operations where event.outcome = "failure"
```

### Resource Usage
```
What's the average memory and CPU usage for mastercard-demo?
```

## 📊 Business Intelligence

### Transaction Volume Analysis
```
What's the total transaction amount checked for fraud today?
```

### Popular Merchants
```
Which merchant categories are most searched?
```

### User Engagement
```
How many unique users accessed the banking API today?
```

### API Usage Patterns
```
Show me the hourly breakdown of API calls for the last 24 hours
```

## 🔧 Debugging Workflows

### Debug Slow Request
```
1. "Show me requests slower than 500ms"
2. "Get the trace_id from the result"
3. "Show me the full trace for trace_id: <id>"
4. "Show me logs for that trace_id"
```

### Debug Error
```
1. "Show me recent errors"
2. "What's the exception message?"
3. "Find all traces with the same error"
4. "When did this error start occurring?"
```

### Investigate Fraud Alert
```
1. "Show me flagged transactions in the last hour"
2. "Get details for transaction_id: <id>"
3. "What risk factors were identified?"
4. "Are there similar patterns in other transactions?"
```

## 💡 Pro Tips

### Time Range Formats
- `now-15m` - Last 15 minutes
- `now-1h` - Last hour
- `now-6h` - Last 6 hours
- `now-24h` - Last 24 hours
- `now-7d` - Last 7 days

### Useful Filters
- `service.name: "mastercard-demo"`
- `transaction.type: "request"`
- `span.name: "mastercard.*"`
- `event.outcome: "failure"`
- `http.status_code: 500`

### Index Patterns
- `traces-apm*` - APM traces
- `logs-*` - Application logs
- `metrics-*` - Metrics data

## 🎨 Creating Dashboards

After running queries, you can:
1. Save interesting queries as Saved Searches in Kibana
2. Create visualizations from aggregation results
3. Build dashboards combining multiple views
4. Set up alerts based on query results

---

**Remember:** All these queries work because of the OpenTelemetry instrumentation and the Elastic MCP Server integration!

