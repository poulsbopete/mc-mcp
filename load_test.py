"""
Load testing script for Mastercard Demo.
Generates traffic to populate Elastic with traces, metrics, and logs.
"""
import asyncio
import httpx
import random
import argparse
from datetime import datetime
import sys


class LoadTester:
    """Generate load for the Mastercard demo API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {
            "success": 0,
            "errors": 0,
            "total": 0
        }
    
    async def test_accounts(self, client: httpx.AsyncClient):
        """Test banking accounts endpoint."""
        user_id = f"user_{random.randint(1, 100)}"
        try:
            response = await client.get(f"{self.base_url}/api/banking/accounts", params={"user_id": user_id})
            response.raise_for_status()
            self.results["success"] += 1
            return "accounts", True
        except Exception as e:
            self.results["errors"] += 1
            return "accounts", False
    
    async def test_merchants(self, client: httpx.AsyncClient):
        """Test merchant location endpoint."""
        queries = ["coffee", "restaurant", "gas", "grocery", "pharmacy", "bank", "atm"]
        query = random.choice(queries)
        try:
            response = await client.get(
                f"{self.base_url}/api/merchant/locate",
                params={
                    "query": query,
                    "latitude": round(random.uniform(37.0, 38.0), 4),
                    "longitude": round(random.uniform(-123.0, -122.0), 4),
                    "radius": random.randint(1, 10)
                }
            )
            response.raise_for_status()
            self.results["success"] += 1
            return "merchants", True
        except Exception as e:
            self.results["errors"] += 1
            return "merchants", False
    
    async def test_fraud(self, client: httpx.AsyncClient):
        """Test fraud detection endpoint."""
        try:
            response = await client.post(
                f"{self.base_url}/api/fraud/check",
                json={
                    "transaction_id": f"txn_{random.randint(100000, 999999)}",
                    "amount": round(random.uniform(10, 5000), 2),
                    "merchant_id": f"mch_{random.randint(1000, 9999)}",
                    "currency": "USD"
                }
            )
            response.raise_for_status()
            self.results["success"] += 1
            return "fraud", True
        except Exception as e:
            self.results["errors"] += 1
            return "fraud", False
    
    async def test_transactions(self, client: httpx.AsyncClient):
        """Test transaction history endpoint."""
        try:
            response = await client.get(
                f"{self.base_url}/api/transactions/history",
                params={
                    "account_id": f"acc_{random.randint(1000, 9999)}",
                    "days": random.randint(7, 90)
                }
            )
            response.raise_for_status()
            self.results["success"] += 1
            return "transactions", True
        except Exception as e:
            self.results["errors"] += 1
            return "transactions", False
    
    async def run_single_request(self, client: httpx.AsyncClient):
        """Run a random API request."""
        operations = [
            self.test_accounts,
            self.test_merchants,
            self.test_fraud,
            self.test_transactions
        ]
        
        operation = random.choice(operations)
        return await operation(client)
    
    async def run_load_test(self, total_requests: int, concurrent: int = 10):
        """Run load test with specified parameters."""
        print(f"🔥 Starting load test")
        print(f"   Total requests: {total_requests}")
        print(f"   Concurrent: {concurrent}")
        print(f"   Target: {self.base_url}")
        print("")
        
        start_time = datetime.now()
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Check if service is up
            try:
                health = await client.get(f"{self.base_url}/health")
                health.raise_for_status()
                print("✅ Service is healthy\n")
            except Exception as e:
                print(f"❌ Service is not reachable: {e}")
                return
            
            # Run requests in batches
            batch_size = concurrent
            num_batches = (total_requests + batch_size - 1) // batch_size
            
            for batch_num in range(num_batches):
                batch_start = batch_num * batch_size
                batch_end = min(batch_start + batch_size, total_requests)
                batch_count = batch_end - batch_start
                
                # Create tasks for this batch
                tasks = [self.run_single_request(client) for _ in range(batch_count)]
                
                # Execute batch
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                self.results["total"] = batch_end
                
                # Progress update
                progress = (batch_end / total_requests) * 100
                print(f"Progress: {batch_end}/{total_requests} ({progress:.1f}%) - "
                      f"Success: {self.results['success']}, Errors: {self.results['errors']}")
                
                # Small delay between batches
                if batch_num < num_batches - 1:
                    await asyncio.sleep(0.1)
        
        # Final results
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "="*60)
        print("📊 Load Test Results")
        print("="*60)
        print(f"Total Requests:  {self.results['total']}")
        print(f"Successful:      {self.results['success']} ({self.results['success']/self.results['total']*100:.1f}%)")
        print(f"Errors:          {self.results['errors']} ({self.results['errors']/self.results['total']*100:.1f}%)")
        print(f"Duration:        {duration:.2f} seconds")
        print(f"Requests/sec:    {self.results['total']/duration:.2f}")
        print("="*60)
        print("\n✅ Telemetry data should now be visible in Elastic!")
        print("   Use MCP workflows to query traces, metrics, and logs.")


async def main():
    parser = argparse.ArgumentParser(description="Load test for Mastercard Demo API")
    parser.add_argument("--requests", type=int, default=50, help="Total number of requests (default: 50)")
    parser.add_argument("--concurrent", type=int, default=10, help="Concurrent requests (default: 10)")
    parser.add_argument("--url", type=str, default="http://localhost:8000", help="Base URL (default: http://localhost:8000)")
    
    args = parser.parse_args()
    
    tester = LoadTester(base_url=args.url)
    await tester.run_load_test(args.requests, args.concurrent)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Load test interrupted by user")
        sys.exit(0)

