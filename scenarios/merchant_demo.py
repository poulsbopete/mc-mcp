"""
Merchant discovery scenario - simulates merchant search and location services.
This generates realistic traces for merchant-related workflows.
"""
import asyncio
import httpx
import random
from datetime import datetime


async def merchant_scenario():
    """
    Simulate merchant discovery workflow:
    1. Search for different types of merchants
    2. Get detailed information
    3. Track popular locations
    """
    base_url = "http://localhost:8000"
    
    print("🏪 Merchant Discovery Scenario")
    print("="*60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("")
    
    # Different search scenarios
    searches = [
        {"query": "coffee", "location": "San Francisco"},
        {"query": "restaurant", "location": "New York"},
        {"query": "gas station", "location": "Los Angeles"},
        {"query": "pharmacy", "location": "Chicago"},
        {"query": "grocery", "location": "Houston"}
    ]
    
    # Coordinates for cities (for demo)
    locations = {
        "San Francisco": (37.7749, -122.4194),
        "New York": (40.7128, -74.0060),
        "Los Angeles": (34.0522, -118.2437),
        "Chicago": (41.8781, -87.6298),
        "Houston": (29.7604, -95.3698)
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for i, search in enumerate(searches, 1):
            lat, lon = locations[search["location"]]
            
            print(f"{i}️⃣  Searching for '{search['query']}' near {search['location']}...")
            
            try:
                response = await client.get(
                    f"{base_url}/api/merchant/locate",
                    params={
                        "query": search["query"],
                        "latitude": lat,
                        "longitude": lon,
                        "radius": random.randint(3, 10)
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                merchants = data['merchants']
                print(f"   ✅ Found {len(merchants)} {search['query']} locations")
                
                # Show top 3 closest merchants
                sorted_merchants = sorted(merchants, key=lambda x: x['distance'])[:3]
                print("   Closest locations:")
                for m in sorted_merchants:
                    print(f"      - {m['name']}: {m['distance']} mi away (⭐ {m['rating']})")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            await asyncio.sleep(1.5)
    
    print("\n" + "="*60)
    print("✅ Merchant discovery scenario completed!")
    print("📊 Check Elastic for merchant search traces")
    print("")


if __name__ == "__main__":
    try:
        asyncio.run(merchant_scenario())
    except KeyboardInterrupt:
        print("\n\n⚠️  Scenario interrupted")

