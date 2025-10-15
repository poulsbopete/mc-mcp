# 🔗 Combined MCP Workflow Guide

This guide shows how to use **both MCP servers together** for a complete development workflow:
- **Mastercard MCP** → API documentation and integration guides
- **Elasticsearch MCP** → Observability data (traces, logs, metrics)

## 🎯 Why Use Both Together?

1. **Documentation-Driven Development**: Look up API specs via Mastercard MCP
2. **Implementation**: Build features in the demo app
3. **Verification**: Query traces via Elasticsearch MCP to verify implementation
4. **Debugging**: Compare actual behavior (traces) with expected behavior (docs)

## 🚀 Quick Demo

### Step 1: Run the MCP Demo Scenario

```bash
cd /opt/mc-mcp
source venv/bin/activate
python3 scenarios/mcp_demo.py
```

This generates diverse API traffic including:
- Banking account queries
- Fraud detection checks (various risk levels)
- Merchant location searches
- Error conditions

### Step 2: Query Mastercard Documentation

Use the Mastercard MCP server to understand the APIs:

```
Show me the Mastercard Fraud Detection API documentation
```

```
What are the request and response parameters for the fraud check endpoint?
```

```
How does Mastercard recommend implementing fraud scoring?
```

### Step 3: Query Observability Data

Use the Elasticsearch MCP server to see what actually happened:

```
Show me all fraud check operations from the last 10 minutes
```

```
What's the average risk score for flagged transactions?
```

```
Show me traces where fraud.status equals 'flagged'
```

### Step 4: Compare & Validate

Compare the documentation with actual implementation:

**Ask Mastercard MCP:**
```
What fields should be in a fraud detection response?
```

**Then ask Elasticsearch MCP:**
```
Show me the attributes captured in fraud check spans
```

**Validate:** Do the traces include all required fields from the spec?

## 💡 Real-World Workflows

### Workflow 1: Implementing a New Feature

1. **📚 Research** (Mastercard MCP):
   ```
   Show me the Transaction History API documentation
   What authentication is required?
   What are the rate limits?
   ```

2. **💻 Implement** the feature in `demo_app.py`

3. **🧪 Test** by generating traffic:
   ```bash
   python3 scenarios/mcp_demo.py
   ```

4. **📊 Verify** (Elasticsearch MCP):
   ```
   Show me traces for the new transaction history endpoint
   What's the average response time?
   Are there any errors?
   ```

### Workflow 2: Debugging Performance Issues

1. **🔍 Identify** (Elasticsearch MCP):
   ```
   Show me the slowest API operations in the last hour
   What spans have duration > 1 second?
   ```

2. **📖 Check Expected Behavior** (Mastercard MCP):
   ```
   What's the expected response time for the merchant location API?
   Are there any performance best practices?
   ```

3. **🔧 Optimize** your code based on findings

4. **✅ Validate** (Elasticsearch MCP):
   ```
   Show me recent merchant location traces
   Has the average response time improved?
   ```

### Workflow 3: Security & Compliance Review

1. **📋 Check Requirements** (Mastercard MCP):
   ```
   What security requirements does Mastercard have for fraud detection?
   Show me OAuth 1.0a integration guide
   ```

2. **🔐 Audit Implementation** (Elasticsearch MCP):
   ```
   Show me all authentication-related spans
   Are API keys being logged? (they shouldn't be)
   Show me any traces with security errors
   ```

3. **✓ Verify Compliance** by comparing docs vs. implementation

### Workflow 4: API Migration or Updates

1. **📰 Check for Changes** (Mastercard MCP):
   ```
   What's new in the latest Fraud Detection API version?
   Are there any deprecated fields?
   ```

2. **📊 Assess Current Usage** (Elasticsearch MCP):
   ```
   Show me all API calls using deprecated fields
   What's our current API version distribution?
   ```

3. **🔄 Plan Migration** based on usage patterns

4. **✅ Verify** after migration:
   ```
   Show me error rates before and after the migration
   Are all calls using the new API version?
   ```

## 🎓 Example Queries

### Combined Investigation: Fraud Detection

**1. Learn about the API** (Mastercard MCP):
```
What parameters does the Mastercard Fraud Detection API accept?
```

**Expected Answer:**
- Transaction ID
- Amount
- Merchant ID
- Timestamp
- Risk factors

**2. Check implementation** (Elasticsearch MCP):
```
Show me fraud check spans and their attributes
```

**3. Validate:**
- Are all required parameters being sent?
- Are response fields being captured in traces?
- Do the risk scores follow expected patterns?

### Combined Investigation: Merchant Search

**1. Understand the spec** (Mastercard MCP):
```
Show me the Merchant Locator API documentation
What's the maximum search radius?
```

**2. Check actual usage** (Elasticsearch MCP):
```
Show me all merchant location searches
What radius values are being used?
List merchants found per search
```

**3. Optimize:**
- Are we using optimal radius values?
- Are we over-fetching data?
- Should we implement caching?

## 🏗️ Architecture: How It All Fits Together

```
┌─────────────────────────────────────────────────────────┐
│                    Cursor IDE                           │
├─────────────────────┬───────────────────────────────────┤
│  Mastercard MCP     │    Elasticsearch MCP              │
│  (Documentation)    │    (Observability)                │
└──────────┬──────────┴───────────────┬──────────────────┘
           │                          │
           ▼                          ▼
    ┌─────────────┐           ┌─────────────┐
    │ Mastercard  │           │  Elastic    │
    │ Developer   │           │ Serverless  │
    │ Portal      │           │  Cluster    │
    └─────────────┘           └──────┬──────┘
                                     │
                                     │ OTLP
                                     │
                              ┌──────▼──────┐
                              │ Demo App    │
                              │ (FastAPI)   │
                              │ + OTel      │
                              └─────────────┘
```

## 📝 Best Practices

1. **Start with Documentation**: Always query Mastercard MCP before implementing
2. **Verify with Traces**: Use Elasticsearch MCP to confirm implementation
3. **Track Attributes**: Ensure traces capture all important fields from the API spec
4. **Compare Patterns**: Look for discrepancies between docs and actual behavior
5. **Iterate**: Use insights from traces to improve implementation

## 🎯 Advanced Use Cases

### Use Case 1: Generate Test Cases from API Specs

1. Query Mastercard MCP for API parameter validation rules
2. Generate test scenarios based on those rules
3. Run tests and capture traces
4. Use Elasticsearch MCP to verify all edge cases are covered

### Use Case 2: Auto-Generate Documentation

1. Query Elasticsearch MCP for actual API usage patterns
2. Query Mastercard MCP for official API specs
3. Compare and document any differences
4. Generate internal docs combining both sources

### Use Case 3: Compliance Monitoring

1. Set up MCP queries for compliance checks
2. Schedule regular reviews of:
   - Are we following Mastercard's security guidelines? (Mastercard MCP)
   - Are our traces showing compliant behavior? (Elasticsearch MCP)
3. Create alerts for non-compliant patterns

## 🔄 Continuous Workflow

Make this part of your daily development:

**Morning:**
- Check Mastercard MCP for any API updates
- Review Elasticsearch MCP for overnight errors

**During Development:**
- Reference Mastercard MCP for implementation details
- Test and verify with Elasticsearch MCP queries

**Before Deployment:**
- Validate all features match Mastercard specs
- Confirm traces show expected patterns

**After Deployment:**
- Monitor with Elasticsearch MCP
- Compare production patterns with dev patterns

## 🎉 Try It Now!

Run the demo scenario:
```bash
python3 scenarios/mcp_demo.py
```

Then try these queries in Cursor:

**Mastercard MCP:**
- "Show me all available Mastercard APIs"
- "What's the fraud detection API specification?"

**Elasticsearch MCP:**
- "Show me recent fraud checks"
- "What's the average API response time?"

**Compare the two!** 🔍

---

**Happy Developing with MCP! 🚀**

