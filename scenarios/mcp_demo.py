#!/usr/bin/env python3
"""
MCP Demo Scenario: Exercise both Elasticsearch and Mastercard MCP servers

This scenario demonstrates:
1. Looking up Mastercard API capabilities via MCP
2. Making API calls through the demo app
3. Querying observability data via Elasticsearch MCP
"""

import asyncio
import httpx
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def run_mcp_demo_scenario():
    """
    Run a scenario that generates diverse API traffic for MCP analysis.
    """
    
    print("🎯 MCP Demo Scenario Starting")
    print("=" * 60)
    print("\n📝 Instructions:")
    print("   1. Run this script to generate API traffic")
    print("   2. Use Mastercard MCP: 'Show me Mastercard fraud detection API documentation'")
    print("   3. Use Elastic MCP: 'Show me fraud check traces with high risk scores'")
    print("   4. Compare the API specs with actual implementation traces")
    print("=" * 60)
    print()
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # === Scenario 1: Banking Operations ===
        print("\n💳 Scenario 1: Banking Operations")
        print("-" * 40)
        
        users = ["user_100", "user_200", "user_300"]
        for user_id in users:
            try:
                resp = await client.get(f"{BASE_URL}/api/banking/accounts", params={"user_id": user_id})
                if resp.status_code == 200:
                    data = resp.json()
                    print(f"  ✓ Retrieved {len(data['accounts'])} accounts for {user_id}")
                    
                    # Get transaction history for first account
                    if data['accounts']:
                        account_id = data['accounts'][0]['account_id']
                        hist_resp = await client.get(
                            f"{BASE_URL}/api/transactions/history",
                            params={"account_id": account_id, "days": 30}
                        )
                        if hist_resp.status_code == 200:
                            hist_data = hist_resp.json()
                            print(f"  ✓ Retrieved {len(hist_data['transactions'])} transactions for {account_id}")
            except Exception as e:
                print(f"  ✗ Error: {e}")
            
            await asyncio.sleep(0.5)
        
        # === Scenario 2: Fraud Detection with Various Risk Levels ===
        print("\n🚨 Scenario 2: Fraud Detection Analysis")
        print("-" * 40)
        
        # Generate transactions with different amounts to trigger different risk scores
        test_transactions = [
            {"txn_id": "txn_low_risk_001", "amount": 10.50, "expected": "low risk"},
            {"txn_id": "txn_med_risk_001", "amount": 500.00, "expected": "medium risk"},
            {"txn_id": "txn_high_risk_001", "amount": 5000.00, "expected": "high risk"},
            {"txn_id": "txn_low_risk_002", "amount": 25.99, "expected": "low risk"},
            {"txn_id": "txn_high_risk_002", "amount": 7500.00, "expected": "high risk"},
        ]
        
        flagged_count = 0
        approved_count = 0
        
        for txn in test_transactions:
            try:
                resp = await client.post(
                    f"{BASE_URL}/api/fraud/check",
                    json={
                        "transaction_id": txn["txn_id"],
                        "amount": txn["amount"],
                        "merchant_id": "mch_test_123"
                    }
                )
                if resp.status_code == 200:
                    data = resp.json()
                    risk_score = data['risk_score']
                    status = data['status']
                    
                    if status == "flagged":
                        flagged_count += 1
                        icon = "🚨"
                    else:
                        approved_count += 1
                        icon = "✓"
                    
                    print(f"  {icon} {txn['txn_id']}: ${txn['amount']:,.2f} -> Risk: {risk_score:.1f} ({status})")
            except Exception as e:
                print(f"  ✗ Error checking {txn['txn_id']}: {e}")
            
            await asyncio.sleep(0.3)
        
        print(f"\n  Summary: {approved_count} approved, {flagged_count} flagged")
        
        # === Scenario 3: Merchant Discovery ===
        print("\n🏪 Scenario 3: Merchant Discovery")
        print("-" * 40)
        
        searches = [
            {"query": "coffee", "lat": 37.7749, "lon": -122.4194, "radius": 5},
            {"query": "atm", "lat": 37.3382, "lon": -121.8863, "radius": 2},
            {"query": "pharmacy", "lat": 37.8044, "lon": -122.2712, "radius": 3},
            {"query": "restaurant", "lat": 37.4419, "lon": -122.1430, "radius": 10},
        ]
        
        for search in searches:
            try:
                resp = await client.get(
                    f"{BASE_URL}/api/merchant/locate",
                    params={
                        "query": search["query"],
                        "latitude": search["lat"],
                        "longitude": search["lon"],
                        "radius": search["radius"]
                    }
                )
                if resp.status_code == 200:
                    data = resp.json()
                    print(f"  ✓ Found {len(data['merchants'])} {search['query']} locations "
                          f"near ({search['lat']:.4f}, {search['lon']:.4f})")
            except Exception as e:
                print(f"  ✗ Error: {e}")
            
            await asyncio.sleep(0.4)
        
        # === Scenario 4: Error Conditions ===
        print("\n⚠️  Scenario 4: Error Handling")
        print("-" * 40)
        
        # Test invalid requests to generate error traces
        error_tests = [
            ("Invalid user", {"url": f"{BASE_URL}/api/banking/accounts", "params": {"user_id": ""}}),
            ("Negative amount", {"url": f"{BASE_URL}/api/fraud/check", "json": {"transaction_id": "txn_err_001", "amount": -100}}),
        ]
        
        for test_name, request_data in error_tests:
            try:
                if "json" in request_data:
                    resp = await client.post(**request_data)
                else:
                    resp = await client.get(**request_data)
                print(f"  ✓ {test_name}: Status {resp.status_code}")
            except Exception as e:
                print(f"  ✓ {test_name}: Caught expected error")
    
    print("\n" + "=" * 60)
    print("✅ MCP Demo Scenario Complete!")
    print("=" * 60)
    print("\n🔍 Now try these MCP queries:")
    print()
    print("📊 Elasticsearch MCP Queries:")
    print("   - 'Show me all fraud checks from the last 5 minutes'")
    print("   - 'What's the average risk score for flagged transactions?'")
    print("   - 'Show me traces with errors or exceptions'")
    print("   - 'List all merchant search operations'")
    print()
    print("📚 Mastercard MCP Queries:")
    print("   - 'Show me the Fraud Detection API reference'")
    print("   - 'What are the request parameters for merchant location API?'")
    print("   - 'How do I authenticate with Mastercard APIs?'")
    print("   - 'What response codes does the fraud API return?'")
    print()
    print("🔗 Combined Workflow:")
    print("   1. Ask Mastercard MCP: 'What fields are in the fraud detection response?'")
    print("   2. Ask Elastic MCP: 'Show me fraud.risk_score values from recent traces'")
    print("   3. Compare: Do the traces match the API spec?")
    print()

if __name__ == "__main__":
    asyncio.run(run_mcp_demo_scenario())

