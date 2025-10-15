# 🎬 Live Demo Script: Dual MCP Workflow

**Duration:** 10-15 minutes  
**Goal:** Show how Mastercard + Elasticsearch MCP servers work together for the complete development lifecycle

---

## 🎯 Demo Story

**Scenario:** You're implementing a new fraud detection feature. You need to:
1. Understand the Mastercard Fraud API
2. Implement and test it
3. Verify it's working correctly
4. Find and fix performance issues

Let's see how both MCP servers help!

---

## 📋 Part 1: Research Phase (Mastercard MCP)

**You say:** "I need to implement fraud detection. Let me ask the Mastercard MCP about their API."

### Query 1: Discover Available APIs

**In Cursor, ask Mastercard MCP:**
```
What Mastercard fraud detection APIs are available?
```

**Expected:** List of fraud-related services and their purposes

### Query 2: Get API Specifications

**Ask:**
```
Show me the fraud detection API request parameters and response format
```

**Expected:** 
- Request fields (transaction_id, amount, merchant_id, etc.)
- Response fields (risk_score, status, risk_factors)
- Status codes and error handling

### Query 3: Authentication Requirements

**Ask:**
```
How do I authenticate with Mastercard fraud detection APIs?
```

**Expected:** OAuth 1.0a details, API key requirements, security best practices

---

## 🔨 Part 2: Implementation & Testing

**You say:** "Now let's test our implementation and generate some traffic."

### Step 1: Start the Demo App

```bash
# Show that the app is running
curl http://localhost:8000/health
```

**Expected:** Healthy response with timestamp

### Step 2: Run the MCP Demo Scenario

```bash
cd /opt/mc-mcp
source venv/bin/activate
python3 scenarios/mcp_demo.py
```

**Point out:** This generates various fraud checks with different risk levels:
- Low risk ($10-$25)
- Medium risk ($500)
- High risk ($5000-$7500)

---

## 📊 Part 3: Verification Phase (Elasticsearch MCP)

**You say:** "Let's verify the fraud detection is working correctly using the observability data."

### Query 1: See Recent Activity

**In Cursor, ask Elasticsearch MCP:**
```
Show me all fraud check operations from the last 5 minutes
```

**Expected:** List of fraud check spans with timestamps and trace IDs

**Point out:** 
- ✅ All operations successful
- ⏱️ Response times visible
- 🆔 Trace IDs for deep dive

### Query 2: Analyze Risk Scores

**Ask:**
```
Show me fraud checks where fraud.risk_score > 70 from the last 10 minutes
```

**Expected:** High-risk transactions that were flagged

**Compare with Mastercard MCP:** 
- Ask Mastercard MCP: "What risk score threshold should trigger fraud alerts?"
- Verify our implementation matches best practices

### Query 3: Check Performance

**Ask:**
```
What's the average duration for fraud check operations?
```

**Expected:** Average response time metrics

---

## 🔍 Part 4: Deep Dive Investigation

**You say:** "I noticed one transaction was flagged. Let's investigate why."

### Query 1: Find Flagged Transactions

**Ask Elasticsearch MCP:**
```
Show me fraud checks where fraud.status equals "flagged"
```

**Expected:** Transactions with high risk scores and flagged status

**Note the trace_id** from one of the results (e.g., `9fdb8d2b7c53b58dfb73c9eae519795a`)

### Query 2: Get Full Trace Details

**Ask:**
```
Show me all spans for trace ID 9fdb8d2b7c53b58dfb73c9eae519795a
```

**Expected:** Complete trace showing:
1. Initial HTTP request
2. Fraud check API call
3. Mastercard client operation
4. Response generation

**Point out the custom attributes:**
- `transaction.amount`: $4,829.01
- `fraud.risk_score`: 77.98
- `fraud.status`: flagged
- `merchant.id`: mch_3325

### Query 3: Cross-Reference with Documentation

**Ask Mastercard MCP:**
```
What risk factors does the Mastercard fraud API consider?
```

**Expected:** List of risk factors (transaction size, merchant category, location, velocity, etc.)

**Compare:** Our trace captured the right fields!

---

## 🚀 Part 5: Performance Optimization

**You say:** "Let's check if there are any performance bottlenecks."

### Query 1: Find Slow Operations

**Ask Elasticsearch MCP:**
```
Show me spans with duration greater than 500 milliseconds
```

**Expected:** Longer-running operations

### Query 2: Analyze Response Time Distribution

**Ask:**
```
Show me the p95 and p99 response times for fraud checks
```

**Expected:** Performance percentiles

### Query 3: Check API Guidelines

**Ask Mastercard MCP:**
```
What are the performance best practices for fraud detection API calls?
```

**Expected:** 
- Recommended batch sizes
- Rate limits
- Caching strategies
- Timeout recommendations

---

## 🎓 Part 6: The "Aha!" Moment

**You say:** "This is where the magic happens - both MCP servers working together!"

### Scenario: Validate Implementation Against Spec

**1. Ask Mastercard MCP:**
```
What HTTP headers should be included in fraud detection API requests?
```

**2. Ask Elasticsearch MCP:**
```
Show me the HTTP headers from recent fraud check requests
```

**3. Compare:**
- Are all required headers present?
- Is authentication working correctly?
- Are we following best practices?

---

## 🎯 Part 7: Continuous Monitoring Setup

**You say:** "Now let's set up ongoing monitoring."

### Query 1: Error Monitoring

**Ask Elasticsearch MCP:**
```
Show me any fraud checks with errors or exceptions in the last hour
```

**Expected:** Error traces (if any)

### Query 2: Business Metrics

**Ask:**
```
How many transactions were flagged vs approved in the last 10 minutes?
```

**Expected:** Business KPIs from traces

### Query 3: Compliance Check

**Ask Mastercard MCP:**
```
What data retention and privacy requirements apply to fraud detection data?
```

**Then verify with Elasticsearch:**
```
Show me what transaction data we're storing in traces
```

**Point out:** We can verify compliance by comparing docs vs. implementation!

---

## 🏆 Key Takeaways

**Summarize:** "We just completed a full development cycle using both MCP servers:"

### With Mastercard MCP, we:
✅ Discovered available APIs  
✅ Got detailed specifications  
✅ Learned authentication requirements  
✅ Found best practices and guidelines  
✅ Validated our implementation

### With Elasticsearch MCP, we:
✅ Verified implementation correctness  
✅ Analyzed real-time performance  
✅ Investigated specific transactions  
✅ Found optimization opportunities  
✅ Monitored business metrics

### Together, they provide:
🔄 **Documentation-to-Implementation feedback loop**  
🐛 **Faster debugging with context**  
📊 **Data-driven development decisions**  
✅ **Automatic compliance verification**  
🚀 **Production-ready observability**

---

## 💡 Bonus Queries to Try

### Mastercard MCP Deep Dives:
```
Show me code examples for OAuth 1.0a authentication
What's the rate limit for fraud detection APIs?
How do I handle webhook callbacks for async fraud checks?
What test data can I use in sandbox mode?
```

### Elasticsearch MCP Advanced Queries:
```
Show me the correlation between transaction amount and risk score
List all unique merchant IDs from fraud checks today
What's the error rate by API endpoint?
Show me traces that took longer than the p99 threshold
```

### Combined Investigations:
```
# Mastercard: What fields are required for merchant risk assessment?
# Elastic: Show me merchant_id attributes from recent traces
# Compare: Are we collecting all required fields?
```

---

## 🎬 Demo Tips

1. **Keep it flowing:** Have queries ready in a text file to copy/paste
2. **Show real data:** The mcp_demo.py generates perfect test data
3. **Tell the story:** Frame it as solving a real problem
4. **Compare and contrast:** Show how the two MCPs complement each other
5. **End with impact:** Emphasize time saved and confidence gained

---

## 🔗 Quick Reference Commands

### Start Demo:
```bash
# Terminal 1: Demo app
cd /opt/mc-mcp && source venv/bin/activate && python3 demo_app.py

# Terminal 2: Generate traffic
cd /opt/mc-mcp && source venv/bin/activate && python3 scenarios/mcp_demo.py
```

### Check Health:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

### More Traffic:
```bash
python3 load_test.py --requests 50
```

---

**Ready to present? Run the MCP demo scenario and start querying!** 🚀

