"""
Fraud detection scenario - simulates fraud checking on various transactions.
This generates realistic traces for fraud detection workflows.
"""
import asyncio
import httpx
import random
from datetime import datetime


async def fraud_scenario():
    """
    Simulate fraud detection workflow:
    1. Check various transaction amounts
    2. Test edge cases (high amounts, unusual patterns)
    3. Generate both approved and flagged transactions
    """
    base_url = "http://localhost:8000"
    
    print("🔒 Fraud Detection Scenario")
    print("="*60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("")
    
    # Various transaction scenarios
    transactions = [
        {"amount": 25.50, "description": "Small coffee purchase"},
        {"amount": 89.99, "description": "Grocery shopping"},
        {"amount": 450.00, "description": "Electronics purchase"},
        {"amount": 1250.00, "description": "Laptop purchase"},
        {"amount": 3500.00, "description": "High-value jewelry"},
        {"amount": 7500.00, "description": "Suspicious large transaction"},
        {"amount": 15000.00, "description": "Very high value - likely fraud"},
        {"amount": 50.00, "description": "Gas station"},
        {"amount": 150.00, "description": "Restaurant dinner"},
        {"amount": 2000.00, "description": "Hotel booking"}
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        flagged_count = 0
        approved_count = 0
        
        for i, txn in enumerate(transactions, 1):
            txn_id = f"txn_{random.randint(100000, 999999)}"
            
            print(f"{i}️⃣  Checking transaction: ${txn['amount']:.2f} - {txn['description']}")
            
            try:
                response = await client.post(
                    f"{base_url}/api/fraud/check",
                    json={
                        "transaction_id": txn_id,
                        "amount": txn['amount'],
                        "merchant_id": f"mch_{random.randint(1000, 9999)}",
                        "currency": "USD"
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                status = data['status']
                risk_score = data['risk_score']
                
                if status == 'flagged':
                    flagged_count += 1
                    print(f"   🚨 FLAGGED - Risk Score: {risk_score:.1f}")
                    if data['risk_factors']:
                        print(f"      Risk Factors: {', '.join(data['risk_factors'])}")
                    print(f"      Recommendation: {data['recommendation'].upper()}")
                else:
                    approved_count += 1
                    print(f"   ✅ APPROVED - Risk Score: {risk_score:.1f}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            await asyncio.sleep(0.8)
        
        # Summary
        print("\n" + "="*60)
        print("📊 Fraud Detection Summary")
        print("="*60)
        print(f"Total Transactions:    {len(transactions)}")
        print(f"Approved:              {approved_count} ({approved_count/len(transactions)*100:.1f}%)")
        print(f"Flagged:               {flagged_count} ({flagged_count/len(transactions)*100:.1f}%)")
        print("="*60)
        print("\n✅ Fraud detection scenario completed!")
        print("📊 Check Elastic for fraud detection traces and metrics")
        print("")


if __name__ == "__main__":
    try:
        asyncio.run(fraud_scenario())
    except KeyboardInterrupt:
        print("\n\n⚠️  Scenario interrupted")

