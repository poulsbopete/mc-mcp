# 🎯 Quick Reference: Demo Queries

Copy/paste these queries during your demo!

---

## 🔵 Mastercard MCP Queries

### API Discovery
```
What Mastercard fraud detection APIs are available?
```

### API Specifications
```
Show me the fraud detection API request parameters and response format
```

### Authentication
```
How do I authenticate with Mastercard fraud detection APIs?
```

### Best Practices
```
What are the performance best practices for fraud detection API calls?
```

### Risk Factors
```
What risk factors does the Mastercard fraud API consider?
```

### Compliance
```
What data retention and privacy requirements apply to fraud detection data?
```

---

## 🟢 Elasticsearch MCP Queries

### Recent Activity
```
Show me all fraud check operations from the last 5 minutes
```

### High Risk Transactions
```
Show me fraud checks where fraud.risk_score > 70 from the last 10 minutes
```

### Performance Metrics
```
What's the average duration for fraud check operations?
```

### Flagged Transactions
```
Show me fraud checks where fraud.status equals "flagged"
```

### Slow Operations
```
Show me spans with duration greater than 500 milliseconds
```

### Error Monitoring
```
Show me any fraud checks with errors or exceptions in the last hour
```

### Business KPIs
```
How many transactions were flagged vs approved in the last 10 minutes?
```

### Trace Investigation
```
Show me all spans for trace ID [PASTE_TRACE_ID_HERE]
```

### All Traces
```
Show me the latest traces from mastercard-demo service
```

### Merchant Analysis
```
List all unique merchant IDs from fraud checks today
```

---

## 🔄 Combined Workflow Examples

### 1. Implementation Validation
**Mastercard:** `What HTTP headers should be included in fraud detection API requests?`  
**Elastic:** `Show me the HTTP headers from recent fraud check requests`  
**Compare:** Are all required headers present?

### 2. Field Verification
**Mastercard:** `What fields are required for merchant risk assessment?`  
**Elastic:** `Show me merchant_id attributes from recent traces`  
**Compare:** Are we collecting all required fields?

### 3. Performance Benchmarking
**Mastercard:** `What's the expected response time for fraud detection?`  
**Elastic:** `What's the p95 response time for fraud checks?`  
**Compare:** Are we meeting SLAs?

### 4. Risk Score Analysis
**Mastercard:** `What risk score threshold should trigger fraud alerts?`  
**Elastic:** `Show me the distribution of risk scores from recent fraud checks`  
**Compare:** Are we using appropriate thresholds?

---

## ⚡ Quick Commands

### Start Demo App
```bash
cd /opt/mc-mcp && source venv/bin/activate && python3 demo_app.py
```

### Run MCP Scenario
```bash
cd /opt/mc-mcp && source venv/bin/activate && python3 scenarios/mcp_demo.py
```

### Generate More Traffic
```bash
python3 load_test.py --requests 50
```

### Check Health
```bash
curl http://localhost:8000/health
```

---

## 📊 Expected Results Cheat Sheet

| Query Type | What to Point Out |
|------------|-------------------|
| Recent traces | ✅ All successful, ⏱️ Response times visible |
| High risk transactions | 🚨 Flagged status, 📈 Risk scores > 70 |
| Performance | ⚡ Average ~300-400ms, some longer |
| Flagged transactions | 💰 High transaction amounts, 🎯 Specific merchants |
| Trace details | 🔍 Complete flow, 📝 Custom attributes captured |
| Business KPIs | 📊 Approval vs flagged ratio, 💹 Transaction volumes |

---

## 🎬 Demo Flow Checklist

- [ ] Demo app running on port 8000
- [ ] MCP demo scenario executed
- [ ] Both MCP servers showing in Cursor
- [ ] Queries ready to copy/paste
- [ ] Story prepared (research → implement → verify → optimize)
- [ ] Terminal windows visible and organized
- [ ] Cursor with MCP panel open

---

## 💡 Ad-Lib Talking Points

**When showing Mastercard MCP:**
- "This is like having a Mastercard API expert sitting next to me"
- "Instead of searching through docs, I just ask"
- "It knows the latest API versions and best practices"

**When showing Elasticsearch MCP:**
- "Now let's see what actually happened in production"
- "This is our implementation's 'source of truth'"
- "We can verify everything we just learned about the API"

**When showing them together:**
- "This is the magic - documentation meets reality"
- "We can instantly validate our implementation against specs"
- "This feedback loop would normally take hours or days"

---

**Pro Tip:** Keep this file open during your demo for quick copy/paste! 📋

