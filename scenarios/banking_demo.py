"""
Banking scenario demo - simulates typical banking operations.
This generates realistic traces for banking workflows.
"""
import asyncio
import httpx
import random
from datetime import datetime


async def banking_scenario():
    """
    Simulate a complete banking workflow:
    1. Get user accounts
    2. Get transaction history
    3. Check fraud on recent transactions
    """
    base_url = "http://localhost:8000"
    
    print("🏦 Banking Scenario Demo")
    print("="*60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Step 1: Get accounts
        print("1️⃣  Fetching user accounts...")
        user_id = f"user_{random.randint(1, 100)}"
        
        try:
            response = await client.get(
                f"{base_url}/api/banking/accounts",
                params={"user_id": user_id}
            )
            response.raise_for_status()
            data = response.json()
            
            print(f"   ✅ Retrieved {len(data['accounts'])} accounts")
            for acc in data['accounts']:
                print(f"      - {acc['account_type']}: ${acc['balance']:.2f}")
            
            account_id = data['accounts'][0]['account_id']
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        await asyncio.sleep(1)
        
        # Step 2: Get transaction history
        print("\n2️⃣  Fetching transaction history...")
        
        try:
            response = await client.get(
                f"{base_url}/api/transactions/history",
                params={"account_id": account_id, "days": 30}
            )
            response.raise_for_status()
            data = response.json()
            
            print(f"   ✅ Retrieved {len(data['transactions'])} transactions")
            print(f"      Total spent: ${data['total_spent']:.2f}")
            
            # Show top 5 transactions
            print("      Recent transactions:")
            for txn in data['transactions'][:5]:
                print(f"        - {txn['merchant']}: ${txn['amount']:.2f} ({txn['category']})")
            
            transactions = data['transactions']
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        await asyncio.sleep(1)
        
        # Step 3: Check fraud on high-value transactions
        print("\n3️⃣  Running fraud checks on high-value transactions...")
        
        high_value_txns = [t for t in transactions if t['amount'] > 200][:3]
        
        for i, txn in enumerate(high_value_txns, 1):
            try:
                response = await client.post(
                    f"{base_url}/api/fraud/check",
                    json={
                        "transaction_id": txn['transaction_id'],
                        "amount": txn['amount'],
                        "currency": txn['currency']
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                status_emoji = "🚨" if data['status'] == 'flagged' else "✅"
                print(f"   {status_emoji} Transaction {i}: {data['status']} (risk: {data['risk_score']:.1f})")
                
                if data['risk_factors']:
                    print(f"      Risk factors: {', '.join(data['risk_factors'])}")
                
            except Exception as e:
                print(f"   ❌ Error checking transaction {i}: {e}")
            
            await asyncio.sleep(0.5)
    
    print("\n" + "="*60)
    print("✅ Banking scenario completed!")
    print("📊 Check Elastic for traces, metrics, and logs")
    print("")


if __name__ == "__main__":
    try:
        asyncio.run(banking_scenario())
    except KeyboardInterrupt:
        print("\n\n⚠️  Scenario interrupted")

